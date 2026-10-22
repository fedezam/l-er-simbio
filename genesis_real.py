import os
from core.ecosistema import Plano
from core.semilla import poblar_entidades
from core.llm.base import SustratoOpenAICompat
from core.juez import Juez
from pathlib import Path

API_KEY = os.environ.get("LER_API_KEY", "")
BASE_URL = "https://api.groq.com/openai/v1"
MODELO = "openai/gpt-oss-120b"

print(f"Inicializando el Plano con IA REAL ({MODELO}) y JUEZ activo...")
sustrato = SustratoOpenAICompat(base_url=BASE_URL, api_key=API_KEY, model=MODELO)

# 1. Encendemos al Juez con presupuesto limitado (para que no gaste tokens de más)
juez = Juez(sustrato_juez=sustrato, presupuesto=10)

plano = Plano(sustrato=sustrato, juez=juez, lenguaje_propuestas=True)
entidades = poblar_entidades(Path("entities/"))

# 2. Inyectamos la misión en el contexto de las entidades
mision = open("mision.py", "r").read()
for entidad in entidades:
    entidad.semilla += f"\n\nMISIÓN ACTUAL DEL ECOSISTEMA:\nEl siguiente código tiene un error lógico. Debes analizarlo y proponer una solución:\n{mision}"

plano.poblar(entidades)

print(f"Población inicial: {[c.id for c in plano.cuerpos.values()]}")
print("--- INICIANDO TICK 1 (JUEZ + MISIÓN) ---")

resultado = plano.paso()

for evento in resultado["eventos"]:
    print(f"Evento: {evento}")

print("\n--- ESTADO DE LAS ENTIDADES ---")
for c in plano.cuerpos.values():
    if c.viva:
        print(f"\n{c.id}: Energía={c.energia:.2f} | Fitness={c.fitness_ema:.2f}")
        # Imprimimos los primeros 250 caracteres de lo que el LLM respondió
        respuesta = c.historial[-1] if c.historial else "Ninguna"
        print(f"   -> Respuesta del LLM: {respuesta[:250]}...")
