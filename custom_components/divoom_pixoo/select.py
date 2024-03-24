"""Divoom Pixoo Select platform."""
from __future__ import annotations

import logging

from bidict import frozenbidict

from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import DivoomPixooDataUpdateCoordinator
from .entity import DivoomPixooEntity

_LOGGER = logging.getLogger(__name__)

HOUR_MODE_OPTIONS: frozenbidict[str, int] = frozenbidict(
    {
        "hour_mode_24": 1,
        "hour_mode_12": 0,
    }
)

TEMPERATURE_MODE_OPTIONS: frozenbidict[str, int] = frozenbidict(
    {
        "temperature_mode_celcius": 0,
        "temperature_mode_fahrenheit": 1,
    }
)

MIRROR_MODE_OPTIONS: frozenbidict[str, int] = frozenbidict(
    {
        "mirror_mode_disable": 0,
        "mirror_mode_enable": 1,
    }
)
ROTATION_MODE_OPTIONS: frozenbidict[str, int] = frozenbidict(
    {
        "rotation_mode_0": 0,
        "rotation_mode_90": 1,
        "rotation_mode_180": 2,
        "rotation_mode_270": 3,
    }
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up select entities."""
    coordinator: DivoomPixooDataUpdateCoordinator = hass.data[DOMAIN][
        config_entry.entry_id
    ]

    divoom_select_entity_hour: DivoomPixooSelectEntityHour = (
        DivoomPixooSelectEntityHour(
            coordinator=coordinator,
            description=SelectEntityDescription(
                key="hour_mode",
                translation_key="hour_mode",
                options=list(HOUR_MODE_OPTIONS),
                entity_category=EntityCategory.CONFIG,
            ),
        )
    )
    divoom_select_entity_temperature: DivoomPixooSelectEntityTemperature = (
        DivoomPixooSelectEntityTemperature(
            coordinator=coordinator,
            description=SelectEntityDescription(
                key="temperature_mode",
                translation_key="temperature_mode",
                options=list(TEMPERATURE_MODE_OPTIONS),
                entity_category=EntityCategory.CONFIG,
            ),
        )
    )
    divoom_select_entity_mirror: DivoomPixooSelectEntityMirror = (
        DivoomPixooSelectEntityMirror(
            coordinator=coordinator,
            description=SelectEntityDescription(
                key="mirror_mode",
                translation_key="mirror_mode",
                options=list(MIRROR_MODE_OPTIONS),
                entity_category=EntityCategory.CONFIG,
            ),
        )
    )
    divoom_select_entity_rotation: DivoomPixooSelectEntityRotation = (
        DivoomPixooSelectEntityRotation(
            coordinator=coordinator,
            description=SelectEntityDescription(
                key="rotation_mode",
                translation_key="rotation_mode",
                options=list(ROTATION_MODE_OPTIONS),
                entity_category=EntityCategory.CONFIG,
            ),
        )
    )

    async_add_entities(
        [
            divoom_select_entity_hour,
            divoom_select_entity_temperature,
            divoom_select_entity_mirror,
            divoom_select_entity_rotation,
        ]
    )


class DivoomPixooSelectEntity(DivoomPixooEntity, SelectEntity):
    """Divoom Pixoo Select Entity."""

    _attr_has_entity_name = True


class DivoomPixooSelectEntityHour(DivoomPixooSelectEntity):
    """Divoom Pixoo Select Entity for Hour Mode."""

    @property
    def current_option(self) -> str | None:
        """Return the currently selected option."""
        hour_mode: str = HOUR_MODE_OPTIONS.inverse[self.coordinator.data.hour_mode]
        _LOGGER.debug(
            "Get hour mode: HA %s / Device %s",
            hour_mode,
            self.coordinator.data.hour_mode,
        )
        return hour_mode

    async def async_select_option(self, option: str) -> None:
        """Update the current selected option."""
        self._attr_current_option = option
        _LOGGER.debug(
            "Set hour mode: HA %s Device %s", option, HOUR_MODE_OPTIONS[option]
        )
        await self.hass.async_add_executor_job(
            self.coordinator.set_hour_mode, HOUR_MODE_OPTIONS[option]
        )
        await self.coordinator.async_refresh()


class DivoomPixooSelectEntityTemperature(DivoomPixooSelectEntity):
    """Divoom Pixoo Select Entity for Temperature Mode."""

    @property
    def current_option(self) -> str | None:
        """Return the currently selected option."""
        temperature_mode: str = TEMPERATURE_MODE_OPTIONS.inverse[
            self.coordinator.data.temperature_mode
        ]
        _LOGGER.debug(
            "Get temperature mode: HA %s / Device %s",
            temperature_mode,
            self.coordinator.data.temperature_mode,
        )
        return temperature_mode

    async def async_select_option(self, option: str) -> None:
        """Update the current selected option."""
        self._attr_current_option = option
        _LOGGER.debug(
            "Set temperature mode: HA %s Device %s",
            option,
            TEMPERATURE_MODE_OPTIONS[option],
        )
        await self.hass.async_add_executor_job(
            self.coordinator.set_temperature_mode, TEMPERATURE_MODE_OPTIONS[option]
        )
        await self.coordinator.async_refresh()


class DivoomPixooSelectEntityMirror(DivoomPixooSelectEntity):
    """Divoom Pixoo Select Entity for Mirror Mode."""

    @property
    def current_option(self) -> str | None:
        """Return the currently selected option."""
        mirror_mode: str = MIRROR_MODE_OPTIONS.inverse[
            self.coordinator.data.mirror_mode
        ]
        _LOGGER.debug(
            "Get mirror mode: HA %s / Device %s",
            mirror_mode,
            self.coordinator.data.mirror_mode,
        )
        return mirror_mode

    async def async_select_option(self, option: str) -> None:
        """Update the current selected option."""
        self._attr_current_option = option
        _LOGGER.debug(
            "Set mirror mode: HA %s Device %s",
            option,
            MIRROR_MODE_OPTIONS[option],
        )
        await self.hass.async_add_executor_job(
            self.coordinator.set_mirror_mode, MIRROR_MODE_OPTIONS[option]
        )
        await self.coordinator.async_refresh()


class DivoomPixooSelectEntityRotation(DivoomPixooSelectEntity):
    """Divoom Pixoo Select Entity for Rotation Mode."""

    @property
    def current_option(self) -> str | None:
        """Return the currently selected option."""
        rotation_mode: str = ROTATION_MODE_OPTIONS.inverse[
            self.coordinator.data.rotation_mode
        ]
        _LOGGER.debug(
            "Get rotation mode: HA %s / Device %s",
            rotation_mode,
            self.coordinator.data.rotation_mode,
        )
        return rotation_mode

    async def async_select_option(self, option: str) -> None:
        """Update the current selected option."""
        self._attr_current_option = option
        _LOGGER.debug(
            "Set rotation mode: HA %s Device %s",
            option,
            ROTATION_MODE_OPTIONS[option],
        )
        await self.hass.async_add_executor_job(
            self.coordinator.set_rotation_mode, ROTATION_MODE_OPTIONS[option]
        )
        await self.coordinator.async_refresh()
