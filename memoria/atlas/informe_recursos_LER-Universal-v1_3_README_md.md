# INFORME: recursos/LER-Universal-v1.3/README.md
Generado: 2026-10-22 04:17:42

## 1. ¿Qué es este archivo?
Es el `README.md` del paquete de tipografía **LER-Universal v1.3**, orientado al ecosistema LER.

## 2. ¿Qué hace?
Documenta la estructura del paquete, la instalación y uso de la fuente en web y Python, las dependencias de formato, los tipos de glifos, la verificación visual y la licencia. También ofrece un ejemplo HTML con CSS y configuración para Matplotlib.

## 3. ¿Cómo se relaciona con el resto del sistema?
No contiene imports ni clases ejecutables. Se vincula con:
- `fonts/`: archivos TTF y WOFF2.
- `css/ler-universal.css`: estilos web.
- `examples/test-glifos.html`: comprobación de glifos.
- `LICENSE.txt` y la fuente base Noto Sans Symbols 2.

Matplotlib es la única dependencia externa-mentioned explícitamente.

## 4. ¿Es esencial o prescindible?
**Prescindible para el funcionamiento**, porque solo documenta el paquete. Sin embargo, es **recomendable para instalación, uso, mantenimiento y verificación** de la tipografía.