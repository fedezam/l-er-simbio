# INFORME: crawler_archivo_por_archivo.py
Generado: 2026-10-22 02:57:09

**Mini-Informe: crawler_archivo_por_archivo.py**

1. **¿Qué es este archivo?**  
   Script crawler principal del repositorio l-er-simbio. Automatiza el análisis iterado de archivos definidos, lee su contenido (máx. 4000 chars) y genera mini-informes estructurados mediante un modelo LLM en Groq, controlando saturación con pausas de 20s.

2. **¿Qué hace?**  
   Carga credenciales y valida la API key de Groq, consulta modelos disponibles y establece la conexión con el sustrato `SustratoOpenAICompat`. Para cada archivo en `archivos_a_analizar`, verifica si ya existe informe previo, lee y trunca el contenido, construye un prompt detallado y envía al LLM para obtener los cuatro puntos clave. Almacena los resultados en `memoria/atlas/`.

3. **¿Cómo se relaciona con el resto del sistema?**  
   Depende de módulos internos `core.tools` (lectura de archivos) y `core.llm.base` (sustrato LLM). Utiliza `load_env` para la configuración. La lista de archivos cubre componentes del ecosistema: núcleos, entidades, glifos, docs y historia. Los informes generados se integran en la carpeta `memoria/atlas/`, alimentando el atlas del sistema.

4. **¿Es esencial o prescindible?**  
   Es una herramienta de infraestructura esencial para análisis automatizado y generación consistente de documentación ligera. Reduce carga manual y asegura inspección sistemática de todo el repositorio. No es prescindible en flujos que requieren monitoreo continuo o reportes automáticos, aunque su dependencia de la API de Groq y la configuración ambiental limita su uso en entornos sin dicha infraestructura.