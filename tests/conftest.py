import os
import sys

import pytest

# El repo se usa tanto como paquete `LER.*` (tests antiguos) como desde la
# raiz `core.*` (modulo nuevo). Aseguramos ambos import paths.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
if os.path.join(BASE_DIR, "core") not in sys.path:
    sys.path.insert(0, os.path.join(BASE_DIR, "core"))
if BASE_DIR not in sys.path:
    pass

try:
    from core.glifo_engine import GlyphEngine as _GlyphEngine
except Exception:  # pragma: no cover - compatibilidad con layout antiguo
    try:
        from glifo_engine import GlyphEngine as _GlyphEngine  # type: ignore
    except Exception:
        _GlyphEngine = None


@pytest.fixture(scope="session")
def ruta_glosario():
    """Ruta absoluta al glosario universal de glifos (si existe)."""
    candidatos = [
        os.path.join(BASE_DIR, "glifos", "universal_glyphs.json"),
        os.path.join(BASE_DIR, "glifos", "glifos_universales.json"),
        os.path.join(BASE_DIR, "core", "glifos", "universal_glyphs.json"),
    ]
    for c in candidatos:
        if os.path.exists(c):
            return c
    return candidatos[0]


@pytest.fixture(scope="session")
def engine(ruta_glosario):
    """Instancia única del motor de glifos para toda la sesión."""
    if _GlyphEngine is None:
        pytest.skip("GlifoEngine no importable en este entorno")
    try:
        return _GlyphEngine()
    except TypeError:
        return _GlyphEngine(ruta_glosario)
