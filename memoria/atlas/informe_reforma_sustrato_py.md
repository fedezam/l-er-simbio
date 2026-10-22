# INFORME: reforma_sustrato.py
Generado: 2026-10-22 03:05:54

# Mini-informe: `reforma_sustrato.py`

**¿Qué es este archivo?**  
Script de orquestación para la reforma autónoma del sustrato del ecosistema mediante un LLM.

**¿Qué hace?**  
Conecta a Groq (`openai/gpt-oss-120b`), carga el código de `core/ecosistema.py` y una plantilla de misión, inyecta esa misión en entidades pobladas desde `entities/`, las hace proponer cambios entre vecinos, evalúa su fitness (densidad de glifos y longitud de respuesta) y rankea las propuestas finales.

**¿Cómo se relaciona con el resto del sistema?**  
Depende de `core.ecosistema` (`Plano`), `core.semilla` (`poblar_entidades`), `core.llm.base` (`SustratoOpenAICompat`), `core.llm.config_loader` (`load_env`) y `core.juez` (`Juez`); además requiere `mision_reforma.txt` y la carpeta `entities/`.

**¿Es esencial o prescindible?**  
Prescindible para el funcionamiento base del ecosistema. Es una herramienta de meta-evolución o refactorización asistida por IA, no un módulo del núcleo operativo.