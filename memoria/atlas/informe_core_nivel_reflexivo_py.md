# INFORME: core/nivel_reflexivo.py
Generado: 2026-10-22 03:49:34

### 1. **¿Qué es este archivo?**
Módulo central para clasificar el nivel reflexivo de entidades simbióticas mediante un sistema híbrido.

### 2. **¿Qué hace?**
- `ReflexivityLevel`: define seis niveles, desde `primitive` hasta `master`.
- `HybridReflexiveProfile`: estructura perfiles con clasificación simple/avanzada, puntuaciones, protocolos, fortalezas, debilidades y recomendaciones; `to_dict()` los serializa.
- `HybridClassifier`: configura entidades centrales, roles arquitectónicos y protocolos asociados a cada categoría. El fragmento provided aparece incompleto durante `__init__`.

### 3. **¿Cómo se relaciona con el resto del sistema?**
Integra clasificadores simple y avanzado en una representation unificada. Solo utiliza dependencias estándar (`json`, `logging`, `dataclasses`, `enum`, `statistics` y `typing`); no se observan imports locales. Es el punto de intercambio entre clasificación rápida, análisis profundo y consumidores de los perfiles.

### 4. **¿Es esencial o prescindible?**
**Esencial** si el resto del sistema depende de niveles reflexivos, puntuación y protocolos. Podría desacoplarse trasladando el modelo a un servicio compartido, pero eliminarlo obligaría a duplicar lógica de clasificación.