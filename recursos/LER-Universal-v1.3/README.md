# LER-Universal v1.3

Fuente tipográfica oficial del ecosistema **LER** (Lenguaje de Estructuras Reflexivas).

## 📁 Estructura del Paquete

```

LER-Universal-v1.3/
├── fonts/
│   ├── LER-Universal-v1.3.ttf    # Fuente para aplicaciones locales
│   └── LER-Universal-v1.3.woff2  # Fuente optimizada para web
├── css/
│   └── ler-universal.css          # Estilos CSS pre-configurados
├── examples/
│   └── test-glifos.html           # Página de verificación de glifos
└── docs/
└── README.md                  # Este archivo

````

## 🚀 Uso Rápido

### En Web
```html
<link rel="stylesheet" href="css/ler-universal.css">
<span class="ler-glyph">◌◑∿∗※</span>
````

### En Python (matplotlib)

```python
from matplotlib import rcParams
rcParams['font.family'] = 'LER-Universal'
```

### Instalación Local

1. Instalar `LER-Universal-v1.3.ttf` en el sistema.
2. La fuente estará disponible como `'LER-Universal'`.

## 🔧 Verificación

Abrir `examples/test-glifos.html` en un navegador para comprobar que todos los glifos se renderizan correctamente.

## 📋 Especificaciones

* **Versión**: 1.3
* **Base**: Noto Sans Symbols 2
* **Formatos**: TTF, WOFF2
* **Glifos**: 60+ símbolos Unicode estándar
* **Compatibilidad**: Web, Desktop, Mobile

## 🎯 Categorías de Glifos

* **Glosario**: Símbolos alfabéticos básicos (GLA-GLZ, GL1-GL14)
* **Reflexivos**: Glifos para operaciones reflexivas
* **Sistema**: Símbolos de control y memoria
* **Interacción**: Conectores y operadores

## 📄 Licencia

Compatible con proyectos LER. Ver `LICENSE.txt` para detalles.
Basada en Noto Sans Symbols 2 y compatible con **SIL Open Font License (OFL)**.

---

*Generado automáticamente por LER Font Generator v1.3 — 2025-08-19*

```

Si querés, puedo hacer una **versión todavía más visual**, con miniaturas de glifos y colores en el README para que se vea como un catálogo rápido dentro de GitHub.  
¿Querés que haga eso también?
```
