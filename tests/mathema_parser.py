import pytest
from core.mathema_parser import MathemaParser

def test_tokenizacion_simple():
    parser = MathemaParser()
    tokens = parser.tokenizar("⟨◑ ⇆ ◌⟩ ⤏ ◇▬")
    assert "◑" in tokens
    assert "⇆" in tokens
    assert "◇" in tokens
