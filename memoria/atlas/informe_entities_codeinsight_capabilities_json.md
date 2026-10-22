# INFORME: entities/codeinsight/capabilities.json
Generado: 2026-10-22 03:39:02

## 1. ¿Qué es este archivo?  
Archivo de configuración JSON que declara las capacidades requeridas por el motor **codeinsight** y sus parámetros operativos.

## 2. ¿Qué hace?  
- Lista las capacidades obligatorias (`required_capabilities`).  
- Define la configuración concreta de cada capacidad (snapshots, tracking, persistencia, traducción, auto‑apply, generación de reportes y telemetría).

## 3. ¿Cómo se relaciona con el resto del sistema?  
- Es leído por el módulo central de **codeinsight** al iniciar, mediante `import json` y `load_capabilities()`.  
- Cada clave se corresponde con clases/servicios en `entities/codeinsight/capabilities/` que implementan la lógica (p. ej., `FileSnapshots`, `ProgressTracking`, `TranslationEngine`).  
- Los valores configuran rutas, flags y comportamientos usados por esos componentes.

## 4. ¿Es esencial o prescindible?  
Es **esencial**: sin él el motor no conoce qué funcionalidades activar ni cómo configurarlas, lo que impediría la captura de snapshots, el seguimiento de progreso, la traducción automática y la generación de reportes.