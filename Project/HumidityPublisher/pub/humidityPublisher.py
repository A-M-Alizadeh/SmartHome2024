import requests
import time
import random
import requests
from MQTT import MyMQTT
from Utils.Utils import colorPrinter
from Simulators.CombinedSim import CombinedSim
import json
import os

config = {}
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(f'{path}/Utils/config.json') as json_file:
        config = json.load(json_file)
        
#--------------------------------------------REST API------------------------------------------------
def getConnectionInfo():
    response = requests.get(f'{config["baseUrl"]}{config["basePort"]}/public/mqtt')
    data = response.json()
    return data

def getSensorData():
    data = {}
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print('-------->',path)
    with open(f'{path}/Utils/config.json') as json_file:
        data = json.load(json_file)
    url = f"{config['baseUrl']}{config['basePort']}/device/findsensor?userId={data['userId']}&houseId={data['houseId']}&sensorId={data['humidSensorId']}"
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
        self.__message = {"bn":clientID, "t": None,  "u":"Percentage", "n":"humidity", "v":None}
        self.sensorData = getSensorData()
        self.connectionDetails = getConnectionInfo()
        self.sensGen = CombinedSim()

    def start(self):
        self.mqttClient.start()

    def stop(self):
        self.mqttClient.stop()

    def publish(self):
        message = self.__message
        message = self.sensGen.getHumidity(self.sensorData['sensor_id'], 'humidity', '%') 
        self.topic = self.connectionDetails['common_topic']+config['userId']+'/'+config['houseId']+'/'+self.sensorData['sensor_id']+'/'+self.sensorData['type'].lower() #smart_house/userId/houseId/sensorId/sensorType
        self.mqttClient.myPublish(self.topic, message)
        colorPrinter(f'Published {message} to {self.topic}', 'blue')

#--------------------------------------------MAIN------------------------------------------------
if __name__ == "__main__":
    connectionInfo = getConnectionInfo()
    # sensorData = getSensorData()

    publisher = SensorPublisher(connectionInfo['clientId']+"Publisher_humid", connectionInfo['broker'], connectionInfo['pubPort'], connectionInfo['common_topic'])#ids are unique for publisher and subscriber
    publisher.start()

    colorPrinter(f'HUMIDITY Publisher Started', 'blue')
    colorPrinter(f'{publisher.topic}', 'blue')
    colorPrinter(f'{publisher.mqttClient.clientID}', 'blue')
    while True:
        publisher.publish()
        time.sleep(10)