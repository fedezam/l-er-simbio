# INFORME: tools/visualizador/stats_ler.json
Generado: 2026-10-22 04:14:34

## Mini‑informe: `tools/visualizador/stats_ler.json`

| Pregunta | Respuesta |
|----------|-----------|
| **¿Qué es este archivo?** | Un archivo JSON que almacena estadísticas de uso del visualizador de *l‑er‑simbio*. |
| **¿Qué hace?** | Contiene cuatro claves: `uso_por_glifo`, `categorias_accedidas`, `sesiones_totales` y `cadenas_creadas`. Cada una registra contadores o mapas que el visualizador actualiza en tiempo de ejecución para llevar registro de la interacción del usuario. |
| **¿Cómo se relaciona con el resto del sistema?** | Es leído y escrito por los scripts dentro de `tools/visualizador/` (p. ej., `visualizador.py`). No hay imports directos en código fuente, pero depende de la lógica de la UI que llama a `json.load`/`json.dump` para persistir los datos. |
| **¿Es esencial o prescindible?** | **Prescindible** para el núcleo funcional del proyecto; solo aporta métricas de uso. Si se elimina, el visualizador seguirá operando, aunque se perderá el historial de estadísticas. |

*Nota:* El archivo está vacío (todos los contadores a 0), lo que indica que aún no se ha generado actividad.