# INFORME: test_hibernacion.py
Generado: 2026-10-22 03:14:16



### Informe del Archivo: `test_hibernacion.py`

1. **¿Qué es este archivo?** Script de prueba automatizado para verificar el comportamiento de la nueva ley de hibernación en el ecosistema.
2. **¿Qué hace?** Inicializa el plano con un sustrato determinista, fuerza una edad alta y fitness bajo en las entidades para simular peligro de extinción, ejecuta un tick (`paso()`) y evalúa si estas sobreviven (hibernan) o mueren.
3. **¿Cómo se relaciona con el resto del sistema?** Depende de los módulos core (`Plano`, `poblar_entidades`, `SustratoDeterminista`) y carga las entidades predefinidas en la carpeta `entities/`.
4. **¿Es esencial o prescindible?** Es prescindible para el sistema productivo, pero esencial en el ciclo de desarrollo para garantizar que el parche de lógica de hibernación funciona correctamente antes del despliegue.