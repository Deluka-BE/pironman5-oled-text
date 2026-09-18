"""Shared entity helpers."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import PironmanCoordinator
from .const import DOMAIN


class PironmanEntity(CoordinatorEntity[PironmanCoordinator]):
    """Base entity with one coherent Pironman device in Home Assistant."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: PironmanCoordinator, entry_id: str) -> None:
        super().__init__(coordinator)
        self._entry_id = entry_id
        self._attr_device_info = DeviceInfo(identifiers={(DOMAIN, entry_id)}, name="Pironman 5", manufacturer="SunFounder", model="Pironman 5")

    @property
    def system(self) -> dict:
        return self.coordinator.data.get("system", {})

    @property
    def oled(self) -> dict:
        return self.coordinator.data.get("oled", {})

