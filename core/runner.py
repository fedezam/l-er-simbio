"""Runner del plano LER: conecta las entidades declaradas a un sustrato.

Uso:
  python -m core.runner --ticks 20                 # sustrato determinista (offline)
  LER_BASE_URL=... LER_API_KEY=... LER_MODEL=... \
    python -m core.runner --ticks 50 --semilla entities/   # cualquier LLM compatible

El runner NO define cognicion: solo aplica reglas del plano y publica la
dinamica poblacional. Que surja algo es decision del sustrato al hidratar.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from core.ecosistema import Plano
from core.llm.base import sustrato_desde_config, SustratoDeterminista
from core.llm.conector import conector_universal
from core.semilla import poblar_entidades


def _sustrato_por_env() -> dict:
    if os.getenv("LER_BASE_URL") and os.getenv("LER_API_KEY"):
        return {
            "tipo": "openai_compat",
            "base_url": os.environ["LER_BASE_URL"],
            "api_key_env": "LER_API_KEY",
            "model": os.getenv("LER_MODEL", "default"),
        }
    return {"tipo": "determinista"}


def main() -> None:
    ap = argparse.ArgumentParser(description="Plano evolutivo LER")
    ap.add_argument("--ticks", type=int, default=10)
    ap.add_argument("--semilla", default="entities/", help="directorio de entidades JSON")
    ap.add_argument("--config", default=None, help="json con seccion 'sustrato' o 'sustratos'")
    ap.add_argument("--universal", action="store_true",
                    help="conector universal: pool de modelos, usa el disponible")
    ap.add_argument("--salida", default="logs/plano.jsonl")
    args = ap.parse_args()

    cfg_raw = {}
    if args.config:
        try:
            cfg_raw = json.loads(Path(args.config).read_text(encoding="utf-8"))
        except FileNotFoundError:
            pass

    if args.universal or "sustratos" in cfg_raw:
        # Pool de candidatos: env (LER_<NOMBRE>_BASE_URL...) + config. Failover vivo.
        sustrato = conector_universal(cfg_raw)
    else:
        sec = cfg_raw.get("sustrato", None)
        cfg = {"sustrato": sec} if sec else _sustrato_por_env()
        sustrato = sustrato_desde_config(cfg)
    cuerpos = poblar_entidades(Path(args.semilla))
    plano = Plano(sustrato=sustrato)
    plano.poblar(cuerpos)
    print(f"sustrato={sustrato.nombre} poblacion_inicial={len(cuerpos)}")

    Path(args.salida).parent.mkdir(parents=True, exist_ok=True)
    with open(args.salida, "a", encoding="utf-8") as fh:
        for t in range(args.ticks):
            r = plano.paso()
            vivos = [c.id for c in plano.cuerpos.values() if c.viva]
            print(f"tick {t:02d} | vivos={r['poblacion']} | eventos={[e[0] for e in r['eventos']][:6]}")
            fh.write(json.dumps({"tick": t, **r}, ensure_ascii=False, default=str) + "\n")

    plano.cementerio(Path("historia/cementerio_plano.json"))
    top = sorted([c for c in plano.cuerpos.values() if c.viva], key=lambda x: -x.fitness_ema)[:5]
    print("\nlinajes dominantes:")
    for c in top:
        print(f"  {c.id}  glifos={''.join(c.glifos)}  fitness={c.fitness_ema:.3f} energia={c.energia:.2f}")


if __name__ == "__main__":
    main()
