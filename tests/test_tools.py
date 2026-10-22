import pytest
from core import tools

# ---------------------------------------------------------------------------
# Herramientas que asumimos existen en ``core/tools.py``
# ---------------------------------------------------------------------------
# 1. is_palindrome(s: str) -> bool
# 2. chunk(iterable, size) -> generator de listas
# 3. retry(attempts: int = 3, exceptions: tuple = (Exception, )) -> decorador
# ---------------------------------------------------------------------------

def test_is_palindrome_true():
    assert tools.is_palindrome(\"radar\") is True
    assert tools.is_palindrome(\"A man a plan a canal Panama\") is True
    # La función debe ser insensible a mayúsculas y espacios
    assert tools.is_palindrome(\"No lemon, no melon\") is True


def test_is_palindrome_false():
    assert tools.is_palindrome(\"python\") is False
    assert tools.is_palindrome(\"OpenAI\") is False


def test_chunk_even():
    data = list(range(10))
    chunks = list(tools.chunk(data, 3))
    # Los trozos deben ser de tamaño 3, salvo el último que puede ser menor
    assert chunks == [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]


def test_chunk_size_one():
    data = [\"a\", \"b\", \"c\"]
    chunks = list(tools.chunk(data, 1))
    assert chunks == [[\"a\"], [\"b\"], [\"c\"]]


def test_chunk_invalid_size():
    with pytest.raises(ValueError):
        list(tools.chunk([1, 2, 3], 0))

# ---------------------------------------------------------------------------
# retry decorator – simulamos una función que falla al principio y luego
# tiene éxito. Verificamos que el decorador re‑intente el número de veces
# especificado y que devuelva el valor correcto.
# ---------------------------------------------------------------------------

class _Flaky:
    def __init__(self, fail_times: int):
        self._remaining = fail_times
        self.calls = 0

    @tools.retry(attempts=5, exceptions=(RuntimeError,))
    def run(self) -> str:
        self.calls += 1
        if self._remaining > 0:
            self._remaining -= 1
            raise RuntimeError(\"temporary failure\")
        return \"ok\"


def test_retry_success_before_exhaustion():
    flaky = _Flaky(fail_times=2)
    result = flaky.run()
    assert result == \"ok\"
    # Debe haber llamado a la función 3 veces (2 fallos + 1 éxito)
    assert flaky.calls == 3


def test_retry_exhaustion_raises():
    flaky = _Flaky(fail_times=5)  # más fallos que los intentos permitidos
    with pytest.raises(RuntimeError):
        flaky.run()
    # Se intentó exactamente 5 veces (el número de intentos configurado)
    assert flaky.calls == 5
