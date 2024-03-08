from SensorTypes import SensorTypes
from Utils.Utils import IdGenerator

class Sensor:
    def __init__(self, type: SensorTypes):
        self.sensor_id = IdGenerator()
        self.type = type.name
        self.measurements = []

    def add_measurement(self, measurement):
        self.measurements.append(measurement)

    def __str__(self) -> str:
        return f"\033[95mSensor: {self.sensor_id} - {self.type} - {self.measurements}\033[0m"
