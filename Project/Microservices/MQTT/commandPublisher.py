import requests
import time
import random
import requests
from Microservices.MQTT.MQTT import MyMQTT
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
    with open(f'{path}/MQTT/config.json') as json_file:
        data = json.load(json_file)
    url = f"http://localhost:8080/device/findsensor?userId={data['userId']}&houseId={data['houseId']}&sensorId={data['airConditionerId']}"
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
        self.__message = {"bn":clientID, "t": None,  "u":"act", "n":"command", "v": self.statusToBool["OFF"]}
        self.sensorData = getSensorData()
        self.connectionDetails = getConnectionInfo()
        self.sensGen = CombinedSim()

    def start(self):
        self.mqttClient.start()

    def stop(self):
        self.mqttClient.stop()

    def publish(self):
        message = self.__message
        message = self.sensGen.getTemperature(self.sensorData['sensor_id'], 'humidity', '%' )
        self.topic = self.connectionDetails['common_topic']+self.sensorData['type'].lower()
        self.mqttClient.myPublish(self.topic, message)
        colorPrinter(f'Published {message} to {self.topic}', 'cyan')

#--------------------------------------------MAIN------------------------------------------------
if __name__ == "__main__":
    connectionInfo = getConnectionInfo()
    # sensorData = getSensorData()

    publisher = SensorPublisher(connectionInfo['clientId']+"Publisher", connectionInfo['broker'], connectionInfo['port'], connectionInfo['common_topic'])#ids are unique for publisher and subscriber
    publisher.start()

    colorPrinter(f'Publisher Started', 'cyan')
    colorPrinter(f'{publisher.topic}', 'cyan')
    colorPrinter(f'{publisher.mqttClient.clientID}', 'cyan')
    while True:
        publisher.publish()
        time.sleep(10)