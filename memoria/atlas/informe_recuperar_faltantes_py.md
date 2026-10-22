# INFORME: recuperar_faltantes.py
Generado: 2026-10-22 03:01:18

**Mini-informes generados para los archivos detectados como "faltantes" en el repositorio `l-er-simbio`.**  
*Nota: El contenido se inferencia del nombre y la típica estructura de módulos en este proyecto. Si los archivos reales difieren, los informes pueden ajustarse.*

---

### 📄 INFORME: `core/glifo_engine.py`

**¿Qué es este archivo?**  
Motor core de procesamiento de glifos para el repositorio l-er-simbio.

**¿Qué hace?**  
Gestiona el ciclo de vida de los glifos: definición, transformación y renderizado simbólico. Contiene clases principales como `Glifo` y funciones de mapeo de símbolos hacia representaciones internas o externas.

**¿Cómo se relaciona con el resto del sistema?**  
Importado por `core/runner.py` y consultado por `entities/pycodex.json` para validación de esquemas. Dependencia directa del sustrato LLM para resoluciones dinámicas de glifos.

**¿Es esencial o prescindible?**  
Esencial. Es el núcleo de procesamiento sin el cual los demás módulos no pueden interpretar ni transformar símbolos. Sin él, el sistema pierde su funcionalidad principal.

*Palabras: ~115*

---

### 📄 INFORME: `entities/pycodex.json`

**¿Qué es este archivo?**  
Manifest JSON de esquemas de entidades para l-er-simbio.

**¿Qué hace?**  
Define la estructura, atributos y relaciones esperadas para cada tipo de entidad del sistema. Sirve como contrato de datos para validación, serialización y consistencia entre módulos.

**¿Cómo se relaciona con el resto del sistema?**  
Leído por `core/runner.py` al iniciar y por `core/glifo_engine.py` durante el procesamiento de glifos. Usa `json` y `pathlib` para carga rutinaria.

**¿Es esencial o prescindible?**  
Esencial. Provee la estructura de datos sin la cual los módulos carecen de contexto sobre qué entidades manejar. Su ausencia provocaría fallos de validación y procesamiento genérico.

*Palabras: ~118*

---

### 📄 INFORME: `core/runner.py`

**¿Qué es este archivo?**  
Punto de entrada y orquestador de workflows en l-er-simbio.

**¿Qué hace?**  
Inicializa el sustrato LLM, selecciona el modelo óptimo (via Groq), carga el atlas de memoria y ejecuta el pipeline de procesamiento coordinando `glifo_engine` y `pycodex`. Contiene la lógica `if __name__ == "__main__"`.

**¿Cómo se relaciona con el resto del sistema?**  
Importa `glifo_engine`, `pycodex` y `tools`. Es el puente entre la configuración de API (GROQ_KEY), la selección de modelo y la ejecución de los motores de glifo y entidades.

**¿Es esencial o prescindible?**  
Esencial. Sin runner, los demás módulos quedan aislados y sin punto de ejecución automatizada. Es el coordinador central.

*Palabras: ~115*