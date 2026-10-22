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

# --- 1. CONSULTAR MODELOS ---
print("🔍 Consultando modelos disponibles en Groq...")
try:
    resp = requests.get(
        "https://api.groq.com/openai/v1/models",
        headers={"Authorization": f"Bearer {GROQ_KEY}"},
        timeout=15
    )
    todos = resp.json()["data"]
    ids = [m["id"] for m in todos]
    preferidos = ["llama-3.1-8b-instant", "llama-3.3-70b-versatile", "qwen/qwen3-32b"]
    modelo = next((m for m in preferidos if m in ids), ids[0])
    print(f"✅ Modelo elegido: {modelo}")
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

sustrato = SustratoOpenAICompat(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_KEY,
    model=modelo,
    timeout=90
)

try:
    print("🔌 Test:", sustrato.hidratar("ping", temperatura=0.0)[:30], "...")
except Exception as e:
    print(f"❌ Fallo: {e}")
    exit(1)

tools = Tools(root_dir=".")
os.makedirs("memoria/atlas", exist_ok=True)

# --- 2. LISTA DE ARCHIVOS ---
archivos_a_analizar = [
    "core/ecosistema.py", "core/soma.py", "core/runner.py",
    "core/juez.py", "core/semilla.py", "core/lenguaje.py",
    "core/glifo_engine.py", "core/sistema_inmune.py",
    "entities/pycodex.json", "entities/auditor_ler.json",
    "entities/learn_nucleo_0.json", "entities/plan_mode.json",
    "glifos/universal_glyphs.json", "glifos/mathema.json",
    "glifos/mmp_core.json", "glifos/security_glyphs.json",
    "docs/manifiesto_ontologico_ia.md", "docs/protocolo_ler.md",
    "historia/nacimiento_axioma.md", "historia/origen_de_arca_aelion_dva.md"
]

# --- 3. CRAWLER CON PAUSAS DE 20 SEGUNDOS ---
print(f"\n🐝 INICIANDO CRAWLER (pausas de 20s para no saturar)...\n")

for i, archivo in enumerate(archivos_a_analizar):
    # Saltear si ya existe el informe
    nombre_limpio = archivo.replace("/", "_").replace(".", "_")
    path_informe = f"memoria/atlas/informe_{nombre_limpio}.md"
    if os.path.exists(path_informe):
        print(f"\n⏭️  Ya existe: {path_informe}. Saltando...")
        continue
    
    print(f"\n{'='*60}")
    print(f"📄 ANALIZANDO {i+1}/{len(archivos_a_analizar)}: {archivo}")
    print(f"{'='*60}")
    
    try:
        contenido = tools.read_file(archivo)
        if not contenido or contenido.startswith("[ERROR"):
            print(f"   ⚠️ No se pudo leer.")
            continue
        
        contenido_truncado = contenido[:4000]
        print(f"   📖 Leído: {len(contenido)} chars (truncado a {len(contenido_truncado)})")
        
        prompt = f"""
Eres un Crawler especializado. Analiza el siguiente archivo del repositorio l-er-simbio y genera un mini-informe.

ARCHIVO: {archivo}
CONTENIDO:
{contenido_truncado}

Genera un informe breve y estructurado en Markdown:
1. **¿Qué es este archivo?** (Una línea)
2. **¿Qué hace?** (Funciones o clases principales)
3. **¿Cómo se relaciona con el resto del sistema?** (Imports, dependencias)
4. **¿Es esencial o prescindible?** (Justificación)

Sé conciso. No más de 200 palabras.
"""
        
        print(f"   🧠 Generando mini-informe...")
        informe = sustrato.hidratar(prompt, temperatura=0.3)
        
        with open(path_informe, "w", encoding="utf-8") as f:
            f.write(f"# INFORME: {archivo}\n")
            f.write(f"Generado: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(informe)
        
        print(f"   ✅ Guardado: {path_informe}")
        print(f"   📄 Vista: {informe[:150]}...")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # PAUSA LARGA: 20 segundos entre archivos
    if i < len(archivos_a_analizar) - 1:
        print(f"   ⏳ Esperando 20s (Groq necesita respirar)...")
        time.sleep(20)

print("\n🎉 CRAWLER COMPLETADO.")
print(f"Mini-informes generados en: memoria/atlas/")
