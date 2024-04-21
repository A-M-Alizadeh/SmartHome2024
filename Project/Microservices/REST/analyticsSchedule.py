import schedule
import time
import requests

def send_request():
    # Define the URL for your API endpoint
    url = 'http://127.0.0.1:8083/airConiditioner'

    payload = {
        "sensorId": "123",
        "temperature": 24,
        "humidity": 80,
        "status": "ON",
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
schedule.every(1).minutes.do(send_request)

# Run the scheduler loop indefinitely
while True:
    schedule.run_pending()
    time.sleep(1)  # Sleep for 1 second to avoid high CPU usage
