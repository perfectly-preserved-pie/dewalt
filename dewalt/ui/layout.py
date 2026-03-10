from __future__ import annotations

from typing import Any

import dash_bootstrap_components as dbc
from dash import dcc, html

from dewalt.tool_families.base import StatCard

from .context import DashboardContext


def build_stat_card(card: StatCard) -> html.Div:
    """Build one hero statistic card.

    Args:
        card: Stat-card metadata to render.

    Returns:
        A ``Div`` containing the stat label and value.
    """
    return html.Div(
        [
            html.Span(card.label, className="stat-label"),
            html.Strong(card.value, className=card.value_class_name),
        ],
        className=card.card_class_name,
    )


def build_layout(
    context: DashboardContext,
    master_grid: Any,
    compare_grid: Any,
    modal: Any,
) -> dbc.Container:
    """Assemble the top-level dashboard layout.

    Args:
        context: Shared dashboard context with family metadata and prepared rows.
        master_grid: The master family AG Grid component.
        compare_grid: The transposed comparison AG Grid component.
        modal: The family detail modal component.

    Returns:
        A Bootstrap container representing the full app layout.
    """
    snapshot_time = context.snapshot["scraped_at"].replace("T", " ").replace("+00:00", " UTC")

    stats = [
        build_stat_card(
            StatCard(
                "Snapshot",
                snapshot_time,
                card_class_name="stat-card stat-card-wide",
                value_class_name="stat-value stat-value-small",
            )
        ),
        *[build_stat_card(card) for card in context.stat_cards],
    ]

    return dbc.Container(
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.P("DEWALT TOOL INDEX", className="eyebrow"),
                            html.H1(context.family.hero_title, className="hero-title"),
                            html.P(context.family.hero_copy, className="hero-copy"),
                        ],
                        className="hero-copy-block",
                    ),
                    html.Div(stats, className="stats-grid"),
                ],
                className="hero-panel",
            ),
            dcc.Tabs(
                id="tool-tabs",
                value=context.family.slug,
                className="tool-tabs",
                children=[
                    dcc.Tab(
                        label=context.family.tab_label,
                        value=context.family.slug,
                        className="tool-tab",
                        selected_className="tool-tab tool-tab-selected",
                        children=[
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.Div(
                                                context.family.selection_note,
                                                className="panel-note",
                                            ),
                                            html.Div(
                                                id=context.family.ids.selection_summary,
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
                                                        context.family.compare_title,
                                                        className="section-title",
                                                    ),
                                                    html.Div(
                                                        id=context.family.ids.compare_note,
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
