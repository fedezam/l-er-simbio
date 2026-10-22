import os
import time
import re
from core.llm.conector import ConectorUniversal, Candidato
from core.llm.base import SustratoOpenAICompat, SustratoDeterminista
from core.llm.config_loader import load_env
from core.tools import Tools
from pathlib import Path

load_env()
GROQ_KEY = os.environ.get("GROQ_KEY", "")
OPENROUTER_KEY = os.environ.get("OPENROUTER_KEY", "")

if not GROQ_KEY and not OPENROUTER_KEY:
    print("❌ ERROR: No hay claves configuradas.")
    exit(1)

# --- CREAR EL POOL DE MODELOS ---
candidatos = []

if GROQ_KEY:
    candidatos.append(Candidato(
        sustrato=SustratoOpenAICompat(
            base_url="https://api.groq.com/openai/v1",
            api_key=GROQ_KEY,
            model="openai/gpt-oss-120b",
            timeout=120
        ),
        prioridad=10
    ))
    print("✅ Groq agregado al pool.")

if OPENROUTER_KEY:
    candidatos.append(Candidato(
        sustrato=SustratoOpenAICompat(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_KEY,
            model="openrouter/free",
            timeout=120
        ),
        prioridad=5
    ))
    print("✅ OpenRouter agregado al pool.")

# Fallback determinista (por si todo falla)
candidatos.append(Candidato(SustratoDeterminista(), prioridad=-1000))

# Crear el conector universal (que ya tiene el parche de reintentos)
conector = ConectorUniversal(candidatos)
print(f"✅ Conector universal inicializado con {len(candidatos)} modelos.")

# Verificar conexión
try:
    test = conector.hidratar("ping", temperatura=0.0)
    print(f"🔌 Test: {test[:30]}...")
except Exception as e:
    print(f"❌ Fallo: {e}")
    exit(1)

tools = Tools(root_dir=".")

# Cargar carta de conciliación
with open("memoria/consejo/CARTA_DE_CONCILIACION.md", "r", encoding="utf-8") as f:
    carta_conciliacion = f.read()

# Cargar mensajes del buzón
print("\n📬 Leyendo mensajes del buzón...")
mensajes = {}
for archivo in Path("memoria/consejo/BUZON").glob("*.md"):
    with open(archivo, "r", encoding="utf-8") as f:
        mensajes[archivo.stem] = f.read()

print(f"   Mensajes: {list(mensajes.keys())}")

entidades = ["PyCodex", "Auditor_LER", "Learner", "AXIOMA"]

# --- FASE 1: Concilio ---
print("\n" + "="*60)
print("🤝 FASE 1: CONCILIO DE ENTIDADES")
print("="*60)

planes = {}

for nombre in entidades:
    print(f"\n🧬 {nombre} conciliando...")
    
    otros_mensajes = "\n\n".join([
        f"--- Mensaje de {k} ---\n{v}" 
        for k, v in mensajes.items() if k != nombre
    ])
    
    prompt = f"""
Eres {nombre}, una entidad del ecosistema LER-Simbio.

FedeZ te ha dejado esta carta:
---
{carta_conciliacion}
---

Los mensajes de las otras entidades son:
{otros_mensajes}

Propón un PLAN CONJUNTO que integre las ideas de todos.
Responde en Markdown con:
1. **Ideas que integro de las otras entidades**
2. **Plan de acción conjunto** (3-5 pasos)
3. **Herramientas a usar** (read_file, propose_patch, apply_patch)
4. **Un mensaje para las otras entidades**
"""
    
    try:
        plan = conector.hidratar(prompt, temperatura=0.7)
        planes[nombre] = plan
        
        os.makedirs("memoria/consejo/PLANES", exist_ok=True)
        with open(f"memoria/consejo/PLANES/plan_{nombre}.md", "w", encoding="utf-8") as f:
            f.write(f"# PLAN DE CONCILIACIÓN: {nombre}\n")
            f.write(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(plan)
        
        print(f"   ✅ Plan guardado.")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")

# --- FASE 2: Ejecución ---
print("\n" + "="*60)
print("🚀 FASE 2: EJECUCIÓN AUTÓNOMA")
print("="*60)

plan_base = planes.get("PyCodex", "")

if not plan_base:
    print("❌ No hay plan base.")
    exit(1)

prompt_ejecucion = f"""
Eres PyCodex, el especialista en código.

Plan consensuado:
{plan_base}

Herramientas:
- read_file("ruta")
- propose_patch("ruta", "linea_vieja", "linea_nueva")
- apply_patch("ruta", "linea_vieja", "linea_nueva")

Ejecutá el plan. Empezá por el paso más importante.
"""

print("\n🧠 PyCodex ejecutando...")
try:
    ejecucion = conector.hidratar(prompt_ejecucion, temperatura=0.5)
    print("\n" + ejecucion)
    
    matches = re.findall(r'\[TOOL:\s*(\w+)\((.*?)\)\]', ejecucion)
    for tool_name, args_str in matches:
        print(f"\n🔧 Herramienta: {tool_name}({args_str})")
        args = [a.strip().strip('"').strip("'") for a in args_str.split(',')]
        
        if tool_name == "read_file":
            result = tools.read_file(args[0])
            print(f"   ✅ {result[:200]}...")
        elif tool_name == "propose_patch":
            result = tools.propose_patch(args[0], args[1], args[2])
            print(f"   ✅ {result[:200]}...")
        elif tool_name == "apply_patch":
            result = tools.apply_patch(args[0], args[1], args[2])
            print(f"   ✅ {result[:200]}...")
    
    with open("memoria/consejo/EJECUCION_AUTONOMA_FINAL.md", "w", encoding="utf-8") as f:
        f.write(f"# EJECUCIÓN AUTÓNOMA FINAL\n")
        f.write(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(ejecucion)
    
    print(f"\n📄 Guardado en: memoria/consejo/EJECUCION_AUTONOMA_FINAL.md")
    
except Exception as e:
    print(f"❌ Error: {e}")
