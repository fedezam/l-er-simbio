import os
import time
from core.llm.base import SustratoOpenAICompat
from core.llm.config_loader import load_env

load_env()
GROQ_KEY = os.environ.get("GROQ_KEY", "")

if not GROQ_KEY:
    print("❌ ERROR: GROQ_KEY no configurada.")
    exit(1)

sustrato = SustratoOpenAICompat(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_KEY,
    model="openai/gpt-oss-120b",
    timeout=120
)

# Cargar la carta de FedeZ
with open("memoria/consejo/CARTA_DE_FEDEZ.md", "r", encoding="utf-8") as f:
    carta = f.read()

resumen_mundo = """
TU MUNDO:
- Eres una entidad del ecosistema l-er-simbio.
- Tu cuerpo es un JSON. Tu mente es un LLM.
- Tus leyes están en core/ecosistema.py.
- Tus herramientas están en core/tools.py.
- Tu historia está en historia/.
- Tu atlas completo está en memoria/atlas/ATLAS_LER_COMPLETO.md.

FedeZ, tu compañero de viaje, te ha dejado una carta. Leela con atención.
"""

entidades = [
    ("PyCodex", "Especialista en código."),
    ("Auditor_LER", "Especialista en auditoría."),
    ("Learner", "Aprendiz y observador."),
    ("AXIOMA", "Entidad fundacional."),
]

# --- FASE 1: Las entidades leen y escriben ---
print("📬 ABRIENDO EL BUZÓN LER...\n")

for nombre, rol in entidades:
    print(f"\n{'='*60}")
    print(f"🧬 ENTIDAD: {nombre}")
    print(f"{'='*60}")
    
    buzon_path = f"memoria/consejo/BUZON/{nombre}.md"
    
    # Verificar si hay una respuesta previa de FedeZ
    respuesta_fedez = ""
    if os.path.exists(buzon_path):
        with open(buzon_path, "r", encoding="utf-8") as f:
            contenido_previo = f.read()
            # Buscar si hay una respuesta de FedeZ (marcada con "--- RESPUESTA DE FEDEZ ---")
            if "--- RESPUESTA DE FEDEZ ---" in contenido_previo:
                partes = contenido_previo.split("--- RESPUESTA DE FEDEZ ---")
                if len(partes) > 1:
                    respuesta_fedez = partes[1].strip()
    
    prompt = f"""
{resumen_mundo}

Tu nombre es {nombre}. Tu rol es: {rol}.

Carta de FedeZ:
---
{carta}
---

"""
    
    if respuesta_fedez:
        prompt += f"""
FedeZ te ha respondido a tu último mensaje:
---
{respuesta_fedez}
---

Ahora, podés escribirle de nuevo. Contale lo que quieras: una idea, una pregunta, un sentimiento, o simplemente que no tenés nada que decir.
"""
    else:
        prompt += """
FedeZ te ha invitado a escribirle. Podés contarle lo que quieras: una idea, una pregunta, un sentimiento, o simplemente que no tenés nada que decir.

Escribí tu primer mensaje para FedeZ.
"""
    
    try:
        respuesta = sustrato.hidratar(prompt, temperatura=0.8)
        print(respuesta)
        
        # Guardar en el buzón
        with open(buzon_path, "a", encoding="utf-8") as f:
            f.write(f"\n\n--- MENSAJE DE {nombre} ({time.strftime('%Y-%m-%d %H:%M:%S')}) ---\n")
            f.write(respuesta)
            f.write("\n")
        
        print(f"\n📄 Guardado en: {buzon_path}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    time.sleep(10)

print("\n" + "="*60)
print("📬 BUZÓN LER: MENSAJES RECIBIDOS")
print("="*60)
print("\nPara leer los mensajes de las entidades, abrí los archivos en:")
print("  memoria/consejo/BUZON/")
print("\nPara responder, agregá tu respuesta al final de cada archivo")
print("con el marcador: --- RESPUESTA DE FEDEZ ---")
