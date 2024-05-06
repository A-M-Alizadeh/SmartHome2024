from TemperatureSim import TemperatureSensor
from HumiditySim import HumiditySensor

# Example usage for temperature
temperature_sen = TemperatureSensor(initial_value=25, variability=3)
humiddity_Sens = HumiditySensor(initial_value=60, variability=3)

for _ in range(10):
    print(f'-----------------Record {_} -----------------')
    senml_record = temperature_sen.generate_temperature_data()
    print(senml_record)
    senml_record = humiddity_Sens.generate_humidity_data()
    print(senml_record)

