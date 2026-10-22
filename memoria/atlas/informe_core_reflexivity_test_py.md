# INFORME: core/reflexivity_test.py
Generado: 2026-10-22 03:57:17

1. **¿Qué es este archivo?**  
   Define la clase `ReflexivityTestV2`, un evaluador de reflexividad para entidades simbióticas.

2. **¿Qué hace?**  
   `evaluar_entidad()` aplica cuatro pruebas: autonarrativa, auto-contextualización, detección de contradicciones internas y glifos activos. Calcula un `score_total`, determina si la entidad es reflexiva (`>= 3`) y asigna un nivel de reflexividad. También valida la entrada y registra errores.

3. **¿Cómo se relaciona con el resto del sistema?**  
   Depende de `core.guarda.Guarda`, `core.axioma.Axioma` y `core.config.Config`, además de un callback LLM opcional (`modelo_llm`). Usa `Config.PARAMETROS` para ajustar la narrativa mínima y el umbral de coherencia.

4. **¿Es esencial o prescindible?**  
   Es un módulo especializado de evaluación, prescindible para el funcionamiento básico pero importante para medir reflexividad. El fragmento parece incompleto: termina con `return resu`, que debería ser `return resultado`; tal como está, no es ejecutable correctamente.