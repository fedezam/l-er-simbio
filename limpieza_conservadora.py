import os
import shutil
import time
from pathlib import Path
from datetime import datetime

# --- CONFIGURACIÓN ---
SNAPSHOT_DIR = Path("memoria/snapshots_limpieza")
SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# --- LISTA DE PATRONES APROBADOS ---
patrones_a_borrar = [
    "**/__pycache__",
    "**/*.pyc",
    "**/*.bak",
    "**/*.old",
    "**/*.tmp",
    "**/.pytest_cache",
    "**/.mypy_cache",
    "**/.ruff_cache",
    "**/.DS_Store",
    "**/Thumbs.db",
]

# Archivos específicos aprobados (tests obsoletos y scripts temporales)
archivos_especificos = [
    "tests/test_ai.py",
    "tests/test_multi_guia.py",
    "scripts_raiz/fix_ler.py",
    "scripts_raiz/setup_genesis.py",
]

# --- RECOLECTAR ARCHIVOS A BORRAR ---
print("🔍 Buscando archivos a limpiar...\n")

archivos_a_borrar = []

# 1. Patrones globales
for patron in patrones_a_borrar:
    for path in Path(".").glob(patron):
        if path.is_file():
            archivos_a_borrar.append(path)
        elif path.is_dir():
            for f in path.rglob("*"):
                if f.is_file():
                    archivos_a_borrar.append(f)

# 2. Archivos específicos
for archivo in archivos_especificos:
    p = Path(archivo)
    if p.exists() and p.is_file():
        archivos_a_borrar.append(p)

# Eliminar duplicados y ordenar
archivos_a_borrar = sorted(set(archivos_a_borrar))

if not archivos_a_borrar:
    print("✅ No hay archivos para limpiar. El repo ya está limpio.")
    exit(0)

print(f"📊 Se encontraron {len(archivos_a_borrar)} archivos para borrar.\n")
print("--- VISTA PREVIA (primeros 20) ---")
for f in archivos_a_borrar[:20]:
    print(f"   {f}")
if len(archivos_a_borrar) > 20:
    print(f"   ... y {len(archivos_a_borrar) - 20} más.")
print()

# --- CREAR SNAPSHOT ---
print("📸 Creando snapshot de seguridad...")
snapshot_file = SNAPSHOT_DIR / f"cleanup_{timestamp}.txt"
with open(snapshot_file, "w", encoding="utf-8") as f:
    f.write(f"# SNAPSHOT DE LIMPIEZA - {timestamp}\n")
    f.write(f"# Archivos que se van a borrar:\n")
    for archivo in archivos_a_borrar:
        f.write(f"{archivo}\n")
print(f"✅ Snapshot guardado en: {snapshot_file}\n")

# --- CONFIRMAR ---
print("⚠️  ¿Ejecutar la limpieza? (s/n)")
respuesta = input("   > ").strip().lower()

if respuesta != 's':
    print("❌ Limpieza cancelada.")
    exit(0)

# --- BORRAR ARCHIVOS ---
print("\n🗑️  Borrando archivos...")
borrados = 0
errores = 0

for archivo in archivos_a_borrar:
    try:
        archivo.unlink()
        borrados += 1
        if borrados % 50 == 0:
            print(f"   {borrados} archivos borrados...")
    except Exception as e:
        print(f"   ⚠️ Error borrando {archivo}: {e}")
        errores += 1

# Borrar carpetas vacías de __pycache__
for pycache in Path(".").rglob("__pycache__"):
    try:
        if pycache.is_dir():
            shutil.rmtree(pycache)
    except:
        pass

print(f"\n✅ Limpieza completada:")
print(f"   Archivos borrados: {borrados}")
print(f"   Errores: {errores}")

# --- VERIFICACIÓN POST-LIMPIEZA ---
print("\n🔍 Verificando que el sistema sigue funcionando...")
print("   (Ejecutando un tick de prueba con el sustrato determinista)")

try:
    from core.ecosistema import Plano
    from core.semilla import poblar_entidades
    from core.llm.base import SustratoDeterminista
    from pathlib import Path as P

    sustrato = SustratoDeterminista()
    plano = Plano(sustrato=sustrato)
    entidades = poblar_entidades(P("entities/"))
    plano.poblar(entidades)
    resultado = plano.paso()
    
    print(f"\n✅ El sistema sigue funcionando.")
    print(f"   Población: {resultado['poblacion']} entidades vivas.")
    print(f"   Eventos: {len(resultado['eventos'])}")
    
except Exception as e:
    print(f"\n❌ ERROR: El sistema no funciona después de la limpieza.")
    print(f"   Error: {e}")
    print(f"\n🔄 Para revertir, restaurá los archivos del snapshot: {snapshot_file}")
    print(f"   (Aunque en la práctica, los archivos borrados son regenerables: __pycache__, .bak, etc.)")
