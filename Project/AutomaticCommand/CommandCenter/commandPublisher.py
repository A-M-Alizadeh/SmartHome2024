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
class CommandPublisher:
    def __init__(self, clientID, broker, port, topic):
        self.mqttClient = MyMQTT(clientID, broker, port, self)
        self.statusToBool = {"ON": True, "OFF": False}
        self.path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.readConfig()
        self.topic = topic
        self.__message = {"bn":clientID, "t": None,  "u":"act", "n":"command", "v": random.choice([True, False])}#self.statusToBool["OFF"]}
        # self.sensorData = self.getSensorData()
        # self.connectionDetails = self.getConnectionInfo()
        self.sensGen = CombinedSim()
        self.config = None

    
    def readConfig(self):
        with open(f'{self.path}/CommandCenter/config.json') as json_file:
            self.config = json.load(json_file)

    def getConnectionInfo(self):
        response = requests.get(f'{self.config["baseUrl"]}{self.config["basePort"]}/public/mqtt')
        data = response.json()
        self.connectionDetails = data
        return data

    def getSensorData(self):
        data = {}
        # path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(f'{self.path}/CommandCenter/config.json') as json_file:
            data = json.load(json_file)
        url = f"{self.config['baseUrl']}{self.config['basePort']}/device/findsensor?userId={data['userId']}&houseId={data['houseId']}&sensorId={data['airConditionerId']}"
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

    def publish(self, temp=None, humid=None, actionType=None, status=None, topiccc=None, sensorId=None):
        message = self.__message
        message = self.sensGen.getAirConditionCommand(sensorId, 'air_condition', temp, humid, actionType, status)
        # self.connectionDetails['common_topic']+self.config['userId']+'/'+self.config['houseId']+'/'+sensorId+'/'+self.sensorData['type'].lower()
        self.topic = topiccc if topiccc else self.topic
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