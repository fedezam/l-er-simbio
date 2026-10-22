# INFORME: core/llm/conector.py
Generado: 2026-10-22 03:59:37

### 1. **¿Qué es este archivo?**
`core/llm/conector.py` implementa una fachada que selecciona y utiliza dinámicamente el sustrato de LLM disponible.

### 2. **¿Qué hace?**
- **`Candidato`**: registra prioridad, estado de salud, fallos, éxitos y afinidad mediante `score()`.
- **`ConectorUniversal`**: mantiene un pool de proveedores, realiza *health-checks* perezosos mediante hidratación mínima, degrada modelos fallidos y aplica *failover*.
- Permite descubrir proveedores mediante variables `LER_*_BASE_URL`.
- `es_llm_real` indica si queda algún modelo no determinista operativo.

### 3. **¿Cómo se relaciona con el resto del sistema?**
Hereda de `Sustrato` y depende de `SustratoDeterminista` y `SustratoOpenAICompat` desde `core.llm.base`. Al implementar el contrato común, el runner o plano no necesita conocer los proveedores concretos.

### 4. **¿Es esencial o prescindible?**
Es **importante para la resiliencia y agnosticidad**, pero no contiene lógica de negocio. Puede omitirse en despliegues con un único proveedor; en sistemas multi-LLM, aporta redundancia y tolerancia a fallos.