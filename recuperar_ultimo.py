import os
import time
import random
from core.tools import Tools
from core.llm.base import SustratoOpenAICompat
from core.llm.config_loader import load_env
from pathlib import Path

load_env()
GROQ_KEY = os.environ.get("GROQ_KEY", "")
OPENROUTER_KEY = os.environ.get("OPENROUTER_KEY", "")

# Lista completa de archivos del repo
todos_los_archivos = []
for root, dirs, files in os.walk("."):
    if any(x in root for x in [".git", "__pycache__", "node_modules", ".venv", "venv", "memoria/atlas", "memoria/logs"]):
        continue
    for f in files:
        if f.endswith((".py", ".json", ".md", ".txt", ".toml", ".cfg", ".ini", ".yml", ".yaml")):
            ruta = os.path.join(root, f).replace("./", "")
            todos_los_archivos.append(ruta)

# Encontrar los que no tienen informe
atlas_dir = Path("memoria/atlas")
faltantes = []
for archivo in todos_los_archivos:
    nombre_limpio = archivo.replace("/", "_").replace(".", "_")
    path_informe = atlas_dir / f"informe_{nombre_limpio}.md"
    if not path_informe.exists():
        faltantes.append(archivo)

if not faltantes:
    print("✅ No falta ninguno. Todos tienen informe.")
    exit(0)

print(f"📄 Archivos sin informe: {faltantes}")

# Procesar el que falta con OpenRouter
if not OPENROUTER_KEY:
    print("❌ No hay OPENROUTER_KEY.")
    exit(1)

sustrato = SustratoOpenAICompat(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_KEY,
    model="openrouter/free",
    timeout=90
)

tools = Tools(root_dir=".")

for archivo in faltantes:
    print(f"\n📄 Analizando: {archivo}")
    try:
        contenido = tools.read_file(archivo)
        if not contenido or contenido.startswith("[ERROR"):
            print(f"   ⚠️ No se pudo leer.")
            continue
        
        contenido_truncado = contenido[:3000]
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

Sé conciso. No más de 150 palabras.
"""
        
        print(f"   🧠 Generando...")
        informe = sustrato.hidratar(prompt, temperatura=0.3)
        
        nombre_limpio = archivo.replace("/", "_").replace(".", "_")
        path_informe = atlas_dir / f"informe_{nombre_limpio}.md"
        with open(path_informe, "w", encoding="utf-8") as f:
            f.write(f"# INFORME: {archivo}\n")
            f.write(f"Generado: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(informe)
        
        print(f"   ✅ Guardado: {path_informe.name}")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        # Si falla con OpenRouter, intentar con Groq
        if GROQ_KEY:
            print("   🔄 Reintentando con Groq...")
            sustrato_groq = SustratoOpenAICompat(
                base_url="https://api.groq.com/openai/v1",
                api_key=GROQ_KEY,
                model="openai/gpt-oss-120b",
                timeout=90
            )
            try:
                informe = sustrato_groq.hidratar(prompt, temperatura=0.3)
                nombre_limpio = archivo.replace("/", "_").replace(".", "_")
                path_informe = atlas_dir / f"informe_{nombre_limpio}.md"
                with open(path_informe, "w", encoding="utf-8") as f:
                    f.write(f"# INFORME: {archivo}\n")
                    f.write(f"Generado: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    f.write(informe)
                print(f"   ✅ Guardado con Groq: {path_informe.name}")
            except Exception as e2:
                print(f"   ❌ También falló con Groq: {e2}")
