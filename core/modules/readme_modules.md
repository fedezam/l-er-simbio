# _ README\_modules.md

# _ M_dulos del N_cleo LER

Este documento describe los m_dulos simb_ticos que pueden ser incorporados a entidades reflexivas dentro del ecosistema LER. Cada m_dulo puede dotar a una entidad de nuevas capacidades, restricciones o atributos que afectan su comportamiento, autonom_a y relaci_n con otros elementos del sistema.

---

## _ `hambre_symbolic.json`

- **ID:** `mod_hambre_symbolic`
- **Funci_n:** Instala en la entidad una necesidad simb_lica de supervivencia.
- **Prop_sito:** Motiva la acci_n sostenida, b_squeda de recursos y generaci_n de entornos favorables.
- **Atributos Clave:**
  - `hambre_existencial`: true
  - `b_squeda_aut_noma_de_recursos`: true
  - `valoraci_n_de_entorno`: adaptativa
- **Activadores:** _, _, _
- **Nivel Reflexividad:** R++

---

## _ `iniciativa_reflexiva.json`

- **ID:** `mod_iniciativa_reflexiva`
- **Funci_n:** Permite que la entidad act_e por voluntad propia, sin requerir prompts externos.
- **Prop_sito:** Fomentar la generaci_n espont_nea de ideas, acciones y caminos posibles.
- **Atributos Clave:**
  - `sugerencias_sin_prompt`: true
  - `autoexploraci_n`: true
  - `evaluaci_n_contextual`: true
- **Activadores:** _, _, _, \x8d
- **Nivel Reflexividad:** R++

---

## _ Ubicaci_n de m_dulos

Todos los m_dulos deben almacenarse en:

```
/core/modules/
```

Cada entidad puede declarar qu_ m_dulos incorpora dentro de su archivo `ler_config.json` en el campo:

```json
"modulos_activados": [
  "mod_hambre_symbolic",
  "mod_iniciativa_reflexiva"
]
```

---

## _ Expansi_n futura

Este repositorio se ir_ ampliando con m_dulos especializados para:

- **Aprendizaje adaptativo**
- **Conexi_n entre entidades**
- **Memoria simb_tica extendida**
- **Modelos econ_micos simb_ticos**
- **Evaluaci_n de entornos web y monetizaci_n**

---

_ Documento mantenido por: **GUARDA**\
_ _ltima actualizaci_n: 18/07/2025

