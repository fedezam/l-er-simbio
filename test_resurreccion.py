import os
from core.ecosistema import Plano, Cuerpo
from core.llm.base import SustratoOpenAICompat
from core.llm.config_loader import load_env
from core.soma import Soma

load_env()

sustrato = SustratoOpenAICompat(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ["GROQ_KEY"],
    model="openai/gpt-oss-20b",
    timeout=90
)

print("🧪 TEST DE RESURRECCIÓN (FORZADA MANUALMENTE)")

plano = Plano(sustrato=sustrato, soma=Soma(defaults={}), lenguaje_propuestas=True)

entidad = Cuerpo(
    id="PyCodex_Test",
    glifos=["Δ", "∞", "⊗"],
    semilla="Eres PyCodex. Estás en modo resurrección. Tenés una última oportunidad para proponer un cambio al soma antes de ser archivado. Usá tu herramienta propose_patch o proponé un cambio en los parámetros del soma.",
    energia=0.1,
    fitness_ema=0.01,
    edad=21,
    especialidad="codigo",
    viva=False,  # Forzamos que esté "muerta" (archivada)
    resucitando=True  # Forzamos el flag de resurrección
)

plano.poblar([entidad])

print(f"Estado inicial: viva={entidad.viva}, resucitando={entidad.resucitando}")

# Corremos un tick para que la entidad en resurrección envíe su propuesta
print("\n🚀 Tick 1: entidad en resurrección...")
resultado = plano.paso()
for evento in resultado["eventos"]:
    print(f"  {evento}")

print(f"\nEstado después del tick:")
print(f"  viva={entidad.viva}")
print(f"  resucitando={entidad.resucitando}")
print(f"  fitness={entidad.fitness_ema:.3f}")

# Ver si el soma cambió
print(f"\nParámetros del soma:")
for canal, prop in plano.soma.activas.items():
    print(f"  {canal} = {prop.valor} (por {prop.proponente})")

# Si no hay propuestas, mostrar el historial de la entidad
if not plano.soma.activas:
    print("\n⚠️ No hubo propuestas. Historial de la entidad:")
    for h in entidad.historial:
        print(f"  {h[:200]}")