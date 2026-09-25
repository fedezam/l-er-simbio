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

import json
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


PROMPT_JUEZ_SOMA = """Eres el JUEZ DEL SOMA de un ecosistema de entidades reflexivas.
Una entidad especialista propuso subir el parametro `{canal}` del plano hasta \
`{valor_propuesto}`, porque percibe ruido/incoherencia en su entorno. El tejido \
ya acumula dolor por escaladas repetidas de este canal, asi que la propuesta fue \
BLOQUEADA y se te consulta a ti: el modelo que habita las entidades decide.

ESTADO ACTUAL DEL SOMA (parametros vivos):
{soma}

Criterios (0.0 a 1.0 cada uno):
- necesidad: el dolor descrito justifica subir ESTE canal, o es sintoma de otra cosa
- moderacion: el valor propuesto es proporcionado al estado actual del soma
- sistemicidad: la subida no destruye condiciones de vida de otras entidades \
(nacimiento, supervivencia, linajes debiles)

Responde EXACTAMENTE con tres lineas clave:valor (decimales), sin nada mas:
necesidad:0.0
moderacion:0.0
sistemicidad:0.0"""


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


_RE_CLAVE = re.compile(
    r"(identidad|glifos|coherencia|necesidad|moderacion|sistemicidad)"
    r"\s*[:=]\s*(0?\.\d+|1(?:\.\d+)?|[01])\b")


def _parsear(texto: str) -> Optional[Veredicto]:
    """Extrae los tres valores; None si el juez no fue entendido (o no existio)."""
    if not texto:
        return None
    vals = {}
    for k, v in _RE_CLAVE.findall(texto):
        vals[k] = max(0.0, min(1.0, float(v)))
    cuerpo = ("identidad", "glifos", "coherencia")
    soma = ("necesidad", "moderacion", "sistemicidad")
    if all(k in vals for k in cuerpo):
        return Veredicto(identidad=vals["identidad"], glifos=vals["glifos"],
                         coherencia=vals["coherencia"], bruto=texto[:400])
    if all(k in vals for k in soma):
        # veredicto sobre el soma: se codifica en los mismos campos
        return Veredicto(identidad=vals["necesidad"], glifos=vals["moderacion"],
                         coherencia=vals["sistemicidad"], bruto=texto[:400],
                         fuente="juez_soma")
    return None


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

    def juzgar_soma(self, canal: str, valor_propuesto: float, soma: dict) -> Optional[Veredicto]:
        """Consulta semantica cuando el tejido bloquea una escalada (dolor somatico).

        No sustituye al sistema inmunologico: lo COMPLEMENTA. El fitness mide;
        el juez interpreta. Si esta de acuerdo con la politica (score alto),
        se relaja el limite de escaladas para ese canal: el dolor se convierte
        en aprendizaje del propio umbral de dolor.
        """
        if not self.disponible:
            return None
        self.usados += 1
        prompt = PROMPT_JUEZ_SOMA.format(
            canal=canal, valor_propuesto=valor_propuesto,
            soma=json.dumps(soma, ensure_ascii=False, default=str)[:800],
        )
        try:
            out = self.sustrato_juez.hidratar(prompt, temperatura=0.0)
        except Exception:
            return None
        v = _parsear(out)
        nota = "juez_ilegible" if v is None else "soma"
        self.historial.append({"canal": canal, "valor": valor_propuesto,
                               "veredicto": vars(v) if v else None, "nota": nota,
                               "bruto": (out or "")[:200]})
        return v
