# INFORME: core/soma.py
Generado: 2026-10-22 02:28:30

### Informe: `core/soma.py`

1. **¿Qué es este archivo?**
El módulo que gestiona el "tejido vivo" del sistema, permitiendo mutaciones reversibles de parámetros operativos sin alterar el código fuente.

2. **¿Qué hace?**
Define la clase `Soma` y la estructura `Propuesta`. Implementa un mecanismo de whitelist estricto (`CANALES_SOMATICOS`) para validar cambios en umbrales de coherencia, mutación y costos metabólicos. Gestiona el ciclo de vida de las propuestas (pendiente, activa, rechazada) y mantiene un historial auditable (`registro`) para permitir la reversión automática ante fallos.

3. **¿Cómo se relaciona con el resto del sistema?**
Depende únicamente de librerías estándar (`json`, `dataclasses`, `pathlib`, `typing`). Actúa como capa de delegación para el `Plano`: este último consulta `Soma.get()` para obtener parámetros vivos en lugar de valores estáticos, y delega la validación de mutaciones aquí.

4. **¿Es esencial o prescindible?**
**Esencial.** Sin este módulo, el sistema carece de su capacidad de auto-optimización y adaptación dinámica. Es el núcleo de la "evolución somática", garantizando que los cambios sean seguros, acotados y reversibles, protegiendo así la integridad del ADN (código) mientras permite la adaptación del entorno.