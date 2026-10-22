# INFORME: agente_reforma.py
Generado: 2026-10-22 03:02:42

# Mini-informe: `agente_reforma.py`

1. **¿Qué es este archivo?**  
Script de orquestación de agentes autónomos para la reforma y modificación de código dentro del ecosistema LER.

2. **¿Qué hace?**  
Carga entidades desde `entities/`, les asigna una misión de reforma para evitar la "muerte silenciosa" y les permite ejecutar herramientas (`read_file`, `propose_patch`, `apply_patch`) con control de permisos por rol mediante un plano y un juez.

3. **¿Cómo se relaciona con el resto del sistema?**  
Depende de módulos del núcleo (`core`): `Plano`, `poblar_entidades`, `SustratoOpenAICompat`, `load_env`, `Tools` y `Juez`. Usa Groq como proveedor LLM y requiere la variable `GROQ_KEY`.

4. **¿Es esencial o prescindible?**  
Esencial para la auto-reforma autónoma del sistema, pero prescindible para la operación base si no se requiere modificación de código por agentes.