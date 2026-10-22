# INFORME: fix_ler.py
Generado: 2026-10-22 03:02:01

1. **¿Qué es este archivo?**  
   Script utilitario que aplica correcciones puntuales al código de `l-er-simbio`.

2. **¿Qué hace?**  
   Define `apply_fixes()`, que modifica archivos bajo `core/`:
   - Sustituye MD5 por SHA256 en `entity_runner.py`.
   - Eleva el umbral del Sistema Inmune de 50 a 200 campos.
   - Actualiza `extract_patterns()` y `validate_expression()` en `glifo_engine.py` para tokenizar símbolos mediante normalización Unicode y expresiones regulares.  
   El contenido proporcionado aparece truncado antes de completar posibles operaciones finales.

3. **¿Cómo se relaciona con el resto del sistema?**  
   Solo importa `os`. Depende de la existencia y estructura de `core/entity_runner.py`, `core/sistema_inmune.py` y `core/glifo_engine.py`; usa rutas relativas y reemplazo textual directo.

4. **¿Es esencial o prescindible?**  
   Es prescindible en tiempo de ejecución: es una herramienta de mantenimiento. Puede ser útil para aplicar o replicar parches, aunque el fragmento incompleto debería revisarse antes de ejecutarlo.