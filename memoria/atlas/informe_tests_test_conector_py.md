# INFORME: tests/test_conector.py
Generado: 2026-10-22 03:27:46

### 1. ¿Qué es este archivo?
Archivo de pruebas unitarias del conector universal de modelos de lenguaje (`tests/test_conector.py`).

### 2. ¿Qué hace?
- Define `SustratoFalso`, un doble de prueba que puede simularProviders caídos.
- `test_usa_el_mejor_disponible`: comprueba la selección por prioridad.
- `test_failover_cuando_cae_el_preferido`: valida el failover y el vetado tras fallar el proveedor preferente.
- `test_fallback_inerte_si_todo_muerre`: verifica el uso del `SustratoDeterminista` como fallback.
- `test_factoria_con_config_y_descubrimiento_env`: prueba la construcción desde configuración y variables `LER_OLLAMA_*`.

### 3. ¿Cómo se relaciona con el resto del sistema?
Importa las abstracciones `Sustrato` y `SustratoDeterminista` de `core.llm.base`, y `Candidato`, `ConectorUniversal` y `conector_universal` de `core.llm.conector`. exercising selection, failover, health checks, deterministic fallback, and configuration discovery.

### 4. ¿Es esencial o prescindible?
Es **prescindible para la ejecución del sistema**, pues solo contiene tests, pero es importante para garantizar la resiliencia del conector y detectar regresiones en prioridades, failover y fallback.