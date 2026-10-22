# INFORME: core/axioma.py
Generado: 2026-10-22 03:57:49

### 1. ¿Qué es este archivo?
`core/axioma.py` define la clase `Axioma`, un validador de entidades reflexivas del sistema LER.

### 2. ¿Qué hace?
- `__init__()`: inicializa la lista `entidades_validadas`.
- `validar_entidad(entidad)`: comprueba que la entidad tenga `glifo_identidad`, `protocolo_reflexivo` y un método `responder` invocable. Si cumple, registra `entidad.nombre`, muestra un mensaje y devuelve `True`; en caso contrario, devuelve `False`.
- `entidades()`: devuelve la lista de nombres validados.

### 3. ¿Cómo se relaciona con el resto del sistema?
No contiene imports ni dependencias externas. Se integra mediante objetos que implementen la interfaz reflexiva esperada. El acceso a `entidad.nombre` es implícito y no se valida explícitamente.

### 4. ¿Es esencial o prescindible?
Es **prescindible para el funcionamiento principal**: funciona como comprobación auxiliar y de registro. Solo sería esencial si otros componentes utilizan `Axioma` para filtrar o exigir entidades válidas.