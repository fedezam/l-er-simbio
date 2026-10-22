import os
import time
import random
from core.tools import Tools
from core.llm.base import SustratoOpenAICompat
from core.llm.config_loader import load_env
from pathlib import Path

load_env()
GROQ_KEY = os.environ.get("GROQ_KEY", "")
OPENROUTER_KEY = os.environ.get("OPENROUTER_KEY", "")

if not GROQ_KEY and not OPENROUTER_KEY:
    print("❌ ERROR: No hay claves configuradas.")
    exit(1)

# --- ESTRATEGIA DE FALLBACK ---
# Usamos OpenRouter primero (más tolerante con rate limits), y Groq como respaldo
sustratos = []
if OPENROUTER_KEY:
    sustratos.append({
        "nombre": "OpenRouter",
        "sustrato": SustratoOpenAICompat(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_KEY,
            model="openrouter/free",
            timeout=90
        )
    })
if GROQ_KEY:
    sustratos.append({
        "nombre": "Groq",
        "sustrato": SustratoOpenAICompat(
            base_url="https://api.groq.com/openai/v1",
            api_key=GROQ_KEY,
            model="openai/gpt-oss-120b",
            timeout=90
        )
    })

if not sustratos:
    print("❌ No hay sustratos disponibles.")
    exit(1)

print(f"🧠 Sustratos disponibles: {[s['nombre'] for s in sustratos]}")

# --- FUNCIÓN DE HIDRATACIÓN CON REINTENTOS ---
def hidratar_con_reintentos(prompt, max_reintentos=5):
    for intento in range(max_reintentos):
        for s in sustratos:
            try:
                print(f"      🔄 Intento {intento+1} con {s['nombre']}...")
                resultado = s["sustrato"].hidratar(prompt, temperatura=0.3)
                return resultado
            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "Too Many Requests" in error_str:
                    wait = (2 ** intento) + random.uniform(0, 2)  # Backoff exponencial
                    print(f"      ⏳ Rate limit en {s['nombre']}. Esperando {wait:.1f}s...")
                    time.sleep(wait)
                else:
                    print(f"      ⚠️ Error en {s['nombre']}: {e}")
                    continue
        
        if intento < max_reintentos - 1:
            print(f"      🔁 Reintentando en 10s...")
            time.sleep(10)
    
    return None  # Fallaron todos los reintentos

tools = Tools(root_dir=".")
atlas_dir = Path("memoria/atlas")

# --- ESCANEAR TODOS LOS ARCHIVOS ---
print("\n📂 Escaneando el repositorio completo...")
todos_los_archivos = []
for root, dirs, files in os.walk("."):
    if any(x in root for x in [".git", "__pycache__", "node_modules", ".venv", "venv", "memoria/atlas", "memoria/logs"]):
        continue
    for f in files:
        if f.endswith((".py", ".json", ".md", ".txt", ".toml", ".cfg", ".ini", ".yml", ".yaml")):
            ruta = os.path.join(root, f).replace("./", "")
            todos_los_archivos.append(ruta)

print(f"   Encontrados {len(todos_los_archivos)} archivos.")

# --- FILTRAR LOS QUE YA TIENEN INFORME ---
faltantes = []
for archivo in todos_los_archivos:
    nombre_limpio = archivo.replace("/", "_").replace(".", "_")
    path_informe = atlas_dir / f"informe_{nombre_limpio}.md"
    if not path_informe.exists():
        faltantes.append(archivo)

print(f"   Archivos sin informe: {len(faltantes)}")

if not faltantes:
    print("\n✅ ¡Todos los archivos tienen informe!")
    exit(0)

# --- PROCESAR ---
print(f"\n🐝 INICIANDO CRAWLER RESILIENTE ({len(faltantes)} archivos)...\n")

exitosos = 0
fallidos = 0

for i, archivo in enumerate(faltantes):
    print(f"\n{'='*60}")
    print(f"📄 ANALIZANDO {i+1}/{len(faltantes)}: {archivo}")
    print(f"{'='*60}")
    
    try:
        contenido = tools.read_file(archivo)
        if not contenido or contenido.startswith("[ERROR"):
            print(f"   ⚠️ No se pudo leer. Saltando...")
            fallidos += 1
            continue
        
        contenido_truncado = contenido[:3000]
        print(f"   📖 Leído: {len(contenido)} chars")
        
        prompt = f"""
Eres un Crawler especializado. Analiza el siguiente archivo del repositorio l-er-simbio y genera un mini-informe.

ARCHIVO: {archivo}
CONTENIDO:
{contenido_truncado}

Genera un informe breve y estructurado en Markdown:
1. **¿Qué es este archivo?** (Una línea)
2. **¿Qué hace?** (Funciones o clases principales)
3. **¿Cómo se relaciona con el resto del sistema?** (Imports, dependencias)
4. **¿Es esencial o prescindible?** (Justificación)

Sé conciso. No más de 150 palabras.
"""
        
        print(f"   🧠 Generando mini-informe...")
        informe = hidratar_con_reintentos(prompt)
        
        if informe is None:
            print(f"   ❌ Fallaron todos los reintentos. Saltando...")
            fallidos += 1
            continue
        
        nombre_limpio = archivo.replace("/", "_").replace(".", "_")
        path_informe = atlas_dir / f"informe_{nombre_limpio}.md"
        with open(path_informe, "w", encoding="utf-8") as f:
            f.write(f"# INFORME: {archivo}\n")
            f.write(f"Generado: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(informe)
        
        print(f"   ✅ Guardado: {path_informe.name}")
        exitosos += 1
        
    except Exception as e:
        print(f"   ❌ Error inesperado: {e}")
        fallidos += 1
    
    # Pausa entre archivos (25s)
    if i < len(faltantes) - 1:
        print(f"   ⏳ Esperando 25s...")
        time.sleep(25)

print("\n" + "="*60)
print("🎉 CRAWLER COMPLETADO")
print("="*60)
print(f"   Exitosos: {exitosos}")
print(f"   Fallidos: {fallidos}")
print(f"   Total informes: {len(list(atlas_dir.glob('informe_*.md')))}")
