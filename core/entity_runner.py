import os
import json
import logging
import shutil
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Tuple


# ---------- Utilidades ----------

def load_json(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path: Path, data: Dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def snapshot_file(file_path: Path, backup_dir: Path) -> Optional[Path]:
    """Crea snapshot del archivo en backup_dir con hash y timestamp."""
    if not file_path.exists():
        return None

    backup_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    hash_digest = hashlib.md5(file_path.read_bytes()).hexdigest()[:8]
    snapshot_name = f"{file_path.stem}_{timestamp}_{hash_digest}{file_path.suffix}"
    snapshot_path = backup_dir / snapshot_name

    shutil.copy(file_path, snapshot_path)
    return snapshot_path

def verify_python_syntax(file_path: Path) -> Tuple[bool, str]:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            compile(f.read(), str(file_path), "exec")
        return True, "OK"
    except SyntaxError as e:
        return False, f"SyntaxError: {e}"
    except Exception as e:
        return False, str(e)


# ---------- Entity Factory ----------

class EntityFactory:
    def __init__(self, ghost_path: Path, plan_path: Path, capabilities_path: Path, strategy_path: Path):
        self.ghost = load_json(ghost_path)
        self.plan = load_json(plan_path)
        self.capabilities_config = load_json(capabilities_path)
        self.strategy_code = strategy_path.read_text(encoding="utf-8") if strategy_path.exists() else None

        self.logger = self.setup_logger()
        self.active_capabilities = {}
        self.setup_capabilities()

    def setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("EntityRunner")
        logger.setLevel(logging.DEBUG)
        if not logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
            logger.addHandler(handler)
        return logger

    def setup_capabilities(self) -> None:
        required = self.capabilities_config.get("required_capabilities", [])
        config = self.capabilities_config.get("capability_config", {})
        for cap in required:
            self.active_capabilities[cap] = config.get(cap, {})
        self.logger.info(f"Capacidades activadas: {list(self.active_capabilities.keys())}")

    def has_capability(self, name: str) -> bool:
        return name in self.active_capabilities

    def get_capability(self, name: str) -> Dict[str, Any]:
        return self.active_capabilities.get(name, {})

    def create_file_snapshot(self, file_path: Path) -> None:
        if self.has_capability("file_snapshots") and file_path.exists():
            config = self.get_capability("file_snapshots")
            backup_dir = Path(config.get("backup_dir", "snapshots"))
            snapshot = snapshot_file(file_path, backup_dir)
            if snapshot:
                self.logger.info(f"Snapshot creado: {snapshot.name}")

    def verify_syntax(self, file_path: Path) -> Tuple[bool, str]:
        if file_path.suffix == ".py":
            return verify_python_syntax(file_path)
        elif file_path.suffix == ".json":
            try:
                load_json(file_path)
                return True, "JSON válido"
            except Exception as e:
                return False, str(e)
        return True, "Sin verificación"

    def run(self) -> None:
        self.logger.info(f"Ejecutando entidad: {self.ghost.get('SEED_NAME', 'Unnamed')}")
        for step in self.plan.get("steps", []):
            action = step.get("action")
            target = step.get("target")

            if action == "audit" and target:
                path = Path(target)
                if path.exists():
                    if path.is_file():
                        self.create_file_snapshot(path)
                        valid, msg = self.verify_syntax(path)
                        self.logger.info(f"{path}: {msg}")
                    else:
                        for file in path.glob("**/*"):
                            if file.is_file():
                                self.create_file_snapshot(file)
                                valid, msg = self.verify_syntax(file)
                                self.logger.info(f"{file}: {msg}")
        self.logger.info("Ejecución completada.")


# ---------- Main Runner ----------

def main():
    base = Path(__file__).parent

    ghost = base / "ghost.json"
    plan = base / "plan.json"
    capabilities = base / "capabilities.json"
    strategy = base / "strategy.py"

    if not all(p.exists() for p in [ghost, plan, capabilities]):
        raise FileNotFoundError("Faltan ghost.json, plan.json o capabilities.json")

    factory = EntityFactory(ghost, plan, capabilities, strategy)
    factory.run()


if __name__ == "__main__":
    main()
