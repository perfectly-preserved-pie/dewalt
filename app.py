from __future__ import annotations

from dash import Dash
import dash_bootstrap_components as dbc

from dewalt.ui import (
    build_compare_base_columns,
    build_compare_columns,
    build_compare_grid,
    build_compare_rows,
    build_layout,
    build_master_column_defs,
    build_master_grid,
    build_modal,
    load_dashboard_context,
    register_callbacks,
)


DASHBOARD = load_dashboard_context()
SNAPSHOT = DASHBOARD.snapshot
RAW_ROWS = DASHBOARD.raw_rows
ANGLE_GRINDER_ROWS = DASHBOARD.angle_grinder_rows
GRID_ROW_FIELDS = DASHBOARD.grid_row_fields
MAX_COMPARE = DASHBOARD.max_compare
CORDLESS_COUNT = DASHBOARD.cordless_count
CORDED_COUNT = DASHBOARD.corded_count
BRUSHLESS_COUNT = DASHBOARD.brushless_count

MASTER_COLUMN_DEFS = build_master_column_defs()
COMPARE_BASE_COLUMNS = build_compare_base_columns()
MASTER_GRID = build_master_grid(ANGLE_GRINDER_ROWS, MASTER_COLUMN_DEFS)
COMPARE_GRID = build_compare_grid(COMPARE_BASE_COLUMNS)
MODAL = build_modal()

app = Dash(
    __name__,
    title="DEWALT Compare",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)

app.layout = build_layout(DASHBOARD, MASTER_GRID, COMPARE_GRID, MODAL)
register_callbacks(app, DASHBOARD)


if __name__ == "__main__":
    app.run(debug=True)
