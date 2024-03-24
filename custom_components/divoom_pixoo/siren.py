"""Divoom Pixoo Siren platform."""
from __future__ import annotations

from collections.abc import Callable
from datetime import datetime, timedelta
import logging
from typing import Any

from homeassistant.components.siren import (
    ATTR_DURATION,
    SirenEntity,
    SirenEntityDescription,
    SirenEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import event
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import DivoomPixooDataUpdateCoordinator
from .entity import DivoomPixooEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up siren entities."""
    coordinator: DivoomPixooDataUpdateCoordinator = hass.data[DOMAIN][
        config_entry.entry_id
    ]
    divoom_siren_entity: DivoomPixooSirenEntity = DivoomPixooSirenEntity(
        coordinator=coordinator,
        description=SirenEntityDescription(
            key="siren", name="siren_name", translation_key="siren"
        ),
    )
    async_add_entities([divoom_siren_entity])


class DivoomPixooSirenEntity(DivoomPixooEntity, SirenEntity):
    """Divoom Pixoo Siren entity.

    There is no turn off support on the device, so will use a delay listener to fake the turn off event
    """

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: DivoomPixooDataUpdateCoordinator,
        description: SirenEntityDescription,
    ) -> None:
        """Initialize the DivoomPixooSirenEntity class."""
        super().__init__(coordinator=coordinator, description=description)
        self._attr_supported_features = (
            SirenEntityFeature.TURN_ON | SirenEntityFeature.DURATION
        )
        self._attr_should_poll = False
        self._attr_is_on = False
        self._delay_listener: Callable | None = None

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the siren on."""
        _LOGGER.debug("Do turn_on")
        duration: int = kwargs.get(ATTR_DURATION, 3)
        duration_in_ms: int = duration * 1000

        self._attr_is_on = True
        self.async_write_ha_state()
        await self.hass.async_add_executor_job(
            self.coordinator.play_buzzer, duration_in_ms
        )

        _LOGGER.debug("Schedule turn_off")
        self._async_cleanup_delay_listener()
        self._async_create_turn_off_delay_listener(duration_in_ms=duration_in_ms)
        self.async_write_ha_state()

    @callback
    def _async_create_turn_off_delay_listener(self, duration_in_ms) -> None:
        """Create delay listener."""
        self._delay_listener = event.async_call_later(
            self.hass,
            timedelta(milliseconds=duration_in_ms),
            self.turn_off_callback,
        )

    @callback
    def _async_cleanup_delay_listener(self) -> None:
        """Clean up a delay listener."""
        if self._delay_listener is not None:
            self._delay_listener()
            self._delay_listener = None

    @callback
    def turn_off_callback(self, now: datetime) -> None:
        """Switch device off after a delay."""
        _LOGGER.debug("Do turn_off")
        self._attr_is_on = False
        self._delay_listener = None
        self.async_write_ha_state()
