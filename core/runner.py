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
from core.juez import Juez
from core.llm.base import sustrato_desde_config, SustratoDeterminista
from core.llm.conector import conector_universal
from core.semilla import poblar_entidades
from core.soma import Soma


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
    ap.add_argument("--soma", action="store_true",
                    help="activar evolucion somatica: las entidades pueden repensar la maquinaria")
    ap.add_argument("--juez", action="store_true",
                    help="fitness semantico: un sustrato juzga la coherencia identitaria (cuesta energia)")
    ap.add_argument("--presupuesto-juez", type=int, default=60,
                    help="numero maximo de juicios por corrida (escasez = presion selectiva)")
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
    soma = Soma(defaults={}) if args.soma else None
    # El juez puede ser un segundo modelo (LER_JUEZ_BASE_URL) o el mismo sustrato:
    # la celula mirandose a si misma. Sin juez dedicado = auto-jurado.
    juez = None
    if args.juez:
        if os.getenv("LER_JUEZ_BASE_URL") and os.getenv("LER_JUEZ_API_KEY"):
            juez_sustrato = sustrato_desde_config({"sustrato": {
                "tipo": "openai_compat",
                "base_url": os.environ["LER_JUEZ_BASE_URL"],
                "api_key_env": "LER_JUEZ_API_KEY",
                "model": os.getenv("LER_JUEZ_MODEL", "default"),
            }})
        else:
            juez_sustrato = sustrato
        juez = Juez(sustrato_juez=juez_sustrato, presupuesto=args.presupuesto_juez)
    plano = Plano(sustrato=sustrato, soma=soma, juez=juez)
    plano.poblar(cuerpos)
    print(f"sustrato={sustrato.nombre} poblacion_inicial={len(cuerpos)} "
          f"soma={'activo' if soma else 'fijo'} "
          f"juez={'activo(pres=' + str(juez.presupuesto) + ')' if juez else 'proxy'}")

    Path(args.salida).parent.mkdir(parents=True, exist_ok=True)
    with open(args.salida, "a", encoding="utf-8") as fh:
        for t in range(args.ticks):
            r = plano.paso()
            vivos = [c.id for c in plano.cuerpos.values() if c.viva]
            print(f"tick {t:02d} | vivos={r['poblacion']} | eventos={[e[0] for e in r['eventos']][:6]}")
            fh.write(json.dumps({"tick": t, **r}, ensure_ascii=False, default=str) + "\n")

    plano.cementerio(Path("historia/cementerio_plano.json"))
    if soma is not None:
        soma.volcar(Path("historia/soma.jsonl"))
        print("\nsoma (mutaciones de la maquinaria):")
        for p in soma.historial:
            print(f"  {p.canal} -> {p.valor}  [{p.estado}]  por {p.proponente}: {p.justificacion}")
    if juez is not None:
        Path("historia/juez.jsonl").parent.mkdir(parents=True, exist_ok=True)
        with open("historia/juez.jsonl", "w", encoding="utf-8") as fh:
            for h in juez.historial:
                fh.write(json.dumps(h, ensure_ascii=False) + "\n")
        ilegibles = sum(1 for h in juez.historial if h.get("veredicto") is None)
        print(f"\njuez: {juez.usados} juicios ({juez.presupuesto} presupuesto), "
              f"{ilegibles} ilegibles→proxy, traza en historia/juez.jsonl")
    top = sorted([c for c in plano.cuerpos.values() if c.viva], key=lambda x: -x.fitness_ema)[:5]
    print("\nlinajes dominantes:")
    for c in top:
        print(f"  {c.id}  glifos={''.join(c.glifos)}  fitness={c.fitness_ema:.3f} energia={c.energia:.2f}")


if __name__ == "__main__":
    main()
