"""Velis device class for Ariston module."""
from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any, Optional

from .ariston_api import AristonAPI
from .const import VelisDeviceProperties
from .velis_base_device import AristonVelisBaseDevice
from .device import AristonDevice

_LOGGER = logging.getLogger(__name__)


class AristonVelisDevice(AristonDevice, AristonVelisBaseDevice, ABC):
    """Class representing a physical device, it's state and properties."""

    def __init__(
        self,
        api: AristonAPI,
        attributes: dict[str, Any],
        is_metric: bool = True,
        language_tag: str = "en-US",
    ) -> None:
        super().__init__(api, attributes)
        self.plant_settings: dict[str, Any] = dict()
        self.umsys = "si" if is_metric else "us"
        self.unit = "°C" if is_metric else "°F"
        self.language_tag = language_tag

    @property
    @abstractmethod
    def anti_legionella_on_off(self) -> str:
        """Final string to get anti-legionella-on-off"""

    @property
    @abstractmethod
    def max_setpoint_temp(self) -> str:
        """Final string to get max setpoint temperature"""

    @property
    def water_anti_leg_value(self) -> Optional[bool]:
        """Get water heater anti-legionella value"""
        return self.plant_settings.get(self.anti_legionella_on_off, None)

    @property
    def proc_req_temp_value(self) -> Optional[float]:
        """Get process requested tempereature value"""
        return self.data.get(VelisDeviceProperties.PROC_REQ_TEMP, None)

    def set_antilegionella(self, anti_leg: bool):
        """Set water heater anti-legionella"""
        self.api.set_velis_plant_setting(
            self.plant_data,
            self.gw,
            self.anti_legionella_on_off,
            1.0 if anti_leg else 0.0,
            1.0 if self.plant_settings[self.anti_legionella_on_off] else 0.0,
            self.umsys,
        )
        self.plant_settings[self.anti_legionella_on_off] = anti_leg

    async def async_set_antilegionella(self, anti_leg: bool):
        """Async set water heater anti-legionella"""
        await self.api.async_set_velis_plant_setting(
            self.plant_data,
            self.gw,
            self.anti_legionella_on_off,
            1.0 if anti_leg else 0.0,
            1.0 if self.plant_settings[self.anti_legionella_on_off] else 0.0,
            self.umsys,
        )
        self.plant_settings[self.anti_legionella_on_off] = anti_leg

    def set_max_setpoint_temp(self, max_setpoint_temp: float):
        """Set water heater maximum setpoint temperature"""
        self.api.set_velis_plant_setting(
            self.plant_data,
            self.gw,
            self.max_setpoint_temp,
            max_setpoint_temp,
            self.plant_settings[self.max_setpoint_temp],
            self.umsys,
        )
        self.plant_settings[self.max_setpoint_temp] = max_setpoint_temp

    async def async_set_max_setpoint_temp(self, max_setpoint_temp: float):
        """Async set water heater maximum setpoint temperature"""
        await self.api.async_set_velis_plant_setting(
            self.plant_data,
            self.gw,
            self.max_setpoint_temp,
            max_setpoint_temp,
            self.plant_settings[self.max_setpoint_temp],
            self.umsys,
        )
        self.plant_settings[self.max_setpoint_temp] = max_setpoint_temp

    @property
    @abstractmethod
    def water_heater_maximum_setpoint_temperature_minimum(self) -> Optional[float]:
        """Get water heater maximum setpoint temperature minimum"""
        raise NotImplementedError

    @property
    @abstractmethod
    def water_heater_maximum_setpoint_temperature_maximum(self) -> Optional[float]:
        """Get water heater maximum setpoint maximum temperature"""
        raise NotImplementedError

    @property
    def water_heater_maximum_setpoint_temperature(self) -> Optional[float]:
        """Get water heater maximum setpoint temperature value"""
        return self.plant_settings.get(self.max_setpoint_temp, None)

    @property
    def water_heater_minimum_temperature(self) -> float:
        """Get water heater minimum temperature"""
        return 40.0

    @property
    def water_heater_maximum_temperature(self) -> Optional[float]:
        """Get water heater maximum temperature"""
        return self.water_heater_maximum_setpoint_temperature

    @property
    def water_heater_temperature_step(self) -> int:
        """Get water heater temperature step"""
        return 1

    @property
    def water_heater_temperature_decimals(self) -> int:
        """Get water heater temperature decimals"""
        return 0

    @property
    def water_heater_temperature_unit(self) -> str:
        """Get water heater temperature unit"""
        return self.unit
