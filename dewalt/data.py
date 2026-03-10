from __future__ import annotations

import json
from pathlib import Path
from typing import Any


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "dewalt_angle_grinders.json"


def normalize_power_source(value: str | None) -> str | None:
    if value == "AC/DC Corded":
        return "Corded"
    return value


def load_snapshot(path: Path = DATA_PATH) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(
            f"Missing data snapshot at {path}. Run `python3 -m dewalt.scrape` first."
        )
    return json.loads(path.read_text())


def load_angle_grinders(path: Path = DATA_PATH) -> list[dict[str, Any]]:
    snapshot = load_snapshot(path)
    rows = []
    for row in snapshot.get("rows", []):
        normalized_row = dict(row)
        normalized_row["power_source"] = normalize_power_source(row.get("power_source"))
        rows.append(normalized_row)
    return rows
