from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from dewalt.data import load_angle_grinders, load_snapshot

from .config import MAX_COMPARE
from .formatting import build_display_rows


@dataclass(frozen=True)
class DashboardContext:
    snapshot: dict[str, Any]
    raw_rows: list[dict[str, Any]]
    angle_grinder_rows: list[dict[str, Any]]
    grid_row_fields: frozenset[str]
    cordless_count: int
    corded_count: int
    brushless_count: int
    max_compare: int = MAX_COMPARE


def load_dashboard_context(
    snapshot: dict[str, Any] | None = None,
    raw_rows: list[dict[str, Any]] | None = None,
    max_compare: int = MAX_COMPARE,
) -> DashboardContext:
    snapshot_data = snapshot or load_snapshot()
    source_rows = raw_rows or load_angle_grinders()
    angle_grinder_rows = build_display_rows(source_rows)

    return DashboardContext(
        snapshot=snapshot_data,
        raw_rows=source_rows,
        angle_grinder_rows=angle_grinder_rows,
        grid_row_fields=frozenset(angle_grinder_rows[0].keys()) if angle_grinder_rows else frozenset(),
        cordless_count=sum(1 for row in angle_grinder_rows if row["power_source"] == "Cordless"),
        corded_count=sum(1 for row in angle_grinder_rows if row["power_source"] != "Cordless"),
        brushless_count=sum(1 for row in angle_grinder_rows if row["brushless"]),
        max_compare=max_compare,
    )
