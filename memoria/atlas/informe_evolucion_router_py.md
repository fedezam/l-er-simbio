# INFORME: evolucion_router.py
Generado: 2026-10-22 02:55:00

## Informe: `evolucion_router.py`

### 1. ¿Qué es este archivo?
Script de arranque (entry point) que configura y ejecuta un bucle de simulación evolutiva utilizando un pool de LLMs gratuitos vía OpenRouter.

### 2. ¿Qué hace?
- **Configura un `ConectorUniversal`** con 4 modelos gratuitos (Llama 3.3, Qwen 2.5, Gemma 2, Mistral) priorizados y un fallback determinista.
- **Inicializa el ecosistema**: `Plano`, `Juez` (presupuesto 15) y puebla entidades desde `entities/`.
- **Inyecta una misión** (leída de `mision.py`) en la semilla de cada entidad.
- **Ejecuta 3 ticks** de evolución, imprimiendo eventos y estado de población.
- **Reporta ranking final** por fitness y estado de rotación de modelos.

### 3. Relación con el sistema
**Dependencias clave:** `core.ecosistema.Plano`, `core.semilla.poblar_entidades`, `core.llm.conector.ConectorUniversal`, `core.llm.base` (sustratos), `core.juez.Juez`. Orquesta la interacción entre el motor evolutivo y la capa de inferencia LLM.

### 4. ¿Esencial o prescindible?
**Prescindible como archivo fijo.** Es un *launcher* hardcodeado (API key expuesta, ticks fijos, misión única). La lógica residente en `core/` es la esencial; este archivo debería ser un CLI parametrizable (`main.py --ticks --mission --models`).