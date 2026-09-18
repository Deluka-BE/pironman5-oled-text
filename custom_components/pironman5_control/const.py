"""Constants for the Pironman 5 Control integration."""

from typing import Final

DOMAIN: Final = "pironman5_control"
PLATFORMS: Final = ["light", "switch", "select", "number", "text", "button"]
CONF_HOST: Final = "host"
CONF_PORT: Final = "port"
DEFAULT_PORT: Final = 34001
API_PREFIX: Final = "/api/v1.0"
UPDATE_INTERVAL_SECONDS: Final = 10
RGB_STYLES: Final = (
    "solid",
    "breathing",
    "flow",
    "flow_reverse",
    "rainbow",
    "rainbow_reverse",
    "hue_cycle",
)
OLED_ICONS: Final = ("none", "home", "heart", "thermometer", "bulb", "check", "warning", "wifi", "fan", "spinner")
OLED_ANIMATIONS: Final = ("none", "blink", "pulse", "spin")
OLED_SIZES: Final = ("8", "12", "16", "24")

