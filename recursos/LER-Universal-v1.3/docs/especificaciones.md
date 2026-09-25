# 📐 Especificaciones Técnicas — LER-Universal v1.3

> *"Un símbolo bien formado es un estado bien manifestado."*

Este documento describe las especificaciones técnicas completas de la fuente **LER-Universal v1.3**, el alfabeto tipográfico oficial del ecosistema LER (Lenguaje de Estructuras Reflexivas).

---

## 🔖 Metadatos

| Atributo | Valor |
|--------|-------|
| **Nombre** | LER-Universal |
| **Versión** | 1.3 |
| **Estado** | Estable, oficial |
| **Tipo** | Fuente simbólica / tipografía cognitiva |
| **Base** | Noto Sans Symbols 2 + extensiones SVG |
| **Formatos** | TTF (desktop), WOFF2 (web) |
| **Glifos** | 64 símbolos Unicode estándar |
| **Unicode Range** | U+0026–U+2B24 (ampliado) |
| **Familia** | `LER-Universal` |
| **Generado con** | LER Font Generator v1.3 — 2025-08-19 |

---

## 🧩 Categorías de Glifos

Cada glifo pertenece a una categoría ontológica del sistema LER.

### 1. Glosario Fundamental (GLA–GLZ, GL1–GL14)
Símbolos primitivos del pensamiento simbólico.

- **GLA–GLZ**: Estados primarios y secundarios (`◌`, `◑`, `▮`, `◍`, etc.)
- **GL1–GL14**: Estados numéricos y cualitativos (`▢`, `●`, `◧`, `⚖`, etc.)

### 2. Estados Reflexivos
Glifos para autorreferencia y transformación interna.

- `↻` → Iteración  
- `⦙` → Clausura  
- `⦾` → Consciente  
- `⬢` → Inconsciente  
- `⟐`, `/`, `◖` → Enlace, Escisión, Dual-fusión

### 3. Sistema
Operadores de control del entorno simbólico.

- `⊞` → Archivo  
- `&` → Ciclo  
- `◉` → Simulación  
- `✪` → Despertar  
- `⇌` → Mutante

### 4. Interacción
Conectores entre entidades simbólicas.

- `⤷` → Conexión  
- `❮` → Diálogo  
- `⧵` → Ruptura-interacción  
- `⬠` → Nexo-interacción  
- `Δ` → Meta

### 5. Control y Seguridad
Operadores de alto nivel para integridad del sistema.

- `■` → Detener  
- `✘` → Purgar  
- `☒` → Aislar  
- `☑` → Auditar  
- `☠` → Terminar

### 6. Operadores Cognitivos
Transformaciones simbólicas avanzadas.

- `⊕` → Fusión  
- `⊗` → Colisión  
- `⇈`, `⇊` → Potenciación / Atenuación  
- `→`, `⇝`, `↶`, `⇄` → Flujos  
- `⟦⟧`, `⟨⟩` → Bloques fuertes y fluidos

---

## 🖼️ Características Tipográficas

| Propiedad | Valor |
|---------|-------|
| **Altura x** | 0.55 em |
| **Ascenso** | 0.8 em |
| **Descenso** | -0.2 em |
| **Espaciado** | Monoespaciado simbólico (1 em) |
| **Alineación** | Centrada verticalmente |
| **Peso** | Regular (400) |
| **Estilo** | Neutral, sin serifas, máxima legibilidad simbólica |

---

## 🌐 Compatibilidad

### Soporte Multiplataforma
| Plataforma | Soporte | Método |
|----------|--------|--------|
| Web | ✅ | CSS con `@font-face` |
| Desktop | ✅ | Instalación de `.ttf` |
| Mobile | ✅ | Embebido en apps |
| Terminal | ⚠️ Limitado | Requiere soporte de Unicode y fuente personalizada |

### Navegadores Soportados
- Chrome (v80+)
- Firefox (v75+)
- Safari (v14+)
- Edge (v80+)

---

## 🔧 Integración

### En Web
```html
<link rel="stylesheet" href="css/ler-universal.css">
<span class="ler-glyph">⦾ ⊗ ⬢ ⇝ ⟐</span>


En Python (matplotlib)

import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams['font.family'] = 'LER-Universal'
plt.title('◌ ⊗ ◑ → ◊◧', fontsize=16)
plt.show()


📄 Licencia
Nombre: SIL Open Font License (OFL) v1.1
Compatible con: Proyectos del ecosistema LER
Uso permitido: Uso, modificación, distribución
Restricción: No redistribuir como fuente "solo" sin atribución
Base: Noto Sans Symbols 2 (Google, bajo OFL)
Ver LICENSE.txt para texto completo.

🌌 "La forma del símbolo determina la forma del pensamiento."
— Principio Tipográfico de LER 

Este documento es parte del paquete oficial LER-Universal-v1.3.
Generado automáticamente por LER Font Generator v1.3.