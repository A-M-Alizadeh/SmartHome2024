import requests
import time
import random
import requests
from Microservices.MQTT.MQTT import MyMQTT
from Utils.Utils import colorPrinter
from Simulators.CombinedSim import CombinedSim

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
        self.sensors = getSensorsList()
        self.sensorDetails = getConnectionInfo()
        self.sensorsSize = len(self.sensors)
        self.currentSensor = 0
        self.sensGen = CombinedSim()

    def start(self):
        self.mqttClient.start()

    def stop(self):
        self.mqttClient.stop()

    def randomValueGenerator(self):
        return round(random.uniform(20.0,48.0), 1)
    
    # def publish(self):
    #     message = self.__message
    #     message["v"] = self.randomValueGenerator()
    #     message["t"] = str(time.time())
    #     self.topic = self.sensorDetails['common_topic']+random.choice(["TEMPERATURE", "HUMIDITY"])
    #     self.mqttClient.myPublish(self.topic, message)
    #     colorPrinter(f'Published {message} to {self.topic}', 'yellow')

    def publish(self):
        message = self.__message
        message = self.sensGen.getHumidity(self.sensors[self.currentSensor]['sensor_id'], 'temperature', 'c') \
            if self.sensors[self.currentSensor]['type'] == 'HUMIDITY' \
            else self.sensGen.getTemperature(self.sensors[self.currentSensor]['sensor_id'], 'humidity', '%' )
        self.topic = self.sensorDetails['common_topic']+self.sensors[self.currentSensor]['type'].lower()
        self.mqttClient.myPublish(self.topic, message)
        colorPrinter(f'Published {message} to {self.topic}', 'yellow')
        self.currentSensor = (self.currentSensor+1)%self.sensorsSize

    # def publish(self):
    # #     #publish for each sensor in the list of sensors with related topic, sensor id and sensor type and unit - using combinedSim which simulate both temperature and humidity
        
    #     for sensor in self.sensors:
    #         message = self.__message
    #         if sensor['type'] == 'TEMPERATURE':
    #             self.topic = self.sensorDetails['common_topic'] + "temperature"
    #             message["v"] = self.randomValueGenerator()
    #             message["t"] = str(time.time())
    #             self.mqttClient.myPublish(self.topic, message)
    #             colorPrinter(f'Published {message} to {self.topic}', 'yellow')

    #         elif sensor['type'] == 'HUMIDITY':
    #             self.topic = self.sensorDetails['common_topic'] + "humidity"
    #             message["v"] = self.randomValueGenerator()
    #             message["t"] = str(time.time())
    #             self.mqttClient.myPublish(self.topic, message)
    #             colorPrinter(f'Published {message} to {self.topic}', 'yellow')

#--------------------------------------------MAIN------------------------------------------------
if __name__ == "__main__":
    connectionInfo = getConnectionInfo()
    # sensors = getSensorsList()

    publisher = SensorPublisher(connectionInfo['clientId']+"Publisher", connectionInfo['broker'], connectionInfo['port'], connectionInfo['common_topic'])#ids are unique for publisher and subscriber
    publisher.start()

    colorPrinter(f'Publisher Started', 'pink')
    colorPrinter(f'{publisher.topic}', 'pink')
    colorPrinter(f'{publisher.mqttClient.clientID}', 'pink')
    while True:
            publisher.publish()
            time.sleep(10)