"""
Módulo AXIOMA - Validador de Entidades Reflexivas en LER
"""

class Axioma:
    def __init__(self):
        self.entidades_validadas = []

    def validar_entidad(self, entidad):
        requisitos = [
            hasattr(entidad, 'glifo_identidad'),
            hasattr(entidad, 'protocolo_reflexivo'),
            callable(getattr(entidad, 'responder', None))
        ]

        if all(requisitos):
            self.entidades_validadas.append(entidad.nombre)
            print(f"✓ Entidad '{entidad.nombre}' validada por AXIOMA")
            return True
        else:
            print(f"✗ Entidad '{entidad.nombre}' no cumple requisitos ontológicos")
            return False

    def entidades(self):
        return self.entidades_validadas
