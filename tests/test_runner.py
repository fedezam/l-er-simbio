import unittest, json
from pathlib import Path

class TestCodeInsightScaffold(unittest.TestCase):
    def test_ghost_has_glyphs(self):
        g = json.loads(Path("ghost.json").read_text(encoding="utf-8"))
        self.assertIn("GLYPHS", g)
        self.assertTrue(len(g["GLYPHS"]["PRIMARY"]) > 0)

    def test_plan_tasks(self):
        p = json.loads(Path("plan.json").read_text(encoding="utf-8"))
        ids = [t["id"] for t in p["TASKS"]]
        for needed in ["audit","translate_to_english","rename_spanish_files","update_references","generate_report"]:
            self.assertIn(needed, ids)

if __name__ == "__main__":
    unittest.main()
