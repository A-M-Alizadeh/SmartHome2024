import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

class AirConditionerController:
    def __init__(self, sensor_data, manual_commands=None):
        self.sensor_data = sensor_data
        self.manual_commands = manual_commands if manual_commands else []

    def make_decision(self):
        # Extract temperature and humidity data from sensor data
        temperature = self.sensor_data['temperature']
        humidity = self.sensor_data['humidity']

        # Analyze historical sensor data for patterns and trends
        temperature_trend = self.analyze_temperature_trend(temperature)
        humidity_trend = self.analyze_humidity_trend(humidity)

        # Consider external factors such as time of day, month, etc.
        # (Add your own logic here based on contextual information)

        # Make a decision based on analysis
        decision = self.decide(temperature_trend, humidity_trend)

        return decision

    def analyze_temperature_trend(self, temperature):
        # Use moving average to analyze temperature trend
        window_size = 5
        temperature_ma = temperature.rolling(window=window_size).mean()

        # Fit ARIMA model to temperature data
        model = ARIMA(temperature, order=(1, 1, 1))
        model_fit = model.fit()

        # Predict future temperature values
        forecast = model_fit.forecast(steps=5)[0]

        return {
            'moving_average': temperature_ma,
            'arima_forecast': forecast
        }

    def analyze_humidity_trend(self, humidity):
        # Use moving average to analyze humidity trend
        window_size = 5
        humidity_ma = humidity.rolling(window=window_size).mean()

        # Fit ARIMA model to humidity data
        model = ARIMA(humidity, order=(1, 1, 1))
        model_fit = model.fit()

        # Predict future humidity values
        forecast = model_fit.forecast(steps=5)[0]

        return {
            'moving_average': humidity_ma,
            'arima_forecast': forecast
        }

    def decide(self, temperature_trend, humidity_trend):
        # Add decision logic based on trend analysis, contextual factors, and manual commands
        # (Add your own decision-making logic here)

        return 'Turn on'  # Placeholder decision

# Example usage
sensor_data = pd.DataFrame({
    'timestamp': pd.date_range(start='2024-04-01', periods=7),
    'temperature': [20, 21, 22, 23, 24, 25, 26],
    'humidity': [40, 45, 50, 55, 60, 65, 70]
})

manual_commands = pd.DataFrame({
    'timestamp': pd.date_range(start='2024-04-01', periods=3),
    'command': ['Turn on', 'Turn off', 'Adjust temperature']
})

controller = AirConditionerController(sensor_data, manual_commands)
decision = controller.make_decision()
print(decision)




ideal_values = {
    'January': {'humidity': 80, 'temperature': 5},
    'February': {'humidity': 75, 'temperature': 6},
    'March': {'humidity': 70, 'temperature': 10},
    'April': {'humidity': 65, 'temperature': 15},
    'May': {'humidity': 70, 'temperature': 20},
    'June': {'humidity': 75, 'temperature': 24},
    'July': {'humidity': 75, 'temperature': 27},
    'August': {'humidity': 75, 'temperature': 27},
    'September': {'humidity': 75, 'temperature': 23},
    'October': {'humidity': 80, 'temperature': 17},
    'November': {'humidity': 80, 'temperature': 11},
    'December': {'humidity': 80, 'temperature': 6}
}




#every hour you get the data related to last 2 weeks and update the model
#every 5 minutes you get the data and make a decision