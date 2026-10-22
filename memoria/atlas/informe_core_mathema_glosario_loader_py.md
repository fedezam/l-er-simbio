# INFORME: core/mathema/glosario_loader.py
Generado: 2026-10-22 04:05:51

## Mini‑informe : `core/mathema/glosario_loader.py`

| # | Pregunta | Respuesta |
|---|----------|-----------|
| **1. ¿Qué es este archivo?** | Módulo que carga y gestiona los *glifos* (símbolos) del proyecto. |
| **2. ¿Qué hace?** | - **`cargar_glifos()`**: lee `glifos_universales.json` y devuelve un diccionario.<br>- **`GLIFOS`**: constante con el contenido cargado.<br>- **`SEGURIDAD`**: diccionario de comandos críticos.<br>- **`GlifoEngine`**: clase con métodos `get_glifo_info(glifo)` y `get_codigo_info(codigo)` para buscar símbolos o códigos en los glifos y en los comandos de seguridad. |
| **3. ¿Cómo se relaciona con el resto del sistema?** | Importa `json` y `os`; depende del archivo JSON en `../glifos/glifos_universales.json`. Otros componentes que necesiten interpretar o mostrar glifos (por ejemplo, módulos de UI, parsers o lógica cognitiva) usarán `GlifoEngine`. |
| **4. ¿Es esencial o prescindible?** | **Esencial**: centraliza la carga y búsqueda de los glifos y comandos de seguridad, evitando duplicación y garantizando consistencia en todo el proyecto. Sin él, cada módulo tendría que leer el JSON y replicar la lógica de búsqueda. |