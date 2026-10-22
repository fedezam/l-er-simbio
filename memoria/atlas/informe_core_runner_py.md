# INFORME: core/runner.py
Generado: 2026-10-22 02:31:36

### Informe: `core/runner.py`

1. **¿Qué es este archivo?**
   Es el punto de entrada principal (CLI) que orquesta la ejecución del plano evolutivo LER.

2. **¿Qué hace?**
   *   **`main()`**: Gestiona argumentos de línea de comandos (ticks, semilla, configuración).
   *   **Configuración del Sustrato**: Determina si usar un LLM externo (vía env vars o config JSON) o un sustrato determinista local. Soporta "conector universal" para failover entre modelos.
   *   **Inicialización de Componentes**: Crea instancias de `Soma` (evolución somática), `Juez` (fitness semántico con presupuesto limitado) y `Plano`.
   *   **Ejecución**: Población inicial de entidades y arranque del ciclo de simulación.

3. **¿Cómo se relaciona con el resto del sistema?**
   *   **Dependencias clave**: Importa `Plano` (motor de simulación), `Juez` (evaluación), `Soma` (adaptación estructural), `conector_universal` y `sustrato_desde_config` (capa LLM), y `poblar_entidades` (carga de datos).
   *   **Rol**: Actúa como el "pegamento" que inyecta la configuración externa en las entidades internas del núcleo.

4. **¿Es esencial o prescindible?**
   **Esencial**. Sin este archivo, no hay forma de inicializar el sistema, cargar las entidades ni ejecutar los ticks de evolución. Es el único punto de arranque operativo del repositorio.