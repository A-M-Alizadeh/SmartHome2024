import time
import requests
from MQTT import MyMQTT
from Utils.Utils import colorPrinter,colorPrinterdouble, printCircle
import json
import os
#--------------------------------------------MQTT------------------------------------------------
class SensorsSubscriber:
    def __init__(self,clientID, broker, port, topic, mqttInfo, restInfo):
        self.mqttClient = MyMQTT(clientID, broker, port, self)
        self.topic = topic
        self.mqttInfo = mqttInfo
        self.restInfo = restInfo

    def findMicro(self, microName):
        for micro in self.restInfo:
            if micro['name'] == microName:
                return micro
        return None

    def sendStatusUpdateRequest(self, status, microInfo):
        data = {}
        with open(f'{path}/Utils/config.json') as json_file:
            data = json.load(json_file)

        response = requests.put(f"{microInfo['url']}{microInfo['port']}/device/updatesensor?userId={data['userId']}&houseId={data['houseId']}&sensorId={data['airConditionerId']}",
                                json={
                                    "sensor_id":data['airConditionerId'],
                                    "status":status,
                                    "type":"AIR_CONDITIONER"
                                })
        return response.json()
    
    def sendDataToDB(self, data, microInfo):
        response = requests.post(f'{microInfo["url"]}{microInfo["port"]}/db/command', json=data)
        return response.json()

    def notify(self, topic, payload): #use senML
        try:
            if f"{config['airConditionerId']}/air_conditioner" in topic:
                # colorPrinter( f'sensor ${topic}:  ${payload}recieved','green')
                
                try:
                    json_string = payload.decode('utf-8')
                    data = json.loads(json_string)
                    colorPrinter(f'AirConditioner data recieved ====> : {data}', 'green')
                    self.sendDataToDB(data, self.findMicro('analytics'))
                    self.sendStatusUpdateRequest(data['v']['status'], self.findMicro('catalog'))
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
    config = {}
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(f'{path}/Utils/config.json') as json_file:
        config = json.load(json_file)
    response = requests.get(f'{config["baseUrl"]}{config["basePort"]}/public/fullservices')
    connectionInfo = response.json()
    mqttInfo = connectionInfo['mqtt']
    restInfo = connectionInfo['micros']

    # customTopic = mqttInfo['common_topic']+"#" #listen to everything
    #listen only to specific user and air_condition
    # customTopic = mqttInfo['common_topic']+config['userId']+config['houseId']+'/'+config['airConditionerId']+"/air_condition"
    # customTopic = mqttInfo['common_topic']+config['userId']+'/+/+'+"/air_conditioner"
    # print(customTopic, '&&&&&&&&&&&&&&&&&&&')
    topic = mqttInfo['common_topic']+config['userId']+'/'+config['houseId']+'/'+config['airConditionerId']+'/'+'air_conditioner'


    subscriber = SensorsSubscriber(mqttInfo['clientId']+config['airConditionerId']+'Subscriber_command', mqttInfo['broker'], mqttInfo['subPort'], topic, mqttInfo, restInfo)
    subscriber.start()

    colorPrinter(f'AIRCONDITION Subscriber Started', 'pink')
    colorPrinter(f'{subscriber.topic}', 'pink')
    colorPrinter(f'{subscriber.mqttClient.clientID}', 'pink')

    while True:
        time.sleep(1)