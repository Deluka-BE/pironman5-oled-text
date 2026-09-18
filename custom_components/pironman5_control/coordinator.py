"""Update coordinator for Pironman state."""

from __future__ import annotations

from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import PironmanApi, PironmanApiError
from .const import DOMAIN, UPDATE_INTERVAL_SECONDS


class PironmanCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Fetch the state exposed by the existing Pironman dashboard API."""

    def __init__(self, hass: HomeAssistant, api: PironmanApi) -> None:
        super().__init__(hass, logger=__import__("logging").getLogger(DOMAIN), name=DOMAIN, update_interval=timedelta(seconds=UPDATE_INTERVAL_SECONDS))
        self.api = api

    async def _async_update_data(self) -> dict[str, Any]:
        try:
            config, oled = await self.api.async_get("get-config"), await self.api.async_get("get-oled-text")
        except PironmanApiError as err:
            raise UpdateFailed(str(err)) from err
        system = config.get("system", {}) if isinstance(config, dict) else {}
        return {"system": system, "oled": oled if isinstance(oled, dict) else {}}

    async def async_set_rgb(self, endpoint: str, payload: dict[str, Any]) -> None:
        await self.api.async_post(endpoint, payload)
        await self.async_request_refresh()

    async def async_set_oled_enabled(self, enabled: bool) -> None:
        await self.api.async_post("set-oled-enable", {"enable": enabled})
        await self.async_request_refresh()

    async def async_set_oled_text(self, message: dict[str, Any]) -> None:
        await self.api.async_post("set-oled-text", message)
        await self.async_request_refresh()

    async def async_clear_oled_text(self) -> None:
        await self.api.async_post("clear-oled-text", {})
        await self.async_request_refresh()

