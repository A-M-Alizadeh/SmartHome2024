import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import json
import os
import requests
from datetime import datetime, timedelta


config = {}
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(f'{path}/CommandCenter/config.json') as json_file:
        config = json.load(json_file)

class DecisionMaker:
    def __init__(self) -> None:
        self.microsInfo = None
        self.historicalData = None
        self.userDecisions = None
        self.comfortEnvironment = config['ideal_values'] #ashrae standard: 
        self.currentAirConditionerStatus = None
        self.model = None
        self.sensorsInfo = {
            "temperature": config['tempSensorId'],
            "humidity": config['humidSensorId'],
            "airConditioner": config['airConditionerId']
            }
        self.predction = None
        self.userDecisionsAvg = None
        
    def findMicro(self, microName):
        for micro in self.microsInfo['micros']:
            if micro['name'] == microName:
                return micro
        return None
        
    def getServicesInfo(self):
        
        result = requests.get(f'{config["baseUrl"]}{config["basePort"]}/public/fullservices')
        self.microsInfo = result.json()

    def getHistoricalData(self):
        reqBody = {
            "sensorIds": [self.sensorsInfo["temperature"], self.sensorsInfo["humidity"]],
            "period": config["modelHistoricalDataDuration"]
        }
        result = requests.post(f'{self.findMicro("analytics")["url"]}{self.findMicro("analytics")["port"]}/analytic/fullAnalytics', json=reqBody)
        self.historicalData = result.json()

    def getUserCommands(self):
        reqBody = {
            "sensorId": self.sensorsInfo["airConditioner"],
            "period": config["modelHistoricalDataDuration"]
        }
        result = requests.post(f'{self.findMicro("analytics")["url"]}{self.findMicro("analytics")["port"]}/analytic/commandAnalytics', json=reqBody)
        #filter the manual commands
        filtered_data = [entry for entry in result.json()["records"] if entry['actionType'] == 'manual']
        # print("User Decisions: ", filtered_data)
        self.userDecisions = filtered_data

        # Current time
        current_time = datetime.utcnow()
        # Convert current time to string format matching the data
        current_time_str = current_time.strftime('%Y-%m-%dT%H:%M:%S.%f+00:00')
        # print("Current Time:", current_time_str)
        # Convert current time to datetime object
        current_time_dt = datetime.strptime(current_time_str, '%Y-%m-%dT%H:%M:%S.%f+00:00')
        # Define time window (2 hours before and after current time)
        time_window_start = current_time_dt - timedelta(hours=1)
        time_window_end = current_time_dt + timedelta(hours=1)
        # Convert time window to string format matching the data
        time_window_start_str = time_window_start.strftime('%Y-%m-%dT%H:%M:%S.%f+00:00')
        time_window_end_str = time_window_end.strftime('%Y-%m-%dT%H:%M:%S.%f+00:00')
        # print("Time Window Start:", time_window_start_str)
        # print("Time Window End:", time_window_end_str)
        # Find items within the time window
        matching_items = [item for item in filtered_data if time_window_start_str <= item['time'] <= time_window_end_str]
        # print("Matching Items:")
        # print(matching_items)

        if len(matching_items) > 0:
            # getting the avg of the user decisions
            # Initialize variables to store the sum of temperature and humidity
            total_temp = 0
            total_humid = 0

            # Iterate through the data and sum up temperature and humidity
            for item in matching_items:
                total_temp += item['temperature']
                total_humid += item['humidity']

            # Calculate the average temperature and humidity
            avg_temp = total_temp / len(matching_items)
            avg_humid = total_humid / len(matching_items)

            # print("Average Temperature:", avg_temp)
            # print("Average Humidity:", avg_humid)

            self.userDecisionsAvg = {
                "temperature": avg_temp,
                "humidity": avg_humid
            }
        else:
            # print("No matching items found.")
            self.userDecisionsAvg = None

    def predictWithNextValues(self):
        temperature_records = [record for record in self.historicalData if record['type'] == 'temperature']
        humidity_records = [record for record in self.historicalData if record['type'] == 'humidity']
        # Extract temperature values and create DataFrame
        temperature_values = [entry['value'] for record in temperature_records for entry in record['records']]
        temperature_df = pd.DataFrame({'Temperature': temperature_values})

        # # Extract humidity values and create DataFrame
        humidity_values = [entry['value'] for record in humidity_records for entry in record['records']]
        humidity_df = pd.DataFrame({'Humidity': humidity_values})

        min_size = min(len(temperature_df), len(humidity_df))
        temperature_df = temperature_df[:min_size]
        humidity_df = humidity_df[:min_size]

        # # Remove time information from one DataFrame and create a separate DataFrame for timestamps
        time_df = pd.DataFrame({'Time': [entry['time'] for record in temperature_records for entry in record['records']]})
        time_df['Time'] = pd.to_datetime(time_df['Time'])
        time_diff = time_df['Time'].diff().fillna(pd.Timedelta(seconds=0))
        time_df.reset_index(drop=True, inplace=True)
        time_diff_mean = time_diff.mean()
        time_diff = time_diff.apply(lambda x: time_diff_mean if x == pd.Timedelta(seconds=0) else x)
        # Create a regular time series
        start_time = time_df['Time'].iloc[0]
        end_time = time_df['Time'].iloc[-1]
        regular_time_series = pd.date_range(start=start_time, end=end_time, freq=time_diff_mean)

        # Reindex DataFrame with the regular time series
        timeee_df = time_df.set_index('Time').reindex(regular_time_series).reset_index()
        # print("Temperature DataFrame: ", len(temperature_df))
        # print(temperature_df)
        # print("\nHumidity DataFrame: ", len(humidity_values))
        # print(humidity_df)
        # print("\nTime DataFrame: ", len(timeee_df))
        # print(timeee_df)
        
        # Fit ARIMA model to temperature data
         # Split the data into training and testing sets
        # train_size = int(len(temperature_df))  # 80% training data, 20% testing data
        # temp_train, temp_test = temperature_df.iloc[:train_size], temperature_df.iloc[train_size:]
        # humid_train, humid_test = humidity_df.iloc[:train_size], humidity_df.iloc[train_size:]

        # Fit ARIMA model for temperature
        # print("Temperature Train: ", temperature_df)
        model_temp = ARIMA(temperature_df, order=(1,0,1))
        model_fit_temp = model_temp.fit()
        # Make predictions for temperature
        forecast_temp = model_fit_temp.forecast(steps=1)

        # # Fit ARIMA model for humidity
        model_hum = ARIMA(humidity_df, order=(1,0,1))
        model_fit_hum = model_hum.fit()
        # # Make predictions for humidity
        forecast_hum = model_fit_hum.forecast(steps=1)

        # print("Prediction of Temperature:", forecast_temp)
        # print("Prediction of Temperature:", forecast_hum)
        self.predction = {
            "temperature": forecast_temp.iloc[0],
            "humidity": forecast_hum.iloc[0]
        }

    def makeDecision(self):
        current_date = datetime.now()
        current_month = current_date.month
        current_hour = current_date.hour

        is_off_hours = False
        for key, value in config["offHours"].items():
            start_hour = value["start"]
            end_hour = value["end"]
            if start_hour <= current_hour <= end_hour:
                is_off_hours = True
                break
        
        if is_off_hours:
            print("Off hours detected. Turning off the air conditioner.")
            suggested_value = {'temperature': 0, 'humidity': 0, 'status': 'OFF'}
            return suggested_value


        if self.userDecisionsAvg is not None:
            comfortZone = self.comfortEnvironment[str(current_month)]
            print("User Decisions Avg: ", self.userDecisionsAvg)
            print("Prediction: ", self.predction)
            print("Comfort Zone: ", comfortZone)
            # Define weights (adjust as needed based on importance)
            weight_user_decision = 0.5
            weight_prediction = 0.1
            weight_comfort_zone = 0.4
            # Calculate weighted averages for temperature and humidity
            weighted_temp = (weight_user_decision * self.userDecisionsAvg['temperature'] +
                            weight_prediction * self.predction['temperature'] +
                            weight_comfort_zone * comfortZone['temperature'])

            weighted_humidity = (weight_user_decision * self.userDecisionsAvg['humidity'] +
                                weight_prediction * self.predction['humidity'] +
                                weight_comfort_zone * comfortZone['humidity'])
            # Suggested value close to the user's decision
            suggested_value = {'temperature': weighted_temp, 'humidity': weighted_humidity, 'status': 'ON'}
            print("Suggested Value:", suggested_value)
            return suggested_value
        else:
            # use weighted average of the prediction and the comfort zone
            comfortZone = self.comfortEnvironment[str(current_month)]
            print("Prediction: ", self.predction)
            print("Comfort Zone: ", comfortZone)
            # Define weights (adjust as needed based on importance)
            weight_prediction = 0.3
            weight_comfort_zone = 0.7
            # Calculate weighted averages for temperature and humidity
            weighted_temp = (weight_prediction * self.predction['temperature'] +
                            weight_comfort_zone * comfortZone['temperature'])
            
            weighted_humidity = (weight_prediction * self.predction['humidity'] +
                                weight_comfort_zone * comfortZone['humidity'])
            # Suggested value close to the user's decision
            suggested_value = {'temperature': weighted_temp, 'humidity': weighted_humidity, 'status': 'ON'}
            print("Suggested Value:", suggested_value)
            return suggested_value


    def sendDecision(self):
        #send the decision to the air conditioner
        pass

    def sendCommand(self):
        #send command to the air conditioner
        pass

    def run(self):
        self.getServicesInfo()
        self.getHistoricalData()
        self.getUserCommands()
        self.predictWithNextValues()
        self.makeDecision()
        pass


if __name__ == "__main__":
    decisionMaker = DecisionMaker()
    decisionMaker.run()