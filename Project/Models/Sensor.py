from SensorTypes import SensorTypes

class Sensor:
    def __init__(self, sensor_id, type: SensorTypes):
        self.sensor_id = sensor_id
        self.type = type
        self.measurements = []

    def add_measurement(self, measurement):
        self.measurements.append(measurement)

    def __str__(self) -> str:
        return f"Sensor: {self.sensor_id} - {self.type} - {self.measurements}"


class TemperatureSensor(Sensor):
    def __init__(self):
        super().__init__()

class HumiditySensor(Sensor):
    def __init__(self):
        super().__init__()