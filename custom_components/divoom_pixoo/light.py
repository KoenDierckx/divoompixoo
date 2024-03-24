"""Divoom Pixoo Light platform."""
import logging
import math
from typing import Any

from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_EFFECT,
    ColorMode,
    LightEntity,
    LightEntityDescription,
    LightEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util.percentage import (
    percentage_to_ranged_value,
    ranged_value_to_percentage,
)

from .const import DOMAIN
from .coordinator import DivoomPixooDataUpdateCoordinator
from .entity import DivoomPixooEntity

_LOGGER = logging.getLogger(__name__)

BRIGHTNESS_SCALE = (0, 255)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up light entities."""
    coordinator: DivoomPixooDataUpdateCoordinator = hass.data[DOMAIN][
        config_entry.entry_id
    ]
    divoom_light_entity = DivoomPixooLightEntity(
        coordinator=coordinator,
        description=LightEntityDescription(
            key="screen", name="screen_name", translation_key="screen"
        ),
    )
    async_add_entities([divoom_light_entity], update_before_add=True)


class DivoomPixooLightEntity(DivoomPixooEntity, LightEntity):
    """Divoom Pixoo Light Entity."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: DivoomPixooDataUpdateCoordinator,
        description: LightEntityDescription,
    ) -> None:
        """Initialize the DivoomPixooLightEntity class."""
        super().__init__(coordinator=coordinator, description=description)
        # INIT DEFAULTS BEFORE UPDATE
        # https://developers.home-assistant.io/docs/core/entity/light#color-modes
        self._attr_color_mode = ColorMode.BRIGHTNESS
        self._attr_supported_color_modes = {ColorMode.ONOFF, ColorMode.BRIGHTNESS}
        self._attr_supported_features = LightEntityFeature.EFFECT

    @property
    def is_on(self) -> bool | None:
        """Return whether this light is on or off."""
        _LOGGER.debug("Get is_on: %s", self.coordinator.data.screen_state > 0)
        return self.coordinator.data.screen_state > 0

    @property
    def brightness(self) -> int | None:
        """Return brightness."""
        ha_brightness: float = percentage_to_ranged_value(
            BRIGHTNESS_SCALE, self.coordinator.data.screen_brightness
        )
        _LOGGER.debug(
            "Get brightness: HA %s / Device %s",
            ha_brightness,
            self.coordinator.data.screen_brightness,
        )
        return ha_brightness

    @property
    def effect(self) -> str | None:
        """Return the current effect."""
        _LOGGER.debug("Get effect: %s", self.coordinator.data.screen_effect)
        return self.coordinator.data.screen_effect

    @property
    def effect_list(self) -> list[str]:
        """Return the list of saved effects."""
        return self.coordinator.screen_effect_list

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the device on."""
        _LOGGER.debug("Do turn_on")

        if ATTR_EFFECT in kwargs:
            clock_id: int = self.coordinator.screen_effect_dict[kwargs[ATTR_EFFECT]]
            _LOGGER.debug(
                "Set effect: HA %s / Device %s",
                kwargs[ATTR_EFFECT],
                clock_id,
            )
            await self.hass.async_add_executor_job(
                self.coordinator.pixoo.set_clock, clock_id
            )

        if ATTR_BRIGHTNESS in kwargs:
            device_brightness: int = math.ceil(
                ranged_value_to_percentage(BRIGHTNESS_SCALE, kwargs[ATTR_BRIGHTNESS])
            )
            _LOGGER.debug(
                "Set brightness: HA %s / Device %s",
                kwargs[ATTR_BRIGHTNESS],
                device_brightness,
            )
            await self.hass.async_add_executor_job(
                self.coordinator.pixoo.set_brightness, device_brightness
            )

        await self.hass.async_add_executor_job(self.coordinator.pixoo.set_screen_on)
        await self.coordinator.async_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn device off."""
        _LOGGER.debug("Do turn_off")
        await self.hass.async_add_executor_job(self.coordinator.pixoo.set_screen_off)
        await self.coordinator.async_refresh()
