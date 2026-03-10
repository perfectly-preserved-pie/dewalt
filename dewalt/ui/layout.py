from __future__ import annotations

from typing import Any

import dash_bootstrap_components as dbc
from dash import dcc, html

from .context import DashboardContext


def build_layout(
    context: DashboardContext,
    master_grid: Any,
    compare_grid: Any,
    modal: Any,
) -> dbc.Container:
    """Assemble the top-level dashboard layout.

    Args:
        context: Shared dashboard context with snapshot metadata and counts.
        master_grid: The master grinder AG Grid component.
        compare_grid: The transposed comparison AG Grid component.
        modal: The grinder detail modal component.

    Returns:
        A Bootstrap container representing the full app layout.
    """
    snapshot_time = context.snapshot["scraped_at"].replace("T", " ").replace("+00:00", " UTC")

    return dbc.Container(
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
                                        snapshot_time,
                                        className="stat-value stat-value-small",
                                    ),
                                ],
                                className="stat-card stat-card-wide",
                            ),
                            html.Div(
                                [
                                    html.Span("Grinders", className="stat-label"),
                                    html.Strong(
                                        str(context.snapshot["product_count"]),
                                        className="stat-value",
                                    ),
                                ],
                                className="stat-card",
                            ),
                            html.Div(
                                [
                                    html.Span("Cordless", className="stat-label"),
                                    html.Strong(str(context.cordless_count), className="stat-value"),
                                ],
                                className="stat-card",
                            ),
                            html.Div(
                                [
                                    html.Span("Corded", className="stat-label"),
                                    html.Strong(str(context.corded_count), className="stat-value"),
                                ],
                                className="stat-card",
                            ),
                            html.Div(
                                [
                                    html.Span("Brushless", className="stat-label"),
                                    html.Strong(
                                        str(context.brushless_count),
                                        className="stat-value",
                                    ),
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
                                                (
                                                    "Select up to 4 grinders to compare. "
                                                    "Clicking a row opens a detail popup."
                                                ),
                                                className="panel-note",
                                            ),
                                            html.Div(
                                                id="selection-summary",
                                                className="selection-summary",
                                            ),
                                        ],
                                        className="panel-header",
                                    ),
                                    master_grid,
                                    modal,
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.H2(
                                                        "Comparison",
                                                        className="section-title",
                                                    ),
                                                    html.Div(
                                                        id="compare-note",
                                                        className="compare-note",
                                                    ),
                                                ],
                                                className="compare-header",
                                            ),
                                            compare_grid,
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
                                            html.H2(
                                                "Reserved For The Next DEWALT Table",
                                                className="section-title",
                                            ),
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
