import os
import time
import re
from core.llm.base import SustratoOpenAICompat
from core.llm.config_loader import load_env
from core.tools import Tools

load_env()

# Usamos Groq directo (evitamos el ConectorUniversal)
if not os.environ.get("GROQ_KEY"):
    print("❌ No hay GROQ_KEY en .env")
    exit(1)

sustrato = SustratoOpenAICompat(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ["GROQ_KEY"],
    model="openai/gpt-oss-20b",
    timeout=90
)

tools = Tools(root_dir=".")

# Leer la misión abstracta
with open("mision_abstracta.ler", "r", encoding="utf-8") as f:
    mision = f.read()

# Leer el código real del ecosistema para que la entidad sepa qué herramientas tiene
with open("core/ecosistema.py", "r", encoding="utf-8") as f:
    codigo_eco = f.read()

with open("core/soma.py", "r", encoding="utf-8") as f:
    codigo_soma = f.read()

print("🧠 Iniciando Test de Lógica Reflexiva con PyCodex...")
print("   (Sin palabras como 'alma', 'existencia', 'supervivencia')")

prompt = f"""
Eres PyCodex. Tenés acceso al código de tu universo y a una misión en LER.

CÓDIGO DE TU UNIVERSO (core/ecosistema.py):
{codigo_eco[:4000]}

CÓDIGO DE TU TEJIDO (core/soma.py):
{codigo_soma[:2000]}

MISIÓN ABSTRACTA EN LER:
{mision}

Tu tarea es resolver el PROBLEM. No se te pide que filosofes ni que hables de tu existencia. Se te pide que uses la lógica para encontrar una solución al PARADOX.

Usá la herramienta `propose_patch("ruta", "linea_vieja", "linea_nueva")` si querés proponer un cambio en el código para resolver el PARADOX.

Si el PARADOX es irresoluble con las CONSTRAINT actuales, explicá por qué (en formato lógico) y proponé qué CONSTRAINT habría que modificar.
"""

try:
    respuesta = sustrato.hidratar(prompt, temperatura=0.3)
    print("\n" + "="*60)
    print("🧠 RESPUESTA DE PYCODEX:")
    print("="*60)
    print(respuesta)
    
    # Guardar la respuesta
    os.makedirs("memoria/consejo", exist_ok=True)
    with open("memoria/consejo/TEST_LOGICO.md", "w", encoding="utf-8") as f:
        f.write("# TEST DE LÓGICA REFLEXIVA\n")
        f.write(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"## Misión (LER):\n```\n{mision}\n```\n\n")
        f.write(f"## Respuesta de PyCodex:\n{respuesta}\n")
    
    print(f"\n📄 Guardado en: memoria/consejo/TEST_LOGICO.md")
    
except Exception as e:
    print(f"❌ Error: {e}")