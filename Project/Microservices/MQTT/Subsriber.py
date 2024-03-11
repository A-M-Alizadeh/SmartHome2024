import time
import requests
import requests
from Microservices.MQTT.MQTT import MyMQTT
from Utils.Utils import colorPrinter
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
        # self.topic = 'IoT/grp4/temperature'

    def notify(self, topic, payload): #use senML
        try:
            colorPrinter( f'sensor ${topic}:  ${payload}recieved','green')
        except:
            colorPrinter('Error saving data', 'red')

    def start(self):
        self.mqttClient.start()
        self.mqttClient.mySubscribe(self. topic)
        
    def stop(self):
        self.mqttClient.stop()


#--------------------------------------------MAIN------------------------------------------------
if __name__ == "__main__":
    connectionInfo = getConnectionInfo()

    subscriber = SensorsSubscriber(connectionInfo['clientId']+'Subscriber', connectionInfo['broker'], connectionInfo['port'], connectionInfo['common_topic']+"+")#ids are unique for publisher and subscriber
    subscriber.start()

    colorPrinter(f'Subscriber Started', 'pink')
    colorPrinter(f'{subscriber.topic}', 'pink')
    colorPrinter(f'{subscriber.mqttClient.clientID}', 'pink')

    while True:
        time.sleep(1)