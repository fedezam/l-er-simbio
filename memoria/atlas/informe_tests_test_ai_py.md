# INFORME: tests/test_ai.py
Generado: 2026-10-22 03:27:11

**1. ¿Qué es este archivo?**  
Script de prueba que invoca la API de Zhipu para obtener una respuesta del modelo *glm‑4*.

**2. ¿Qué hace?**  
- Define `api_key`, `endpoint` y el payload con un mensaje de usuario.  
- Envía una petición POST a `https://open.bigmodel.cn/api/paas/v4/chat/completions`.  
- Imprime la respuesta o cualquier error de comunicación.

**3. ¿Cómo se relaciona con el resto del sistema?**  
Depende exclusivamente de la librería `requests` y de la API externa de BigModel. No utiliza módulos propios del repositorio; sirve como integración de prueba entre el código interno y el servicio de IA.

**4. ¿Es esencial o prescindible?**  
**Esencial.** Sin esta llamada no se puede validar que el pipeline de IA funcione correctamente en el entorno de pruebas.  

*(≈115 palabras)*