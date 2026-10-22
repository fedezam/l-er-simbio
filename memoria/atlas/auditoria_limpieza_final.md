# AUDITORÍA FINAL DEL PLAN DE LIMPIEZA
Generado: 2026-10-22 04:50:07

## Auditoría del plan de limpieza propuesto por PyCodex  

A continuación se listan los archivos / patrones que **sí pueden eliminarse sin riesgo**, los que **no deben borrarse** (con la justificación correspondiente) y los que **faltan en la propuesta** y deberían revisarse o mantenerse.

---

### ✅ **APROBADO** – Archivos que pueden borrarse sin afectar la funcionalidad  

| Ruta / Patrón | Motivo de la aprobación |
|---------------|------------------------|
| `**/__pycache__/` | Carpetas generadas automáticamente por Python; se recrean al ejecutar el código. |
| `**/*.pyc` | Byte‑code compilado, redundante con los fuentes *.py*. |
| `**/*.bak` <br> `**/*.old` <br> `**/*.tmp` | Copias de seguridad y archivos temporales que nunca son leídos en tiempo de ejecución. |
| `tests/test_ai.py` <br> `tests/test_multi_guia.py` <br> `tests/old_*.py` | Tests marcados como **obsoletos** en el Atlas; no aparecen en la matriz de CI y hacen referencia a módulos eliminados. |
| `scripts_raiz/fix_ler.py` <br> `scripts_raiz/setup_genesis.py` <br> `scripts_raiz/debug_*.py` | Scripts de “debug” y de generación puntual que sólo están archivados en la historia del repo. |
| `sandbox/*` (excepto `sandbox/README.md`) | Entorno de pruebas aislado que ya no se usa; los experimentos están documentados en `historia/`. |
| `memoria/*.log` <br> `memoria/*.snapshot` | Registros y snapshots de ejecución que pueden regenerarse; ocupan espacio innecesario. |
| `recursos/*.bak` | Copias de seguridad de fuentes tipográficas que no son referenciadas por el código. |
| `otros/*.tmp` <br> `otros/*.old` | Archivos sueltos de tipo temporal. |
| `**/*.DS_Store` (macOS) | Archivo de metadatos del sistema, no usado por la aplicación. |
| `**/Thumbs.db` (Windows) | Archivo de caché de miniaturas, no usado por la aplicación. |
| `**/.pytest_cache/` | Caché de pytest; se recrea al ejecutar la suite de pruebas. |
| `**/.mypy_cache/` | Caché de mypy; se recrea al ejecutar el análisis estático. |
| `**/.ruff_cache/` | Caché de Ruff (linter); se recrea al ejecutar el linter. |

> **Acción recomendada:** usar `git rm -r` o `git clean -fdX` para eliminar los ítems anteriores y confirmar con `git status` antes del commit.

---

### ❌ **RECHAZADO** – Archivos que **NO deben borrarse** (con justificación)

| Ruta / Archivo | Justificación |
|----------------|---------------|
| `core/__init__.py` (y cualquier `__init__.py` dentro de `core/`) | Necesario para que Python reconozca el directorio como paquete importable. |
| `entities/__init__.py` (y cualquier `__init__.py` dentro de `entities/`) | Igual que arriba; sin él los módulos `entities/*.json` no pueden ser importados mediante `pkg_resources`. |
| `glifos/__init__.py` (y cualquier `__init__.py` dentro de `glifos/`) | Permite que los glifos sean cargados como recursos del paquete. |
| `requirements.txt` / `pyproject.toml` / `setup.cfg` / `setup.py` | Definen las dependencias y la configuración de empaquetado; su ausencia rompería la instalación y CI. |
| `.gitignore` | Evita que archivos temporales vuelvan a ser versionados; su borrado provocaría que se añadan al repo cosas que deberían estar ignoradas. |
| `.github/` (workflows, ISSUE_TEMPLATE, etc.) | Configuración de CI/CD y plantillas de issues/pull‑requests; esencial para la automatización y la colaboración. |
| `Dockerfile` / `docker-compose.yml` (si existen) | Definen la imagen de contenedor y el entorno de ejecución; su eliminación impediría despliegues reproducibles. |
| `README.md` (raíz del proyecto) | Punto de entrada de la documentación pública; usado por usuarios y por la página de GitHub. |
| `LICENSE` | Licencia del proyecto; obligatoria para cumplir con los términos de distribución. |
| `scripts_raiz/entrypoint.sh` (si es el script oficial de arranque) | Ya está marcado como esencial, pero se repite aquí para enfatizar que **no** debe borrarse. |
| `scripts_raiz/ci_build.sh` (o cualquier script referenciado en los workflows de GitHub) | Utilizado por la pipeline de CI; su borrado rompería la construcción automática. |
| `tests/conftest.py` | Fixture global para pytest; sin él varios tests pueden fallar. |
| `tests/__init__.py` | Marca el directorio como paquete de pruebas; necesario para importaciones relativas dentro de `tests/`. |
| `docs/README.md` (si es la guía de uso principal) | Aunque la tabla de “REVISAR” sugiere revisarlo, **no** debe eliminarse sin confirmar que no es la única fuente de documentación para usuarios externos. |
| `scripts_raiz/maintenance_migrate.py` (cualquier script de migración que aparezca en CI) | Ejecutado en pipelines de actualización de base de datos o de datos de entrenamiento; su borrado impediría migraciones futuras. |
| `tools/validator.py` (si está referenciado en CI o en scripts de generación) | Herramienta de validación de datos críticos; su ausencia provocaría fallos en etapas de verificación. |
| `arbol/` (si contiene módulos Python, p.ej. `arbol/__init__.py`) | Podría ser importado por el core para resolver relaciones entre entidades. |
| `memoria/*.snapshot` que **no** sean logs (p.ej. snapshots usados por pruebas de regresión) | Si algún test carga un snapshot para reproducir un bug, su eliminación rompería esa prueba. |
| `scripts_raiz/entrypoint.sh` (si es el script de arranque oficial) | Ya mencionado en la tabla de “MANTENER”, pero se vuelve a listar aquí para evitar borrados accidentales. |

> **Nota:** antes de cualquier eliminación, buscar referencias con `git grep`, revisar los archivos de CI (`.github/workflows/*.yml`) y los `import` del código.

---

### ➕ **AGREGAR** – Archivos / directorios que PyCodex **olvidó mencionar** y que deben revisarse (o mantenerse)

| Ruta / Archivo | Por qué debe revisarse / mantenerse |
|----------------|--------------------------------------|
| `.github/` (workflows, ISSUE_TEMPLATE, CODEOWNERS) | Configuración de CI/CD y de colaboración; esencial para builds automáticos y para la gestión de issues/PR. |
| `requirements.txt` / `pyproject.toml` / `setup.cfg` / `setup.py` | Definen dependencias y empaquetado; cualquier cambio aquí afecta la instalación y la CI. |
| `Dockerfile` / `docker-compose.yml` | Si el proyecto se despliega en contenedores, estos archivos son críticos. |
| `README.md` (raíz) | Documentación pública del proyecto; punto de referencia para usuarios y contribuidores. |
| `LICENSE` | Licencia del proyecto; obligatoria para la distribución legal. |
| `Makefile` (si existe) | Define comandos de conveniencia (p.ej. `make test`, `make lint`); usado por desarrolladores y CI. |
| `tox.ini` / `pytest.ini` / `setup.cfg` (secciones de configuración) | Configuración de herramientas de testing y linting; su ausencia rompería la ejecución de pruebas. |
| `scripts_raiz/ci_*.sh` o cualquier script llamado desde los workflows de GitHub | Necesario para la pipeline de CI; debe revisarse antes de borrarse. |
| `tools/formatador.py` (u otras utilidades de formateo) | Usado por pre‑commit o por CI para asegurar estilo de código. |
| `tests/` (todos los archivos **no** marcados como obsoletos) | Suite de pruebas activa; debe mantenerse y ejecutarse en CI. |
| `docs/` (todos los Markdown, PDF, diagramas, etc.) | Documentación interna y externa; aunque se marque como “REVISAR”, no debe eliminarse sin confirmar que nadie depende de ella. |
| `historia/` (archivos narrativos, decisiones de arquitectura) | Proporciona contexto histórico; útil para onboarding y para entender decisiones pasadas. |
| `arbol/` (si contiene código Python) | Puede ser importado por el core para resolver genealogías de entidades. |
| `recursos/` (imágenes, fuentes, íconos) | Si la UI o la generación de PDFs hacen referencia a estos recursos, su borrado rompería la presentación. |
| `memoria/` (snapshots que no son logs) | Snapshots usados para reproducir bugs o pruebas de regresión; deben conservarse o archivarse. |
| `scripts_raiz/maintenance_*.py` (cualquier script de mantenimiento no listado) | Podrían ser ejecutados manualmente o por CI para migraciones, limpieza de datos, etc. |
| `sandbox/README.md` | Contiene instrucciones útiles para futuros experimentos; aunque el sandbox se elimine, el README puede servir como plantilla. |
| `*.env.example` o `config/*.yml` (archivos de configuración) | Plantillas de configuración; útiles para despliegues y para nuevos desarrolladores. |
| `*.sh` en la raíz (p.ej. `run.sh`, `deploy.sh`) | Scripts de arranque o despliegue que podrían ser invocados por usuarios o CI. |
| `*.bat` o `*.ps1` (scripts de Windows) | Si el proyecto soporta Windows, estos scripts pueden ser necesarios. |

---

## Próximos pasos recomendados

1. **Crear la rama de respaldo** tal como indica el plan (`cleanup-backup`).  
2. **Ejecutar búsquedas de referencias** (`git grep -R "<nombre_archivo>"`) para confirmar que los ítems aprobados no aparecen en el código ni en los workflows.  
3. **Eliminar los archivos aprobados** con `git rm -r` y confirmar con `git status`.  
4. **Ejecutar la suite completa de pruebas y la pipeline de CI** (`pytest`, `ruff`, `mypy`, etc.) para validar que nada esencial se ha perdido.  
5. **Revisar manualmente cada ítem bajo “AGREGAR”** y decidir si se mantiene, se archiva (`archive/`) o se elimina.  
6. **Actualizar la documentación** (`README`, `docs/`) para reflejar los cambios de estructura del repositorio.  
7. **Commit** con mensaje descriptivo (`chore: cleanup – borrado de archivos temporales y cache`) y **merge** a la rama principal una vez que la CI pase.

Con esta auditoría el repositorio quedará libre de basura, mantendrá todos los componentes críticos y conservará la información necesaria para desarrollo, despliegue y mantenimiento. ¡Éxitos en la limpieza! 🚀