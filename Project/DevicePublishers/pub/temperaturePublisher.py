import requests
import time
import random
import requests
from MQTT import MyMQTT
from Utils.Utils import colorPrinter
from Simulators.CombinedSim import CombinedSim
import json
import os

#--------------------------------------------REST API------------------------------------------------
def getConnectionInfo():
    response = requests.get('http://localhost:8080/public/mqtt')
    data = response.json()
    return data

def getSensorData():
    data = {}
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(f'{path}/Utils/config.json') as json_file:
        data = json.load(json_file)
    url = f"http://localhost:8080/device/findsensor?userId={data['userId']}&houseId={data['houseId']}&sensorId={data['tempSensorId']}"
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {data["token"]}'}
    response = requests.get(url, headers={'Content-Type': 'application/json', 'Authorization': f'{data["token"]}'})
    data = response.json()
    colorPrinter(f'Sensor Data Received: {data}', 'yellow')
    return data

#--------------------------------------------MQTT------------------------------------------------
class SensorPublisher:
    def __init__(self, clientID, broker, port, topic):
        self.mqttClient = MyMQTT(clientID, broker, port, self)
        self.statusToBool = {"ON": True, "OFF": False}
        self.topic = topic
        self.__message = {"bn":clientID, "t": None,  "u":"Cel", "n":"temperature", "v":None}
        self.sensorData = getSensorData()
        self.sensorDetails = getConnectionInfo()
        self.sensGen = CombinedSim()

    def start(self):
        self.mqttClient.start()

    def stop(self):
        self.mqttClient.stop()

    def publish(self):
        message = self.__message
        message = self.sensGen.getTemperature(self.sensorData['sensor_id'], 'temperature', 'c') 
        self.topic = self.sensorDetails['common_topic']+self.sensorData['type'].lower()
        self.mqttClient.myPublish(self.topic, message)
        colorPrinter(f'Published {message} to {self.topic}', 'red')

#--------------------------------------------MAIN------------------------------------------------
if __name__ == "__main__":
    connectionInfo = getConnectionInfo()
    # sensors = getSensorsList()

    publisher = SensorPublisher(connectionInfo['clientId']+"Publisher_temp", connectionInfo['broker'], connectionInfo['port'], connectionInfo['common_topic'])#ids are unique for publisher and subscriber
    publisher.start()

    colorPrinter(f'TEMPERATURE Publisher Started', 'red')
    colorPrinter(f'{publisher.topic}', 'red')
    colorPrinter(f'{publisher.mqttClient.clientID}', 'red')
    while True:
        publisher.publish()
        time.sleep(10)