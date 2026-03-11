from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

import dash_bootstrap_components as dbc
from dash import dcc, html

from dewalt.tool_families.base import StatCard

from .context import DashboardContext


@dataclass(frozen=True)
class DashboardSection:
    """Component bundle for one tool-family tab.

    Attributes:
        context: Shared dashboard context for the tool family.
        master_grid: Dash AG Grid instance for the family master table.
        compare_grid: Dash AG Grid instance for the family comparison table.
        modal: Dash Bootstrap modal instance for the family detail popup.
    """

    context: DashboardContext
    master_grid: Any
    compare_grid: Any
    modal: Any


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


def format_family_list(labels: list[str]) -> str:
    """Format tool-family labels into natural-language copy.

    Args:
        labels: Ordered list of family labels.

    Returns:
        A human-readable string joining the family labels, sorted alphabetically.
    """
    labels = sorted(labels)
    if not labels:
        return "DEWALT tools"
    if len(labels) == 1:
        return labels[0]
    if len(labels) == 2:
        return f"{labels[0]} and {labels[1]}"
    return f"{', '.join(labels[:-1])}, and {labels[-1]}"


def build_family_tab(section: DashboardSection) -> dcc.Tab:
    """Build the complete tab content for one tool family.

    Args:
        section: Tool-family component bundle to render.

    Returns:
        A populated Dash tab for the given family.
    """
    context = section.context
    family_stats = [build_stat_card(card) for card in context.stat_cards]

    return dcc.Tab(
        label=context.family.tab_label,
        value=context.family.slug,
        className="tool-tab",
        selected_className="tool-tab tool-tab-selected",
        children=[
            html.Div(
                [
                    html.Div(
                        [
                            html.H2(context.family.hero_title, className="section-title"),
                            html.P(context.family.hero_copy, className="family-copy"),
                        ],
                        className="family-overview",
                    ),
                    html.Div(family_stats, className="stats-grid family-stats"),
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
                            section.master_grid,
                            section.modal,
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
                                    section.compare_grid,
                                ],
                                className="compare-shell",
                            ),
                        ],
                        className="family-panel",
                    ),
                ],
                className="tab-panel",
            )
        ],
    )


def build_layout(sections: Sequence[DashboardSection]) -> dbc.Container:
    """Assemble the top-level dashboard layout.

    Args:
        sections: Ordered component bundles for each tool-family tab.

    Returns:
        A Bootstrap container representing the full app layout.
    """
    if not sections:
        raise ValueError("At least one dashboard section is required.")

    latest_snapshot = max(section.context.snapshot["scraped_at"] for section in sections)
    snapshot_time = latest_snapshot.replace("T", " ").replace("+00:00", " UTC")
    family_labels = [section.context.family.tab_label for section in sections]
    total_models = sum(len(section.context.display_rows) for section in sections)

    stats = [
        build_stat_card(
            StatCard(
                "Snapshot",
                snapshot_time,
                card_class_name="stat-card stat-card-wide",
                value_class_name="stat-value stat-value-small",
            )
        ),
        build_stat_card(StatCard("Families", str(len(sections)))),
        build_stat_card(StatCard("Models", str(total_models))),
    ]

    return dbc.Container(
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.P("DEWALT TOOL INDEX", className="eyebrow"),
                            html.H1("DEWALT Compare", className="hero-title"),
                            html.P(
                                (
                                    f"Dash AG Grid catalogs for {format_family_list(family_labels)}. "
                                    "Each tab includes a master table, a row-detail modal, and a "
                                    "side-by-side comparison view."
                                ),
                                className="hero-copy",
                            ),
                        ],
                        className="hero-copy-block",
                    ),
                    html.Div(stats, className="stats-grid"),
                ],
                className="hero-panel",
            ),
            dcc.Tabs(
                id="tool-tabs",
                value=sections[0].context.family.slug,
                className="tool-tabs",
                children=sorted([build_family_tab(section) for section in sections], key=lambda tab: tab.label),
            ),
        ],
        fluid=True,
        className="app-shell",
    )
