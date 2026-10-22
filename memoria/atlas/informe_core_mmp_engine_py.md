# INFORME: core/mmp_engine.py
Generado: 2026-10-22 03:50:31

1. **¿Qué es este archivo?**
Un motor de archivo back-end ligero para gestionar la Meta-Memoria de Preguntas (MMP).

2. **¿Qué hace?**
Define un schema JSON base y proporciona la clase `MMPEngine` para cargar, guardar y operar sobre preguntas y mutaciones experimentales, utilizando `AtomicFileWriter` para escrituras atómicas.

3. **¿Cómo se relaciona con el resto del sistema?**
Depende exclusivamente de la biblioteca estándar (`json`, `os`, `threading`, `datetime`). Es un módulo autocondenado diseñado para entornos limitados.

4. **¿Es esencial o dispensible?**
Esencial para prototipos rápios (Colab/Drive); dispensable en producción escalada, donde se requiere una base de藉数据库 real y concurrente.