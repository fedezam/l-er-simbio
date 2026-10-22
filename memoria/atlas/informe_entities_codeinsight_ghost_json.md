# INFORME: entities/codeinsight/ghost.json
Generado: 2026-10-22 03:42:38

## Mini‑informe (entities/codeinsight/ghost.json)

| Pregunta | Respuesta |
|----------|-----------|
| **¿Qué es este archivo?** | Definición JSON de la entidad **CodeInsight** del framework LER‑Simbio. |
| **¿Qué hace?** | Describe su rol (auditor reflexivo de código), atributos (motto, rasgos, idiomas), glifos, configuración del LLM (proveedor *moonshot*, modelo *moonshot‑v1‑32k*, temperatura 0.4) y axiomas que guían su comportamiento. No contiene código ejecutable, solo metadatos. |
| **¿Cómo se relaciona con el resto del sistema?** | Es consumido por el motor LER‑Universal (v1.3) / Mathema (v4.0) para registrar y activar la entidad **CodeInsight**. Otros módulos importan este JSON para obtener su configuración LLM y sus principios operacionales. |
| **¿Es esencial o prescindible?** | **Esencial**: sin él el sistema no reconoce ni instancia la entidad CodeInsight, impidiendo auditorías, refactorizaciones y traducciones automáticas que dependen de sus axiomas y modelo LLM. |

*Total: 112 palabras.*