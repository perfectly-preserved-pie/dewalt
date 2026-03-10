from __future__ import annotations

from dash import Dash, Input, Output, State, callback_context, dcc, html, no_update
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

from dewalt.data import load_angle_grinders, load_snapshot


SNAPSHOT = load_snapshot()
RAW_ROWS = load_angle_grinders()
MAX_COMPARE = 4

AG_GRID_THEME = {
    "function": (
        "themeQuartz.withParams({"
        "accentColor: '#f0c534', "
        "backgroundColor: '#14181d', "
        "browserColorScheme: 'dark', "
        "foregroundColor: '#f5f6f8', "
        "headerBackgroundColor: '#0f1317', "
        "headerFontWeight: 700, "
        "oddRowBackgroundColor: 'rgba(255,255,255,0.03)'"
        "})"
    )
}

TEXT_FILTER = "agTextColumnFilter"
NUMBER_FILTER = "agNumberColumnFilter"
SET_FILTER = "agSetColumnFilter"
BOOLEAN_FILTER = SET_FILTER

COMPARE_FIELDS = [
    ("sku", "SKU"),
    ("title", "Model"),
    ("series", "Series"),
    ("power_source", "Power Source"),
    ("voltage_system", "Voltage System"),
    ("nominal_voltage_v", "Nominal Voltage"),
    ("amp_rating", "Amp Rating"),
    ("horsepower_hp", "Horsepower"),
    ("max_watts_out", "Max Watts Out"),
    ("power_input_watts", "Power Input"),
    ("wheel_size_display", "Wheel Size"),
    ("switch_type", "Switch Type"),
    ("rpm_max", "Max RPM"),
    ("brushless", "Brushless"),
    ("variable_speed", "Variable Speed"),
    ("anti_rotation_system", "Anti-Rotation"),
    ("e_clutch", "E-CLUTCH"),
    ("kickback_brake", "Kickback Brake"),
    ("wireless_tool_control", "Wireless Tool Control"),
    ("tool_connect_ready", "Tool Connect Ready"),
    ("power_loss_reset", "Power Loss Reset"),
    ("no_volt_switch", "No-Volt Switch"),
    ("lanyard_ready", "Lanyard Ready"),
    ("description", "Overview"),
    ("features", "Primary Features"),
    ("additional_features", "Additional Features"),
    ("includes", "Includes"),
    ("applications", "Applications"),
    ("disclaimers", "Disclaimers"),
]


def format_bool(value: bool | None) -> str:
    if value is None:
        return "-"
    return "Yes" if value else "No"


def format_numeric(value: float | int | None, suffix: str = "") -> str:
    if value is None:
        return "-"
    if isinstance(value, float) and value.is_integer():
        value = int(value)
    return f"{value}{suffix}"


def format_wheel_size(min_value: float | None, max_value: float | None) -> str:
    if min_value is None:
        return "-"
    if max_value is None or min_value == max_value:
        return f"{format_numeric(min_value)} in."
    return f"{format_numeric(min_value)} - {format_numeric(max_value)} in."


def format_lines(values: list[str] | None) -> str:
    if not values:
        return "-"
    return "\n".join(values)


def build_display_rows(rows: list[dict]) -> list[dict]:
    display_rows = []
    for row in rows:
        prepared_row = dict(row)
        prepared_row["series_display"] = ", ".join(row.get("series", [])) or "-"
        prepared_row["wheel_size_display"] = format_wheel_size(
            row.get("wheel_min_in"), row.get("wheel_max_in")
        )
        prepared_row["nominal_voltage_display"] = (
            f"{row['nominal_voltage_v']} V" if row.get("nominal_voltage_v") else "-"
        )
        prepared_row["amp_rating_display"] = (
            f"{row['amp_rating']} A" if row.get("amp_rating") else "-"
        )
        prepared_row["horsepower_display"] = (
            f"{row['horsepower_hp']} HP" if row.get("horsepower_hp") else "-"
        )
        prepared_row["max_watts_out_display"] = (
            f"{row['max_watts_out']} W" if row.get("max_watts_out") else "-"
        )
        prepared_row["power_input_display"] = (
            f"{row['power_input_watts']} W" if row.get("power_input_watts") else "-"
        )
        prepared_row["rpm_display"] = f"{row['rpm_max']:,}" if row.get("rpm_max") else "-"
        prepared_row["brushless_display"] = format_bool(row.get("brushless"))
        prepared_row["variable_speed_display"] = format_bool(row.get("variable_speed"))
        prepared_row["anti_rotation_display"] = format_bool(row.get("anti_rotation_system"))
        prepared_row["e_clutch_display"] = format_bool(row.get("e_clutch"))
        prepared_row["kickback_brake_display"] = format_bool(row.get("kickback_brake"))
        prepared_row["tool_connect_display"] = format_bool(row.get("tool_connect_ready"))
        prepared_row["wireless_tool_control_display"] = format_bool(
            row.get("wireless_tool_control")
        )
        prepared_row["features_display"] = format_lines(row.get("features"))
        prepared_row["additional_features_display"] = format_lines(
            row.get("additional_features")
        )
        prepared_row["includes_display"] = format_lines(row.get("includes"))
        prepared_row["applications_display"] = format_lines(row.get("applications"))
        prepared_row["disclaimers_display"] = format_lines(row.get("disclaimers"))
        display_rows.append(prepared_row)
    return display_rows


ANGLE_GRINDER_ROWS = build_display_rows(RAW_ROWS)

CORDLESS_COUNT = sum(1 for row in ANGLE_GRINDER_ROWS if row["power_source"] == "Cordless")
CORDED_COUNT = sum(1 for row in ANGLE_GRINDER_ROWS if row["power_source"] != "Cordless")
BRUSHLESS_COUNT = sum(1 for row in ANGLE_GRINDER_ROWS if row["brushless"])

def text_column(field: str, header_name: str, **kwargs) -> dict:
    column = {"field": field, "headerName": header_name, "filter": TEXT_FILTER}
    column.update(kwargs)
    return column


def categorical_column(field: str, header_name: str, **kwargs) -> dict:
    column = {"field": field, "headerName": header_name, "filter": SET_FILTER}
    column.update(kwargs)
    return column


def number_column(field: str, header_name: str, formatter: str | None = None, **kwargs) -> dict:
    column = {
        "field": field,
        "headerName": header_name,
        "filter": NUMBER_FILTER,
        "type": "numericColumn",
    }
    if formatter:
        column["valueFormatter"] = {"function": formatter}
    column.update(kwargs)
    return column


def boolean_column(field: str, header_name: str, **kwargs) -> dict:
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


MASTER_COLUMN_DEFS = [
    text_column(
        "sku",
        "SKU",
        checkboxSelection=True,
        headerCheckboxSelection=True,
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
    categorical_column("power_source", "Power", minWidth=130),
    categorical_column("series_display", "Series", minWidth=170),
    categorical_column("voltage_system", "Voltage", minWidth=130),
    number_column(
        "nominal_voltage_v",
        "Nominal",
        "params.value == null ? '-' : `${params.value} V`",
        minWidth=120,
    ),
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

COMPARE_BASE_COLUMNS = [
    {
        "field": "field_label",
        "headerName": "Specification",
        "pinned": "left",
        "minWidth": 230,
        "wrapText": True,
        "autoHeight": True,
    }
]

MASTER_GRID = dag.AgGrid(
    id="angle-grinders-grid",
    rowData=ANGLE_GRINDER_ROWS,
    columnDefs=MASTER_COLUMN_DEFS,
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
        "rowSelection": "multiple",
        "theme": AG_GRID_THEME,
    },
    className="grid-shell",
    enableEnterpriseModules=True,
)

COMPARE_GRID = dag.AgGrid(
    id="compare-grid",
    rowData=[],
    columnDefs=COMPARE_BASE_COLUMNS,
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


def build_compare_columns(selected_rows: list[dict]) -> list[dict]:
    columns = list(COMPARE_BASE_COLUMNS)
    for index, row in enumerate(selected_rows, start=1):
        columns.append(
            {
                "field": f"model_{index}",
                "headerName": row["sku"],
                "minWidth": 280,
                "tooltipField": f"model_{index}",
            }
        )
    return columns


def compare_display_value(row: dict, field_name: str) -> str:
    value = row.get(field_name)
    if field_name in {"series", "features", "additional_features", "includes", "applications", "disclaimers"}:
        return format_lines(value)
    if field_name == "nominal_voltage_v":
        return f"{value} V" if value else "-"
    if field_name == "amp_rating":
        return f"{value} A" if value else "-"
    if field_name == "horsepower_hp":
        return f"{value} HP" if value else "-"
    if field_name == "max_watts_out":
        return f"{value} W" if value else "-"
    if field_name == "power_input_watts":
        return f"{value} W" if value else "-"
    if field_name == "wheel_size_display":
        return row.get("wheel_size_display", "-")
    if field_name == "rpm_max":
        return f"{value:,}" if value else "-"
    if isinstance(value, bool):
        return format_bool(value)
    if value in (None, "", []):
        return "-"
    return str(value)


def build_compare_rows(selected_rows: list[dict]) -> list[dict]:
    rows = []
    for field_name, label in COMPARE_FIELDS:
        compare_row = {"field_label": label}
        for index, product_row in enumerate(selected_rows, start=1):
            compare_row[f"model_{index}"] = compare_display_value(product_row, field_name)
        rows.append(compare_row)
    return rows


DETAIL_FIELDS = [
    ("Series", lambda row: row.get("series_display", "-")),
    ("Power Source", lambda row: row.get("power_source", "-")),
    ("Voltage System", lambda row: row.get("voltage_system", "-")),
    ("Nominal Voltage", lambda row: compare_display_value(row, "nominal_voltage_v")),
    ("Wheel Size", lambda row: row.get("wheel_size_display", "-")),
    ("Switch Type", lambda row: row.get("switch_type") or "-"),
    ("Max RPM", lambda row: compare_display_value(row, "rpm_max")),
    ("Amp Rating", lambda row: compare_display_value(row, "amp_rating")),
    ("Horsepower", lambda row: compare_display_value(row, "horsepower_hp")),
    ("Max Watts Out", lambda row: compare_display_value(row, "max_watts_out")),
    ("Power Input", lambda row: compare_display_value(row, "power_input_watts")),
    ("Brushless", lambda row: format_bool(row.get("brushless"))),
    ("Variable Speed", lambda row: format_bool(row.get("variable_speed"))),
    ("Anti-Rotation", lambda row: format_bool(row.get("anti_rotation_system"))),
    ("E-CLUTCH", lambda row: format_bool(row.get("e_clutch"))),
    ("Kickback Brake", lambda row: format_bool(row.get("kickback_brake"))),
    ("Tool Connect Ready", lambda row: format_bool(row.get("tool_connect_ready"))),
    ("Wireless Tool Control", lambda row: format_bool(row.get("wireless_tool_control"))),
    ("Power Loss Reset", lambda row: format_bool(row.get("power_loss_reset"))),
    ("No-Volt Switch", lambda row: format_bool(row.get("no_volt_switch"))),
    ("Lanyard Ready", lambda row: format_bool(row.get("lanyard_ready"))),
]


def build_detail_table(row: dict) -> dbc.Table:
    body_rows = []
    for label, resolver in DETAIL_FIELDS:
        value = resolver(row)
        if value in (None, "", "-", []):
            continue
        body_rows.append(
            html.Tr(
                [
                    html.Th(label, className="modal-spec-label"),
                    html.Td(value, className="modal-spec-value"),
                ]
            )
        )

    return dbc.Table(body_rows, borderless=True, hover=False, className="modal-spec-table")


def build_detail_block(title: str, values: list[str] | None) -> html.Div | None:
    if not values:
        return None
    return html.Div(
        [
            html.H4(title, className="modal-section-title"),
            html.Ul([html.Li(value) for value in values], className="modal-list"),
        ],
        className="modal-section",
    )


def build_modal_content(row: dict) -> list:
    content = [
        html.P(row.get("description", "-"), className="modal-overview"),
        build_detail_table(row),
    ]

    for title, field_name in (
        ("Primary Features", "features"),
        ("Additional Features", "additional_features"),
        ("Includes", "includes"),
        ("Applications", "applications"),
        ("Disclaimers", "disclaimers"),
    ):
        section = build_detail_block(title, row.get(field_name))
        if section:
            content.append(section)

    return content


MODAL = dbc.Modal(
    [
        dbc.ModalHeader(id="grinder-modal-header"),
        dbc.ModalBody(id="grinder-modal-content"),
        dbc.ModalFooter(
            dbc.Button("Close", id="grinder-modal-close", color="secondary", n_clicks=0)
        ),
    ],
    id="grinder-modal",
    is_open=False,
    size="xl",
    scrollable=True,
)


app = Dash(
    __name__,
    title="DEWALT Compare",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)

app.layout = dbc.Container(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.P("DEWALT TOOL INDEX", className="eyebrow"),
                        html.H1("Angle Grinder Compare", className="hero-title"),
                        html.P(
                            (
                                "A Dash AG Grid catalog for DEWALT bare-tool angle grinders. "
                                "Corded grinders are included, and cordless grinders are limited "
                                "to bare-tool SKUs. Filter the master table, select models, and compare specs "
                                "and feature sets side by side."
                            ),
                            className="hero-copy",
                        ),
                    ],
                    className="hero-copy-block",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Span("Snapshot", className="stat-label"),
                                html.Strong(
                                    SNAPSHOT["scraped_at"].replace("T", " ").replace("+00:00", " UTC"),
                                    className="stat-value stat-value-small",
                                ),
                            ],
                            className="stat-card stat-card-wide",
                        ),
                        html.Div(
                            [
                                html.Span("Grinders", className="stat-label"),
                                html.Strong(str(SNAPSHOT["product_count"]), className="stat-value"),
                            ],
                            className="stat-card",
                        ),
                        html.Div(
                            [
                                html.Span("Cordless", className="stat-label"),
                                html.Strong(str(CORDLESS_COUNT), className="stat-value"),
                            ],
                            className="stat-card",
                        ),
                        html.Div(
                            [
                                html.Span("Corded", className="stat-label"),
                                html.Strong(str(CORDED_COUNT), className="stat-value"),
                            ],
                            className="stat-card",
                        ),
                        html.Div(
                            [
                                html.Span("Brushless", className="stat-label"),
                                html.Strong(str(BRUSHLESS_COUNT), className="stat-value"),
                            ],
                            className="stat-card",
                        ),
                    ],
                    className="stats-grid",
                ),
            ],
            className="hero-panel",
        ),
        dcc.Tabs(
            id="tool-tabs",
            value="angle-grinders",
            className="tool-tabs",
            children=[
                dcc.Tab(
                    label="Angle Grinders",
                    value="angle-grinders",
                    className="tool-tab",
                    selected_className="tool-tab tool-tab-selected",
                    children=[
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            "Select up to 4 grinders to compare. Clicking a row opens a detail popup.",
                                            className="panel-note",
                                        ),
                                        html.Div(id="selection-summary", className="selection-summary"),
                                    ],
                                    className="panel-header",
                                ),
                                MASTER_GRID,
                                MODAL,
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.H2("Comparison", className="section-title"),
                                                html.Div(id="compare-note", className="compare-note"),
                                            ],
                                            className="compare-header",
                                        ),
                                        COMPARE_GRID,
                                    ],
                                    className="compare-shell",
                                ),
                            ],
                            className="tab-panel",
                        )
                    ],
                ),
                dcc.Tab(
                    label="Coming Soon",
                    value="placeholder",
                    className="tool-tab",
                    selected_className="tool-tab tool-tab-selected",
                    children=[
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H2("Reserved For The Next DEWALT Table", className="section-title"),
                                        html.P(
                                            (
                                                "This tab is a placeholder for the next product family. "
                                                "The same master-table and comparison pattern can be reused "
                                                "for saws, drills, or nailers once you choose the next scrape target."
                                            ),
                                            className="placeholder-copy",
                                        ),
                                    ],
                                    className="placeholder-card",
                                )
                            ],
                            className="tab-panel",
                        )
                    ],
                ),
            ],
        ),
    ],
    fluid=True,
    className="app-shell",
)


@app.callback(
    Output("selection-summary", "children"),
    Input("angle-grinders-grid", "virtualRowData"),
    Input("angle-grinders-grid", "selectedRows"),
)
def update_selection_summary(
    visible_rows: list[dict] | None, selected_rows: list[dict] | None
) -> list[html.Span]:
    visible_count = len(visible_rows) if visible_rows is not None else len(ANGLE_GRINDER_ROWS)
    selected_count = len(selected_rows or [])
    return [
        html.Span(f"{visible_count} visible", className="summary-pill"),
        html.Span(f"{selected_count} selected", className="summary-pill"),
        html.Span(f"{MAX_COMPARE} max compare", className="summary-pill summary-pill-accent"),
    ]


@app.callback(
    Output("compare-note", "children"),
    Output("compare-grid", "rowData"),
    Output("compare-grid", "columnDefs"),
    Input("angle-grinders-grid", "selectedRows"),
)
def update_compare_grid(selected_rows: list[dict] | None) -> tuple[str, list[dict], list[dict]]:
    rows = selected_rows or []
    if not rows:
        return (
            "No grinders selected yet. Use the checkboxes in the master table to build a comparison.",
            [],
            COMPARE_BASE_COLUMNS,
        )

    note = f"Comparing {min(len(rows), MAX_COMPARE)} grinder(s)."
    if len(rows) > MAX_COMPARE:
        note += f" Showing the first {MAX_COMPARE} selected rows."

    compare_rows = rows[:MAX_COMPARE]
    return note, build_compare_rows(compare_rows), build_compare_columns(compare_rows)


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

    header = html.Div(
        [
            html.Div(selected_row.get("sku", "Unknown SKU"), className="modal-sku"),
            html.H3(selected_row.get("title", "Grinder Details"), className="modal-title"),
        ]
    )
    return True, header, build_modal_content(selected_row)


if __name__ == "__main__":
    app.run(debug=True)
