"""
Ultra-Low Power Digital Gas Sensor for Monitoring Indoor Air Quality.
"""

import adafruit_ccs811
from my_sensors.models import Measurement, Sensor


class CCS811(Sensor):
    """
    Ultra-Low Power Digital Gas Sensor for Monitoring Indoor Air Quality.

    More information: https://learn.adafruit.com/adafruit-ccs811-air-quality-sensor
    """

    def __init__(self, i2c, sensor_id=None):
        super().__init__(sensor_id)
        self._sensor = adafruit_ccs811.CCS811(i2c)

    def _read_eco2(self) -> Measurement:
        """
        Reads eco2 from the sensor.
        """
        return Measurement("eco2", "ppm", self._sensor.eco2)

    def _read_tvoc(self) -> Measurement:
        """
        Reads tvoc from the sensor.
        """
        return Measurement("tvoc", "ppb", self._sensor.tvoc)
