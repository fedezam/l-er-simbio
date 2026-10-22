import os
import time
from core.llm.conector import ConectorUniversal, Candidato
from core.llm.base import SustratoOpenAICompat, SustratoDeterminista
from core.llm.config_loader import load_env

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

# Leer el archivo que escribió PyCodex
if os.path.exists("core/design_log.py"):
    with open("core/design_log.py", "r", encoding="utf-8") as f:
        contenido = f.read()
    
    print("🔍 Auditor_LER auditando core/design_log.py...")
    
    prompt = f"""
Eres Auditor_LER, el especialista en auditoría del ecosistema LER-Simbio.
PyCodex ha escrito el siguiente código:

{contenido[:4000]}

Tu tarea es auditarlo. Verifica:
- Que el código sea sintácticamente correcto.
- Que implemente la API pública (log, record, get_all, find, export).
- Que sea thread-safe.
- Que no tenga dependencias inexistentes.

Responde con APROBADO o RECHAZADO (con justificación).
"""
    
    try:
        auditoria = conector.hidratar(prompt, temperatura=0.3)
        print("\n🔍 Auditoría:")
        print(auditoria)
        
        with open("memoria/consejo/AUDITORIA_FINAL.md", "w", encoding="utf-8") as f:
            f.write(f"# AUDITORÍA FINAL\n")
            f.write(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(auditoria)
        
        print(f"\n📄 Guardado en: memoria/consejo/AUDITORIA_FINAL.md")
        
    except Exception as e:
        print(f"❌ Error: {e}")
else:
    print("❌ El archivo core/design_log.py no existe.")