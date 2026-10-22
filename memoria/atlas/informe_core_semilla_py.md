# INFORME: core/semilla.py
Generado: 2026-10-22 02:28:47

### Informe: `core/semilla.py`

1. **¿Qué es este archivo?**
Módulo de inicialización que convierte definiciones JSON estáticas en instancias activas de `Cuerpo` para el ecosistema LER.

2. **¿Qué hace?**
*   **`_aplanar`**: Serializa diccionarios anidados en texto plano, filtrando credenciales sensibles.
*   **`sembrar_desde_json`**: Crea un `Cuerpo` individual, asignando glifos según su linaje y deduciendo su especialidad (código, auditoría, etc.) si no está explícita.
*   **`poblar_entidades`**: Escanea recursivamente el directorio `entities/`, filtrando solo entidades válidas y gestionando colisiones de nombres mediante sufijos.

3. **¿Cómo se relaciona con el resto del sistema?**
Depende de `core.ecosistema.Cuerpo` para la estructura de datos. Actúa como la "puerta de entrada" del sistema: transforma la configuración declarativa (`*.json`) en el estado inicial que el LLM (sustrato) utilizará para interactuar.

4. **¿Es esencial o prescindible?**
**Esencial.** Sin este módulo, las entidades JSON permanecerían como datos inertes. Es el único componente que "hidrata" la identidad, glifos y especialidad de cada agente, permitiendo que el ecosistema funcione.