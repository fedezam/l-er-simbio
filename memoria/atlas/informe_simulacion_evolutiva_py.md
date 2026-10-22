# INFORME: simulacion_evolutiva.py
Generado: 2026-10-22 03:09:10

## Mini-informe

1. **¿Qué es este archivo?**  
Script de arranque para preparar una simulación evolutiva con modelos de IA accesibles mediante OpenRouter.

2. **¿Qué hace?**  
- Consulta los modelos disponibles y filtra los gratuitos.  
- Prioriza modelos conocidos y prepara una cadena de fallback.  
- Configura `SustratoOpenAICompat`, realiza una prueba de conexión yVc intenta cambiar de modelo si falla.  
- Importa componentes para poblar el ecosistema, generar candidatos y evaluar soluciones mediante el `Juez` (el fragmento termina durante el fallback).

3. **¿Cómo se relaciona con el resto del sistema?**  
Depende de `core.ecosistema.Plano`, `core.semilla.poblar_entencias`, `core.llm.conector`, `core.llm.base` y `core.juez`; además, consume directamente la API de OpenRouter.

4. **¿Es esencial o prescindible?**  
Es esencial como punto de entrada ejecutable actual, aunque su lógica podría separarse en módulos. **Riesgo crítico:** contiene una clave de API hardcodeada; debe revocarse y sustituirse por una variable de entorno o gestor de secretos.