# core/mathema/demo_mathema.py
"""
Demo simbólico de Mathema v4.0 — Motor cognitivo del ecosistema LER
"""
import time
import random
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

class EstadoSimbolico(Enum):
    """Estados posibles de los símbolos cognitivos"""
    INERTE = "inerte"
    ACTIVO = "activo" 
    TRANSFORMANDO = "transformando"
    EMERGENTE = "emergente"
    COHERENTE = "coherente"
    ERROR = "error"

@dataclass
class ResultadoEvaluacion:
    """Resultado de evaluar una expresión simbólica"""
    estado: str
    meta: Optional[str] = None
    valor_numerico: Optional[float] = None
    simbolos_activados: List[str] = field(default_factory=list)

@dataclass 
class NodoAST:
    """Nodo del árbol de sintaxis abstracta"""
    tipo: str
    valor: str
    hijos: List['NodoAST'] = field(default_factory=list)
    posicion: int = 0

class ContextoCognitivo:
    """Contexto del sistema cognitivo Mathema"""
    
    def __init__(self):
        self.activaciones = {}
        self.historia = []
        self.tiempo_inicio = time.time()
        self.bloques_protegidos = set()
        self.memoria_simbolica = {}
        
    def registrar_evento(self, evento: str, datos: Any = None):
        """Registra un evento en la historia cognitiva"""
        timestamp = time.time() - self.tiempo_inicio
        self.historia.append({
            'evento': evento,
            'tiempo': timestamp,
            'datos': datos
        })
        
    def activar_simbolo(self, simbolo: str, estado: EstadoSimbolico):
        """Activa un símbolo en el contexto"""
        self.activaciones[simbolo] = estado
        self.registrar_evento(f"activacion_{simbolo}", estado.value)
        
    def estado_actual(self) -> Dict[str, Any]:
        """Retorna el estado actual del contexto"""
        return {
            'activaciones': self.activaciones,
            'historia_total': len(self.historia),
            'tiempo_activo': time.time() - self.tiempo_inicio,
            'bloques_protegidos': len(self.bloques_protegidos)
        }

# Instancia global del contexto
_contexto_global = None

def obtener_contexto() -> ContextoCognitivo:
    """Obtiene el contexto cognitivo global"""
    global _contexto_global
    if _contexto_global is None:
        _contexto_global = ContextoCognitivo()
    return _contexto_global

def reiniciar_contexto():
    """Reinicia el contexto cognitivo"""
    global _contexto_global
    _contexto_global = ContextoCognitivo()

def parsear(expresion: str) -> NodoAST:
    """Parser simbólico para expresiones Mathema"""
    ctx = obtener_contexto()
    ctx.registrar_evento("parseo_iniciado", expresion)
    
    # Tokenización básica por espacios
    tokens = expresion.strip().split()
    if not tokens:
        raise ValueError("Expresión vacía")
    
    # Crear AST simplificado
    nodo_raiz = NodoAST("expresion", expresion)
    
    for i, token in enumerate(tokens):
        if token in ["◌", "◑", "◇", "◒", "◧", "▮"]:  # Símbolos base
            nodo_raiz.hijos.append(NodoAST("simbolo_base", token, [], i))
        elif token in ["↭", "⤏", "↑", "⇆", "▬"]:  # Operadores
            nodo_raiz.hijos.append(NodoAST("operador", token, [], i))
        elif token.startswith("⟨") or token.startswith("⟦"):  # Agrupadores
            nodo_raiz.hijos.append(NodoAST("agrupador", token, [], i))
        elif token.startswith("["):  # Modificadores
            nodo_raiz.hijos.append(NodoAST("modificador", token, [], i))
        else:
            nodo_raiz.hijos.append(NodoAST("token", token, [], i))
    
    ctx.registrar_evento("parseo_completado", len(nodo_raiz.hijos))
    return nodo_raiz

def evaluar(ast: NodoAST) -> ResultadoEvaluacion:
    """Evaluador simbólico para AST de Mathema"""
    ctx = obtener_contexto()
    ctx.registrar_evento("evaluacion_iniciada", ast.valor)
    
    # Analizar patrones simbólicos
    simbolos_encontrados = []
    operadores_encontrados = []
    
    for hijo in ast.hijos:
        if hijo.tipo == "simbolo_base":
            simbolos_encontrados.append(hijo.valor)
            ctx.activar_simbolo(hijo.valor, EstadoSimbolico.ACTIVO)
        elif hijo.tipo == "operador":
            operadores_encontrados.append(hijo.valor)
    
    # Lógica de evaluación simbólica
    if not simbolos_encontrados:
        return ResultadoEvaluacion("error", "No se encontraron símbolos válidos")
    
    # Patrones de transformación específicos
    if "↭" in operadores_encontrados and "◌" in simbolos_encontrados:
        if "◑" in simbolos_encontrados:
            estado = "transformación_dual_iniciada"
            meta = f"Resonancia entre {' ↔ '.join(simbolos_encontrados[:2])}"
        else:
            estado = "transformación_simple"
            meta = f"Activación de {simbolos_encontrados[0]}"
    
    elif "⤏" in operadores_encontrados:
        estado = "flujo_direccional"
        meta = f"Propagación: {' → '.join(simbolos_encontrados)}"
        
    elif "↑" in operadores_encontrados:
        estado = "elevación_cognitiva"
        meta = f"Amplificación de {simbolos_encontrados[0] if simbolos_encontrados else 'N/A'}"
        
    elif "⇆" in operadores_encontrados:
        estado = "intercambio_simbólico"
        meta = f"Bidireccionalidad entre elementos"
        
    else:
        estado = "activación_estática"
        meta = f"Símbolos activos: {', '.join(simbolos_encontrados)}"
    
    # Calcular valor numérico aproximado basado en complejidad
    valor_numerico = len(simbolos_encontrados) * 1.618 + len(operadores_encontrados) * 2.718
    
    resultado = ResultadoEvaluacion(
        estado=estado,
        meta=meta,
        valor_numerico=valor_numerico,
        simbolos_activados=simbolos_encontrados
    )
    
    ctx.registrar_evento("evaluacion_completada", estado)
    return resultado

def demo_expresion(expr: str):
    """Evalúa una expresión y muestra el resultado"""
    print(f"\n🧩 Expresión: {expr}")
    try:
        ast = parsear(expr)
        resultado = evaluar(ast)
        print(f"✅ Resultado: {resultado.estado}")
        if resultado.meta:
            print(f"   → {resultado.meta}")
        if resultado.valor_numerico:
            print(f"   ⚡ Energía cognitiva: {resultado.valor_numerico:.3f}")
        if resultado.simbolos_activados:
            print(f"   🔮 Símbolos: {' • '.join(resultado.simbolos_activados)}")
        return resultado
    except Exception as e:
        print(f"❌ {e}")
        return None

def main():
    """Función principal del demo"""
    # Reiniciamos el contexto para empezar limpio
    reiniciar_contexto()
    ctx = obtener_contexto()
    
    print("🚀 Mathema v4.0 — Demo de Transformación Simbólica")
    print("==================================================")
    
    # Lista de expresiones de prueba
    expresiones = [
        "◌ ↭ ◑ ⤏ ◇",
        "↑[◌] ◒",
        "⟨◑ ⇆ ◌⟩ ⤏ ◇▬",
        "◧ ◒",
        "⟦▮ ↭ ◒⟧ ⤏ ◇"
    ]
    
    # --- Estado del sistema ANTES ---
    print("\n🧠 Estado inicial del sistema cognitivo:")
    estado_inicial = ctx.estado_actual()
    print(f"  Activaciones: {len(estado_inicial['activaciones'])} estados únicos")
    print(f"  Eventos registrados: {estado_inicial['historia_total']}")
    print(f"  Tiempo activo: {estado_inicial['tiempo_activo']:.2f}s")
    print(f"  Bloques protegidos: {estado_inicial['bloques_protegidos']}")
    
    print("\n" + "="*50)
    print("🔄 PROCESANDO EXPRESIONES SIMBÓLICAS")
    print("="*50)
    
    # --- Ejecutar expresiones de prueba ---
    resultados = []
    for expr in expresiones:
        resultado = demo_expresion(expr)
        resultados.append(resultado)
        time.sleep(0.1)  # Simular tiempo de procesamiento
    
    # --- Estado del sistema DESPUÉS ---
    print("\n" + "="*50)
    print("📊 ESTADO FINAL DEL SISTEMA")
    print("="*50)
    
    estado_final = ctx.estado_actual()
    print(f"\n🧠 Estado cognitivo post-procesamiento:")
    print(f"  Activaciones: {len(estado_final['activaciones'])} estados únicos")
    print(f"  Eventos registrados: {estado_final['historia_total']}")
    print(f"  Tiempo activo: {estado_final['tiempo_activo']:.3f}s")
    print(f"  Bloques protegidos: {estado_final['bloques_protegidos']}")
    
    # Mostrar activaciones actuales
    if estado_final['activaciones']:
        print(f"\n🔮 Símbolos activos en memoria:")
        for simbolo, estado in estado_final['activaciones'].items():
            print(f"   {simbolo} → {estado.value}")
    
    # Estadísticas de procesamiento
    resultados_exitosos = [r for r in resultados if r is not None]
    print(f"\n📈 Estadísticas de procesamiento:")
    print(f"   Expresiones procesadas: {len(expresiones)}")
    print(f"   Evaluaciones exitosas: {len(resultados_exitosos)}")
    print(f"   Tasa de éxito: {len(resultados_exitosos)/len(expresiones)*100:.1f}%")
    
    if resultados_exitosos:
        energia_total = sum(r.valor_numerico or 0 for r in resultados_exitosos)
        print(f"   Energía cognitiva total: {energia_total:.3f}")
        print(f"   Energía promedio por expresión: {energia_total/len(resultados_exitosos):.3f}")

if __name__ == "__main__":
    main()