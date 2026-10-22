import os
import shutil
from datetime import datetime
from pathlib import Path

class Tools:
    def __init__(self, root_dir="."):
        self.root_dir = Path(root_dir)
        self.snapshots_dir = self.root_dir / "memoria" / "snapshots"
        self.snapshots_dir.mkdir(parents=True, exist_ok=True)

    def read_file(self, path: str) -> str:
        full_path = self.root_dir / path
        if not full_path.exists():
            return f"[ERROR: Archivo no encontrado: {path}]"
        try:
            return full_path.read_text(encoding="utf-8")
        except Exception as e:
            return f"[ERROR leyendo {path}: {e}]"

    def write_file(self, path: str, content: str) -> str:
        """Escribe un archivo en el disco del Codespace."""
        full_path = self.root_dir / path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            if full_path.exists():
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                snapshot = self.snapshots_dir / f"{full_path.name}.{timestamp}.bak"
                shutil.copy(full_path, snapshot)
            full_path.write_text(content, encoding="utf-8")
            return f"[ARCHIVO ESCRITO: {path}] ({len(content)} caracteres)"
        except Exception as e:
            return f"[ERROR escribiendo {path}: {e}]"

    def propose_patch(self, path: str, old_line: str, new_line: str) -> str:
        return f"[PATCH PROPUESTO en {path}]\n- ANTES: {old_line}\n+ DESPUÉS: {new_line}\n[Esperando aprobación de Auditor_LER para aplicar]"

    def apply_patch(self, path: str, old_line: str, new_line: str) -> str:
        full_path = self.root_dir / path
        if not full_path.exists():
            return f"[ERROR: Archivo no encontrado: {path}]"
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            snapshot = self.snapshots_dir / f"{full_path.name}.{timestamp}.bak"
            shutil.copy(full_path, snapshot)
            content = full_path.read_text(encoding="utf-8")
            if old_line not in content:
                return f"[ERROR: Línea no encontrada en {path}. Abortando.]"
            new_content = content.replace(old_line, new_line, 1)
            full_path.write_text(new_content, encoding="utf-8")
            return f"[PATCH APLICADO en {path}]\nSnapshot: {snapshot.name}"
        except Exception as e:
            return f"[ERROR aplicando patch en {path}: {e}]"
