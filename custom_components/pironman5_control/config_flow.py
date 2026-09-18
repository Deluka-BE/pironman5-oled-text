"""Config flow for Pironman 5 Control."""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .api import PironmanApi, PironmanApiError
from .const import CONF_HOST, CONF_PORT, DEFAULT_PORT, DOMAIN


class PironmanConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Add the Pironman app by its Home Assistant hostname."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        errors = {}
        if user_input is not None:
            try:
                await PironmanApi(self.hass, user_input[CONF_HOST], user_input[CONF_PORT]).async_get("test")
            except PironmanApiError:
                errors["base"] = "cannot_connect"
            else:
                await self.async_set_unique_id(f"{user_input[CONF_HOST]}:{user_input[CONF_PORT]}")
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title="Pironman 5", data=user_input)
        schema = vol.Schema({vol.Required(CONF_HOST, default="8639c588-pironman5-text"): str, vol.Required(CONF_PORT, default=DEFAULT_PORT): vol.Coerce(int)})
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

