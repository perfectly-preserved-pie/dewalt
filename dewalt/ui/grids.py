from __future__ import annotations

from typing import Any

import dash_ag_grid as dag

from .config import (
    AG_GRID_THEME,
    BOOLEAN_FILTER,
    COMPARE_BOOLEAN_FIELDS,
    COMPARE_FIELDS,
    MULTI_FILTER,
    NUMBER_FILTER,
    SET_FILTER,
    TEXT_FILTER,
)
from .formatting import compare_display_value

ColumnDef = dict[str, Any]
RowData = dict[str, Any]


def text_column(field: str, header_name: str, **kwargs: Any) -> ColumnDef:
    """Build a text-filtered AG Grid column definition.

    Args:
        field: Data field name for the column.
        header_name: Visible header label.
        **kwargs: Additional AG Grid column properties to merge in.

    Returns:
        An AG Grid column definition configured with a text filter.
    """
    column = {"field": field, "headerName": header_name, "filter": TEXT_FILTER}
    column.update(kwargs)
    return column


def categorical_column(field: str, header_name: str, **kwargs: Any) -> ColumnDef:
    """Build a set-filtered AG Grid column definition.

    Args:
        field: Data field name for the column.
        header_name: Visible header label.
        **kwargs: Additional AG Grid column properties to merge in.

    Returns:
        An AG Grid column definition configured with a set filter.
    """
    column = {"field": field, "headerName": header_name, "filter": SET_FILTER}
    column.update(kwargs)
    return column


def number_column(
    field: str,
    header_name: str,
    formatter: str | None = None,
    **kwargs: Any,
) -> ColumnDef:
    """Build a numeric AG Grid column with both value-list and range filters.

    Args:
        field: Data field name for the column.
        header_name: Visible header label.
        formatter: Optional JavaScript formatter function string.
        **kwargs: Additional AG Grid column properties to merge in.

    Returns:
        An AG Grid column definition configured for numeric values.
    """
    column = {
        "field": field,
        "headerName": header_name,
        "filter": MULTI_FILTER,
        "type": "numericColumn",
        "filterParams": {
            "filters": [
                {
                    "filter": SET_FILTER,
                    "title": "Values",
                },
                {
                    "filter": NUMBER_FILTER,
                    "title": "Range",
                },
            ]
        },
    }
    if formatter:
        formatter_config = {"function": formatter}
        column["valueFormatter"] = formatter_config
        column["filterParams"]["filters"][0]["filterParams"] = {
            "valueFormatter": formatter_config
        }
    column.update(kwargs)
    return column


def boolean_column(field: str, header_name: str, **kwargs: Any) -> ColumnDef:
    """Build a boolean AG Grid column definition.

    Args:
        field: Data field name for the column.
        header_name: Visible header label.
        **kwargs: Additional AG Grid column properties to merge in.

    Returns:
        An AG Grid column definition configured for boolean data.
    """
    column = {
        "field": field,
        "headerName": header_name,
        "filter": BOOLEAN_FILTER,
        "cellDataType": "boolean",
        "valueFormatter": {
            "function": (
                "params.value === true ? 'Yes' : "
                "params.value === false ? 'No' : '-'"
            )
        },
        "filterParams": {
            "valueFormatter": {
                "function": (
                    "params.value === true ? 'Yes' : "
                    "params.value === false ? 'No' : '-'"
                )
            }
        },
    }
    column.update(kwargs)
    return column


def build_master_column_defs() -> list[ColumnDef]:
    """Build the grouped column definitions for the master grinder grid.

    Args:
        None.

    Returns:
        A list of AG Grid column definitions for the master grid.
    """
    identity_column_defs = [
        text_column(
            "sku",
            "SKU",
            pinned="left",
            minWidth=120,
        ),
        text_column(
            "title",
            "Model",
            flex=2.4,
            minWidth=340,
            tooltipField="title",
            wrapText=True,
            autoHeight=True,
        ),
    ]

    spec_column_defs = [
        categorical_column("power_source", "Power", minWidth=130),
        categorical_column("series_display", "Series", minWidth=170),
        categorical_column("voltage_system", "Voltage", minWidth=130),
        categorical_column("wheel_size_display", "Wheel Size", minWidth=140),
        categorical_column("switch_type", "Switch", minWidth=150),
        number_column(
            "rpm_max",
            "RPM",
            "params.value == null ? '-' : params.value.toLocaleString()",
            minWidth=110,
        ),
        number_column(
            "amp_rating",
            "Amp",
            "params.value == null ? '-' : `${params.value} A`",
            minWidth=110,
        ),
        number_column(
            "horsepower_hp",
            "HP",
            "params.value == null ? '-' : `${params.value} HP`",
            minWidth=110,
        ),
        number_column(
            "max_watts_out",
            "MWO",
            "params.value == null ? '-' : `${params.value.toLocaleString()} W`",
            minWidth=120,
        ),
        number_column(
            "power_input_watts",
            "Power Input",
            "params.value == null ? '-' : `${params.value.toLocaleString()} W`",
            minWidth=135,
        ),
    ]

    feature_column_defs = [
        boolean_column("brushless", "Brushless", minWidth=120),
        boolean_column("variable_speed", "Variable Speed", minWidth=145),
        boolean_column("anti_rotation_system", "Anti-Rotation", minWidth=140),
        boolean_column("e_clutch", "E-CLUTCH", minWidth=120),
        boolean_column("kickback_brake", "Kickback Brake", minWidth=145),
        boolean_column("tool_connect_ready", "Tool Connect", minWidth=135),
        boolean_column(
            "wireless_tool_control",
            "Wireless Tool Control",
            minWidth=185,
        ),
    ]

    return [
        *identity_column_defs,
        {
            "headerName": "Specs",
            "marryChildren": True,
            "children": spec_column_defs,
        },
        {
            "headerName": "Features",
            "marryChildren": True,
            "children": feature_column_defs,
        },
    ]


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
    column_defs: list[ColumnDef] | None = None,
) -> dag.AgGrid:
    """Create the master AG Grid for angle grinders.

    Args:
        rows: Prepared row data for the master grid.
        column_defs: Optional prebuilt master column definitions.

    Returns:
        A configured Dash AG Grid component for the master grinder table.
    """
    return dag.AgGrid(
        id="angle-grinders-grid",
        rowData=rows,
        columnDefs=column_defs or build_master_column_defs(),
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


def build_compare_grid(column_defs: list[ColumnDef] | None = None) -> dag.AgGrid:
    """Create the transposed comparison AG Grid.

    Args:
        column_defs: Optional prebuilt column definitions for the comparison grid.

    Returns:
        A configured Dash AG Grid component for model comparison rows.
    """
    return dag.AgGrid(
        id="compare-grid",
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
    """Build dynamic comparison-grid columns for the selected grinders.

    Args:
        selected_rows: Grinder rows chosen for comparison.
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


def build_compare_rows(selected_rows: list[RowData]) -> list[RowData]:
    """Transpose selected grinder rows into comparison-grid rows.

    Args:
        selected_rows: Grinder rows chosen for comparison.

    Returns:
        A list of row dictionaries keyed by specification label and model columns.
    """
    rows = []
    for field_name, label in COMPARE_FIELDS:
        value_type = "boolean" if field_name in COMPARE_BOOLEAN_FIELDS else "text"
        compare_row = {
            "field_label": label,
            "field_name": field_name,
            "value_type": value_type,
        }
        for index, product_row in enumerate(selected_rows, start=1):
            if value_type == "boolean":
                compare_row[f"model_{index}"] = product_row.get(field_name)
            else:
                compare_row[f"model_{index}"] = compare_display_value(product_row, field_name)
        rows.append(compare_row)
    return rows
