import schedule
import time
import requests
import random

def send_request():
    # Define the URL for your API endpoint
    url = 'http://127.0.0.1:8083/command/airConiditioner'

    payload = {
        "sensorId": "e8073adc-38a8-44e6-a8e2-532bce5cd8bb",
        "temperature": random.randint(18, 30),
        "humidity": random.randint(10, 60),
        "status": random.choice(["ON", "OFF"]),
        "actionType": "auto"
    }

    # Send the request
    response = requests.post(url, json=payload)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        print('Request sent successfully!')
    else:
        print('Failed to send request. Status code:', response.status_code)

# Schedule the request to be sent every 10 minutes
schedule.every(10).seconds.do(send_request)

# Run the scheduler loop indefinitely
while True:
    schedule.run_pending()
    time.sleep(1)  # Sleep for 1 second to avoid high CPU usage
