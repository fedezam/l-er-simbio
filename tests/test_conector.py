"""Tests del conector universal: failover, health-check y fallback inerte."""
import pytest

from core.llm.base import Sustrato, SustratoDeterminista
from core.llm.conector import Candidato, ConectorUniversal, conector_universal


class SustratoFalso(Sustrato):
    def __init__(self, responde=True, nombre="falso"):
        self.responde = responde
        self._n = nombre
        self.llamadas = 0

    def hidratar(self, prompt, temperatura=0.7):
        self.llamadas += 1
        if not self.responde:
            raise ConnectionError("caido")
        return f"{self._n}:{prompt[:6]}"

    @property
    def nombre(self):
        return self._n


def test_usa_el_mejor_disponible():
    bueno = SustratoFalso(nombre="kimi")
    c = ConectorUniversal([Candidato(bueno, prioridad=5),
                           Candidato(SustratoDeterminista(), prioridad=-1000)])
    out = c.hidratar("hola mundo")
    assert out.startswith("kimi:")
    assert "ConectorUniversal" in c.nombre


def test_failover_cuando_cae_el_preferido():
    caido = SustratoFalso(responde=False, nombre="muerto")
    vivo = SustratoFalso(nombre="local")
    c = ConectorUniversal([Candidato(caido, prioridad=9),
                           Candidato(vivo, prioridad=1)], max_fallos=1)
    out = c.hidratar("test prompt")
    assert out.startswith("local:")
    muerto_cand = next(x for x in c.candidatos if x.sustrato is caido)
    assert muerto_cand.sano is False
    # El siguiente tick ya no pasa por el muerto: 3 llamadas en vivo
    # (ping + primer prompt + segundo prompt), ninguna reintentada en caido.
    c.hidratar("otro prompt")
    assert vivo.llamadas == 3
    assert caido.llamadas == 1  # solo el ping inicial; despues, vetado


def test_fallback_inerte_si_todo_muerde():
    """Sin LLM disponible la celula no muere: respira en modo determinista."""
    muerto = SustratoFalso(responde=False, nombre="api")
    det = SustratoDeterminista()
    c = ConectorUniversal([Candidato(muerto, prioridad=5),
                           Candidato(det, prioridad=-1000)], max_fallos=1)
    out = c.hidratar("glifo AXIOMA semilla prueba")
    assert isinstance(out, str)  # respiracion inerte, sin excepcion


def test_factoria_con_config_y_descubrimiento_env(monkeypatch):
    monkeypatch.setenv("LER_OLLAMA_BASE_URL", "http://localhost:11434/v1")
    monkeypatch.setenv("LER_OLLAMA_MODEL", "llama3")
    cfg = {"sustratos": [{"tipo": "openai_compat",
                          "base_url": "https://api.moonshot.cn/v1",
                          "model": "kimi", "prioridad": 10}]}
    c = conector_universal(cfg)
    # 2 descubiertos (env + config) + determinista siempre al final
    assert len(c.candidatos) == 3
    assert isinstance(c.candidatos[-1].sustrato, SustratoDeterminista)
    assert c.candidatos[0].sustrato.model == "kimi"  # prioridad 10 > 0
