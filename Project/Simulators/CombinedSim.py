from Simulators import HumiditySim, TemperatureSim

class CombinedSim:
    def __init__(self):
        self.humiditySim = HumiditySim.HumiditySensor(20, 3)
        self.temperatureSim = TemperatureSim.TemperatureSensor(40, 1)

    def getHumidity(self,sensor_id,type,unit):
        return self.humiditySim.generate_humidity_data(sensor_id,type,unit)

    def getTemperature(self,sensor_id,type,unit):
        return self.temperatureSim.generate_temperature_data(sensor_id,type,unit)