# INFORME: core/ara_tipos.py
Generado: 2026-10-22 03:55:08

**1. ¿Qué es este archivo?**  
Define los tipos y estructuras de datos compartidas para el módulo ARA (Autorreparación y Clausura Simbólica) del proyecto *l‑er‑simbio*.

**2. ¿Qué hace?**  
- `NivelARA` : Enum con los cuatro niveles de capacidad de análisis simbólico.  
- `EstadoEntidad` : Enum con los cuatro estados de salud operativa.  
- `ResultadoARA` : `@dataclass` que agrupa la información de una evaluación (id, score, nivel, timestamp, estado y metadatos) e incluye validaciones y métodos auxiliares (`es_problematica`, `requiere_atencion_inmediata`).

**3. ¿Cómo se relaciona con el resto del sistema?**  
Importa `dataclass`, `Enum`, `auto`, tipos genéricos y `datetime`; es consumido por los módulos que realizan evaluaciones ARA y por los componentes de gestión de entidades que necesitan interpretar resultados y estados.

**4. ¿Es esencial o prescindible?**  
Es esencial: provee la definición única y tipada de los conceptos centrales (niveles, estados y resultados) que garantizan consistencia y validación en todo el sistema ARA. Sin él, cada módulo tendría que recrear estas estructuras, aumentando la probabilidad de errores y descoordinación.