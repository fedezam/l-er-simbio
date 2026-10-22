# INFORME: entities/codeinsight/runner.py
Generado: 2026-10-22 03:40:38

**1. ¿Qué es este archivo?**  
`runner.py` es el punto de entrada que orquesta la ejecución del plan de CodeInsight.

**2. ¿Qué hace?**  
- **Funciones auxiliares:** `load_json`, `save_json` y `snapshot` manejan I/O de JSON y copias de seguridad.  
- **Clase `Runner`:**  
  - Inicializa rutas, carga configuración (`ghost.json`, `plan.json`, `capabilities.json`), estado de memoria y el adaptador LLM.  
  - Instancia `CodeInsightStrategy` con los recursos necesarios.  
  - El método `run` recorre las tareas del plan y delega a los métodos correspondientes de la estrategia (audit, translate, rename, update, refactor, generate_report).  
  - Actualiza la marca temporal y persiste la memoria.

**3. ¿Cómo se relaciona con el resto del sistema?**  
Importa `LLMAdapter` y `CodeInsightStrategy`, y depende de los archivos de configuración y de la estructura de directorios definida en `capabilities.json`. Actúa como puente entre la configuración del proyecto y la lógica de la estrategia.

**4. ¿Es esencial o prescindible?**  
Es esencial: coordina todo el flujo de trabajo, carga el estado y dispara las operaciones de la estrategia; sin él el proceso de CodeInsight no se ejecutaría.