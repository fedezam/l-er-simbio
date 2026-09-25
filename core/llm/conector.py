"""Conector universal de sustratos: el plano usa el modelo que haya disponible.

Principio: la entidad es informacion inerte; el LLM es el catalizador prestado.
Si un catalizador se apaga (API sin creditos, host caido, timeout), la celula no
muere: busca otro sustrato y sigue latiendo. Agnosticidad llevada a runtime.

El `ConectorUniversal` mantiene un pool de candidatos ordenados por afinidad y:
  - hace health-check perezoso (una hidratacion minima) antes de confiar en uno
  - si el activo falla durante el tick, lo degrada y hace failover al siguiente
  - puede descubrir proveedores desde variables de entorno (LER_*_BASE_URL)
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Optional

from core.llm.base import Sustrato, SustratoDeterminista, SustratoOpenAICompat


@dataclass
class Candidato:
    """Un sustrato potencial + su historial de fiabilidad."""
    sustrato: Sustrato
    prioridad: int = 0            # mayor = mas deseado (afinidad del plano)
    sano: Optional[bool] = None   # None = aun no verificado
    fallos: int = 0
    exitos: int = 0
    _verificado: bool = False

    def score(self) -> int:
        base = self.prioridad * 100
        if self.sano is False:
            base -= 10_000
        return base + self.exitos - self.fallos * 3


class ConectorUniversal(Sustrato):
    """Fachada Sustrato sobre un pool: delega en el mejor modelo disponible.

    Implementa el contrato `Sustrato`, por lo que el Plano/runner no necesitan
    saber cuantos ni cuales modelos hay detras: solo hidratan.
    """

    def __init__(self, candidatos: list[Candidato], max_fallos: int = 2):
        if not candidatos:
            raise ValueError("El conector universal necesita al menos un candidato.")
        self.candidatos = sorted(candidatos, key=lambda c: -c.score())
        self.max_fallos = max_fallos
        self._activo: Optional[Candidato] = None

    # ---- seleccion ----------------------------------------------------- #
    def _mejor_disponible(self, excluir: set[int] = frozenset()) -> Optional[Candidato]:
        for i, c in enumerate(self.candidatos):
            if i in excluir:
                continue
            if c.sano is False and c.fallos >= self.max_fallos:
                continue
            return c
        return None

    def _verificar(self, c: Candidato) -> bool:
        """Health-check perezoso: una hidratacion minima debe devolver texto."""
        if c._verificado:
            return c.sano is not False
        try:
            out = c.sustrato.hidratar("ping", temperatura=0.0)
            c.sano = bool(out and out.strip())
        except Exception:
            c.sano = False
        c._verificado = True
        return c.sano

    # ---- contrato Sustrato --------------------------------------------- #
    def hidratar(self, prompt: str, temperatura: float = 0.7) -> str:
        excluidos: set[int] = set()
        ultima_exc: Optional[Exception] = None
        while True:
            activo = self._mejor_disponible(excluidos)
            if activo is None:
                break
            idx = self.candidatos.index(activo)
            if not self._verificar(activo):
                excluidos.add(idx)
                continue
            try:
                out = activo.sustrato.hidratar(prompt, temperatura)
                activo.exitos += 1
                activo.fallos = max(0, activo.fallos - 1)  # recuperacion lenta
                activo.sano = True
                self._activo = activo
                return out
            except Exception as e:
                ultima_exc = e
                activo.fallos += 1
                if activo.fallos >= self.max_fallos:
                    activo.sano = False
                excluidos.add(idx)
        # Todos los LLM cayeron: la celula respira en modo inerte, no muere.
        fallback = self.candidatos[-1]
        if isinstance(fallback.sustrato, SustratoDeterminista):
            return fallback.sustrato.hidratar(prompt, temperatura)
        raise RuntimeError(
            "Sin sustrato disponible y sin fallback determinista."
        ) from ultima_exc

    @property
    def nombre(self) -> str:
        act = self._activo.sustrato.nombre if self._activo else "sin-activo"
        return f"ConectorUniversal({act})"

    def estado(self) -> list[dict]:
        """Observable del panel: quien esta vivo, quien fallo, quien espera."""
        return [
            {
                "sustrato": c.sustrato.nombre,
                "modelo": getattr(c.sustrato, "model", "-"),
                "sano": c.sano,
                "exitos": c.exitos,
                "fallos": c.fallos,
                "activo": c is self._activo,
            }
            for c in self.candidatos
        ]


# ---- descubrimiento ---------------------------------------------------- #
def _candidatos_desde_env() -> list[Candidato]:
    """Descubre proveedores LER_<NOMBRE>_BASE_URL / _API_KEY_ENV / _MODEL.

    Ejemplo:
      LER_MOONSHOT_BASE_URL=https://api.moonshot.cn/v1
      LER_MOONSHOT_API_KEY_ENV=MOONSHOT_API_KEY
      LER_MOONSHOT_MODEL=kimi-k2-0711-preview
      LER_OLLAMA_BASE_URL=http://localhost:11434/v1
      LER_OLLAMA_API_KEY_ENV=
      LER_OLLAMA_MODEL=llama3
    """
    out: list[Candidato] = []
    sufijos = ("BASE_URL", "API_KEY_ENV", "MODEL", "PRIORIDAD")
    for var in os.environ:
        if not var.startswith("LER_") or not var.endswith("_BASE_URL"):
            continue
        nombre = var[len("LER_"): -len("_BASE_URL")]
        get = lambda suf, n=nombre: os.environ.get(f"LER_{n}_{suf}", "")
        out.append(
            Candidato(
                sustrato=SustratoOpenAICompat(
                    base_url=get("BASE_URL"),
                    api_key=os.environ.get(get("API_KEY_ENV") or "LER_API_KEY", ""),
                    model=get("MODEL") or "default",
                ),
                prioridad=int(get("PRIORIDAD") or "0"),
            )
        )
    return out


def conector_universal(
    config: Optional[dict] = None,
    incluir_determinista: bool = True,
) -> ConectorUniversal:
    """Factoria: env vars + seccion 'sustratos' del config -> conector vivo.

    El determinista SIEMPRE entra al pool como ultimo recurso: garantiza que
    la maquina nunca se pare por falta de modelo (latencia inerte).
    """
    candidatos = _candidatos_desde_env()
    for sec in (config or {}).get("sustratos", []):
        tipo = sec.get("tipo", "openai_compat")
        if tipo == "openai_compat":
            s = SustratoOpenAICompat(
                base_url=sec["base_url"],
                api_key=os.environ.get(sec.get("api_key_env", "LER_API_KEY"), ""),
                model=sec.get("model", "default"),
            )
        elif tipo == "determinista":
            s = SustratoDeterminista()
        else:
            continue
        candidatos.append(Candidato(s, prioridad=int(sec.get("prioridad", 0))))
    if incluir_determinista:
        candidatos.append(Candidato(SustratoDeterminista(), prioridad=-1000))
    return ConectorUniversal(candidatos)
