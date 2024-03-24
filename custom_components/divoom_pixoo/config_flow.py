"""Divoom Pixoo Config flow."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow
from homeassistant.const import CONF_DEVICE
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.selector import (
    SelectOptionDict,
    SelectSelector,
    SelectSelectorConfig,
)

from .const import DIVOOM_PIXOO_CONFIG, DOMAIN
from .coordinator import DivoomPixooConfig, DivoomPixooDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


class DivoomPixooConfigFlow(ConfigFlow, domain=DOMAIN):
    """Divoom Pixoo Config flow."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the DivoomPixooConfigFlow class."""
        self._discovered_devices: dict[str, DivoomPixooConfig] | None = None

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """When a user add a new device via the user interface. (i.e. adds this integration the first time, or adds a new device to it)."""
        errors: dict[str, str] = {}
        # Query the Divoom API to find the local devices
        if self._discovered_devices is None:
            try:
                self._discovered_devices: dict[
                    str, DivoomPixooConfig
                ] = await DivoomPixooDataUpdateCoordinator.async_discover_divoom_devices(
                    hass=self.hass
                )
            except Exception as exception:
                _LOGGER.exception("Unknown exception %s", exception)
                return self.async_abort(reason="unknown")

        # Show possible devices to the user
        if user_input is None:
            if len(self._discovered_devices) <= 0:
                return self.async_abort(reason="no_devices_found")

            devices_as_options: list[SelectOptionDict] = [
                SelectOptionDict(
                    value=device_id,
                    label=f"{device.name} ({device.id}), IP: {device.ip}, MAC: {device.mac}",
                )
                for device_id, device in self._discovered_devices.values()
            ]
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(
                    {
                        vol.Required(CONF_DEVICE): SelectSelector(
                            SelectSelectorConfig(options=devices_as_options, sort=True)
                        )
                    }
                ),
                errors=errors,
            )

        # selected device id
        device_id: str = user_input[CONF_DEVICE]
        divoom_pixoo_config: DivoomPixooConfig = self._discovered_devices[device_id]

        # Ensure we don't add duplicates
        await self.async_set_unique_id(device_id)
        # Update device data, in case it has changed (i.e. the name or ip address has changed, and we reconfigured it)
        self._abort_if_unique_id_configured(
            updates={DIVOOM_PIXOO_CONFIG: vars(divoom_pixoo_config)},
            error="already_configured",
        )

        # Create entry with chosen device
        return self.async_create_entry(
            title=divoom_pixoo_config.name,
            description=f"ID: {divoom_pixoo_config.id}, MAC: {divoom_pixoo_config.mac}, IP: {divoom_pixoo_config.ip}",
            data={DIVOOM_PIXOO_CONFIG: vars(divoom_pixoo_config)},
        )
