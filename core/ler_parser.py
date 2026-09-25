# ler_parser.py
"""
LER Symbolic Analysis Module
Interprets glyphs, evaluates symbolic meaning, and converts entities into tree-like structures.
Includes pattern analysis, symbolic relationships, and graph generation.
"""

import json
import logging
from collections import defaultdict
from enum import Enum
from typing import Dict, List, Any, Optional, Set

from core.config import get_config  # usa el config centralizado

# Configure logging
logger = logging.getLogger(__name__)

class GlyphType(Enum):
    """Types of glyphs according to their symbolic function."""
    PRIMARY_KEY = "primary_key"
    DIGITAL_SIGNATURE = "digital_signature"
    CONTAINER = "container"
    CHANGE = "change"
    RECONFIGURATION = "reconfiguration"
    BRIDGE = "bridge"
    UNKNOWN = "unknown"

class LERParser:
    """Main parser for LER symbolic structures."""

    def __init__(self):
        cfg = get_config()
        universal_path = cfg.glyphs_path / "universal_glyphs.json"
        mmp_path = cfg.glyphs_path / "mmp_core.json"

        # Load glyphs
        for path in (universal_path, mmp_path):
            if not path.exists():
                raise FileNotFoundError(f"Glyph file not found: {path}")

        with open(universal_path, 'r', encoding='utf-8') as f:
            self.glyphs = json.load(f)

        with open(mmp_path, 'r', encoding='utf-8') as f:
            mmp_data = json.load(f)
        for key, val in mmp_data.get("MMP_GLYPHS", {}).items():
            glyph_symbol = val["glyph"]
            self.glyphs[glyph_symbol] = {
                "description": val.get("name", "MMP Glyph"),
                "category": "MMP",
                "level": 1
            }

        self.glyph_types = GlyphType

    def identify_glyph_type(self, glyph: str) -> GlyphType:
        """Determine the type of a glyph based on glossary information."""
        info = self.glyphs.get(glyph)
        if not info:
            return GlyphType.UNKNOWN
        type_str = info.get("type", "unknown")
        try:
            return GlyphType(type_str)
        except ValueError:
            return GlyphType.UNKNOWN

    def parse_entity(self, entity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Converts an entity dictionary into a structured tree representation."""
        tree = {}
        for key, value in entity_data.items():
            if isinstance(value, list):
                tree[key] = [self.parse_entity(v) if isinstance(v, dict) else v for v in value]
            elif isinstance(value, dict):
                tree[key] = self.parse_entity(value)
            else:
                tree[key] = value
        return tree

    def extract_patterns(self, text: str) -> List[str]:
        """Simple pattern extraction from a string of glyphs."""
        return [glyph for glyph in text if glyph in self.glyphs]

    def generate_graph(self, entity_tree: Dict[str, Any]) -> Dict[str, Set[str]]:
        """Generates a simple adjacency graph from the entity tree."""
        graph = defaultdict(set)

        def _recurse(node: Any, parent: Optional[str] = None):
            if isinstance(node, dict):
                for key, value in node.items():
                    if parent:
                        graph[parent].add(key)
                    _recurse(value, key)
            elif isinstance(node, list):
                for idx, item in enumerate(node):
                    node_name = f"{parent}_{idx}" if parent else str(idx)
                    if parent:
                        graph[parent].add(node_name)
                    _recurse(item, node_name)

        _recurse(entity_tree)
        return graph


# --- Test mode ---
if __name__ == "__main__":
    parser = LERParser()

    sample_entity = {
        "id": "entity_001",
        "components": [
            {"type": "GLA", "value": "◌"},
            {"type": "GLB", "value": "◑"}
        ],
        "metadata": {"author": "AXIOMA"}
    }

    tree = parser.parse_entity(sample_entity)
    graph = parser.generate_graph(tree)

    print("Parsed entity tree:")
    print(tree)
    print("\nGenerated adjacency graph:")
    print(dict(graph))
