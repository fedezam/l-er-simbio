# INFORME: core/README_CORE.md
Generado: 2026-10-22 03:56:17

**1. ¿Qué es este archivo?**  
Es el README de la carpeta **/core** del proyecto *LER* que describe su estructura y propósito.

**2. ¿Qué hace?**  
Resume la función de cada módulo (p. ej. `entity_runner.py`, `ler_parser.py`, `sandbox.py`, `glif_engine.py`, etc.), indica los archivos de configuración (`ler.core.json`, `ler_config.json`) y explica conceptos clave como los Glifos Universales y la Ley Sintáctica LER v1.1.

**3. ¿Cómo se relaciona con el resto del sistema?**  
Los módulos listados importan y utilizan recursos externos (`/glifos/glifos_universales.json`, `Mathema`, `GUARDA`) y forman la columna vertebral del núcleo: el *parser*, el *runner*, el *engine* de glifos y los mecanismos de seguridad, registro y sandbox que son consumidos por capas superiores (interfaz, API, etc.).

**4. ¿Es esencial o prescindible?**  
Es esencial como documentación central del núcleo; aunque el código seguiría funcionando sin él, su ausencia dificultaría la comprensión, el onboarding y el mantenimiento del proyecto.