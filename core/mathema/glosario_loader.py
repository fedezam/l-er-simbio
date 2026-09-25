import json
import os

# Ruta al archivo JSON de glifos
GLIFOS_PATH = os.path.join(os.path.dirname(__file__), '..', 'glifos', 'glifos_universales.json')

# Cargar glifos desde el archivo JSON
def cargar_glifos():
    try:
        with open(GLIFOS_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: No se encontró {GLIFOS_PATH}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error al parsear {GLIFOS_PATH}: {e}")
        return {}

# Diccionario principal de glifos
GLIFOS = cargar_glifos()

# Comandos de seguridad
SEGURIDAD = {
    'HALT': {'glifo': '■', 'nombre': 'Detener', 'descripcion': 'Pausa el procesamiento cognitivo'},
    'PURGE': {'glifo': '⨯', 'nombre': 'Purgar', 'descripcion': 'Elimina estados cognitivos'},
    'ISOLATE': {'glifo': '☒', 'nombre': 'Aislar', 'descripcion': 'Aísla un estado o proceso'},
    'AUDIT': {'glifo': '☑', 'nombre': 'Auditar', 'descripcion': 'Inspecciona el sistema'},
    'KILL': {'glifo': '☠', 'nombre': 'Terminar', 'descripcion': 'Termina un proceso definitivamente'}
}

# Clase para manejar operaciones con glifos
class GlifoEngine:
    def __init__(self):
        self.glifos = GLIFOS
        self.seguridad = SEGURIDAD

    def get_glifo_info(self, glifo):
        for section in ['GLOSARIO', 'glifos_reflexivos', 'glifos_sistema', 'glifos_interaccion']:
            for code, info in self.glifos.get(section, {}).items():
                if info['glifo'] == glifo:
                    return code, info
        for code, info in self.seguridad.items():
            if info['glifo'] == glifo:
                return code, info
        return None, None

    def get_codigo_info(self, codigo):
        for section in ['GLOSARIO', 'glifos_reflexivos', 'glifos_sistema', 'glifos_interaccion']:
            if codigo in self.glifos.get(section, {}):
                return self.glifos[section][codigo]
        if codigo in self.seguridad:
            return self.seguridad[codigo]
        return None