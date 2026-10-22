# INFORME: aplicar_parche_humano.py
Generado: 2026-10-22 02:56:04

## Informe: `aplicar_parche_humano.py`

### 1. ¿Qué es este archivo?
Script de mantenimiento *ad-hoc* para aplicar un hotfix específico en la lógica de supervivencia del ecosistema.

### 2. ¿Qué hace?
Reemplaza una línea en `core/ecosistema.py` que mataba entidades viejas con baja fitness (`c.viva = False`) por un bloque que induce **hibernación** (`c.energia = 0.1`) manteniéndolas vivas (`c.viva = True`). Usa `Tools.apply_patch` para la sustitución exacta de texto.

### 3. Relación con el sistema
- **Dependencia:** `core.tools.Tools` (utilidad de parcheo).
- **Objetivo:** `core/ecosistema.py` (núcleo de simulación).
- **Origen:** Implementa una corrección propuesta externamente ("PyCodex") para evitar extinción prematura de la población.

### 4. ¿Esencial o prescindible?
**Prescindible (post-ejecución).** Es una herramienta *one-shot* para migrar el código base. Una vez aplicado el parche con éxito, el archivo ya no sirve para la operación normal del simulador y puede eliminarse o archivarse.