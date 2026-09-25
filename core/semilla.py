"""Sembrador: convierte entidades LER declarativas en Cuerpos del plano.

Una entidad JSON (auditor_ler.json, ghost_auditor.json, AXIOMA/*.json...) es
solo informacion: aqui se "plana" a texto hidratable. El sustrato (cualquier
LLM) decide si esa informacion cobra vida; el codigo solo mide coherencia.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import List

from core.ecosistema import Cuerpo

# glifos canonicos de cada linaje (mutables por el plano via epsilon)
GLIFOS_POR_TIPO = {
    "entidad_reflexiva": ["⟁", "∆"],
    "axioma": ["Δ", "∞"],
    "aprendiz": ["∘", "+"],
}


def _aplanar(obj, prefijo: str = "") -> List[str]:
    lineas = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("api_key", "conexion_llm"):  # la entidad es agnostica: sin modelo
                continue
            lineas += _aplanar(v, f"{prefijo}{k}.")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            lineas += _aplanar(v, f"{prefijo}{i}.")
    else:
        s = str(obj)
        if s and s != "{}":
            lineas.append(f"{prefijo.rstrip('.')}={s}")
    return lineas


def sembrar_desde_json(ruta: Path) -> Cuerpo:
    data = json.loads(Path(ruta).read_text(encoding="utf-8"))
    nombre = data.get("nombre", Path(ruta).stem)
    tipo = data.get("tipo", "entidad_reflexiva")
    cuerpo = "\n".join(_aplanar(data))[:2000]
    semilla = (
        f"SOY {nombre} ({tipo}).\n"
        f"Habita esta identidad y responde desde ella, manteniendo sus glifos.\n"
        f"DEFINICION:\n{cuerpo}"
    )
    return Cuerpo(id=nombre, glifos=list(GLIFOS_POR_TIPO.get(tipo, ["·"])), semilla=semilla)


def poblar_entidades(base: Path) -> List[Cuerpo]:
    """Siembra todas las entidades JSON declaradas bajo entities/.

    Un archivo con glifos propios (glifo_identidad / glifos) se siembra con
    ellos; los demas heredan el alfabeto simbolico de su linaje.
    """
    cuerpos, vistos = [], {}
    for p in sorted(Path(base).rglob("*.json")):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                continue
            c = sembrar_desde_json(p)
            if not c.semilla.strip():
                continue
            if "AXIOMA/" in str(p).replace("\\", "/"):
                c.glifos = ["Δ", "∞"]  # linaje axiomático
            # colision de nombres: la variante mutada es otra entidad
            if c.id in vistos:
                c.id = f"{c.id}@{p.parent.name}"
                c.glifos = list(dict.fromkeys(c.glifos + [p.parent.name[:1].upper()]))
            vistos[c.id] = True
            cuerpos.append(c)
        except Exception:
            continue  # JSON corrupto/vacio = no-nacida, no error
    return cuerpos
