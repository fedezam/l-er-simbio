# INFORME: tests/test_ecosistema.py
Generado: 2026-10-22 03:22:34

**1. ¿Qué es este archivo?**  
Archivo de pruebas unitarias para el módulo del ecosistema del autómata semántico.

**2. ¿Qué hace?**  
Valida cuatro comportamientos: reproductibilidad con misma semilla, ocurrencia de hidratación en entidades vivas, muerte por inanición cuando la energía es escasa, y archivado de entidades muertas en un cementerio sin borrado. Incluye la función auxiliar `_poblacion_inicial()` y cuatro funciones `test_*`.

**3. ¿Cómo se relaciona con el resto del sistema?**  
Importa `SustratoDeterminista` de `core.llm.base` y `Plano`, `Cuerpo` de `core.ecosistema`. Añade la raíz del repositorio a `sys.path` para resolver los módulos internos.

**4. ¿Es esencial o prescindible?**  
Prescindible en producción, pero esencial para garantizar calidad, evitar regresiones y verificar el determinismo del núcleo del ecosistema.