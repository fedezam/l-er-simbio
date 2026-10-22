# INFORME: core/tools.py
Generado: 2026-10-22 03:56:45

## Mini‑informe de `core/tools.py`

| Pregunta | Respuesta |
|----------|-----------|
| **¿Qué es este archivo?** | Módulo de utilidades que gestiona lectura de archivos y aplicación de parches con snapshots. |
| **¿Qué hace?** | - **Clase `Tools`**: inicializa rutas de proyecto y carpeta de snapshots.<br> - `read_file`: devuelve el contenido de un archivo o error.<br> - `propose_patch`: genera un mensaje descriptivo de un cambio propuesto.<br> - `apply_patch`: crea backup, sustituye una línea, verifica sintaxis (si es *.py*) y revierte en caso de error. |
| **¿Cómo se relaciona con el resto del sistema?** | No importa módulos externos salvo la biblioteca estándar (`os`, `shutil`, `importlib.util`, `datetime`, `pathlib`). Es probable que sea usado por scripts de mantenimiento, auditoría o CI que necesiten modificar código de forma controlada. |
| **¿Es esencial o prescindible?** | **Esencial** para operaciones de parcheo seguro y auditoría de código; sin él, la aplicación de cambios y la creación de snapshots tendría que implementarse de forma ad‑hoc en varios lugares. |