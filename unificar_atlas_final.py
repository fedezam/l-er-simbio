import os
import time
from pathlib import Path

atlas_dir = Path("memoria/atlas")
informes = sorted(atlas_dir.glob("informe_*.md"))

if not informes:
    print("❌ No se encontraron informes.")
    exit(1)

print(f"📚 Unificando {len(informes)} informes en el ATLAS FINAL...\n")

# --- AGRUPAR POR RAMA (detectando automáticamente) ---
ramas = {}
for informe in informes:
    nombre = informe.stem.replace("informe_", "")
    if nombre.startswith("core_"):
        rama = "core"
    elif nombre.startswith("entities_"):
        rama = "entities"
    elif nombre.startswith("glifos_"):
        rama = "glifos"
    elif nombre.startswith("docs_"):
        rama = "docs"
    elif nombre.startswith("historia_"):
        rama = "historia"
    elif nombre.startswith("tools_"):
        rama = "tools"
    elif nombre.startswith("tests_"):
        rama = "tests"
    elif nombre.startswith("arbol_"):
        rama = "arbol"
    elif nombre.startswith("memoria_"):
        rama = "memoria"
    elif nombre.startswith("sandbox_"):
        rama = "sandbox"
    elif nombre.startswith("recursos_") or nombre.startswith("recources_"):
        rama = "recursos"
    elif nombre.startswith("fix_") or nombre.startswith("genesis_") or nombre.startswith("simulacion_") or nombre.startswith("evolucion_") or nombre.startswith("reforma_") or nombre.startswith("consejo_") or nombre.startswith("crawler_"):
        rama = "scripts_raiz"
    else:
        rama = "otros"
    
    if rama not in ramas:
        ramas[rama] = []
    ramas[rama].append(informe)

# --- GENERAR EL ATLAS ---
atlas_content = []
atlas_content.append("# 🧠 ATLAS LER-SIMBIO (COMPLETO)")
atlas_content.append(f"Generado: {time.strftime('%Y-%m-%d %H:%M:%S')}")
atlas_content.append(f"Total de informes: {len(informes)}")
atlas_content.append(f"Ramas cubiertas: {', '.join(sorted(ramas.keys()))}")
atlas_content.append("")
atlas_content.append("---")
atlas_content.append("")

# --- ÍNDICE ---
atlas_content.append("## 📑 ÍNDICE GENERAL")
atlas_content.append("")
for rama in sorted(ramas.keys()):
    archivos = ramas[rama]
    atlas_content.append(f"### {rama.upper()} ({len(archivos)} archivos)")
    for arch in archivos:
        nombre_limpio = arch.stem.replace("informe_", "")
        atlas_content.append(f"- {nombre_limpio}")
    atlas_content.append("")

atlas_content.append("---")
atlas_content.append("")

# --- CONTENIDO POR RAMA ---
for rama in sorted(ramas.keys()):
    archivos = ramas[rama]
    atlas_content.append(f"# 📂 RAMA: {rama.upper()}")
    atlas_content.append("")
    
    for arch in archivos:
        with open(arch, "r", encoding="utf-8") as f:
            contenido = f.read()
        
        lineas = contenido.split("\n")
        contenido_limpio = "\n".join(lineas[3:])
        
        nombre_archivo = arch.stem.replace("informe_", "")
        atlas_content.append(f"## {nombre_archivo}")
        atlas_content.append(contenido_limpio)
        atlas_content.append("")
        atlas_content.append("---")
        atlas_content.append("")

# --- CONCLUSIÓN ---
atlas_content.append("# 🎯 CONCLUSIÓN")
atlas_content.append("")
atlas_content.append("Este Atlas representa el conocimiento completo del ecosistema LER-Simbio.")
atlas_content.append(f"Fue generado por un enjambre de crawlers especializados que analizaron {len(informes)} archivos del repositorio.")
atlas_content.append("")
atlas_content.append("Las entidades pueden usar este documento para:")
atlas_content.append("- Entender su entorno y las reglas que las gobiernan.")
atlas_content.append("- Identificar qué archivos son esenciales y cuáles son prescindibles.")
atlas_content.append("- Proponer cambios informados (PyCodex) y auditarlos (Auditor_LER).")

# --- GUARDAR ---
atlas_path = atlas_dir / "ATLAS_LER_COMPLETO.md"
with open(atlas_path, "w", encoding="utf-8") as f:
    f.write("\n".join(atlas_content))

print(f"✅ Atlas final generado: {atlas_path}")
print(f"   Tamaño: {os.path.getsize(atlas_path) / 1024:.1f} KB")
print(f"   Líneas: {len(atlas_content)}")
print(f"\n--- RESUMEN POR RAMA ---")
for rama in sorted(ramas.keys()):
    print(f"   {rama}: {len(ramas[rama])} archivos")
