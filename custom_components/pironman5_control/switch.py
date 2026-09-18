"""Switches for Pironman hardware."""

from __future__ import annotations

from homeassistant.components.switch import SwitchEntity

from .entity import PironmanEntity


async def async_setup_entry(hass, entry, async_add_entities) -> None:
    async_add_entities([PironmanOledSwitch(entry.runtime_data, entry.entry_id)])


class PironmanOledSwitch(PironmanEntity, SwitchEntity):
    """Turn the physical OLED on or off without touching its content."""

    _attr_name = "OLED"
    _attr_icon = "mdi:monitor"

    def __init__(self, coordinator, entry_id) -> None:
        super().__init__(coordinator, entry_id)
        self._attr_unique_id = f"{entry_id}_oled"

    @property
    def is_on(self) -> bool:
        return bool(self.system.get("oled_enable", False))

    async def async_turn_on(self, **kwargs) -> None:
        await self.coordinator.async_set_oled_enabled(True)

    async def async_turn_off(self, **kwargs) -> None:
        await self.coordinator.async_set_oled_enabled(False)

