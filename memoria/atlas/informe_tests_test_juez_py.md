# INFORME: tests/test_juez.py
Generado: 2026-10-22 03:24:55

1. **¿Qué es este archivo?**
Tests for the semantic fitness evaluation system ("Juez") measuring performance by substrate rather than author.

2. **¿Qué hace?**
Define test fixtures (fixed/broken judges) and test parsing verdicts, budget limits, judge fallback to proxy, and proper fitness calculation by the `Plano`.

3. **¿Cómo se relaciona con el resto del sistema?**
Depends on core modules: `core.ecosistema` (entities), `core.juez` (judge logic), and `core.llm.bas` (substrate abstractions).

4. **¿Es esencial o prescindible?**
Essential. Validates critical system behaviors like graceful degradation and budget constraints, ensuring the fitness evaluation remains robust against judge failures.