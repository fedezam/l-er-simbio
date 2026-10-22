# PLAN DE LIMPIEZA FINAL PROPUESTO POR PYCODEX
Generado: 2026-10-22 04:50:00

## 📂 PLAN DE LIMPIEZA DEL REPOSITORIO *l‑er‑simbio*

> **Objetivo:** liberar espacio y reducir ruido sin comprometer la funcionalidad del proyecto.  
> **Enfoque:** eliminar todo lo que claramente no se usa, conservar los componentes críticos y marcar para inspección manual los archivos que pueden ser útiles pero requieren confirmación.

---

### 🗑️ **BORRAR** – Archivos / carpetas que **no aportan** al código en producción  

| Ruta / Patrón | Motivo de eliminación |
|---------------|-----------------------|
| `**/__pycache__/` | Carpetas generadas automáticamente por Python; pueden recrearse. |
| `**/*.pyc` | Byte‑code compilado, redundante con los fuentes *.py*. |
| `**/*.bak` <br> `**/*.old` <br> `**/*.tmp` | Copias de seguridad y archivos temporales que nunca se usan en tiempo de ejecución. |
| `tests/test_ai.py` <br> `tests/test_multi_guia.py` <br> `tests/old_*.py` | Tests marcados como **obsoletos** en el Atlas; no se ejecutan en CI y hacen referencia a módulos eliminados. |
| `scripts_raiz/fix_ler.py` <br> `scripts_raiz/setup_genesis.py` <br> `scripts_raiz/debug_*.py` | Scripts creados “sobre la marcha” durante la sesión de desarrollo; su contenido está archivado en la historia y no se invocan desde el código. |
| `sandbox/*` (excepto `sandbox/README.md`) | Entorno de pruebas aislado que ya no se usa; los experimentos están documentados en *historia/*. |
| `memoria/*.log` <br> `memoria/*.snapshot` | Registros y snapshots de ejecución que pueden regenerarse; ocupan espacio innecesario. |
| `recursos/*.bak` | Copias de seguridad de fuentes tipográficas. |
| `otros/*.tmp` <br> `otros/*.old` | Archivos sueltos de tipo temporal. |

> **Nota:** antes de ejecutar el borrado masivo, se recomienda hacer un *commit* de respaldo o crear una rama `cleanup‑backup` con los cambios, por si surge alguna duda posterior.

---

### ✅ **MANTENER** – Archivos **esenciales** que forman el núcleo del proyecto  

| Ruta | Comentario |
|------|------------|
| `core/ecosistema.py` | Motor principal del ecosistema. |
| `core/soma.py` | Gestión de la “célula” del sistema. |
| `core/juez.py` | Lógica de evaluación y decisiones. |
| `core/runner.py` | Orquestador de procesos. |
| `core/lenguaje.py` | Definiciones de lenguaje interno. |
| `core/semilla.py` | Generación de semillas aleatorias. |
| `core/sistema_inmune.py` | Mecanismo de defensa y validación. |
| `core/*.py` (cualquier otro archivo dentro de `core/` no listado explícitamente) | Parte del corazón del framework; se asume que son necesarios. |
| `entities/pycodex.json` | Definición de la entidad principal. |
| `entities/auditor_ler.json` | Configuración del auditor. |
| `entities/*.json` (todos los JSON bajo `entities/`) | Esquemas de entidades que el core consume. |
| `glifos/universal_glyphs.json` | Diccionario universal de símbolos. |
| `glifos/mmp_core.json` | Glifo del núcleo MMP. |
| `glifos/mathema.json` | Glifo matemático. |
| `glifos/security_glyphs.json` | Glifos de seguridad. |
| `glifos/*.json` (cualquier otro glifo) | Necesarios para la interpretación simbólica. |
| `docs/README.md` (si existe) | Punto de entrada de la documentación. |
| `scripts_raiz/entrypoint.sh` (si es el script de arranque oficial) | Script de lanzamiento oficial. |

> **Regla de oro:** **NUNCA** eliminar archivos dentro de `core/`, `entities/` o `glifos/` sin una revisión exhaustiva del código que los importa.

---

### 🔍 **REVISAR** – Archivos que **pueden ser útiles** pero requieren confirmación manual  

| Ruta / Tipo | Qué revisar | Preguntas clave |
|-------------|-------------|-----------------|
| `docs/` (todos los archivos Markdown, PDF, etc.) | Documentación interna, guías de uso, diagramas. | ¿Están actualizados? ¿Alguien depende de ellos? |
| `historia/` (archivos narrativos, logs de decisiones) | Contexto histórico del proyecto. | ¿Se usan como referencia en pruebas o en la generación de datos? |
| `tests/` (excepto los marcados como obsoletos) | Suite de pruebas actual. | ¿Pasaron todas las pruebas en CI? ¿Hay pruebas que cubren funcionalidades críticas que no están en los tests obsoletos? |
| `scripts_raiz/maintenance_*.py` | Scripts de mantenimiento (p.ej., migraciones, generación de datos). | ¿Se ejecutan en algún pipeline? ¿Necesitan ser conservados para futuras actualizaciones? |
| `tools/` (cualquier utilidad como `formatador.py`, `validator.py`) | Herramientas auxiliares. | ¿Son usadas por desarrolladores o CI? |
| `arbol/` (genealogía de entidades) | Información de relaciones entre entidades. | ¿Se consulta desde el código o solo es documentación? |
| `recursos/` (fuentes tipográficas, imágenes) | Recursos visuales. | ¿Son referenciados por la UI o por la generación de PDFs? |
| `sandbox/README.md` | Descripción del sandbox. | ¿ contiene instrucciones que podrían ser útiles para futuros experimentos? |
| `memoria/` (archivos de snapshot que no son logs) | Snapshots de estado. | ¿Se usan para reproducir bugs o para pruebas de regresión? |

> **Acción recomendada:** abrir cada archivo, validar su uso (búsqueda de importaciones, referencias en CI, menciones en `README`), y decidir:
> - **Mantener** (si es necesario),
> - **Mover a** `archive/` (si se quiere conservar histórico pero fuera del árbol activo),
> - **Eliminar** (si se confirma que es redundante).

---

## 📋 Resumen rápido de pasos a seguir

1. **Crear rama de respaldo**  
   ```bash
   git checkout -b cleanup-backup
   git push -u origin cleanup-backup
   ```

2. **Eliminar los elementos listados en **BORRAR** (usando `git rm -r` o `git clean`).**  
3. **Commit** con mensaje claro, p.ej. `chore: cleanup de archivos temporales y cache`.  
4. **Ejecutar la suite de pruebas** (`pytest -q`) para asegurar que nada esencial se ha borrado.  
5. **Revisar manualmente cada ítem bajo **REVISAR**; mover a `archive/` lo que se decida conservar pero no usar.**  
6. **Merge** a `main` (o rama de desarrollo) una vez que la CI pase y la revisión esté completa.

Con este plan, el repositorio quedará más liviano, más fácil de navegar y con una base de código clara y mantenible. ¡Éxitos en la limpieza! 🚀