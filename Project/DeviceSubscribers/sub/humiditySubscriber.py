import time
import requests
from MQTT import MyMQTT
from Utils.Utils import colorPrinter
import json
import os


config = {}
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(f'{path}/Utils/config.json') as json_file:
        config = json.load(json_file)


def findMicro(micros, microName):
    for micro in micros:
        if micro['name'] == microName:
            return micro
    return None

#--------------------------------------------REST API------------------------------------------------
def getConnectionInfo():
    response = requests.get(f'{config["baseUrl"]}{config["basePort"]}/public/fullservices')
    data = response.json()
    return data

def sendDataToDB(data, microInfo):
    colorPrinter(f'Sending data to {str(microInfo)}', 'yellow')
    response = requests.post(f'{microInfo["url"]}{microInfo["port"]}/db/measurement', json=data)
    return response.json()
#--------------------------------------------MQTT------------------------------------------------
class SensorsSubscriber:
    def __init__(self,clientID, broker, port, topic, mqttInfo, restInfo):
        self.mqttClient = MyMQTT(clientID, broker, port, self)
        self.topic = topic
        self.mqttInfo = mqttInfo
        self.restInfo = restInfo

    def notify(self, topic, payload): #use senML
        try:
            if "humidity" in topic:
                colorPrinter( f'sensor ${topic}:  ${payload}recieved','blue')
                json_string = payload.decode('utf-8')
                data = json.loads(json_string)
                sendDataToDB(data,findMicro(self.restInfo, 'analytics'))
                colorPrinter(f'Writing data to InfluxDB: {str(data)}', 'yellow')
        except Exception as e:
            colorPrinter(f'Error saving data {e}', 'orange')

    def start(self):
        self.mqttClient.start()
        self.mqttClient.mySubscribe(self. topic)
        
    def stop(self):
        self.mqttClient.stop()


#--------------------------------------------MAIN------------------------------------------------
if __name__ == "__main__":
    connectionInfo = getConnectionInfo()
    mqttInfo = connectionInfo['mqtt']
    restInfo = connectionInfo['micros']
    
    subscriber = SensorsSubscriber(mqttInfo['clientId']+'Subscriber_humidity', mqttInfo['broker'], mqttInfo['subPort'], mqttInfo['common_topic']+"+", mqttInfo, restInfo)
    subscriber.start()

    colorPrinter(f'HUMIDITY Subscriber Started', 'pink')
    colorPrinter(f'{subscriber.topic}', 'pink')
    colorPrinter(f'{subscriber.mqttClient.clientID}', 'pink')
    while True:
        time.sleep(1)