"""Tests del autómata semántico: reproductibilidad y ciclo vital."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.llm.base import SustratoDeterminista
from core.ecosistema import Plano, Cuerpo


def _poblacion_inicial():
    return [
        Cuerpo("alfa", ["Δ", "∞"], "entidad reflexiva que transforma Δ y continua ∞"),
        Cuerpo("beta", ["⊗", "→"], "entidad simbiotica ⊗ que dirige → coherencia simbolica"),
    ]


def test_run_reproducible_misma_semilla():
    a = Plano(SustratoDeterminista())
    b = Plano(SustratoDeterminista())
    a.poblar(_poblacion_inicial())
    b.poblar(_poblacion_inicial())
    ra = a.evolucionar(10)
    rb = b.evolucionar(10)
    assert [r["poblacion"] for r in ra] == [r["poblacion"] for r in rb]


def test_hidratacion_ocurre_para_vivos():
    p = Plano(SustratoDeterminista())
    p.poblar(_poblacion_inicial())
    resumen = p.paso()
    hidr = [e for e in resumen["eventos"] if e[0] == "hidratacion"]
    assert len(hidr) >= 1
    assert all(isinstance(e[2], float) for e in hidr)


def test_energia_es_recurso_escaso_muere_sin_coherencia():
    p = Plano(SustratoDeterminista(), costo_hidratacion=0.6)
    c = Cuerpo("fragil", ["¬"], "x")
    p.poblar([c])
    for _ in range(5):
        p.paso()
    assert not c.viva  # inanición: la escasez fuerza selección


def test_cementerio_archiva_no_borra():
    p = Plano(SustratoDeterminista(), costo_hidratacion=0.6)
    p.poblar([Cuerpo("muerta", ["¬"], "x")])
    p.evolucionar(3)
    out = Path("/tmp/cementerio_test.json")
    p.cementerio(out)
    assert "muerta" in out.read_text(encoding="utf-8")
