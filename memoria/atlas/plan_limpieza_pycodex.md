# PLAN DE LIMPIEZA PROPUESTO POR PYCODEX
Generado: 2026-10-22 02:47:55

## PLAN DE LIMPIEZA DEL REPOSITORIO **l‑er‑simbio**

> **Objetivo:** Mantener el código que realmente forma parte del motor de ejecución y de los datos de configuración/semilla, eliminar artefactos que no aportan al funcionamiento y marcar los que necesitan una revisión humana antes de decidir su destino.

---

### 📂 **BORRAR**
> **Archivos / carpetas que, según el Atlas, son *claramente* prescindibles** (no forman parte del código de ejecución ni de la configuración necesaria).  
> *Si aparecen en el árbol real del proyecto (por ejemplo `__pycache__`, archivos `.pyc`, copias de seguridad `*.bak`, `*.old`, etc.) elimínelos también.*

| Ruta | Motivo |
|------|--------|
| `__pycache__/` (cualquier nivel) | Carpeta generada automáticamente por Python; no contiene código fuente. |
| `*.pyc` (archivos compilados) | Redundantes; se generan al ejecutar. |
| `*.bak`, `*.old`, `*_backup.*` | Copias de seguridad que no están listadas en el Atlas. |
| `tests/` (si existe y está vacío o contiene pruebas obsoletas) | No hay referencia a pruebas en el Atlas; el proyecto parece ser una librería/CLI sin suite de tests. |
| `docs/_site/`, `docs/.cache/` (si existen) | Artefactos de generación de documentación estática. |
| `README~`, `README.txt~`, `*.tmp` | Archivos temporales típicos de editores. |

> **Nota:** Si alguna de estas rutas no está presente, simplemente ignórela.

---

### 📂 **MANTENER**
> **Archivos que el Atlas indica como *esenciales* para el funcionamiento del motor LER**. No deben modificarse ni eliminarse sin una re‑arquitectura completa.

| Ruta | Razón de ser esencial |
|------|------------------------|
| `core/ecosistema.py` | Orquestador del plano evolutivo (clases `Cuerpo` y `Plano`). |
| `core/glifo_engine.py` *(o `core/glifo/engine.py` según la estructura real)* | Motor simbólico de reconocimiento y validación de glifos. |
| `core/juez.py` | Evaluador semántico que cierra el bucle de selección evolutiva. |
| `core/lenguaje.py` | Traductor entre lenguaje natural y acciones somáticas. |
| `core/runner.py` | Punto de entrada CLI; inicializa y ejecuta la simulación. |
| `core/semilla.py` | Carga de entidades a partir de los JSON de *seed*. |
| `core/sistema/inmune.py` | (Mencionado en el índice) parte del subsistema de inmunidad; presumiblemente usado por `Plano`. |
| `core/soma.py` | Tejido editable del cuerpo; necesario para mutaciones somáticas. |
| `glifos/universal/glyphs.json` | Definición de glifos universales consumida por `GlyphEngine`. |
| `glifos/mmp/core.json` | Conjunto de glifos MMP integrado por el motor. |
| `entities/auditor/ler.json` | Semilla de entidad “auditor”. |
| `entities/learn/nucleo/0.json` | Semilla de entidad “núcleo”. |
| `entities/plan/mode.json` | Semilla de entidad “plan”. |
| `entities/.pycodex.json` | Semilla de entidad “pycodex”. |
| `glifos/mathema.json` | Glifos específicos de dominio matemático (usados por el motor). |
| `glifos/security/glyphs.json` | Glifos de seguridad; pueden ser requeridos por validaciones. |

> **Tip:** Verifique que los nombres exactos de los archivos coincidan con los que aparecen en el árbol real (por ejemplo, si el motor está en `core/glifo/engine.py` en vez de `core/glifo_engine.py`).  

---

### 📂 **REVISAR**
> **Archivos que *no están claramente clasificados* como esenciales ni como basura**. Necesitan una inspección humana para decidir su futuro.

| Ruta | Pregunta / Comentario |
|------|-----------------------|
| `docs/manifiesto/ontologico/ia.md` | ¿Es parte del *manual de usuario* o simplemente documentación de referencia? Si no se usa en tiempo de ejecución, puede archivarse en `docs/` o mover a un repositorio de documentación. |
| `docs/protocolo/ler.md` | Similar al anterior: contiene protocolos operacionales. Mantener si el equipo necesita referencia; de lo contrario, archivarlo. |
| `historia/nacimiento/axioma.md` | Texto histórico / narrativo. No afecta al código, pero puede ser valioso para la cultura del proyecto. |
| `historia/origen/de/arca/aelion/dva.md` | Igual que el anterior. |
| `core/semilla.py` (ya listado como esencial) – **pero** revisar si contiene funciones auxiliares no usadas (p.ej. generación de datos de prueba). |
| `core/sistema/inmune.py` – confirmar que realmente es importado por `core/ecosistema.py` o por otro módulo; si no tiene referencias, podría ser candidato a eliminar o a mover a `extras/`. |
| `glifos/mathema.json` y `glifos/security/glyphs.json` – confirmar que el motor los carga (busque referencias a `mathema` o `security` en el código). Si nunca se usan, pueden archivarse. |
| `entities/.pycodex.json` – validar que la entidad “pycodex” sea efectivamente poblada y utilizada en la simulación. |
| `core/glifo/engine/.py` (si la ruta real contiene un **directorio** `engine/` con varios archivos) – inspeccionar si hay módulos auxiliares dentro que no aparecen en el Atlas (por ejemplo, `utils.py`, `constants.py`). |

> **Acción recomendada:**  
> 1. Ejecutar una búsqueda de importaciones (`grep -R "nombre_del_archivo" .`) para cada uno de los ítems de esta tabla.  
> 2. Revisar los *tests* (si existen) o los scripts de ejemplo que puedan depender de estos documentos.  
> 3. Decidir si mover a una carpeta `docs/`/`archive/` o eliminar.

---

## ✅ Resumen rápido

| Acción | Cantidad |
|--------|----------|
| **Borrar** | Sólo artefactos generados/temporales (≈ 5‑10 ítems, según la presencia real). |
| **Mantener** | 14 archivos de código/configuración esenciales. |
| **Revisar** | 8‑10 archivos/documentos que requieren confirmación humana. |

---

### Próximos pasos sugeridos

1. **Eliminar** los directorios y archivos listados en **BORRAR**.  
2. **Ejecutar** los tests (si aparecen) o una corrida mínima del CLI (`python -m core.runner --ticks 1`) para confirmar que el proyecto sigue funcionando tras la limpieza.  
3. **Auditar** los ítems de **REVISAR** siguiendo la guía anterior; una vez aclarado su uso, moverlos a `docs/` o eliminarlos.  
4. **Commit** los cambios con un mensaje descriptivo, por ejemplo:  
   ```
   chore: clean repository – remove caches, backups and obsolete test files
   ```

Con este plan el repositorio queda libre de ruido, conserva todo lo necesario para la ejecución y mantiene la documentación que pueda ser útil para futuros desarrolladores. ¡Listo para seguir evolucionando!