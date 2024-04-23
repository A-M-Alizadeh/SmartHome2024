import time
import requests
from Microservices.MQTT.MQTT import MyMQTT
from Utils.Utils import colorPrinter
from Utils.influx.influxUtil import InfluxDBManager
import json
#--------------------------------------------REST API------------------------------------------------
def getConnectionInfo():
    response = requests.get('http://localhost:8080/public/mqtt')
    data = response.json()
    return data

#--------------------------------------------MQTT------------------------------------------------
class SensorsSubscriber:
    def __init__(self,clientID, broker, port, topic):
        self.mqttClient = MyMQTT(clientID, broker, port, self)
        self.topic = topic
        self.dbConnector = InfluxDBManager()

    def notify(self, topic, payload): #use senML
        try:
            if "air_condition" in topic:
                colorPrinter( f'sensor ${topic}:  ${payload}recieved','green')
                # colorPrinter( str(json.loads(payload.decode('utf-8'))['v']['temperature']), 'yellow')
                try:
                    json_string = payload.decode('utf-8')
                    data = json.loads(json_string)
                    point = (
                        self.dbConnector.Point("Command")
                        .tag("sensorId", data['bn'])
                        .tag("unit", data['u'])
                        .tag("type", data['n'])
                        .tag("status", data['v']['status'])
                        .tag("actionType", data['v']['actionType'])
                        .field("humidity", data['v']['humidity'])
                        .field("temperature", data['v']['temperature'])
                    )
                    self.dbConnector.writeData(point)
                    colorPrinter(f'Writing data to InfluxDB: {str(point)}', 'yellow')
                except Exception as e:
                    colorPrinter(f'Error saving data {e}', 'orange')
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

    subscriber = SensorsSubscriber(connectionInfo['clientId']+'Subscriber_command', connectionInfo['broker'], connectionInfo['port'], connectionInfo['common_topic']+"+")#ids are unique for publisher and subscriber
    subscriber.start()

    colorPrinter(f'AIRCONDITION Subscriber Started', 'pink')
    colorPrinter(f'{subscriber.topic}', 'pink')
    colorPrinter(f'{subscriber.mqttClient.clientID}', 'pink')

    while True:
        time.sleep(1)