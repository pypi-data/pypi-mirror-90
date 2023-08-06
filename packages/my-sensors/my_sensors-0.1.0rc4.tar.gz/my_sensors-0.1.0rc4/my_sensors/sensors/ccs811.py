import adafruit_ccs811
from my_sensors.models import Measurement, Sensor


class CCS811(Sensor):
    def __init__(self, i2c, sensor_id):
        super().__init__(sensor_id)
        self._sensor = adafruit_ccs811.CCS811(i2c)

    def _read_eco2(self):
        return self._sensor.eco2

    def _read_tvoc(self):
        return self._sensor.tvoc
