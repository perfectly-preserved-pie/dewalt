from __future__ import annotations


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
MULTI_FILTER = "agMultiColumnFilter"
BOOLEAN_FILTER = SET_FILTER

COMPARE_FIELDS = [
    ("sku", "SKU"),
    ("title", "Model"),
    ("series", "Series"),
    ("power_source", "Power Source"),
    ("voltage_system", "Voltage System"),
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

COMPARE_BOOLEAN_FIELDS = {
    "brushless",
    "variable_speed",
    "anti_rotation_system",
    "e_clutch",
    "kickback_brake",
    "wireless_tool_control",
    "tool_connect_ready",
    "power_loss_reset",
    "no_volt_switch",
    "lanyard_ready",
}
