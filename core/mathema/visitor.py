# core/mathema/visitor.py

from dataclasses import dataclass
from typing import Any, Dict, Optional, List
import time

# Importar el AST
from .mathema_ast import (
    Nodo, Estado, Modificador, OperacionBinaria,
    Flujo, Bloque, Control
)
from .errores import ErrorEjecucion, ErrorSintactico
from .fallback import a_fallback

# Importar el contexto global del sistema LER
from .contexto import ContextoLER  
from core.glosario_loader import GLIFOS, SEGURIDAD  # asegurate de crear este loader

# === ESTADO INTERNO DEL EVALUADOR ===

@dataclass
class ResultadoSimbolico:
    """Representa el resultado de una transformación cognitiva"""
    estado: str  # glifo resultante
    meta: Dict[str, Any] = None  # información adicional
    colapsado: bool = False  # si fue observado/manifestado

class EvaluadorMathema:
    """
    Visitor que ejecuta transformaciones simbólicas según las reglas de Mathema v4.0.
    No calcula. Transforma.
    """

    def __init__(self, contexto: ContextoLER = None):
        self.contexto = contexto or ContextoLER()
        self.memoria_temporal = {}  # para estados intermedios
        self.historia = []  # registro de transformaciones
        self.detenido = False
        self.aislado = False

    def visit(self, nodo: Nodo) -> ResultadoSimbolico:
        """Entrada genérica al visitante"""
        if self.detenido:
            raise ErrorEjecucion("Ejecución detenida por ■ (HALT)", nodo.fila, nodo.columna)
        if self.aislado and not isinstance(nodo, Control):
            raise ErrorEjecucion("Sistema aislado: no se permiten transformaciones", nodo.fila, nodo.columna)
        return nodo.accept(self)

    def visit_estado(self, nodo: Estado) -> ResultadoSimbolico:
        """Activación de un estado fundamental"""
        glifo = nodo.glifo
        info = GLIFOS.get(glifo, None) or next((v for v in GLIFOS.values() if v['glifo'] == glifo), None)
        
        if not info:
            raise ErrorEjecucion(f"Estado desconocido: {glifo}", nodo.fila, nodo.columna)

        # Registrar activación
        self.contexto.registrar_activacion(glifo)
        self.historia.append({
            'tipo': 'ACTIVACION',
            'estado': glifo,
            'tiempo': time.time()
        })

        return ResultadoSimbolico(
            estado=glifo,
            meta={
                'codigo': nodo.codigo,
                'nombre': nodo.nombre,
                'dominio': info.get('dominio', 'desconocido')
            },
            colapsado=True
        )

    def visit_modificador(self, nodo: Modificador) -> ResultadoSimbolico:
        """Aplica ↑ (potenciación) o ↓ (atenuación) a un estado"""
        contenido = self.visit(nodo.contenido)
        glifo = contenido.estado

        if nodo.tipo == 'SUP':
            # Potenciación: eleva el estado
            if nodo.nivel is None:
                # ↑ glifo → glifo↑ (simbólico)
                nuevo_glifo = f"{glifo}↑"
            else:
                # ↑[HIGH] glifo → potencia máxima
                nivel = nodo.nivel
                if 'HIGH' in nivel or 'MAX' in nivel:
                    nuevo_glifo = f"{glifo}⇈"
                elif 'TRANSCEND' in nivel:
                    nuevo_glifo = f"{glifo}⇈⇈"
                else:
                    nuevo_glifo = f"{glifo}↑"
            return ResultadoSimbolico(estado=nuevo_glifo, meta={'tipo': 'POTENCIADO', 'nivel': nodo.nivel})
        
        elif nodo.tipo == 'SUB':
            # Atenuación: sumerge el estado
            if nodo.nivel is None:
                nuevo_glifo = f"{glifo}↓"
            else:
                if 'CORE' in nodo.nivel or 'DEEP' in nodo.nivel:
                    nuevo_glifo = f"{glifo}⇊⇊"
                elif 'NULL' in nodo.nivel:
                    return ResultadoSimbolico(estado='∅', meta={'tipo': 'ANULADO'})
                else:
                    nuevo_glifo = f"{glifo}↓"
            return ResultadoSimbolico(estado=nuevo_glifo, meta={'tipo': 'ATENUADO', 'nivel': nodo.nivel})

    def visit_operacion_binaria(self, nodo: OperacionBinaria) -> ResultadoSimbolico:
        """Combina dos estados con un operador cognitivo"""
        izq = self.visit(nodo.izq)
        der = self.visit(nodo.der)

        op = nodo.op

        if op == '⊗':  # Colisión → emergencia
            return ResultadoSimbolico(
                estado='◊',
                meta={
                    'tipo': 'EMERGENCIA',
                    'origen': f"{izq.estado}⊗{der.estado}",
                    'componentes': [izq.estado, der.estado]
                }
            )
        
        elif op == '⊕':  # Fusión → integración
            return ResultadoSimbolico(
                estado=izq.estado,
                meta={
                    'tipo': 'FUSION',
                    'integra': der.estado
                }
            )
        
        elif op == '⇆':  # Intercambio → resonancia
            self.contexto.intercambiar_estado(izq.estado, der.estado)
            return ResultadoSimbolico(
                estado=der.estado,
                meta={'tipo': 'RESONANCIA', 'intercambio': True}
            )
        
        elif op == '+':  # Suma de estados → combinación
            return ResultadoSimbolico(
                estado=f"{izq.estado}+{der.estado}",
                meta={'tipo': 'COMBINACION'}
            )
        
        else:
            # Operador desconocido
            raise ErrorEjecucion(f"Operación cognitiva no soportada: {op}", nodo.fila, nodo.columna)

    def visit_flujo(self, nodo: Flujo) -> ResultadoSimbolico:
        """Ejecuta una transformación o resultado"""
        origen = self.visit(nodo.origen)

        if nodo.tipo == 'RESULT':
            destino = self.visit(nodo.destino)
            # Registro de transformación
            self.historia.append({
                'tipo': 'TRANSFORMACION',
                'origen': origen.estado,
                'destino': destino.estado,
                'tiempo': time.time()
            })
            return destino

        elif nodo.tipo == 'FLOW':
            # Flujo continuo: puede evolucionar
            destino = self.visit(nodo.destino)
            self.contexto.iniciar_flujo(origen.estado, destino.estado)
            return destino

        elif nodo.tipo == 'LOOP':
            # Retroacción: vuelve al origen para reconfiguración
            self.historia.append({
                'tipo': 'LOOP',
                'estado': origen.estado,
                'tiempo': time.time()
            })
            return origen

        elif nodo.tipo == 'CYCLE':
            # Ciclo: oscilación
            self.contexto.iniciar_ciclo(origen.estado)
            return origen

    def visit_bloque(self, nodo: Bloque) -> ResultadoSimbolico:
        """Ejecuta un bloque con semántica de mutabilidad"""
        resultado = self.visit(nodo.contenido)

        if nodo.tipo == 'BLK':
            # Bloque fuerte: inmutable, protegido
            self.contexto.proteger_bloque(resultado.estado)
            return ResultadoSimbolico(
                estado=f"⟦{resultado.estado}⟧",
                meta={'tipo': 'INMUTABLE', 'contenido': resultado.estado}
            )
        
        elif nodo.tipo == 'DYN':
            # Bloque dinámico: puede mutar
            self.contexto.registrar_bloque_dinamico(resultado.estado)
            return ResultadoSimbolico(
                estado=f"⟨{resultado.estado}⟩",
                meta={'tipo': 'MUTABLE', 'contenido': resultado.estado}
            )

    def visit_control(self, nodo: Control) -> ResultadoSimbolico:
        """Ejecuta operadores de seguridad y control"""
        comando = nodo.comando

        if comando == 'HALT':
            self.detenido = True
            self.historia.append({'tipo': 'HALT', 'tiempo': time.time()})
            raise ErrorEjecucion("Ejecución detenida por ■ (HALT)", nodo.fila, nodo.columna)

        elif comando == 'PURGE':
            self.memoria_temporal.clear()
            self.contexto.limpiar_memoria()
            return ResultadoSimbolico(estado='∅', meta={'tipo': 'PURGADO'})

        elif comando == 'ISOLATE':
            self.aislado = True
            self.historia.append({'tipo': 'ISOLATE', 'tiempo': time.time()})
            return ResultadoSimbolico(estado='☒', meta={'tipo': 'AISLADO'})

        elif comando == 'AUDIT':
            # Devuelve estado del sistema
            return ResultadoSimbolico(
                estado='☑',
                meta={
                    'tipo': 'AUDITORIA',
                    'historia': len(self.historia),
                    'detenido': self.detenido,
                    'aislado': self.aislado,
                    'contexto': self.contexto.estado_actual()
                }
            )

        elif comando == 'KILL':
            self.historia.append({'tipo': 'KILL', 'tiempo': time.time()})
            raise ErrorEjecucion("Sistema terminado irreversiblemente por ☠ (KILL)", nodo.fila, nodo.columna)

        else:
            raise ErrorEjecucion(f"Comando de control desconocido: {comando}", nodo.fila, nodo.columna)