# INFORME: tests/test_soma.py
Generado: 2026-10-22 03:25:34

**1. ¿Qué es este archivo?**  
Archivo de pruebas unitarias que verifica la evolución somática del ecosistema.  

**2. ¿Qué hace?**  
Define `_plano_con_soma()` que crea un `Plano` con un `Soma` y varios `Cuerpo`. Luego contiene cinco tests: rechazo de propuestas con canal ilegal, clamping del rango de valor, emergence y mutación del soma tras varios `paso()`, escritura cíclica de memoria episódica y garantía de que `Soma` puede existir sin genoma fijo.  

**3. Relación con el resto del sistema**  
Importa `Plano`, `Cuerpo`, `SustratoDeterminista`, `Propuesta` y `Soma` del paquete `core`. Los tests manipulan directamente estos objetos para validar su comportamiento interno.  

**4. ¿Es esencial o prescindible?**  
Es esencial: los tests cubren la lógica central de la soma (rechazo de propuestas, rangos, mutación y memoria), sin los cuales la evolución somática no podría garantizarse.