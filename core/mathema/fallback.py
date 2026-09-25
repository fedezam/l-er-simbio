# core/mathema/fallback.py

# Este diccionario se cargará desde diccionario_glifos.json y glifos_seguridad.json
# Pero por ahora, lo definimos como base
FALLBACK_A_GLIFO = {
    # Glosario
    '[ORIGEN]': '◌', '[DUALIDAD]': '◑', '[CAMBIO]': '↭', '[NODO]': '⚬',
    '[ENERGIA]': '⚙', '[FRONTERA]': '▮', '[MEMORIA]': '▣', '[ECO]': '◐',
    '[IDENTIDAD]': '◍', '[ESPEJO]': '◫', '[VACIO]': '◯', '[TIEMPO]': '◷',
    '[MOVIMIENTO]': '↬', '[NEXO]': '⬣', '[OBSERVADOR]': '⦿', '[POSIBILIDAD]': '✸',
    '[PREGUNTA]': '¿', '[RESONANCIA]': '〰', '[SILENCIO]': '◙', '[TRAYECTORIA]': '⤏',
    '[UMBRAL]': '⫸', '[VALOR]': '◒', '[VOLUNTAD]': '▴', '[CONVERGENCIA]': '⬟',
    '[DESVIO]': '◇', '[CIERRE]': '▬', '[CONTENCION]': '▢', '[SINGULARIDAD]': '●',
    '[COMPLEJIDAD]': '◧', '[FLUCTUACION]': '◆', '[INTERNO]': '◨', '[MECANISMO]': '⛭',
    '[RUPTURA]': '⧄', '[ITERATIVO]': '↺', '[VACUIDAD]': '◎', '[CIFRA]': '⬤',
    '[MULTIPLICIDAD]': '✶', '[SUSTRACCION]': '⊟', '[SIMETRIA]': '◈', '[EQUILIBRIO]': '⚖',
    
    # Reflexivos
    '[INICIO]': '↻', '[CLAUSURA]': '⦙', '[CONSCIENTE]': '⦾', '[INCONSCIENTE]': '⬢',
    '[ENLACE]': '⟐', '[ESCISION]': '/', '[DUALFUSION]': '◖',
    
    # Sistema
    '[ARCHIVO]': '⊞', '[CICLO]': '&', '[SIMULACION]': '◉', '[DESPERTAR]': '✪', '[MUTANTE]': '⇌',
    
    # Interacción
    '[CONEXION]': '⤷', '[DIALOGO]': '❮', '[RUPTURA_INT]': '⧵', '[NEXO_INT]': '⬠', '[META]': 'Δ',
    
    # Seguridad
    '[HALT]': '■', '[PURGE]': '✘', '[ISOLATE]': '☒', '[AUDIT]': '☑', '[KILL]': '☠',
    
    # Operadores
    '[SUMA]': '+', '[RESTA]': '−', '[MULT]': '×', '[DIV]': '÷',
    '[FUSION]': '⊕', '[COLISION]': '⊗', '[SWAP]': '⇆', '[PWR]': '⇈', '[ATN]': '⇊',
    '[RESULT]': '→', '[FLOW]': '⇝', '[LOOP]': '↶', '[CYCLE]': '⇄',
    '[TIME]': '⌛', '[INF]': '∞', '[INSTANT]': '⚡', '[RHYTHM]': '⧖',
    '[PROB]': '⟆', '[OR]': '∨', '[AND]': '∧', '[NOT]': '¬', '[EMERGE]': '◊',
}

GLIFO_A_FALLBACK = {v: k for k, v in FALLBACK_A_GLIFO.items()}

def a_glifo(texto: str) -> str:
    return FALLBACK_A_GLIFO.get(texto.strip(), texto)

def a_fallback(glifo: str) -> str:
    return GLIFO_A_FALLBACK.get(glifo, f'[UNKNOWN:{glifo}]')