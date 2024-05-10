import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import json
import os
import requests
from datetime import datetime, timedelta
import schedule
import time
# statsmodels 0.14.1


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
        self.suggestedValues = None
        self.connectionError = False
        

    def findMicro(self, microName):
        for micro in self.microsInfo['micros']:
            if micro['name'] == microName:
                return micro
        return None
        
    def getServicesInfo(self):
        try:
            result = requests.get(f'{config["baseUrl"]}{config["basePort"]}/public/fullservices')
            self.microsInfo = result.json()
            self.connectionError = False
        except Exception as e:
            self.microsInfo = None
            self.connectionError = True
            print("Error: ", str(e))


    def getHistoricalData(self):
        try:
            reqBody = {
                "sensorIds": [self.sensorsInfo["temperature"], self.sensorsInfo["humidity"]],
                "period": config["modelHistoricalDataDuration"]
            }
            result = requests.post(f'{self.findMicro("analytics")["url"]}{self.findMicro("analytics")["port"]}/analytic/fullAnalytics', json=reqBody)
            self.historicalData = result.json()
            self.connectionError = False
        except Exception as e:
            self.historicalData = None
            self.connectionError = True
            print("Error: ", e)


    def getUserCommands(self):
        try:
            print("Getting User Decisions............../ AIR2", self.sensorsInfo["airConditioner"], config["modelHistoricalDataDuration"])
            reqBody = {
                "sensorId": self.sensorsInfo["airConditioner"],
                "period": config["modelHistoricalDataDuration"]
            }
            result = requests.post(f'{self.findMicro("analytics")["url"]}{self.findMicro("analytics")["port"]}/analytic/commandAnalytics', json=reqBody)
            #filter the manual commands
            filtered_data = [entry for entry in result.json()["records"] if entry['actionType'] == 'manual']
            print("User Decisions: ", filtered_data)
            self.userDecisions = filtered_data
            self.connectionError = False
        except Exception as e:
            self.userDecisions = None
            self.connectionError = True
            print("Error: ", str(e))

        if self.connectionError:
            return


        try:
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
            print("Time Window Start:", time_window_start_str)
            print("Time Window End:", time_window_end_str)
            print("Filtered Data:", filtered_data)
            # Find items within the time window
            matching_items = [item for item in filtered_data if time_window_start_str <= item['time'] <= time_window_end_str]
            print("Matching Items:")
            print(matching_items)
        except Exception as e:
            print("Error:", str(e))
            matching_items = []



        # print("Matching Items:", matching_items[0:5])
        if len(matching_items) > 0:
            try:
                print("Matching Items Found............../ AIR2")
                # Extract temperature and humidity values from the records
                temperatures = [record['temperature'] for record in matching_items]
                humidities = [record['humidity'] for record in matching_items]

                weights = [0.1, 0.3, 0.5]
                num_parts = len(temperatures) // len(weights)

                # Split temps into equal parts
                temp_parts = np.array_split(temperatures, num_parts)
                humid_parts = np.array_split(humidities, num_parts)
                # Calculate weighted average for each part
                weighted_avg_temps = []
                for i, part in enumerate(temp_parts):
                    weighted_avg_temps.append(sum(part) / len(part))

                weighted_avg_humids = []
                for i, part in enumerate(humid_parts):
                    weighted_avg_humids.append(sum(part) / len(part))
                
                # Calculate overall weighted average
                overall_weighted_avg_temp = sum(weight * avg_temp for weight, avg_temp in zip(weights, weighted_avg_temps))
                overall_weighted_avg_humid = sum(weight * avg_humid for weight, avg_humid in zip(weights, weighted_avg_humids))

                self.userDecisionsAvg = {
                    "temperature": overall_weighted_avg_temp,
                    "humidity": overall_weighted_avg_humid
                }
            except Exception as e:
                print("Error:", str(e))
                self.userDecisionsAvg = None
            
        else:
            print("No matching items found.")
            self.userDecisionsAvg = None

    def predictWithNextValues(self):
        current_date = datetime.now()
        current_month = current_date.month
        try:
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

            # Remove time information from one DataFrame and create a separate DataFrame for timestamps
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

            finalTempDf = pd.DataFrame(temperature_df, index=timeee_df)
            print("Temperature DF ====> : ", finalTempDf)

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
        except Exception as e:
            print("Error:", str(e))
            self.predction = {
                "temperature": self.comfortEnvironment[str(current_month)]['temperature'],
                "humidity": self.comfortEnvironment[str(current_month)]['humidity']
            }
        

    def makeDecision(self):
        current_date = datetime.now()
        current_month = current_date.month
        current_hour = current_date.hour

        is_off_hours = False
        for key, value in config["offHours"].items():
            start_hour = value["start"]
            end_hour = value["end"]
            
            # Handling the case where the period spans across two days
            if start_hour > end_hour:
                if current_hour >= start_hour or current_hour < end_hour:
                    is_off_hours = True
                    break
            # Handling the case where the period is within the same day
            else:
                if start_hour <= current_hour <= end_hour:
                    is_off_hours = True
                    break
        
        if is_off_hours:
            print("Off hours detected. Turning off the air conditioner.")
            suggested_value = {'temperature': 0, 'humidity': 0, 'status': 'OFF'}
            self.suggestedValues = suggested_value
            return suggested_value


        if self.userDecisionsAvg is not None:
            comfortZone = self.comfortEnvironment[str(current_month)]
            print("User Decisions Avg: ", self.userDecisionsAvg)
            print("Prediction: ", self.predction)
            print("Comfort Zone: ", comfortZone)
            # Define weights (adjust as needed based on importance)
            weight_user_decision = 0.5
            weight_prediction = 0.2
            weight_comfort_zone = 0.3
            # Calculate weighted averages for temperature and humidity
            weighted_temp = (weight_user_decision * self.userDecisionsAvg['temperature'] +
                            weight_prediction * self.predction['temperature'] +
                            weight_comfort_zone * comfortZone['temperature'])

            weighted_humidity = (weight_user_decision * self.userDecisionsAvg['humidity'] +
                                weight_prediction * self.predction['humidity'] +
                                weight_comfort_zone * comfortZone['humidity'])
            # Suggested value close to the user's decision
            suggested_value = {'temperature': round(weighted_temp, 2), 'humidity': round(weighted_humidity, 2), 'status': 'ON'}
            print("Suggested Value:", suggested_value)
            self.suggestedValues = suggested_value
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
            suggested_value = {'temperature': round(weighted_temp, 2), 'humidity': round(weighted_humidity, 2), 'status': 'ON'}
            print("Suggested Value:", suggested_value)
            self.suggestedValues = suggested_value
            return suggested_value

    def sendCommand(self):
        try:
            url = f'{self.findMicro("command")["url"]}{self.findMicro("command")["port"]}/command/airConiditioner'
            # url = f'{config["commandUrl"]}{config["commandPort"]}/command/airConiditioner'
            payload = {
                "userId": config["userId"],
                "houseId": config["houseId"],
                "sensorId": config["airConditionerId"],
                "temperature": self.suggestedValues['temperature'],
                "humidity": self.suggestedValues['humidity'],
                "status": self.suggestedValues['status'],
                "actionType": "auto"
            }

            print('Sending request to:', url, payload)
            # Send the request
            response = requests.post(url, json=payload)
            print('Response:', response)
            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                print('Request sent successfully!')
            else:
                print('Failed to send request. Status code:', response.status_code)
        except Exception as e:
            print('An error occurred with the Auto Command: ', str(e))

    def run(self):
        # self.getServicesInfo()
        self.getHistoricalData()
        self.getUserCommands()
        print("--------------Step1")
        if self.connectionError:
            return
        print("-------------------Step2")
        self.predictWithNextValues()
        self.makeDecision()
        self.sendCommand()


if __name__ == "__main__":
    config = {}
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(f'{path}/CommandCenter/config.json') as json_file:
        config = json.load(json_file)
        
    decisionMaker = DecisionMaker()
    decisionMaker.getServicesInfo()
    schedule.every(config["modelCommandInterval"]).seconds.do(decisionMaker.run)
    # Run the scheduler loop indefinitely
    while True:
        schedule.run_pending()
        time.sleep(config["modelCommandInterval"])  # Sleep for 1 second to avoid high CPU usage
    


# check if air status is OFF then do nothing until status is switches to ON
#check it inside the air subscriber
#make some meaningfull intervals of sending sensor info and making decision and other intervals