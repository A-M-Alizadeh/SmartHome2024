import requests
import time
import random
import requests
from MQTT import MyMQTT
from Utils.Utils import colorPrinter
from Simulators.CombinedSim import CombinedSim
import json
import os

#--------------------------------------------MQTT------------------------------------------------
class SensorPublisher:
    def __init__(self, clientID, broker, port, topic):
        self.mqttClient = MyMQTT(clientID, broker, port, self)
        self.statusToBool = {"ON": True, "OFF": False}
        self.topic = topic
        self.__message = {"bn":clientID, "t": None,  "u":"Cel", "n":"temperature", "v":None}
        self.sensorData = None
        self.connectionDetails = None
        self.sensGen = CombinedSim()

    
    def getConnectionInfo(self):
        response = requests.get(f'{config["baseUrl"]}{config["basePort"]}/public/mqtt')
        data = response.json()
        self.connectionDetails = data
        # return data

    def getSensorData(self):
        data = {}
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # print('-------->',path)
        with open(f'{path}/Utils/config.json') as json_file:
            data = json.load(json_file)
        url = f"{config['baseUrl']}{config['basePort']}/device/findsensor?userId={data['userId']}&houseId={data['houseId']}&sensorId={data['tempSensorId']}"
        # headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {data["token"]}'}
        response = requests.get(url, headers={'Content-Type': 'application/json', 'Authorization': f'{data["token"]}'})
        data = response.json()
        colorPrinter(f'Sensor Data Received: {data}', 'yellow')
        self.sensorData = data
        # return data

    def start(self):
        self.mqttClient.start()

    def stop(self):
        self.mqttClient.stop()

    def publish(self):
        message = self.__message
        message = self.sensGen.getTemperature(self.sensorData['sensor_id'], 'temperature', 'c') 
        self.topic = self.connectionDetails['common_topic']+config['userId']+'/'+config['houseId']+'/'+self.sensorData['sensor_id']+'/'+self.sensorData['type'].lower()
        self.mqttClient.myPublish(self.topic, message)
        colorPrinter(f'Published {message} to {self.topic}', 'red')

#--------------------------------------------MAIN------------------------------------------------
if __name__ == "__main__":
    config = {}
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(f'{path}/Utils/config.json') as json_file:
        config = json.load(json_file)

    response = requests.get(f'{config["baseUrl"]}{config["basePort"]}/public/mqtt')
    connectionInfo = response.json()

    publisher = SensorPublisher(connectionInfo['clientId']+config["tempSensorId"]+"Publisher_temp2", connectionInfo['broker'], connectionInfo['pubPort'], connectionInfo['common_topic'])#ids are unique for publisher and subscriber
    publisher.getConnectionInfo()
    publisher.getSensorData()
    publisher.start()

    colorPrinter(f'TEMPERATURE Publisher Started', 'red')
    colorPrinter(f'{publisher.topic}', 'red')
    colorPrinter(f'{publisher.mqttClient.clientID}', 'red')
    while True:
        publisher.publish()
        time.sleep(10)