# INFORME: reforma_quirurgica.py
Generado: 2026-10-22 02:55:33

### 1. **¿Qué es este archivo?**
Script de orquestación para ejecutar una “reforma quirúrgica” sobre las entidades del sistema mediante un LLM y herramientas autorizadas.

### 2. **¿Qué hace?**
- Carga la configuración y la misión desde `mision_reforma.txt`.
- Crea el sustrato Groq (`gpt-oss-120b`), `Tools`, `Juez` y `Plano`.
- Pobló las entidades de `entities/` y les incorpora la misión.
- Procesa las entidades vivas, genera prompts, consulta al LLM y conserva sus historiales.
- Deteña llamadas `[TOOL: ...]`, aplica permisos por entidad y ejecuta herramientas como `read_file`, `propose_patch` y `apply_patch`.

### 3. **¿Cómo se relaciona con el resto del sistema?**
Depende de `core.ecosistema`, `core.semilla`, `core.llm`, `core.tools` y `core.juez`. Integra el LLM de Groq con el grafo de entidades y el sistema de herramientas.

### 4. **¿Es esencial o prescindible?**
Es **prescindible para el núcleo**, pero esencial para automatizar el flujo completo de reforma; sin él, las entidades no son convocadas ni pueden aplicar herramientas de forma coordinada.