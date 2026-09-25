"""El 'plano': el tablero de Conway donde conviven las entidades LER.

Ninguna entidad accede a otra directamente: solo ven glifos proyectados
por vecinas y reciben de vuelta texto hidratado. La cognición (si surge)
es propiedad del plano, no de ninguna entidad.

Reglas tipo Conway, pero semánticas:
  1. NACIMIENTO  — dos entidades compatibles pueden fusionarse (∘) si el
                   resultado pasa la validación del guarda.
  2. SUPERVIVENCIA — una entidad que no es interpretada durante N ciclos
                     pierde coherencia y muere (se archiva, no se borra).
  3. MUTACIÓN    — con probabilidad ε, un glifo se reemplaza por otro del
                     mismo nivel, generando variación para la selección.
  4. SELECCIÓN   — la fitness NO la define el autor: es la capacidad de la
                   entidad de generar respuestas coherentes en el sustrato
                   (medida, no declarada).
"""
from __future__ import annotations

import random
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

from core.llm.base import Sustrato
from core.soma import Propuesta, Soma


@dataclass
class Cuerpo:
    """Entidad textualizada: lo único que ve el sustrato."""
    id: str
    glifos: List[str]
    semilla: str                      # instrucción/axiomas hidratables
    energia: float = 1.0              # presupuesto simbólico (recurso escaso)
    edad: int = 0
    fitness_ema: float = 0.0          # media móvil de coherencia medida
    viva: bool = True
    especialidad: str = ""            # p.ej. "codigo", "auditoria": habilita propuesta somática
    historial: List[str] = field(default_factory=list)  # memoria episódica (texto hidratado)

    def proyectar(self, vecinos: List["Cuerpo"]) -> str:
        """Los sentidos del organismo: self + glifos de vecinas + entorno."""
        vs = " ".join(f"[{v.id}:{''.join(v.glifos)}]" for v in vecinos[:3])
        return f"{self.semilla}\nGLIFOS:{''.join(self.glifos)}\nVECINOS:{vs}"


@dataclass
class Plano:
    sustrato: Sustrato
    cuerpos: Dict[str, Cuerpo] = field(default_factory=dict)
    rng: random.Random = field(default_factory=lambda: random.Random(42))
    umbral_coherencia: float = 0.5
    costo_hidratacion: float = 0.05
    epsilon_mutacion: float = 0.1
    alfabeto: List[str] = field(default_factory=lambda: list("Δ⊗¬∞→⇆∘·+"))
    log: List[dict] = field(default_factory=list)
    tick: int = 0
    soma: Optional[Soma] = None       # tejido editable; None = genoma fijo del autor
    _fitness_antes: Dict[str, float] = field(default_factory=dict)

    def __post_init__(self):
        if self.soma is None:
            return
        # el plano lee sus parametros VIVOS desde el soma (defaults = genoma)
        self.soma.defaults.setdefault("umbral_coherencia", self.umbral_coherencia)
        self.soma.defaults.setdefault("epsilon_mutacion", self.epsilon_mutacion)
        self.soma.defaults.setdefault("costo_hidratacion", self.costo_hidratacion)

    def _param(self, nombre: str, fallback: float) -> float:
        return self.soma.get(nombre) if self.soma else fallback

    def poblar(self, cuerpos: List[Cuerpo]) -> None:
        for c in cuerpos:
            self.cuerpos[c.id] = c

    def _evaluar(self, cuerpo: Cuerpo, respuesta: str) -> float:
        """Coherencia medida, no declarada: ¿la respuesta reproduce glifos
        propios o de vecinas? Proxy trivial; sustituible por ReflexivityTestV2
        o por un LLM-juez cuando haya presupuesto."""
        if not respuesta:
            return 0.0
        presentes = sum(1 for g in cuerpo.glifos if g in respuesta)
        densidad = presentes / max(1, len(cuerpo.glifos))
        longitud = min(1.0, len(respuesta) / 200)
        return 0.7 * densidad + 0.3 * longitud

    def paso(self) -> dict:
        """Un tick del autómata. Devuelve resumen del ciclo."""
        self.tick += 1
        umbral = self._param("umbral_coherencia", self.umbral_coherencia)
        costo = self._param("costo_hidratacion", self.costo_hidratacion)
        epsilon = self._param("epsilon_mutacion", self.epsilon_mutacion)
        vivos = [c for c in self.cuerpos.values() if c.viva]
        eventos = []

        # 1. CADA CUERPO PERCIBE → HIDRATA → ACTÚA
        for c in vivos:
            if c.energia <= 0:
                c.viva = False
                eventos.append(("inanicion", c.id))
                continue
            vecinos = [v for v in vivos if v.id != c.id]
            prompt = c.proyectar(vecinos)
            try:
                resp = self.sustrato.hidratar(prompt)
            except Exception as e:  # el sustrato puede fallar; la vida sigue
                eventos.append(("fallo_sustrato", c.id, str(e)))
                continue
            # memoria episódica: lo hidratado se escribe de vuelta en la historia
            c.historial.append(resp[:280])
            c.historial = c.historial[-5:]
            score = self._evaluar(c, resp)
            c.fitness_ema = 0.8 * c.fitness_ema + 0.2 * score
            c.energia -= costo
            c.edad += 1
            if score >= umbral:
                c.energia = min(2.0, c.energia + score * 0.1)  # la coherencia alimenta
            eventos.append(("hidratacion", c.id, round(score, 3)))

        # 1b. PROPUESTA SOMÁTICA: las especializadas repiensan la maquinaria
        eventos.extend(self._proponer(vivos))

        # 2. NACIMIENTO: fusión ∘ de las dos más aptas adyacentes
        ranked = sorted([c for c in vivos if c.viva], key=lambda x: -x.fitness_ema)
        if len(ranked) >= 2 and self.rng.random() < 0.3:
            a, b = ranked[0], ranked[1]
            hijo = Cuerpo(
                id=f"{a.id}∘{b.id}@{sum(c.edad for c in self.cuerpos.values())}",
                glifos=list(dict.fromkeys(a.glifos + b.glifos))[:6],
                semilla=a.semilla if a.fitness_ema >= b.fitness_ema else b.semilla,
                energia=0.5,
                especialidad=a.especialidad or b.especialidad,
            )
            self.cuerpos[hijo.id] = hijo
            eventos.append(("nacimiento", hijo.id))

        # 3. MUTACIÓN ε
        for c in ranked[:3]:
            if c.viva and self.rng.random() < epsilon and c.glifos:
                i = self.rng.randrange(len(c.glifos))
                viejo = c.glifos[i]
                c.glifos[i] = self.rng.choice(self.alfabeto)
                eventos.append(("mutacion", c.id, viejo, c.glifos[i]))

        # 4. MUERTE: sin interpretación sostenida
        for c in self.cuerpos.values():
            if c.viva and c.edad > 20 and c.fitness_ema < umbral / 2:
                c.viva = False
                eventos.append(("extincion", c.id))

        resumen = {"tick": self.tick,
                   "poblacion": sum(1 for c in self.cuerpos.values() if c.viva),
                   "eventos": eventos}
        self.log.append(resumen)
        return resumen

    # ---- escisión del sustrato: capacidad evolucionable ------------------ #
    def _fitness_global(self) -> float:
        vivos = [c for c in self.cuerpos.values() if c.viva]
        if not vivos:
            return 0.0
        return sum(c.fitness_ema for c in vivos) / len(vivos)

    def _proponer(self, vivos: List[Cuerpo]) -> List[tuple]:
        """Las entidades con especialidad emiten propuestas sobre el soma.

        No es inteligencia programada: cada especialista deriva su propuesta
        de SU estado medido (fitness, energía, ruido histórico). La guarda
        (whitelist + rangos) filtra; la verificación post-tick revierte si la
        mutación somática derrumba el fitness global. Si una propuesta ayuda,
        los linajes que la heredan prosperan: selección sobre la maquinaria.
        """
        eventos: List[tuple] = []
        if self.soma is None:
            return eventos

        # cuarentena: tras aplicar, dejamos pasar 3 ticks antes de juzgar
        pendientes = [p for p in self.soma.historial
                      if p.estado == "activa" and getattr(p, "_aplicada_en", None) is not None
                      and self.tick - p._aplicada_en >= 3]
        for p in pendientes:
            actual = self._fitness_global()
            antes = self._fitness_antes.get(p.canal, actual)
            if antes > 0 and (antes - actual) / antes > 0.25:
                self.soma.revertir(p.canal, motivo="caida_fitness")
                eventos.append(("reversion", p.canal, p.proponente))
            else:
                p._aplicada_en = None  # consolidada: ya no se re-juzga
                eventos.append(("consolidacion", p.canal, p.valor))

        for c in vivos:
            if not c.especialidad or c.energia < 0.3:
                continue  # proponer cuesta: solo organismos con excedente
            canal, valor, por_que = self._derivar_propuesta(c)
            if canal is None:
                continue
            activa = self.soma.activas.get(canal)
            if activa is not None and abs(activa.valor - valor) < 1e-9:
                continue  # el soma ya expresa esta voluntad: no spam de propuestas
            prop = Propuesta(id=f"{c.id}@{self.tick}", proponente=c.id,
                             canal=canal, valor=valor, justificacion=por_que)
            prop = self.soma.postular(prop)
            if prop.estado == "pendiente":
                activada = self.soma.aplicar(prop)
                if activada:
                    prop._aplicada_en = self.tick
                    self._fitness_antes[canal] = self._fitness_global()
                    eventos.append(("propuesta_somatica", c.id, canal, prop.valor))
                else:
                    eventos.append(("propuesta_rechazada", c.id, canal))
        return eventos

    def _derivar_propuesta(self, c: Cuerpo):
        """La propuesta emerge del estado medido del cuerpo, no de un guión."""
        umbral = self._param("umbral_coherencia", self.umbral_coherencia)
        eps = self._param("epsilon_mutacion", self.epsilon_mutacion)
        espec = c.especialidad.lower()
        # "codigo" como token aparte (pycodex -> codigo) o substring obvio
        tokens = set(espec.replace("_", " ").replace("-", " ").split())
        es_codigo = ("codigo" in tokens or "code" in tokens or "codeinsight" in tokens
                     or "code" in espec.replace(" ", ""))
        es_auditor = ("auditoria" in tokens or "auditor" in tokens or "audit" in espec)
        if es_codigo:
            # especialista en código: detecta ruido → sube exigencia de coherencia
            if c.fitness_ema < umbral + 0.15:
                return ("umbral_coherencia", min(0.9, umbral + 0.05),
                        f"{c.glifos} ruido→Δexigencia")
        if es_auditor:
            # auditor: población derrocha energía → presión metabólica
            media_e = sum(v.energia for v in self.cuerpos.values() if v.viva) / max(
                1, sum(1 for v in self.cuerpos.values() if v.viva))
            if media_e > 1.2:
                return ("costo_hidratacion", min(0.3, self._param(
                    "costo_hidratacion", self.costo_hidratacion) + 0.02),
                    "⟁ holgancia→¬energía")
        if "learn" in espec or "aprendiz" in espec:
            # aprendiz: estancamiento → más variabilidad simbólica
            if eps < 0.4 and c.fitness_ema < 0.3:
                return ("epsilon_mutacion", min(0.5, eps + 0.05),
                        "∘+ estancamiento→ε↑")
        return (None, None, "")

    def evolucionar(self, n: int) -> List[dict]:
        return [self.paso() for _ in range(n)]

    def cementerio(self, path: Path) -> None:
        """La historia no se borra: se archiva (ciclo vital LER)."""
        muertos = [c.__dict__ for c in self.cuerpos.values() if not c.viva]
        path.write_text(json.dumps(muertos, ensure_ascii=False, indent=2), encoding="utf-8")
