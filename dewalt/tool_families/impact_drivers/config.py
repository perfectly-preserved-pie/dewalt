from __future__ import annotations

from dewalt.data import load_impact_driver_snapshot, load_impact_drivers
from dewalt.tool_families.base import ToolFamilyDefinition, build_family_ids

from .formatting import build_display_rows, build_stat_cards, compare_display_value
from .grids import build_master_column_defs


IMPACT_DRIVER_FAMILY = ToolFamilyDefinition(
    slug="impact-drivers",
    tab_label="Impact Drivers",
    hero_title="Impact Driver Compare",
    hero_copy=(
        "A Dash AG Grid catalog for DEWALT impact drivers. "
        "The current snapshot follows the existing repo scope: cordless tools are limited "
        "to bare-tool SKUs, while kits, accessories, and impact wrenches are excluded. "
        "Filter the master table, open detail popups, and compare core fastening specs "
        "side by side."
    ),
    selection_note="Select up to 4 impact drivers to compare. Clicking a row opens a detail popup.",
    no_selection_note=(
        "No impact drivers selected yet. Use the checkboxes in the master table to build a comparison."
    ),
    compare_title="Comparison",
    compare_fields=(
        ("sku", "SKU"),
        ("title", "Model"),
        ("series", "Series"),
        ("power_source", "Power Source"),
        ("voltage_system", "Voltage System"),
        ("chuck_size_display", "Drive Size"),
        ("speed_count", "Speed Settings"),
        ("no_load_speed", "No Load Speed"),
        ("rpm_max", "Max RPM"),
        ("impact_rate_bpm", "Impact Rate"),
        ("max_torque_in_lbs", "Max Torque"),
        ("power_watts", "Power"),
        ("tool_length_in", "Tool Length"),
        ("weight_lbs", "Weight"),
        ("brushless", "Brushless"),
        ("led_light", "LED Light"),
        ("hydraulic", "Hydraulic"),
        ("high_torque", "High Torque"),
        ("tool_connect_ready", "Tool Connect Ready"),
        ("lanyard_ready", "Lanyard Ready"),
        ("description", "Overview"),
        ("features", "Primary Features"),
        ("additional_features", "Additional Features"),
        ("includes", "Includes"),
        ("applications", "Applications"),
        ("disclaimers", "Disclaimers"),
    ),
    compare_boolean_fields=frozenset(
        {
            "brushless",
            "led_light",
            "hydraulic",
            "high_torque",
            "tool_connect_ready",
            "lanyard_ready",
        }
    ),
    detail_fields=(
        ("Series", "series_display"),
        ("Power Source", "power_source"),
        ("Voltage System", "voltage_system"),
        ("Drive Size", "chuck_size_display"),
        ("Speed Settings", "speed_count"),
        ("No Load Speed", "no_load_speed"),
        ("Max RPM", "rpm_max"),
        ("Impact Rate", "impact_rate_bpm"),
        ("Max Torque", "max_torque_in_lbs"),
        ("Power", "power_watts"),
        ("Tool Length", "tool_length_in"),
        ("Weight", "weight_lbs"),
        ("Brushless", "brushless"),
        ("LED Light", "led_light"),
        ("Hydraulic", "hydraulic"),
        ("High Torque", "high_torque"),
        ("Tool Connect Ready", "tool_connect_ready"),
        ("Lanyard Ready", "lanyard_ready"),
    ),
    ids=build_family_ids("impact-drivers"),
    load_snapshot=load_impact_driver_snapshot,
    load_rows=load_impact_drivers,
    build_display_rows=build_display_rows,
    compare_display_value=compare_display_value,
    build_master_column_defs=build_master_column_defs,
    build_stat_cards=build_stat_cards,
)
