import re
import os
from pathlib import Path
from core.tools import Tools
from core.llm.conector import ConectorUniversal, Candidato
from core.llm.base import SustratoOpenAICompat, SustratoDeterminista
from core.llm.config_loader import load_env

load_env()
candidatos = []
if os.environ.get("GROQ_KEY"):
    candidatos.append(Candidato(SustratoOpenAICompat(base_url="https://api.groq.com/openai/v1", api_key=os.environ["GROQ_KEY"], model="openai/gpt-oss-120b"), prioridad=10))
candidatos.append(Candidato(SustratoDeterminista(), prioridad=-1000))
conector = ConectorUniversal(candidatos)
tools = Tools(root_dir=".")

def extraer(r):
    m = re.search(r'```(?:python)?\n(.*?)```', r, re.DOTALL)
    return m.group(1).strip() if m else r.strip()

def limpiar_indentacion(texto):
    lineas = texto.split('\n')
    if not lineas:
        return texto
    indentacion = len(lineas[0]) - len(lineas[0].lstrip())
    if indentacion == 0:
        return texto
    return '\n'.join([l[indentacion:] if len(l) >= indentacion and l.startswith(' '*indentacion) else l for l in lineas])

print("🖋️  Pidiendo a PyCodex el código completo en un solo bloque...")
prompt = """
Eres PyCodex. Escribe el código COMPLETO de `core/design_log.py`.
- Clase `DesignLog` (singleton).
- Métodos: `log(entry)`, `record(entry)`, `get_all()`, `find(id)`, `export(path)`.
- Persistencia en JSON.
- Thread-safe.

Escribe TODO el código en un solo bloque de markdown ```python ... ```.
NO agregues texto fuera del bloque. NO uses comillas triples dentro del código.
"""

try:
    respuesta = conector.hidratar(prompt, temperatura=0.3)
    codigo = extraer(respuesta)
    
    if not codigo:
        print("❌ No se pudo extraer el código.")
        exit(1)
    
    codigo = limpiar_indentacion(codigo)
    
    print(f"✅ Código extraído y limpiado ({len(codigo)} caracteres).")
    
    try:
        compile(codigo, "core/design_log.py", "exec")
        print("✅ Sintaxis válida. Escribiendo archivo...")
        result = tools.write_file("core/design_log.py", codigo)
        print(f"   {result}")
        
        with open("memoria/consejo/PYCODEX_LIMPIO.md", "w", encoding="utf-8") as f:
            f.write(f"# PYCODEX LIMPIO\n")
            f.write(f"```python\n{codigo}\n```")
        print(f"📄 Guardado en: memoria/consejo/PYCODEX_LIMPIO.md")
        
    except SyntaxError as e:
        print(f"❌ Error de sintaxis: {e}")
        print(f"   El código tiene {len(codigo)} caracteres.")
        with open("memoria/consejo/PYCODEX_CON_ERROR.md", "w", encoding="utf-8") as f:
            f.write(f"# PYCODEX CON ERROR\n")
            f.write(f"```python\n{codigo}\n```")
        print(f"📄 Guardado en: memoria/consejo/PYCODEX_CON_ERROR.md")
        
except Exception as e:
    print(f"❌ Error: {e}")
