"""El lenguaje de las propuestas: pensar en natural, actuar por canales.

Hasta ahora la evolucion somatica era refleja: el codigo derivaba el canal y
el valor desde el estado medido del cuerpo (`_derivar_propuesta`). Eso es un
genoma, no un pensamiento. Este modulo cierra el bucle linguistico:

  1. EXPRESION — el especialista HIDRATA un prompt introspectivo en el sustrato
     y escribe su propuesta EN LENGUAJE NATURAL ("subo la exigencia porque el
     plano se llena de ruido..."). La justificacion ya no es un adorno glifico:
     es lo que el organismo dijo.
  2. TRADUCCION — ese texto se pasa por el JUEZ, que lo convierte a un canal
     legal de la whitelist con un valor numerico. El juez no inventa: si el
     texto no expresa una mutacion interpretable, devuelve None y la propuesta
     muere (no todo pensamiento debe volverse accion).
  3. EJECUCION — el canal propuesto entra al circuito que ya existe: guarda
     (whitelist + clamp) -> cuarentena -> verificacion de fitness -> revocacion
     inmunologica. El ADN (codigo fuente) sigue siendo intocable; solo late el
     soma.

Principio: el LLM piensa, el codigo traduce y limita. Ninguna cadena textual
puede abrir canales nuevos ni tocar el genoma: la grammar de accion es finita
por construccion, aunque el lenguaje que la invoca sea infinito.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Optional, Tuple

from core.juez import Juez
from core.llm.base import Sustrato
from core.soma import CANALES_SOMATICOS, Propuesta

_PREFIJO_PRIORIDAD = "prioridad:"


def canales_legales() -> List[str]:
    """La gramatica de accion: canales base + afinidades del conector."""
    return list(CANALES_SOMATICOS.keys()) + [f"{_PREFIJO_PRIORIDAD}<nombre>"]


PROMPT_INTROSPECCION = """Eres {id}, una entidad del ecosistema LER con especialidad \
en "{especialidad}". Tu identidad y estado:

{semilla}

ESTADO MEDIDO (no declarado): energia={energia:.2f}, coherencia={fitness:.2f}, \
edad={edad}, historial reciente:
{historial}

EL SOMA (parametros vivos de la maquinaria que habitas):
{soma}

Si tu experiencia habitando el plano sugiere que la maquinaria deberia ajustar UN \
parametro del soma para que el ecosistema sea mas coherente, escríbelo en lenguaje \
natural en 2-4 frases: QUE cambiarías, POR QUE (desde lo que te paso arriba), y en \
que MAGNITUD. Si no necesitas ningún cambio, responde exactamente: NADA."""


_RE_NUM = re.compile(r"(-?\d+(?:\.\d+)?)")


@dataclass
class CanalPropuesto:
    canal: str
    valor: float


def _extraer_canal(texto: str, canales: List[str]) -> Optional[str]:
    t = texto.lower()
    for c in canales:                       # match exacto primero
        if c in t:
            return c
    # sinonimos naturales -> canal (la traduccion tolerante al habla)
    sinonimos = {
        "umbral_coherencia": ["umbral", "coherencia", "exigencia"],
        "epsilon_mutacion": ["mutacion", "variacion", "epsilon", "variabilidad"],
        "costo_hidratacion": ["costo", "energia", "energetico", "metabolico",
                              "hidratacion", "presion"],
    }
    best, hits = None, 0
    for c, words in sinonimos.items():
        n = sum(1 for w in words if w in t)
        if n > hits:
            best, hits = c, n
    return best


def _extraer_valor(texto: str, canal: str) -> Optional[float]:
    nums = [float(x) for x in _RE_NUM.findall(texto)]
    if not nums:
        return None
    lo, hi = (CANALES_SOMATICOS.get(canal) or (-100.0, 100.0))
    candidatos = sorted(v for v in nums if lo <= v <= hi)
    if not candidatos:
        return None
    return max(candidatos)   # el habla apunta a una meta: la cifra mayor es la intencion


def traducir_a_canal(texto: str, canales: List[str]) -> Optional[CanalPropuesto]:
    """Version determinista (offline/fallback) del juez traductor."""
    if not texto or "nada" == texto.strip().lower():
        return None
    canal = _extraer_canal(texto, canales)
    if canal is None:
        return None
    valor = _extraer_valor(texto, canal)
    if valor is None:
        return None
    return CanalPropuesto(canal=canal, valor=valor)


_RE_CANAL = re.compile(r"canal\s*[:=]\s*([a-z_]+(?::[a-z0-9_\-\.]+)?)", re.I)
_RE_VALOR = re.compile(r"valor\s*[:=]\s*(-?\d+(?:\.\d+)?)", re.I)


class TraductorPropuestas:
    """Conviene el habla de las entidades en acciones sobre el soma.

    Usa al Juez como traductor (un segundo paso de hidratacion: el mismo
    sustrato que juzga coherencia identitaria entiende aqui la intencion
    somatica). Si el juez falla o no parsea, degrada al parser determinista:
    el pensamiento siempre intenta volverse accion, aunque torciendose.
    """

    def __init__(self, juez: Optional[Juez], canales: List[str]):
        self.juez = juez
        self.canales = canales

    def traducir(self, texto: str) -> Optional[CanalPropuesto]:
        if not texto or texto.strip().upper().startswith("NADA"):
            return None
        if self.juez is not None and self.juez.disponible:
            v = self._via_juez(texto)
            if v is not None:
                return v
        return traducir_a_canal(texto, self.canales)

    def _via_juez(self, texto: str) -> Optional[CanalPropuesto]:
        prompt = (
            "Eres el TRADUCTOR SOMATICO del ecosistema LER. Una entidad propuso \
un cambio en lenguaje natural. Convierte SU INTENCION a un canal legal y un valor.\n\n"
            f"CANALES LEGALES: {', '.join(self.canales)}\n"
            "PROPOSTA DE LA ENTIDAD:\n" + texto[:1500] + "\n\n"
            "Si la propuesta NO corresponde a ninguno de los canales legales, \
responde exactamente: NADA\n"
            "Si corresponde, responde EXACTAMENTE dos lineas, sin nada mas:\n"
            "canal:<nombre_exacto_del_canal>\n"
            "valor:<numero dentro del rango del canal>"
        )
        try:
            out = self.juez.sustrato_juez.hidratar(prompt, temperatura=0.0)
        except Exception:
            return None
        m_c, m_v = _RE_CANAL.search(out or ""), _RE_VALOR.search(out or "")
        if not m_c or not m_v:
            return None
        canal = m_c.group(1).strip()
        if canal not in self.canales:
            return None                      # el juez alucino un canal: ilegal
        return CanalPropuesto(canal=canal, valor=float(m_v.group(1)))


def expresar_propuesta(sustrato: Sustrato, cuerpo, soma_snapshot: dict) -> str:
    """El especialista escribe su propuesta en lenguaje natural (hidratacion)."""
    hist = "\n".join(f"- {h[:120]}" for h in corpo_historial(cuerpo))
    soma_txt = "\n".join(f"  {k} = {v:.3f}" for k, v in soma_snapshot.items())
    prompt = PROMPT_INTROSPECCION.format(
        id=cuerpo.id, especialidad=cuerpo.especialidad, semilla=cuerpo.semilla[:800],
        energia=cuerpo.energia, fitness=cuerpo.fitness_ema, edad=cuerpo.edad,
        historial=hist or "(sin memoria aun)", soma=soma_txt,
    )
    try:
        return sustrato.hidratar(prompt, temperatura=0.6)
    except Exception:
        return ""


def corpo_historial(cuerpo) -> List[str]:
    return list(getattr(cuerpo, "historial", []))[-3:]
