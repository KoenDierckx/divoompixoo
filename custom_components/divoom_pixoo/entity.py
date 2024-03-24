"""Divoom Pixoo Entity.

Generic entity, to ensure all platform entities have a unique id but still use the same DeviceInfo
"""
import logging

from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import EntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import DivoomPixooDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


class DivoomPixooEntity(CoordinatorEntity[DivoomPixooDataUpdateCoordinator]):
    """Define a generic Divoom Device entity."""

    def __init__(
        self,
        coordinator: DivoomPixooDataUpdateCoordinator,
        description: EntityDescription,
    ) -> None:
        """Initialize the DivoomPixooEntity class."""
        super().__init__(coordinator)

        self._attr_unique_id = (
            f"{self.coordinator.divoom_pixoo_config.id}-{description.key}"
        )
        self.entity_description = description

    @property
    def device_info(self) -> DeviceInfo:
        """Return device registry information for this entity.

        https://developers.home-assistant.io/docs/device_registry_index
        """
        return DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.divoom_pixoo_config.id)},
            serial_number=self.coordinator.divoom_pixoo_config.id,
            name=self.coordinator.divoom_pixoo_config.name,
            connections={
                (dr.CONNECTION_NETWORK_MAC, self.coordinator.divoom_pixoo_config.mac)
            },
            hw_version=self.coordinator.divoom_pixoo_config.hardware,
            model="Pixoo64",
            manufacturer="Divoom",
        )
