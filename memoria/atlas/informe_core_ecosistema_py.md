# INFORME: core/ecosistema.py
Generado: 2026-10-22 02:28:24

### Informe: `core/ecosistema.py`

1. **¿Qué es este archivo?**
El núcleo del "plano" de simulación, implementando un tablero de Conway semántico donde conviven entidades textuales.

2. **¿Qué hace?**
Define dos clases principales:
*   **`Cuerpo`**: Representa una entidad con glifos, energía y memoria. Proyecta su estado hacia el entorno.
*   **`Plano`**: Gestiona el ciclo de vida (nacimiento, supervivencia, mutación, selección). Controla la interacción con el sustrato LLM, la mutación de glifos y la validación de propuestas somáticas mediante un juez.

3. **¿Cómo se relaciona con el resto del sistema?**
Depende de `core.llm.base` (Sustrato), `core.lenguaje` (traducción de propuestas) y `core.soma` (tejido editable). Se integra con `core.juez` para medir la coherencia semántica (fitness).

4. **¿Es esencial o prescindible?**
**Esencial.** Es el orquestador central que conecta el lenguaje, la lógica de vida artificial y el sustrato cognitivo. Sin él, no hay ciclo de evolución ni interacción entre entidades.