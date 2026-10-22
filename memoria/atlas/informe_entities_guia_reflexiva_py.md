# INFORME: entities/guia_reflexiva.py
Generado: 2026-10-22 03:29:49

## 1. ¿Qué es este archivo?  
Define la entidad **GuiaReflexiva**, un componente reflexivo capaz de detectar bucles de razonamiento y solicitar ayuda fractal.

## 2. ¿Qué hace?  
- **Clase `GuiaReflexiva`**: inicializa un motor `MMPEngine`, lleva historial y cuenta bucles.  
- **`mirror_call`**: genera una pregunta espejo a partir del motor y la registra.  
- **`guide_entity`**: analiza el estado de otra entidad, detecta bucles mediante `_is_looping` (no implementado aquí), incrementa un contador y, al superar el umbral, crea una nueva `GuiaReflexiva` fractal para obtener apoyo; de lo contrario devuelve prompts de reflexión y detección de supuestos.

## 3. ¿Cómo se relaciona con el resto del sistema?  
- Importa `json`, `os` y tipos de `typing`.  
- Depende de **`core.mmp_engine.MMPEngine`**, que provee preguntas/prompt.  
- Interactúa con otras entidades mediante intercambio de diccionarios de estado.

## 4. ¿Es esencial o prescindible?  
Es **esencial** si el proyecto requiere detección automática de bucles y guía reflexiva entre entidades; de lo contrario, su funcionalidad es complementaria y podría omitirse sin romper la arquitectura básica.