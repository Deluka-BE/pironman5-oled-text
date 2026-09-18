"""RGB light entity."""

from __future__ import annotations

from homeassistant.components.light import ATTR_BRIGHTNESS, ATTR_EFFECT, ATTR_RGB_COLOR, ColorMode, LightEntity

from .const import RGB_STYLES
from .entity import PironmanEntity


async def async_setup_entry(hass, entry, async_add_entities) -> None:
    async_add_entities([PironmanRgbLight(entry.runtime_data, entry.entry_id)])


class PironmanRgbLight(PironmanEntity, LightEntity):
    """Control the four WS2812 LEDs as one Home Assistant light."""

    _attr_name = "RGB"
    _attr_icon = "mdi:led-strip-variant"
    _attr_supported_color_modes = {ColorMode.RGB}
    _attr_color_mode = ColorMode.RGB
    _attr_effect_list = RGB_STYLES

    def __init__(self, coordinator, entry_id) -> None:
        super().__init__(coordinator, entry_id)
        self._attr_unique_id = f"{entry_id}_rgb"

    @property
    def is_on(self) -> bool:
        return bool(self.system.get("rgb_enable", False))

    @property
    def brightness(self) -> int | None:
        value = self.system.get("rgb_brightness")
        return round(max(0, min(100, value)) * 255 / 100) if isinstance(value, (int, float)) else None

    @property
    def rgb_color(self) -> tuple[int, int, int] | None:
        value = self.system.get("rgb_color")
        if not isinstance(value, str) or len(value.lstrip("#")) != 6:
            return None
        try:
            color = value.lstrip("#")
            return tuple(int(color[index:index + 2], 16) for index in (0, 2, 4))
        except ValueError:
            return None

    @property
    def effect(self) -> str | None:
        return self.system.get("rgb_style")

    async def async_turn_on(self, **kwargs) -> None:
        await self.coordinator.async_set_rgb("set-rgb-enable", {"enable": True})
        if ATTR_BRIGHTNESS in kwargs:
            await self.coordinator.async_set_rgb("set-rgb-brightness", {"brightness": round(kwargs[ATTR_BRIGHTNESS] * 100 / 255)})
        if ATTR_RGB_COLOR in kwargs:
            rgb = kwargs[ATTR_RGB_COLOR]
            await self.coordinator.async_set_rgb("set-rgb-color", {"color": "#{:02x}{:02x}{:02x}".format(*rgb)})
        if ATTR_EFFECT in kwargs:
            await self.coordinator.async_set_rgb("set-rgb-style", {"style": kwargs[ATTR_EFFECT]})

    async def async_turn_off(self, **kwargs) -> None:
        await self.coordinator.async_set_rgb("set-rgb-enable", {"enable": False})

