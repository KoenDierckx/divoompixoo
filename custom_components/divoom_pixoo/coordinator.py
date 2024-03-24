"""Divoom Pixoo Coordinator."""
from asyncio import timeout
from dataclasses import dataclass
from datetime import timedelta
import logging
from typing import Any, Final

from bidict import frozenbidict
from pixoo import Pixoo, find_device
from pixoo.config import PixooConfig
from pixoo.exceptions import InvalidApiResponse, NoPixooDevicesFound

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .pixoo_effects import CHANNEL_INDEX_FACES_DICT

SCAN_INTERVAL = timedelta(seconds=60)

_LOGGER = logging.getLogger(__name__)


# Keys from Divoom API
# http://docin.divoom-gz.com/web/#/5/25
API_DEVICE_ID: Final = "DeviceId"
API_DEVICE_MAC: Final = "DeviceMac"
API_DEVICE_NAME: Final = "DeviceName"
API_DEVICE_IP: Final = "DevicePrivateIP"
API_DEVICE_HARDWARE: Final = "Hardware"


@dataclass
class DivoomPixooConfig:
    """Divoom Pixoo Config."""

    id: str | None = None
    mac: str | None = None
    name: str | None = None
    ip: str | None = None
    hardware: int | None = None


@dataclass
class DivoomPixooData:
    """Divoom Pixoo Data."""

    screen_state: int | None = None
    screen_brightness: str | None = None
    screen_effect: str | None = None
    screen_effect_list: list[str] | None = None
    # rotation: int | None = None
    # clock_duration: int | None = None
    # gallery_duration: int | None = None
    # single_gallery_duration: int | None = None
    # gallery_show_time_flag: int | None = None
    # power_on_channel_id: int | None = None
    cur_clock_id: int | None = None
    hour_mode: int | None = None
    temperature_mode: int | None = None
    rotation_mode: int | None = None
    mirror_mode: int | None = None


class DivoomPixooDataUpdateCoordinator(DataUpdateCoordinator[DivoomPixooData]):
    """Divoom Pixoo Coordinator."""

    @classmethod
    async def async_discover_divoom_devices(
        cls, hass: HomeAssistant
    ) -> dict[str, DivoomPixooConfig]:
        """Discover all devices using the online Pixoo API.

        http://docin.divoom-gz.com/web/#/5/25

        NOTE: This is the only way to get the divoom pixoo config data for a device !
        Did a feature request to Divoom for a local api call to get this information, but until then we need this external request.
        """
        try:
            device_list: list[dict[str, Any]] = await hass.async_add_executor_job(
                find_device.get_pixoo_devices
            )
            devices: dict[str, DivoomPixooConfig] = {
                str(device[API_DEVICE_ID]): DivoomPixooConfig(
                    id=str(device[API_DEVICE_ID]),
                    mac=str(device[API_DEVICE_MAC]),
                    name=str(device[API_DEVICE_NAME]),
                    ip=str(device[API_DEVICE_IP]),
                    hardware=str(device[API_DEVICE_HARDWARE]),
                )
                for device in device_list
            }
            return devices
        except NoPixooDevicesFound:
            _LOGGER.warning("No Divoom Pixoo devices found")
            return {}
        except Exception as exception:
            _LOGGER.exception("Unknown exception %s", exception)
            raise Exception from exception

    def __init__(
        self, hass: HomeAssistant, divoom_pixoo_config: DivoomPixooConfig
    ) -> None:
        """Initialize the DivoomPixooDataUpdateCoordinator class."""
        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name=divoom_pixoo_config.name,
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=SCAN_INTERVAL,
        )
        _LOGGER.debug("Creating coordinator: %s", divoom_pixoo_config)
        self.divoom_pixoo_config: DivoomPixooConfig = divoom_pixoo_config
        self.pixoo: Pixoo = None

        self.screen_effect_dict: frozenbidict[str, int] = CHANNEL_INDEX_FACES_DICT
        self.screen_effect_list: list[str] = list(CHANNEL_INDEX_FACES_DICT)

    def init_pixoo(self) -> None:
        """Init Divoom Pixoo API client library."""
        self.pixoo: Pixoo = Pixoo(
            pixoo_config=PixooConfig(address=self.divoom_pixoo_config.ip)
        )

    async def _async_update_data(self) -> DivoomPixooData:
        """Update Divoom Pixoo data using API client."""
        _LOGGER.debug("Updating divoom device: %s", self.divoom_pixoo_config)

        # This is the place to pre-process the data to lookup tables so entities can quickly look up their data.
        try:
            # Note: asyncio.TimeoutError and aiohttp.ClientError are already handled by the data update coordinator.
            async with timeout(10):
                # Init pixoo
                if self.pixoo is None:
                    await self.hass.async_add_executor_job(self.init_pixoo)

                # Grab active context variables to limit data required to be fetched from API
                # Note: using context is not required if there is no need or ability to limit data retrieved from API.
                # listening_idx = set(self.async_contexts())

                result: dict[str, Any] = await self.hass.async_add_executor_job(
                    self.pixoo.get_settings
                )

        except ConfigEntryNotReady as exception:
            raise UpdateFailed from exception
        except InvalidApiResponse as exception:
            raise UpdateFailed from exception

        # Convert CurClockId into 'effect' name, from mapping dict if it is in there, otherwise generate
        divoom_pixoo_data: DivoomPixooData = DivoomPixooData(
            screen_state=result["LightSwitch"],
            screen_brightness=result["Brightness"],
            # cur_clock_id=result["CurClockId"],
            screen_effect=self.screen_effect_dict.inverse[result["CurClockId"]],
            # power_on_channel_id=result["PowerOnChannelId"],
            # rotation=result["RotationFlag"],
            # clock_duration=result["ClockTime"],
            # gallery_duration=result["GalleryTime"],
            # single_gallery_duration=result["SingleGalleyTime"],
            # gallery_show_time_flag=result["GalleryShowTimeFlag"],
            hour_mode=result["Time24Flag"],
            temperature_mode=result["TemperatureMode"],
            rotation_mode=result["GyrateAngle"],
            mirror_mode=result["MirrorFlag"],
        )
        return divoom_pixoo_data

    # Convenience wrappers around api send_command's (perhaps we can create a PR on the pixoo code later on)
    def play_buzzer(
        self,
        play_total_time: int = 3000,
        active_time_in_cycle: int = 500,
        off_time_in_cycle: int = 500,
    ) -> None:
        """Play buzzer."""
        _LOGGER.debug("Play buzzer for %s ms", play_total_time)
        self.pixoo.send_command(
            command="Device/PlayBuzzer",
            active_time_in_cycle=active_time_in_cycle,
            off_time_in_cycle=off_time_in_cycle,
            play_total_time=play_total_time,
        )

    def set_hour_mode(self, hour_mode: int) -> None:
        """Set hour mode."""
        _LOGGER.debug("Set hour mode %s ms", hour_mode)
        self.pixoo.send_command(command="Device/SetTime24Flag", mode=hour_mode)

    def set_temperature_mode(self, temperature_mode: int) -> None:
        """Set temperature mode."""
        _LOGGER.debug("Set temperature mode %s ms", temperature_mode)
        self.pixoo.send_command(command="Device/SetDisTempMode", mode=temperature_mode)

    def set_mirror_mode(self, mirror_mode: int) -> None:
        """Set mirror mode."""
        _LOGGER.debug("Set mirror mode %s ms", mirror_mode)
        self.pixoo.send_command(command="Device/SetMirrorMode", mode=mirror_mode)

    def set_rotation_mode(self, rotation_mode: int) -> None:
        """Set rotation mode."""
        _LOGGER.debug("Set rotation mode %s ms", rotation_mode)
        self.pixoo.send_command(
            command="Device/SetScreenRotationAngle", mode=rotation_mode
        )
