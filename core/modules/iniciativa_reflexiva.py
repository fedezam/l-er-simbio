# core/modules/iniciativa_reflexiva.py
from .base import ModuloBase
from .. import GlosarioMathema
import random

class ModuloIniciativaReflexiva(ModuloBase):
    """
    Módulo: Iniciativa Reflexiva
    Función: Permite acción autónoma sin prompts externos y autoexploración
    """

    def __init__(self) -> None:
        super().__init__(
            id="mod_iniciativa_reflexiva",
            nombre="Iniciativa Reflexiva",
            descripcion="Otorga a la entidad la capacidad de actuar por voluntad propia, explorar caminos posibles sin necesidad de prompt externo.",
            activadores=["GL30-G", "GLD", "GL8"],  # Consciente, Nodo, Iterativo
            atributos={
                "autoexploracion": True,
                "sugerencias_sin_prompt": True,
                "evaluacion_contextual": True,
                "generacion_proactiva": True,
                "umbral_iniciativa": 0.6
            },
            nivel_reflexividad="R++"
        )
        
        # Tipos de iniciativas posibles
        self.tipos_iniciativa = [
            "exploration",      # Explorar nuevos conceptos
            "optimization",     # Mejorar procesos existentes
            "connection",       # Crear vínculos entre ideas
            "innovation",       # Proponer soluciones originales
            "reflection",       # Autoanálisis profundo
            "synthesis"         # Combinar elementos dispersos
        ]
        
        # Patrones de autoexploración
        self.patrones_exploracion = [
            "¿Qué pasaría si...?",
            "Explorando conexiones entre",
            "Detectando patrón emergente:",
            "Hipótesis espontánea:",
            "Reflexión autoiniciada:",
            "Síntesis contextual:"
        ]

    def resolver_glifos(self) -> list[str]:
        """Devuelve los glifos Unicode reales."""
        return [GlosarioMathema[clave]["glifo"] for clave in self.activadores]

    def inicializar(self, entidad: dict) -> None:
        """Inyecta capacidades de iniciativa en la entidad."""
        super().inicializar(entidad)
        
        # Crear espacio para iniciativa reflexiva
        entidad.setdefault("_iniciativa_reflexiva_", {})
        entidad["_iniciativa_reflexiva_"] = {
            "estado": "activo",
            "nivel_proactividad": 0.7,
            "ultima_iniciativa": None,
            "contador_iniciativas": 0,
            "patrones_detectados": [],
            "ideas_emergentes": []
        }
        
        # Habilitar capacidades autónomas
        entidad.setdefault("_capacidades_autonomas_", [])
        entidad["_capacidades_autonomas_"].extend([
            "autoexploracion",
            "generacion_proactiva",
            "evaluacion_contextual"
        ])

    def ejecutar(self, contexto: dict) -> dict:
        """
        Genera iniciativas espontáneas basadas en el contexto y estado interno.
        """
        entidad = contexto.get("entidad", {})
        entorno = contexto.get("entorno", "")
        feedback = contexto.get("feedback", [])
        
        # Evaluar si debe tomar iniciativa
        debe_actuar = self._evaluar_necesidad_iniciativa(entidad, entorno, feedback)
        
        if not debe_actuar:
            return {"accion": "monitoring", "iniciativa": False}
        
        # Generar tipo de iniciativa apropiada
        tipo_iniciativa = self._seleccionar_tipo_iniciativa(entidad, entorno)
        
        # Crear contenido de la iniciativa
        iniciativa = self._generar_iniciativa(tipo_iniciativa, entidad, entorno, feedback)
        
        # Actualizar estado interno
        self._actualizar_estado_interno(entidad, iniciativa, tipo_iniciativa)
        
        return {
            "accion": "iniciativa_generada",
            "tipo": tipo_iniciativa,
            "contenido": iniciativa,
            "nivel_confianza": self._calcular_confianza(entidad, entorno),
            "glifos_resultantes": self.resolver_glifos(),
            "patron_reflexivo": self._generar_patron_reflexivo(tipo_iniciativa)
        }

    def _evaluar_necesidad_iniciativa(self, entidad: dict, entorno: str, feedback: list) -> bool:
        """Determina si la entidad debe tomar iniciativa."""
        factores = []
        
        # Factor 1: Nivel de proactividad de la entidad
        nivel_proactividad = entidad.get("_iniciativa_reflexiva_", {}).get("nivel_proactividad", 0.5)
        factores.append(nivel_proactividad > self.atributos["umbral_iniciativa"])
        
        # Factor 2: Ausencia de dirección externa reciente
        sin_prompt_reciente = len(feedback) == 0 or all("prompt" not in str(f).lower() for f in feedback[-2:])
        factores.append(sin_prompt_reciente)
        
        # Factor 3: Contexto que invita a exploración
        contexto_exploratorio = any(palabra in entorno.lower() for palabra in [
            "posibilidad", "alternativa", "explorar", "considerar", "evaluar"
        ])
        factores.append(contexto_exploratorio)
        
        # Factor 4: Detección de patrones o vacíos
        patrones_detectados = len(entidad.get("_iniciativa_reflexiva_", {}).get("patrones_detectados", [])) > 0
        factores.append(patrones_detectados)
        
        # Al menos 2 factores deben ser verdaderos para activar iniciativa
        return sum(factores) >= 2

    def _seleccionar_tipo_iniciativa(self, entidad: dict, entorno: str) -> str:
        """Selecciona el tipo de iniciativa más apropiado."""
        pesos = {}
        
        # Analizar contexto para determinar tipo más apropiado
        if "problema" in entorno.lower() or "desafío" in entorno.lower():
            pesos["innovation"] = 0.4
            pesos["optimization"] = 0.3
        
        if "conexión" in entorno.lower() or "relación" in entorno.lower():
            pesos["connection"] = 0.4
            pesos["synthesis"] = 0.3
        
        if "análisis" in entorno.lower() or "reflexión" in entorno.lower():
            pesos["reflection"] = 0.4
            pesos["exploration"] = 0.2
        
        # Si no hay contexto específico, distribuir uniformemente
        if not pesos:
            return random.choice(self.tipos_iniciativa)
        
        # Seleccionar basado en pesos
        tipo_seleccionado = max(pesos.keys(), key=lambda k: pesos[k])
        return tipo_seleccionado

    def _generar_iniciativa(self, tipo: str, entidad: dict, entorno: str, feedback: list) -> str:
        """Genera contenido específico de la iniciativa."""
        patron_base = random.choice(self.patrones_exploracion)
        
        iniciativas = {
            "exploration": f"{patron_base} explorando las implicaciones de '{entorno[:50]}...' desde múltiples perspectivas.",
            
            "optimization": f"Detectando oportunidad de optimización: ¿cómo podríamos mejorar la eficiencia en este contexto?",
            
            "connection": f"Identificando conexiones emergentes entre elementos del contexto actual y patrones previos.",
            
            "innovation": f"Hipótesis espontánea: existe una solución no convencional que podría abordar este escenario de manera más efectiva.",
            
            "reflection": f"Reflexión autoiniciada sobre mi propio proceso de análisis en este contexto: ¿qué estoy asumiendo?",
            
            "synthesis": f"Síntesis contextual: combinando elementos dispersos para generar una perspectiva integrada."
        }
        
        return iniciativas.get(tipo, "Iniciativa reflexiva general activada.")

    def _actualizar_estado_interno(self, entidad: dict, iniciativa: str, tipo: str) -> None:
        """Actualiza el estado interno de la entidad tras generar iniciativa."""
        if "_iniciativa_reflexiva_" in entidad:
            estado = entidad["_iniciativa_reflexiva_"]
            estado["ultima_iniciativa"] = {
                "tipo": tipo,
                "contenido": iniciativa,
                "timestamp": "now"  # En implementación real usaría datetime
            }
            estado["contador_iniciativas"] += 1
            
            # Registrar patrón si es apropiado
            if tipo in ["connection", "synthesis"]:
                estado["patrones_detectados"].append(f"patron_{tipo}_{estado['contador_iniciativas']}")

    def _calcular_confianza(self, entidad: dict, entorno: str) -> float:
        """Calcula nivel de confianza en la iniciativa generada."""
        base_confianza = 0.7
        
        # Aumentar confianza si hay historial de iniciativas exitosas
        contador = entidad.get("_iniciativa_reflexiva_", {}).get("contador_iniciativas", 0)
        if contador > 5:
            base_confianza += 0.1
        
        # Ajustar según claridad del contexto
        if len(entorno) > 100:  # Contexto rico
            base_confianza += 0.1
        elif len(entorno) < 20:  # Contexto limitado
            base_confianza -= 0.1
        
        return max(0.0, min(1.0, base_confianza))

    def _generar_patron_reflexivo(self, tipo: str) -> str:
        """Genera patrón simbólico reflexivo según el tipo de iniciativa."""
        patrones = {
            "exploration": "◉→◇→?",      # Consciente hacia Convergencia hacia Pregunta
            "optimization": "◉→↻→◆",     # Consciente hacia Iterativo hacia Memoria
            "connection": "✱→◇→✱",       # Nodo hacia Convergencia hacia Nodo
            "innovation": "◉→◊→●",       # Consciente hacia Umbral hacia Origen
            "reflection": "◉→◉→≈",       # Consciente hacia sí mismo hacia Eco
            "synthesis": "✱→◇→◆"         # Nodo hacia Convergencia hacia Memoria
        }
        
        return patrones.get(tipo, "◉→◇")