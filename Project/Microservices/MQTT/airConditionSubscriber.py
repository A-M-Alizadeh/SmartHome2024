import time
import requests
from Microservices.MQTT.MQTT import MyMQTT
from Utils.Utils import colorPrinter,colorPrinterdouble, printCircle
from Utils.influx.influxUtil import InfluxDBManager
import json
import os
#--------------------------------------------REST API------------------------------------------------
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def getConnectionInfo():
    response = requests.get('http://localhost:8080/public/mqtt')
    data = response.json()
    return data

def sendStatusUpdateRequest(status):
    data = {}
    with open(f'{path}/MQTT/config.json') as json_file:
        data = json.load(json_file)

    print('--------------',data['userId'],data['houseId'],data['airConditionerId'],status)
    response = requests.put(f"http://localhost:8080/device/updatesensor?userId={data['userId']}&houseId={data['houseId']}&sensorId={data['airConditionerId']}",
                             json={
                                "sensor_id":data['airConditionerId'],
                                "status":status,
                                "type":"AIR_CONDITIONER"
                            })
    return response.json()

def sendDataToDB(data):
    response = requests.post('http://localhost:8084/db/command', json=data)
    return response.json()

#--------------------------------------------MQTT------------------------------------------------
class SensorsSubscriber:
    def __init__(self,clientID, broker, port, topic):
        self.mqttClient = MyMQTT(clientID, broker, port, self)
        self.topic = topic
        self.dbConnector = InfluxDBManager()

    def notify(self, topic, payload): #use senML
        try:
            if "air_condition" in topic:
                # colorPrinter( f'sensor ${topic}:  ${payload}recieved','green')
                
                try:
                    json_string = payload.decode('utf-8')
                    data = json.loads(json_string)
                    sendDataToDB(data)
                    sendStatusUpdateRequest(data['v']['status'])
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

    subscriber = SensorsSubscriber(connectionInfo['clientId']+'Subscriber_command', connectionInfo['broker'], connectionInfo['port'], connectionInfo['common_topic']+"+")#ids are unique for publisher and subscriber
    subscriber.start()

    colorPrinter(f'AIRCONDITION Subscriber Started', 'pink')
    colorPrinter(f'{subscriber.topic}', 'pink')
    colorPrinter(f'{subscriber.mqttClient.clientID}', 'pink')

    while True:
        time.sleep(1)