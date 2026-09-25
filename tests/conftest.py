import pytest
import os
from LER.core.glifo_engine import GlifoEngine


@pytest.fixture(scope="session")
def ruta_glosario():
    """
    Devuelve la ruta absoluta al glosario universal de glifos.
    Se ejecuta una sola vez por sesión de test.
    """
    base_dir = os.path.dirname(os.path.dirname(__file__))  # sube un nivel desde /tests
    return os.path.join(base_dir, "glifos", "glifos_universales.json")

@pytest.fixture(scope="session")
def engine(ruta_glosario):
    """
    Crea una única instancia de GlifoEngine para todos los tests.
    """
    return GlifoEngine(ruta_glosario)

