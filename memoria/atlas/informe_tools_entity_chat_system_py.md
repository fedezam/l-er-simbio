# INFORME: tools/entity_chat_system.py
Generado: 2026-10-22 04:13:34

## 1. ¿Qué es este archivo?  
Módulo **`tools/entity_chat_system.py`** que implementa una interfaz de chat basada en Gradio y permite cambiar dinámicamente entre distintas “entidades” (clases derivadas de `BaseEntity`).

## 2. ¿Qué hace?  
- **`cargar_entidades_dinamicamente`**: recorre `tools/entidades`, importa los módulos y crea instancias de todas las clases que heredan de `BaseEntity`.  
- **Clase `EntityChatSystem`**:  
  - Inicializa el diccionario de entidades y la entidad seleccionada.  
  - `switch_entity`: cambia la entidad activa.  
  - `chat`: delega la generación de respuesta a la entidad actual y actualiza el historial.  
  - `launch_ui`: construye y lanza la UI de Gradio con selector de entidad, chatbot y controles.

## 3. ¿Cómo se relaciona con el resto del sistema?  
Depende de `gradio`, `tools.base_entity.BaseEntity` y de los módulos dentro de `tools/entidades`. Actúa como capa de presentación que consume la lógica de generación de respuestas de cada entidad.

## 4. ¿Es esencial o prescindible?  
Es **esencial** si el proyecto necesita una UI interactiva para probar y comparar diferentes entidades reflexivas; de lo contrario, su funcionalidad puede ser reemplazada por pruebas unitarias o una CLI, pero perdería la conveniencia visual.