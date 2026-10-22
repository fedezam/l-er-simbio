# INFORME: core/mathema/__init__.py
Generado: 2026-10-22 04:01:03

## 1. ¿Qué es este archivo?  
Es el paquete de inicialización (`__init__.py`) del motor simbólico **Mathema** de LER.

## 2. ¿Qué hace?  
- Exporta los componentes centrales (AST, lexer, parser, visitor, contexto y errores).  
- Crea un **contexto global** y un **evaluador** compartido.  
- Proporciona la función `evaluar(ast)` que delega al visitor global.  
- Ofrece utilidades para obtener y reiniciar el contexto.  
- Define metadatos de versión (`__version__`, `__sistema__`).

## 3. ¿Cómo se relaciona con el resto del sistema?  
Importa módulos internos (`mathema_ast`, `lexer`, `parser`, `visitor`, `contexto`, `fallback`, `errores`) y los expone como API pública. Otros paquetes del repositorio importarán `parsear`, `evaluar` y los tipos de AST desde aquí para trabajar con expresiones simbólicas.

## 4. ¿Es esencial o prescindible?  
Es **esencial**: actúa como punto de entrada único del motor Mathema, centraliza la configuración global y brinda la interfaz de alto nivel que el resto del ecosistema LER utiliza para parsear y ejecutar expresiones simbólicas. Sin él, el motor no tendría una API coherente ni estado compartido.