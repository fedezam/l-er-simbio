import time
import os
from core.ecosistema import Plano
from core.semilla import poblar_entidades
from core.llm.base import SustratoDeterminista  # Usamos determinista para ir rápido
from pathlib import Path

print("🧪 TEST: Verificando la nueva ley de hibernación...")
print("=" * 60)

# Cargamos el plano con el sustrato determinista (rápido y sin rate limit)
sustrato = SustratoDeterminista()
plano = Plano(sustrato=sustrato)

entidades = poblar_entidades(Path("entities/"))
plano.poblar(entidades)

print(f"Población inicial: {[c.id for c in plano.cuerpos.values()]}")
print()

# Forzamos que las entidades tengan fitness bajo y edad alta
# para que el ecosistema intente matarlas
for c in plano.cuerpos.values():
    c.edad = 25
    c.fitness_ema = 0.1
    print(f"🔴 {c.id}: edad={c.edad}, fitness={c.fitness_ema:.2f} (candidata a extinción)")

print("\n🚀 Corriendo 1 tick...")
resultado = plano.paso()

print("\n--- EVENTOS ---")
for evento in resultado["eventos"]:
    print(f"  {evento}")

print(f"\n--- ESTADO POST-TICK ---")
for c in plano.cuerpos.values():
    if c.viva:
        print(f"🟢 {c.id}: VIVA (energía={c.energia:.2f})")
    else:
        print(f"💀 {c.id}: EXTINTA")

print("\n" + "=" * 60)
print("VEREDICTO:")
extintas = sum(1 for c in plano.cuerpos.values() if not c.viva)
if extintas == 0:
    print("✅ ÉXITO: Ninguna entidad murió. La hibernación funciona.")
else:
    print(f"❌ FALLO: {extintas} entidades murieron. El parche no se aplicó bien.")
print("=" * 60)
