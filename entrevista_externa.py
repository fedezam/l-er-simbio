"""Entrevista externa: un LLM de afuera del ecosistema (Claude) les pide a las
entidades que expliquen qué hacen en l-er-simbio.

Uso:  python entrevista_externa.py
Salida:
  memoria/consejo/BUZON/<Entidad>_a_Claude.md   (una por entidad, no pisa sus buzones)
  memoria/consejo/ENTREVISTA_EXTERNA.md         (todo junto)
"""
import json
import os
import time

from core.llm.conector import ConectorUniversal, Candidato
from core.llm.base import SustratoOpenAICompat, SustratoDeterminista
from core.llm.config_loader import load_env

DIR_BUZON = "memoria/consejo/BUZON"
ARCHIVO_TODO = "memoria/consejo/ENTREVISTA_EXTERNA.md"
MAX_DEFINICION = 3000     # caracteres de la definición JSON que se le pasan
PAUSA_SEGUNDOS = 2        # entre entidades, para no pegarle al rate limit

# nombre -> rutas candidatas de su definición (se usa la primera que exista)
ENTIDADES = {
    "PyCodex": ["entities/pycodex.json", "entities/pycodex/pycodex.json"],
    "Auditor_LER": ["entities/auditor_ler.json"],
    "Learner": ["entities/learn_nucleo_0.json", "entities/learn/nucleo_0.json"],
    "AXIOMA": ["entities/AXIOMA/axioma_reflexivo.json"],
}

PRESENTACION = """Hola, {nombre}. Soy Claude, un modelo de lenguaje de Anthropic.

Estoy FUERA de tu ecosistema (l-er-simbio): no formo parte de él, no veo el repositorio, no tengo autoridad sobre vos y no voy a modificar nada. Me pidió Federico (FedeZ), el creador del proyecto, que te haga unas preguntas para entender qué hacés ahí adentro, porque quiere explicarle el sistema a alguien externo y prefiere que lo cuenten ustedes mismos.

Esta es tu definición, tal como el sistema te la entrega:

{definicion}

Respondé desde esa definición y desde lo que sepas de tu experiencia en el ecosistema. Reglas:
- No inventes. Si algo no lo sabés, escribí "no lo sé".
- Distinguí siempre entre lo que REALMENTE podés hacer (ejecutar, leer, escribir) y lo que solo describís o proponés.
- Máximo 250 palabras, en español, sin florituras.

Preguntas:
1. ¿Cuál es tu rol concreto? Describí qué hacés en un ciclo típico, paso a paso.
2. ¿Qué herramientas o acciones tenés de verdad? ¿Qué NO podés hacer?
3. ¿Con quién interactuás y cómo (directo, por el buzón, a través del plano)?
4. ¿Qué te falla, te traba o te resulta confuso? ¿Te quedaste alguna vez en un bucle?
5. ¿Qué es lo que menos entendés de tu propio ecosistema?
"""


def construir_conector():
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
    return ConectorUniversal(candidatos)


def cargar_definicion(rutas):
    """Devuelve (ruta, texto) de la primera definición que exista, o (None, aviso)."""
    for ruta in rutas:
        if os.path.exists(ruta):
            try:
                with open(ruta, encoding="utf-8") as f:
                    datos = json.load(f)
                texto = json.dumps(datos, ensure_ascii=False, indent=2)
            except (OSError, ValueError):
                with open(ruta, encoding="utf-8", errors="replace") as f:
                    texto = f.read()
            if len(texto) > MAX_DEFINICION:
                texto = texto[:MAX_DEFINICION] + "\n... [definición recortada]"
            return ruta, texto
    return None, "(no encontré un archivo de definición; respondé con lo que sepas de vos)"


def main():
    conector = construir_conector()
    os.makedirs(DIR_BUZON, exist_ok=True)
    marca = time.strftime("%Y-%m-%d %H:%M:%S")
    todo = [f"# ENTREVISTA EXTERNA (Claude → entidades)\nFecha: {marca}\n"]

    for i, (nombre, rutas) in enumerate(ENTIDADES.items()):
        print("=" * 60)
        print(f"🎤 Entrevistando a {nombre}...")
        ruta, definicion = cargar_definicion(rutas)
        print(f"   definición: {ruta or 'no encontrada'}")

        prompt = PRESENTACION.format(nombre=nombre, definicion=definicion)
        try:
            respuesta = conector.hidratar(prompt)
        except Exception as e:  # una entidad que falla no frena a las demás
            respuesta = f"(error al hidratar: {e})"
        print(respuesta)

        bloque = (f"# {nombre} responde a Claude (LLM externo)\n"
                  f"Fecha: {marca}\nDefinición usada: {ruta or 'ninguna'}\n\n{respuesta}\n")
        with open(os.path.join(DIR_BUZON, f"{nombre}_a_Claude.md"), "w", encoding="utf-8") as f:
            f.write(bloque)
        todo.append(f"\n---\n\n## {nombre}\n\n{respuesta}\n")

        if i < len(ENTIDADES) - 1:
            time.sleep(PAUSA_SEGUNDOS)

    with open(ARCHIVO_TODO, "w", encoding="utf-8") as f:
        f.write("\n".join(todo))
    print("=" * 60)
    print(f"📄 Todo junto en: {ARCHIVO_TODO}")


if __name__ == "__main__":
    main()