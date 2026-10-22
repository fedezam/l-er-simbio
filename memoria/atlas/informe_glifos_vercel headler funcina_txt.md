# INFORME: glifos/vercel headler funcina.txt
Generado: 2026-10-22 03:46:11

**1. ¿Qué es este archivo?**  
Es un endpoint API de Vercel (`handler`) que genera un prompt de asistente IA a partir de datos JSON externos.

**2. ¿Qué hace?**  
- Valida el parámetro `json` y permite solo dominios en una whitelist.  
- Descarga el JSON, extrae información de comercio, tratamientos, productos y la configuración de la IA.  
- Construye un mensaje “natural” con los datos (máximo 5 tratamientos y 5 productos).  
- Añade o suprime instrucciones según la variable `HIDE_INSTRUCTIONS` o el query `hide`.

**3. ¿Cómo se relaciona con el resto del sistema?**  
No importa módulos externos; depende de `fetch` (API de Node/Vercel) y de variables de entorno. Sirve como puente entre datos externos y la UI/cliente que consume el prompt.

**4. ¿Es esencial o prescindible?**  
Es esencial si la aplicación necesita generar dinámicamente prompts personalizados para la IA; de lo contrario, podría reemplazarse por un archivo estático o una lógica más simple.