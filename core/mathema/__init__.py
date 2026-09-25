# core/mathema/__init__.py

"""
Mathema v4.0 — Motor simbólico del ecosistema LER
==================================================

Este módulo proporciona el núcleo de transformación cognitiva de LER.
Permite parsear y evaluar expresiones simbólicas usando glifos universales.

Ejemplo:
    from core.mathema import parsear, evaluar

    expr = "⟦◌ ⊗ ◑⟧ ⇝ ◊◧"
    ast = parsear(expr)
    resultado = evaluar(ast)

    print(resultado.estado)  # ◊
"""

# Importar componentes clave
from .mathema_ast import Nodo, Estado, Modificador, OperacionBinaria, Flujo, Bloque, Control
from .lexer import lexer
from .parser import parsear
from .visitor import EvaluadorMathema
from .contexto import ContextoLER
from .fallback import a_glifo, a_fallback
from .errores import ErrorSintactico, ErrorEjecucion

# Contexto global compartido
_contexto_global = ContextoLER()
_evaluador_global = EvaluadorMathema(contexto=_contexto_global)

def evaluar(ast: Nodo):
    """
    Evalúa un AST simbólico y devuelve un ResultadoSimbolico.
    
    Args:
        ast (Nodo): Nodo raíz del AST (resultado de `parsear`).
    
    Returns:
        ResultadoSimbolico
    """
    return _evaluador_global.visit(ast)

def obtener_contexto():
    """Devuelve el contexto global del sistema cognitivo."""
    return _contexto_global

def reiniciar_contexto():
    """Reinicia el estado global del sistema."""
    global _contexto_global, _evaluador_global
    _contexto_global = ContextoLER()
    _evaluador_global = EvaluadorMathema(contexto=_contexto_global)

# Exponer versiones
__version__ = "4.0.0"
__sistema__ = "LER-Universal v1.3"