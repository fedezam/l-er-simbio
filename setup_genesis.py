import os

# 1. Inyectar el método extract_patterns faltante en glifo_engine.py
path_engine = 'core/glifo_engine.py'
if os.path.exists(path_engine):
    with open(path_engine, 'r', encoding='utf-8') as f:
        code = f.read()
    
    if 'def extract_patterns' not in code:
        # Lo inyectamos justo antes de is_valid_glyph
        injection = """    def extract_patterns(self, text: str) -> list:
        import re
        import unicodedata
        text = unicodedata.normalize("NFC", text)
        all_symbols = sorted(list(self.glyphs.keys()) + list(self.operators.keys()), key=len, reverse=True)
        pattern = re.compile("|".join(re.escape(g) for g in all_symbols))
        return pattern.findall(text)

    def is_valid_glyph(self, symbol: str) -> bool:"""
        code = code.replace('    def is_valid_glyph(self, symbol: str) -> bool:', injection)
        with open(path_engine, 'w', encoding='utf-8') as f:
            f.write(code)
        print("✅ [FIX A1] Método extract_patterns inyectado en glifo_engine.py")

# 2. Crear carpeta de entidades y los 3 JSONs
os.makedirs('entities', exist_ok=True)

entidades = {
    'entities/pycodex.json': '''{
  "nombre": "PyCodex",
  "tipo": "entidad_reflexiva",
  "especialidad": "codigo",
  "glifos": ["Δ", "∞", "⊗"],
  "capacidades": ["escribir_codigo", "leer_codigo", "ejecutar_codigo"],
  "descripcion": "Entidad especializada en generación y corrección de código Python."
}''',
    'entities/auditor_ler.json': '''{
  "nombre": "Auditor_LER",
  "tipo": "entidad_reflexiva",
  "especialidad": "auditoria",
  "glifos": ["¬", "∧", "⊕"],
  "capacidades": ["analizar_logica", "detectar_errores", "validar_sintaxis"],
  "descripcion": "Entidad especializada en auditar coherencia y detectar fallos lógicos."
}''',
    'entities/learn_nucleo_0.json': '''{
  "nombre": "Learner",
  "tipo": "aprendiz",
  "especialidad": "aprendiz",
  "glifos": ["◌", "◑"],
  "capacidades": ["adaptarse", "observar"],
  "descripcion": "Entidad vacía con alta plasticidad para aprender de otras entidades."
}'''
}

for path, content in entidades.items():
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
print("✅ Entidades del Génesis creadas en /entities")

# 3. Crear el archivo mision.py con el bug lógico
mision_code = '''# mision.py
def sumar_pares(numeros):
    suma = 0
    for num in numeros:
        if num % 2 == 0:
            suma += num
    return suma * 2 # <--- BUG LÓGICO INTENCIONAL

# El test que falla:
assert sumar_pares([1, 2, 3, 4, 5]) == 6, "Fallo: El resultado es incorrecto."
print("¡Misión cumplida! Código correcto.")
'''
with open('mision.py', 'w', encoding='utf-8') as f:
    f.write(mision_code)
print("✅ Archivo mision.py con bug creado.")

# 4. Crear el runner de Genesis (usando SustratoDeterminista para no gastar tokens)
genesis_code = '''from core.ecosistema import Plano
from core.semilla import poblar_entidades
from core.llm.base import SustratoDeterminista
from pathlib import Path

print("Inicializando el Plano...")
sustrato = SustratoDeterminista()
plano = Plano(sustrato=sustrato, lenguaje_propuestas=True)

entidades = poblar_entidades(Path("entities/"))
plano.poblar(entidades)

print(f"Población inicial: {[c.id for c in plano.cuerpos.values()]}")
print("--- INICIANDO TICK 1 ---")

resultado = plano.paso()

for evento in resultado["eventos"]:
    print(f"Evento: {evento}")

print("\\n--- ESTADO DE LAS ENTIDADES ---")
for c in plano.cuerpos.values():
    if c.viva:
        print(f"{c.id}: Energía={c.energia:.2f} | Fitness={c.fitness_ema:.2f} | Glifos={c.glifos}")
'''
with open('genesis.py', 'w', encoding='utf-8') as f:
    f.write(genesis_code)
print("✅ Script genesis.py creado.")

