# core/glossary_loader.py
"""
LER / Mathema v4.0 Universal Glossary
-------------------------------------

This module centralizes the loading of glyphs from official JSON files.
If the file is not found, it uses an empty fallback to keep the engine running.

Exposes:
    - MATHEMA_GLOSSARY: instance of GlosarioMathema
    - GLYPHS: dictionary of universal glyphs
    - SECURITY: dictionary of security glyphs
"""

import json
import os


class MathemaGlossary:
    def __init__(self, json_path: str = None):
        if json_path:
            self.json_path = json_path
        else:
            self.json_path = self._find_glyph_file()

        self.glossary = None
        self.load_glossary()

    def _find_glyph_file(self) -> str:
        base_path = os.path.dirname(os.path.abspath(__file__))
        possible_paths = [
            os.path.join(base_path, "../glyphs/universal_glyphs.json"),
            os.path.join(base_path, "glyphs/universal_glyphs.json"),
            "/content/drive/MyDrive/LER/glyphs/universal_glyphs.json",
            "/content/drive/MyDrive/LER/core/glyphs/universal_glyphs.json",
            os.path.join(base_path, "../../glyphs/universal_glyphs.json"),
            os.path.join(base_path, "universal_glyphs.json"),
        ]

        for path in possible_paths:
            if os.path.exists(path):
                print(f"INFO - Glyphs found at: {path}")
                return path

        print("WARNING - universal_glyphs.json not found in known locations")
        print(f"INFO - Using default path: {os.path.join(base_path, 'glyphs/universal_glyphs.json')}")
        return os.path.join(base_path, "glyphs/universal_glyphs.json")

    def load_glossary(self) -> None:
        try:
            if not os.path.exists(self.json_path):
                raise FileNotFoundError(f"File not found: {self.json_path}")

            with open(self.json_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                self.glossary = json.loads(content)

            if 'GLOSSARY' not in self.glossary:
                raise KeyError("The file does not contain the key 'GLOSSARY'")

            glyphs_count = len(self.glossary['GLOSSARY'])
            print(f"INFO - MathemaGlossary active: True")
            print(f"INFO - Universal glyphs loaded: {glyphs_count}")

        except Exception as e:
            print(f"ERROR - Error loading glyphs: {e}")
            self.glossary = {'GLOSSARY': {}, 'security_glyphs': {}}

    def __getitem__(self, key: str) -> dict:
        if not self.glossary or 'GLOSSARY' not in self.glossary:
            raise KeyError("Glossary not properly loaded")

        if key not in self.glossary['GLOSSARY']:
            raise KeyError(f"Glyph '{key}' not found in glossary")

        return self.glossary['GLOSSARY'][key]

    def get(self, key: str, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def list_glyphs(self) -> list:
        if not self.glossary or 'GLOSSARY' not in self.glossary:
            return []
        return list(self.glossary['GLOSSARY'].keys())

    def get_statistics(self) -> dict:
        if not self.glossary:
            return {"error": "Glossary not loaded"}

        return {
            "file": self.json_path,
            "universal_glyphs": len(self.glossary.get('GLOSSARY', {})),
            "reflexive_glyphs": len(self.glossary.get('reflexive_glyphs', {})),
            "system_glyphs": len(self.glossary.get('system_glyphs', {})),
            "interaction_glyphs": len(self.glossary.get('interaction_glyphs', {})),
            "mathema_operators": len(self.glossary.get('MATHEMA_OPERATORS', {})),
            "security_glyphs": len(self.glossary.get('security_glyphs', {})),
        }


# === Global initialization ===
try:
    MATHEMA_GLOSSARY = MathemaGlossary()
    print("INFO - GlyphEngine active: True")
except Exception as e:
    print(f"CRITICAL - Error initializing MathemaGlossary: {e}")
    MATHEMA_GLOSSARY = MathemaGlossary("dummy_path")

# === Compatibility aliases for parser/visitor ===
GLYPHS = MATHEMA_GLOSSARY.glossary.get("GLOSSARY", {})
SECURITY = MATHEMA_GLOSSARY.glossary.get("security_glyphs", {})


# Convenience function
def get_glossary_info():
    return MATHEMA_GLOSSARY.get_statistics()
