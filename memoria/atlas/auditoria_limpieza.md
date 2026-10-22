# AUDITORÍA DEL PLAN DE LIMPIEZA
Generado: 2026-10-22 02:48:01

## Auditoría del plan de limpieza propuesto por PyCodex  

A continuación se revisan los ítems del plan y se indica, con la justificación correspondiente, si pueden ser eliminados sin riesgo, si deben conservarse o si hay archivos que no aparecen en la propuesta y que deberían considerarse.

---

### **✅ APROBADO** – Archivos / carpetas que **sí pueden borrarse**  

| Ruta / patrón | Motivo de la aprobación |
|---------------|------------------------|
| `**/__pycache__/` | Carpetas generadas automáticamente por el intérprete de Python. No contienen código fuente. |
| `**/*.pyc` | Archivos byte‑code compilado; se regeneran al ejecutar. |
| `**/*.bak` , `**/*.old` , `**/*_backup.*` | Copias de seguridad creadas por editores o scripts; no forman parte del proyecto. |
| `docs/_site/` (si existe) | Salida estática de generadores de documentación (MkDocs, Sphinx, etc.). Se vuelve a generar cuando sea necesario. |
| `docs/.cache/` (si existe) | Cache interno de la herramienta de documentación. |
| `README~` , `README.txt~` , `*.tmp` | Archivos temporales típicos de editores. |
| `*.log` (si aparecen en el árbol) | Registros de ejecución que pueden ser recreados. |
| `*.DS_Store` / `Thumbs.db` | Metadatos de sistemas operativos, sin valor para el código. |

> **Nota:** Cada patrón se aplica recursivamente (`**/`) para cubrir cualquier nivel de profundidad.

---

### **❌ RECHAZADO** – Archivos / carpetas que **NO deben borrarse** (esenciales o con riesgo)  

| Ruta | Justificación |
|------|----------------|
| `tests/` (cuando **no está vacío** o contiene pruebas útiles) | El plan sugiere borrarlo solo “si está vacío o contiene pruebas obsoletas”. Si el directorio contiene pruebas unitarias, de integración o ejemplos, su eliminación rompería la capacidad de validar el motor y dificultaría el desarrollo futuro. Se debe inspeccionar su contenido antes de decidir. |
| `core/glifo_engine.py` **o** `core/glifo/engine.py` (según la estructura real) | Este archivo está listado como **esencial** en la tabla “MANTENER”. Si la ruta real es `core/glifo_engine.py` y el plan lo incluye en “BORRAR” por error, se perdería el motor de reconocimiento de glifos. Verificar la ubicación exacta y conservarlo. |
| `core/semilla.py` (aunque está en “MANTENER”, el plan sugiere revisarlo) | Si contiene lógica de carga de semillas que es usada por `core/runner.py`, su eliminación impediría la inicialización de entidades. Mantenerlo; solo revisar funciones auxiliares no usadas. |
| `core/sistema/inmune.py` (si no está referenciado) | El plan lo coloca en “MANTENER”, pero advierte revisar su uso. **No** borrarlo sin confirmar que no es importado por `core/ecosistema.py` u otros módulos; podría romper funcionalidades de inmunidad. |
| `glifos/mathema.json` y `glifos/security/glyphs.json` (si son cargados dinámicamente) | Aunque están en “REVISAR”, si el motor los busca por nombre (p.ej. `mathema` o `security`) su eliminación provocaría errores de carga. Mantener hasta confirmar que nunca se usan. |
| `entities/.pycodex.json` | Si la entidad “pycodex” es parte de la simulación (referenciada en `core/runner.py` o en configuraciones), su borrado impediría crear esa entidad. |
| `pyproject.toml` / `setup.cfg` / `setup.py` | Archivos de configuración del proyecto y del empaquetado. No aparecen en el plan, pero son críticos para la instalación y para herramientas como `pip`, `poetry` o `setuptools`. |
| `requirements.txt` | Lista de dependencias externas; necesaria para reproducir el entorno. |
| `LICENSE` | Información legal del proyecto; su eliminación no afecta la ejecución pero sí la distribución y cumplimiento de licencias. |
| `.gitignore` | Define qué archivos deben ser ignorados por Git; su ausencia puede generar commits de artefactos no deseados. |
| `README.md` (versión principal) | Documento de presentación del proyecto; útil para usuarios y colaboradores. No debe borrarse. |
| `docs/` (carpeta completa) | Aunque algunos archivos dentro de `docs/` están en “REVISAR”, la carpeta de documentación en sí es valiosa para usuarios y para la mantenibilidad del proyecto. No eliminarla. |
| `scripts/` (si existe) | Scripts auxiliares (p.ej. de despliegue, generación de datos) que pueden ser usados por CI/CD o por desarrolladores. |

> **Resumen:** Los ítems marcados como RECHAZADO son aquellos que, aunque aparecen en la lista de “BORRAR” o están bajo duda, son **esenciales** para la ejecución, pruebas o gestión del proyecto. Se recomienda **no borrarlos** hasta confirmar su inutilidad mediante búsqueda de importaciones y pruebas de ejecución.

---

### **➕ AGREGAR** – Archivos / carpetas que **faltan en la propuesta** y que deben revisarse / conservarse  

| Ruta | Tipo | Comentario / Acción sugerida |
|------|------|------------------------------|
| `.gitignore` | Configuración | Mantener; asegura que artefactos temporales no se versionen. |
| `pyproject.toml` | Configuración de empaquetado | Mantener; define dependencias, versión, entry‑points, etc. |
| `setup.cfg` / `setup.py` | Configuración de empaquetado (si existen) | Mantener; necesario para instalación con `pip`. |
| `requirements.txt` | Dependencias | Mantener; permite reproducir el entorno. |
| `LICENSE` | Legal | Mantener; importante para distribución. |
| `CONTRIBUTING.md` | Guía de contribución | Mantener; útil para colaboradores. |
| `CHANGELOG.md` | Historial de cambios | Mantener; facilita seguimiento de versiones. |
| `.github/` (workflows, ISSUE_TEMPLATE, etc.) | CI/CD y gestión de issues | Mantener; automatiza pruebas y despliegues. |
| `scripts/` (cualquier script de utilidad) | Utilidad | Revisar su uso; si es parte de CI o de generación de datos, conservar. |
| `data/` o `resources/` (archivos de datos estáticos) | Datos | Verificar que los JSON de semillas y glifos estén bajo `entities/` y `glifos/`; cualquier otro recurso debe mantenerse. |
| `notebooks/` (Jupyter notebooks) | Documentación / experimentación | Si existen, mover a `docs/` o `examples/` según corresponda. |
| `examples/` (código de ejemplo) | Tutoriales | Mantener; ayuda a usuarios a entender el motor. |
| `Dockerfile` / `docker-compose.yml` | Contenedores | Mantener si el proyecto se despliega en contenedores. |
| `Makefile` | Automatización | Mantener; facilita tareas comunes. |
| `tox.ini` / `pytest.ini` | Configuración de pruebas | Mantener si existen pruebas. |
| `tests/` (cuando contiene pruebas) | Pruebas | **No borrar**; revisar contenido y conservar. |
| `docs/manifiesto/ontologico/ia.md` | Documentación | Ya está en “REVISAR”, pero debe quedar en `docs/` o archivarse. |
| `docs/protocolo/ler.md` | Documentación | Igual que anterior. |
| `historia/*` (cualquier archivo bajo `historia/`) | Narrativa / cultura del proyecto | No afecta al código; puede archivarse en `docs/` o `archive/`. |
| `core/__init__.py` (si existe) | Inicializador del paquete | Mantener; necesario para que `core` sea un paquete importable. |
| `glifos/__init__.py` | Inicializador del paquete | Mantener. |
| `entities/__init__.py` | Inicializador del paquete | Mantener. |
| `*.md` en raíz que no estén listados (p.ej. `USAGE.md`, `ROADMAP.md`) | Documentación | Mantener o mover a `docs/`. |
| `*.yml` o `*.yaml` de configuración (p.ej. `config.yaml`) | Configuración | Verificar uso; conservar si es leído por el motor. |

> **Acción recomendada:**  
> 1. Ejecutar `git ls-files` para obtener la lista completa del árbol.  
> 2. Comparar con las tablas anteriores y marcar los ítems que aparecen en el repositorio pero no en ninguna de las tres listas.  
> 3. Para cada nuevo ítem, buscar referencias (`grep -R "<nombre>" .`) y decidir si es esencial, opcional o documentación.  

---

## Resumen ejecutivo

| Categoría | Nº de ítems | Comentario |
|-----------|------------|------------|
| **APROBADO** (puede borrarse) | ~8‑12 | Artefactos generados, temporales o de caché. |
| **RECHAZADO** (no borrar) | 8‑10 | Archivos esenciales para ejecución, pruebas, empaquetado o documentación crítica. |
| **AGREGAR** (faltantes) | 15‑20 | Configuración del proyecto, licencia, documentación, scripts, CI/CD, etc. |

Con esta auditoría el equipo puede proceder a **eliminar con seguridad** los archivos marcados como **APROBADO**, **preservar** los **RECHAZADO** y **añadir** a la lista de seguimiento los ítems bajo **AGREGAR** para una revisión más detallada. Después de aplicar los cambios, se recomienda ejecutar la suite de pruebas (si existe) o una corrida mínima del CLI (`python -m core.runner --ticks 1`) para validar que el motor sigue funcionando correctamente.  

---  

**Próximos pasos sugeridos**

1. **Eliminar** los archivos de la sección **APROBADO**.  
2. **Revisar** los ítems de **RECHAZADO** y confirmar que realmente son necesarios (búsqueda de importaciones, pruebas de ejecución).  
3. **Incorporar** los archivos de **AGREGAR** al control de versiones y documentar su propósito.  
4. **Commit** con mensaje descriptivo, por ejemplo:  
   ```
   chore: repo cleanup – remove caches, backups & obsolete test files
   ```  

Con esto el repositorio quedará libre de ruido, mantendrá todo lo necesario para la ejecución y conservará la documentación y configuración que facilitan su mantenimiento y evolución. ¡Buen trabajo!