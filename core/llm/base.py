"""Interfaz LLM agnóstica para LER.

El sustrato cognitivo NO es el código: es el texto hidratable que un
modelo cualquiera puede interpretar. Este módulo define el contrato mínimo
para inyectar cualquier modelo (API, local, o incluso un humano leyendo
el prompt) sin tocar el núcleo.
"""
from __future__ import annotations

import hashlib
import json
from abc import ABC, abstractmethod
from typing import Optional


class Sustrato(ABC):
    """Contrato único: texto dentro, texto fuera. Agnóstico de modelo."""

    @abstractmethod
    def hidratar(self, prompt: str, temperatura: float = 0.7) -> str:
        """Invoca el modelo sobre una entidad textualizada."""
        ...

    @property
    def nombre(self) -> str:
        return self.__class__.__name__


class SustratoDeterminista(Sustrato):
    """Mock juguetón pero útil: deriva salida del hash del glifo+prompt.

    Sirve para pruebas y como 'organismo' trivial en experimentos de
    emergencia: dos entidades con prompts ligeramente distintos producen
    conductas distintas y estables, lo que permite medir coherencia
    reproductible sin coste ni aleatoriedad externa.
    """

    def hidratar(self, prompt: str, temperatura: float = 0.7) -> str:
        h = hashlib.sha256(prompt.encode("utf-8")).hexdigest() * 2  # padding circular
        tokens = [w for w in prompt.split() if any(c.isalpha() for c in w)]
        if not tokens:
            return ""
        n = max(3, len(tokens) // 4)
        picks = [tokens[int(h[i:i + 4], 16) % len(tokens)] for i in range(0, n * 4, 4)]
        return " ".join(picks)


class SustratoOpenAICompat(Sustrato):
    """Cubre OpenAI, Moonshot, Ollama (/v1), LM Studio, etc. vía base_url."""

    def __init__(self, base_url: str, api_key: str, model: str, timeout: int = 60):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.timeout = timeout

    def hidratar(self, prompt: str, temperatura: float = 0.7) -> str:
        import requests  # import perezoso: el núcleo no depende de red
        resp = requests.post(
            f"{self.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": temperatura,
            },
            timeout=self.timeout,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]


def sustrato_desde_config(config: dict) -> Sustrato:
    """Factoría: lee core/ler_config.json → sección 'sustrato'.

    {"sustrato": {"tipo": "determinista"}}
    {"sustrato": {"tipo": "openai_compat", "base_url": ..., "model": ..., "api_key_env": "LER_API_KEY"}}
    """
    import os
    sec = config.get("sustrato", {"tipo": "determinista"})
    tipo = sec.get("tipo", "determinista")
    if tipo == "determinista":
        return SustratoDeterminista()
    if tipo == "openai_compat":
        key = os.environ.get(sec.get("api_key_env", "LER_API_KEY"), "")
        return SustratoOpenAICompat(sec["base_url"], key, sec["model"])
    raise ValueError(f"Sustrato desconocido: {tipo}")
