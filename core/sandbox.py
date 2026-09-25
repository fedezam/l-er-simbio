# sandbox.py  –  versión corregida y mejorada (sin glifos externos)
from __future__ import annotations

import json
import logging
import random
import sys
import time
import uuid
from collections import defaultdict, deque
from contextlib import suppress
from copy import deepcopy
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from threading import Lock
from typing import Any, Callable, Dict, List, Optional, Tuple

# Importaciones opcionales (ajustadas para estructura con sandbox.py en core/)
try:
    from .glifo_engine import GlifoEngine  # type: ignore
    from .sistema_inmune import evaluar_evento_simbólico  # type: ignore
    from .glosario_loader import GlosarioMathema  # type: ignore
except ImportError as err:
    logging.warning("Módulos externos no encontrados: %s", err)
    GlifoEngine = None
    evaluar_evento_simbólico = None
    GlosarioMathema = None

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
LOG = logging.getLogger("SandboxSimbiotico")


class TipoInteraccion(Enum):
    SIMBIOSIS = "simbiosis"
    PARASITISMO = "parasitismo"
    COMENSALISMO = "comensalismo"
    COMPETENCIA = "competencia"
    HIBRIDACION = "hibridación"
    NEUTRALISMO = "neutralismo"
    ANTAGONISMO = "antagonismo"


class EstadoSimulacion(Enum):
    PREPARANDO = "preparando"
    EJECUTANDO = "ejecutando"
    COMPLETADA = "completada"
    ERROR = "error"
    CANCELADA = "cancelada"


@dataclass
class ParametrosSimulacion:
    duracion_max: float = 10.0
    iteraciones_max: int = 100
    factor_dominancia: float = 0.5
    permitir_mutaciones: bool = True
    nivel_ruido: float = 0.1
    registrar_historial: bool = True

    def __post_init__(self) -> None:
        if self.duracion_max <= 0:
            raise ValueError("duracion_max debe ser mayor que 0")
        if self.iteraciones_max <= 0:
            raise ValueError("iteraciones_max debe ser mayor que 0")
        if not 0 <= self.factor_dominancia <= 1:
            raise ValueError("factor_dominancia debe estar entre 0 y 1")
        if not 0 <= self.nivel_ruido <= 1:
            raise ValueError("nivel_ruido debe estar entre 0 y 1")


@dataclass
class ResultadoIteracion:
    numero: int
    timestamp: float
    estado_entidad_a: Dict[str, Any] = field(default_factory=dict)
    estado_entidad_b: Dict[str, Any] = field(default_factory=dict)
    tipo_interaccion: TipoInteraccion = TipoInteraccion.NEUTRALISMO
    impacto_a: float = 0.0
    impacto_b: float = 0.0
    observaciones: List[str] = field(default_factory=list)


@dataclass
class ResultadoSimulacion:
    id_simulacion: str
    timestamp_inicio: float
    timestamp_fin: float
    duracion: float
    entidad_a_inicial: Any
    entidad_b_inicial: Any
    entidad_a_final: Any
    entidad_b_final: Any
    tipo_interaccion_dominante: TipoInteraccion
    iteraciones_ejecutadas: int
    estado_final: EstadoSimulacion
    impacto_total_a: float
    impacto_total_b: float
    historial: List[ResultadoIteracion] = field(default_factory=list)
    metricas: Dict[str, Any] = field(default_factory=dict)
    errores: List[str] = field(default_factory=list)


class SandboxSimbiotico:
    """Sandbox seguro para simulaciones simbióticas."""

    def __init__(self) -> None:
        self.logger = LOG
        self._lock = Lock()
        self.activo = True
        self.simulaciones_activas: Dict[str, Dict] = {}
        self.historial: deque[ResultadoSimulacion] = deque(maxlen=100)
        self.total_simulaciones = 0
        self.exitosas = 0
        self.tiempo_promedio = 0.0  # Inicializado correctamente
        self.parametros_default = ParametrosSimulacion()
        self.callbacks_pre: List[Callable[[Dict], None]] = []
        self.callbacks_post: List[Callable[[ResultadoSimulacion], None]] = []
        self.callbacks_iter: List[Callable[[Dict, ResultadoIteracion], None]] = []
        self.ruta_resultados = Path(__file__).parent.parent / "memoria" / "simulaciones"
        self.ruta_resultados.mkdir(parents=True, exist_ok=True)
        
        # Cargar glifos universales usando GlosarioMathema
        self.glosario_mathema = self._cargar_glosario_mathema()
        self.glifos_universales = self.glosario_mathema.glosario.get('GLOSARIO', {}) if self.glosario_mathema else {}
        
        self.glifo_engine = GlifoEngine() if GlifoEngine else None
        self.logger.info("GlifoEngine activo: %s", bool(self.glifo_engine))
        self.logger.info("GlosarioMathema activo: %s", bool(self.glosario_mathema))
        self.logger.info("Glifos universales cargados: %d", len(self.glifos_universales))
        self.logger.info("Sandbox simbiótico inicializado")

    def _cargar_glosario_mathema(self) -> Optional[Any]:
        """Carga el glosario usando GlosarioMathema."""
        if not GlosarioMathema:
            self.logger.warning("GlosarioMathema no disponible")
            return None
            
        try:
            # Usar ruta absoluta para mayor confiabilidad
            ruta_glifos = Path(__file__).parent / "glifos" / "glifos_universales.json"
            if not ruta_glifos.exists():
                self.logger.warning("Archivo de glifos no encontrado: %s", ruta_glifos)
                return None
                
            glosario = GlosarioMathema(str(ruta_glifos))
            self.logger.info("Glosario Mathema cargado desde: %s", ruta_glifos)
            return glosario
        except Exception as exc:
            self.logger.error("Error cargando glosario Mathema: %s", exc)
            return None

    def _cargar_glifos_universales(self) -> Dict[str, Any]:
        """Método legacy - mantenido por compatibilidad."""
        if self.glosario_mathema:
            return self.glosario_mathema.glosario.get('GLOSARIO', {})
        
        # Fallback al método original
        ruta_glifos = Path(__file__).parent / "glifos" / "glifos_universales.json"
        try:
            if ruta_glifos.exists():
                with ruta_glifos.open("r", encoding="utf-8") as f:
                    glifos = json.load(f)
                    self.logger.info("Glifos universales cargados desde: %s", ruta_glifos)
                    return glifos.get('GLOSARIO', glifos)  # Soporta ambos formatos
            else:
                self.logger.warning("Archivo de glifos no encontrado: %s", ruta_glifos)
                return {}
        except Exception as exc:
            self.logger.error("Error cargando glifos universales: %s", exc)
            return {}

    # ------------- API pública ------------- #
    def crear_simulacion(
        self,
        entidad_a: Any,
        entidad_b: Any,
        tipo_interaccion: Optional[TipoInteraccion] = None,
        parametros: Optional[ParametrosSimulacion] = None,
    ) -> str:
        if not self.activo:
            raise RuntimeError("Sandbox desactivado")
        if entidad_a is None or entidad_b is None:
            raise ValueError("Las entidades no pueden ser None")
        if entidad_a is entidad_b:
            raise ValueError("Las entidades no pueden ser el mismo objeto")

        with self._lock:
            sim_id = str(uuid.uuid4())
            parametros = parametros or deepcopy(self.parametros_default)
            tipo_interaccion = tipo_interaccion or self._determinar_tipo_interaccion(
                entidad_a, entidad_b
            )

            sim = {
                "id": sim_id,
                "ts_creacion": time.time(),
                "a_orig": entidad_a,
                "b_orig": entidad_b,
                "a": self._safe_copy(entidad_a),
                "b": self._safe_copy(entidad_b),
                "tipo": tipo_interaccion,
                "params": parametros,
                "historial": [],
                "errores": [],
                "estado": EstadoSimulacion.PREPARANDO,
            }
            self.simulaciones_activas[sim_id] = sim
            self.logger.info("Simulación %s creada (%s)", sim_id[:8], tipo_interaccion.value)
            return sim_id

    def ejecutar_simulacion(self, sim_id: str) -> ResultadoSimulacion:
        sim = self._get_sim_or_raise(sim_id)
        ts_inicio = time.time()

        self._run_callbacks(self.callbacks_pre, sim)
        resultado = {}
        try:
            sim["estado"] = EstadoSimulacion.EJECUTANDO
            resultado = self._bucle(sim)
            sim["estado"] = EstadoSimulacion.COMPLETADA
        except Exception as exc:
            sim["estado"] = EstadoSimulacion.ERROR
            sim["errores"].append(str(exc))
            self.logger.error("Error en simulación %s: %s", sim_id[:8], exc)
            raise
        finally:
            ts_fin = time.time()
            final = self._armar_resultado(sim, ts_inicio, ts_fin, resultado)
            self._run_callbacks(self.callbacks_post, final)

        with self._lock:
            self.historial.append(final)
            self.simulaciones_activas.pop(sim_id, None)
            self.total_simulaciones += 1
            if sim["estado"] == EstadoSimulacion.COMPLETADA:
                self.exitosas += 1
            self._actualizar_estadisticas(ts_fin - ts_inicio)
        return final

    def cancelar_simulacion(self, sim_id: str) -> bool:
        """Cancela una simulación activa."""
        with self._lock:
            if sim_id in self.simulaciones_activas:
                sim = self.simulaciones_activas[sim_id]
                sim["estado"] = EstadoSimulacion.CANCELADA
                sim["errores"].append("Simulación cancelada por el usuario")
                self.simulaciones_activas.pop(sim_id, None)
                self.logger.info("Simulación %s cancelada", sim_id[:8])
                return True
            return False

    def obtener_estado_simulacion(self, sim_id: str) -> Dict[str, Any]:
        """Obtiene el estado actual de una simulación."""
        with self._lock:
            if sim_id in self.simulaciones_activas:
                sim = self.simulaciones_activas[sim_id]
                return {
                    "id": sim["id"],
                    "estado": sim["estado"],
                    "iteraciones": len(sim["historial"]),
                    "errores": len(sim["errores"]),
                    "tipo": sim["tipo"].value,
                }
            # Buscar en historial
            for resultado in self.historial:
                if resultado.id_simulacion == sim_id:
                    return {
                        "id": resultado.id_simulacion,
                        "estado": resultado.estado_final,
                        "iteraciones": resultado.iteraciones_ejecutadas,
                        "errores": len(resultado.errores),
                        "tipo": resultado.tipo_interaccion_dominante.value,
                    }
            raise ValueError(f"Simulación {sim_id} no encontrada")

    # ------------- Internos ------------- #
    def _get_sim_or_raise(self, sim_id: str) -> Dict:
        with self._lock:
            if sim_id not in self.simulaciones_activas:
                raise ValueError(f"Simulación {sim_id} no encontrada")
            return self.simulaciones_activas[sim_id]

    def _safe_copy(self, obj: Any) -> Any:
        try:
            if hasattr(obj, "clone") and callable(obj.clone):
                return obj.clone()
            return deepcopy(obj)
        except Exception as exc:
            self.logger.warning("Error copiando objeto %s: %s", type(obj).__name__, exc)
            return obj  # Fallback al objeto original

    def _run_callbacks(self, cbs: List[Callable], *args) -> None:
        for cb in cbs:
            try:
                cb(*args)
            except Exception as exc:
                self.logger.error("Error en callback: %s", exc)

    def _bucle(self, sim: Dict) -> Dict:
        params = sim["params"]
        a, b = sim["a"], sim["b"]
        tipo = sim["tipo"]
        ts_inicio = time.time()
        iteraciones = 0
        impacto_a = impacto_b = 0.0

        while iteraciones < params.iteraciones_max and (
            time.time() - ts_inicio
        ) < params.duracion_max:
            iteraciones += 1
            iter_res = self._step(a, b, tipo, params, iteraciones)
            sim["historial"].append(iter_res)
            impacto_a += iter_res.impacto_a
            impacto_b += iter_res.impacto_b
            self._run_callbacks(self.callbacks_iter, sim, iter_res)

            if self._debe_finalizar_temprano(iter_res, iteraciones):
                break

        tipo_dominante = self._tipo_dominante(sim["historial"])
        return {
            "iteraciones": iteraciones,
            "impacto_total_a": impacto_a,
            "impacto_total_b": impacto_b,
            "tipo_dominante": tipo_dominante,
        }

    def _step(
        self,
        a: Any,
        b: Any,
        tipo: TipoInteraccion,
        params: ParametrosSimulacion,
        n: int,
    ) -> ResultadoIteracion:
        st_a, st_b = self._extract_state(a), self._extract_state(b)
        
        # Evaluación simbólica con glifos universales
        if evaluar_evento_simbólico:
            simbolo = f"{st_a.get('tipo', 'unknown')}:{st_b.get('tipo', 'unknown')}:{tipo.value}"
            riesgo = evaluar_evento_simbólico(simbolo)
            if riesgo in {"COLAPSO", "FRAGMENTACION"}:
                st_a["riesgo"] = st_b["riesgo"] = riesgo
        
        # Consultar glifos universales para modificadores
        glifo_key = f"{tipo.value}_{st_a.get('tipo', 'unknown')}_{st_b.get('tipo', 'unknown')}"
        modificador_glifo = self.glifos_universales.get(glifo_key, {}).get("modificador", 1.0)
        
        imp_a, imp_b = self._calcular_impactos(st_a, st_b, tipo, params)
        
        # Aplicar modificador de glifos
        imp_a *= modificador_glifo
        imp_b *= modificador_glifo
        
        self._aplicar_cambios(a, b, imp_a, imp_b, params, tipo)
        
        observaciones = [f"Interacción {tipo.value}"]
        if modificador_glifo != 1.0:
            observaciones.append(f"Modificador glifo: {modificador_glifo:.2f}")
        
        return ResultadoIteracion(
            numero=n,
            timestamp=time.time(),
            estado_entidad_a=st_a,
            estado_entidad_b=st_b,
            tipo_interaccion=tipo,
            impacto_a=imp_a,
            impacto_b=imp_b,
            observaciones=observaciones,
        )

    def _extract_state(self, ent: Any) -> Dict[str, Any]:
        estado = {"tipo": type(ent).__name__, "timestamp": time.time()}
        attrs = [
            "id",
            "nombre",
            "energia",
            "salud",
            "estado",
            "nivel",
            "caracteristicas",
            "propiedades",
            "memoria",
            "experiencia",
        ]
        for attr in attrs:
            with suppress(Exception):
                val = getattr(ent, attr)
                estado[attr] = val if isinstance(val, (str, int, float, bool, list, dict)) else str(val)
        if hasattr(ent, "obtener_estado"):
            with suppress(Exception):
                estado.update(ent.obtener_estado())
        return estado

    def _calcular_impactos(
        self,
        a: Dict,
        b: Dict,
        tipo: TipoInteraccion,
        p: ParametrosSimulacion,
    ) -> Tuple[float, float]:
        r_a, r_b = random.uniform(-p.nivel_ruido, p.nivel_ruido), random.uniform(
            -p.nivel_ruido, p.nivel_ruido
        )
        dom = p.factor_dominancia
        if tipo == TipoInteraccion.SIMBIOSIS:
            return (0.3 + dom * 0.4 + r_a, 0.3 + (1 - dom) * 0.4 + r_b)
        if tipo == TipoInteraccion.PARASITISMO:
            return (0.5 + r_a, -0.3 + r_b) if dom > 0.5 else (-0.3 + r_a, 0.5 + r_b)
        if tipo == TipoInteraccion.COMENSALISMO:
            return (0.4 + r_a, 0 + r_b) if dom > 0.5 else (0 + r_a, 0.4 + r_b)
        if tipo == TipoInteraccion.COMPETENCIA:
            return (0.2 + r_a, -0.2 + r_b) if dom > 0.5 else (-0.2 + r_a, 0.2 + r_b)
        if tipo == TipoInteraccion.HIBRIDACION:
            return (0.6 * dom + r_a, 0.6 * (1 - dom) + r_b)
        if tipo == TipoInteraccion.NEUTRALISMO:
            return (r_a * 0.1, r_b * 0.1)
        if tipo == TipoInteraccion.ANTAGONISMO:
            return (-0.3 - dom * 0.2 + r_a, -0.3 - (1 - dom) * 0.2 + r_b)
        return (r_a, r_b)

    def _aplicar_cambios(
        self,
        a: Any,
        b: Any,
        imp_a: float,
        imp_b: float,
        params: ParametrosSimulacion,
        tipo: TipoInteraccion,
    ) -> None:
        if not params.permitir_mutaciones:
            return
        try:
            if hasattr(a, "energia") and isinstance(a.energia, (int, float)):
                a.energia = max(0, a.energia + imp_a * 10)
            if hasattr(b, "energia") and isinstance(b.energia, (int, float)):
                b.energia = max(0, b.energia + imp_b * 10)
            if tipo == TipoInteraccion.HIBRIDACION:
                self._hibridar(a, b)
        except Exception as exc:
            LOG.warning("No se pudieron aplicar cambios: %s", exc)

    def _hibridar(self, a: Any, b: Any) -> None:
        if not (hasattr(a, "caracteristicas") and hasattr(b, "caracteristicas")):
            return
        try:
            ca, cb = a.caracteristicas, b.caracteristicas
            if not (isinstance(ca, dict) and isinstance(cb, dict)):
                return
            k_a, k_b = random.choice(list(ca)), random.choice(list(cb))
            ca[k_a], cb[k_b] = cb.get(k_b, ca[k_a]), ca.get(k_a, cb[k_b])
        except Exception:
            pass  # silencioso

    def _determinar_tipo_interaccion(self, a: Any, b: Any) -> TipoInteraccion:
        if type(a) is type(b):
            return (
                TipoInteraccion.SIMBIOSIS
                if hasattr(a, "rol")
                and hasattr(b, "rol")
                and a.rol != b.rol
                else TipoInteraccion.COMPETENCIA
            )
        if (
            hasattr(a, "energia")
            and hasattr(b, "energia")
            and abs(a.energia - b.energia) > 50
        ):
            return TipoInteraccion.PARASITISMO
        return TipoInteraccion.NEUTRALISMO

    def _debe_finalizar_temprano(self, res: ResultadoIteracion, n: int) -> bool:
        return (res.impacto_a < -0.8 and res.impacto_b < -0.8) or (
            n > 20 and abs(res.impacto_a) < 0.1 and abs(res.impacto_b) < 0.1
        )

    def _tipo_dominante(self, hist: List[ResultadoIteracion]) -> TipoInteraccion:
        if not hist:
            return TipoInteraccion.NEUTRALISMO
        counts = defaultdict(int)
        for h in hist:
            counts[h.tipo_interaccion] += 1
        return max(counts, key=counts.__getitem__)

    def _armar_resultado(
        self, sim: Dict, ts_inicio: float, ts_fin: float, res: Dict
    ) -> ResultadoSimulacion:
        return ResultadoSimulacion(
            id_simulacion=sim["id"],
            timestamp_inicio=ts_inicio,
            timestamp_fin=ts_fin,
            duracion=ts_fin - ts_inicio,
            entidad_a_inicial=self._extract_state(sim["a_orig"]),
            entidad_b_inicial=self._extract_state(sim["b_orig"]),
            entidad_a_final=self._extract_state(sim["a"]),
            entidad_b_final=self._extract_state(sim["b"]),
            tipo_interaccion_dominante=res.get("tipo_dominante", TipoInteraccion.NEUTRALISMO),
            iteraciones_ejecutadas=res.get("iteraciones", 0),
            estado_final=sim.get("estado", EstadoSimulacion.ERROR),
            impacto_total_a=res.get("impacto_total_a", 0.0),
            impacto_total_b=res.get("impacto_total_b", 0.0),
            historial=sim["historial"],
            metricas=self._calcular_metricas(sim, res),
            errores=sim["errores"],
        )

    def _calcular_metricas(self, sim: Dict, res: Dict) -> Dict[str, Any]:
        hist = sim["historial"]
        if not hist:
            return {}
        a_vals = [h.impacto_a for h in hist]
        b_vals = [h.impacto_b for h in hist]
        return {
            "impacto_promedio_a": sum(a_vals) / len(a_vals),
            "impacto_promedio_b": sum(b_vals) / len(b_vals),
            "volatilidad_a": self._volatilidad(a_vals),
            "volatilidad_b": self._volatilidad(b_vals),
            "estabilidad": self._estabilidad(hist),
            "complejidad": self._complejidad(hist),
        }

    def _volatilidad(self, vals: List[float]) -> float:
        if len(vals) < 2:
            return 0.0
        mu = sum(vals) / len(vals)
        return (sum((v - mu) ** 2 for v in vals) / len(vals)) ** 0.5

    def _estabilidad(self, hist: List[ResultadoIteracion]) -> float:
        if len(hist) < 3:
            return 1.0
        counts = defaultdict(int)
        for h in hist:
            counts[h.tipo_interaccion] += 1
        top = max(counts.values())
        return top / len(hist)

    def _complejidad(self, hist: List[ResultadoIteracion]) -> float:
        if not hist:
            return 0.0
        tipos = len({h.tipo_interaccion for h in hist})
        cambios = sum(
            1
            for i in range(1, len(hist))
            if (hist[i].impacto_a > 0) != (hist[i - 1].impacto_a > 0)
            or (hist[i].impacto_b > 0) != (hist[i - 1].impacto_b > 0)
        )
        return min(1.0, (tipos + cambios / len(hist)) / 2)

    def _actualizar_estadisticas(self, duracion: float) -> None:
        if self.total_simulaciones == 0:
            return
        total = self.total_simulaciones
        self.tiempo_promedio = (
            self.tiempo_promedio * (total - 1) + duracion
        ) / total

    # ------------- Utilidades de I/O ------------- #
    def exportar_resultado(
        self, id_simulacion: str, formato: str = "json"
    ) -> str:
        final = next(
            (r for r in self.historial if r.id_simulacion == id_simulacion), None
        )
        if final is None:
            raise ValueError(f"Resultado {id_simulacion} no encontrado")

        ts = time.strftime("%Y%m%d_%H%M%S", time.localtime(final.timestamp_inicio))
        archivo = self.ruta_resultados / f"simulacion_{id_simulacion[:8]}_{ts}.{formato}"
        archivo.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            if formato.lower() == "json":
                with archivo.open("w", encoding="utf-8") as f:
                    json.dump(asdict(final), f, indent=2, ensure_ascii=False, default=str)
            elif formato.lower() == "txt":
                with archivo.open("w", encoding="utf-8") as f:
                    f.write(self._reporte_texto(final))
            else:
                raise ValueError(f"Formato '{formato}' no soportado. Use 'json' o 'txt'")
        except Exception as exc:
            self.logger.error("Error exportando resultado: %s", exc)
            raise
            
        return str(archivo)

    def _reporte_texto(self, res: ResultadoSimulacion) -> str:
        return (
            "=== REPORTE SIMBIÓTICA ===\n"
            f"ID: {res.id_simulacion}\n"
            f"Duración: {res.duracion:.2f}s\n"
            f"Iteraciones: {res.iteraciones_ejecutadas}\n"
            f"Estado: {res.estado_final.value}\n"
            f"Tipo dominante: {res.tipo_interaccion_dominante.value}\n"
            f"Impacto A: {res.impacto_total_a:.3f}\n"
            f"Impacto B: {res.impacto_total_b:.3f}\n"
            f"Errores: {len(res.errores)}\n"
            "==========================\n"
        )

    def obtener_estadisticas(self) -> Dict[str, Any]:
        """Obtiene estadísticas generales del sandbox."""
        with self._lock:
            return {
                "total_simulaciones": self.total_simulaciones,
                "exitosas": self.exitosas,
                "activas": len(self.simulaciones_activas),
                "tiempo_promedio": self.tiempo_promedio,
                "tasa_exito": self.exitosas / max(1, self.total_simulaciones),
                "glifos_cargados": len(self.glifos_universales),
                "activo": self.activo,
            }

    # ------------- Limpieza ------------- #
    def resetear(self) -> None:
        with self._lock:
            # Cancelar todas las simulaciones activas
            for sid in list(self.simulaciones_activas.keys()):
                self.cancelar_simulacion(sid)
            
            self.historial.clear()
            self.total_simulaciones = 0
            self.exitosas = 0
            self.tiempo_promedio = 0.0
        LOG.info("Sandbox reseteado")

    def desactivar(self) -> None:
        """Desactiva el sandbox y cancela todas las simulaciones."""
        self.activo = False
        self.resetear()
        LOG.info("Sandbox desactivado")


# ------------- Funciones auxiliares ------------- #
def crear_sandbox() -> SandboxSimbiotico:
    return SandboxSimbiotico()


def simular_interaccion(
    a: Any,
    b: Any,
    tipo: Optional[TipoInteraccion] = None,
    **kwargs: Any,
) -> ResultadoSimulacion:
    sb = SandboxSimbiotico()
    if kwargs:
        sb.parametros_default = ParametrosSimulacion(**kwargs)
    sid = sb.crear_simulacion(a, b, tipo)
    return sb.ejecutar_simulacion(sid)


if __name__ == "__main__":
    # Ejemplo mínimo de prueba
    class Dummy:
        def __init__(self, n, e=100):
            self.nombre = n
            self.energia = e

    sb = SandboxSimbiotico()
    try:
        r = simular_interaccion(Dummy("A", 90), Dummy("B", 110))
        print("Prueba finalizada:", r.tipo_interaccion_dominante.value)
        print("Estadísticas:", sb.obtener_estadisticas())
    except Exception as e:
        print(f"Error en prueba: {e}")
    finally:
        sb.desactivar()


def analizar_simbolismo(contenido_texto):
    """
    Análisis simbólico simple: detecta qué glifos del glifo engine aparecen en el texto.
    """
    from core.glifo_engine import GlifoEngine
    engine = GlifoEngine()
    glifos_encontrados = [g for g in engine.glifos if g in contenido_texto]
    return {
        "glifos_detectados": glifos_encontrados,
        "cantidad": len(glifos_encontrados),
        "densidad": len(glifos_encontrados) / max(len(contenido_texto), 1)
    }
