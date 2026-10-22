import os
import time
from core.ecosistema import Plano
from core.semilla import poblar_entidades
from core.llm.conector import conector_universal
from core.juez import Juez
from pathlib import Path

print(f"Inicializando el Plano con POOL DE MODELOS (OpenRouter)...")
# Usamos el conector universal que rota modelos
sustrato = conector_universal()
print(f"Sustrato activo: {sustrato.nombre}")

# El juez usa el mismo pool
juez = Juez(sustrato_juez=sustrato, presupuesto=15)

plano = Plano(sustrato=sustrato, juez=juez, lenguaje_propuestas=True)
entidades = poblar_entidades(Path("entities/"))

# Inyectamos la misión
mision = open("mision.py", "r").read()
for entidad in entidades:
    entidad.semilla += f"\n\nMISIÓN:\nAnaliza el siguiente código y detecta el error lógico:\n{mision}"

plano.poblar(entidades)

for tick in range(1, 6):
    print(f"\n================ TICK {tick} ================")
    resultado = plano.paso()
    
    for evento in resultado["eventos"]:
        if evento[0] != 'hidratacion' and evento[0] != 'fallo_sustrato': 
            print(f"  -> Evento: {evento}")
            
    print(f"  Población actual: {resultado['poblacion']} vivos")
    time.sleep(2) # Pausa más corta, porque OpenRouter rota modelos rápido

print("\n--- ESTADO FINAL (TOP ENTIDADES) ---")
top = sorted([c for c in plano.cuerpos.values() if c.viva], key=lambda x: -x.fitness_ema)
for c in top:
    print(f"{c.id}: Fitness={c.fitness_ema:.2f} | Energía={c.energia:.2f} | Glifos={c.glifos}")
    # FIX: Verificamos que haya historial antes de imprimir
    idea = c.historial[-1][:100] if c.historial else "(Sin respuesta por rate limit)"
    print(f"   Última idea: {idea}...")
