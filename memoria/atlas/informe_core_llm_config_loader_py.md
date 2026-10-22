# INFORME: core/llm/config_loader.py
Generado: 2026-10-22 04:00:06

## 1. ¿Qué es este archivo?  
Módulo de configuración que carga variables de entorno y devuelve la clave de API requerida.

## 2. ¿Qué hace?  
- **`load_env()`**: lee el archivo `.env` (ubicado tres niveles arriba) y exporta sus pares `KEY=VALUE` a `os.environ`.  
- **`get_api_key(provider)`**: asegura que el `.env` esté cargado, selecciona la clave correspondiente (`OPENROUTER_KEY` o `GROQ_KEY`) y lanza una excepción si falta o contiene el placeholder `"tu_clave"`.

## 3. ¿Cómo se relaciona con el resto del sistema?  
- Importa `os` y `Path` de la biblioteca estándar.  
- Es llamado por los componentes que interactúan con LLMs (p. ej., `core/llm/client.py`) para obtener credenciales de proveedores externos.  
- No depende de paquetes externos, solo del archivo `.env` del proyecto.

## 4. ¿Es esencial o prescindible?  
Es esencial: sin él los módulos que consumen APIs de LLM no pueden obtener sus claves, provocando fallos de autenticación. Su ausencia obliga a gestionar manualmente las variables de entorno, rompiendo la consistencia del proyecto.