# INFORME: core/llm/base.py
Generado: 2026-10-22 04:00:34

## Mini‑informe de `core/llm/base.py`

| # | Contenido |
|---|-----------|
| **1. ¿Qué es este archivo?** | Define la **interfaz abstracta** y una **implementación mock** para cualquier modelo de lenguaje (LLM) usado por LER. |
| **2. ¿Qué hace?** | - `class Sustrato(ABC)`: contrato mínimo con método `hidratar(prompt, temperatura)` y propiedades `nombre` y `es_llm_real`. <br> - `class SustratoDeterminista(Sustrato)`: mock determinista que genera respuestas a partir de hashes del prompt (para pruebas y fallback). |
| **3. ¿Cómo se relaciona con el resto del sistema?** | - Importa solo módulos estándar (`hashlib`, `json`, `abc`, `typing`). <br> - Otros componentes (juez, traductor, etc.) dependen de esta API para “hidratar” prompts sin conocer el modelo subyacente. |
| **4. ¿Es esencial o prescindible?** | **Esencial**: constituye el **punto de integración** de cualquier LLM en la arquitectura; sin él, los módulos semánticos no podrían interactuar con modelos reales ni con el mock de pruebas. |

*(≈ 115 palabras)*