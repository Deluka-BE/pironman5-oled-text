"""Text input entity for the existing OLED overlay."""

from __future__ import annotations

from homeassistant.components.text import TextEntity, TextMode

from .entity import PironmanEntity


async def async_setup_entry(hass, entry, async_add_entities) -> None:
    async_add_entities([PironmanOledText(entry.runtime_data, entry.entry_id)])


class PironmanOledText(PironmanEntity, TextEntity):
    """Write up to four lines to the OLED using the current display options."""

    _attr_name = "OLED text"
    _attr_icon = "mdi:message-text"
    _attr_mode = TextMode.TEXT
    _attr_native_max = 320

    def __init__(self, coordinator, entry_id) -> None:
        super().__init__(coordinator, entry_id)
        self._attr_unique_id = f"{entry_id}_oled_text"

    @property
    def native_value(self) -> str:
        return "\n".join(self.oled.get("lines", []))

    async def async_set_value(self, value: str) -> None:
        lines = value.splitlines() or [""]
        # The underlying app rejects empty lines-only content; its icon remains usable.
        lines = [line for line in lines if line]
        if not lines:
            await self.coordinator.async_clear_oled_text()
            return
        previous = self.oled
        message = {
            "lines": lines,
            "duration": previous.get("remaining") or 0,
            "font_size": previous.get("font_size", 8),
            "icon": previous.get("icon"),
            "animation": previous.get("animation", "none"),
        }
        await self.coordinator.async_set_oled_text(message)

