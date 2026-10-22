# INFORME: core/mathema/errores.py
Generado: 2026-10-22 04:07:31

### 1. **¿Qué es este archivo?**
Define la jerarquía de excepciones del sistema Mathema v4.0 para gestionar errores simbólicos de forma uniforme.

### 2. **¿Qué hace?**
- `ErrorMathema`: clase base; almacena mensaje, línea y columna.
- `GlifoInvalido`: error léxico.
- `SintaxisMathemaError`, `ContenedorDesbalanceado`, `AnidamientoExcesivo`, `PatronProhibido`: errores sintácticos.
- `EjecucionMathemaError`, `EstadoNoDefinido`, `TransformacionInvalida`: errores de ejecución.
- `SeguridadMathemaError`, `SistemaTerminado`: errores de seguridad.
- `ErrorLexico`, `ErrorSintactico`, `ErrorEjecucion`: aliases de compatibilidad.

### 3. **¿Cómo se relaciona con el resto del sistema?**
No realiza imports ni depende de otros módulos del repositorio; solo utiliza `Exception` de Python. Sus clases están preparadas para ser importadas y capturadas por lexer, parser, evaluador y componentes de seguridad.

### 4. **¿Es esencial o prescindible?**
Es **esencial para la gestión centralizada y consistente de errores**. Sus aliases también看来 son parte de la API pública; quitarlo requeriría adaptar los módulos consumidores.