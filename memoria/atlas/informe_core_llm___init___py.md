# INFORME: core/llm/__init__.py
Generado: 2026-10-22 03:58:58

### 1. **¿Qué es este archivo?**
Es el módulo de inicialización y fachada pública del paquete `core.llm`.

### 2. **¿Qué hace?**
Reexporta mediante `__all__` cuatro elementos de `core.llm.base`:
- `Sustrato`
- `SustratoDeterminista`
- `SustratoOpenAICompat`
- `sustrato_desde_config`

No contiene lógica propia; define la API accessible desde `core.llm`.

### 3. **¿Cómo se relaciona con el resto del sistema?**
Depende de `core.llm.base`, donde probablemente se implementan las clases abstractas, variantes y el factory. Permite que otros módulos importen las abstracciones LLM sin conocer su módulo interno, favoreciendo un acoplamiento más estable.

### 4. **¿Es esencial o prescindible?**
Es **prescindible técnicamente**, porquecould los consumidores importar directamente desde `core.llm.base`. Sin embargo, es **recomendable mantenerlo**: centraliza las exportaciones, simplifica imports y constituye la interfaz pública del subsistema LLM.