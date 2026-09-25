"""Soma: el cuerpo editable de la maquina (el sustrato como tejido vivo).

Principio: una entidad no solo evoluciona DENTRO del plano; las entidades con
capacidad pueden emitir propuestas para modificar el propio plano (el soma).
Pero una propuesta es solo informacion: NUNCA toca codigo fuente. Modifica
parametros vivos del plano, pasa por validacion (guarda + cuarentena), y si
falla, el sistema inmunologico revierte. El ADN (codigo) permanece intacto:
la evolucion somatica es reversible y auditable.

Canales de mutacion somatica (whitelist cerrado):
  umbral_coherencia   que cuenta como "vida"          [0.1 .. 0.9]
  epsilon_mutacion    variabilidad simbolica          [0.0 .. 0.5]
  costo_hidratacion   presion metabolica              [0.01 .. 0.3]
  prioridad:<sustrato> afinidad del conector universal [-1000 .. 100]

Quien propone: cuerpos cuya especialidad declarada lo permite (un PYcodex que
detecta ruido puede proponer subir el umbral; un auditor puede pedir mas
presion metabolica; una entidad puede proponer favorecer el modelo local).
La seleccion hace el resto: una propuesta que mejora el fitness promedio del
linaje proponente se propaga; una que lo hunde, muere con el linaje.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List, Optional

# whitelist: nombre de canal -> (min, max). Lo que no esta aqui es ilegal.
CANALES_SOMATICOS: Dict[str, tuple] = {
    "umbral_coherencia": (0.1, 0.9),
    "epsilon_mutacion": (0.0, 0.5),
    "costo_hidratacion": (0.01, 0.3),
}
_PREFIJO_PRIORIDAD = "prioridad:"


def _rango_de(canal: str) -> Optional[tuple]:
    if canal in CANALES_SOMATICOS:
        return CANALES_SOMATICOS[canal]
    if canal.startswith(_PREFIJO_PRIORIDAD):
        return (-100, 100)
    return None


@dataclass
class Propuesta:
    """Mutacion somatica candidateada por una entidad. Informacion, no accion."""
    id: str                       # <proponente>@<tick>#<seq>
    proponente: str               # id del cuerpo que la emite
    canal: str                    # debe estar en la whitelist
    valor: float                  # valor propuesto (se recorta al rango)
    justificacion: str = ""       # glifos/razones: trazabilidad simbolica
    estado: str = "pendiente"     # pendiente|activa|rechazada|revertida
    valor_anterior: Optional[float] = None

    def clamps(self) -> "Propuesta":
        lo, hi = _rango_de(self.canal) or (0.0, 1.0)
        self.valor = max(lo, min(hi, self.valor))
        return self


@dataclass
class Soma:
    """Tejido editable del plano + historial de sus mutaciones.

    El Plano delega sus parametros vivos aqui. Si un canal no tiene propuesta
    activa, usa el valor por defecto del autor (genoma estable).
    """
    defaults: Dict[str, float]
    activas: Dict[str, Propuesta] = field(default_factory=dict)
    historial: List[Propuesta] = field(default_factory=list)
    registro: List[dict] = field(default_factory=list)   # traza JSONL-ready

    def get(self, canal: str) -> float:
        p = self.activas.get(canal)
        return p.valor if p else self.defaults[canal]

    def candidatos(self, canales: List[str]) -> dict:
        """Snapshot ANTES de aplicar: sirve para revertir."""
        return {c: self.get(c) for c in canales}

    # ---- ciclo de vida de una propuesta -------------------------------- #
    def postular(self, propuesta: Propuesta) -> Propuesta:
        """Guarda somatico: solo canales legales, valores en rango.
        Una propuesta nueva por canal reemplaza a la activa (revision, no caos)."""
        if _rango_de(propuesta.canal) is None:
            propuesta.estado = "rechazada"
            self.registro.append({"evento": "rechazo", "motivo": "canal_ilegal",
                                  **asdict(propuesta)})
        else:
            propuesta.clamps()
            propuesta.estado = "pendiente"
        self.historial.append(propuesta)
        return propuesta

    def aplicar(self, propuesta: Propuesta) -> bool:
        """Activa una propuesta pendiente ya validada. Devuelve True si aplico."""
        if propuesta.estado != "pendiente" or _rango_de(propuesta.canal) is None:
            return False
        anterior = self.get(propuesta.canal)
        propuesta.valor_anterior = anterior
        self.activas[propuesta.canal] = propuesta
        propuesta.estado = "activa"
        self.registro.append({"evento": "activacion", "canal": propuesta.canal,
                              "de": anterior, "a": propuesta.valor,
                              "proponente": propuesta.proponente})
        return True

    def revertir(self, canal: str, motivo: str = "") -> bool:
        """Sistema inmunologico: deshace la ultima mutacion activa del canal."""
        p = self.activas.pop(canal, None)
        if not p:
            return False
        p.estado = "revertida"
        self.registro.append({"evento": "reversion", "canal": canal,
                              "motivo": motivo, "valor": p.valor})
        return True

    def verificacion(self, antes: dict, despues: dict, umbral_caidas: float = 0.25) -> List[str]:
        """¿La mutacion derrumbo el fitness global? Canales sospechosos."""
        culpables = []
        for canal, v_antes in antes.items():
            v_despues = despues.get(canal, v_antes)
            if v_antes > 0 and (v_antes - v_despues) / v_antes > umbral_caidas:
                culpables.append(canal)
        return culpables

    # ---- persistencia: la historia del cuerpo, no solo de las entidades -- #
    def volcar(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            for r in self.registro:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
