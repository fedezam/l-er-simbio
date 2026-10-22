import json
from pathlib import Path

RUTA_JSONL = Path("historia/corrida_ab.jsonl")

if not RUTA_JSONL.exists():
    print("❌ No hay archivo de resultados.")
    exit(1)

lineas = RUTA_JSONL.read_text(encoding="utf-8").splitlines()
print(f"📊 Total de respuestas guardadas: {len(lineas)}\n")

for linea in lineas:
    try:
        d = json.loads(linea)
        print(f"--- Condición {d['condicion']} | {d['id']} (tick {d['tick']}) ---")
        print(d['texto'])
        print()
    except:
        pass
