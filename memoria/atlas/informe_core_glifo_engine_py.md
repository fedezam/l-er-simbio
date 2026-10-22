# INFORME: core/glifo_engine.py
Generado: 2026-10-22 02:44:30

## 1. ¿Qué es este archivo?

`core/glifo_engine.py` implementa el motor simbólico de LER para reconocer, validar, describir y analizar expresiones basadas en glifos y operadores matemáticos.

## 2. ¿Qué hace?

Define la clase `GlyphEngine`, que:

- Obtiene las rutas de configuración mediante `get_config()`.
- Carga `universal_glyphs.json` y `mmp_core.json`.
- Integra los glifos MMP con los universales.
- Define operadores como `+`, `⊗`, `¬`, `Δ`, `∞`, `→`, `⇆`, `∘` y `·`.
- Permite extraer símbolos (`extract_patterns`), comprobarlos (`is_valid_glyph`), describirlos (`glyph_description`), validar expresiones (`validate_expression`), representarlas (`represent_expression`) y analizar su flujo (`analyze_flow`).

**Observación:** `validate_expression()` solo valida los tokens extraídos del conjunto conocido, por lo que difícilmente detectará símbolos desconocidos. Además, la representación y el análisis de flujo dependen de tokens separados por espacios.

## 3. ¿Cómo se relaciona con el resto del sistema?

Depende de `core.config.get_config()` y de los archivos JSON alojados en `cfg.glyphs_path`. Sirve como interfaz entre la configuración centralizada y las funciones simbólicas de LER.

## 4. ¿Es esencial o prescindible?

Es **esencial si LER utiliza representaciones, validaciones o análisis simbólicos**. Técnicamente puede reemplazarse por otro motor, pero eliminarlo rompería esas funcionalidades.