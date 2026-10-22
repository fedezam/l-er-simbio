import os
from core.tools import Tools

tools = Tools(root_dir=".")

# El parche exacto que propuso PyCodex (copiado de la salida)
old_line = "if c.edad > 20 and c.fitness_ema < umbral / 2: c.viva = False"
new_line = """if c.edad > 20 and c.fitness_ema < umbral / 2:
                    c.energia = 0.1  # hibernación
                    c.viva = True  # mantiene la entidad viva"""

print("🔧 Aplicando parche propuesto por PyCodex...")
print(f"ANTES: {old_line}")
print(f"DESPUÉS: {new_line}")

resultado = tools.apply_patch("core/ecosistema.py", old_line, new_line)
print(f"\n{resultado}")
