import json
import threading
import uuid
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional


class DesignLog:
    """
    Singleton class that stores design log entries in a JSON file.
    Provides thread‑safe methods to add, retrieve and export entries.
    """

    _instance: Optional["DesignLog"] = None
    _instance_lock = threading.Lock()

    def __new__(cls, *args: Any, **kwargs: Any) -> "DesignLog":
        # Double‑checked locking to guarantee a single instance even in multithreaded contexts
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, file_path: Optional[Path] = None) -> None:
        """
        Initialise the singleton. Subsequent calls with a different ``file_path`` are ignored
        because the instance already exists.
        """
        # ``__init__`` may be called multiple times due to the singleton pattern;
        # guard against re‑initialisation.
        if getattr(self, "_initialized", False):
            return

        self._lock = threading.RLock()
        self.file_path = Path(file_path) if file_path else Path(__file__).with_name("design_log.json")
        self._entries: List[Dict[str, Any]] = []
        self._load()
        self._initialized = True

    # --------------------------------------------------------------------- #
    # Persistence helpers
    # --------------------------------------------------------------------- #
    def _load(self) -> None:
        """Load entries from the JSON file if it exists."""
        with self._lock:
            if self.file_path.is_file():
                try:
                    with self.file_path.open("r", encoding="utf-8") as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            self._entries = data
                except (json.JSONDecodeError, OSError):
                    # Corrupted file – start with an empty log but keep the file for debugging
                    self._entries = []

    def _save(self) -> None:
        """Write the current entries to the JSON file atomically."""
        with self._lock:
            temp_path = self.file_path.with_suffix(".tmp")
            try:
                with temp_path.open("w", encoding="utf-8") as f:
                    json.dump(self._entries, f, ensure_ascii=False, indent=2)
                temp_path.replace(self.file_path)
            finally:
                if temp_path.is_file():
                    temp_path.unlink(missing_ok=True)

    # --------------------------------------------------------------------- #
    # Public API
    # --------------------------------------------------------------------- #
    def log(self, entry: Dict[str, Any]) -> Dict[str, Any]:
        """
        Alias for :meth:`record`. Returns the stored entry (including generated fields).
        """
        return self.record(entry)

    def record(self, entry: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a new entry to the log.

        The method ensures that each entry has a unique ``id`` and a ``timestamp``.
        The entry is persisted immediately.

        Parameters
        ----------
        entry: dict
            Arbitrary data describing the log entry.

        Returns
        -------
        dict
            The stored entry (including the generated ``id`` and ``timestamp``).
        """
        if not isinstance(entry, dict):
            raise TypeError("entry must be a dictionary")

        with self._lock:
            # Clone to avoid side‑effects on the caller's dict
            stored = dict(entry)

            # Ensure a unique identifier
            stored_id = stored.get("id")
            if stored_id is None:
                stored["id"] = str(uuid.uuid4())
            else:
                # Verify uniqueness; if duplicate, raise
                if any(e.get("id") == stored_id for e in self._entries):
                    raise ValueError(f"An entry with id '{stored_id}' already exists")

            # Add timestamp if not present
            stored.setdefault("timestamp", datetime.utcnow().isoformat() + "Z")

            self._entries.append(stored)
            self._save()
            return stored

    def get_all(self) -> List[Dict[str, Any]]:
        """
        Return a shallow copy of all log entries.

        Returns
        -------
        list[dict]
            List containing all stored entries.
        """
        with self._lock:
            return list(self._entries)

    def find(self, entry_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a single entry by its ``id``.

        Parameters
        ----------
        entry_id: str
            Identifier of the entry to locate.

        Returns
        -------
        dict or None
            The matching entry, or ``None`` if not found.
        """
        with self._lock:
            for entry in self._entries:
                if entry.get("id") == entry_id:
                    return dict(entry)  # Return a copy to protect internal state
            return None

    def export(self, path: Path) -> None:
        """
        Export the current log to an external JSON file.

        Parameters
        ----------
        path: pathlib.Path
            Destination file path. Parent directories are created if necessary.
        """
        export_path = Path(path)
        export_path.parent.mkdir(parents=True, exist_ok=True)

        with self._lock:
            # Write using a temporary file to avoid partial writes
            temp_path = export_path.with_suffix(".tmp")
            try:
                with temp_path.open("w", encoding="utf-8") as f:
                    json.dump(self._entries, f, ensure_ascii=False, indent=2)
                temp_path.replace(export_path)
            finally:
                if temp_path.is_file():
                    temp_path.unlink(missing_ok=True)