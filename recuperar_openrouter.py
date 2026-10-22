import os
import time
from core.tools import Tools
from core.llm.base import SustratoOpenAICompat
from core.llm.config_loader import load_env
from pathlib import Path

load_env()
OPENROUTER_KEY = os.environ.get("OPENROUTER_KEY", "")

if not OPENROUTER_KEY:
    print("❌ ERROR: OPENROUTER_KEY no configurada.")
    exit(1)

# Usamos el router de OpenRouter (elige el modelo gratis que esté disponible)
sustrato = SustratoOpenAICompat(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_KEY,
    model="openrouter/free",
    timeout=90
)

tools = Tools(root_dir=".")
atlas_dir = Path("memoria/atlas")

archivo = "core/glifo_engine.py"
nombre_limpio = archivo.replace("/", "_").replace(".", "_")
path_informe = atlas_dir / f"informe_{nombre_limpio}.md"

if path_informe.exists():
    print("✅ El informe ya existe.")
    exit(0)

print(f"📄 Analizando: {archivo} con OpenRouter...")

try:
    contenido = tools.read_file(archivo)
    contenido_truncado = contenido[:4000]
    
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
    
    print("🧠 Generando informe...")
    informe = sustrato.hidratar(prompt, temperatura=0.3)
    
    with open(path_informe, "w", encoding="utf-8") as f:
        f.write(f"# INFORME: {archivo}\n")
        f.write(f"Generado: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(informe)
    
    print(f"✅ Guardado: {path_informe}")
    print(f"📄 Vista: {informe[:150]}...")
    
except Exception as e:
    print(f"❌ Error: {e}")
