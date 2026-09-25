# core/mathema/ast.py

class Nodo:
    """Nodo base del AST simbólico para representar estados y operaciones cognitivas"""
    def accept(self, visitor):
        raise NotImplementedError
    
    def __str__(self):
        """Representación textual para debugging cognitivo"""
        return f"{self.__class__.__name__}({self.__dict__})"

class Estado(Nodo):
    """Un estado cognitivo fundamental representado por un glifo"""
    def __init__(self, glifo, codigo=None, nombre=None, fila=None, columna=None, 
                 intensidad=None, duracion=None, contexto=None):
        self.glifo = glifo              # Símbolo visual del estado
        self.codigo = codigo            # Código interno (ej: 'GLA', 'GLB')
        self.nombre = nombre            # Nombre semántico ('Origen', 'Dualidad')
        self.fila = fila                # Posición para debugging
        self.columna = columna
        
        # Propiedades cognitivas específicas
        self.intensidad = intensidad    # Intensidad del estado (0.0-1.0)
        self.duracion = duracion        # Duración temporal del estado
        self.contexto = contexto        # Contexto cognitivo asociado
    
    def accept(self, visitor):
        return visitor.visit_estado(self)
    
    def es_meta_cognitivo(self):
        """Verifica si es un estado de meta-cognición"""
        return self.codigo and self.codigo.startswith('REFLEXIVO')
    
    def es_sistema(self):
        """Verifica si es un estado del sistema"""
        return self.codigo and self.codigo.startswith('SIS_')
    
    def es_interactivo(self):
        """Verifica si es un estado de interacción"""
        return self.codigo and self.codigo.startswith('INT_')

class Modificador(Nodo):
    """Aplica modificación de profundidad cognitiva (meta-nivel vs sub-nivel)"""
    def __init__(self, tipo, nivel, contenido, fila=None, columna=None, 
                 recursividad=None, persistencia=None):
        self.tipo = tipo                # 'SUP' (meta) o 'SUB' (sub-consciente)
        self.nivel = nivel              # Nivel de profundidad (puede ser numérico o simbólico)
        self.contenido = contenido      # Estado o expresión modificada
        self.fila = fila
        self.columna = columna
        
        # Propiedades cognitivas del modificador
        self.recursividad = recursividad  # ¿Aplica recursivamente?
        self.persistencia = persistencia  # ¿El cambio de nivel persiste?
    
    def accept(self, visitor):
        return visitor.visit_modificador(self)
    
    def es_meta_nivel(self):
        """Verifica si eleva a meta-nivel (pensar sobre pensar)"""
        return self.tipo == 'SUP'
    
    def es_sub_nivel(self):
        """Verifica si baja a sub-nivel (procesos automáticos)"""
        return self.tipo == 'SUB'

class OperacionBinaria(Nodo):
    """Combina dos estados cognitivos mediante una operación mental"""
    def __init__(self, op, izq, der, fila=None, columna=None, 
                 resultado_emergente=None, estabilidad=None):
        self.op = op                    # Tipo de operación cognitiva
        self.izq = izq                  # Estado cognitivo izquierdo
        self.der = der                  # Estado cognitivo derecho
        self.fila = fila
        self.columna = columna
        
        # Propiedades del resultado cognitivo
        self.resultado_emergente = resultado_emergente  # ¿Produce emergencia?
        self.estabilidad = estabilidad  # Estabilidad del estado resultante
    
    def accept(self, visitor):
        return visitor.visit_operacion_binaria(self)
    
    def es_fusion(self):
        """Fusión armónica de estados"""
        return self.op == '⊕'
    
    def es_colision(self):
        """Conflicto/tensión entre estados"""
        return self.op == '⊗'
    
    def es_intercambio(self):
        """Intercambio bidireccional"""
        return self.op == '⇆'
    
    def tipo_cognitivo(self):
        """Retorna el tipo de operación cognitiva"""
        operaciones = {
            '⊕': 'fusion_armorica',
            '⊗': 'tension_cognitiva', 
            '⇆': 'intercambio_bidireccional',
            '⇈': 'amplificacion',
            '⇊': 'atenuacion'
        }
        return operaciones.get(self.op, 'operacion_desconocida')

class Flujo(Nodo):
    """Representa flujos y transiciones en el procesamiento cognitivo"""
    def __init__(self, tipo, origen, destino, temporal=None, fila=None, columna=None,
                 velocidad=None, probabilidad=None, condiciones=None):
        self.tipo = tipo                # 'RESULT', 'FLOW', 'CYCLE', 'LOOP'
        self.origen = origen            # Estado origen
        self.destino = destino          # Estado destino (puede ser None en loops)
        self.temporal = temporal        # Información temporal
        self.fila = fila
        self.columna = columna
        
        # Propiedades del flujo cognitivo
        self.velocidad = velocidad      # Velocidad de transición
        self.probabilidad = probabilidad # Probabilidad de ocurrencia
        self.condiciones = condiciones  # Condiciones para la transición
    
    def accept(self, visitor):
        return visitor.visit_flujo(self)
    
    def es_resultado(self):
        """Transición que produce un resultado definitivo"""
        return self.tipo == 'RESULT'
    
    def es_flujo_continuo(self):
        """Flujo continuo de consciencia"""
        return self.tipo == 'FLOW'
    
    def es_retroalimentacion(self):
        """Bucle de retroalimentación"""
        return self.tipo == 'LOOP'
    
    def es_ciclico(self):
        """Procesamiento cíclico"""
        return self.tipo == 'CYCLE'

class Bloque(Nodo):
    """Agrupamiento con semántica de mutabilidad cognitiva"""
    def __init__(self, contenido, tipo, fila=None, columna=None,
                 aislamiento=None, permeabilidad=None, persistencia=None):
        self.contenido = contenido      # Estados/expresiones contenidas
        self.tipo = tipo                # 'BLK' (rígido) o 'DYN' (adaptable)
        self.fila = fila
        self.columna = columna
        
        # Propiedades cognitivas del contenedor
        self.aislamiento = aislamiento  # Nivel de aislamiento cognitivo
        self.permeabilidad = permeabilidad  # ¿Permite influencia externa?
        self.persistencia = persistencia    # ¿Persiste en memoria?
    
    def accept(self, visitor):
        return visitor.visit_bloque(self)
    
    def es_rigido(self):
        """Bloque rígido - memoria fija, no adaptable"""
        return self.tipo == 'BLK'
    
    def es_dinamico(self):
        """Bloque dinámico - memoria adaptable"""
        return self.tipo == 'DYN'
    
    def nivel_mutabilidad(self):
        """Retorna nivel de mutabilidad del bloque"""
        if self.es_rigido():
            return 'inmutable'
        elif self.es_dinamico():
            return 'adaptable'
        else:
            return 'desconocido'

class Control(Nodo):
    """Operadores de control y seguridad cognitiva"""
    def __init__(self, comando, objetivo=None, fila=None, columna=None,
                 urgencia=None, alcance=None, reversible=None):
        self.comando = comando          # Tipo de control ('HALT', 'PURGE', 'KILL', etc.)
        self.objetivo = objetivo        # Estado/proceso objetivo (opcional)
        self.fila = fila
        self.columna = columna
        
        # Propiedades del control cognitivo
        self.urgencia = urgencia        # Nivel de urgencia (0-10)
        self.alcance = alcance          # Alcance del control ('local', 'global', 'sistema')
        self.reversible = reversible    # ¿Es reversible el control?
    
    def accept(self, visitor):
        return visitor.visit_control(self)
    
    def es_destructivo(self):
        """Verifica si el comando es destructivo/irreversible"""
        destructivos = ['KILL', 'PURGE']
        return self.comando in destructivos
    
    def es_seguridad(self):
        """Verifica si es un comando de seguridad"""
        seguridad = ['HALT', 'ISOLATE', 'AUDIT']
        return self.comando in seguridad
    
    def nivel_peligrosidad(self):
        """Retorna nivel de peligrosidad del comando"""
        niveles = {
            'AUDIT': 1,      # Solo inspección
            'HALT': 3,       # Pausa temporal
            'ISOLATE': 5,    # Aislamiento
            'PURGE': 8,      # Limpieza destructiva
            'KILL': 10       # Terminación definitiva
        }
        return niveles.get(self.comando, 0)

# === NODOS ESPECIALIZADOS PARA COGNICIÓN AVANZADA ===

class EstadoComposite(Nodo):
    """Estado cognitivo compuesto por múltiples sub-estados"""
    def __init__(self, sub_estados, patron=None, coherencia=None, fila=None, columna=None):
        self.sub_estados = sub_estados  # Lista de estados componentes
        self.patron = patron            # Patrón de combinación
        self.coherencia = coherencia    # Nivel de coherencia interna
        self.fila = fila
        self.columna = columna
    
    def accept(self, visitor):
        return visitor.visit_estado_composite(self)

class ContextoCognitivo(Nodo):
    """Representa el contexto cognitivo que influye en las operaciones"""
    def __init__(self, factores, peso=None, duracion=None, fila=None, columna=None):
        self.factores = factores        # Factores contextuales
        self.peso = peso                # Peso/influencia del contexto
        self.duracion = duracion        # Duración temporal del contexto
        self.fila = fila
        self.columna = columna
    
    def accept(self, visitor):
        return visitor.visit_contexto(self)

class Emergencia(Nodo):
    """Estado de emergencia cognitiva que requiere atención inmediata"""
    def __init__(self, estado_base, nivel_urgencia, respuesta_requerida=None, 
                 fila=None, columna=None):
        self.estado_base = estado_base          # Estado que causó la emergencia
        self.nivel_urgencia = nivel_urgencia    # Nivel de urgencia (1-10)
        self.respuesta_requerida = respuesta_requerida  # Respuesta necesaria
        self.fila = fila
        self.columna = columna
    
    def accept(self, visitor):
        return visitor.visit_emergencia(self)
    
    def es_critica(self):
        """Verifica si la emergencia es crítica"""
        return self.nivel_urgencia >= 8

# === UTILIDADES PARA ANÁLISIS COGNITIVO ===

def analizar_complejidad_cognitiva(nodo):
    """Analiza la complejidad cognitiva de una expresión AST"""
    if isinstance(nodo, Estado):
        return 1 + (1 if nodo.es_meta_cognitivo() else 0)
    elif isinstance(nodo, OperacionBinaria):
        return 2 + analizar_complejidad_cognitiva(nodo.izq) + analizar_complejidad_cognitiva(nodo.der)
    elif isinstance(nodo, Modificador):
        return 1 + analizar_complejidad_cognitiva(nodo.contenido) + (1 if nodo.es_meta_nivel() else 0)
    elif isinstance(nodo, Flujo):
        comp = 1 + analizar_complejidad_cognitiva(nodo.origen)
        if nodo.destino:
            comp += analizar_complejidad_cognitiva(nodo.destino)
        return comp
    elif isinstance(nodo, Bloque):
        return 1 + analizar_complejidad_cognitiva(nodo.contenido)
    elif isinstance(nodo, Control):
        return nodo.nivel_peligrosidad()
    else:
        return 0

def extraer_estados_cognitivos(nodo, estados=None):
    """Extrae todos los estados cognitivos de una expresión AST"""
    if estados is None:
        estados = []
    
    if isinstance(nodo, Estado):
        estados.append(nodo)
    elif hasattr(nodo, 'izq') and hasattr(nodo, 'der'):
        extraer_estados_cognitivos(nodo.izq, estados)
        extraer_estados_cognitivos(nodo.der, estados)
    elif hasattr(nodo, 'contenido'):
        extraer_estados_cognitivos(nodo.contenido, estados)
    elif hasattr(nodo, 'origen'):
        extraer_estados_cognitivos(nodo.origen, estados)
        if hasattr(nodo, 'destino') and nodo.destino:
            extraer_estados_cognitivos(nodo.destino, estados)
    
    return estados

def detectar_riesgos_cognitivos(nodo):
    """Detecta posibles riesgos en la estructura cognitiva"""
    riesgos = []
    
    if isinstance(nodo, Control) and nodo.es_destructivo():
        riesgos.append(f"Control destructivo: {nodo.comando}")
    
    if isinstance(nodo, Flujo) and nodo.tipo == 'LOOP' and not nodo.destino:
        riesgos.append("Bucle potencialmente infinito detectado")
    
    if isinstance(nodo, Modificador) and nodo.es_meta_nivel() and nodo.nivel and nodo.nivel > 5:
        riesgos.append("Meta-nivel excesivamente profundo")
    
    # Recursivamente verificar sub-nodos
    for attr_name in ['izq', 'der', 'contenido', 'origen', 'destino']:
        if hasattr(nodo, attr_name):
            sub_nodo = getattr(nodo, attr_name)
            if sub_nodo:
                riesgos.extend(detectar_riesgos_cognitivos(sub_nodo))
    
    return riesgos