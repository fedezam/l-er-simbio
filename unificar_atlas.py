import os
import time
from pathlib import Path

atlas_dir = Path("memoria/atlas")
informes = sorted(atlas_dir.glob("informe_*.md"))

if not informes:
    print("❌ No se encontraron informes para unificar.")
    exit(1)

print(f"📚 Unificando {len(informes)} informes en el ATLAS LER...\n")

# --- Organizar por ramas ---
ramas = {
    "core": [],
    "entities": [],
    "glifos": [],
    "docs": [],
    "historia": [],
    "otros": []
}

for informe in informes:
    nombre = informe.stem  # informe_core_ecosistema_py
    if "core_" in nombre:
        ramas["core"].append(informe)
    elif "entities_" in nombre:
        ramas["entities"].append(informe)
    elif "glifos_" in nombre:
        ramas["glifos"].append(informe)
    elif "docs_" in nombre:
        ramas["docs"].append(informe)
    elif "historia_" in nombre:
        ramas["historia"].append(informe)
    else:
        ramas["otros"].append(informe)

# --- Generar el Atlas ---
atlas_content = []
atlas_content.append("# 🧠 ATLAS LER-SIMBIO")
atlas_content.append(f"Generado: {time.strftime('%Y-%m-%d %H:%M:%S')}")
atlas_content.append(f"Total de informes: {len(informes)}")
atlas_content.append("")
atlas_content.append("---")
atlas_content.append("")
atlas_content.append("## 📑 ÍNDICE")
atlas_content.append("")

for rama, archivos in ramas.items():
    if archivos:
        atlas_content.append(f"- **{rama.upper()}** ({len(archivos)} archivos)")
        for arch in archivos:
            nombre_limpio = arch.stem.replace("informe_", "").replace("_", "/").replace("py", ".py").replace("json", ".json").replace("md", ".md")
            atlas_content.append(f"  - {nombre_limpio}")

atlas_content.append("")
atlas_content.append("---")
atlas_content.append("")

# --- Agregar el contenido de cada rama ---
for rama, archivos in ramas.items():
    if not archivos:
        continue
    
    atlas_content.append(f"# 📂 RAMA: {rama.upper()}")
    atlas_content.append("")
    
    for arch in archivos:
        with open(arch, "r", encoding="utf-8") as f:
            contenido = f.read()
        
        # Limpiar el título del informe para no duplicar
        lineas = contenido.split("\n")
        # Saltamos las primeras líneas (título y fecha)
        contenido_limpio = "\n".join(lineas[3:])
        
        atlas_content.append(f"## {arch.stem.replace('informe_', '').replace('_', '/')}")
        atlas_content.append(contenido_limpio)
        atlas_content.append("")
        atlas_content.append("---")
        atlas_content.append("")

# --- Agregar conclusión ---
atlas_content.append("# 🎯 CONCLUSIÓN")
atlas_content.append("")
atlas_content.append("Este Atlas representa el conocimiento colectivo del ecosistema LER-Simbio.")
atlas_content.append("Fue generado por un enjambre de crawlers especializados, cada uno encargado de una rama del repositorio.")
atlas_content.append("")
atlas_content.append("Las entidades pueden usar este documento para:")
atlas_content.append("- Entender su entorno y las reglas que las gobiernan.")
atlas_content.append("- Identificar qué archivos son esenciales y cuáles son prescindibles.")
atlas_content.append("- Proponer cambios informados (PyCodex) y auditarlos (Auditor_LER).")
atlas_content.append("")
atlas_content.append("**Próximo paso:** Que las entidades lean este Atlas y propongan la primera limpieza del código muerto.")

# --- Guardar el Atlas ---
atlas_path = atlas_dir / "ATLAS_LER.md"
with open(atlas_path, "w", encoding="utf-8") as f:
    f.write("\n".join(atlas_content))

print(f"✅ Atlas generado: {atlas_path}")
print(f"   Tamaño: {os.path.getsize(atlas_path) / 1024:.1f} KB")
print(f"   Líneas: {len(atlas_content)}")
print("")
print("--- VISTA PREVIA ---")
print("\n".join(atlas_content[:50]))
