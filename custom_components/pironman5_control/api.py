"""Local API client for the Pironman add-on."""

from __future__ import annotations

from typing import Any

from aiohttp import ClientError

from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import API_PREFIX


class PironmanApiError(Exception):
    """Raised when the Pironman API cannot complete a request."""


class PironmanApi:
    """Talk to a Pironman app over Home Assistant's internal add-on network."""

    def __init__(self, hass, host: str, port: int) -> None:
        self._session = async_get_clientsession(hass)
        self._base_url = f"http://{host}:{port}{API_PREFIX}"

    async def async_get(self, path: str) -> Any:
        return await self._async_request("get", path)

    async def async_post(self, path: str, payload: dict[str, Any]) -> Any:
        return await self._async_request("post", path, json=payload)

    async def _async_request(self, method: str, path: str, **kwargs: Any) -> Any:
        try:
            async with self._session.request(method, f"{self._base_url}/{path}", timeout=10, **kwargs) as response:
                body = await response.json(content_type=None)
        except (ClientError, TimeoutError, ValueError) as err:
            raise PironmanApiError(f"Pironman is niet bereikbaar: {err}") from err
        if response.status >= 400 or not isinstance(body, dict) or not body.get("status"):
            detail = body.get("error", response.reason) if isinstance(body, dict) else response.reason
            raise PironmanApiError(f"Pironman weigerde de opdracht: {detail}")
        return body.get("data")

