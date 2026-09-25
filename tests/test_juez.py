"""Tests del Juez: fitness semantico medido por el sustrato, no por el autor."""
import random

from core.ecosistema import Cuerpo, Plano
from core.juez import Juez, Veredicto, _parsear
from core.llm.base import Sustrato, SustratoDeterminista


class SustratoJuezFijo(Sustrato):
    """Simula un LLM-juez: siempre dictamina 0.9/0.1/0.5 en formato clave:valor."""
    def __init__(self, salida="identidad:0.9\nglifos:0.1\ncoherencia:0.5"):
        self._salida = salida
        self.llamadas = 0

    def hidratar(self, prompt, temperatura=0.7):
        self.llamadas += 1
        return self._salida


class SustratoJuezRoto(Sustrato):
    def hidratar(self, prompt, temperatura=0.7):
        raise RuntimeError("el juez cayo")


def _cuerpo():
    return Cuerpo(id="AXIOMA", glifos=["Δ", "∞"],
                  semilla="SOY AXIOMA. Habita esta identidad.")


def test_parseo_veredicto():
    v = _parsear("identidad:0.9\nglifos:0.1\ncoherencia:0.5")
    assert v is not None and v.identidad == 0.9 and v.score == round(0.4*0.9+0.2*0.1+0.4*0.5, 4)


def test_juez_ilegible_no_castiga():
    """Si el juez no entiende o divaga, se devuelve None (queda el proxy)."""
    j = Juez(SustratoJuezFijo(salida="no se que responder"))
    assert j.juzgar(_cuerpo(), "Δ algo") is None


def test_presupuesto_limita_juicios():
    sj = SustratoJuezFijo()
    j = Juez(sj, presupuesto=3)
    for _ in range(5):
        j.juzgar(_cuerpo(), "respuesta Δ")
    assert j.usados == 3 and sj.llamadas == 3   # juzgar cuesta: no hay juicio gratis


def test_plano_usa_juez_como_fitness():
    """El score del tick viene del veredicto del juez, no del proxy."""
    cuerpo = _cuerpo()
    plano = Plano(SustratoDeterminista(), juez=Juez(SustratoJuezFijo()),
                  rng=random.Random(1))
    plano.poblar([cuerpo])
    r = plano.paso()
    hidr = [e for e in r["eventos"] if e[0] == "hidratacion"][0]
    assert hidr[3] == "juez"
    assert hidr[2] == round(0.4*0.9 + 0.2*0.1 + 0.4*0.5, 4)


def test_fallo_del_juez_degrada_a_proxy():
    """Juez caido = vida sigue con proxy determinista (degradacion elegante)."""
    plano = Plano(SustratoDeterminista(), juez=Juez(SustratoJuezRoto()))
    plano.poblar([_cuerpo()])
    r = plano.paso()
    hidr = [e for e in r["eventos"] if e[0] == "hidratacion"][0]
    assert hidr[3] == "proxy" and plano.cuerpos["AXIOMA"].viva
