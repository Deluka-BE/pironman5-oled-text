"""Numeric controls for Pironman."""

from __future__ import annotations

from homeassistant.components.number import NumberEntity, NumberMode

from .entity import PironmanEntity


async def async_setup_entry(hass, entry, async_add_entities) -> None:
    async_add_entities([PironmanRgbSpeed(entry.runtime_data, entry.entry_id)])


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

