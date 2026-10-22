# INFORME: core/entity_builder.py
Generado: 2026-10-22 03:52:09

### 1. **¿Qué es este archivo?**
Constructor de entidades a partir de esqueletos JSON, con interfaz de línea de comandos.

### 2. **¿Qué hace?**
- `save_json(path, data)`: serializa datos en JSON con formato UTF-8.
- `build_entity(skeleton_path, force_rebuild)`: carga el esqueleto, crea `./entities/<SEED_NAME>` y genera:
  - `ghost.json`, `plan.json` y `capabilities.json`.
  - Un `runner.py` ejecutable.
- Sustituye IDs `UUID-PLACEHOLDER` por UUID aleatorios y actualiza la marca de tiempo.
- Con `--force`, elimina los archivos existentes de la entidad y la reconstruye.

### 3. **¿Cómo se relaciona con el resto del sistema?**
Usa únicamente librerías estándar (`json`, `uuid`, `pathlib`, `datetime`; `os` no se utiliza). El `runner.py` generado importa `entity_runner.EntityFactory`, que carga y ejecuta los tres JSON produced.

### 4. **¿Es esencial o prescindible?**
Es esencial durante la creación o regeneración de entidades, pero prescindible en la ejecución日常 de una entidad ya generada.