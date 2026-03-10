from __future__ import annotations

from typing import Any

import dash_bootstrap_components as dbc
from dash import html

from .formatting import compare_display_value, format_bool


DETAIL_FIELDS = [
    ("Series", lambda row: row.get("series_display", "-")),
    ("Power Source", lambda row: row.get("power_source", "-")),
    ("Voltage System", lambda row: row.get("voltage_system", "-")),
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


def build_detail_table(row: dict[str, Any]) -> dbc.Table:
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


def build_modal_content(row: dict[str, Any]) -> list[Any]:
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


def build_modal_header(row: dict[str, Any]) -> html.Div:
    return html.Div(
        [
            html.Div(row.get("sku", "Unknown SKU"), className="modal-sku"),
            html.H3(row.get("title", "Grinder Details"), className="modal-title"),
        ]
    )


def build_modal() -> dbc.Modal:
    return dbc.Modal(
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
