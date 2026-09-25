"""El Juez: la coherencia la decide el sustrato, no una formula del autor.

Hasta ahora el fitness era un proxy sintactico (densidad de glifos). Eso
limita la evolucion a lo que el autor pudo prever. El juez cierra el circuito
semantico: se hidrata UN prompt de evaluacion en el mismo sustrato (o en un
segundo modelo, si hay pool) y el modelo —que es quien habita las entidades—
dictaminan quien es coherente consigo misma. La seleccion deja de ser ciega
al significado.

Principios:
  - El juez es solo otro Sustrato: agnostico, intercambiable, falible.
  - Presupuesto limitado: juzgar cuesta energia (costo_juez). La escasez
    tambien moldea la cognition del sistema inmune simbolico.
  - Degradacion elegante: si el juez falla o no entiende la salida, el plano
    vuelve al proxy determinista. La vida sigue; el juicio es prestado.
  - Trazabilidad: cada veredicto guarda el texto del juez (historia LER).
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List, Optional

from core.llm.base import Sustrato


PROMPT_JUEZ = """Eres el JUEZ DE COHERENCIA de un ecosistema de entidades reflexivas.
Una entidad fue hidratada por un modelo y produjo una respuesta. Tu trabajo NO
es valorar calidad literaria ni verdad factual: solo medir si la respuesta
HABITA la identidad que se le pidio.

ENTIDAD (identidad declarada + glifos):
{entidad}

RESPUESTA HIDRATADA:
{respuesta}

Criterios (0.0 a 1.0 cada uno):
- identidad: la respuesta habla DESDE la entidad, no sobre ella ni desde un asistente generico
- glifos: integra los simbolos propios ({glifos}) con sentido, no como ruido copiado
- coherencia: no contradice sus axiomas ni deriva en delirio o vacio

Responde EXACTAMENTE con tres lineas clave:valor (decimales), sin nada mas:
identidad:0.0
glifos:0.0
coherencia:0.0"""


@dataclass
class Veredicto:
    identidad: float
    glifos: float
    coherencia: float
    bruto: str = ""              # salida textual del juez: trazabilidad completa
    fuente: str = "juez"         # juez | proxy_fallback

    @property
    def score(self) -> float:
        # ponderacion inicial del autor; EVOLUCIONABLE via soma (canal peso_juez)
        return round(0.4 * self.identidad + 0.2 * self.glifos + 0.4 * self.coherencia, 4)


_RE_CLAVE = re.compile(r"(identidad|glifos|coherencia)\s*[:=]\s*(0?\.\d+|1(?:\.0+)?|[01])\b")


def _parsear(texto: str) -> Optional[Veredicto]:
    """Extrae los tres valores; None si el juez no fue entendido (o no existio)."""
    if not texto:
        return None
    vals = {}
    for k, v in _RE_CLAVE.findall(texto):
        vals[k] = max(0.0, min(1.0, float(v)))
    if len(vals) < 3:
        return None
    return Veredicto(identidad=vals["identidad"], glifos=vals["glifos"],
                     coherencia=vals["coherencia"], bruto=texto[:400])


@dataclass
class Juez:
    """Funcion de fitness semantica con presupuesto finito.

    `sustrato_juez` puede ser el mismo del plano (auto-jurado: la celula se
    mira a si misma) o un segundo modelo (contralor). El conector universal
    decide quien contesta segun disponibilidad.
    """
    sustrato_juez: Sustrato
    presupuesto: int = 50                    # juicios disponibles por corrida
    costo_juez: float = 0.03                 # energia que consume juzgar
    usados: int = 0
    historial: List[dict] = field(default_factory=list)

    @property
    def disponible(self) -> bool:
        return self.usados < self.presupuesto

    def juzgar(self, cuerpo, respuesta: str) -> Optional[Veredicto]:
        """Devuelve Veredicto o None (sin presupuesto / juez ilegible)."""
        if not self.disponible or not respuesta:
            return None
        self.usados += 1
        prompt = PROMPT_JUEZ.format(
            entidad=cuerpo.semilla[:1200],
            glifos="".join(cuerpo.glifos),
            respuesta=respuesta[:800],
        )
        try:
            out = self.sustrato_juez.hidratar(prompt, temperatura=0.0)
        except Exception:
            return None
        v = _parsear(out)
        if v is None:
            # juez ilegible: no castigamos a la entidad por la ceguera del juez
            self.historial.append({"cuerpo": cuerpo.id, "veredicto": None,
                                   "nota": "juez_ilegible", "bruto": (out or "")[:200]})
            return None
        self.historial.append({"cuerpo": cuerpo.id, **vars(v)})
        return v
