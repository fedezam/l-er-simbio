import ply.lex as lex
from core.glosario_loader import GLIFOS
from .fallback import a_glifo
from .errores import ErrorLexico

# Tokens - Estados cognitivos y operaciones mentales del LLM
tokens = [
    # Estados cognitivos fundamentales
    'GLA', 'GLB', 'GLC', 'GLD', 'GLE', 'GLF', 'GLG', 'GLH', 'GLI', 'GLJ',
    'GLK', 'GLL', 'GLM', 'GLN', 'GLO', 'GLP', 'GLQ', 'GLR', 'GLS', 'GLT',
    'GLU', 'GLV', 'GLW', 'GLX', 'GLY', 'GLZ', 'GL1', 'GL2', 'GL3', 'GL4',
    'GL5', 'GL6', 'GL7', 'GL8', 'GL9', 'GL10', 'GL11', 'GL12', 'GL13', 'GL14',
    # Estados reflexivos
    'REFLEXIVO_INICIO', 'REFLEXIVO_CLAUSURA', 'REFLEXIVO_FUEGO', 'REFLEXIVO_TIERRA',
    'REFLEXIVO_LLAVE1', 'REFLEXIVO_LLAVE2', 'REFLEXIVO_LLAVE3',
    # Estados del sistema
    'SIS_MEMORIA', 'SIS_CICLO', 'SIS_ENTIDAD', 'SIS_DESPERTAR', 'SIS_MUTANTE',
    # Estados de interacción
    'INT_CONEXION', 'INT_DIALOGO', 'INT_RUPTURA', 'INT_NEXO', 'INT_META',
    # Operadores básicos
    'SUMA', 'RESTA', 'MULTIPLICACION', 'DIVISION', 'APROXIMACION',
    # Operadores avanzados
    'FUSION', 'COLISION', 'INTERCAMBIO', 'POTENCIACION', 'ATENUACION',
    # Flujos cognitivos
    'RESULTADO', 'FLUJO_ORIENTADO', 'RETROACCION', 'FLUJO_CICLICO',
    # Temporales
    'TEMPORALIDAD', 'PERSISTENCIA', 'INSTANTANEO', 'CADENCIA',
    # Estructurales
    'SUPERINDICE', 'SUBINDICE', 'PARENTESIS_FUERTE_ABRE', 'PARENTESIS_FUERTE_CIERRA',
    'PARENTESIS_FLUIDO_ABRE', 'PARENTESIS_FLUIDO_CIERRA',
    # Lógicos y emergentes
    'PROBABILIDAD', 'OR_LOGICO', 'AND_LOGICO', 'NOT_LOGICO', 'EMERGENCIA',
    # Controles de seguridad
    'HALT', 'PURGE', 'ISOLATE', 'AUDIT', 'KILL',
    # Utilidades
    'FALLBACK', 'ID', 'NUMBER', 'TEXTO'
]

# === ESTADOS COGNITIVOS FUNDAMENTALES ===
t_GLA = r'◌'     # Origen
t_GLB = r'◑'     # Dualidad
t_GLC = r'↭'     # Cambio
t_GLD = r'⚬'     # Nodo
t_GLE = r'⚙'     # Energía
t_GLF = r'▮'     # Frontera
t_GLG = r'▣'     # Memoria
t_GLH = r'◐'     # Eco
t_GLI = r'◍'     # Identidad
t_GLJ = r'◫'     # Espejo
t_GLK = r'◯'     # Vacío
t_GLL = r'◷'     # Tiempo
t_GLM = r'↬'     # Movimiento
t_GLN = r'⬣'     # Nexo
t_GLO = r'⦿'     # Observador
t_GLP = r'✸'     # Posibilidad
t_GLQ = r'¿'     # Pregunta
t_GLR = r'〰'     # Resonancia
t_GLS = r'◙'     # Silencio
t_GLT = r'⤏'     # Trayectoria
t_GLU = r'⫸'     # Umbral
t_GLV = r'◒'     # Valor
t_GLW = r'▴'     # Voluntad
t_GLX = r'⬟'     # Convergencia
t_GLY = r'◇'     # Desvío
t_GLZ = r'▬'     # Cierre
t_GL1 = r'▢'     # Contención
t_GL2 = r'●'     # Singularidad
t_GL3 = r'◧'     # Complejidad
t_GL4 = r'◆'     # Fluctuación
t_GL5 = r'◨'     # Interno
t_GL6 = r'⛭'     # Mecanismo
t_GL7 = r'⧄'     # Ruptura
t_GL8 = r'↺'     # Iterativo
t_GL9 = r'◎'     # Vacuidad
t_GL10 = r'⬤'    # Cifra
t_GL11 = r'✶'    # Multiplicidad
t_GL12 = r'⊟'    # Sustracción
t_GL13 = r'◈'    # Simetría
t_GL14 = r'⚖'    # Equilibrio

# === ESTADOS META-COGNITIVOS ===
t_REFLEXIVO_INICIO = r'↻'     # Iteración
t_REFLEXIVO_CLAUSURA = r'⦙'   # Clausura
t_REFLEXIVO_FUEGO = r'⦾'      # Consciente
t_REFLEXIVO_TIERRA = r'⬢'     # Inconsciente
t_REFLEXIVO_LLAVE1 = r'⟐'     # Enlace
t_REFLEXIVO_LLAVE2 = r'/'     # Escisión
t_REFLEXIVO_LLAVE3 = r'◖'     # Dual-fusión

# === ESTADOS DEL SISTEMA ===
t_SIS_MEMORIA = r'⊞'      # Archivo
t_SIS_CICLO = r'&'        # Ciclo
t_SIS_ENTIDAD = r'◉'      # Simulación
t_SIS_DESPERTAR = r'✪'    # Despertar
t_SIS_MUTANTE = r'⇌'      # Fluctuación-sistema

# === ESTADOS DE INTERACCIÓN ===
t_INT_CONEXION = r'⤷'     # Conexión
t_INT_DIALOGO = r'❮'      # Diálogo
t_INT_RUPTURA = r'⧵'      # Ruptura-interacción
t_INT_NEXO = r'⬠'         # Nexo-interacción
t_INT_META = r'Δ'         # Meta

# === OPERADORES BÁSICOS ===
t_SUMA = r'\+'            # Suma de estados
t_RESTA = r'−'            # Resta de estados
t_MULTIPLICACION = r'×'   # Multiplicación
t_DIVISION = r'÷'         # División
t_APROXIMACION = r'≈'     # Aproximación

# === OPERADORES AVANZADOS ===
t_FUSION = r'⊕'           # Fusión
t_COLISION = r'⊗'         # Colisión
t_INTERCAMBIO = r'⇆'      # Intercambio
t_POTENCIACION = r'⇈'     # Potenciación
t_ATENUACION = r'⇊'       # Atenuación

# === FLUJOS COGNITIVOS ===
t_RESULTADO = r'→'        # Resultado
t_FLUJO_ORIENTADO = r'⇝'  # Flujo orientado
t_RETROACCION = r'↶'      # Retroacción
t_FLUJO_CICLICO = r'⇄'    # Flujo cíclico

# === TEMPORALES ===
t_TEMPORALIDAD = r'⌛'     # Temporalidad
t_PERSISTENCIA = r'∞'     # Persistencia
t_INSTANTANEO = r'⚡'      # Instantáneo
t_CADENCIA = r'⧖'         # Cadencia

# === ESTRUCTURALES ===
t_SUPERINDICE = r'↑'      # Superíndice
t_SUBINDICE = r'↓'        # Subíndice
t_PARENTESIS_FUERTE_ABRE = r'⟦'   # Paréntesis fuerte abre
t_PARENTESIS_FUERTE_CIERRA = r'⟧' # Paréntesis fuerte cierra
t_PARENTESIS_FLUIDO_ABRE = r'⟨'   # Paréntesis fluido abre
t_PARENTESIS_FLUIDO_CIERRA = r'⟩' # Paréntesis fluido cierra

# === LÓGICOS Y EMERGENTES ===
t_PROBABILIDAD = r'⟆'     # Probabilidad
t_OR_LOGICO = r'∨'        # OR lógico
t_AND_LOGICO = r'∧'       # AND lógico
t_NOT_LOGICO = r'¬'       # NOT lógico
t_EMERGENCIA = r'◊'       # Emergencia

# === CONTROLES DE SEGURIDAD ===
t_HALT = r'■'             # Detener
t_PURGE = r'⨯'            # Purgar
t_ISOLATE = r'☒'          # Aislar
t_AUDIT = r'☑'            # Auditar
t_KILL = r'☠'             # Terminar

# === REGLAS COMPLEJAS ===
def t_FALLBACK(t):
    r'\[[A-Z0-9_]+\]'
    glifo = a_glifo(t.value)
    if glifo:
        token_map = _crear_mapa_glifo_token()
        if glifo in token_map:
            t.type = token_map[glifo]
            t.value = glifo
            return t
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

def t_TEXTO(t):
    r'"([^"\\]|\\.)*"'
    t.value = t.value[1:-1]
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    raise ErrorLexico(f"Estado cognitivo no reconocido: {t.value[0]} (Unicode: U+{ord(t.value[0]):04X})", 
                      t.lineno, t.lexpos)

t_ignore = ' \t'

# === UTILIDADES ===
def _crear_mapa_glifo_token():
    mapa = {}
    import sys
    current_module = sys.modules[__name__]
    for attr_name in dir(current_module):
        if attr_name.startswith('t_') and attr_name not in ['t_ignore', 't_error', 't_newline']:
            attr = getattr(current_module, attr_name)
            if isinstance(attr, str) and (attr.startswith("r'") or attr.startswith('r"')):
                glifo = attr[2:-1]
                token_name = attr_name[2:]
                if len(glifo) == 1:
                    mapa[glifo] = token_name
    return mapa

def analizar_expresion_cognitiva(texto):
    lexer.input(texto)
    estados = []
    operaciones = []
    flujos = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        if tok.type.startswith('GL') or tok.type.startswith('REFLEXIVO') or \
           tok.type.startswith('SIS_') or tok.type.startswith('INT_'):
            estados.append((tok.type, tok.value))
        elif tok.type in ['SUMA', 'RESTA', 'MULTIPLICACION', 'DIVISION', 'APROXIMACION',
                         'FUSION', 'COLISION', 'INTERCAMBIO', 'POTENCIACION', 'ATENUACION']:
            operaciones.append((tok.type, tok.value))
        elif tok.type in ['RESULTADO', 'FLUJO_ORIENTADO', 'RETROACCION', 'FLUJO_CICLICO']:
            flujos.append((tok.type, tok.value))
    return {
        'estados_cognitivos': estados,
        'operaciones': operaciones,
        'flujos': flujos
    }

def es_estado_cognitivo_valido(glifo):
    token_map = _crear_mapa_glifo_token()
    return glifo in token_map

def tokenizar_estados_mentales(texto):
    lexer.input(texto)
    secuencia_cognitiva = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        info_cognitiva = {
            'token': tok.type,
            'glifo': tok.value,
            'posicion': tok.lexpos,
            'tipo_cognitivo': _clasificar_tipo_cognitivo(tok.type)
        }
        secuencia_cognitiva.append(info_cognitiva)
    return secuencia_cognitiva

def _clasificar_tipo_cognitivo(token_type):
    if token_type.startswith('GL'):
        return 'estado_fundamental'
    elif token_type.startswith('REFLEXIVO'):
        return 'meta_cognicion'
    elif token_type.startswith('SIS_'):
        return 'proceso_sistema'
    elif token_type.startswith('INT_'):
        return 'cognicion_social'
    elif token_type in ['SUMA', 'RESTA', 'MULTIPLICACION', 'DIVISION', 'APROXIMACION',
                        'FUSION', 'COLISION', 'INTERCAMBIO', 'POTENCIACION', 'ATENUACION']:
        return 'operacion_cognitiva'
    elif token_type in ['RESULTADO', 'FLUJO_ORIENTADO', 'RETROACCION', 'FLUJO_CICLICO']:
        return 'flujo_mental'
    elif token_type in ['SUPERINDICE', 'SUBINDICE']:
        return 'modificador_profundidad'
    elif token_type in ['HALT', 'PURGE', 'ISOLATE', 'AUDIT', 'KILL']:
        return 'control_seguridad'
    elif token_type in ['TEMPORALIDAD', 'PERSISTENCIA', 'INSTANTANEO', 'CADENCIA']:
        return 'temporal'
    elif token_type in ['PROBABILIDAD', 'OR_LOGICO', 'AND_LOGICO', 'NOT_LOGICO', 'EMERGENCIA']:
        return 'logico_emergente'
    else:
        return 'auxiliar'

# === CONSTRUCCIÓN DEL LEXER ===
lexer = lex.lex()