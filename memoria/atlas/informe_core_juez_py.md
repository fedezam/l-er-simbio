# INFORME: core/juez.py
Generado: 2026-10-22 02:28:41

### Informe: `core/juez.py`

1. **¿Qué es este archivo?**
Módulo de evaluación semántica que permite a un LLM actuar como "Juez" para medir la coherencia de las entidades generadas, superando las limitaciones de métricas sintácticas.

2. **¿Qué hace?**
Define la clase `Veredicto` (dataclass) para almacenar puntuaciones de identidad, glifos y coherencia, calculando un score ponderado. Incluye dos prompts específicos (`PROMPT_JUEZ` y `PROMPT_JUEZ_SOMA`) para evaluar la habitabilidad de la identidad y la moderación de parámetros del sistema ("Soma"). Implementa lógica de parsing robusta para extraer valores numéricos estrictos de la salida del LLM.

3. **¿Cómo se relaciona con el resto del sistema?**
Depende de `core.llm.base.Sustrato` para interactuar con el modelo de lenguaje. Se integra en el ciclo de selección evolutiva, reemplazando o complementando el fitness proxy determinista. Su diseño permite degradación elegante: si el juez falla, el sistema vuelve a la métrica sintáctica previa.

4. **¿Es esencial o prescindible?**
**Esencial** para la evolución semántica. Sin él, el sistema se limita a optimizar densidad de glifos (sintaxis) en lugar de coherencia de significado (semántica). Es el componente que "cierra el circuito" de sentido, permitiendo que la selección natural actúe sobre la calidad reflexiva de las entidades, no solo su estructura.