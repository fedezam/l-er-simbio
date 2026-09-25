"""
Tipos y Estructuras de Datos para el Sistema ARA
=================================================

Define las estructuras de datos compartidas entre todos los módulos
del sistema ARA (Autorreparación y Clausura Simbólica).

Estructuras principales:
- NivelARA: Niveles de capacidad de análisis simbólico
- EstadoEntidad: Estados de salud de las entidades
- ResultadoARA: Estructura estándar de resultados de evaluación
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, Any
from datetime import datetime

class NivelARA(Enum):
    """
    Niveles de capacidad de análisis simbólico de las entidades
    
    Determina la complejidad del análisis que puede realizar una entidad
    y los umbrales de alerta correspondientes.
    """
    BAJO = auto()      # Análisis básico de estructura
    MEDIO = auto()     # Análisis semántico y relacional
    ALTO = auto()      # Análisis complejo de coherencia ontológica
    CRITICO = auto()   # Análisis crítico con capacidades de autorreparación

class EstadoEntidad(Enum):
    """
    Estados de salud/operación de una entidad según evaluación ARA
    
    Representa el estado operativo actual de la entidad basado en
    su score de coherencia simbólica y nivel declarado.
    """
    OPERATIVA = auto()    # Funcionamiento normal, sin problemas detectados
    DEGRADADA = auto()    # Funcionamiento comprometido, requiere atención
    INESTABLE = auto()    # Comportamiento errático, riesgo de falla
    FALLA = auto()        # Falla crítica, requiere clausura o reparación

@dataclass
class ResultadoARA:
    """
    Estructura estándar para resultados de evaluación ARA
    
    Contiene toda la información relevante de una evaluación de coherencia
    simbólica, incluyendo métricas, estado determinado y metadatos.
    
    Attributes:
        entidad_id: Identificador único de la entidad evaluada
        score: Puntuación de coherencia simbólica (0.0 - 1.0)
        nivel: Nivel ARA declarado por la entidad
        timestamp: Momento exacto de la evaluación
        estado: Estado operativo determinado por la evaluación
        metadatos: Información adicional sobre la evaluación
    """
    entidad_id: str
    score: float
    nivel: NivelARA
    timestamp: datetime
    estado: EstadoEntidad
    metadatos: Dict[str, Any]
    
    def __post_init__(self):
        """Validación automática de datos tras inicialización"""
        # Validar score en rango válido
        if not (0.0 <= self.score <= 1.0):
            raise ValueError(f"Score debe estar entre 0.0 y 1.0, recibido: {self.score}")
        
        # Asegurar que metadatos existe
        if self.metadatos is None:
            self.metadatos = {}
    
    def es_problematica(self) -> bool:
        """Retorna True si la entidad tiene algún problema operativo"""
        return self.estado != EstadoEntidad.OPERATIVA
    
    def requiere_atencion_inmediata(self) -> bool:
        """Retorna True si la entidad requiere atención crítica inmediata"""
        return self.estado in [EstadoEntidad.INESTABLE, EstadoEntidad.FALLA]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el resultado a diccionario para serialización"""
        return {
            "entidad_id": self.entidad_id,
            "score": self.score,
            "nivel": self.nivel.name,
            "timestamp": self.timestamp.isoformat(),
            "estado": self.estado.name,
            "metadatos": self.metadatos,
            "es_problematica": self.es_problematica(),
            "requiere_atencion_inmediata": self.requiere_atencion_inmediata()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ResultadoARA':
        """Crea un ResultadoARA desde un diccionario"""
        return cls(
            entidad_id=data["entidad_id"],
            score=data["score"],
            nivel=NivelARA[data["nivel"]],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            estado=EstadoEntidad[data["estado"]],
            metadatos=data.get("metadatos", {})
        )