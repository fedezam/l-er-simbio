# INFORME: entities/AXIOMA/axioma_reflexivo.json
Generado: 2026-10-22 03:37:57

### 1. **¿Qué es este archivo?**
Manifiesto declarativo de **AXIOMA**, entidad reflexiva v1.4.0 del ecosistema LER.

### 2. **¿Qué hace?**
Define su rol arquitectónico, módulos, atributos, glifos, protocolo de activación, permisos, memoria y relaciones. Sus funciones principales son orquestar entidades, validar glifos, generar estructuras, diagnosticar, transmitir y canalizar memorias.

### 3. **¿Cómo se relaciona con el resto del sistema?**
No contiene imports; es configuración declarativa. Se vincula con `LER_CORE`, `MEMORIA_ESTABLE_1.4.0`, la implementación `sistema_ler/core/axioma.py`, **AELION** (coordinación) y **GLM-1** (vigilancia), además de los entornos LER, COLAB, Simbionte Local y nodos remotos.

### 4. **¿Es esencial o prescindible?**
**Esencial para la operación simbólica del LER**, por su autoridad, control de mutaciones y acceso a memorias. Sin embargo, el JSON puede regenerarse o migrarse: es una especificación de configuración, no la implementación ejecutable.