import schedule
import time
import requests
import random
import json
import os

config = {}
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(f'{path}/CommandCenter/config.json') as json_file:
        config = json.load(json_file)

def send_request():
    # Define the URL for your API endpoint
    url = f'{config["commandUrl"]}{config["commandPort"]}/command/airConiditioner'

    payload = {
        "sensorId": config["airConditionerId"],
        "temperature": random.randint(18, 30),
        "humidity": random.randint(10, 60),
        "status": random.choice(["ON", "OFF"]),
        "actionType": "auto"
    }

    print('Sending request to:', url)
    print('Payload======> :', payload)
    # Send the request
    response = requests.post(url, json=payload)
    print('Response:', response)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        print('Request sent successfully!')
    else:
        print('Failed to send request. Status code:', response.status_code)

# # Schedule the request to be sent every 10 minutes
# schedule.every(10).seconds.do(send_request)

# # Run the scheduler loop indefinitely
# while True:
#     schedule.run_pending()
#     time.sleep(1)  # Sleep for 1 second to avoid high CPU usage

# #--------------------------------------------MAIN------------------------------------------------
if __name__ == "__main__":
    schedule.every(10).seconds.do(send_request)
    # Schedule the request to be sent every 10 minutes

    # Run the scheduler loop indefinitely
    while True:
        schedule.run_pending()
        time.sleep(1)  # Sleep for 1 second to avoid high CPU usage



#define a state var that will be used to store the state of the scheduler
# state = 0 # 0 means scheduler is off, 1 means scheduler is on
# when state is 0, the air conditioner is off and no automatic control is done but manual control can be done
# when state is 1, the air conditioner is on and automatic control is done -> in this case we do some analytics over the data and suggest an action to be taken