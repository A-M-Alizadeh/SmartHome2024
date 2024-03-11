import requests
import time
import random
import requests
from Microservices.MQTT.MQTT import MyMQTT
from Utils.Utils import colorPrinter
from Simulators import HumiditySim, TemperatureSim

#--------------------------------------------REST API------------------------------------------------
def getConnectionInfo():
    response = requests.get('http://localhost:8080/public/mqtt')
    data = response.json()
    return data

def getSensorsList():
    response = requests.get('http://localhost:8080/public/fullsensors')
    data = response.json()
    return data

#--------------------------------------------MQTT------------------------------------------------
class SensorPublisher:
    def __init__(self, clientID, broker, port, topic):
        self.mqttClient = MyMQTT(clientID, broker, port, self)
        self.statusToBool = {"ON": True, "OFF": False}
        self.topic = topic
        # self.topic = 'IoT/grp4/temperature'
        self.__message = {"bn":clientID, "t": None,  "u":"Cel", "n":"temp", "v":None}

    def start(self):
        self.mqttClient.start()

    def stop(self):
        self.mqttClient.stop()

    def randomValueGenerator(self):
        return round(random.uniform(20.0,48.0), 1)

    def publish(self):
        message = self.__message
        message["v"] = self.randomValueGenerator()
        message["t"] = str(time.time())
        self.mqttClient.myPublish(self.topic, message)
        colorPrinter(f'Published {message} to {self.topic}', 'yellow')

#--------------------------------------------MAIN------------------------------------------------
if __name__ == "__main__":
    connectionInfo = getConnectionInfo()
    sensors = getSensorsList()

    publisher = SensorPublisher(connectionInfo['clientId']+'Publisher', connectionInfo['broker'], connectionInfo['port'], connectionInfo['common_topic'])
    #staticversion to debug
    # publisher = SensorPublisher("sensor2", "broker.hivemq.com", 1883, "IoT/grp4/temperature")
    publisher.start()
    # time.sleep(2)
    colorPrinter(f'Publisher Started', 'pink')
    colorPrinter(f'{publisher.topic}', 'pink')
    colorPrinter(f'{publisher.mqttClient.clientID}', 'pink')
    while True:
            publisher.publish()
            time.sleep(5)