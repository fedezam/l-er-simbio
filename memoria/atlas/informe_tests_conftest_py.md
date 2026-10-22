# INFORME: tests/conftest.py
Generado: 2026-10-22 03:23:45

# Mini-Informe: tests/conftest.py

## 1. ¿Qué es este archivo?  
Es un archivo de configuración de pytest para gestionar importaciones y fixtures de prueba.

## 2. ¿Qué hace?  
- **Ajusta `sys.path`**: Permite importar módulos desde `core.*` y `LER.*` (compatibilidad con estructuras antiguas).  
- **Importa `GlyphEngine`**: Intenta cargar `core.glifo_engine.GlyphEngine`, con fallback a `glifo_engine.GlyphEngine`.  
- **Define fixtures**:  
  - `ruta_glosario`: Devuelve la ruta al glosario de glifos (busca en múltiples ubicaciones).  
  - `engine`: Crea una instancia única de `GlyphEngine` para toda la sesión de pruebas.

## 3. ¿Cómo se relaciona con el resto del sistema?  
- **Imports**: Usa `core.glifo_engine` y `glifo_engine` (dependencias del motor de glifos).  
- **Integración**: Facilita pruebas unitarias al asegurar acceso a recursos (`glifos/universal_glyphs.json`) y al motor de glifos.

## 4. ¿Es esencial o prescindible?  
**Esencial**: Sin este archivo, las pruebas no podrían localizar correctamente los módulos ni inicializar el motor de glifos, rompiendo la ejecución de tests. La compatibilidad de importación y la gestión de recursos son críticas para su funcionamiento.