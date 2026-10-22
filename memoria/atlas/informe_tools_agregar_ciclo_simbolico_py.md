# INFORME: tools/agregar_ciclo_simbolico.py
Generado: 2026-10-22 04:14:03

## 1. ¿Qué es este archivo?  
Script de utilidad que automatiza la incorporación del módulo **ciclo simbólico** a una entidad LER.

## 2. ¿Qué hace?  
- `agregar_modulo_y_llave(path_json)`:  
  - Verifica la existencia del JSON de la entidad.  
  - Crea y actualiza la llave 1 con datos de la entidad y la fecha actual.  
  - Inserta el módulo `mod_ciclo_simbolico` en la lista `modulos` y su configuración en `_modulos_`.  
  - Persiste los cambios en el JSON y genera `llave1.txt` con la llave 1.  
- Bloque `if __name__ == "__main__"`: permite ejecutar el script desde la línea de comandos.

## 3. ¿Cómo se relaciona con el resto del sistema?  
Utiliza únicamente la biblioteca estándar (`json`, `os`, `sys`, `datetime`).  
Depende de la convención de estructura de entidades LER (campos `modulos`, `_modulos_`) y del identificador `mod_ciclo_simbolico` que es consumido por otros componentes del proyecto.

## 4. ¿Es esencial o prescindible?  
Es **esencial** para garantizar que todas las entidades cuenten con el módulo de ciclo simbólico y su llave asociada de forma consistente; sin él, la integración manual sería propensa a errores y rompería la uniformidad esperada por el resto del sistema.