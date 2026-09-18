"""Numeric controls for Pironman."""

from __future__ import annotations

from homeassistant.components.number import NumberEntity, NumberMode

from .entity import PironmanEntity


async def async_setup_entry(hass, entry, async_add_entities) -> None:
    coordinator = entry.runtime_data
    async_add_entities([
        PironmanRgbSpeed(coordinator, entry.entry_id),
        PironmanOledDuration(coordinator, entry.entry_id),
    ])


class PironmanRgbSpeed(PironmanEntity, NumberEntity):
    """Set the speed of an RGB effect."""

    _attr_name = "RGB effect speed"
    _attr_icon = "mdi:speedometer"
    _attr_native_min_value = 0
    _attr_native_max_value = 100
    _attr_native_step = 1
    _attr_mode = NumberMode.SLIDER

    def __init__(self, coordinator, entry_id) -> None:
        super().__init__(coordinator, entry_id)
        self._attr_unique_id = f"{entry_id}_rgb_speed"

    @property
    def native_value(self) -> float | None:
        value = self.system.get("rgb_speed")
        return value if isinstance(value, (int, float)) else None

    async def async_set_native_value(self, value: float) -> None:
        await self.coordinator.async_set_rgb("set-rgb-speed", {"speed": round(value)})


class PironmanOledDuration(PironmanEntity, NumberEntity):
    """Set how long the active temporary OLED message remains visible."""

    _attr_name = "OLED duration"
    _attr_icon = "mdi:timer-outline"
    _attr_native_min_value = 0
    _attr_native_max_value = 86400
    _attr_native_step = 1
    _attr_native_unit_of_measurement = "s"
    _attr_mode = NumberMode.BOX

    def __init__(self, coordinator, entry_id) -> None:
        super().__init__(coordinator, entry_id)
        self._attr_unique_id = f"{entry_id}_oled_duration"

    @property
    def native_value(self) -> float | None:
        return self.oled.get("remaining") or 0

    async def async_set_native_value(self, value: float) -> None:
        if not self.oled.get("active"):
            return
        message = {
            "lines": self.oled.get("lines", []),
            "duration": round(value),
            "font_size": self.oled.get("font_size", 8),
            "icon": self.oled.get("icon"),
            "animation": self.oled.get("animation", "none"),
        }
        await self.coordinator.async_set_oled_text(message)

