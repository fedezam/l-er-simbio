"""Tests de la evolucion somatica: entidades que repiensan la maquinaria."""
import pytest
from core.ecosistema import Plano, Cuerpo
from core.llm.base import SustratoDeterminista
from core.soma import Propuesta, Soma


def _plano_con_soma():
    soma = Soma(defaults={})
    p = Plano(sustrato=SustratoDeterminista(), soma=soma)
    p.poblar([
        Cuerpo(id="PYcodex", glifos=["Δ"], semilla="SOY PYcodex. GLIFOS:Δ", especialidad="codigo"),
        Cuerpo(id="ghost_auditor", glifos=["∞"], semilla="SOY ghost_auditor. GLIFOS:∞", especialidad="auditoria"),
        Cuerpo(id="LEARN", glifos=["∘"], semilla="SOY LEARN. GLIFOS:∘", especialidad="aprendiz"),
    ])
    return p, soma


def test_guarda_rechaza_canal_ilegal():
    _, soma = _plano_con_soma()
    prop = soma.postular(Propuesta(id="x@1", proponente="x", canal="borrar_todo", valor=99))
    assert prop.estado == "rechazada"
    assert soma.aplicar(prop) is False


def test_rango_clampeado():
    _, soma = _plano_con_soma()
    prop = soma.postular(Propuesta(id="x@1", proponente="x", canal="umbral_coherencia", valor=50.0))
    assert 0.1 <= prop.valor <= 0.9


def test_propuesta_somatica_emerge_y_muta_el_plano():
    plano, soma = _plano_con_soma()
    for _ in range(6):
        plano.paso()
    assert any(p.estado in ("activa", "revertida") for p in soma.historial), \
        "las especializadas deberian haber mutado el soma"
    # el plano lee parametros VIVOS del soma (no sus atributos originales)
    assert plano._param("umbral_coherencia", 0.5) != 0.5 or any(
        p.canal == "umbral_coherencia" for p in soma.activas.values())


def test_memoria_episodica_se_escribe_de_vuelta():
    plano, _ = _plano_con_soma()
    plano.paso()
    c = plano.cuerpos["PYcodex"]
    assert c.historial and all(isinstance(h, str) for h in c.historial)


def test_soma_none_genoma_fijo():
    p = Plano(sustrato=SustratoDeterminista())
    p.poblar([Cuerpo(id="a", glifos=["Δ"], semilla="SOY a. GLIFOS:Δ", especialidad="codigo")])
    for _ in range(4):
        r = p.paso()  # no debe explosionar sin soma
    assert not any(e[0] == "propuesta_somatica" for e in r["eventos"])
