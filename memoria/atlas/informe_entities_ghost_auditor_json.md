# INFORME: entities/ghost_auditor.json
Generado: 2026-10-22 03:32:01

1. **¿Qué es este archivo?**  
   Configuración declarativa de la entidad reflexiva `arbiter.planificador` para auditar y estabilizar el ecosistema LER.

2. **¿Qué hace?**  
   No define funciones ni clases ejecutables. Define identidad, axiomas, estado cognitivo, heurísticas de prioridad, estrategia de corrección, verificación y prompts para el flujo `THINK → PLAN → CONFIRM → DO`. El fragmento provided está truncado dentro de `CONFIRM`, por lo que el JSON no parece completo.

3. **¿Cómo se relaciona con el resto del sistema?**  
   No tiene imports. Depende conceptualmente de LER, Mathema, sus glifos y módulos del repositorio; prioriza entrypoints, configuración, dependencias, pruebas y documentación. Sus planes deben producir cambios atómicos y verificables.

4. **¿Es esencial o prescindible?**  
   Es esencial si el orquestador utiliza sus prompts y axiomas para governar reparaciones. Es prescindible para la ejecución directa del código, pues no implementa lógica por sí mismo; únicamente configura comportamiento.