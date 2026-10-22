#!/bin/bash
cat << 'PYEOF' > fases.py
import os, time, re
from core.llm.conector import ConectorUniversal, Candidato
from core.llm.base import SustratoOpenAICompat, SustratoDeterminista
from core.llm.config_loader import load_env
from core.tools import Tools

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

print("Fase 1: Estructura...")
p1 = "Escribe la estructura básica de core/design_log.py (imports, clase DesignLog, __init__, _load, _dump). NO escribas los métodos públicos. Usa bloque ```python ... ```."
c1 = extraer(conector.hidratar(p1))

print("Fase 2: Métodos log, record, get_all...")
p2 = f"Este es el código actual:\n```python\n{c1}\n```\nAgrega los métodos log(entry), record(entry), get_all() a la clase. No repitas el código anterior. Usa bloque ```python ... ```."
c2 = extraer(conector.hidratar(p2))

print("Fase 3: Métodos find, export, cierre...")
p3 = f"Este es el código actual:\n```python\n{c1}\n{c2}\n```\nAgrega los métodos find(entry_id), export(path) y cierra la clase. Usa bloque ```python ... ```."
c3 = extraer(conector.hidratar(p3))

codigo = c1 + "\n\n" + c2 + "\n\n" + c3
try:
    compile(codigo, "core/design_log.py", "exec")
    print("✅ Sintaxis válida")
except SyntaxError as e:
    print(f"❌ Error de sintaxis: {e}")

print(tools.write_file("core/design_log.py", codigo))
PYEOF
echo "✅ fases.py creado."
