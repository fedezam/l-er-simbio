# INFORME: entities/pycodex/pycodex.json
Generado: 2026-10-22 03:33:35

## Informe breve – `entities/pycodex/pycodex.json`

| Pregunta | Respuesta |
|----------|-----------|
| **¿Qué es este archivo?** | Archivo JSON que describe la entidad simbólica **PYcodex** dentro del repositorio L‑ER‑Simbio. |
| **¿Qué hace?** | Define metadatos (nombre, tipo, rol, versión), glifos identificadores y lista sus **capacidades** (`analisis_estatico`, `ejecucion_diagnostica`, `evaluacion_reflexiva`, `comunicacion_llm`). Además enumera los **módulos relacionados** que implementan esas capacidades. |
| **¿Cómo se relaciona con el resto del sistema?** | Los módulos citados (`nivel_reflexivo.py`, `sandbox.py`, `sistema_inmune.py`, `modulo_ara.py`) importan esta entidad para obtener su configuración y activar sus funciones de auditoría simbólica. Otros componentes del LER pueden consultar este JSON para descubrir dinámicamente las capacidades de PYcodex. |
| **¿Es esencial o prescindible?** | **Esencial**: actúa como contrato declarativo que permite a todo el sistema reconocer, cargar y coordinar la auditoría reflexiva de PYcodex; sin él, los módulos dependientes perderían la información estructurada necesaria para su operación. |