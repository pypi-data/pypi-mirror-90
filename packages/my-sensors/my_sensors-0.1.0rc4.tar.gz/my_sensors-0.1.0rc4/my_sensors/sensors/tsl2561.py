"""
TSL2561 luminosity sensor.
"""


from typing import Tuple

from my_sensors.models import Measurement, Sensor

import tsl2561


def _make_broadband_measurement(value):
    return Measurement("broadband", None, value)


def _make_infrared_measurement(value):
    return Measurement("infrared", None, value)


def _make_lux_measurement(value):
    return Measurement("lux", None, value)


class TSL2561(tsl2561.TSL2561):
    """
    TSL2561 luminosity sensor.

    More information: https://www.adafruit.com/product/439
    """

    def __init__(self, i2c, gain, integration_time, sensor_id):
        super().__init__(sensor_id)
        self._sensor = tsl2561.TSL2561(
            address=i2c, integration_time=integration_time, gain=gain
        )

    def _read_broadband(self) -> Measurement:
        broadband, _ = self._sensor._get_luminosity()
        return _make_broadband_measurement(broadband)

    def _read_infrared(self) -> Measurement:
        _, infrared = self._sensor._get_luminosity()
        return _make_infrared_measurement(infrared)

    def _read_lux(self):
        broadband, infrared = self._sensor._get_luminosity()
        lux = self._sensor._calculate_lux(broadband, infrared)
        return _make_lux_measurement(lux)

    def _read_all(self):
        broadband, infrared = self._sensor._get_luminosity()
        lux = self._sensor._calculate_lux(broadband, infrared)
        return (
            _make_broadband_measurement(broadband),
            _make_infrared_measurement(infrared),
            _make_lux_measurement(lux),
        )
