# INFORME: core/ler_parser.py
Generado: 2026-10-22 03:51:38

**1. ¿Qué es este archivo?**  
`core/ler_parser.py` es el módulo central de análisis simbólico del proyecto L‑ER, encargado de interpretar glifos y transformar datos en estructuras tipo árbol.

**2. ¿Qué hace?**  
- Define la enumeración **GlyphType** con los tipos simbólicos.  
- Clase **LERParser**: carga los glifos desde `universal_glyphs.json` y `mmp_core.json`; identifica el tipo de un glifo (`identify_glyph_type`); convierte entidades arbitrarias en árboles (`parse_entity`); extrae secuencias de glifos de texto (`extract_patterns`).  

**3. ¿Cómo se relaciona con el resto del sistema?**  
- Importa `get_config` de `core.config` para localizar los archivos de glifos.  
- Utiliza `json`, `logging`, `re` y `unicodedata`.  
- Provee la lógica que otros componentes (p.ej., visualizadores, generadores de grafos) consumen para interpretar datos simbólicos.

**4. ¿Es esencial o prescindible?**  
Es esencial: constituye la única fuente de conocimiento sobre los glifos y su tipología, y ofrece la transformación estructural que habilita el resto de la cadena de procesamiento (análisis, visualización y generación de grafos). Sin él, el proyecto perdería su capacidad de interpretar y manipular los símbolos L‑ER.