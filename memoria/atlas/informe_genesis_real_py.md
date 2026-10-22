# INFORME: genesis_real.py
Generado: 2026-10-22 03:06:55

**1. ¿Qué es este archivo?**
Un script de arranque que lanza una simulación de ecosistema con un LLM real (Groq) y un juez, inyectando una misión en las entidades.

**2. ¿Qué hace?**
- Configura un sustrato compatible con OpenAI usando la API de Groq.
- Crea un `Juez` con un presupuesto limitado.
- Construye un `Plano`, carga entidades desde *entities/*, añade el contenido de *mision.py* a cada semilla y ejecuta un tick de simulación.
- Imprime los eventos generados y el estado (energía, fitness, respuesta del LLM) de cada entidad viva.

**3. ¿Cómo se relaciona con el resto del sistema?**
Importa los módulos centrales (`Plano`, `poblar_entidades`, `SustratoOpenAICompat`, `Juez`) y depende de recursos externos (clave API, archivo de misión, carpeta de entidades) que otros componentes del proyecto utilizan.

**4. ¿Es esencial o prescindible?**
**Esencial** – es el punto de entrada principal para ejecutar la simulación con el LLM real y aplicar la misión a las entidades. Sin él, el ecosistema no se inicializaría ni se ejecutaría.