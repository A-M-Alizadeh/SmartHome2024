import time
import requests
from Microservices.MQTT.MQTT import MyMQTT
from Utils.Utils import colorPrinter,colorPrinterdouble, printCircle
import json
import os

def findMicro(micros, microName):
    for micro in micros:
        if micro['name'] == microName:
            return micro
    return None
#--------------------------------------------REST API------------------------------------------------
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def getConnectionInfo():
    response = requests.get('http://localhost:8080/public/fullservices')
    data = response.json()
    return data

def sendStatusUpdateRequest(status, microInfo):
    data = {}
    with open(f'{path}/config.json') as json_file:
        data = json.load(json_file)

    response = requests.put(f"{microInfo['url']}{microInfo['port']}/device/updatesensor?userId={data['userId']}&houseId={data['houseId']}&sensorId={data['airConditionerId']}",
                             json={
                                "sensor_id":data['airConditionerId'],
                                "status":status,
                                "type":"AIR_CONDITIONER"
                            })
    return response.json()

def sendDataToDB(data, microInfo):
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
            if "air_condition" in topic:
                # colorPrinter( f'sensor ${topic}:  ${payload}recieved','green')
                
                try:
                    json_string = payload.decode('utf-8')
                    data = json.loads(json_string)
                    sendDataToDB(data, findMicro(self.restInfo, 'analytics'))
                    sendStatusUpdateRequest(data['v']['status'], findMicro(self.restInfo, 'catalog'))
                    if data['v']['status'] == 'ON':
                        colorPrinter('-----------------AIR-CONDITIONER STATUS-----------------', 'white')
                        printCircle('green')
                        colorPrinterdouble( f'AIR-CONDITIONER STATUS:    ', data['v']['status'],'yellow', 'green')
                        colorPrinterdouble( f'IDEAL HUMIDITY:            ', str(data['v']['humidity'])+' %','yellow', 'green')
                        colorPrinterdouble( f'IDEAL TEMPERATURE:         ', str(data['v']['temperature'])+' c\n\n\n\n\n\n\n\n\n','yellow', 'green')    
                    else:
                        colorPrinter('-----------------AIR-CONDITIONER STATUS-----------------', 'white')
                        printCircle('red')
                        colorPrinterdouble( f'AIR-CONDITIONER STATUS:    ', data['v']['status'],'white', 'red')
                        colorPrinterdouble( f'IDEAL HUMIDITY:            ', str(0)+' %','white', 'white')
                        colorPrinterdouble( f'IDEAL TEMPERATURE:         ', str(0)+' c\n\n\n\n\n\n\n\n\n','white', 'white')   
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
    mqttInfo = connectionInfo['mqtt']
    restInfo = connectionInfo['micros']

    subscriber = SensorsSubscriber(mqttInfo['clientId']+'Subscriber_command', mqttInfo['broker'], mqttInfo['port'], mqttInfo['common_topic']+"+", mqttInfo, restInfo)
    subscriber.start()

    colorPrinter(f'AIRCONDITION Subscriber Started', 'pink')
    colorPrinter(f'{subscriber.topic}', 'pink')
    colorPrinter(f'{subscriber.mqttClient.clientID}', 'pink')

    while True:
        time.sleep(1)