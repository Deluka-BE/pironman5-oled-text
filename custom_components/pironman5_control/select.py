"""Selectors that modify the currently visible OLED message."""

from __future__ import annotations

from homeassistant.components.select import SelectEntity

from .const import OLED_ANIMATIONS, OLED_ICONS, OLED_SIZES, RGB_STYLES
from .entity import PironmanEntity


async def async_setup_entry(hass, entry, async_add_entities) -> None:
    coordinator = entry.runtime_data
    async_add_entities([
        PironmanRgbEffect(coordinator, entry.entry_id),
        PironmanOledOption(coordinator, entry.entry_id, "icon", "OLED icon", OLED_ICONS),
        PironmanOledOption(coordinator, entry.entry_id, "animation", "OLED animation", OLED_ANIMATIONS),
        PironmanOledOption(coordinator, entry.entry_id, "font_size", "OLED text size", OLED_SIZES),
    ])


class PironmanRgbEffect(PironmanEntity, SelectEntity):
    _attr_name = "RGB effect"
    _attr_options = RGB_STYLES
    _attr_icon = "mdi:palette"

    def __init__(self, coordinator, entry_id) -> None:
        super().__init__(coordinator, entry_id)
        self._attr_unique_id = f"{entry_id}_rgb_effect"

    @property
    def current_option(self) -> str | None:
        return self.system.get("rgb_style")

    async def async_select_option(self, option: str) -> None:
        await self.coordinator.async_set_rgb("set-rgb-style", {"style": option})


class PironmanOledOption(PironmanEntity, SelectEntity):
    """Change a setting of the active temporary OLED message."""

    def __init__(self, coordinator, entry_id, field, name, options) -> None:
        super().__init__(coordinator, entry_id)
        self._field = field
        self._attr_name = name
        self._attr_options = options
        self._attr_unique_id = f"{entry_id}_oled_{field}"

    @property
    def current_option(self) -> str | None:
        value = self.oled.get(self._field)
        if self._field == "icon" and value is None:
            return "none"
        return str(value) if value is not None else None

    async def async_select_option(self, option: str) -> None:
        if not self.oled.get("active"):
            return
        message = dict(self.oled)
        message.pop("active", None)
        message.pop("enabled", None)
        message.pop("remaining", None)
        message["lines"] = self.oled.get("lines", [])
        message["duration"] = self.oled.get("remaining") or 0
        message[self._field] = None if self._field == "icon" and option == "none" else (int(option) if self._field == "font_size" else option)
        await self.coordinator.async_set_oled_text(message)

