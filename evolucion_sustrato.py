import time
import os
from core.ecosistema import Plano
from core.semilla import poblar_entidades
from core.llm.base import SustratoOpenAICompat
from core.llm.config_loader import load_env
from core.juez import Juez
from pathlib import Path

load_env()
GROQ_KEY = os.environ.get("GROQ_KEY", "")

print("🧠 Iniciando LER-Simbio en MODO ULTRA-PACIENTE (30s entre entidades)...\n")

sustrato = SustratoOpenAICompat(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_KEY,
    model="openai/gpt-oss-120b",
    timeout=90
)

try:
    print("🔌 Test:", sustrato.hidratar("ping", temperatura=0.0)[:30], "...")
except Exception as e:
    print(f"❌ Fallo: {e}")
    exit(1)

with open("core/ecosistema.py", "r") as f: code_eco = f.read()
with open("core/soma.py", "r") as f: code_soma = f.read()
with open("core/runner.py", "r") as f: code_runner = f.read()
with open("mision_sustrato.txt", "r") as f: mision_template = f.read()

mision = mision_template.replace("[PEGAR EL CÓDIGO DE ecosistema.py ACÁ]", code_eco[:2000])
mision = mision.replace("[PEGAR EL CÓDIGO DE soma.py ACÁ]", code_soma[:2000])
mision = mision.replace("[PEGAR EL CÓDIGO DE runner.py ACÁ]", code_runner[:2000])

juez = Juez(sustrato_juez=sustrato, presupuesto=5)
plano = Plano(sustrato=sustrato, juez=juez, lenguaje_propuestas=True)
entidades = poblar_entidades(Path("entities/"))

for entidad in entidades:
    entidad.semilla += f"\n\n{mision}"

plano.poblar(entidades)

print("🚀 INICIANDO ANÁLISIS (pausas de 30s)...")

vivos = [c for c in plano.cuerpos.values() if c.viva]
for i, entidad in enumerate(vivos):
    print(f"\n  🧠 Hidratando {entidad.id} ({i+1}/{len(vivos)})...")
    
    try:
        vecinos = [v for v in vivos if v.id != entidad.id]
        prompt = entidad.proyectar(vecinos)
        
        resp = sustrato.hidratar(prompt)
        entidad.historial.append(resp[:280])
        entidad.historial = entidad.historial[-5:]
        
        presentes = sum(1 for g in entidad.glifos if g in resp)
        densidad = presentes / max(1, len(entidad.glifos))
        score = 0.7 * densidad + 0.3 * min(1.0, len(resp) / 200)
        
        entidad.fitness_ema = 0.8 * entidad.fitness_ema + 0.2 * score
        entidad.energia -= 0.05
        entidad.edad += 1
        
        print(f"     Fitness: {score:.2f}")
        print(f"     Respuesta: {resp[:200]}...")
        
    except Exception as e:
        print(f"     ⚠️ Fallo: {e}")
    
    if i < len(vivos) - 1:
        print("     ⏳ Esperando 30s (Groq necesita respirar)...")
        time.sleep(30)

print("\n--- ANÁLISIS FINAL DEL SUSTRATO ---")
top = sorted([c for c in plano.cuerpos.values() if c.viva], key=lambda x: -x.fitness_ema)
for c in top:
    print(f"\n🧬 {c.id} (Fitness: {c.fitness_ema:.2f})")
    idea = c.historial[-1] if c.historial else "(Sin respuesta)"
    print(f"   💡 {idea[:1000]}...")
