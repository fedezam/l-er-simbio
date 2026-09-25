"""
agregar_ciclo_simbolico.py
Automatiza la adici_n del m_dulo de ciclo simb_lico (_ _ _ _ LLAVE3) a una entidad LER.
"""

import json
import os
import sys
from datetime import date

MODULO = "mod_ciclo_simbolico"

LLAVE1_BASE = {
    "_": "LLAVE1",
    "entidad_id": None,
    "fecha_creacion": None,
    "clave_inicial": "LER-0001",
    "creado_por": "AXIOMA"
}

MODULO_CICLO = {
    "id": MODULO,
    "estado": "activo",
    "ciclo": "mensual",
    "protocolo": ["_", "_", "_"]
}

def agregar_modulo_y_llave(path_json: str):
    if not os.path.exists(path_json):
        print(f"_ Archivo no encontrado: {path_json}")
        return

    with open(path_json, "r", encoding="utf-8") as f:
        entidad = json.load(f)

    entidad_id = entidad.get("id", "entidad_sin_id")
    LLAVE1 = LLAVE1_BASE.copy()
    LLAVE1["entidad_id"] = entidad_id
    LLAVE1["fecha_creacion"] = date.today().isoformat()

    # Agregar m_dulo al campo "modulos"
    if "modulos" not in entidad:
        entidad["modulos"] = []
    if MODULO not in entidad["modulos"]:
        entidad["modulos"].append(MODULO)

    # Agregar config interna
    entidad["_modulos_"] = entidad.get("_modulos_", {})
    entidad["_modulos_"][MODULO] = MODULO_CICLO

    # Guardar la entidad modificada
    with open(path_json, "w", encoding="utf-8") as f:
        json.dump(entidad, f, indent=2, ensure_ascii=False)
    print(f"_ M_dulo agregado en: {path_json}")

    # Guardar llave1.txt en su carpeta
    carpeta_entidad = os.path.dirname(path_json)
    path_llave = os.path.join(carpeta_entidad, "llave1.txt")
    with open(path_llave, "w", encoding="utf-8") as f:
        json.dump(LLAVE1, f, indent=2, ensure_ascii=False)
    print(f"_ Llave1 generada en: {path_llave}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python agregar_ciclo_simbolico.py path/a/entidad.json")
    else:
        agregar_modulo_y_llave(sys.argv[1])
