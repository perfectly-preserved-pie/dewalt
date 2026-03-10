from __future__ import annotations

import json
from pathlib import Path
from typing import Any


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "dewalt_angle_grinders.json"


def load_snapshot(path: Path = DATA_PATH) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(
            f"Missing data snapshot at {path}. Run `python3 -m dewalt.scrape` first."
        )
    return json.loads(path.read_text())


def load_angle_grinders(path: Path = DATA_PATH) -> list[dict[str, Any]]:
    snapshot = load_snapshot(path)
    return snapshot.get("rows", [])
