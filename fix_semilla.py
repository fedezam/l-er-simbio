import re

path = 'core/semilla.py'
with open(path, 'r', encoding='utf-8') as f:
    code = f.read()

# Inyectamos un filtro en poblar_entidades para ignorar configs
old_func = """    for p in sorted(Path(base).rglob("*.json")):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                continue
            c = sembrar_desde_json(p)"""

new_func = """    for p in sorted(Path(base).rglob("*.json")):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                continue
            
            # FILTRO: Ignorar archivos de configuración (solo entidades reales)
            tipo = data.get("tipo", "")
            if tipo not in ("entidad_reflexiva", "aprendiz"):
                continue
            
            c = sembrar_desde_json(p)"""

if old_func in code:
    code = code.replace(old_func, new_func)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(code)
    print("✅ [FIX 6] Filtro de entidades aplicado en semilla.py")
else:
    print("❌ No se encontró el patrón en semilla.py")
