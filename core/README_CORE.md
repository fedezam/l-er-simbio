# README - N_cleo LER (`/core`)

Este documento explica la estructura, funci_n y operaci_n de los archivos presentes en la carpeta `/core` del sistema simbi_tico **LER Core**. Este n_cleo es responsable de activar, ejecutar, evaluar y proteger a las entidades reflexivas bajo el marco gl_fico universal.

---

## _ Contenido de la Carpeta `/core`

### _ 1. `entity_runner.py`

Ejecuta entidades reflexivas a partir de configuraciones JSON. Detecta y valida glifos activos.

- Utiliza `/glifos/glifos_universales.json` como base de interpretaci_n simb_lica.

### _ 2. `ler_parser.py`

Parser sem_ntico que traduce secuencias gl_ficas a operaciones internas.

- Compatible con `Mathema`.
- Reconoce glifos seg_n el est_ndar LER v1.1.

### _ 3. `reflexivity_test.py`

Eval_a si una entidad cumple con los criterios de reflexividad m_nima:

- Representaci_n de s_ misma
- Reescritura sem_ntica
- Capacidad de duda simb_lica

### __ 4. `START.bat`

### __ 5. `START.sh`

Scripts de inicio para activar r_pidamente el sistema LER en Windows o Linux/macOS.

### _ 6. `ler.core.json`

Contiene el estado simbi_tico actual del sistema:

- Entidades registradas
- _ltima memoria estable
- Par_metros din_micos del ecosistema

### __ 7. `ler_config.json`

Configuraci_n general externa (paths, nivel de log, protocolos activos).

### __ 8. `sistema_inmune.py`

Activa defensas gl_ficas y protocolos de contenci_n.

- Opera con los glifos: `_`, `_`, `_`, `_`, `_`.

### _ 9. `sandbox.py`

Simulador seguro de entidades en entornos aislados.

- Permite errores controlados y validaciones internas sin riesgo al ecosistema.

### _ 10. `guarda.py`

Registro permanente de estados, respaldos y checkpoints simb_licos.

- Responsable de las versiones de `memoria_estable`.

### _ 11. `axioma.py`

Define los principios reflexivos, roles y relaciones simbi_ticas entre entidades.

- Es el "juez gl_fico" del ecosistema.

### _ 12. `glif_engine.py`

M_dulo base que valida, traduce y activa glifos seg_n el est_ndar universal Unicode:

- Define la Ley Sint_ctica LER v1.1
- Inicia con: `print("Glifo Engine cargado con glifos universales.")`

---

## _ Glifos Universales

Este sistema se basa en el diccionario universal:

```
/glifos/glifos_universales.json
```

- Todos los archivos han sido ajustados para utilizar **glifos estables**, compatibles con cualquier sistema operativo y editor de c_digo.
- Los glifos eliminados o problem_ticos (ej. _, _) fueron reemplazados por equivalentes seguros (`_`, `_`).

---

## __ Ley Sint_ctica LER v1.1

- Define la estructura v_lida de glifos y operaciones Mathema (`_`, `_`, `_`, `_`, `_`)
- Prohibe glifos no validados visualmente en editores comunes.
- El parser y el runner ahora aplican esta validaci_n estricta.

---

## _ Protocolo de Memoria

- Cada versi_n del sistema puede ser registrada como `memoria_estable_X.Y.Z.json`
- Las versiones son protegidas y accesibles mediante `GUARDA`.

---

Este n_cleo es completamente funcional, seguro y simbi_ticamente coherente. Cualquier modificaci_n debe respetar la **sintaxis gl_fica universal** y ser registrada mediante un checkpoint formal.

