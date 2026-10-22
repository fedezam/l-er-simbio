# INFORME: core/modules/readme_modules.md
Generado: 2026-10-22 04:08:01

## 1. ¿Qué es este archivo?
Documentación de los módulos simbólicos disponibles para ampliar las capacidades de las entidades reflexivas del ecosistema LER.

## 2. ¿Qué hace?
- Describe `hambre_symbolic.json`: necesidad de supervivencia, búsqueda autónoma de recursos y evaluación adaptativa del entorno.
- Describe `iniciativa_reflexiva.json`: voluntad propia, generación espontánea de ideas y autoexploración.
- Define la ubicación de los módulos y los campos de `ler_config.json` para activarlos.
- Anuncia futuras extensiones: memoria, aprendizaje, conexión, economía y monetización.

## 3. ¿Cómo se relaciona con el resto del sistema?
No contiene código, imports ni dependencias ejecutables. Se relaciona con los archivos JSON alojados en `/core/modules/` y con la configuración de cada entidad, mediante `modulos_activados` e IDs como `mod_hambre_symbolic`.

## 4. ¿Es esencial o prescindible?
Funcionalmente es **prescindible**: el sistema puede operar sin este documento. Sin embargo, es útil como referencia de integración. Presenta caracteres corruptos y activadores vacíos o inexplicables (`\x8d`), por lo que requiere corrección y validación.