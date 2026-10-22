# INFORME: enjambre_crawlers.py
Generado: 2026-10-22 03:15:04

**1. ¿Qué es este archivo?**  
Un script de orquestación que configura el entorno y define los crawlers del sistema.

**2. ¿Qué hace?**  
Carga la clave GROQ del `.env`, consulta modelos disponibles en Groq, inicializa el sustrato LLM y crea una lista de configuraciones de crawlers para los módulos `core/`, `entities/` y `glifos/`.

**3. ¿Cómo se relaciona con el resto?**  
Importa `Tools`, `SustratoOpenAICompat` y `load_env` desde `core`; depende de la variable `GROQ_KEY`; crea el directorio `memoria/atlas`; actúa como punto de entrada que prepara la infraestructura antes de que los crawlers ejecuten sus misiones.

**4. ¿Es esencial o prescindible?**  
Es esencial para el arranque: sin ella, el sustrato LLM y los crawlers nunca se configurarían. Sin embargo, la lógica real está descentralizada en los diccionarios que define, lo que la hace crítica pero modular.