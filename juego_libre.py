import os
import time
import json
from core.ecosistema import Plano
from core.semilla import poblar_entidades
from core.llm.base import SustratoOpenAICompat
from core.llm.config_loader import load_env
from core.soma import Soma
from pathlib import Path

load_env()

sustrato = SustratoOpenAICompat(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ["GROQ_KEY"],
    model="openai/gpt-oss-20b",
    timeout=90
)

print("🎲 INICIANDO SIMULACIÓN DE JUEGO LIBRE (10 ticks)...")
print("   Las entidades deciden qué hacer en cada tick. Sin instrucciones humanas.")
print("="*60)

# Creamos el plano con soma (para que puedan proponer cambios)
plano = Plano(sustrato=sustrato, soma=Soma(defaults={}), lenguaje_propuestas=True)

# Cargamos las entidades reales
entidades = poblar_entidades(Path("entities/"))
plano.poblar(entidades)

# Para que sea rápido, forzamos un poco de energía inicial
for c in plano.cuerpos.values():
    c.energia = 0.8

# --- BUCLE DE JUEGO LIBRE ---
for tick in range(1, 11):
    print(f"\n{'='*60}")
    print(f"🎮 TICK {tick}")
    print(f"   Vivos: {sum(1 for c in plano.cuerpos.values() if c.viva)} | "
          f"Archivados: {sum(1 for c in plano.cuerpos.values() if not c.viva)}")
    print(f"{'='*60}")
    
    # Le damos el control a las entidades (esto dispara _proponer y _derivar)
    resultado = plano.paso()
    
    # Mostramos lo que pasó (eventos importantes)
    for evento in resultado["eventos"]:
        if evento[0] in ['nacimiento', 'extincion', 'mutacion', 'propuesta_somatica', 'resurreccion', 'consolidacion']:
            print(f"  🌟 {evento}")
            
    # Mostramos las propuestas que hicieron las entidades (si las hay)
    if plano.soma.activas:
        print(f"  🧬 Soma actual: {dict((k, v.valor) for k, v in plano.soma.activas.items())}")
    
    # Pausa entre ticks para no saturar
    time.sleep(10)

print("\n" + "="*60)
print("🏁 SIMULACIÓN TERMINADA")
print("="*60)

# Resumen final
vivos = [c for c in plano.cuerpos.values() if c.viva]
print(f"Supervivientes: {[c.id for c in vivos]}")
print(f"Fitness promedio: {sum(c.fitness_ema for c in vivos) / max(1, len(vivos)):.3f}")
print(f"\nHistorial de propuestas somáticas:")
for prop in plano.soma.historial:
    print(f"  {prop.proponente} -> {prop.canal} = {prop.valor} ({prop.estado})")