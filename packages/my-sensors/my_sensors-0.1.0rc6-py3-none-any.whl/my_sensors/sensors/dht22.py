"""
Humidity and temperature sensor.
"""

from typing import Tuple

from my_sensors.models import Measurement, Sensor


def _make_humidity_measurement(value) -> Measurement:
    return Measurement("humidity", "percent", value)


def _make_temperature_measurement(value) -> Measurement:
    return Measurement("temperature", "celsius", value)


class DHT22(Sensor):
    """
    Humidity and temperature sensor.

    More information: https://learn.adafruit.com/dht
    """

    sensor_type = "DHT22"

    def __init__(self, sensor_pin, sensor_id):
        try:
            import Adafruit_DHT
        except ModuleNotFoundError:
            raise ModuleNotFoundError(
                "Cannot import `Adafruit_DHT`. Install with `pip install Adafruit_DHT`."
            )
        super().__init__(sensor_id)
        self._sensor_pin = sensor_pin
        self._sensor = Adafruit_DHT.DHT22

    def _read(self) -> Tuple[float]:
        """
        Reads humidity and temperature from the sensor.
        """
        return Adafruit_DHT.read_retry(self._sensor, self._sensor_pin)

    def _read_humidity(self) -> Measurement:
        """
        Reads humidity from the sensor.
        """
        humidity = self._read()[0]
        return _make_humidity_measurement(humidity)

    def _read_temperature(self) -> Measurement:
        """
        Reads temperature from the sensor.
        """
        temperature = self._read()[1]
        return _make_temperature_measurement(temperature)

    def _read_all(self) -> Tuple[Measurement]:
        """
        Reads humidity and temperature from the sensor.
        """
        humidity, temperature = self._read()
        return (
            _make_humidity_measurement(humidity),
            _make_temperature_measurement(temperature),
        )
