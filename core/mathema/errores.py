# core/mathema/errores.py
"""
Gestión de errores simbólicos para el sistema Mathema v4.0.
Define una jerarquía rica de excepciones y exporta aliases compatibles.
"""

# === CLASE BASE ===
class ErrorMathema(Exception):
    def __init__(self, mensaje: str, linea=None, columna=None):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.linea = linea
        self.columna = columna

    def __str__(self):
        if self.linea is not None and self.columna is not None:
            return f"[L{self.linea}:C{self.columna}] {self.mensaje}"
        return self.mensaje

# === ERRORES LÉXICOS ===
class GlifoInvalido(ErrorMathema):
    def __init__(self, glifo: str, linea=None, columna=None):
        mensaje = f"Glifo inválido: '{glifo}'"
        super().__init__(mensaje, linea, columna)

# === ERRORES SINTÁCTICOS ===
class SintaxisMathemaError(ErrorMathema):
    def __init__(self, mensaje: str, linea=None, columna=None):
        super().__init__(mensaje, linea, columna)

class ContenedorDesbalanceado(ErrorMathema):
    def __init__(self, tipo: str, linea=None, columna=None):
        mensaje = f"Contenedor {tipo} sin cerrar"
        super().__init__(mensaje, linea, columna)

class AnidamientoExcesivo(ErrorMathema):
    def __init__(self, profundidad: int, limite: int, linea=None, columna=None):
        mensaje = f"Anidamiento excesivo: {profundidad} > {limite}"
        super().__init__(mensaje, linea, columna)

class PatronProhibido(ErrorMathema):
    def __init__(self, patron: list, linea=None, columna=None):
        mensaje = f"Patrón prohibido: {' '.join(patron)}"
        super().__init__(mensaje, linea, columna)

# === ERRORES DE EJECUCIÓN ===
class EjecucionMathemaError(ErrorMathema):
    def __init__(self, mensaje: str, linea=None, columna=None):
        super().__init__(mensaje, linea, columna)

class EstadoNoDefinido(EjecucionMathemaError):
    def __init__(self, codigo: str, linea=None, columna=None):
        mensaje = f"Estado no definido: {codigo}"
        super().__init__(mensaje, linea, columna)

class TransformacionInvalida(EjecucionMathemaError):
    def __init__(self, op: str, a: str, b: str, linea=None, columna=None):
        mensaje = f"Transformación inválida: {a} {op} {b}"
        super().__init__(mensaje, linea, columna)

# === ERRORES DE SEGURIDAD ===
class SeguridadMathemaError(ErrorMathema):
    def __init__(self, mensaje: str, comando: str, linea=None, columna=None):
        super().__init__(mensaje, linea, columna)
        self.comando = comando

class SistemaTerminado(SeguridadMathemaError):
    def __init__(self, linea=None, columna=None):
        mensaje = "Ejecución terminada irreversiblemente por ☠ (KILL)"
        super().__init__(mensaje, comando='KILL', linea=linea, columna=columna)

# === 🔁 ALIASES DE COMPATIBILIDAD ===
ErrorLexico = GlifoInvalido
ErrorSintactico = SintaxisMathemaError
ErrorEjecucion = EjecucionMathemaError
