import os
import time
from pathlib import Path
from dotenv import load_dotenv

from core.ecosistema import Plano
from core.semilla import poblar_entidades
from core.llm.conector import ConectorUniversal, Candidato
from core.llm.base import SustratoOpenAICompat, SustratoDeterminista
from core.juez import Juez

# --- CONFIGURACIÓN DE OPENROUTER ---
load_dotenv()
OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")

if not OPENROUTER_KEY:
    print("❌ ERROR: Falta OPENROUTER_KEY. Definila en tu archivo .env")
    exit(1)

BASE_URL = "https://openrouter.ai/api/v1"
# Pool de modelos gratuitos de OpenRouter (ordenados por prioridad)
modelos = [
    "meta-llama/llama-3.3-70b-instruct:free",     # Muy bueno en código
    "qwen/qwen-2.5-72b-instruct:free",            # Excelente en lógica
    "google/gemma-2-9b-it:free",                  # Rápido y equilibrado
    "mistralai/mistral-7b-instruct:free"          # Bueno como fallback
]

candidatos = []
# Agregamos todos los modelos al pool con distintas prioridades
for i, modelo in enumerate(modelos):
    prioridad = 10 - i # El primero tiene prioridad 10, el segundo 9, etc.
    candidato = Candidato(
        sustrato=SustratoOpenAICompat(base_url=BASE_URL, api_key=OPENROUTER_KEY, model=modelo),
        prioridad=prioridad
    )
    candidatos.append(candidato)

# Agregamos el modelo "tonto" como última red de seguridad
candidatos.append(Candidato(SustratoDeterminista(), prioridad=-1000))

# Instanciamos el Conector Universal con nuestra lista
sustrato = ConectorUniversal(candidatos)
print(f"✅ Pool de modelos inicializado. Total: {len(modelos)} IAs en rotación.")
print(f"Sustrato activo: {sustrato.nombre}")

# El Juez usará el mismo pool de modelos
juez = Juez(sustrato_juez=sustrato, presupuesto=15)

plano = Plano(sustrato=sustrato, juez=juez, lenguaje_propuestas=True)
entidades = poblar_entidades(Path("entities/"))

# Inyectamos la misión
mision = open("mision.py", "r").read()
for entidad in entidades:
    entidad.semilla += f"\n\nMISIÓN:\nAnaliza el siguiente código y detecta el error lógico:\n{mision}"

plano.poblar(entidades)

for tick in range(1, 4):
    print(f"\n================ TICK {tick} ================")
    resultado = plano.paso()
    
    for evento in resultado["eventos"]:
        if evento[0] not in ['hidratacion']: 
            print(f"  -> Evento: {evento}")
            
    print(f"  Población actual: {resultado['poblacion']} vivos")
    time.sleep(3)

print("\n--- ESTADO FINAL (TOP ENTIDADES) ---")
top = sorted([c for c in plano.cuerpos.values() if c.viva], key=lambda x: -x.fitness_ema)
for c in top:
    print(f"\n{c.id}: Fitness={c.fitness_ema:.2f} | Energía={c.energia:.2f}")
    idea = c.historial[-1][:200] if c.historial else "(Sin respuesta)"
    print(f"   Última idea: {idea}...")
    
# Mostramos el estado de la rotación
print("\n--- ESTADO DEL POOL DE MODELOS ---")
for estado in sustrato.estado():
    print(f"  {estado['modelo']} | Sano: {estado['sano']} | Éxitos: {estado['exitos']} | Fallos: {estado['fallos']}")
