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
tools = Tools(root_dir=".")

def extraer_codigo(respuesta: str) -> str:
    """Extrae el código de un bloque de markdown ```python ... ```"""
    match = re.search(r'```(?:python)?\n(.*?)```', respuesta, re.DOTALL)
    if match:
        return match.group(1).strip()
    return respuesta.strip()

print("\n" + "="*60)
print("🖋️  PyCodex escribiendo core/design_log.py")
print("="*60)

prompt = """
Eres PyCodex, el especialista en código del ecosistema LER-Simbio.
Tu tarea es escribir el código completo de `core/design_log.py`.

Requisitos:
- Clase `DesignLog` (singleton).
- Métodos: `log(entry)`, `record(entry)`, `get_all()`, `find(id)`, `export(path)`.
- Persistencia en JSON.
- Thread-safe.

Escribe el código en un bloque de markdown con ```python ... ```.
No agregues explicaciones fuera del bloque.
"""

try:
    respuesta = conector.hidratar(prompt, temperatura=0.5)
    
    codigo = extraer_codigo(respuesta)
    
    if codigo:
        print(f"✅ Código extraído ({len(codigo)} caracteres)")
        
        result = tools.write_file("core/design_log.py", codigo)
        print(f"   {result}")
        
        try:
            compile(codigo, "core/design_log.py", "exec")
            print("✅ Sintaxis válida.")
        except SyntaxError as e:
            print(f"❌ Error de sintaxis: {e}")
        
        with open("memoria/consejo/PYCODEX_FINAL.md", "w", encoding="utf-8") as f:
            f.write(f"# PYCODEX FINAL\n")
            f.write(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"## Código extraído:\n```python\n{codigo}\n```")
        
        print(f"\n📄 Guardado en: memoria/consejo/PYCODEX_FINAL.md")
    else:
        print("❌ No se pudo extraer el código del bloque markdown.")
        
except Exception as e:
    print(f"❌ Error: {e}")