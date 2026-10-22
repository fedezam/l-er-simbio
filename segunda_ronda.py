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

candidatos = []
if GROQ_KEY:
    candidatos.append(Candidato(SustratoOpenAICompat(
        base_url="https://api.groq.com/openai/v1",
        api_key=GROQ_KEY,
        model="openai/gpt-oss-120b",
        timeout=120
    ), prioridad=10))
if OPENROUTER_KEY:
    candidatos.append(Candidato(SustratoOpenAICompat(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_KEY,
        model="openrouter/free",
        timeout=120
    ), prioridad=5))
candidatos.append(Candidato(SustratoDeterminista(), prioridad=-1000))

conector = ConectorUniversal(candidatos)
print(f"✅ Conector inicializado.")

tools = Tools(root_dir=".")

# Leer la auditoría de Auditor_LER
with open("memoria/consejo/AUDITORIA_ARCHIVOS.md", "r", encoding="utf-8") as f:
    auditoria = f.read()

# --- FASE 1: PyCodex corrige los archivos ---
print("\n" + "="*60)
print("🖋️  FASE 1: PyCodex corrige los archivos")
print("="*60)

prompt_pycodex = f"""
Eres PyCodex, el especialista en código del ecosistema LER-Simbio.
Auditor_LER ha revisado tus archivos y los ha RECHAZADO. Esta es su auditoría:

{auditoria[:3000]}

Tu tarea es CORREGIR los archivos basándote en esta auditoría.
Usa la herramienta `write_file("ruta", "contenido")` para reescribir los archivos corregidos.

Corregí:
1. **core/design_log.py** — Implementá la API pública completa (log, record, get_all, find, export).
2. **tests/test_tools.py** — Completá la clase _Flaky y agregá aserciones.

IMPORTANTE: No uses comillas triples dentro del contenido. Usa comillas simples o escapadas.
Escribe el contenido en una sola línea, usando \\n para los saltos de línea.
"""

try:
    respuesta_pycodex = conector.hidratar(prompt_pycodex, temperatura=0.5)
    print("\n🧠 PyCodex está corrigiendo los archivos...")
    print(respuesta_pycodex[:1000] + "...")
    
    matches = re.findall(r'\[TOOL:\s*(\w+)\((.*?)\)\]', respuesta_pycodex, re.DOTALL)
    for tool_name, args_str in matches:
        print(f"\n🔧 Herramienta: {tool_name}")
        if tool_name == "write_file":
            # Parseo simple
            parts = args_str.split(',', 1)
            if len(parts) == 2:
                path = parts[0].strip().strip('"').strip("'")
                content = parts[1].strip().strip('"').strip("'")
                content = content.replace('\\n', '\n').replace('\\t', '\t')
                result = tools.write_file(path, content)
                print(f"   ✅ {result}")
    
    with open("memoria/consejo/PYCODEX_CORRECCION.md", "w", encoding="utf-8") as f:
        f.write(f"# PYCODEX CORRECCIÓN\n")
        f.write(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(respuesta_pycodex)
    
    print(f"\n📄 Guardado en: memoria/consejo/PYCODEX_CORRECCION.md")
    
except Exception as e:
    print(f"❌ Error: {e}")

# --- FASE 2: Auditor_LER re-audita ---
print("\n" + "="*60)
print("🔍 FASE 2: Auditor_LER re-audita")
print("="*60)

archivos = ["core/design_log.py", "tests/test_tools.py"]
contenido = ""
for archivo in archivos:
    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            contenido += f"\n--- {archivo} ---\n{f.read()[:2000]}\n"

prompt_auditor = f"""
Eres Auditor_LER. PyCodex ha corregido los archivos. Auditá de nuevo:

{contenido}

Responde con APROBADO o RECHAZADO para cada archivo.
"""

try:
    re_auditoria = conector.hidratar(prompt_auditor, temperatura=0.3)
    print("\n🔍 Re-auditoría:")
    print(re_auditoria)
    
    with open("memoria/consejo/RE_AUDITORIA.md", "w", encoding="utf-8") as f:
        f.write(f"# RE-AUDITORÍA\n")
        f.write(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(re_auditoria)
    
    print(f"\n📄 Guardado en: memoria/consejo/RE_AUDITORIA.md")
    
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "="*60)
print("🎯 SEGUNDA RONDA COMPLETADA")
print("="*60)
