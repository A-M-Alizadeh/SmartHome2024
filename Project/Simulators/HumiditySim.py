import random
import json
from datetime import datetime

class HumiditySensor:
    def __init__(self, initial_value=60, variability=3):
        self.current_value = initial_value
        self.variability = variability

    def generate_humidity_data(self):
        # Introduce a bit of randomness around the current value
        noise = random.uniform(-self.variability, self.variability)
        # Update the current value with some memory of the past value
        self.current_value = 0.8 * self.current_value + 0.2 * (self.current_value + noise)
        # Ensure the humidity value is within the valid range (0% to 100%)
        self.current_value = max(0, min(100, self.current_value))

        # Create a SenML record
        senml_record = {
            "bn": "urn:dev:humidity:",
            "n": "humidity",
            "u": "%",  # Unit: Percentage
            "v": round(self.current_value, 2),
            "t": int(datetime.now().timestamp())
        }

        return json.dumps(senml_record, indent=2)

    def set_initial_value(self, new_initial_value):
        self.current_value = new_initial_value


#   # Example usage for humidity
# humidity_sensor = HumiditySensor(initial_value=60, variability=3)
# for _ in range(10):
#     senml_record = humidity_sensor.generate_humidity_data()
#     print(json.dumps(senml_record, indent=2))

# # Change the initial value dynamically
# humidity_sensor.set_initial_value(70)
# print("\nInitial value changed dynamically.")
# for _ in range(10):
#     senml_record = humidity_sensor.generate_humidity_data()
#     print(json.dumps(senml_record, indent=2))