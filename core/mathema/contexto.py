# core/mathema/contexto.py

import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class EventoCognitivo:
    tipo: str
    datos: Dict[str, Any]
    timestamp: float
    contexto: Dict[str, Any] = None

class ContextoLER:
    """
    Estado global del sistema cognitivo LER.
    Registra activaciones, flujos, memoria, seguridad y tiempo.
    """

    def __init__(self):
        self.activaciones: Dict[str, int] = {}  # glifo → veces activado
        self.memoria_estable: Dict[str, Any] = {}  # estados persistentes
        self.bloques_protegidos: List[str] = []
        self.bloques_dinamicos: List[str] = []
        self.ciclos_activos: List[Dict[str, Any]] = []
        self.flujos_activos: List[Dict[str, Any]] = []
        self.historia: List[EventoCognitivo] = []
        self.ultima_auditoria: Optional[Dict[str, Any]] = None
        self.tiempo_inicio = time.time()
        self.entidad_activa: Optional[str] = None

    def registrar_activacion(self, glifo: str):
        """Registra que un estado fue activado"""
        self.activaciones[glifo] = self.activaciones.get(glifo, 0) + 1
        self._log('ACTIVACION', {'glifo': glifo})

    def intercambiar_estado(self, a: str, b: str):
        """Registra un intercambio entre dos estados"""
        self._log('INTERCAMBIO', {'a': a, 'b': b})

    def iniciar_flujo(self, origen: str, destino: str):
        """Registra un flujo continuo de transformación"""
        flujo = {
            'origen': origen,
            'destino': destino,
            'inicio': time.time(),
            'activo': True
        }
        self.flujos_activos.append(flujo)
        self._log('FLUJO_INICIADO', flujo)

    def iniciar_ciclo(self, estado: str):
        """Registra un ciclo de repetición evolutiva"""
        ciclo = {
            'estado': estado,
            'inicio': time.time(),
            'iteraciones': 0
        }
        self.ciclos_activos.append(ciclo)
        self._log('CICLO_INICIADO', ciclo)

    def proteger_bloque(self, contenido: str):
        """Registra un bloque inmutable"""
        self.bloques_protegidos.append(contenido)
        self._log('BLOQUE_PROTEGIDO', {'contenido': contenido})

    def registrar_bloque_dinamico(self, contenido: str):
        """Registra un bloque que puede mutar"""
        self.bloques_dinamicos.append(contenido)
        self._log('BLOQUE_MUTABLE', {'contenido': contenido})

    def limpiar_memoria(self):
        """Limpia la memoria temporal (PURGE)"""
        self.memoria_estable.clear()
        self._log('MEMORIA_PURGADA', {})

    def estado_actual(self) -> Dict[str, Any]:
        """Devuelve el estado actual del sistema para auditoría"""
        return {
            'activaciones': dict(self.activaciones),
            'memoria_estable': dict(self.memoria_estable),
            'bloques_protegidos': len(self.bloques_protegidos),
            'bloques_dinamicos': len(self.bloques_dinamicos),
            'ciclos_activos': len(self.ciclos_activos),
            'flujos_activos': len(self.flujos_activos),
            'historia_total': len(self.historia),
            'tiempo_activo': time.time() - self.tiempo_inicio,
            'entidad_activa': self.entidad_activa
        }

    def _log(self, tipo: str, datos: Dict[str, Any]):
        """Registra un evento en la historia cognitiva"""
        evento = EventoCognitivo(
            tipo=tipo,
            datos=datos,
            timestamp=time.time(),
            contexto=self.estado_actual()
        )
        self.historia.append(evento)

    def __str__(self):
        return f"<ContextoLER: {len(self.historia)} eventos, {len(self.activaciones)} activaciones>"