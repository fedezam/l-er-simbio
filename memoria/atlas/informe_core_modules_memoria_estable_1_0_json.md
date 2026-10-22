# INFORME: core/modules/memoria_estable_1_0.json
Generado: 2026-10-22 04:13:02

## Informe del archivo `core/modules/memoria_estable_1_0.json`

| Pregunta | Respuesta |
|----------|-----------|
| **¿Qué es este archivo?** | Es el descriptor JSON de la versión *MEMORIA ESTABLE 1.0* que define la configuración base del ecosistema simbiótico LER. |
| **¿Qué hace?** | - Declara la versión, fecha y descripción.<br>- Lista los componentes críticos (lenguaje, glifos, operadores Mathema, manifiestos, parser, ejecutor, pruebas de reflexividad, scripts de inicio, etc.).<br>- Registra las entidades fundacionales (`AXIOMA`, `GUARDA`, `VELM`, `RACUL`). |
| **¿Cómo se relaciona con el resto del sistema?** | Cada ruta apuntada (`/core/ler_parser.py`, `/core/entity_runner.py`, `/docs/...`) es importada o invocada por el motor LER en tiempo de arranque; los glifos y la ley sintáctica son consumidos por el parser y el ejecutor, mientras que los scripts `START.*` usan este JSON para cargar la configuración. |
| **¿Es esencial o prescindible?** | **Esencial**: sin él el núcleo no conoce su propia versión, los componentes a cargar ni las entidades básicas, impidiendo la inicialización y la auto‑defensa simbólica del sistema. |