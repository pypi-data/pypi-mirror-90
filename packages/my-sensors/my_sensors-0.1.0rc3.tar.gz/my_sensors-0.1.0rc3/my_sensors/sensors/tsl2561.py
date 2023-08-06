import adafruit_tsl2561
from my_sensors.models import Measurement, Sensor


class TSL2561(Sensor):
    """
    TSL2561 luminosity sensor.

    More information: https://www.adafruit.com/product/439
    """

    def __init__(self, i2c, gain, integration_time, sensor_id):
        super().__init__(sensor_id)
        self._sensor = adafruit_tsl2561.TSL2561(i2c)
        self._sensor.gain = gain
        self._sensor.integration_time = integration_time

    def read_broadband(self) -> Measurement:
        return Measurement("broadband", None, self._sensor.broadband)

    def read_infrared(self) -> Measurement:
        return Measurement("infrared", None, self._sensor.infrared)

    def read_lux(self) -> Measurement:
        return Measurement("lux", None, self._sensor.lux)
