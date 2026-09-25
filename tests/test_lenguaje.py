"""Tests del bucle linguistico somatico: habla -> traduccion -> canal legal.

Se prueba sin red: el "LLM" es un sustrato guionizado que simula al especialista
proponiendo en lenguaje natural y al juez traductor devolviendo canales.
"""
import pytest

from core.ecosistema import Plano, Cuerpo
from core.juez import Juez
from core.llm.base import Sustrato, SustratoDeterminista
from core.lenguaje import (canales_legales, traducir_a_canal, expresar_propuesta,
                           TraductorPropuestas)
from core.soma import Soma


class SustratoGuion(Sustrato):
    """Devuelve respuestas prefijadas segun contenga o no la semilla de juez."""

    def __init__(self, habla: str, traduccion: str = ""):
        self.habla = habla
        self.traduccion = traduccion
        self.llamadas = []

    def hidratar(self, prompt: str, temperatura: float = 0.7) -> str:
        self.llamadas.append(prompt)
        if "TRADUCTOR SOMATICO" in prompt:
            return self.traduccion
        return self.habla


# ---------- traduccion determinista (fallback offline) ------------------- #

def test_traduce_umbral_desde_el_habla():
    cp = traducir_a_canal(
        "Deberiamos subir el umbral de coherencia a 0.65; el plano tolera demasiado ruido.",
        canales_legales())
    assert cp is not None and cp.canal == "umbral_coherencia"
    assert 0.1 <= cp.valor <= 0.9


def test_no_inventa_canales():
    assert traducir_a_canal("apaga todos los servidores", canales_legales()) is None
    assert traducir_a_canal("NADA", canales_legales()) is None


def test_sin_numero_no_hay_accion():
    assert traducir_a_canal("sube la exigencia de coherencia, sin cifras",
                            canales_legales()) is None


# ---------- traduccion via juez ------------------------------------------- #

def test_juez_traduce_habla_a_canal():
    s = SustratoGuion(habla="...", traduccion="canal: epsilon_mutacion\nvalor: 0.2")
    j = Juez(sustrato_juez=s, presupuesto=10)
    t = TraductorPropuestas(j, canales_legales())
    cp = t.traducir("quiero mas variabilidad simbolica, algo como 0.2")
    assert cp is not None and cp.canal == "epsilon_mutacion" and cp.valor == 0.2


def test_juez_alucinado_es_ilegal_y_degrada_a_parser():
    # juez devuelve un canal inexistente -> se rechaza; fallback al parser determinista
    s = SustratoGuion(habla="...", traduccion="canal: borrar_todo\nvalor: 9")
    j = Juez(sustrato_juez=s, presupuesto=10)
    t = TraductorPropuestas(j, canales_legales())
    cp = t.traducir("sube el costo de hidratacion a 0.1")
    assert cp is not None and cp.canal == "costo_hidratacion"  # lo salvo el parser


# ---------- bucle completo en el plano ------------------------------------- #

def _plano_hablado(guion: SustratoGuion):
    soma = Soma(defaults={})
    juez_s = SustratoGuion(habla="", traduccion="canal: umbral_coherencia\nvalor: 0.6")
    juez = Juez(sustrato_juez=juez_s, presupuesto=30)
    p = Plano(sustrato=guion, soma=soma, juez=juez, lenguaje_propuestas=True)
    p.poblar([Cuerpo(id="PYcodex", glifos=["Δ"],
                     semilla="SOY PYcodex, guardiano del codigo. GLIFOS:Δ",
                     especialidad="codigo")])
    return p, soma


def test_propuesta_hablada_muta_el_soma():
    guion = SustratoGuion(habla="Soy PYcodex y el plano se llena de ruido; "
                                "subiria el umbral de coherencia a 0.6.")
    p, soma = _plano_hablado(guion)
    for _ in range(3):
        r = p.paso()
    habladas = [e for e in sum((x["eventos"] for x in p.log), [])
                if e[0] == "propuesta_somatica" and e[-1] == "hablada"]
    assert habladas, "la propuesta hablada deberia haber mutado el soma"
    prop = next(pr for pr in soma.historial if pr.estado in ("activa", "revertida"))
    # LA JUSTIFICACION ES EL HABLA DEL ORGANISMO, no un glifo generado por el autor
    assert "ruido" in prop.justificacion or "umbral" in prop.justificacion.lower()
    assert abs(soma.get("umbral_coherencia") - 0.6) < 1e-9


def test_expresion_usa_estado_medido_del_cuerpo():
    guion = SustratoGuion(habla="NADA")
    p, soma = _plano_hablado(guion)
    c = p.cuerpos["PYcodex"]
    snap = p._snapshot_soma()
    texto = expresar_propuesta(guion, c, snap)
    assert texto == "NADA"
    prompt = guion.llamadas[-1]
    assert "ESTADO MEDIDO" in prompt and "EL SOMA" in prompt
    assert c.especialidad in prompt


def test_lenguaje_apagado_comportamiento_reflejo():
    soma = Soma(defaults={})
    p = Plano(sustrato=SustratoDeterminista(), soma=soma)  # lenguaje off
    p.poblar([Cuerpo(id="ghost", glifos=["∞"], semilla="SOY ghost. GLIFOS:∞",
                     especialidad="auditoria")])
    for _ in range(6):
        p.paso()
    habladas = [e for e in sum((x["eventos"] for x in p.log), [])
                if e[0] == "propuesta_somatica" and e[-1] == "hablada"]
    assert not habladas  # sin bandera, solo reflejos
