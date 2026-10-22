# INFORME: fix_semilla.py
Generado: 2026-10-22 02:59:50

# Informe: `fix_semilla.py`

1. **¿Qué es este archivo?**  
   Script de parche que modifica `core/semilla.py` para filtrar entidades no esenciales.

2. **¿Qué hace?**  
   Inyecta un filtro en la función `poblar_entidades` de `semilla.py`, ignorando archivos JSON con `tipo` distinto de `"entidad_reflexiva"` o `"aprendiz"`.

3. **¿Cómo se relaciona con el sistema?**  
   Depende de `core/semilla.py` y utiliza `re` y operaciones de lectura/escritura de archivos. No importa módulos externos del sistema.

4. **¿Es esencial o prescindible?**  
   **Prescindible**. Es una herramienta de mantenimiento puntual para corregir la lógica de carga de entidades, no parte del núcleo funcional del sistema.