from __future__ import annotations

from dash import Dash
import dash_bootstrap_components as dbc

from dewalt.tool_families import ANGLE_GRINDER_FAMILY
from dewalt.ui import (
    build_compare_base_columns,
    build_compare_grid,
    build_layout,
    build_master_grid,
    build_modal,
    load_dashboard_context,
    register_callbacks,
)


FAMILY = ANGLE_GRINDER_FAMILY
DASHBOARD = load_dashboard_context(FAMILY)
SNAPSHOT = DASHBOARD.snapshot
RAW_ROWS = DASHBOARD.raw_rows
DISPLAY_ROWS = DASHBOARD.display_rows
ANGLE_GRINDER_ROWS = DASHBOARD.display_rows
GRID_ROW_FIELDS = DASHBOARD.grid_row_fields
MAX_COMPARE = DASHBOARD.max_compare

CORDLESS_COUNT = sum(1 for row in DISPLAY_ROWS if row["power_source"] == "Cordless")
CORDED_COUNT = sum(1 for row in DISPLAY_ROWS if row["power_source"] != "Cordless")
BRUSHLESS_COUNT = sum(1 for row in DISPLAY_ROWS if row["brushless"])

MASTER_COLUMN_DEFS = FAMILY.build_master_column_defs()
COMPARE_BASE_COLUMNS = build_compare_base_columns()
MASTER_GRID = build_master_grid(DISPLAY_ROWS, MASTER_COLUMN_DEFS, FAMILY.ids)
COMPARE_GRID = build_compare_grid(FAMILY.ids, COMPARE_BASE_COLUMNS)
MODAL = build_modal(FAMILY.ids)

app = Dash(
    __name__,
    title="DEWALT Compare",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)

app.layout = build_layout(DASHBOARD, MASTER_GRID, COMPARE_GRID, MODAL)
register_callbacks(app, DASHBOARD)


if __name__ == "__main__":
    app.run(debug=True)
