"""Handles integration switches."""

from datetime import UTC, datetime, timedelta
import logging

from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN, JLR_DATA, SUPPORTED_SWITCH_SERVICES
from .entity import JLREntity
from .services import JLRService
from .util import get_attribute, requires_pin, to_local_datetime

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Set up Wiser climate device."""

    jlr_switches = []
    coordinator = hass.data[DOMAIN][config_entry.entry_id][JLR_DATA]  # Get Handler

    # Get list of supported services
    for vehicle in coordinator.vehicles.values():
        services = vehicle.supported_services

        _LOGGER.debug("Setting up switches for %s", vehicle.name)
        jlr_switches = [
            JLRSwitch(coordinator, vehicle.vin, service_code)
            for service_code in SUPPORTED_SWITCH_SERVICES
            if service_code in services
        ]

    async_add_entities(jlr_switches, True)


class JLRSwitch(JLREntity, SwitchEntity):
    """Button entity."""

    def __init__(
        self,
        coordinator,
        vin: str,
        service_code: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(
            coordinator,
            vin,
            SUPPORTED_SWITCH_SERVICES[service_code].get("name"),
        )
        self.service_code = service_code
        self._icon = SUPPORTED_SWITCH_SERVICES[service_code].get("icon")

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        _LOGGER.debug(
            "%s switch update requested. State is %s",
            self.name,
            self.is_on,
        )

        self.async_write_ha_state()

    @property
    def is_on(self):
        """Return the state of the switch."""
        if state_attr := SUPPORTED_SWITCH_SERVICES[self.service_code].get("state"):
            return get_attribute(self.vehicle.tracked_status, state_attr)
        return False

    async def async_turn_on(self, **kwargs):
        """Turn the device on."""
        _LOGGER.debug("Switch %s turned on", self._name)

        if (
            requires_pin(SUPPORTED_SWITCH_SERVICES, self.service_code)
            and not self.vehicle.pin
        ):
            raise HomeAssistantError("Unable to perform function.  No pin set")

        service = SUPPORTED_SWITCH_SERVICES[self.service_code].get("on_service")
        params = self.get_service_params(True)
        jlr_service = JLRService(self.coordinator, self.vin, service)

        result = await jlr_service.async_call_service(**params)
        if result:
            self._attr_is_on = True

        await self.async_force_update(delay=2)

    async def async_turn_off(self, **kwargs):
        """Turn the device off."""
        _LOGGER.debug("Switch %s turned off", self._name)
        if (
            requires_pin(SUPPORTED_SWITCH_SERVICES, self.service_code)
            and not self.vehicle.pin
        ):
            raise HomeAssistantError("Unable to perform function.  No pin set")
        service = SUPPORTED_SWITCH_SERVICES[self.service_code].get("off_service")
        params = self.get_service_params(False)
        jlr_service = JLRService(self.coordinator, self.vin, service)

        result = await jlr_service.async_call_service(**params)
        if result:
            self._attr_is_on = False

        await self.async_force_update(delay=2)

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        attrs = {}
        switch_attrs = SUPPORTED_SWITCH_SERVICES[self.service_code].get("attrs", {})
        if switch_attrs:
            for name, value in switch_attrs.items():
                value = get_attribute(self.vehicle, value)
                # Check if date and convert to local time
                if local_dt := to_local_datetime(value):
                    attrs[name] = local_dt
                else:
                    attrs[name] = value

        return attrs

    def get_service_params(self, is_turn_on: bool):
        """Get params required for service call."""
        service = SUPPORTED_SWITCH_SERVICES[self.service_code]
        params = list(service.get("params"))

        _LOGGER.debug("Service required params - %s", params)

        if is_turn_on:
            add_params = service.get("add_on_params", [])
        else:
            add_params = service.get("add_off_params", [])

        _LOGGER.debug("Service required additional params - %s", add_params)

        if add_params:
            params.extend(add_params)

        # Assign values to params
        result = {}
        if "pin" in params:
            result["pin"] = self.vehicle.pin

        if "target_value" in params:
            result["target_value"] = self.coordinator.default_climate_temp

        if "target_temp" in params:
            result["target_temp"] = self.coordinator.default_climate_temp

        if "expiration_time" in params:
            if is_turn_on:
                result["expiration_time"] = (
                    datetime.now(UTC)
                    + timedelta(hours=self.coordinator.default_service_duration)
                ).strftime("%Y-%m-%d %H:%M:00")
            else:
                result["expiration_time"] = datetime.now(UTC).strftime(
                    "%Y-%m-%d %H:%M:00"
                )

        return result
