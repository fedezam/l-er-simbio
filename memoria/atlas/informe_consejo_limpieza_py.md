# INFORME: consejo_limpieza.py
Generado: 2026-10-22 03:08:34

**MINI-INFORME TÉCNICO - CRAWLER ESPECIALIZADO**

**Archivo:** `consejo_limpieza.py`
**Repositorio:** l-er-simbio

---

**1. Naturaleza del Archivo**
Script de orquestación multi-fase para la gestión automatizada del ciclo de vida de repositorios mediante LLMs.

**2. Función Principal**
Automatiza el proceso de propuesta y auditoría de planes de limpieza mediante dos agentes de IA especializados (PyCodex y Auditor_LER).

**3. Componentes Clave**
- **Cliente LLM**: Integración con Groq API (`openai/gpt-oss-120b`) para inferencia.
- **Fuente de Contexto**: Atlas del repositorio (`memoria/atlas/ATLAS_LER.md`) como base de conocimiento.
- **Fase 1**: PyCodex analiza el Atlas y genera plan de limpieza estructurado (BORRAR/MANTENER/REVISAR).
- **Fase 2**: Auditor_LER evalúa el plan propuesto, validando decisiones y marcando rechazos/aprobaciones.

**4. Relación con el Sistema**
Componente crítico del módulo de mantenimiento inteligente. Depende de la infraestructura LLM central y del Atlas generado previamente por crawlers.

**5. Valoración**
**Esencial** para el framework de limpieza proactiva. No debe eliminarse, pero su ejecución requiere monitoreo y posible intervención humana para casos límite.