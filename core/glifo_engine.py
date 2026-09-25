# glifo_engine.py
import json
from pathlib import Path
from core.config import get_config  # <- usa tu config.py centralizado

class GlyphEngine:
    """
    Symbolic engine for LER.
    Depends on universal glyphs + MMP glyphs defined in config.
    """

    def __init__(self):
        cfg = get_config()
        self.universal_path = cfg.glyphs_path / "universal_glyphs.json"
        self.mmp_path = cfg.glyphs_path / "mmp_core.json"

        # Mathema operators
        self.operators = {
            "+": "Symbolic sum / Fusion",
            "⊗": "Tensor product / Interaction",
            "¬": "Negation / Inversion",
            "Δ": "Transformation / Delta",
            "∞": "Infinity / Continuity",
            "→": "Implication / Directional flow",
            "⇆": "Bidirectional equivalence",
            "∘": "Functional composition",
            "·": "Dot product / Resonance"
        }

        # Load glyphs
        for path in (self.universal_path, self.mmp_path):
            if not path.exists():
                raise FileNotFoundError(f"Glyph file not found: {path}")

        with open(self.universal_path, "r", encoding="utf-8") as f:
            universal = json.load(f)

        with open(self.mmp_path, "r", encoding="utf-8") as f:
            mmp_data = json.load(f)

        # Merge universal + MMP glyphs
        self.glyphs = universal
        for key, val in mmp_data.get("MMP_GLYPHS", {}).items():
            glyph_symbol = val["glyph"]
            self.glyphs[glyph_symbol] = {
                "description": val.get("name", "MMP Glyph"),
                "category": "MMP",
                "level": 1
            }

    def is_valid_glyph(self, symbol: str) -> bool:
        return symbol in self.glyphs or symbol in self.operators

    def glyph_description(self, symbol: str) -> str:
        if symbol in self.glyphs:
            data = self.glyphs[symbol]
            category = data.get("category", "general")
            level = data.get("level", 0)
            return f"{data['description']} [{category.title()}, Level {level}]"
        if symbol in self.operators:
            return f"Mathema Operator: {self.operators[symbol]}"
        return f"Unrecognized symbol: '{symbol}'"

    def validate_expression(self, expression: str):
        parts = expression.split()
        errors = [f"Position {i+1}: '{s}' is not valid" for i, s in enumerate(parts) if not self.is_valid_glyph(s)]
        return len(errors) == 0, errors

    def represent_expression(self, expression: str) -> str:
        parts = expression.split()
        if not parts:
            return "Empty expression"

        is_valid, errors = self.validate_expression(expression)
        result = [f"Mathema Expression: {expression}", "="*50]

        if not is_valid:
            result.append("VALIDATION ERRORS:")
            result.extend(f"  {e}" for e in errors)
            result.append("="*50)

        for i, symbol in enumerate(parts, 1):
            result.append(f"{i:2d}. {symbol} → {self.glyph_description(symbol)}")

        return "\n".join(result)

    def analyze_flow(self, expression: str):
        parts = expression.split()
        if len(parts) < 2:
            return "Expression too short for flow analysis"

        result = ["SYMBOLIC FLOW ANALYSIS", "="*40]
        for i, symbol in enumerate(parts, 1):
            if symbol in self.operators:
                result.append(f"{i:2d}. Operator → {self.operators[symbol]}")
            elif symbol in self.glyphs:
                result.append(f"{i:2d}. Glyph → {symbol}")
            else:
                result.append(f"{i:2d}. Unknown → {symbol}")

        return "\n".join(result)

    def get_statistics(self) -> str:
        total_glyphs = len(self.glyphs)
        total_operators = len(self.operators)

        categories = {}
        for data in self.glyphs.values():
            cat = data.get("category", "no_category")
            categories[cat] = categories.get(cat, 0) + 1

        result = [
            "GLYPH ENGINE STATISTICS",
            "="*40,
            f"Total glyphs loaded: {total_glyphs}",
            f"Total operators: {total_operators}",
            "",
            "Distribution by categories:"
        ]
        for cat, count in categories.items():
            result.append(f"  {cat.title()}: {count}")

        return "\n".join(result)


# --- Test mode ---
if __name__ == "__main__":
    engine = GlyphEngine()
    test_expression = "◌ → ◰ ⊗ ○"
    print(engine.get_statistics())
    print(engine.represent_expression(test_expression))
    print(engine.analyze_flow(test_expression))
