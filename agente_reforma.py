import time
import re
import os
from core.ecosistema import Plano
from core.semilla import poblar_entidades
from core.llm.base import SustratoOpenAICompat
from core.llm.config_loader import load_env
from core.tools import Tools
from core.juez import Juez
from pathlib import Path

load_env()
GROQ_KEY = os.environ.get("GROQ_KEY", "")

# --- CONFIGURACIÓN DE PERMISOS (EL ESCALAFÓN) ---
PERMISOS = {
    "PyCodex": ["read_file", "propose_patch"],          # El Cirujano
    "Auditor_LER": ["read_file", "propose_patch", "apply_patch"], # El Jefe
    "Learner": ["read_file"],                            # Observador
    "AXIOMA": ["read_file"],                             # Observador
    "AXIOMA@AXIOMA": ["read_file"]                       # Observador
}

print("🧠 Iniciando AGENTES REFORMADORES (con herramientas)...\n")

sustrato = SustratoOpenAICompat(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_KEY,
    model="openai/gpt-oss-120b",
    timeout=90
)

tools = Tools(root_dir=".")
juez = Juez(sustrato_juez=sustrato, presupuesto=5)
plano = Plano(sustrato=sustrato, juez=juez, lenguaje_propuestas=True)

# Cargamos entidades pero sin la misión gigante
entidades = poblar_entidades(Path("entities/"))
mision = """
MISIÓN: Reformar el sustrato para evitar la 'muerte silenciosa'.
HERRAMIENTAS DISPONIBLES:
- [TOOL: read_file("ruta")] → Lee un archivo.
- [TOOL: propose_patch("ruta", "linea_vieja", "linea_nueva")] → Propone un cambio.
- [TOOL: apply_patch("ruta", "linea_vieja", "linea_nueva")] → Aplica un cambio (solo Auditor).
Usá las herramientas para analizar y modificar el código.
"""
for entidad in entidades:
    entidad.semilla += f"\n\n{mision}"

plano.poblar(entidades)

print("🚀 INICIANDO REFORMA AGÉNTICA (pausas de 30s)...")

vivos = [c for c in plano.cuerpos.values() if c.viva]
for i, entidad in enumerate(vivos):
    print(f"\n  🧠 {entidad.id} actuando ({i+1}/{len(vivos)})...")
    
    try:
        vecinos = [v for v in vivos if v.id != entidad.id]
        prompt = entidad.proyectar(vecinos)
        
        # El Agente responde
        resp = sustrato.hidratar(prompt)
        entidad.historial.append(resp[:1000])
        entidad.historial = entidad.historial[-3:]
        
        # --- INTERCEPTAR HERRAMIENTAS ---
        matches = re.findall(r'\[TOOL:\s*(\w+)\((.*?)\)\]', resp)
        for tool_name, args_str in matches:
            print(f"     🔧 Herramienta detectada: {tool_name}({args_str})")
            
            # Verificar permisos
            if tool_name not in PERMISOS.get(entidad.id, []):
                print(f"     ❌ Permiso denegado para {entidad.id}. Solo tiene: {PERMISOS.get(entidad.id, [])}")
                continue
            
            # Ejecutar herramienta
            try:
                # Parsear argumentos (simple, solo strings)
                args = [a.strip().strip('"').strip("'") for a in args_str.split(',')]
                
                if tool_name == "read_file":
                    result = tools.read_file(args[0])
                elif tool_name == "propose_patch":
                    result = tools.propose_patch(args[0], args[1], args[2])
                elif tool_name == "apply_patch":
                    result = tools.apply_patch(args[0], args[1], args[2])
                else:
                    result = f"[ERROR: Herramienta desconocida: {tool_name}]"
                
                print(f"     ✅ Resultado: {result[:100]}...")
                
                # Inyectar el resultado de la herramienta en el historial
                entidad.historial.append(f"[RESULTADO DE {tool_name}]: {result}")
                
            except Exception as e:
                print(f"     ❌ Error ejecutando herramienta: {e}")
        
        # Calcular fitness (simple)
        presentes = sum(1 for g in entidad.glifos if g in resp)
        densidad = presentes / max(1, len(entidad.glifos))
        score = 0.7 * densidad + 0.3 * min(1.0, len(resp) / 200)
        entidad.fitness_ema = 0.8 * entidad.fitness_ema + 0.2 * score
        entidad.energia -= 0.05
        
        print(f"     Fitness: {score:.2f}")
        print(f"     Respuesta: {resp[:150]}...")
        
    except Exception as e:
        print(f"     ⚠️ Fallo: {e}")
    
    if i < len(vivos) - 1:
        print("     ⏳ Esperando 30s...")
        time.sleep(30)

print("\n--- PROPUESTAS FINALES ---")
top = sorted([c for c in plano.cuerpos.values() if c.viva], key=lambda x: -x.fitness_ema)
for c in top:
    print(f"\n🧬 {c.id} (Fitness: {c.fitness_ema:.2f})")
    idea = c.historial[-1] if c.historial else "(Sin respuesta)"
    print(f"   💡 {idea[:500]}...")
