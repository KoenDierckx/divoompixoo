"""Divoom Pixoo integration."""
from __future__ import annotations

import logging

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DIVOOM_PIXOO_CONFIG, DOMAIN
from .coordinator import DivoomPixooConfig, DivoomPixooDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.LIGHT, Platform.SIREN, Platform.SELECT]

RUN_COMMANDS_SCHEMA: vol.Schema = vol.Schema({vol.Required("command_list")})


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up our integration for a Divoom Pixoo device based on a config entry.

    The config entry is the minimal config data we need to instantiate this integrations
    The initial config entry is created using our config flow, but after that will be returned from a saved copy by HA
    In our case this is the unique serial id of our device and it's last known ip
    """

    # The hass.data, is a dictionary that components can use to store and pass data along, using their integration domain as a key
    hass.data.setdefault(DOMAIN, {})

    # Initialize this config entry (a device) within our domain if needed
    hass.data[DOMAIN].setdefault(config_entry.entry_id, {})

    # From the stored config entry, recreate the DivoomPixooConfig (to get a nice typesafe object and not a dict)
    divoom_pixoo_config: DivoomPixooConfig = DivoomPixooConfig(
        **config_entry.data[DIVOOM_PIXOO_CONFIG]
    )
    # With that device data, create our coordinator object and store it on the central hass.data, to share it with all our platforms and their entity instances
    # The coordinator will be the central shared code that does the actual api calls to our device
    coordinator: DivoomPixooDataUpdateCoordinator = DivoomPixooDataUpdateCoordinator(
        hass=hass, divoom_pixoo_config=divoom_pixoo_config
    )
    hass.data[DOMAIN][config_entry.entry_id] = coordinator
    # And have it fetch the first live device data
    await coordinator.async_config_entry_first_refresh()

    # No we can ask our platforms to create their entities
    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a specific Divoom Pixoo device, and all its platorms with their entities."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
