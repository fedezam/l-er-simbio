# INFORME: evolucion.py
Generado: 2026-10-22 02:53:12

# Mini-Informe: evolucion.py

## 1. ¿Qué es este archivo?
Es el script principal que orquesta la simulación evolutiva de entidades en un ecosistema, integrando modelos de lenguaje y evaluación.

## 2. ¿Qué hace?
- Inicializa un `Plano` (ecosistema) con un pool de modelos (`conector_universal`).
- Crea entidades (`poblar_entidades`) y les inyecta una misión desde `mision.py`.
- Ejecuta 5 ticks de evolución, registrando eventos y actualizando la población.
- Muestra las entidades más fitnes al finalizar.

## 3. ¿Cómo se relaciona con el resto del sistema?
Importa y coordina módulos clave:
- `core.ecosistema.Plano`: Gestiona el entorno evolutivo.
- `core.llm.conector`: Rotación de modelos (OpenRouter).
- `core.juez.Juez`: Evalúa propuestas.
- `entities/`: Carga entidades personalizadas.

## 4. ¿Es esencial o prescindible?
**Esencial**. Actúa como núcleo de la simulación, integrando todos los componentes y dirigiendo su interacción. Sin él, el sistema no ejecuta su flujo evolutivo.