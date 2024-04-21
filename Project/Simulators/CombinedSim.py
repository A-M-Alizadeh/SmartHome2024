from Simulators import HumiditySim, TemperatureSim
from datetime import datetime
import random

class CombinedSim:
    def __init__(self):
        self.humiditySim = HumiditySim.HumiditySensor(40, 3)
        self.temperatureSim = TemperatureSim.TemperatureSensor(20, 1)

    def getHumidity(self,sensor_id,type,unit):
        return self.humiditySim.generate_humidity_data(sensor_id,type,unit)

    def getTemperature(self,sensor_id,type,unit):
        return self.temperatureSim.generate_temperature_data(sensor_id,type,unit)
    
    def getAirConditionCommand(self,sensor_id,type,temp,humid, actionType,status):
        return {
            "bn": sensor_id,
            "n": type,
            "u": 'act',  # Unit: Celsius
            'type': type, #manual or auto
            "v": {
                "temperature": temp,
                "humidity": humid,
                "actionType": actionType,
                "status": status
            },
            "t": int(datetime.now().timestamp())
        }