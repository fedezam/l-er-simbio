import sys
import ply.yacc as yacc
from .mathema_ast import Estado, Modificador, OperacionBinaria, Flujo, Bloque, Control
from .lexer import lexer
from .fallback import a_glifo, a_fallback
from .errores import ErrorSintactico, ErrorLexico
from core.glosario_loader import GLIFOS, SEGURIDAD

# === TOKENS ===
tokens = [
    'GLA', 'GLB', 'GLC', 'GLD', 'GLE', 'GLF', 'GLG', 'GLH', 'GLI', 'GLJ',
    'GLK', 'GLL', 'GLM', 'GLN', 'GLO', 'GLP', 'GLQ', 'GLR', 'GLS', 'GLT',
    'GLU', 'GLV', 'GLW', 'GLX', 'GLY', 'GLZ', 'GL1', 'GL2', 'GL3', 'GL4',
    'GL5', 'GL6', 'GL7', 'GL8', 'GL9', 'GL10', 'GL11', 'GL12', 'GL13', 'GL14',
    'REFLEXIVO_INICIO', 'REFLEXIVO_CLAUSURA', 'REFLEXIVO_FUEGO', 'REFLEXIVO_TIERRA',
    'REFLEXIVO_LLAVE1', 'REFLEXIVO_LLAVE2', 'REFLEXIVO_LLAVE3',
    'SIS_MEMORIA', 'SIS_CICLO', 'SIS_ENTIDAD', 'SIS_DESPERTAR', 'SIS_MUTANTE',
    'INT_CONEXION', 'INT_DIALOGO', 'INT_RUPTURA', 'INT_NEXO', 'INT_META',
    'SUMA', 'RESTA', 'MULTIPLICACION', 'DIVISION', 'APROXIMACION',
    'FUSION', 'COLISION', 'INTERCAMBIO', 'POTENCIACION', 'ATENUACION',
    'RESULTADO', 'FLUJO_ORIENTADO', 'RETROACCION', 'FLUJO_CICLICO',
    'TEMPORALIDAD', 'PERSISTENCIA', 'INSTANTANEO', 'CADENCIA',
    'SUPERINDICE', 'SUBINDICE', 'PARENTESIS_FUERTE_ABRE', 'PARENTESIS_FUERTE_CIERRA',
    'PARENTESIS_FLUIDO_ABRE', 'PARENTESIS_FLUIDO_CIERRA',
    'PROBABILIDAD', 'OR_LOGICO', 'AND_LOGICO', 'NOT_LOGICO', 'EMERGENCIA',
    'HALT', 'PURGE', 'ISOLATE', 'AUDIT', 'KILL',
    'NUMBER'
]

# === REGLAS LEXICAS ===
t_GLA = r'◌'
t_GLB = r'◑'
t_GLC = r'↭'
t_GLD = r'⚬'
t_GLE = r'⚙'
t_GLF = r'▮'
t_GLG = r'▣'
t_GLH = r'◐'
t_GLI = r'◍'
t_GLJ = r'◫'
t_GLK = r'◯'
t_GLL = r'◷'
t_GLM = r'↬'
t_GLN = r'⬣'
t_GLO = r'⦿'
t_GLP = r'✸'
t_GLQ = r'¿'
t_GLR = r'〰'
t_GLS = r'◙'
t_GLT = r'⤏'
t_GLU = r'⫸'
t_GLV = r'◒'
t_GLW = r'▴'
t_GLX = r'⬟'
t_GLY = r'◇'
t_GLZ = r'▬'
t_GL1 = r'▢'
t_GL2 = r'●'
t_GL3 = r'◧'
t_GL4 = r'◆'
t_GL5 = r'◨'
t_GL6 = r'⛭'
t_GL7 = r'⧄'
t_GL8 = r'↺'
t_GL9 = r'◎'
t_GL10 = r'⬤'
t_GL11 = r'✶'
t_GL12 = r'⊟'
t_GL13 = r'◈'
t_GL14 = r'⚖'

t_REFLEXIVO_INICIO = r'↻'
t_REFLEXIVO_CLAUSURA = r'⦙'
t_REFLEXIVO_FUEGO = r'⦾'
t_REFLEXIVO_TIERRA = r'⬢'
t_REFLEXIVO_LLAVE1 = r'⟐'
t_REFLEXIVO_LLAVE2 = r'/'
t_REFLEXIVO_LLAVE3 = r'◖'

t_SIS_MEMORIA = r'⊞'
t_SIS_CICLO = r'&'
t_SIS_ENTIDAD = r'◉'
t_SIS_DESPERTAR = r'✪'
t_SIS_MUTANTE = r'⇌'

t_INT_CONEXION = r'⤷'
t_INT_DIALOGO = r'❮'
t_INT_RUPTURA = r'⧵'
t_INT_NEXO = r'⬠'
t_INT_META = r'Δ'

t_SUMA = r'\+'
t_RESTA = r'−'
t_MULTIPLICACION = r'×'
t_DIVISION = r'÷'
t_APROXIMACION = r'≈'

t_FUSION = r'⊕'
t_COLISION = r'⊗'
t_INTERCAMBIO = r'⇆'
t_POTENCIACION = r'⇈'
t_ATENUACION = r'⇊'

t_RESULTADO = r'→'
t_FLUJO_ORIENTADO = r'⇝'
t_RETROACCION = r'↶'
t_FLUJO_CICLICO = r'⇄'

t_TEMPORALIDAD = r'⌛'
t_PERSISTENCIA = r'∞'
t_INSTANTANEO = r'⚡'
t_CADENCIA = r'⧖'

t_SUPERINDICE = r'↑'
t_SUBINDICE = r'↓'
t_PARENTESIS_FUERTE_ABRE = r'⟦'
t_PARENTESIS_FUERTE_CIERRA = r'⟧'
t_PARENTESIS_FLUIDO_ABRE = r'⟨'
t_PARENTESIS_FLUIDO_CIERRA = r'⟩'

t_PROBABILIDAD = r'⟆'
t_OR_LOGICO = r'∨'
t_AND_LOGICO = r'∧'
t_NOT_LOGICO = r'¬'
t_EMERGENCIA = r'◊'

t_HALT = r'■'
t_PURGE = r'⨯'
t_ISOLATE = r'☒'
t_AUDIT = r'☑'
t_KILL = r'☠'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = ' \t\n'

def t_error(t):
    raise ErrorLexico(f"Carácter ilegal '{t.value[0]}'", t.lineno, get_column(t.lexpos))

# === PRECEDENCIA ===
precedence = (
    ('left', 'RESULTADO', 'FLUJO_ORIENTADO'),
    ('left', 'RETROACCION', 'FLUJO_CICLICO'),
    ('left', 'OR_LOGICO', 'AND_LOGICO'),
    ('right', 'NOT_LOGICO'),
    ('left', 'APROXIMACION'),
    ('left', 'FUSION', 'COLISION', 'INTERCAMBIO'),
    ('left', 'SUMA', 'RESTA'),
    ('left', 'MULTIPLICACION', 'DIVISION'),
    ('right', 'POTENCIACION', 'ATENUACION'),
    ('right', 'SUPERINDICE', 'SUBINDICE'),
    ('left', 'PROBABILIDAD', 'EMERGENCIA'),
    ('nonassoc', 'PARENTESIS_FUERTE_ABRE', 'PARENTESIS_FUERTE_CIERRA',
     'PARENTESIS_FLUIDO_ABRE', 'PARENTESIS_FLUIDO_CIERRA'),
    ('nonassoc', 'HALT', 'PURGE', 'ISOLATE', 'AUDIT', 'KILL'),
)

# === REGLAS DEL PARSER ===

def p_programa_expresion(p):
    'programa : expresion'
    p[0] = p[1]


def p_expresion_glifo_principal(p):
    '''expresion : GLA
                 | GLB
                 | GLC
                 | GLD
                 | GLE
                 | GLF
                 | GLG
                 | GLH
                 | GLI
                 | GLJ
                 | GLK
                 | GLL
                 | GLM
                 | GLN
                 | GLO
                 | GLP
                 | GLQ
                 | GLR
                 | GLS
                 | GLT
                 | GLU
                 | GLV
                 | GLW
                 | GLX
                 | GLY
                 | GLZ
                 | GL1
                 | GL2
                 | GL3
                 | GL4
                 | GL5
                 | GL6
                 | GL7
                 | GL8
                 | GL9
                 | GL10
                 | GL11
                 | GL12
                 | GL13
                 | GL14'''
    glifo = p[1]
    codigo = None
    nombre = None
    for cod, info in GLIFOS.get("GLOSARIO", {}).items():
        if info['glifo'] == glifo:
            codigo = cod
            nombre = info['nombre']
            break
    p[0] = Estado(glifo=glifo, codigo=codigo or 'UNKNOWN',
                  nombre=nombre or 'Desconocido',
                  fila=p.lineno(1), columna=get_column(p.lexpos(1)))


def p_expresion_glifo_reflexivo(p):
    '''expresion : REFLEXIVO_INICIO
                 | REFLEXIVO_CLAUSURA
                 | REFLEXIVO_FUEGO
                 | REFLEXIVO_TIERRA
                 | REFLEXIVO_LLAVE1
                 | REFLEXIVO_LLAVE2
                 | REFLEXIVO_LLAVE3'''
    glifo = p[1]
    codigo = None
    nombre = None
    for cod, info in GLIFOS.get("glifos_reflexivos", {}).items():
        if info['glifo'] == glifo:
            codigo = cod
            nombre = info['nombre']
            break
    p[0] = Estado(glifo=glifo, codigo=codigo or 'UNKNOWN',
                  nombre=nombre or 'Desconocido',
                  fila=p.lineno(1), columna=get_column(p.lexpos(1)))


def p_expresion_glifo_sistema(p):
    '''expresion : SIS_MEMORIA
                 | SIS_CICLO
                 | SIS_ENTIDAD
                 | SIS_DESPERTAR
                 | SIS_MUTANTE'''
    glifo = p[1]
    codigo = None
    nombre = None
    for cod, info in GLIFOS.get("glifos_sistema", {}).items():
        if info['glifo'] == glifo:
            codigo = cod
            nombre = info['nombre']
            break
    p[0] = Estado(glifo=glifo, codigo=codigo or 'UNKNOWN',
                  nombre=nombre or 'Desconocido',
                  fila=p.lineno(1), columna=get_column(p.lexpos(1)))


def p_expresion_glifo_interaccion(p):
    '''expresion : INT_CONEXION
                 | INT_DIALOGO
                 | INT_RUPTURA
                 | INT_NEXO
                 | INT_META'''
    glifo = p[1]
    codigo = None
    nombre = None
    for cod, info in GLIFOS.get("glifos_interaccion", {}).items():
        if info['glifo'] == glifo:
            codigo = cod
            nombre = info['nombre']
            break
    p[0] = Estado(glifo=glifo, codigo=codigo or 'UNKNOWN',
                  nombre=nombre or 'Desconocido',
                  fila=p.lineno(1), columna=get_column(p.lexpos(1)))


def p_expresion_suma(p):
    'expresion : expresion SUMA expresion'
    p[0] = OperacionBinaria(op=p[2], izq=p[1], der=p[3],
                            fila=p.lineno(1), columna=get_column(p.lexpos(1)))


def p_expresion_resta(p):
    'expresion : expresion RESTA expresion'
    p[0] = OperacionBinaria(op=p[2], izq=p[1], der=p[3],
                            fila=p.lineno(1), columna=get_column(p.lexpos(1)))


def p_expresion_multiplicacion(p):
    'expresion : expresion MULTIPLICACION expresion'
    p[0] = OperacionBinaria(op=p[2], izq=p[1], der=p[3],
                            fila=p.lineno(1), columna=get_column(p.lexpos(1)))


def p_expresion_division(p):
    'expresion : expresion DIVISION expresion'
    p[0] = OperacionBinaria(op=p[2], izq=p[1], der=p[3],
                            fila=p.lineno(1), columna=get_column(p.lexpos(1)))


def p_expresion_aproximacion(p):
    'expresion : expresion APROXIMACION expresion'
    p[0] = OperacionBinaria(op=p[2], izq=p[1], der=p[3],
                            fila=p.lineno(1), columna=get_column(p.lexpos(1)))


def p_expresion_fusion(p):
    'expresion : expresion FUSION expresion'
    p[0] = OperacionBinaria(op=p[2], izq=p[1], der=p[3],
                            fila=p.lineno(1), columna=get_column(p.lexpos(1)))


def p_expresion_colision(p):
    'expresion : expresion COLISION expresion'
    p[0] = OperacionBinaria(op=p[2], izq=p[1], der=p[3],
                            fila=p.lineno(1), columna=get_column(p.lexpos(1)))


def p_expresion_intercambio(p):
    'expresion : expresion INTERCAMBIO expresion'
    p[0] = OperacionBinaria(op=p[2], izq=p[1], der=p[3],
                            fila=p.lineno(1), columna=get_column(p.lexpos(1)))


def p_expresion_potenciacion(p):
    'expresion : expresion POTENCIACION expresion'
    p[0] = OperacionBinaria(op=p[2], izq=p[1], der=p[3],
                            fila=p.lineno(1), columna=get_column(p.lexpos(1)))


def p_expresion_atenuacion(p):
    'expresion : expresion ATENUACION expresion'
    p[0] = OperacionBinaria(op=p[2], izq=p[1], der=p[3],
                            fila=p.lineno(1), columna=get_column(p.lexpos(1)))


def p_expresion_resultado(p):
    'expresion : expresion RESULTADO expresion'
    p[0] = Flujo(tipo='RESULT', origen=p[1], destino=p[3],
                 fila=p.lineno(1), columna=get_column(p.lexpos(1)))


def p_expresion_flujo_orientado(p):
    'expresion : expresion FLUJO_ORIENTADO expresion'
    p[0] = Flujo(tipo='FLOW', origen=p[1], destino=p[3],
                 fila=p.lineno(1), columna=get_column(p.lexpos(1)))


def p_expresion_retroaccion(p):
    'expresion : RETROACCION expresion'
    p[0] = Flujo(tipo='LOOP', origen=p[2], destino=None,
                 fila=p.lineno(1), columna=get_column(p.lexpos(1)))


def p_expresion_flujo_ciclico(p):
    'expresion : FLUJO_CICLICO expresion'
    p[0] = Flujo(tipo='CYCLE', origen=p[2], destino=p[2],
                 fila=p.lineno(1), columna=get_column(p.lexpos(1)))


def p_expresion_temporal(p):
    '''expresion : TEMPORALIDAD expresion
                 | PERSISTENCIA expresion
                 | INSTANTANEO expresion
                 | CADENCIA expresion'''
    tipo = {'⌛': 'TIME', '∞': 'PERSIST', '⚡': 'INSTANT', '⧖': 'RHYTHM'}[p[1]]
    p[0] = Modificador(tipo=tipo, nivel=None, contenido=p[2],
                       fila=p.lineno(1), columna=get_column(p.lexpos(1)))


def p_expresion_logica(p):
    '''expresion : expresion OR_LOGICO expresion
                 | expresion AND_LOGICO expresion'''
    p[0] = OperacionBinaria(op=p[2], izq=p[1], der=p[3],
                            fila=p.lineno(1), columna=get_column(p.lexpos(1)))


def p_expresion_not_logico(p):
    'expresion : NOT_LOGICO expresion'
    p[0] = Modificador(tipo='NOT', contenido=p[2],
                       fila=p.lineno(1), columna=get_column(p.lexpos(1)))


def p_expresion_probabilidad(p):
    'expresion : PROBABILIDAD expresion'
    p[0] = Modificador(tipo='PROB', contenido=p[2],
                       fila=p.lineno(1), columna=get_column(p.lexpos(1)))


def p_expresion_emergencia(p):
    'expresion : EMERGENCIA expresion'
    p[0] = Modificador(tipo='EMERGE', contenido=p[2],
                       fila=p.lineno(1), columna=get_column(p.lexpos(1)))


def p_expresion_modificador(p):
    '''expresion : SUPERINDICE expresion
                 | SUBINDICE expresion'''
    tipo = 'SUP' if p[1] == '↑' else 'SUB'
    p[0] = Modificador(tipo=tipo, nivel=None, contenido=p[2],
                       fila=p.lineno(1), columna=get_column(p.lexpos(1)))


def p_expresion_bloque_fuerte(p):
    'expresion : PARENTESIS_FUERTE_ABRE expresion PARENTESIS_FUERTE_CIERRA'
    p[0] = Bloque(contenido=p[2], tipo='BLK',
                  fila=p.lineno(1), columna=get_column(p.lexpos(1)))


def p_expresion_bloque_fluido(p):
    'expresion : PARENTESIS_FLUIDO_ABRE expresion PARENTESIS_FLUIDO_CIERRA'
    p[0] = Bloque(contenido=p[2], tipo='DYN',
                  fila=p.lineno(1), columna=get_column(p.lexpos(1)))


def p_expresion_control(p):
    '''expresion : HALT
                 | PURGE
                 | ISOLATE
                 | AUDIT
                 | KILL'''
    p[0] = Control(comando=p[1],
                   fila=p.lineno(1), columna=get_column(p.lexpos(1)))


def p_error(p):
    if p:
        raise ErrorSintactico(f"Error sintáctico cerca del token '{p.value}'",
                              p.lineno, get_column(p.lexpos))
    else:
        raise ErrorSintactico("Expresión incompleta o vacía",
                              lexer.lineno, 0)


def get_column(lexpos):
    if lexer.lexdata is None:
        return 0
    line_start = lexer.lexdata.rfind('\n', 0, lexpos) + 1
    return lexpos - line_start


parser = yacc.yacc(
    debug=True,
    write_tables=True,
    errorlog=yacc.PlyLogger(sys.stderr)
)


def parsear(expresion: str):
    """
    Parsea una cadena Mathema v4.0 y devuelve un AST simbólico para estados de conciencia.
    """
    lexer.lineno = 1
    return parser.parse(expresion, lexer=lexer)
