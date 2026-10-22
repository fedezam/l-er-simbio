import os
import re
from core.tools import Tools

tools = Tools(root_dir=".")

# Leer el archivo real
with open("core/ecosistema.py", "r") as f:
    contenido = f.read()

# La línea que sabemos que existe (buscamos por el patrón, no por los espacios)
patron = r"(if c\.edad > 20 and c\.fitness_ema < umbral / 2:)\s*(c\.viva = False)"

# Verificamos si está
if re.search(patron, contenido):
    print("✅ Patrón encontrado en el archivo.")
    # Reemplazar respetando la indentación
    def reemplazar(match):
        indentacion = match.group(0)[:match.group(0).index("if")]
        return f"""{indentacion}if c.edad > 20 and c.fitness_ema < umbral / 2:
{indentacion}    c.energia = 0.1  # hibernación
{indentacion}    c.viva = True  # mantiene la entidad viva"""
    
    nuevo_contenido = re.sub(patron, reemplazar, contenido)
    
    # Hacer snapshot (backup)
    import shutil
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"memoria/snapshots/ecosistema.py.{timestamp}.bak"
    os.makedirs("memoria/snapshots", exist_ok=True)
    shutil.copy("core/ecosistema.py", backup_path)
    print(f"📸 Snapshot creado: {backup_path}")
    
    # Escribir el nuevo contenido
    with open("core/ecosistema.py", "w") as f:
        f.write(nuevo_contenido)
    
    print("✅ Parche aplicado exitosamente.")
    
    # Verificar sintaxis
    try:
        compile(nuevo_contenido, "core/ecosistema.py", "exec")
        print("✅ Sintaxis válida.")
    except SyntaxError as e:
        print(f"❌ Error de sintaxis: {e}. Revirtiendo...")
        shutil.copy(backup_path, "core/ecosistema.py")
        print("🔄 Cambios revertidos.")
else:
    print("❌ Patrón no encontrado. Revisá el archivo manualmente.")
