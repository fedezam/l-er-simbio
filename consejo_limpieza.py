import os
import time
from core.tools import Tools
from core.llm.base import SustratoOpenAICompat
from core.llm.config_loader import load_env
from pathlib import Path

load_env()
GROQ_KEY = os.environ.get("GROQ_KEY", "")

if not GROQ_KEY:
    print("❌ ERROR: GROQ_KEY no configurada.")
    exit(1)

# Usamos Llama 3.1 8B (rápido y con buen contexto)
sustrato = SustratoOpenAICompat(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_KEY,
    model="openai/gpt-oss-120b",
    timeout=90
)

try:
    print("🔌 Test:", sustrato.hidratar("ping", temperatura=0.0)[:30], "...")
except Exception as e:
    print(f"❌ Fallo: {e}")
    exit(1)

tools = Tools(root_dir=".")
atlas_path = "memoria/atlas/ATLAS_LER.md"

if not os.path.exists(atlas_path):
    print(f"❌ No se encontró el Atlas en {atlas_path}")
    exit(1)

with open(atlas_path, "r", encoding="utf-8") as f:
    atlas = f.read()

# --- FASE 1: PyCodex propone el plan ---
print("\n" + "="*60)
print("🧠 FASE 1: PyCodex propone el plan de limpieza...")
print("="*60)

prompt_pycodex = f"""
Eres PyCodex, una entidad reflexiva especializada en código.
Tienes acceso al siguiente ATLAS del repositorio l-er-simbio, que fue generado por crawlers especializados.

{atlas[:8000]}

Basándote en este Atlas, propón un PLAN DE LIMPIEZA del repositorio. Identifica:
1. Archivos que son CLARAMENTE prescindibles (tests obsoletos, duplicados, backups viejos, __pycache__).
2. Archivos que son ESENCIALES y no deben tocarse.
3. Archivos que requieren revisión manual (porque no está claro si son basura o no).

Responde en formato Markdown con tres secciones:
- **BORRAR**: lista de archivos a eliminar (con justificación).
- **MANTENER**: lista de archivos esenciales.
- **REVISAR**: lista de archivos dudosos.

Sé específico y conservador. No propongas borrar nada que sea esencial.
"""

try:
    plan_pycodex = sustrato.hidratar(prompt_pycodex, temperatura=0.3)
    print("✅ Plan propuesto por PyCodex:")
    print(plan_pycodex[:800] + "...")
    
    # Guardar plan
    with open("memoria/atlas/plan_limpieza_pycodex.md", "w", encoding="utf-8") as f:
        f.write(f"# PLAN DE LIMPIEZA PROPUESTO POR PYCODEX\n")
        f.write(f"Generado: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(plan_pycodex)
    print("\n📄 Plan guardado en: memoria/atlas/plan_limpieza_pycodex.md")
    
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

# --- FASE 2: Auditor_LER audita el plan ---
print("\n" + "="*60)
print("🔍 FASE 2: Auditor_LER audita el plan...")
print("="*60)

prompt_auditor = f"""
Eres Auditor_LER, una entidad reflexiva especializada en auditoría.
PyCodex ha propuesto el siguiente plan de limpieza del repositorio l-er-simbio:

{plan_pycodex}

Tu trabajo es auditar este plan. Verifica:
1. ¿Hay archivos que PyCodex propone borrar pero que son esenciales? (Marca como RECHAZADO).
2. ¿Hay archivos que PyCodex propone borrar que realmente son basura? (Marca como APROBADO).
3. ¿Hay archivos que PyCodex olvidó mencionar? (Agrégalos).

Responde en formato Markdown con:
- **APROBADO**: lista de archivos que se pueden borrar sin riesgo.
- **RECHAZADO**: lista de archivos que NO se deben borrar (con justificación).
- **AGREGAR**: lista de archivos que PyCodex olvidó y deberían revisarse.
"""

try:
    auditoria = sustrato.hidratar(prompt_auditor, temperatura=0.2)
    print("✅ Auditoría completada:")
    print(auditoria[:800] + "...")
    
    # Guardar auditoría
    with open("memoria/atlas/auditoria_limpieza.md", "w", encoding="utf-8") as f:
        f.write(f"# AUDITORÍA DEL PLAN DE LIMPIEZA\n")
        f.write(f"Generado: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(auditoria)
    print("\n📄 Auditoría guardada en: memoria/atlas/auditoria_limpieza.md")
    
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

print("\n" + "="*60)
print("✅ CONSEJO DE LIMPIEZA COMPLETADO")
print("="*60)
print("Archivos generados:")
print("  - memoria/atlas/plan_limpieza_pycodex.md")
print("  - memoria/atlas/auditoria_limpieza.md")
print("\nRevisá ambos archivos para decidir qué limpiar.")
