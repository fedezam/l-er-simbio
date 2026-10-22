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
    print("❌ ERROR: GROQ_KEY no configurada.")
    exit(1)

# Consultar modelo
print("🔍 Consultando modelos...")
try:
    resp = requests.get(
        "https://api.groq.com/openai/v1/models",
        headers={"Authorization": f"Bearer {GROQ_KEY}"},
        timeout=15
    )
    ids = [m["id"] for m in resp.json()["data"]]
    preferidos = ["qwen/qwen3.8-27b", "llama-3.1-8b-instant", "llama-3.3-70b-versatile"]
    modelo = next((m for m in preferidos if m in ids), ids[0])
    print(f"✅ Modelo: {modelo}")
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

sustrato = SustratoOpenAICompat(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_KEY,
    model=modelo,
    timeout=90
)

tools = Tools(root_dir=".")
atlas_dir = Path("memoria/atlas")

# --- BUSCAR LOS QUE FALTAN ---
faltantes = []
for archivo in [
    "core/glifo_engine.py",
    "entities/pycodex.json",
    "core/runner.py"  # Por si acaso también falló
]:
    nombre_limpio = archivo.replace("/", "_").replace(".", "_")
    path_informe = atlas_dir / f"informe_{nombre_limpio}.md"
    if not path_informe.exists():
        faltantes.append(archivo)

if not faltantes:
    print("✅ No faltan informes. Todo está completo.")
    exit(0)

print(f"\n📄 Faltan {len(faltantes)} informes: {faltantes}\n")

# --- PROCESAR LOS QUE FALTAN CON PAUSAS LARGAS ---
for i, archivo in enumerate(faltantes):
    print(f"\n{'='*60}")
    print(f"📄 ANALIZANDO {i+1}/{len(faltantes)}: {archivo}")
    print(f"{'='*60}")
    
    try:
        contenido = tools.read_file(archivo)
        if not contenido or contenido.startswith("[ERROR"):
            print(f"   ⚠️ No se pudo leer.")
            continue
        
        contenido_truncado = contenido[:4000]
        print(f"   📖 Leído: {len(contenido)} chars")
        
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
        
        nombre_limpio = archivo.replace("/", "_").replace(".", "_")
        path_informe = atlas_dir / f"informe_{nombre_limpio}.md"
        with open(path_informe, "w", encoding="utf-8") as f:
            f.write(f"# INFORME: {archivo}\n")
            f.write(f"Generado: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(informe)
        
        print(f"   ✅ Guardado: {path_informe}")
        print(f"   📄 Vista: {informe[:150]}...")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # PAUSA LARGA de 30 segundos entre faltantes
    if i < len(faltantes) - 1:
        print(f"   ⏳ Esperando 30s...")
        time.sleep(30)

print("\n🎉 RECUPERACIÓN COMPLETADA.")
