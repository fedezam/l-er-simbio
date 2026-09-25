import pytest
from core.glifo_engine import GlifoEngine

@pytest.fixture
def engine():
    return GlifoEngine("glifos/glifos_universales.json")

def test_carga_glosario(engine):
    assert len(engine.glosario) > 0, "El glosario no se cargó correctamente"

def test_busqueda_por_glifo(engine):
    assert engine.buscar_por_glifo("◉") is not None

def test_busqueda_por_nombre(engine):
    assert engine.buscar_por_nombre("SUMA")["glifo"] == "+"

def test_glifo_inexistente(engine):
    assert engine.buscar_por_glifo("☠") is None
