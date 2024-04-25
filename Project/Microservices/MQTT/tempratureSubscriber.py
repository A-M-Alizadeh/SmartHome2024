
import requests
import time
from Microservices.MQTT.MQTT import MyMQTT
from Utils.Utils import colorPrinter
from Utils.influx.influxUtil import InfluxDBManager
import json

def findMicro(micros, microName):
    for micro in micros:
        if micro['name'] == microName:
            return micro
    return None

#--------------------------------------------REST API------------------------------------------------
def getConnectionInfo():
    response = requests.get('http://localhost:8080/public/fullservices')
    data = response.json()
    return data

def sendDataToDB(data, microInfo):
    response = requests.post(f'{microInfo["url"]}{microInfo["port"]}/db/measurement', json=data)
    return response.json()

#--------------------------------------------MQTT------------------------------------------------
class SensorsSubscriber:
    def __init__(self,clientID, broker, port, topic, mqttInfo, restInfo):
        self.mqttClient = MyMQTT(clientID, broker, port, self)
        self.topic = topic
        self.dbConnector = InfluxDBManager()
        self.mqttInfo = mqttInfo
        self.restInfo = restInfo

    def notify(self, topic, payload): #use senML
        try:
            if "temperature" in topic:
                colorPrinter( f'sensor ${topic}:  ${payload}recieved','red')
                json_string = payload.decode('utf-8')
                data = json.loads(json_string)
                sendDataToDB(data, findMicro(self.restInfo, 'analytics'))
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

    subscriber = SensorsSubscriber(mqttInfo['clientId']+'Subscriber_temperature', mqttInfo['broker'], mqttInfo['port'], mqttInfo['common_topic']+"+", mqttInfo, restInfo)
    subscriber.start()

    colorPrinter(f'TEMPERATURE Subscriber Started', 'pink')
    colorPrinter(f'{subscriber.topic}', 'pink')
    colorPrinter(f'{subscriber.mqttClient.clientID}', 'pink')
    while True:
        time.sleep(1)