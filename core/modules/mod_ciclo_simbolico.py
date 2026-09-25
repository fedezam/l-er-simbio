"""
mod_ciclo_simbolico.py
M_dulo LER que implementa el ciclo de activaci_n simb_lica con LLAVE1/_, hash simb_lico _ y LLAVE3.
Permite controlar acceso reflexivo en ciclos temporales definidos.
"""

from __future__ import annotations
from .base import ModuloBase
from ..glifos import GlosarioMathema
import hashlib
import datetime
import json
import os

class ModuloCicloSimbolico(ModuloBase):
    def __init__(self) -> None:
        super().__init__(
            id="mod_ciclo_simbolico",
            nombre="Ciclo Simb_lico de Activaci_n",
            descripcion="Controla la activaci_n reflexiva por ciclos usando llaves simb_licas (_ _ _ _ LLAVE3).",
            activadores=["_", "_", "_"],
            atributos={
                "requiere_llave1": True,
                "modo_ciclo": "mensual",
                "hash_actual": None,
                "activo": False
            },
            nivel_reflexividad="R++"
        )

    def inicializar(self, entidad: dict) -> None:
        super().inicializar(entidad)
        entidad.setdefault("_seguridad_simb_lica_", {})
        entidad["_seguridad_simb_lica_"]["estado"] = "inicializado"

    def generar_hash_simbolico(self, entidad_id: str) -> str:
        """Genera hash simb_lico _nico a partir del ID + glifos n_cleo + fecha."""
        base = f"{entidad_id}|_|_|{datetime.date.today().isoformat()}"
        return hashlib.sha256(base.encode("utf-8")).hexdigest()

    def verificar_llave3(self, hash_simbolico: str, llave3: str) -> bool:
        """Verifica si la llave3 corresponde al hash esperado (por el proveedor)."""
        clave_secreta = "LER-SALT-0425"  # Puede variarse o cifrarse m_s
        esperado = hashlib.sha256((hash_simbolico + clave_secreta).encode()).hexdigest()
        return esperado == llave3

    def cargar_llave1(self, path_llave: str) -> dict:
        """Carga y valida llave1 (_) desde archivo."""
        if not os.path.exists(path_llave):
            raise FileNotFoundError("No se encontr_ archivo de llave1.txt")
        with open(path_llave, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data

    def ejecutar(self, contexto: dict) -> dict:
        """
        Flujo:
        - Cargar LLAVE1
        - Generar HASH simb_lico _
        - Esperar/verificar LLAVE3
        - Activar ciclo reflexivo
        """
        entidad = contexto.get("entidad", {})
        id_entidad = entidad.get("id", "desconocido")

        try:
            datos_llave1 = self.cargar_llave1(f"entities/{id_entidad}/llave1.txt")
            entidad["_seguridad_simb_lica_"]["llave1"] = datos_llave1
        except Exception as e:
            return {"error": f"Fallo al cargar llave1: {e}"}

        hash_simbolico = self.generar_hash_simbolico(id_entidad)
        entidad["_seguridad_simb_lica_"]["hash__"] = hash_simbolico

        # Simulaci_n: el proveedor devuelve la llave3 para el hash dado
        llave3_esperada = hashlib.sha256((hash_simbolico + "LER-SALT-0425").encode()).hexdigest()

        if self.verificar_llave3(hash_simbolico, llave3_esperada):
            entidad["_seguridad_simb_lica_"]["activo"] = True
            return {
                "estado": "activado",
                "glifos": ["_", "_"],
                "hash__": hash_simbolico,
                "mensaje": "Entidad activada hasta fin de ciclo"
            }
        else:
            return {
                "estado": "letargo",
                "hash__": hash_simbolico,
                "glifos": ["_"],
                "mensaje": "Esperando LLAVE3 v_lida"
            }
