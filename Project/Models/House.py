from Sensor import TemperatureSensor, HumiditySensor
class House:
    def __init__(self, house_id, address, title):
        self.house_id = house_id
        self.address = address
        self.title = title
        self.sensors = []

    def add_sensor(self, sensor):
        self.sensors.append(sensor)

    def __str__(self) -> str:
        return f"House: {self.house_id} - {self.address} - {self.title} - {self.sensors}"