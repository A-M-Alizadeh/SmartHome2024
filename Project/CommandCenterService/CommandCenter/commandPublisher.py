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
with open(f'{path}/CommandCenter/config.json') as json_file:
        config = json.load(json_file)
#--------------------------------------------REST API------------------------------------------------
def getConnectionInfo():
    response = requests.get(f'{config["baseUrl"]}{config["basePort"]}/public/mqtt')
    data = response.json()
    return data

def getSensorData():
    data = {}
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(f'{path}/CommandCenter/config.json') as json_file:
        data = json.load(json_file)
    url = f"{config['baseUrl']}{config['basePort']}/device/findsensor?userId={data['userId']}&houseId={data['houseId']}&sensorId={data['airConditionerId']}"
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {data["token"]}'}
    response = requests.get(url, headers={'Content-Type': 'application/json', 'Authorization': f'{data["token"]}'})
    data = response.json()
    colorPrinter(f'Sensor Data Received: {data}', 'yellow')
    return data

#--------------------------------------------MQTT------------------------------------------------
class CommandPublisher:
    def __init__(self, clientID, broker, port, topic):
        self.mqttClient = MyMQTT(clientID, broker, port, self)
        self.statusToBool = {"ON": True, "OFF": False}
        self.topic = topic
        self.__message = {"bn":clientID, "t": None,  "u":"act", "n":"command", "v": random.choice([True, False])}#self.statusToBool["OFF"]}
        self.sensorData = getSensorData()
        self.connectionDetails = getConnectionInfo()
        self.sensGen = CombinedSim()

    def start(self):
        self.mqttClient.start()

    def stop(self):
        self.mqttClient.stop()

    def publish(self, temp=None, humid=None, actionType=None, status=None):
        message = self.__message
        message = self.sensGen.getAirConditionCommand(self.sensorData['sensor_id'], 'air_condition', temp, humid, actionType, status)
        self.topic = self.connectionDetails['common_topic']+config['userId']+'/'+config['houseId']+'/'+self.sensorData['sensor_id']+'/'+self.sensorData['type'].lower()
        self.mqttClient.myPublish(self.topic, message)
        colorPrinter(f'Published {message} to {self.topic}', 'cyan')

#--------------------------------------------MAIN------------------------------------------------
# connectionInfo = getConnectionInfo()
# commandPublisher = CommandPublisher(connectionInfo['clientId']+"Publisher_command", connectionInfo['broker'], connectionInfo['pubPort'], connectionInfo['common_topic'])#ids are unique for publisher and subscriber

# if __name__ == "__main__":
#     connectionInfo = getConnectionInfo()
#     # sensorData = getSensorData()

#     publisher = CommandPublisher(connectionInfo['clientId']+"Publisher_command", connectionInfo['broker'], connectionInfo['port'], connectionInfo['common_topic'])#ids are unique for publisher and subscriber
#     publisher.start()

#     colorPrinter(f'Publisher Started', 'cyan')
#     colorPrinter(f'{publisher.topic}', 'cyan')
#     colorPrinter(f'{publisher.mqttClient.clientID}', 'cyan')
#     while True:
#         publisher.publish()
#         time.sleep(10)