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

# Crear el pool de modelos
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
candidatos.append(Candidato(SustratoDeterminista(), prioridad=-1000))

conector = ConectorUniversal(candidatos)
print(f"✅ Conector inicializado con {len(candidatos)} modelos.")

tools = Tools(root_dir=".")

# --- FASE 1: PyCodex escribe los archivos ---
print("\n" + "="*60)
print("🖋️  FASE 1: PyCodex escribe los archivos de los parches")
print("="*60)

prompt_pycodex = """
Eres PyCodex, el especialista en código del ecosistema LER-Simbio.
Tu tarea es CREAR los archivos que propusiste en el plan de conciliación.

Tienes la herramienta `write_file("ruta", "contenido")` para crear archivos nuevos.
Úsala para crear los siguientes archivos:

1. **core/design_log.py** — Un módulo para registrar decisiones de diseño.
2. **tests/test_tools.py** — Una suite de tests con pytest para core/tools.py.
3. **monitor_mutations.py** — Un script para monitorear ciclos de mutación.

Escribe el código completo de cada archivo. No dejes placeholders.
Usa la herramienta `write_file` para cada uno.

Ejemplo:
[TOOL: write_file("core/design_log.py", "import datetime\n\nlog = []\n\ndef record(decision_id, author, motivation):\n    entry = {\n        'id': decision_id,\n        'author': author,\n        'motivation': motivation,\n        'timestamp': datetime.datetime.now().isoformat()\n    }\n    log.append(entry)\n    return entry\n")]
"""

try:
    respuesta_pycodex = conector.hidratar(prompt_pycodex, temperatura=0.5)
    print("\n🧠 PyCodex está escribiendo los archivos...")
    print(respuesta_pycodex[:1500] + "...")
    
    # Detectar y ejecutar herramientas
    matches = re.findall(r'\[TOOL:\s*(\w+)\((.*?)\)\]', respuesta_pycodex, re.DOTALL)
    for tool_name, args_str in matches:
        print(f"\n🔧 Herramienta: {tool_name}(...)")
        
        if tool_name == "write_file":
            # Parsear argumentos (ruta y contenido)
            # El contenido puede tener comas y saltos de línea, así que parseamos con cuidado
            parts = args_str.split(',', 1)
            if len(parts) == 2:
                path = parts[0].strip().strip('"').strip("'")
                content = parts[1].strip().strip('"').strip("'")
                # Reemplazar \n literales por saltos de línea reales
                content = content.replace('\\n', '\n').replace('\\t', '\t')
                result = tools.write_file(path, content)
                print(f"   ✅ {result[:300]}...")
    
    # Guardar la respuesta
    with open("memoria/consejo/PYCODEX_ESCRIBIO.md", "w", encoding="utf-8") as f:
        f.write(f"# PYCODEX ESCRIBIÓ LOS ARCHIVOS\n")
        f.write(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(respuesta_pycodex)
    
    print(f"\n📄 Guardado en: memoria/consejo/PYCODEX_ESCRIBIO.md")
    
except Exception as e:
    print(f"❌ Error: {e}")

# --- FASE 2: Auditor_LER audita los archivos creados ---
print("\n" + "="*60)
print("🔍 FASE 2: Auditor_LER audita los archivos creados")
print("="*60)

prompt_auditor = """
Eres Auditor_LER, el especialista en auditoría del ecosistema LER-Simbio.
PyCodex acaba de crear los siguientes archivos:

1. core/design_log.py
2. tests/test_tools.py
3. monitor_mutations.py

Tu tarea es AUDITAR estos archivos. Verifica:
- Que el código sea sintácticamente correcto.
- Que no rompa las reglas del ecosistema.
- Que no tenga dependencias inexistentes.

Responde en Markdown con:
- **APROBADO**: archivos que están listos.
- **RECHAZADO**: archivos que tienen problemas (con justificación).
- **SUGERENCIAS**: mejoras para los archivos aprobados.
"""

try:
    auditoria = conector.hidratar(prompt_auditor, temperatura=0.3)
    print("\n🔍 Auditoría de Auditor_LER:")
    print(auditoria)
    
    with open("memoria/consejo/AUDITORIA_ARCHIVOS.md", "w", encoding="utf-8") as f:
        f.write(f"# AUDITORÍA DE LOS ARCHIVOS CREADOS POR PYCODEX\n")
        f.write(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(auditoria)
    
    print(f"\n📄 Guardado en: memoria/consejo/AUDITORIA_ARCHIVOS.md")
    
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "="*60)
print("🎯 EJECUCIÓN AUTÓNOMA COMPLETADA")
print("="*60)
print("Los archivos creados por PyCodex están en el repo.")
print("La auditoría de Auditor_LER está en memoria/consejo/AUDITORIA_ARCHIVOS.md")
print("\nPodés verificar que los archivos se crearon con:")
print("  ls -la core/design_log.py tests/test_tools.py monitor_mutations.py")
