import os
import time
from core.llm.base import SustratoOpenAICompat
from core.llm.config_loader import load_env
from pathlib import Path

load_env()
GROQ_KEY = os.environ.get("GROQ_KEY", "")
OPENROUTER_KEY = os.environ.get("OPENROUTER_KEY", "")

if not GROQ_KEY and not OPENROUTER_KEY:
    print("❌ ERROR: No hay claves configuradas.")
    exit(1)

# Usamos Groq (gpt-oss-120b) que es más potente para el razonamiento
if GROQ_KEY:
    sustrato = SustratoOpenAICompat(
        base_url="https://api.groq.com/openai/v1",
        api_key=GROQ_KEY,
        model="openai/gpt-oss-120b",
        timeout=120
    )
    print("🧠 Usando Groq (gpt-oss-120b)...")
else:
    sustrato = SustratoOpenAICompat(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_KEY,
        model="openrouter/free",
        timeout=120
    )
    print("🧠 Usando OpenRouter...")

atlas_path = "memoria/atlas/ATLAS_LER_COMPLETO.md"

if not os.path.exists(atlas_path):
    print(f"❌ No se encontró el Atlas en {atlas_path}")
    exit(1)

with open(atlas_path, "r", encoding="utf-8") as f:
    atlas = f.read()

print(f"📚 Atlas cargado: {len(atlas)} caracteres, {atlas.count(chr(10))} líneas.")

# --- FASE 1: PyCodex propone el plan ---
print("\n" + "="*60)
print("🧠 FASE 1: PyCodex propone el plan de limpieza...")
print("="*60)

# Como el Atlas es muy grande (173KB), vamos a darle un resumen de las ramas + los archivos
# para que no sature el contexto
resumen_atlas = """
RESUMEN DEL ATLAS LER-SIMBIO (160 archivos analizados):

RAMAS:
- core: 55 archivos (el corazón del sistema: ecosistema, soma, juez, runner, etc.)
- entities: 29 archivos (las entidades: pycodex, auditor_ler, learn, axioma, etc.)
- glifos: 9 archivos (los diccionarios de símbolos)
- docs: 3 archivos (documentación)
- historia: 5 archivos (narrativa)
- tools: 5 archivos (utilidades)
- tests: 11 archivos (pruebas)
- arbol: 5 archivos (genealogía)
- sandbox: 2 archivos (simulador)
- memoria: 2 archivos (logs y snapshots)
- recursos: 3 archivos (fuentes tipográficas)
- scripts_raiz: 13 archivos (scripts creados durante la sesión)
- otros: 18 archivos (archivos sueltos)

ARCHIVOS CLAVE IDENTIFICADOS COMO ESENCIALES (según el Atlas):
- core/ecosistema.py
- core/soma.py
- core/juez.py
- core/lenguaje.py
- core/runner.py
- core/semilla.py
- core/sistema_inmune.py
- glifos/universal_glyphs.json
- glifos/mmp_core.json
- glifos/mathema.json
- glifos/security_glyphs.json
- entities/pycodex.json
- entities/auditor_ler.json

ARCHIVOS IDENTIFICADOS COMO PRESCINDIBLES:
- Todos los __pycache__ y *.pyc
- Archivos .bak, .old, .tmp
- Tests obsoletos (test_ai.py, test_multi_guia.py, etc. - requieren revisión)
- Scripts temporales creados durante la sesión (fix_ler.py, setup_genesis.py, etc.)
"""

prompt_pycodex = f"""
Eres PyCodex, una entidad reflexiva especializada en código.
Tienes acceso al siguiente resumen del Atlas completo del repositorio l-er-simbio.

{resumen_atlas}

Basándote en este resumen, propón un PLAN DE LIMPIEZA del repositorio. Identifica:
1. Archivos que son CLARAMENTE prescindibles (__pycache__, .bak, tests obsoletos, scripts temporales).
2. Archivos que son ESENCIALES y no deben tocarse (el core, las entidades, los glifos).
3. Archivos que requieren revisión manual (docs, historia, tests dudosos).

Responde en formato Markdown con tres secciones:
- **BORRAR**: lista de archivos/carpetas a eliminar (con justificación).
- **MANTENER**: lista de archivos esenciales.
- **REVISAR**: lista de archivos dudosos.

Sé específico y conservador. No propongas borrar nada que sea esencial.
"""

try:
    plan_pycodex = sustrato.hidratar(prompt_pycodex, temperatura=0.3)
    print("✅ Plan propuesto por PyCodex:")
    print(plan_pycodex[:1000] + "...")
    
    with open("memoria/atlas/plan_limpieza_final_pycodex.md", "w", encoding="utf-8") as f:
        f.write(f"# PLAN DE LIMPIEZA FINAL PROPUESTO POR PYCODEX\n")
        f.write(f"Generado: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(plan_pycodex)
    print("\n📄 Plan guardado en: memoria/atlas/plan_limpieza_final_pycodex.md")
    
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
    print(auditoria[:1000] + "...")
    
    with open("memoria/atlas/auditoria_limpieza_final.md", "w", encoding="utf-8") as f:
        f.write(f"# AUDITORÍA FINAL DEL PLAN DE LIMPIEZA\n")
        f.write(f"Generado: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(auditoria)
    print("\n📄 Auditoría guardada en: memoria/atlas/auditoria_limpieza_final.md")
    
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

print("\n" + "="*60)
print("✅ CONSEJO DE LIMPIEZA FINAL COMPLETADO")
print("="*60)
print("Archivos generados:")
print("  - memoria/atlas/plan_limpieza_final_pycodex.md")
print("  - memoria/atlas/auditoria_limpieza_final.md")
