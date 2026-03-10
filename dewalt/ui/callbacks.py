from __future__ import annotations

from dash import Dash, Input, Output, State, callback_context, html, no_update
from dash.exceptions import PreventUpdate

from .context import DashboardContext
from .grids import build_compare_base_columns, build_compare_columns, build_compare_rows
from .modal import build_modal_content, build_modal_header


def register_callbacks(app: Dash, context: DashboardContext) -> None:
    @app.callback(
        Output("selection-summary", "children"),
        Input("angle-grinders-grid", "virtualRowData"),
        Input("angle-grinders-grid", "selectedRows"),
    )
    def update_selection_summary(
        visible_rows: list[dict] | None, selected_rows: list[dict] | None
    ) -> list[html.Span]:
        visible_count = (
            len(visible_rows)
            if visible_rows is not None
            else len(context.angle_grinder_rows)
        )
        selected_count = len(selected_rows or [])
        return [
            html.Span(f"{visible_count} visible", className="summary-pill"),
            html.Span(f"{selected_count} selected", className="summary-pill"),
            html.Span(
                f"{context.max_compare} max compare",
                className="summary-pill summary-pill-accent",
            ),
        ]

    @app.callback(
        Output("compare-note", "children"),
        Output("compare-grid", "rowData"),
        Output("compare-grid", "columnDefs"),
        Input("angle-grinders-grid", "selectedRows"),
    )
    def update_compare_grid(
        selected_rows: list[dict] | None,
    ) -> tuple[str, list[dict], list[dict]]:
        rows = selected_rows or []
        if not rows:
            return (
                "No grinders selected yet. Use the checkboxes in the master table to build a comparison.",
                [],
                build_compare_base_columns(),
            )

        note = f"Comparing {min(len(rows), context.max_compare)} grinder(s)."
        if len(rows) > context.max_compare:
            note += f" Showing the first {context.max_compare} selected rows."

        compare_rows = rows[: context.max_compare]
        return (
            note,
            build_compare_rows(compare_rows),
            build_compare_columns(compare_rows),
        )

    @app.callback(
        Output("grinder-modal", "is_open"),
        Output("grinder-modal-header", "children"),
        Output("grinder-modal-content", "children"),
        Input("angle-grinders-grid", "cellClicked"),
        Input("grinder-modal-close", "n_clicks"),
        State("grinder-modal", "is_open"),
        State("angle-grinders-grid", "virtualRowData"),
        prevent_initial_call=True,
    )
    def open_grinder_modal(
        cell_clicked_data: dict | None,
        close_clicks: int | None,
        is_open: bool,
        virtual_row_data: list[dict] | None,
    ) -> tuple[bool, object, object]:
        ctx = callback_context
        if not ctx.triggered:
            raise PreventUpdate

        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if trigger_id == "grinder-modal-close":
            return False, no_update, no_update

        if trigger_id != "angle-grinders-grid" or not cell_clicked_data:
            raise PreventUpdate

        if cell_clicked_data.get("colId") not in context.grid_row_fields:
            raise PreventUpdate

        selected_row = cell_clicked_data.get("data")
        row_index = cell_clicked_data.get("rowIndex")
        if (
            selected_row is None
            and isinstance(row_index, int)
            and virtual_row_data
            and 0 <= row_index < len(virtual_row_data)
        ):
            selected_row = virtual_row_data[row_index]

        if not selected_row:
            raise PreventUpdate

        return True, build_modal_header(selected_row), build_modal_content(selected_row)
