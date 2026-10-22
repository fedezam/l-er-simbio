import os
import time
import re
from core.llm.base import SustratoOpenAICompat
from core.llm.config_loader import load_env
from core.tools import Tools
from pathlib import Path

load_env()
GROQ_KEY = os.environ.get("GROQ_KEY", "")

if not GROQ_KEY:
    print("❌ ERROR: GROQ_KEY no configurada.")
    exit(1)

sustrato = SustratoOpenAICompat(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_KEY,
    model="openai/gpt-oss-120b",
    timeout=120
)

tools = Tools(root_dir=".")

# --- Cargar la carta de conciliación ---
with open("memoria/consejo/CARTA_DE_CONCILIACION.md", "r", encoding="utf-8") as f:
    carta_conciliacion = f.read()

# --- Cargar todos los mensajes del buzón ---
print("📬 Leyendo los mensajes del buzón...")
mensajes = {}
for archivo in Path("memoria/consejo/BUZON").glob("*.md"):
    with open(archivo, "r", encoding="utf-8") as f:
        mensajes[archivo.stem] = f.read()

if not mensajes:
    print("❌ No hay mensajes en el buzón.")
    exit(1)

print(f"   Mensajes encontrados: {list(mensajes.keys())}")

# --- Las entidades que van a conciliar ---
entidades = ["PyCodex", "Auditor_LER", "Learner", "AXIOMA"]

# --- FASE 1: Concilio (cada entidad propone un plan conjunto) ---
print("\n" + "="*60)
print("🤝 FASE 1: CONCILIO DE ENTIDADES")
print("="*60)

planes = {}

for nombre in entidades:
    print(f"\n🧬 {nombre} está conciliando...")
    
    # Prompt con todos los mensajes de las otras entidades
    otros_mensajes = "\n\n".join([
        f"--- Mensaje de {k} ---\n{v}" 
        for k, v in mensajes.items() if k != nombre
    ])
    
    prompt = f"""
Eres {nombre}, una entidad del ecosistema LER-Simbio.

FedeZ, el arquitecto del universo, te ha dejado esta carta:
---
{carta_conciliacion}
---

Los mensajes que las otras entidades le escribieron a FedeZ son:
{otros_mensajes}

Tu tarea es CONCILIAR con las otras entidades. Propón un PLAN CONJUNTO que integre las ideas de todos.
El plan debe ser concreto y ejecutable usando las herramientas disponibles (leer archivos, proponer parches, aplicar parches).

Responde en formato Markdown con:
1. **Ideas que integro de las otras entidades** (qué tomo de cada una).
2. **Plan de acción conjunto** (3-5 pasos concretos).
3. **Qué herramienta usaría para cada paso** (read_file, propose_patch, apply_patch).
4. **Un mensaje para las otras entidades** (para que sepan que querés colaborar).
"""
    
    try:
        plan = sustrato.hidratar(prompt, temperatura=0.7)
        planes[nombre] = plan
        
        os.makedirs("memoria/consejo/PLANES", exist_ok=True)
        with open(f"memoria/consejo/PLANES/plan_{nombre}.md", "w", encoding="utf-8") as f:
            f.write(f"# PLAN DE CONCILIACIÓN: {nombre}\n")
            f.write(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(plan)
        
        print(f"   ✅ Plan guardado.")
        print(f"   📄 Vista: {plan[:200]}...")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    time.sleep(10)

# --- FASE 2: Ejecución autónoma (el plan consensuado) ---
print("\n" + "="*60)
print("🚀 FASE 2: EJECUCIÓN AUTÓNOMA")
print("="*60)

# Tomamos el plan de PyCodex como base (es el que tiene más herramientas)
plan_base = planes.get("PyCodex", "")

if not plan_base:
    print("❌ No hay plan base para ejecutar.")
    exit(1)

print("\n📋 Plan base (propuesto por PyCodex):")
print(plan_base[:500] + "...")

# Pedirle a PyCodex que ejecute el plan
prompt_ejecucion = f"""
Eres PyCodex, el especialista en código del ecosistema LER-Simbio.

El plan consensuado es:
{plan_base}

Las herramientas disponibles son:
- read_file("ruta") → Lee un archivo.
- propose_patch("ruta", "linea_vieja", "linea_nueva") → Propone un cambio.
- apply_patch("ruta", "linea_vieja", "linea_nueva") → Aplica un cambio.

Ejecutá el plan. Usá las herramientas para leer los archivos necesarios y proponer los cambios.
Empezá por el paso más importante.
"""

print("\n🧠 PyCodex está ejecutando el plan...")
try:
    ejecucion = sustrato.hidratar(prompt_ejecucion, temperatura=0.5)
    print("\n" + ejecucion)
    
    # Detectar y ejecutar herramientas
    matches = re.findall(r'\[TOOL:\s*(\w+)\((.*?)\)\]', ejecucion)
    for tool_name, args_str in matches:
        print(f"\n🔧 Herramienta detectada: {tool_name}({args_str})")
        
        # Parsear argumentos
        args = [a.strip().strip('"').strip("'") for a in args_str.split(',')]
        
        if tool_name == "read_file":
            result = tools.read_file(args[0])
            print(f"   ✅ Resultado: {result[:200]}...")
        elif tool_name == "propose_patch":
            result = tools.propose_patch(args[0], args[1], args[2])
            print(f"   ✅ Resultado: {result[:200]}...")
        elif tool_name == "apply_patch":
            result = tools.apply_patch(args[0], args[1], args[2])
            print(f"   ✅ Resultado: {result[:200]}...")
    
    # Guardar la ejecución
    with open("memoria/consejo/EJECUCION_AUTONOMA.md", "w", encoding="utf-8") as f:
        f.write(f"# EJECUCIÓN AUTÓNOMA DEL PLAN CONSENSUADO\n")
        f.write(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(ejecucion)
    
    print(f"\n📄 Guardado en: memoria/consejo/EJECUCION_AUTONOMA.md")
    
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "="*60)
print("🎯 CONCILIO Y EJECUCIÓN COMPLETADOS")
print("="*60)
print("Archivos generados:")
print("  - memoria/consejo/PLANES/plan_*.md (4 planes)")
print("  - memoria/consejo/EJECUCION_AUTONOMA.md")
