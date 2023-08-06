"""

"""

import abc
import inspect
from typing import Dict, List, Tuple


class Measurement:
    def __init__(
        self,
        metric: str,
        unit: str,
        value: float,
        sensor_type: str = None,
        sensor_id: int = None,
    ):
        self.sensor_type = sensor_type
        self.sensor_id = sensor_id
        self._metric = metric
        self._unit = unit
        self._value = value

    @property
    def metric(self) -> str:
        return self._metric

    @property
    def unit(self) -> str:
        return self._unit

    @property
    def value(self) -> float:
        return self._value

    def __repr__(self):
        return f"{self.__class__.__name__}(sensor_type={self.sensor_type}, sensor_id={self.sensor_id}, metric={self.metric}, unit={self.unit}, value={self.value})"

    def to_dict(self) -> Dict:
        return {
            "sensor_type": self.sensor_type,
            "sensor_id": self.sensor_id,
            "metric": self.metric,
            "unit": self.unit,
            "value": self.value,
        }


class Sensor(abc.ABC):

    _measure_prefix = "read_"

    def __init__(self, sensor_id):
        self._sensor_id = sensor_id

    @property
    def sensor_id(self):
        return self._sensor_id

    @property
    @abc.abstractmethod
    def sensor_type(self) -> str:
        raise NotImplementedError

    @property
    def measures(self):
        """
        Lists all measures that this sensor supports.
        """
        return tuple(
            func_name.replace(self._measure_prefix, "")
            for func_name, func in inspect.getmembers(
                self.__class__, predicate=inspect.isfunction
            )
            if func_name.startswith(self._measure_prefix) and func_name != "read_all"
        )

    def read(self, metric: str, *args, **kwargs) -> Measurement:
        """
        Reads a measure from a sensor.
        """
        measurement = getattr(self, f"{self._measure_prefix}{metric}")(*args, **kwargs)
        measurement.sensor_type = self.sensor_type
        measurement.sensor_id = self.sensor_id
        return measurement

    def read_all(self, *args, **kwargs) -> Tuple[Measurement]:
        return tuple(self.read(measure) for measure in self.measures)


class RandomSensor(Sensor):

    sensor_type = "DHT22"

    def read_random(self) -> Measurement:
        return Measurement("random", "irritation/second", 1)


if __name__ == "__main__":
    sensor = RandomSensor(1)
    print(sensor.read("random"))
    print(sensor.measures)
    print(sensor.read_all())
