# INFORME: entities/codeinsight/mutate_codeinsight.py
Generado: 2026-10-22 03:42:03

### 1. **¿Qué es este archivo?**
Ejecutor auxiliar para que **AuditorLER** aplique de forma segura correcciones automáticas sobre los componentes de **CodeInsight**.

### 2. **¿Qué hace?**
- Crea copias de seguridad en `storage/snapshots` antes de modificar archivos.
- Lee y escribe texto/JSON mediante `read_text`, `write_text`, `load_json` y `save_json`.
- `json_set` actualiza valores JSON condicionalmente.
- `ensure_import` incorpora imports faltantes.
- `python_syntax_ok` valida la sintaxis Python.
- `op_json_set` modifica y vuelve a validar un JSON.

El extracto termina truncado en `op_ensure_import`.

### 3. **¿Cómo se relaciona con el resto del sistema?**
Depende solo de la biblioteca estándar (`json`, `re`, `os`, `shutil`, `sys`, `time` y `pathlib`). Actúa dentro de `entities/codeinsight`, declara el plan `auditor_plan_apply_codeinsight.json` y utiliza `storage/snapshots` para respaldo y trazabilidad.

### 4. **¿Es esencial o prescindible?**
Es **prescindible para el funcionamiento principal** de CodeInsight, pero **relevante para su autosanación**: centraliza mutaciones, validaciones y recuperación ante errores.