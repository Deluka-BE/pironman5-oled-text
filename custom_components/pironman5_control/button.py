"""One-tap OLED actions."""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity

from .entity import PironmanEntity


async def async_setup_entry(hass, entry, async_add_entities) -> None:
    async_add_entities([PironmanOledClearButton(entry.runtime_data, entry.entry_id)])


class PironmanOledClearButton(PironmanEntity, ButtonEntity):
    """Return from the custom overlay to the normal Pironman status screen."""

    _attr_name = "OLED clear"
    _attr_icon = "mdi:monitor-off"

    def __init__(self, coordinator, entry_id) -> None:
        super().__init__(coordinator, entry_id)
        self._attr_unique_id = f"{entry_id}_oled_clear"

    async def async_press(self) -> None:
        await self.coordinator.async_clear_oled_text()

