from __future__ import annotations

import json
from pathlib import Path
from typing import Any


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "dewalt_angle_grinders.json"


def normalize_power_source(value: str | None) -> str | None:
    """Normalize power source labels from the DEWALT snapshot.

    Args:
        value: Raw power source label from the snapshot.

    Returns:
        The normalized power source label, or ``None`` when the input is ``None``.
    """
    if value == "AC/DC Corded":
        return "Corded"
    return value


def load_snapshot(path: Path = DATA_PATH) -> dict[str, Any]:
    """Load the raw saved grinder snapshot from disk.

    Args:
        path: Filesystem path to the snapshot JSON file.

    Returns:
        The parsed snapshot payload as a dictionary.
    """
    if not path.exists():
        raise FileNotFoundError(
            f"Missing data snapshot at {path}. Run `python3 -m dewalt.scrape` first."
        )
    return json.loads(path.read_text())


def load_angle_grinders(path: Path = DATA_PATH) -> list[dict[str, Any]]:
    """Load normalized grinder rows from the snapshot.

    Args:
        path: Filesystem path to the snapshot JSON file.

    Returns:
        A list of grinder row dictionaries with normalized power source labels.
    """
    snapshot = load_snapshot(path)
    rows = []
    for row in snapshot.get("rows", []):
        normalized_row = dict(row)
        normalized_row["power_source"] = normalize_power_source(row.get("power_source"))
        rows.append(normalized_row)
    return rows
