"""Pironman 5 Control integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .api import PironmanApi
from .const import CONF_HOST, CONF_PORT, PLATFORMS
from .coordinator import PironmanCoordinator

type PironmanConfigEntry = ConfigEntry[PironmanCoordinator]


async def async_setup_entry(hass: HomeAssistant, entry: PironmanConfigEntry) -> bool:
    coordinator = PironmanCoordinator(hass, PironmanApi(hass, entry.data[CONF_HOST], entry.data[CONF_PORT]))
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, [Platform(platform) for platform in PLATFORMS])
    return True


async def async_unload_entry(hass: HomeAssistant, entry: PironmanConfigEntry) -> bool:
    return await hass.config_entries.async_unload_platforms(entry, [Platform(platform) for platform in PLATFORMS])

