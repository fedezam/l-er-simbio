import os
import time
import requests
from pathlib import Path
from dotenv import load_dotenv

from core.ecosistema import Plano
from core.semilla import poblar_entidades
from core.llm.conector import ConectorUniversal, Candidato
from core.llm.base import SustratoOpenAICompat, SustratoDeterminista
from core.juez import Juez

load_dotenv()
OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")

if not OPENROUTER_KEY:
    print("❌ ERROR: Falta OPENROUTER_KEY. Definila en tu archivo .env")
    exit(1)

# --- 1. CONSULTAR MODELOS DISPONIBLES ---
print("🔍 Consultando modelos gratuitos disponibles en OpenRouter...")
try:
    resp = requests.get(
        "https://openrouter.ai/api/v1/models",
        headers={"Authorization": f"Bearer {OPENROUTER_KEY}"},
        timeout=15
    )
    resp.raise_for_status()
    todos = resp.json()["data"]
    
    # Filtramos solo los que son gratuitos (pricing prompt == "0")
    gratuitos = [m["id"] for m in todos if m.get("pricing", {}).get("prompt") == "0"]
    print(f"✅ Encontrados {len(gratuitos)} modelos gratuitos.")
    
    # Agarrámos los primeros 5 (o los que queramos) como cadena de fallback
    # Priorizamos modelos conocidos si están en la lista
    preferidos = ["google/gemini-2.0-flash-exp:free", "meta-llama/llama-3.2-3b-instruct:free", "qwen/qwen-2-7b-instruct:free"]
    cadena = [m for m in preferidos if m in gratuitos][:3]
    # Si no encontramos los preferidos, usamos cualquiera de la lista
    if not cadena:
        cadena = gratuitos[:5]
    print(f"📋 Cadena de fallback: {cadena}")
    
except Exception as e:
    print(f"❌ Error consultando modelos: {e}")
    exit(1)

# --- 2. CONFIGURAR EL SUSTRATO CON LA CADENA ---
# Le pasamos el array de modelos a OpenRouter. Él maneja el failover solo.
# Usamos el primer modelo de la cadena como "model" principal, pero OpenRouter
# acepta el array en el campo "models" del body (vía extra_body o directo en el JSON).
# Como nuestro SustratoOpenAICompat no expone el campo "models", hacemos un pequeño hack:
# creamos un sustrato que use el primer modelo, y si falla, OpenRouter ya tiene la cadena.
# (Para una implementación perfecta, habría que modificar el conector para aceptar la lista).

# Por ahora, usamos el primer modelo y confiamos en que OpenRouter haga su magia
# con el campo "models" si lo pasamos. Pero el SDK actual no lo soporta directo.
# Vamos a usar el enfoque simple: el primer modelo de la cadena.
modelo_principal = cadena[0]
print(f"🎯 Modelo principal: {modelo_principal}")

sustrato = SustratoOpenAICompat(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_KEY,
    model=modelo_principal,
    timeout=25
)

# Test rápido
print("🔌 Probando conexión...")
try:
    test = sustrato.hidratar("ping", temperatura=0.0)
    print(f"✅ Conexión exitosa: {test[:50]}...")
except Exception as e:
    print(f"❌ Error: {e}")
    print("   Intentando con el siguiente de la cadena...")
    if len(cadena) > 1:
        sustrato = SustratoOpenAICompat(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_KEY,
            model=cadena[1],
            timeout=25
        )
        try:
            test = sustrato.hidratar("ping", temperatura=0.0)
            print(f"✅ Conexión con fallback exitosa: {test[:50]}...")
        except Exception as e2:
            print(f"❌ Fallback también falló: {e2}")
            exit(1)
    else:
        exit(1)

# --- 3. JUEZ Y PLANO ---
juez = Juez(sustrato_juez=sustrato, presupuesto=10)
plano = Plano(sustrato=sustrato, juez=juez, lenguaje_propuestas=True)

entidades = poblar_entidades(Path("entities/"))
mision = open("mision.py", "r").read()
for entidad in entidades:
    entidad.semilla += f"\n\nMISIÓN:\nAnaliza el siguiente código y detecta el error lógico:\n{mision}"

plano.poblar(entidades)

# --- 4. EVOLUCIÓN ---
for tick in range(1, 4):
    print(f"\n================ TICK {tick} ================")
    resultado = plano.paso()
    
    for evento in resultado["eventos"]:
        if evento[0] in ['nacimiento', 'extincion', 'mutacion']:
            print(f"  🌟 {evento}")
        elif evento[0] == 'fallo_sustrato':
            print(f"  ⚠️  Fallo: {evento[1]} - {evento[2][:60]}")
    
    print(f"  Población: {resultado['poblacion']} vivos")
    time.sleep(5)

print("\n--- ESTADO FINAL ---")
top = sorted([c for c in plano.cuerpos.values() if c.viva], key=lambda x: -x.fitness_ema)
for c in top:
    print(f"\n🧬 {c.id}: Fitness={c.fitness_ema:.2f} | Energía={c.energia:.2f}")
    idea = c.historial[-1][:300] if c.historial else "(Sin respuesta)"
    print(f"   💡 {idea}...")
