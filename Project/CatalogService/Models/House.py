from CatalogService.Models.Sensor import Sensor
from CatalogService.Utils.Utils import IdGenerator
import json
class House:
    def __init__(self, address, title):
        self.house_id = IdGenerator()
        self.address = address
        self.title = title
        self.sensors = []

    def add_sensor(self, sensor:Sensor):
        self.sensors.append(sensor)
    
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=None)

    def __str__(self) -> str:
        return f"\033[92mHouse: {self.house_id} - {self.address} - {self.title} - {self.sensors}\033[0m"