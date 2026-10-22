# INFORME: core/lenguaje.py
Generado: 2026-10-22 02:31:57

### Informe: `core/lenguaje.py`

1. **¿Qué es este archivo?**
Módulo de traducción que convierte propuestas en lenguaje natural de los especialistas en acciones somáticas estructuradas.

2. **¿Qué hace?**
*   **`PROMPT_INTROSPECCION`**: Define la plantilla para que el LLM genere justificaciones naturales.
*   **`_extraer_canal` / `_extraer_valor`**: Funciones deterministas que extraen el parámetro y su valor numérico del texto usando coincidencia de sinónimos y regex.
*   **`traducir_a_canal`**: Lógica de fallback offline para validar y estructurar la propuesta antes de su ejecución.

3. **¿Cómo se relaciona con el resto del sistema?**
Depende de `core.juez` (validación final), `core.llm.base` (sustrato LLM) y `core.soma` (definición de canales legales). Actúa como puente entre la "mente" (LLM) y el "cuerpo" (Soma), asegurando que solo canales whitelisted sean modificados.

4. **¿Es esencial o prescindible?**
**Esencial.** Sin este módulo, el sistema carece de la capacidad de "pensar" en lenguaje natural y traducirlo a acciones. Es el componente crítico que cierra el bucle lingüístico, permitiendo que las mutaciones sean justificadas semánticamente en lugar de ser puramente reflejas o aleatorias.