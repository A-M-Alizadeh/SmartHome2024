from Models.SensorTypes import SensorTypes
from Utils.Utils import IdGenerator
import json

class Sensor:
    def __init__(self, type: SensorTypes):
        self.sensor_id = IdGenerator()
        self.type = type.name
        self.status = "on"

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=None)

    def __str__(self) -> str:
        return f"\033[95mSensor: {self.sensor_id} - {self.type} - {self.status}\033[0m"