from core.ecosistema import Plano
from core.semilla import poblar_entidades
from core.llm.base import SustratoDeterminista
from pathlib import Path

print("Inicializando el Plano...")
sustrato = SustratoDeterminista()
plano = Plano(sustrato=sustrato, lenguaje_propuestas=True)

entidades = poblar_entidades(Path("entities/"))
plano.poblar(entidades)

print(f"Población inicial: {[c.id for c in plano.cuerpos.values()]}")
print("--- INICIANDO TICK 1 ---")

resultado = plano.paso()

for evento in resultado["eventos"]:
    print(f"Evento: {evento}")

print("\n--- ESTADO DE LAS ENTIDADES ---")
for c in plano.cuerpos.values():
    if c.viva:
        print(f"{c.id}: Energía={c.energia:.2f} | Fitness={c.fitness_ema:.2f} | Glifos={c.glifos}")
