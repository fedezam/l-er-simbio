import json
import os
import uuid
from pathlib import Path
from datetime import datetime

BASE_DIR = Path("./entities")

def save_json(path: Path, data: dict):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def build_entity(skeleton_path: Path, force_rebuild: bool = False):
    with open(skeleton_path, "r", encoding="utf-8") as f:
        skeleton = json.load(f)

    entity_name = skeleton["SEED_NAME"]
    entity_dir = BASE_DIR / entity_name
    if entity_dir.exists():
        if not force_rebuild:
            print(f"❌ Entity '{entity_name}' already exists. Use force_rebuild=True to overwrite.")
            return
        else:
            for item in entity_dir.iterdir():
                if item.is_file():
                    item.unlink()

    entity_dir.mkdir(parents=True, exist_ok=True)

    # UUID
    ghost = skeleton["GHOST"]
    if ghost["identity"]["id"].startswith("UUID-PLACEHOLDER"):
        ghost["identity"]["id"] = str(uuid.uuid4())

    # Timestamps
    skeleton["TIMESTAMP"] = datetime.now().isoformat() + "Z"

    # Save files
    save_json(entity_dir / "ghost.json", ghost)
    save_json(entity_dir / "plan.json", skeleton["PLAN"])
    save_json(entity_dir / "capabilities.json", skeleton["CAPABILITIES"])

    runner_code = f"""# Runner for {entity_name}
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from entity_runner import EntityFactory

def main():
    ghost = Path(__file__).parent / "ghost.json"
    plan = Path(__file__).parent / "plan.json"
    capabilities = Path(__file__).parent / "capabilities.json"

    factory = EntityFactory(ghost, plan, capabilities)
    factory.run()

if __name__ == "__main__":
    main()
"""
    (entity_dir / "runner.py").write_text(runner_code, encoding="utf-8")

    print(f"✅ Entity '{entity_name}' created at {entity_dir}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python entity_builder.py skeleton.json [--force]")
        sys.exit(1)

    skeleton_file = Path(sys.argv[1])
    force = "--force" in sys.argv
    build_entity(skeleton_file, force_rebuild=force)

