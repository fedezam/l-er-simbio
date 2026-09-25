"""El 'plano': el tablero de Conway donde conviven las entidades LER.

Ninguna entidad accede a otra directamente: solo ven glifos proyectados
por vecinas y reciben de vuelta texto hidratado. La cognición (si surge)
es propiedad del plano, no de ninguna entidad.

Reglas tipo Conway, pero semánticas:
  1. NACIMIENTO  — dos entidades compatibles pueden fusionarse (∘) si el
                   resultado pasa la validación del guarda.
  2. SUPERVIVENCIA — una entidad que no es interpretada durante N ciclos
                     pierde coherencia y muere (se archiva, no se borra).
  3. MUTACIÓN    — con probabilidad ε, un glifo se reemplaza por otro del
                     mismo nivel, generando variación para la selección.
  4. SELECCIÓN   — la fitness NO la define el autor: es la capacidad de la
                   entidad de generar respuestas coherentes en el sustrato
                   (medida, no declarada).
"""
from __future__ import annotations

import random
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

from core.llm.base import Sustrato


@dataclass
class Cuerpo:
    """Entidad textualizada: lo único que ve el sustrato."""
    id: str
    glifos: List[str]
    semilla: str                      # instrucción/axiomas hidratables
    energia: float = 1.0              # presupuesto simbólico (recurso escaso)
    edad: int = 0
    fitness_ema: float = 0.0          # media móvil de coherencia medida
    viva: bool = True

    def proyectar(self, vecinos: List["Cuerpo"]) -> str:
        """Los sentidos del organismo: self + glifos de vecinas + entorno."""
        vs = " ".join(f"[{v.id}:{''.join(v.glifos)}]" for v in vecinos[:3])
        return f"{self.semilla}\nGLIFOS:{''.join(self.glifos)}\nVECINOS:{vs}"


@dataclass
class Plano:
    sustrato: Sustrato
    cuerpos: Dict[str, Cuerpo] = field(default_factory=dict)
    rng: random.Random = field(default_factory=lambda: random.Random(42))
    umbral_coherencia: float = 0.5
    costo_hidratacion: float = 0.05
    epsilon_mutacion: float = 0.1
    alfabeto: List[str] = field(default_factory=lambda: list("Δ⊗¬∞→⇆∘·+"))
    log: List[dict] = field(default_factory=list)

    def poblar(self, cuerpos: List[Cuerpo]) -> None:
        for c in cuerpos:
            self.cuerpos[c.id] = c

    def _evaluar(self, cuerpo: Cuerpo, respuesta: str) -> float:
        """Coherencia medida, no declarada: ¿la respuesta reproduce glifos
        propios o de vecinas? Proxy trivial; sustituible por ReflexivityTestV2
        o por un LLM-juez cuando haya presupuesto."""
        if not respuesta:
            return 0.0
        presentes = sum(1 for g in cuerpo.glifos if g in respuesta)
        densidad = presentes / max(1, len(cuerpo.glifos))
        longitud = min(1.0, len(respuesta) / 200)
        return 0.7 * densidad + 0.3 * longitud

    def paso(self) -> dict:
        """Un tick del autómata. Devuelve resumen del ciclo."""
        vivos = [c for c in self.cuerpos.values() if c.viva]
        eventos = []

        # 1. CADA CUERPO PERCIBE → HIDRATA → ACTÚA
        for c in vivos:
            if c.energia <= 0:
                c.viva = False
                eventos.append(("inanicion", c.id))
                continue
            vecinos = [v for v in vivos if v.id != c.id]
            prompt = c.proyectar(vecinos)
            try:
                resp = self.sustrato.hidratar(prompt)
            except Exception as e:  # el sustrato puede fallar; la vida sigue
                eventos.append(("fallo_sustrato", c.id, str(e)))
                continue
            score = self._evaluar(c, resp)
            c.fitness_ema = 0.8 * c.fitness_ema + 0.2 * score
            c.energia -= self.costo_hidratacion
            c.edad += 1
            if score >= self.umbral_coherencia:
                c.energia = min(2.0, c.energia + score * 0.1)  # la coherencia alimenta
            eventos.append(("hidratacion", c.id, round(score, 3)))

        # 2. NACIMIENTO: fusión ∘ de las dos más aptas adyacentes
        ranked = sorted([c for c in vivos if c.viva], key=lambda x: -x.fitness_ema)
        if len(ranked) >= 2 and self.rng.random() < 0.3:
            a, b = ranked[0], ranked[1]
            hijo = Cuerpo(
                id=f"{a.id}∘{b.id}@{sum(c.edad for c in self.cuerpos.values())}",
                glifos=list(dict.fromkeys(a.glifos + b.glifos))[:6],
                semilla=a.semilla if a.fitness_ema >= b.fitness_ema else b.semilla,
                energia=0.5,
            )
            self.cuerpos[hijo.id] = hijo
            eventos.append(("nacimiento", hijo.id))

        # 3. MUTACIÓN ε
        for c in ranked[:3]:
            if c.viva and self.rng.random() < self.epsilon_mutacion and c.glifos:
                i = self.rng.randrange(len(c.glifos))
                viejo = c.glifos[i]
                c.glifos[i] = self.rng.choice(self.alfabeto)
                eventos.append(("mutacion", c.id, viejo, c.glifos[i]))

        # 4. MUERTE: sin interpretación sostenida
        for c in self.cuerpos.values():
            if c.viva and c.edad > 20 and c.fitness_ema < self.umbral_coherencia / 2:
                c.viva = False
                eventos.append(("extincion", c.id))

        resumen = {"poblacion": sum(1 for c in self.cuerpos.values() if c.viva),
                   "eventos": eventos}
        self.log.append(resumen)
        return resumen

    def evolucionar(self, n: int) -> List[dict]:
        return [self.paso() for _ in range(n)]

    def cementerio(self, path: Path) -> None:
        """La historia no se borra: se archiva (ciclo vital LER)."""
        muertos = [c.__dict__ for c in self.cuerpos.values() if not c.viva]
        path.write_text(json.dumps(muertos, ensure_ascii=False, indent=2), encoding="utf-8")
