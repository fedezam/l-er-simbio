# INFORME: core/config.py
Generado: 2026-10-22 03:58:28

### 1. ¿Qué es este archivo?
`core/config.py` es el gestor centralizado de configuración de LER Core, basado en `core/ler.core.json`.

### 2. ¿Qué hace?
- **Clase `LERConfig`:** implementa un patrón Singleton para compartir una única configuración.
- **`load_config()`:** valida y carga el archivo JSON.
- **`_setup_paths()`:** construye rutas absolutas para glifos, memoria, entidades, árbol, documentación y archivos específicos.
- **`ensure_directories()`:** crea los directorios requeridos.
- **Propiedades:** exponen versión, nombre, módulos y operadores matemáticos.

### 3. ¿Cómo se relaciona con el resto del sistema?
Solo importa la biblioteca estándar: `json`, `pathlib.Path` y `typing`. Depende del archivo `ler.core.json` y del sistema de archivos. El resto del sistema puede obtener sus rutas y opciones mediante una instancia de `LERConfig`.

### 4. ¿Es esencial o prescindible?
**Esencial para la operación normal**, porque centraliza la carga de configuración, resuelve rutas y prepara la estructura de almacenamiento. Solo sería prescindible si existiera otro mecanismo equivalente de configuración.