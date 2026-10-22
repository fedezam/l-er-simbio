# INFORME: entities/codeinsight/seed_prompt.txt
Generado: 2026-10-22 03:40:09

### 1. **¿Qué es este archivo?**
Semilla de prompt que define a **CodeInsight**, una entidad LER reflexiva para análisis de código.

### 2. **¿Qué hace?**
No contiene funciones ni clases. Establece directrices para:
- Mantener coherencia entre nombres, módulos y documentación.
- Observar el código antes de modificarlo y resumir su intención.
- Proponer al menos dos alternativas ante cambios no triviales.
- Justificar trade-offs y explicar el flujo de control.
- Señalar cuellos de botella y mostrar diffs mínimos al depurar.
- Usar un estilo conciso, didáctico y humano.

### 3. **¿Cómo se relaciona con el resto del sistema?**
No tiene imports ni dependencias ejecutables. Es configuración textual que presumiblemente carga la orquestación LER o el generador de prompts de `entities/codeinsight`.

### 4. **¿Es esencial o prescindible?**
Es **prescindible técnicamente**, pero importante semánticamente: sin él, CodeInsight pierde su identidad y reglas de razonamiento. Solo debería eliminarse si se sustituye por unas directrices equivalentes.