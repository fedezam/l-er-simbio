import os
import time
import requests
from core.tools import Tools
from core.llm.base import SustratoOpenAICompat
from core.llm.config_loader import load_env
from pathlib import Path

load_env()
GROQ_KEY = os.environ.get("GROQ_KEY", "")

if not GROQ_KEY:
    print("❌ ERROR: GROQ_KEY no configurada en .env")
    exit(1)

# --- 1. CONSULTAR MODELOS DISPONIBLES EN GROQ ---
print("🔍 Consultando modelos disponibles en Groq...")
try:
    resp = requests.get(
        "https://api.groq.com/openai/v1/models",
        headers={"Authorization": f"Bearer {GROQ_KEY}"},
        timeout=15
    )
    todos = resp.json()["data"]
    ids = [m["id"] for m in todos]
    
    # Buscamos un modelo de Llama 3 o Qwen (buenos para resumir)
    preferidos = [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "llama-3.1-70b-versatile",
        "qwen/qwen3-32b"
    ]
    modelo_elegido = None
    for m in preferidos:
        if m in ids:
            modelo_elegido = m
            break
    
    if not modelo_elegido:
        # Si no encontramos ninguno de los preferidos, usamos el primero de la lista
        modelo_elegido = ids[0]
    
    print(f"✅ Modelo elegido: {modelo_elegido}")
    
except Exception as e:
    print(f"❌ Error consultando modelos: {e}")
    exit(1)

# --- 2. CONFIGURAR EL SUSTRATO ---
sustrato = SustratoOpenAICompat(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_KEY,
    model=modelo_elegido,
    timeout=90
)

# Test rápido
try:
    print("🔌 Test:", sustrato.hidratar("ping", temperatura=0.0)[:30], "...")
except Exception as e:
    print(f"❌ Fallo: {e}")
    exit(1)

tools = Tools(root_dir=".")
os.makedirs("memoria/atlas", exist_ok=True)

# --- 3. DEFINICIÓN DE LOS CRAWLERS ---
crawlers = [
    {
        "nombre": "crawler_core",
        "rama": "core",
        "mision": "Eres un Crawler especializado en el núcleo del sistema. Lee los archivos de 'core/' y genera un mapa técnico de cómo funciona el ecosistema: las leyes de vida, el soma, el juez, el runner. Explica qué hace cada archivo.",
        "archivos": [
            "core/ecosistema.py", "core/soma.py", "core/runner.py",
            "core/juez.py", "core/semilla.py", "core/lenguaje.py",
            "core/glifo_engine.py", "core/sistema_inmune.py"
        ]
    },
    {
        "nombre": "crawler_entities",
        "rama": "entities",
        "mision": "Eres un Crawler especializado en las entidades. Lee los archivos JSON de 'entities/' y genera un inventario de todas las entidades disponibles. Describe el nombre, tipo, especialidad y propósito de cada una.",
        "archivos": [
            "entities/pycodex.json", "entities/auditor_ler.json",
            "entities/learn_nucleo_0.json", "entities/AXIOMA/axioma_reflexivo.json",
            "entities/ghost_auditor.json", "entities/plan_mode.json"
        ]
    },
    {
        "nombre": "crawler_glifos",
        "rama": "glifos",
        "mision": "Eres un Crawler especializado en el lenguaje simbólico. Lee los archivos JSON de 'glifos/' y genera un diccionario explicativo de los glifos disponibles.",
        "archivos": [
            "glifos/universal_glyphs.json", "glifos/mathema.json",
            "glifos/mmp_core.json", "glifos/security_glyphs.json"
        ]
    },
    {
        "nombre": "crawler_docs",
        "rama": "docs",
        "mision": "Eres un Crawler especializado en la filosofía y la historia. Lee los Markdown de 'docs/' e 'historia/' y genera un resumen de los manifiestos y crónicas.",
        "archivos": [
            "docs/manifiesto_ontologico_ia.md",
            "docs/protocolo_ler.md",
            "historia/nacimiento_axioma.md",
            "historia/origen_de_arca_aelion_dva.md"
        ]
    }
]

# --- 4. EJECUCIÓN ---
print("\n🐝 INICIANDO ENJAMBRE DE CRAWLERS...\n")

for i, crawler in enumerate(crawlers):
    print(f"\n{'='*60}")
    print(f"🔍 CRAWLER {i+1}/{len(crawlers)}: {crawler['nombre']}")
    print(f"{'='*60}")
    
    contexto = ""
    for archivo in crawler["archivos"]:
        try:
            contenido = tools.read_file(archivo)
            contexto += f"\n--- ARCHIVO: {archivo} ---\n{contenido[:3000]}\n"
            print(f"   📖 Leído: {archivo}")
        except Exception as e:
            print(f"   ⚠️ Error leyendo {archivo}: {e}")
    
    if not contexto:
        continue
    
    prompt = f"""
{crawler['mision']}

Archivos de la rama '{crawler['rama']}':
{contexto}

Genera un informe estructurado en Markdown con:
1. Un título descriptivo.
2. Un resumen de lo que hace esta rama.
3. Un detalle de cada archivo.
4. Conclusiones sobre cómo se relaciona con el resto del ecosistema.
"""
    
    print(f"   🧠 Generando informe...")
    try:
        informe = sustrato.hidratar(prompt, temperatura=0.3)
        
        path_informe = f"memoria/atlas/{crawler['nombre']}.md"
        with open(path_informe, "w", encoding="utf-8") as f:
            f.write(f"# INFORME: {crawler['rama'].upper()}\n")
            f.write(f"Generado: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Modelo: {modelo_elegido}\n\n")
            f.write(informe)
        
        print(f"   ✅ Guardado: {path_informe}")
        print(f"   📄 Vista: {informe[:150]}...")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    if i < len(crawlers) - 1:
        time.sleep(5)

print("\n🎉 ENJAMBRE COMPLETADO. Revisá la carpeta memoria/atlas/")
