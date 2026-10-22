# INFORME: core/sandbox.py
Generado: 2026-10-22 03:47:58

1. **¿Qué es este archivo?**  
Módulo del `core/` para definir y coordinar simulaciones de interacciones simbióticas entre entidades.

2. **¿Qué hace?**  
- Modela parámetros, tipos de interacción y estados de simulación.  
- Registra iteraciones, impactos, observaciones e historial mediante dataclasses.  
- Valida duración, iteraciones, dominancia y nivel de ruido.  
- Controla mutaciones, aleatoriedad y límites temporales.  
- Integra opcionalmente el motor de glifos, el sistema inmune y el glosario matemático.

3. **¿Cómo se relaciona con el resto del sistema?**  
Importa `GlifoEngine`, `evaluar_evento_simbiótico` y `GlosarioMathema` mediante rutas relativas. Actúa como orquestador entre esos subsistemas. Si no están disponibles, registra una advertencia y continúa con funcionalidad degradada.

4. **¿Es esencial o prescindible?**  
**Esencial para la funcionalidad de simulación**, aunque no para el arranque completo del sistema. Sus dependencias externas son opcionales; solo sería prescindible si no se requieren simulaciones, resultados ni historial de interacciones.