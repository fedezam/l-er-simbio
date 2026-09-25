"""
/core/mathema/__init__.py
Paquete Mathema – parser, AST y utilidades simbólicas
"""

# Nodos AST
from .ast_mathema import (
    NodoAST,
    NodoOperacion,
    NodoContenedor,
    NodoFractal,
    NodoMutacion,
    NodoGlifo,
    VisorAST,
    TipoNodo
)

# Errores
from .errores import (
    ErrorMathema,
    GlifoInvalido,
    SintaxisMathemaError,
    ContenedorDesbalanceado,
    AnidamientoExcesivo,
    PatronProhibido
)

# Patrones y glifos
from .patrones import (
    PATRON_GLIFO_SIMPLE,
    PATRON_FUNCION,
    PATRON_CONTENEDOR_APERTURA,
    PATRON_CONTENEDOR_CIERRE,
    TOKEN_REGEX,
    GLIFO_REGEX
)

# Parser principal
from .mathema_parser import (
    ParserMathema,
    AnalizadorAST,
    OptimizadorMathema,
    GeneradorMathema,
    ValidadorMathema,
    GlosarioMathema,
    ErrorParseo
)

# Constantes rápidas
__version__ = "1.5.0"
__all__ = [
    # AST
    "NodoAST", "NodoOperacion", "NodoContenedor", "NodoFractal", "NodoMutacion", "NodoGlifo", "VisorAST", "TipoNodo",
    # Errores
    "ErrorMathema", "GlifoInvalido", "SintaxisMathemaError", "ContenedorDesbalanceado", "AnidamientoExcesivo", "PatronProhibido",
    # Patrones
    "PATRON_GLIFO_SIMPLE", "PATRON_FUNCION", "TOKEN_REGEX",
    # Parser y utilidades
    "ParserMathema", "AnalizadorAST", "OptimizadorMathema", "GeneradorMathema", "ValidadorMathema", "GlosarioMathema"
]