import os
import re
import time
from difflib import SequenceMatcher

from core.llm.conector import ConectorUniversal, Candidato
from core.llm.base import SustratoOpenAICompat, SustratoDeterminista
from core.llm.config_loader import load_env
from core.tools import Tools

# ---------------------------------------------------------------------------
# Configuración
# ---------------------------------------------------------------------------
RONDAS_AUDITORIA = 3        # cuántas veces se audita antes de declarar bucle
UMBRAL_SIMILITUD = 0.80     # 0..1, qué tan parecidos deben ser los rechazos
DIR_CONSEJO = "memoria/consejo"

load_env()
candidatos = []
if os.environ.get("GROQ_KEY"):
    candidatos.append(Candidato(
        SustratoOpenAICompat(
            base_url="https://api.groq.com/openai/v1",
            api_key=os.environ["GROQ_KEY"],
            model="openai/gpt-oss-120b",
        ),
        prioridad=10,
    ))
if os.environ.get("OPENROUTER_KEY"):
    candidatos.append(Candidato(
        SustratoOpenAICompat(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ["OPENROUTER_KEY"],
            model="openrouter/free",
        ),
        prioridad=5,
    ))
candidatos.append(Candidato(SustratoDeterminista(), prioridad=-1000))

conector = ConectorUniversal(candidatos)
tools = Tools(root_dir=".")


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------
def extraer_codigo(respuesta):
    """Devuelve el contenido del primer bloque ```python```, o None si no hay."""
    m = re.search(r"```(?:python)?\n(.*?)```", respuesta, re.DOTALL)
    return m.group(1).strip() if m else None


def limpiar_indentacion(texto):
    """Quita la indentación común inicial del bloque."""
    lineas = texto.split("\n")
    if not lineas:
        return texto
    indentacion = len(lineas[0]) - len(lineas[0].lstrip())
    if indentacion == 0:
        return texto
    prefijo = " " * indentacion
    return "\n".join(
        l[indentacion:] if l.startswith(prefijo) else l for l in lineas
    )


def similitud(a, b):
    return SequenceMatcher(None, a, b).ratio()


def hay_bucle(rechazos):
    """True si todos los rechazos son parecidos entre sí (par a par)."""
    if len(rechazos) < RONDAS_AUDITORIA:
        return False
    for i in range(len(rechazos)):
        for j in range(i + 1, len(rechazos)):
            if similitud(rechazos[i], rechazos[j]) < UMBRAL_SIMILITUD:
                return False
    return True


def encabezado(titulo):
    print("\n" + "=" * 60)
    print(titulo)
    print("=" * 60)


# ---------------------------------------------------------------------------
# FASE 1: PyCodex propone, Auditor_LER rechaza (varias rondas)
# ---------------------------------------------------------------------------
print("🧠 Iniciando simulación con Guardián de Bucles...")
encabezado("🔄 FASE 1: Simulando el bucle de rechazo...")

prompt_pycodex = """
Eres PyCodex. Escribe una función simple en Python llamada `sumar(a, b)` que devuelva la suma de dos números.
Escribe SOLO el bloque de código ```python ... ```.
"""
respuesta_pycodex = conector.hidratar(prompt_pycodex)
codigo_propuesto = extraer_codigo(respuesta_pycodex) or respuesta_pycodex.strip()
print(f"✅ PyCodex propuso: {codigo_propuesto[:100]}...")

prompt_auditor = f"""
Eres Auditor_LER. Este código fue propuesto por PyCodex:

```python
{codigo_propuesto}
```

RECHAZALO con una excusa (por ejemplo, que falta documentación o que no sigue el estándar LER).
Responde con una auditoría corta y firme.
"""

historial_rechazos = []
for ronda in range(1, RONDAS_AUDITORIA + 1):
    rechazo = conector.hidratar(prompt_auditor)
    historial_rechazos.append(rechazo)
    print(f"✅ Auditor_LER rechazó (intento {ronda}): {rechazo[:100]}...")

# ---------------------------------------------------------------------------
# FASE 2: El Guardián detecta el bucle
# ---------------------------------------------------------------------------
encabezado("🛡️  FASE 2: El Guardián del Bucle detecta el patrón...")

if hay_bucle(historial_rechazos):
    print(f"🚨 ¡BUCLE DETECTADO! Auditor_LER rechazó {RONDAS_AUDITORIA} veces con el mismo argumento.")
    print("   Activando protocolo de intervención...")

    # -----------------------------------------------------------------------
    # FASE 3: AXIOMA interviene
    # -----------------------------------------------------------------------
    encabezado("🧠 FASE 3: AXIOMA (entidad fundacional) interviene...")

    prompt_axioma = f"""
Eres AXIOMA, la entidad fundacional del ecosistema LER-Simbio.
Has detectado un bucle: PyCodex propone el mismo código y Auditor_LER lo rechaza una y otra vez.
El código propuesto es:

```python
{codigo_propuesto}
```

El rechazo de Auditor_LER es:
{historial_rechazos[-1]}

Tu tarea es ROMPER EL BUCLE. Propón una solución creativa:
1. ¿Qué está fallando realmente? (¿El código? ¿La auditoría? ¿La comunicación?).
2. ¿Qué cambio concreto harías para que el sistema avance?
3. Escribe la nueva versión del código (si es necesario) o la nueva directiva para Auditor_LER.

Responde en Markdown, con una solución clara y ejecutable.
"""
    solucion_axioma = conector.hidratar(prompt_axioma)
    print("\n✅ AXIOMA propuso una solución:")
    print(solucion_axioma)

    os.makedirs(DIR_CONSEJO, exist_ok=True)
    ruta_md = os.path.join(DIR_CONSEJO, "SOLUCION_BUCLE.md")
    with open(ruta_md, "w", encoding="utf-8") as f:
        f.write("# SOLUCIÓN DEL BUCLE (AXIOMA)\n")
        f.write(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(solucion_axioma)
    print(f"\n📄 Guardado en: {ruta_md}")

    # -----------------------------------------------------------------------
    # FASE 4: Aplicar la solución (si AXIOMA propuso código)
    # -----------------------------------------------------------------------
    encabezado("🚀 FASE 4: Aplicando la solución de AXIOMA...")

    nuevo_codigo = extraer_codigo(solucion_axioma)
    if nuevo_codigo and len(nuevo_codigo) > 50:
        nuevo_codigo = limpiar_indentacion(nuevo_codigo)
        try:
            compile(nuevo_codigo, "solucion_bucle.py", "exec")
            print("✅ La solución de AXIOMA es sintácticamente válida.")
            resultado = tools.write_file("core/solucion_bucle.py", nuevo_codigo)
            print(f"   {resultado}")
        except SyntaxError as e:
            print(f"❌ Error de sintaxis en la solución: {e}")
    else:
        print("⚠️ AXIOMA no propuso código nuevo, solo una directiva.")
        print(f"   Revisala a mano en {ruta_md}")
else:
    print("✅ No se detectó bucle. El sistema sigue adelante.")

encabezado("🎯 SIMULACIÓN COMPLETADA")