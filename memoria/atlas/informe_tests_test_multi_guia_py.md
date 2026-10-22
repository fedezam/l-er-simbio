# INFORME: tests/test_multi_guia.py
Generado: 2026-10-22 03:28:17

### 1. ¿Qué es este archivo?
Un script de prueba/integración que simula una sesión de reflexión circular entre múltiples instancias de `GuiaReflexiva`.

### 2. ¿Qué hace?
Define `circular_reflection_session(rounds)`, que crea tres guías (A, B, C) y las encadena en un bucle cerrado: A guía a una entidad, B reflexiona sobre A, C sobre B, y C retorna la insight a A como nuevo estado. Incluye bloque `main` para ejecutar 3 rondas e imprimir resultados en JSON.

### 3. ¿Cómo se relaciona con el resto del sistema?
Importa `json` y la clase `GuiaReflexiva` desde `entities.guia_reflexiva`. Depende del método `guide_entity` de esa entidad para generar respuestas estructuradas.

### 4. ¿Es esencial o prescindible?
Prescindible. Ubicado en `tests/`, funciona como demo o prueba de comportamiento recursivo/multi-agente; no es requerido para el núcleo operativo del sistema.