# INFORME: core/ler.core.json
Generado: 2026-10-22 03:48:30

## 1. ¿Qué es este archivo?
Manifiesto central de configuración de **LER Core v1.5.0**, que registra rutas, módulos, sintaxis, seguridad, memoria, entidades y metadatos del sistema.

## 2. ¿Qué hace?
No contiene funciones ni clases propias. Coordina componentes como `entity_runner.py`, `ler_parser.py`, `reflexivity_test.py`, `axiom.py`, `guard.py`, `glyph_engine.py`, `sandbox.py` e `immune_system.py`. También define operadores matemáticos, reglas sintácticas, glifos de alerta, umbrales de seguridad, carga y validación de entidades, respaldos de memoria y opciones de ejecución.

## 3. ¿Cómo se relaciona con el resto del sistema?
No realiza imports. Actúa como índice y configuración: declara dependencias hacia módulos Python, `glyphs/universal_glyphs.json`, memoria estable, entidades, árbol, documentación y scripts `start.bat`/`start.sh`. Requiere **Python 3.8+** y activa entidades al cargar, con validación obligatoria.

## 4. ¿Es esencial o prescindible?
**Es esencial para la operación integrada**, pues centraliza rutas, controles y parámetros de seguridad. Su eliminación o desalineación impediría localizar componentes y aplicar coherentemente las reglas del sistema, salvo que otros componentes mantengan una configuración equivalente.