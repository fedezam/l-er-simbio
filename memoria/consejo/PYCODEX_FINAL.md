# PYCODEX FINAL
Fecha: 2026-10-22 05:40:17

## Código extraído:
```python
"""
core/design_log.py

DesignLog – a thread‑safe singleton that stores design log entries in a JSON file.
"""

from __future__ import annotations

import json
import os
import threading
from typing import Any, Dict, List, Optional


class DesignLog:
    """
    Singleton class responsible for persisting design‑log entries.

    The log is stored in a JSON file (default: ``design_log.json``) and all
    operations are protected by a re‑entrant lock to guarantee thread safety.
    """

    _instance: Optional["DesignLog"] = None
    _instance_lock = threading.Lock()

    # --------------------------------------------------------------------- #
    # Singleton construction
    # --------------------------------------------------------------------- #
    def __new__(cls, *args: Any, **kwargs: Any) -> "DesignLog":
        # Double‑checked locking pattern
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, storage_path: str = "design_log.json") -> None:
        """
        Initialise the singleton.

        Parameters
        ----------
        storage_path: str
            Path to the JSON file used for persistence. Subsequent calls with a
            different path are ignored – the first initialisation wins.
        """
        # ``__init__`` may be called multiple times (because of the singleton
        # pattern). Guard against re‑initialisation.
        if getattr(self, "_initialized", False):
            return

        self._storage_path = storage_path
        self._lock = threading.RLock()
        self._entries: List[Dict[str, Any]] = []

        self._load()
        self._initialized = True

    # --------------------------------------------------------------------- #
    # Persistence helpers
    # --------------------------------------------------------------------- #
    def _load(self) -> None:
        """Load entries from the JSON storage file, if it exists."""
        if not os.path.isfile(self._storage_path):
            return

        try:
            with open(self._storage_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    self._entries = data
        except (json.JSONDecodeError, OSError):
            # Corrupted or unreadable file – start with an empty log.
            self._entries = []

    def _dump(self) -> None:
        """Write the current entries list to the JSON storage file."""
        tmp_path = f"{self._storage_path}.tmp"
        try:
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(self._entries, f, ensure_ascii=False, indent=2)
            os.replace(tmp_path, self._storage_path)
        finally:
            # Ensure temporary file does not linger on failure.
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except OSError:
                    pass

    # --------------------------------------------------------------------- #
    # Public API
    # --------------------------------------------------------------------- #
    def log(self, entry: Dict[str, Any]) -> None:
        """
        Add a new entry to the log and persist it.

        Parameters
        ----------
        entry: dict
            A dictionary representing the log entry. It must contain an ``id``
            key that uniquely identifies the entry.
        """
        self.record(entry)

    def record(self, entry: Dict[str, Any]) -> None:
        """
        Alias for :meth:`log`. Provided for semantic clarity in the code base.

        The method validates that the entry contains an ``id`` field and that
        the identifier is not already present in the log.
        """
        if "id" not in entry:
            raise ValueError("Log entry must contain an 'id' field.")

        with self._lock:
            if any(e["id"] == entry["id"] for e in self._entries):
                raise ValueError(f"An entry with id '{entry['id']}' already exists.")
            self._entries.append(entry)
            self._dump()

    def get_all(self) -> List[Dict[str, Any]]:
        """
        Return a shallow copy of all log entries.

        Returns
        -------
        list[dict]
            List of stored entries.
        """
        with self._lock:
            return list(self._entries)

    def find(self, entry_id: Any) -> Optional[Dict[str, Any]]:
        """
        Retrieve a single entry by its ``id``.

        Parameters
        ----------
        entry_id: Any
            The identifier of the entry to locate.

        Returns
        -------
        dict | None
            The matching entry, or ``None`` if not found.
        """
        with self._lock:
            for entry in self._entries:
                if entry.get("id") == entry_id:
                    return entry
        return None

    def export(self, path: str) -> None:
        """
        Export the entire log to an external JSON file.

        Parameters
        ----------
        path: str
            Destination file path. The export operation does **not** modify the
            internal storage file.
        """
        with self._lock:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(self._entries, f, ensure_ascii=False, indent=2)
            except OSError as exc:
                raise IOError(f"Unable to export design log to '{path}': {exc}") from exc
```