import random
import json
from datetime import datetime

class TemperatureSensor:
    def __init__(self, initial_value=25, variability=1):
        self.current_value = initial_value
        self.variability = variability

    def generate_temperature_data(self,sensor_id,type,unit):
        # Introduce a bit of randomness around the current value
        noise = random.uniform(-self.variability, self.variability)
        # Update the current value with some memory of the past value
        self.current_value = 0.9 * self.current_value + 0.1 * (self.current_value + noise)

        # Create a SenML record
        senml_record = {
            "bn": sensor_id,
            "n": type,
            "u": unit,  # Unit: Celsius
            "v": round(self.current_value, 2),
            "t": int(datetime.now().timestamp())
        }

        return senml_record

    def set_initial_value(self, new_initial_value):
        self.current_value = new_initial_value


# # Example usage for temperature
# temperature_sensor = TemperatureSensor(initial_value=25, variability=1)
# for _ in range(10):
#     senml_record = temperature_sensor.generate_temperature_data()
#     print(json.dumps(senml_record, indent=2))

# # Change the initial value dynamically
# temperature_sensor.set_initial_value(30)
# print("\nInitial value changed dynamically.")
# for _ in range(10):
#     senml_record = temperature_sensor.generate_temperature_data()
#     print(json.dumps(senml_record, indent=2))