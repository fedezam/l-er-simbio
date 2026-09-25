# core/mmp_engine.py
# MMP Engine for LER (English)
# Version: 1.1
#
# Purpose:
#   - Manage the Meta-Memory of Questions (MMP)
#   - Allow proposing experimental question mutations, register tests, and promote to central corpus
#   - Provide a simple GuideReflective (mirror) that returns questions (never solutions)
#   - Lightweight, file-backed prototype suitable for prototyping in Colab / Drive
#
# NOTE:
#   - For concurrent/multi-process usage, prefer a real DB (SQLite/Postgres) or run this as a single service.
#   - This file is intentionally self-contained and dependency-light.

import json
import tempfile
import os
import threading
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime


DEFAULT_SCHEMA = {
    "MMP_VERSION": "1.1",
    "LAST_UPDATE": None,
    "corpus_central": {"preguntas_validadas": []},           # validated questions
    "mutaciones_experimentales": [],                        # experimental mutations
    "metrics": {
        "total_interventions": 0,
        "mutations_proposed": 0,
        "mutations_promoted": 0
    }
}


def _now_iso() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


class AtomicFileWriter:
    """Atomic write helper to avoid corrupting JSON files on crash."""
    @staticmethod
    def write_json_atomic(path: Path, obj: Any) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = None
        try:
            fd, tmp_path = tempfile.mkstemp(dir=str(path.parent), prefix=".tmp_mmp_", text=True)
            tmp = Path(tmp_path)
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(obj, f, indent=2, ensure_ascii=False)
            os.replace(str(tmp), str(path))
        finally:
            if tmp and tmp.exists():
                try:
                    tmp.unlink()
                except Exception:
                    pass


class MMPEngine:
    """
    Core engine that manages the MMP corpus file (JSON).
    This is a file-backed prototype suitable for single-process or low-concurrency usage.
    """

    def __init__(self, corpus_path: str):
        self.corpus_path = Path(corpus_path)
        self._lock = threading.RLock()
        if not self.corpus_path.exists():
            self._init_corpus()
        self._load()

    # ------------------------
    # Internal load/save
    # ------------------------
    def _init_corpus(self) -> None:
        base = DEFAULT_SCHEMA.copy()
        base["LAST_UPDATE"] = _now_iso()
        AtomicFileWriter.write_json_atomic(self.corpus_path, base)

    def _load(self) -> None:
        with self._lock:
            with open(self.corpus_path, "r", encoding="utf-8") as f:
                self._data = json.load(f)

    def _save(self) -> None:
        with self._lock:
            self._data["LAST_UPDATE"] = _now_iso()
            AtomicFileWriter.write_json_atomic(self.corpus_path, self._data)

    # ------------------------
    # Introspection
    # ------------------------
    @property
    def data(self) -> Dict[str, Any]:
        # return a shallow copy to avoid accidental direct modification
        with self._lock:
            return dict(self._data)

    # ------------------------
    # Corpus accessors
    # ------------------------
    def list_validated_questions(self) -> List[Dict[str, Any]]:
        with self._lock:
            return list(self._data["corpus_central"]["preguntas_validadas"])

    def list_experimentals(self) -> List[Dict[str, Any]]:
        with self._lock:
            return list(self._data["mutaciones_experimentales"])

    # ------------------------
    # Propose mutation
    # ------------------------
    def propose_mutation(self, origin_id: str, text: str, proposed_by: str,
                         criteria: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Add a new experimental mutation derived from an existing validated question.
        Returns the mutation record.
        """
        with self._lock:
            idx = len(self._data["mutaciones_experimentales"]) + 1
            mut_id = f"{origin_id}-M{idx}"
            default_criteria = {"min_pruebas": 5, "min_validadores": 3, "umbral_eficacia": 0.8, "periodo_prueba_days": 7}
            m = {
                "id_origen": origin_id,
                "mutacion_id": mut_id,
                "texto": text,
                "propuesto_por": proposed_by,
                "estado": "EXPERIMENTAL",
                "timestamp_propuesta": _now_iso(),
                "metricas": {"pruebas_realizadas": 0, "eficacia_promedio": 0.0, "validadores_unicos": []},
                "criterios_promocion": criteria or default_criteria
            }
            self._data["mutaciones_experimentales"].append(m)
            self._data["metrics"]["mutations_proposed"] += 1
            self._save()
            return m

    # ------------------------
    # Register a test of an experimental mutation
    # ------------------------
    def register_test(self, mutacion_id: str, efficacy: float, validator: str) -> Dict[str, Any]:
        """
        Register a test result for a mutation.
        efficacy: float in [0.0, 1.0] representing relative success (domain-specific).
        validator: entity id that ran/validated this test.
        Returns the updated mutation record.
        """
        with self._lock:
            m = next((x for x in self._data["mutaciones_experimentales"] if x["mutacion_id"] == mutacion_id), None)
            if m is None:
                raise KeyError(f"Mutation {mutacion_id} not found")

            # update metrics
            prev_n = m["metricas"]["pruebas_realizadas"]
            # incremental average for efficacy
            new_n = prev_n + 1
            prev_avg = m["metricas"]["eficacia_promedio"]
            m["metricas"]["eficacia_promedio"] = (prev_avg * prev_n + efficacy) / new_n
            m["metricas"]["pruebas_realizadas"] = new_n

            # unique validators tracking
            validators: List[str] = m["metricas"].get("validadores_unicos", [])
            if validator not in validators:
                validators.append(validator)
            m["metricas"]["validadores_unicos"] = validators

            # check promotion
            promoted = self._maybe_promote(m)
            if promoted:
                self._data["metrics"]["mutations_promoted"] += 1

            # update global counters
            self._data["metrics"]["total_interventions"] += 1
            self._save()
            return m

    def _maybe_promote(self, m: Dict[str, Any]) -> bool:
        """
        Check whether mutation m fulfills promotion criteria.
        If yes, promote to corpus_central and mark state PROMOTED.
        """
        c = m["criterios_promocion"]
        met = m["metricas"]
        n_tests = met["pruebas_realizadas"]
        n_validators = len(met.get("validadores_unicos", []))
        avg_eff = met["eficacia_promedio"]

        if (n_tests >= c["min_pruebas"] and
                n_validators >= c["min_validadores"] and
                avg_eff >= c["umbral_eficacia"]):
            # promote
            promo = {
                "id": m["mutacion_id"],
                "texto": m["texto"],
                "categoria": "mutacion_promovida",
                "validaciones": {
                    "pruebas_superadas": n_tests,
                    "eficacia_promedio": avg_eff,
                    "validadores_unicos": n_validators
                },
                "estado": "VALIDADA",
                "timestamp_promocion": _now_iso(),
                "id_origen": m["id_origen"]
            }
            self._data["corpus_central"]["preguntas_validadas"].append(promo)
            m["estado"] = "PROMOVIDA"
            m["timestamp_promocion"] = _now_iso()
            return True
        return False

    # ------------------------
    # Utilities: add validated question manually
    # ------------------------
    def add_validated_question(self, qid: str, text: str, category: str = "manual", validations: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Add a validated question directly to the central corpus (admin action).
        """
        with self._lock:
            record = {
                "id": qid,
                "texto": text,
                "categoria": category,
                "validaciones": validations or {"pruebas_superadas": 0, "eficacia_promedio": 0.0, "validadores_unicos": 0},
                "estado": "VALIDADA",
                "timestamp_added": _now_iso()
            }
            self._data["corpus_central"]["preguntas_validadas"].append(record)
            self._save()
            return record

    # ------------------------
    # Debug / quick export
    # ------------------------
    def export_snapshot(self, dest_path: str) -> None:
        p = Path(dest_path)
        AtomicFileWriter.write_json_atomic(p, self._data)


# ------------------------
# GuideReflective (mirror)
# ------------------------
class GuideReflective:
    """
    Mirror cognitive guide that returns reflective questions (never direct solutions).
    It uses the MMPEngine corpus to select a question that fits the supplied context.
    """

    def __init__(self, engine: MMPEngine, heuristics: Optional[Dict[str, Any]] = None):
        self.engine = engine
        # heuristics can guide selection (e.g. prefer 'technical' category for technical loops)
        self.heuristics = heuristics or {}

    def _score_question(self, q: Dict[str, Any], context: Dict[str, Any]) -> float:
        """
        Basic heuristic scoring function for questions.
        Higher score means more suitable. This is intentionally simple and replaceable.
        """
        score = 0.0
        # prefer questions with more validations (more reliable)
        val = q.get("validaciones", {})
        score += float(val.get("pruebas_superadas", 0)) * 0.1
        # prefer category match if heuristic provides 'category'
        pref_cat = self.heuristics.get("category")
        if pref_cat and q.get("categoria") == pref_cat:
            score += 1.0
        # small boost for recently promoted (freshness)
        # fallback safe: questions without 'timestamp_promocion' get lower boost
        if q.get("timestamp_promocion"):
            score += 0.2
        return score

    def select_question(self, context: Dict[str, Any]) -> Tuple[str, Optional[str]]:
        """
        Return (question_text, question_id) chosen for the context.
        If none available, returns a default seed question.
        """
        validated = self.engine.list_validated_questions()
        scored: List[Tuple[float, Dict[str, Any]]] = []
        for q in validated:
            s = self._score_question(q, context)
            scored.append((s, q))
        scored.sort(key=lambda x: x[0], reverse=True)

        if scored and scored[0][0] > 0:
            chosen = scored[0][1]
            return chosen["texto"], chosen.get("id")
        # fallback default question (seed)
        fallback = "What implicit assumption might be blocking your view?"
        return fallback, None

    def propose_experimental(self, origin_question_id: str, variation_text: str, proposed_by: str) -> Dict[str, Any]:
        """
        Convenience wrapper to propose an experimental mutation via the engine.
        """
        return self.engine.propose_mutation(origin_question_id, variation_text, proposed_by)


# ------------------------
# MMPAgent: orchestration helper
# ------------------------
class MMPAgent:
    """
    Simple orchestrator that ties loop detection -> mirror_call -> register feedback.
    This class is minimal and intended as an integration helper for entities in LER.
    """

    def __init__(self, corpus_path: str):
        self.engine = MMPEngine(corpus_path)
        self.guide = GuideReflective(self.engine)

    def on_loop_detected(self, entity_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Called when an entity detects it is in a loop.
        Returns a payload with the mirror question and meta-information.
        """
        # choose heuristics from context (optional)
        heuristics = {}
        if "loop_type" in context:
            heuristics["category"] = "mutacion_promovida" if context["loop_type"] == "conceptual" else None
            # we keep simple mapping; production can be richer

        self.guide.heuristics = heuristics
        q_text, q_id = self.guide.select_question(context)

        payload = {
            "mirror_question": q_text,
            "mirror_question_id": q_id,
            "suggested_action": "reflect_and_test",  # explicit guidance vocalized as meta-policy
            "timestamp": _now_iso(),
            "invoked_by": entity_id
        }
        return payload

    def report_test_result(self, mutacion_id: str, efficacy: float, validator_id: str) -> Dict[str, Any]:
        """
        Entity calls this to register the outcome of testing a mutation (or question).
        Returns updated mutation record.
        """
        return self.engine.register_test(mutacion_id, efficacy, validator_id)


# ------------------------
# Example usage (if run directly)
# ------------------------
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="MMP Engine quick demo (file-backed prototype).")
    parser.add_argument("--corpus", type=str, default="./memoria/mmp_corpus.json", help="Path to corpus JSON file.")
    args = parser.parse_args()

    # bootstrap engine and sample flow
    engine = MMPEngine(args.corpus)
    agent = MMPAgent(args.corpus)

    # admin: add a validated question if corpus is empty
    if not engine.list_validated_questions():
        engine.add_validated_question(qid="Q-INIT-001",
                                      text="What assumption are you taking for granted?",
                                      category="suposiciones_ocultas",
                                      validations={"pruebas_superadas": 5, "eficacia_promedio": 0.75, "validadores_unicos": 2})
        print("Added seed validated question.")

    # simulate an entity in loop
    context = {"loop_type": "technical", "note": "repeated syntax->logic confusion"}
    mirror_payload = agent.on_loop_detected(entity_id="pycodex_reflexivo", context=context)
    print("Mirror payload:", json.dumps(mirror_payload, indent=2))

    # simulate proposing an experimental mutation (entity experiments locally)
    mut = agent.engine.propose_mutation(origin_id="Q-INIT-001",
                                        text="What might be different if this apparent constant were actually variable?",
                                        proposed_by="pycodex_reflexivo")
    print("Proposed mutation:", mut["mutacion_id"])

    # simulate registering tests (different validators)
    agent.report_test_result(mut["mutacion_id"], efficacy=0.8, validator_id="auditor_ler")
    agent.report_test_result(mut["mutacion_id"], efficacy=0.9, validator_id="velm")
    agent.report_test_result(mut["mutacion_id"], efficacy=0.85, validator_id="pycodex_reflexivo")
    agent.report_test_result(mut["mutacion_id"], efficacy=0.8, validator_id="external_entity_1")
    agent.report_test_result(mut["mutacion_id"], efficacy=0.82, validator_id="external_entity_2")

    # after tests, inspect corpus
    print("Validated questions:", json.dumps(engine.list_validated_questions(), indent=2))
    print("Experimental mutations:", json.dumps(engine.list_experimentals(), indent=2))
