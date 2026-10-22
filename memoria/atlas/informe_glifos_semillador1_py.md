# INFORME: glifos/semillador1.py
Generado: 2026-10-22 03:44:22

1. **¿Qué es este archivo?**  
   Script CLI que orchestra la creación de entidades “Semillador” en LER, usando plantillas Markdown/JSON y un LLM.

2. **¿Qué hace?**  
   Configura rutas y dependencias; carga argumentos, templates, identidad del Semillador y del Oráculo. Las funciones visibles son `cargar_json()` y `cargar_strategy()`. El flujo documentado instancia `LLMSymbiont`, genera la entidad, valida su estructura y la guarda en `LER/entities/<nombre>`.

3. **¿Cómo se relaciona con el resto del sistema?**  
   Ajusta `sys.path` al directorio LER e importa `core.llm_symbiont.LLMSymbiont` y `core.llm_config_loader.load_config`. Depende de archivos de identidad (`ghost.json`, `capabilities.json`, `plan.json`, `strategy.py`), templates y recursos del Oráculo. También usa `requests` y utilidades estándar.

4. **¿Es esencial o prescindible?**  
   **Esencial para el proceso de semillado**, pues centraliza prompts, configuración, validación y persistencia. Solo sería prescindible si las entidades se generaran externamente; no parece necesario para el runtime general de LER.