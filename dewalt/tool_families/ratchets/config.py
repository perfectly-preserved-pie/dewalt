from __future__ import annotations

from dewalt.data import load_ratchet_snapshot, load_ratchets
from dewalt.tool_families.base import ToolFamilyDefinition, build_family_ids

from .formatting import build_display_rows, build_stat_cards, compare_display_value
from .grids import build_master_column_defs


RATCHET_FAMILY = ToolFamilyDefinition(
    slug="ratchets",
    tab_label="Ratchets",
    hero_title="Ratchet Compare",
    hero_copy=(
        "A Dash AG Grid catalog for DEWALT cordless ratchets. Bare-tool cordless "
        "SKUs are kept in scope, kits are excluded, and the comparison view focuses "
        "on drive sizes, ratchet head styles, torque, and reach."
    ),
    selection_note="Select up to 4 ratchets to compare. Clicking a row opens a detail popup.",
    no_selection_note=(
        "No ratchets selected yet. Use the checkboxes in the master table to build a comparison."
    ),
    compare_title="Comparison",
    compare_fields=(
        ("sku", "SKU"),
        ("title", "Model"),
        ("series", "Series"),
        ("power_source", "Power Source"),
        ("voltage_system", "Voltage System"),
        ("drive_size_display", "Drive Size"),
        ("head_type", "Head Type"),
        ("no_load_speed", "No Load Speed"),
        ("rpm_max", "Max RPM"),
        ("max_torque_ft_lbs", "Max Torque"),
        ("tool_length_in", "Tool Length"),
        ("weight_lbs", "Weight"),
        ("brushless", "Brushless"),
        ("variable_speed", "Variable Speed"),
        ("led_light", "LED Light"),
        ("fw_rev_switch", "FW / REV Switch"),
        ("extended_reach", "Extended Reach"),
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
            "variable_speed",
            "led_light",
            "fw_rev_switch",
            "extended_reach",
        }
    ),
    detail_fields=(
        ("Series", "series_display"),
        ("Power Source", "power_source"),
        ("Voltage System", "voltage_system"),
        ("Drive Size", "drive_size_display"),
        ("Head Type", "head_type"),
        ("No Load Speed", "no_load_speed"),
        ("Max RPM", "rpm_max"),
        ("Max Torque", "max_torque_ft_lbs"),
        ("Tool Length", "tool_length_in"),
        ("Weight", "weight_lbs"),
        ("Brushless", "brushless"),
        ("Variable Speed", "variable_speed"),
        ("LED Light", "led_light"),
        ("FW / REV Switch", "fw_rev_switch"),
        ("Extended Reach", "extended_reach"),
    ),
    ids=build_family_ids("ratchets"),
    load_snapshot=load_ratchet_snapshot,
    load_rows=load_ratchets,
    build_display_rows=build_display_rows,
    compare_display_value=compare_display_value,
    build_master_column_defs=build_master_column_defs,
    build_stat_cards=build_stat_cards,
)
