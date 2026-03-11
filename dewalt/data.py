from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ANGLE_GRINDER_DATA_PATH = (
    Path(__file__).resolve().parents[1] / "data" / "dewalt_angle_grinders.json"
)
DRILL_DRIVER_DATA_PATH = (
    Path(__file__).resolve().parents[1] / "data" / "dewalt_drill_drivers.json"
)
HAMMER_DRILL_DATA_PATH = (
    Path(__file__).resolve().parents[1] / "data" / "dewalt_hammer_drills.json"
)
IMPACT_DRIVER_DATA_PATH = (
    Path(__file__).resolve().parents[1] / "data" / "dewalt_impact_drivers.json"
)
IMPACT_WRENCH_DATA_PATH = (
    Path(__file__).resolve().parents[1] / "data" / "dewalt_impact_wrenches.json"
)
OSCILLATING_MULTI_TOOL_DATA_PATH = (
    Path(__file__).resolve().parents[1] / "data" / "dewalt_oscillating_multi_tools.json"
)
RATCHET_DATA_PATH = (
    Path(__file__).resolve().parents[1] / "data" / "dewalt_ratchets.json"
)
ROTARY_HAMMER_DATA_PATH = (
    Path(__file__).resolve().parents[1] / "data" / "dewalt_rotary_hammers.json"
)


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


def load_snapshot(path: Path = ANGLE_GRINDER_DATA_PATH) -> dict[str, Any]:
    """Load a raw saved DEWALT snapshot from disk.

    Args:
        path: Filesystem path to the snapshot JSON file.

    Returns:
        The parsed snapshot payload as a dictionary.
    """
    if not path.exists():
        raise FileNotFoundError(f"Missing data snapshot at {path}.")
    return json.loads(path.read_text())


def load_angle_grinder_snapshot(path: Path = ANGLE_GRINDER_DATA_PATH) -> dict[str, Any]:
    """Load the saved angle-grinder snapshot from disk.

    Args:
        path: Filesystem path to the grinder snapshot JSON file.

    Returns:
        The parsed grinder snapshot payload as a dictionary.
    """
    return load_snapshot(path)


def load_angle_grinders(path: Path = ANGLE_GRINDER_DATA_PATH) -> list[dict[str, Any]]:
    """Load normalized grinder rows from the snapshot.

    Args:
        path: Filesystem path to the snapshot JSON file.

    Returns:
        A list of grinder row dictionaries with normalized power source labels.
    """
    snapshot = load_angle_grinder_snapshot(path)
    rows = []
    for row in snapshot.get("rows", []):
        normalized_row = dict(row)
        normalized_row["power_source"] = normalize_power_source(row.get("power_source"))
        rows.append(normalized_row)
    return rows


def load_drill_driver_snapshot(path: Path = DRILL_DRIVER_DATA_PATH) -> dict[str, Any]:
    """Load the saved drill-driver snapshot from disk.

    Args:
        path: Filesystem path to the drill-driver snapshot JSON file.

    Returns:
        The parsed drill-driver snapshot payload as a dictionary.
    """
    return load_snapshot(path)


def load_drill_drivers(path: Path = DRILL_DRIVER_DATA_PATH) -> list[dict[str, Any]]:
    """Load normalized drill-driver rows from the snapshot.

    Args:
        path: Filesystem path to the snapshot JSON file.

    Returns:
        A list of drill-driver row dictionaries with normalized power source labels.
    """
    snapshot = load_drill_driver_snapshot(path)
    rows = []
    for row in snapshot.get("rows", []):
        normalized_row = dict(row)
        normalized_row["power_source"] = normalize_power_source(row.get("power_source"))
        rows.append(normalized_row)
    return rows


def load_hammer_drill_snapshot(path: Path = HAMMER_DRILL_DATA_PATH) -> dict[str, Any]:
    """Load the saved hammer-drill snapshot from disk.

    Args:
        path: Filesystem path to the hammer-drill snapshot JSON file.

    Returns:
        The parsed hammer-drill snapshot payload as a dictionary.
    """
    return load_snapshot(path)


def load_hammer_drills(path: Path = HAMMER_DRILL_DATA_PATH) -> list[dict[str, Any]]:
    """Load normalized hammer-drill rows from the snapshot.

    Args:
        path: Filesystem path to the snapshot JSON file.

    Returns:
        A list of hammer-drill row dictionaries with normalized power source labels.
    """
    snapshot = load_hammer_drill_snapshot(path)
    rows = []
    for row in snapshot.get("rows", []):
        normalized_row = dict(row)
        normalized_row["power_source"] = normalize_power_source(row.get("power_source"))
        rows.append(normalized_row)
    return rows


def load_impact_driver_snapshot(path: Path = IMPACT_DRIVER_DATA_PATH) -> dict[str, Any]:
    """Load the saved impact-driver snapshot from disk.

    Args:
        path: Filesystem path to the impact-driver snapshot JSON file.

    Returns:
        The parsed impact-driver snapshot payload as a dictionary.
    """
    return load_snapshot(path)


def load_impact_drivers(path: Path = IMPACT_DRIVER_DATA_PATH) -> list[dict[str, Any]]:
    """Load normalized impact-driver rows from the snapshot.

    Args:
        path: Filesystem path to the snapshot JSON file.

    Returns:
        A list of impact-driver row dictionaries with normalized power-source labels.
    """
    snapshot = load_impact_driver_snapshot(path)
    rows = []
    for row in snapshot.get("rows", []):
        normalized_row = dict(row)
        normalized_row["power_source"] = normalize_power_source(row.get("power_source"))
        rows.append(normalized_row)
    return rows


def load_impact_wrench_snapshot(path: Path = IMPACT_WRENCH_DATA_PATH) -> dict[str, Any]:
    """Load the saved impact-wrench snapshot from disk.

    Args:
        path: Filesystem path to the impact-wrench snapshot JSON file.

    Returns:
        The parsed impact-wrench snapshot payload as a dictionary.
    """
    return load_snapshot(path)


def load_impact_wrenches(path: Path = IMPACT_WRENCH_DATA_PATH) -> list[dict[str, Any]]:
    """Load normalized impact-wrench rows from the snapshot.

    Args:
        path: Filesystem path to the snapshot JSON file.

    Returns:
        A list of impact-wrench row dictionaries with normalized power-source labels.
    """
    snapshot = load_impact_wrench_snapshot(path)
    rows = []
    for row in snapshot.get("rows", []):
        normalized_row = dict(row)
        normalized_row["power_source"] = normalize_power_source(row.get("power_source"))
        rows.append(normalized_row)
    return rows


def load_oscillating_multi_tool_snapshot(
    path: Path = OSCILLATING_MULTI_TOOL_DATA_PATH,
) -> dict[str, Any]:
    """Load the saved oscillating multi-tool snapshot from disk.

    Args:
        path: Filesystem path to the oscillating multi-tool snapshot JSON file.

    Returns:
        The parsed oscillating multi-tool snapshot payload as a dictionary.
    """
    return load_snapshot(path)


def load_oscillating_multi_tools(
    path: Path = OSCILLATING_MULTI_TOOL_DATA_PATH,
) -> list[dict[str, Any]]:
    """Load normalized oscillating multi-tool rows from the snapshot.

    Args:
        path: Filesystem path to the snapshot JSON file.

    Returns:
        A list of oscillating multi-tool row dictionaries with normalized power-source
        labels.
    """
    snapshot = load_oscillating_multi_tool_snapshot(path)
    rows = []
    for row in snapshot.get("rows", []):
        normalized_row = dict(row)
        normalized_row["power_source"] = normalize_power_source(row.get("power_source"))
        rows.append(normalized_row)
    return rows


def load_ratchet_snapshot(path: Path = RATCHET_DATA_PATH) -> dict[str, Any]:
    """Load the saved ratchet snapshot from disk.

    Args:
        path: Filesystem path to the ratchet snapshot JSON file.

    Returns:
        The parsed ratchet snapshot payload as a dictionary.
    """
    return load_snapshot(path)


def load_ratchets(path: Path = RATCHET_DATA_PATH) -> list[dict[str, Any]]:
    """Load normalized ratchet rows from the snapshot.

    Args:
        path: Filesystem path to the snapshot JSON file.

    Returns:
        A list of ratchet row dictionaries with normalized power-source labels.
    """
    snapshot = load_ratchet_snapshot(path)
    rows = []
    for row in snapshot.get("rows", []):
        normalized_row = dict(row)
        normalized_row["power_source"] = normalize_power_source(row.get("power_source"))
        rows.append(normalized_row)
    return rows


def load_rotary_hammer_snapshot(path: Path = ROTARY_HAMMER_DATA_PATH) -> dict[str, Any]:
    """Load the saved rotary-hammer snapshot from disk.

    Args:
        path: Filesystem path to the rotary-hammer snapshot JSON file.

    Returns:
        The parsed rotary-hammer snapshot payload as a dictionary.
    """
    return load_snapshot(path)


def load_rotary_hammers(path: Path = ROTARY_HAMMER_DATA_PATH) -> list[dict[str, Any]]:
    """Load normalized rotary-hammer rows from the snapshot.

    Args:
        path: Filesystem path to the snapshot JSON file.

    Returns:
        A list of rotary-hammer row dictionaries with normalized power-source labels.
    """
    snapshot = load_rotary_hammer_snapshot(path)
    rows = []
    for row in snapshot.get("rows", []):
        normalized_row = dict(row)
        normalized_row["power_source"] = normalize_power_source(row.get("power_source"))
        rows.append(normalized_row)
    return rows
