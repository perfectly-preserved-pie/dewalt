from __future__ import annotations

from typing import Any

import dash_bootstrap_components as dbc
from dash import html

from .formatting import compare_display_value, format_bool
from .config import COMPARE_BOOLEAN_FIELDS


RowData = dict[str, Any]


DETAIL_FIELDS: list[tuple[str, str]] = [
    ("Series", "series_display"),
    ("Power Source", "power_source"),
    ("Voltage System", "voltage_system"),
    ("Wheel Size", "wheel_size_display"),
    ("Switch Type", "switch_type"),
    ("Max RPM", "rpm_max"),
    ("Amp Rating", "amp_rating"),
    ("Horsepower", "horsepower_hp"),
    ("Max Watts Out", "max_watts_out"),
    ("Power Input", "power_input_watts"),
    ("Brushless", "brushless"),
    ("Variable Speed", "variable_speed"),
    ("Anti-Rotation", "anti_rotation_system"),
    ("E-CLUTCH", "e_clutch"),
    ("Kickback Brake", "kickback_brake"),
    ("Tool Connect Ready", "tool_connect_ready"),
    ("Wireless Tool Control", "wireless_tool_control"),
    ("Power Loss Reset", "power_loss_reset"),
    ("No-Volt Switch", "no_volt_switch"),
    ("Lanyard Ready", "lanyard_ready"),
]


def resolve_detail_value(row: RowData, field_name: str) -> str:
    """Resolve a modal detail value for a named field.

    Args:
        row: Grinder row used to populate the modal.
        field_name: Internal field name to resolve.

    Returns:
        A formatted detail value string for the modal table.
    """
    if field_name == "switch_type":
        return row.get(field_name) or "-"
    if field_name in {"rpm_max", "amp_rating", "horsepower_hp", "max_watts_out", "power_input_watts"}:
        return compare_display_value(row, field_name)
    if field_name in COMPARE_BOOLEAN_FIELDS:
        return format_bool(row.get(field_name))
    return row.get(field_name, "-")


def build_detail_table(row: RowData) -> dbc.Table:
    """Build the modal's specification table for one grinder.

    Args:
        row: Grinder row used to populate the modal.

    Returns:
        A Bootstrap table component containing labeled specification rows.
    """
    body_rows = []
    for label, field_name in DETAIL_FIELDS:
        value = resolve_detail_value(row, field_name)
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
    """Build a titled modal section for a list of bullet values.

    Args:
        title: Section heading shown above the bullet list.
        values: Optional list of string values to render.

    Returns:
        A section ``Div`` when values exist, otherwise ``None``.
    """
    if not values:
        return None
    return html.Div(
        [
            html.H4(title, className="modal-section-title"),
            html.Ul([html.Li(value) for value in values], className="modal-list"),
        ],
        className="modal-section",
    )


def build_modal_content(row: RowData) -> list[Any]:
    """Build the full modal body content for one grinder.

    Args:
        row: Grinder row used to populate the modal.

    Returns:
        An ordered list of Dash components for the modal body.
    """
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


def build_modal_header(row: RowData) -> html.Div:
    """Build the modal header for one grinder.

    Args:
        row: Grinder row used to populate the modal header.

    Returns:
        A ``Div`` containing the SKU and model title.
    """
    return html.Div(
        [
            html.Div(row.get("sku", "Unknown SKU"), className="modal-sku"),
            html.H3(row.get("title", "Grinder Details"), className="modal-title"),
        ]
    )


def build_modal() -> dbc.Modal:
    """Create the reusable grinder detail modal component.

    Args:
        None.

    Returns:
        A configured Bootstrap modal component.
    """
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
