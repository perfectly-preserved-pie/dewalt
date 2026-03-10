from __future__ import annotations

from typing import Any

import dash_ag_grid as dag

from dewalt.tool_families.base import ColumnDef, RowData, ToolFamilyDefinition, ToolFamilyIds

from .config import AG_GRID_THEME


def build_compare_base_columns() -> list[ColumnDef]:
    """Build the fixed leading column for the comparison grid.

    Args:
        None.

    Returns:
        A list containing the pinned specification-label column definition.
    """
    return [
        {
            "field": "field_label",
            "headerName": "Specification",
            "pinned": "left",
            "minWidth": 230,
            "wrapText": True,
            "autoHeight": True,
        }
    ]


def build_master_grid(
    rows: list[RowData],
    column_defs: list[ColumnDef],
    ids: ToolFamilyIds,
) -> dag.AgGrid:
    """Create the master AG Grid for a tool family.

    Args:
        rows: Prepared row data for the master grid.
        column_defs: Prebuilt master column definitions.
        ids: Tool-family-specific component ids.

    Returns:
        A configured Dash AG Grid component for the master table.
    """
    return dag.AgGrid(
        id=ids.grid,
        rowData=rows,
        columnDefs=column_defs,
        getRowId="params.data.sku",
        persisted_props=[],
        persistence=False,
        defaultColDef={
            "sortable": True,
            "resizable": True,
            "floatingFilter": True,
        },
        columnSize="sizeToFit",
        style={"width": "100%", "height": "620px"},
        dashGridOptions={
            "animateRows": False,
            "pagination": True,
            "paginationPageSize": 12,
            "paginationPageSizeSelector": [12, 24, 48],
            "rowSelection": {
                "mode": "multiRow",
                "checkboxes": True,
                "headerCheckbox": True,
                "enableClickSelection": True,
            },
            "selectionColumnDef": {
                "pinned": "left",
                "minWidth": 56,
                "width": 56,
                "maxWidth": 56,
                "resizable": False,
                "sortable": False,
                "filter": False,
            },
            "theme": AG_GRID_THEME,
        },
        className="grid-shell",
        enableEnterpriseModules=True,
    )


def build_compare_grid(
    ids: ToolFamilyIds,
    column_defs: list[ColumnDef] | None = None,
) -> dag.AgGrid:
    """Create the transposed comparison AG Grid.

    Args:
        ids: Tool-family-specific component ids.
        column_defs: Optional prebuilt column definitions for the comparison grid.

    Returns:
        A configured Dash AG Grid component for model comparison rows.
    """
    return dag.AgGrid(
        id=ids.compare_grid,
        rowData=[],
        columnDefs=column_defs or build_compare_base_columns(),
        defaultColDef={
            "sortable": False,
            "resizable": True,
            "wrapText": True,
            "autoHeight": True,
        },
        style={"width": "100%", "height": "620px"},
        dashGridOptions={
            "animateRows": False,
            "theme": AG_GRID_THEME,
        },
        className="grid-shell compare-grid",
    )


def build_compare_columns(
    selected_rows: list[RowData],
    base_columns: list[ColumnDef] | None = None,
) -> list[ColumnDef]:
    """Build dynamic comparison-grid columns for the selected models.

    Args:
        selected_rows: Family rows chosen for comparison.
        base_columns: Optional base comparison columns to reuse.

    Returns:
        A complete list of comparison-grid column definitions.
    """
    columns = [dict(column) for column in (base_columns or build_compare_base_columns())]
    for index, row in enumerate(selected_rows, start=1):
        columns.append(
            {
                "field": f"model_{index}",
                "headerName": row["sku"],
                "minWidth": 280,
                "tooltipField": f"model_{index}",
                "cellRendererSelector": {
                    "function": (
                        "params.data.value_type === 'boolean' && params.value != null "
                        "? {component: 'agCheckboxCellRenderer', params: {disabled: true}} : undefined"
                    )
                },
                "cellStyle": {
                    "function": (
                        "params.data.value_type === 'boolean' "
                        "? ({display: 'flex', alignItems: 'center', justifyContent: 'flex-start', paddingLeft: '12px'}) "
                        ": null"
                    )
                },
                "tooltipValueGetter": {
                    "function": (
                        "params.data.value_type === 'boolean' "
                        "? (params.value === true ? 'Yes' : params.value === false ? 'No' : '-') "
                        ": params.value"
                    )
                },
            }
        )
    return columns


def build_compare_rows(
    selected_rows: list[RowData],
    family: ToolFamilyDefinition,
) -> list[RowData]:
    """Transpose selected family rows into comparison-grid rows.

    Args:
        selected_rows: Family rows chosen for comparison.
        family: Tool family definition that owns compare-field metadata.

    Returns:
        A list of row dictionaries keyed by specification label and model columns.
    """
    rows = []
    for field_name, label in family.compare_fields:
        value_type = "boolean" if field_name in family.compare_boolean_fields else "text"
        compare_row: RowData = {
            "field_label": label,
            "field_name": field_name,
            "value_type": value_type,
        }
        for index, product_row in enumerate(selected_rows, start=1):
            if value_type == "boolean":
                compare_row[f"model_{index}"] = product_row.get(field_name)
            else:
                compare_row[f"model_{index}"] = family.compare_display_value(
                    product_row, field_name
                )
        rows.append(compare_row)
    return rows
