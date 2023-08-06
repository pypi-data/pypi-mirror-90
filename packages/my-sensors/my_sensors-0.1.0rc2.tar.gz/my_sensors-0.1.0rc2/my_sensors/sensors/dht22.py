from typing import Tuple

import Adafruit_DHT
from my_sensors.models import Measurement, Sensor


def _make_humidity_measurement(value):
    return Measurement("humidity", "percent", value)


def _make_temperature_measurement(value):
    return Measurement("temperature", "celsius", value)


class DHT22(Sensor):
    """
    DHT22 humidity and temperature sensor.

    More information: https://learn.adafruit.com/dht
    """

    sensor_type = "DHT22"

    def __init__(self, sensor_pin, sensor_id):
        super().__init__(sensor_id)
        self._sensor_pin = sensor_pin
        self._sensor = Adafruit_DHT.DHT22

    def _read(self) -> Tuple[float]:
        """
        Reads humidity and temperature from the sensor.
        """
        return Adafruit_DHT.read_retry(self._sensor, self._sensor_pin)

    def read_humidity(self) -> Measurement:
        """
        Reads humidity from the sensor.
        """
        humidity = self._read()[0]
        return _make_humidity_measurement(humidity)

    def read_temperature(self) -> Measurement:
        """
        Reads temperature from the sensor.
        """
        temperature = self._read[1]
        return _make_temperature_measurement(temperature)

    def read_all(self) -> Tuple[Measurement]:
        """
        Reads humidity and temperature from the sensor.
        """
        humidity, temperature = self._read()
        return (
            _make_humidity_measurement(humidity),
            _make_temperature_measurement(temperature),
        )
