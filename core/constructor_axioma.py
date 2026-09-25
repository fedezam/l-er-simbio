"""
M_dulo AXIOMA - Validador de Entidades Reflexivas en LER
========================================================

AXIOMA es el validador ontol_gico central del sistema LER.
Verifica que las entidades cumplan con los requisitos b_sicos
para participar en el ecosistema simb_lico reflexivo.

Funciones principales:
- Validaci_n de estructura ontol_gica de entidades
- Registro de entidades validadas
- Verificaci_n de protocolos reflexivos
- Control de acceso al sistema simb_lico
"""

import datetime
from typing import List, Dict, Any, Optional

class Axioma:
    """
    Validador ontol_gico de entidades reflexivas en LER.
    
    AXIOMA act_a como el guardi_n del sistema, asegurando que
    solo entidades correctamente estructuradas puedan participar
    en el ecosistema simb_lico.
    """
    
    def __init__(self):
        """Inicializa AXIOMA con registros vac_os."""
        self.entidades_validadas: List[str] = []
        self.registro_validaciones: Dict[str, Dict[str, Any]] = {}
        self.timestamp_creacion = datetime.datetime.now()
        print("_ AXIOMA inicializado - Validador ontol_gico activo")
    
    def validar_entidad(self, entidad) -> bool:
        """
        Valida si una entidad cumple con los requisitos ontol_gicos b_sicos.
        
        Requisitos verificados:
        1. glifo_identidad: S_mbolo _nico de identificaci_n
        2. protocolo_reflexivo: Versi_n del protocolo que implementa
        3. responder: M_todo callable para interacci_n
        4. nombre: Identificador textual
        
        Args:
            entidad: Objeto a validar
            
        Returns:
            bool: True si la entidad es v_lida, False en caso contrario
        """
        nombre_entidad = getattr(entidad, 'nombre', 'DESCONOCIDA')
        
        # Definir requisitos ontol_gicos
        requisitos = {
            'glifo_identidad': hasattr(entidad, 'glifo_identidad'),
            'protocolo_reflexivo': hasattr(entidad, 'protocolo_reflexivo'),
            'metodo_responder': callable(getattr(entidad, 'responder', None)),
            'nombre_valido': hasattr(entidad, 'nombre') and entidad.nombre
        }
        
        # Verificar todos los requisitos
        requisitos_cumplidos = all(requisitos.values())
        
        if requisitos_cumplidos:
            # Registrar entidad validada
            if nombre_entidad not in self.entidades_validadas:
                self.entidades_validadas.append(nombre_entidad)
            
            # Guardar detalles de validaci_n
            self.registro_validaciones[nombre_entidad] = {
                'timestamp': datetime.datetime.now(),
                'glifo': getattr(entidad, 'glifo_identidad', ''),
                'protocolo': getattr(entidad, 'protocolo_reflexivo', ''),
                'requisitos_cumplidos': requisitos,
                'estado': 'VALIDADA'
            }
            
            print(f"_ AXIOMA: Entidad '{nombre_entidad}' validada ontol_gicamente")
            print(f"  Glifo: {getattr(entidad, 'glifo_identidad', 'N/A')}")
            print(f"  Protocolo: {getattr(entidad, 'protocolo_reflexivo', 'N/A')}")
            return True
        
        else:
            # Registrar fallo de validaci_n
            fallos = [req for req, cumplido in requisitos.items() if not cumplido]
            
            self.registro_validaciones[nombre_entidad] = {
                'timestamp': datetime.datetime.now(),
                'requisitos_cumplidos': requisitos,
                'fallos': fallos,
                'estado': 'RECHAZADA'
            }
            
            print(f"_ AXIOMA: Entidad '{nombre_entidad}' NO cumple requisitos ontol_gicos")
            print(f"  Fallos detectados: {', '.join(fallos)}")
            return False
    
    def entidades(self) -> List[str]:
        """
        Retorna lista de entidades validadas.
        
        Returns:
            List[str]: Nombres de entidades validadas
        """
        return self.entidades_validadas.copy()
    
    def obtener_registro(self, nombre_entidad: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene el registro completo de validaci_n de una entidad.
        
        Args:
            nombre_entidad: Nombre de la entidad a consultar
            
        Returns:
            Dict con detalles de validaci_n o None si no existe
        """
        return self.registro_validaciones.get(nombre_entidad)
    
    def estado_sistema(self) -> Dict[str, Any]:
        """
        Retorna el estado completo del sistema AXIOMA.
        
        Returns:
            Dict con estad_sticas del sistema
        """
        total_validaciones = len(self.registro_validaciones)
        entidades_aceptadas = len(self.entidades_validadas)
        entidades_rechazadas = total_validaciones - entidades_aceptadas
        
        return {
            'timestamp_creacion': self.timestamp_creacion,
            'total_validaciones': total_validaciones,
            'entidades_aceptadas': entidades_aceptadas,
            'entidades_rechazadas': entidades_rechazadas,
# Refactorizaci_n de la l_nea 134
'tasa_aceptacion': (
    entidades_aceptadas / total_validaciones
    if total_validaciones > 0 else 0
),
            'entidades_validadas': self.entidades_validadas
        }
    
    def limpiar_registros(self):
        """Limpia todos los registros de validaci_n (usar con precauci_n)."""
        self.entidades_validadas.clear()
        self.registro_validaciones.clear()
        print("_ AXIOMA: Registros limpiados")
    
    def __str__(self):
        """Representaci_n textual del estado de AXIOMA."""
        estado = self.estado_sistema()
        return (f"AXIOMA - Validador Ontol_gico LER\n"
                f"Entidades validadas: {estado['entidades_aceptadas']}\n"
                f"Validaciones totales: {estado['total_validaciones']}\n"
                f"Tasa de aceptaci_n: {estado['tasa_aceptacion']:.2%}")
    
    def __repr__(self):
        """Representaci_n t_cnica de AXIOMA."""
        return f"Axioma(entidades_validadas={len(self.entidades_validadas)})"