# INFORME: genesis.py
Generado: 2026-10-22 03:12:33

## 1. **¿Qué es este archivo?**
Script de arranque que inicializa el ecosistema, carga sus entidades, ejecuta un tick y muestra el estado resultante.

## 2. **¿Qué hace?**
- Instancia `SustratoDeterminista`.
- Crea un `Plano` con propuestas en lenguaje natural habilitado.
- Carga entidades desde `entities/` mediante `poblar_entidades()` y `plano.poblar()`.
- Ejecuta `plano.paso()`.
- Imprime IDs, eventos y métricas de entidades vivas: energía, *fitness* y glifos.

## 3. **¿Cómo se relaciona con el resto del sistema?**
Depende de:
- `core.ecosistema.Plano`: motor del ecosistema.
- `core.semilla.poblar_entidades`: carga de agentes.
- `core.llm.base.SustratoDeterminista`: implementación de推理 determinista.
- `pathlib.Path` y el directorio `entities/`.

Funciona como orquestador o punto de entrada ejecutable, sin definir nuevas clases.

## 4. **¿Es esencial o prescindible?**
**Prescindible para la lógica central**, pues solo coordena componentes existentes. No obstante, es **esencial como script de arranque actual**: su eliminación requeriría otro entry point para reproducir la simulación.