import os
import time
import re
import json
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

# --- FUNCIÓN PARA PARSEAR ARGUMENTOS DE HERRAMIENTAS ---
def parse_tool_args(args_str: str) -> list:
    """Parsea los argumentos de una herramienta, respetando comillas y saltos de línea."""
    args = []
    current = ""
    in_quotes = False
    quote_char = None
    
    for char in args_str:
        if char in ['"', "'"] and not in_quotes:
            in_quotes = True
            quote_char = char
        elif char == quote_char and in_quotes:
            in_quotes = False
            quote_char = None
        elif char == ',' and not in_quotes:
            args.append(current.strip())
            current = ""
        else:
            current += char
    
    if current:
        args.append(current.strip())
    
    # Limpiar comillas y convertir \n literales a saltos de línea
    cleaned = []
    for arg in args:
        arg = arg.strip()
        if (arg.startswith('"') and arg.endswith('"')) or (arg.startswith("'") and arg.endswith("'")):
            arg = arg[1:-1]
        # Convertir \n literales a saltos de línea reales
        arg = arg.replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"')
        cleaned.append(arg)
    
    return cleaned

# --- FASE 1: PyCodex escribe los archivos ---
print("\n" + "="*60)
print("🖋️  FASE 1: PyCodex escribe los archivos")
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

IMPORTANTE: No uses comillas triples dentro del contenido. Usa comillas simples o escapadas.
Escribe el contenido en una sola línea, usando \\n para los saltos de línea.

Ejemplo:
[TOOL: write_file("core/design_log.py", "import datetime\\n\\nlog = []\\n\\ndef record(decision_id, author, motivation):\\n    entry = {'id': decision_id, 'author': author, 'motivation': motivation, 'timestamp': datetime.datetime.now().isoformat()}\\n    log.append(entry)\\n    return entry")]
"""

try:
    respuesta_pycodex = conector.hidratar(prompt_pycodex, temperatura=0.5)
    print("\n🧠 PyCodex está escribiendo los archivos...")
    print(respuesta_pycodex[:800] + "...")
    
    # Detectar herramientas
    matches = re.findall(r'\[TOOL:\s*(\w+)\((.*?)\)\]', respuesta_pycodex, re.DOTALL)
    for tool_name, args_str in matches:
        print(f"\n🔧 Herramienta: {tool_name}")
        
        if tool_name == "write_file":
            args = parse_tool_args(args_str)
            if len(args) >= 2:
                path = args[0]
                content = args[1]
                result = tools.write_file(path, content)
                print(f"   ✅ {result}")
            else:
                print(f"   ⚠️ Argumentos insuficientes: {args}")
    
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

# Leer los archivos creados para pasárselos al auditor
archivos_creados = ["core/design_log.py", "tests/test_tools.py", "monitor_mutations.py"]
contenido_archivos = ""
for archivo in archivos_creados:
    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            contenido_archivos += f"\n--- {archivo} ---\n{f.read()[:2000]}\n"

prompt_auditor = f"""
Eres Auditor_LER, el especialista en auditoría del ecosistema LER-Simbio.
PyCodex acaba de crear los siguientes archivos:

{contenido_archivos}

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
print("🎯 EJECUCIÓN COMPLETADA")
print("="*60)
print("Verificá los archivos creados con:")
for archivo in archivos_creados:
    if os.path.exists(archivo):
        print(f"  ✅ {archivo} ({os.path.getsize(archivo)} bytes)")
    else:
        print(f"  ❌ {archivo} (no existe)")
