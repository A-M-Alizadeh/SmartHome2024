import time
import requests
from MQTT import MyMQTT
from Utils.Utils import colorPrinter
import json
import os
import requests

#--------------------------------------------MQTT------------------------------------------------
class SensorsSubscriber:
    def __init__(self,clientID, broker, port, topic, mqttInfo, restInfo,config):
        self.mqttClient = MyMQTT(clientID, broker, port, self)
        self.topic = topic
        self.mqttInfo = mqttInfo
        self.restInfo = restInfo
        self.config = config

    def sendDataToDB(self, data, microInfo):
        colorPrinter(f'Sending data to {str(microInfo)}', 'yellow')
        response = requests.post(f'{microInfo["url"]}{microInfo["port"]}/db/measurement', json=data)
        return response.json()
    
    def findMicro(self,microName):
        for micro in self.restInfo:
            if micro['name'] == microName:
                return micro
        return None

    def notify(self, topic, payload): #use senML
        try:
            if "humidity" in topic:
                colorPrinter( f'sensor ${topic}:  ${payload}recieved','blue')
                json_string = payload.decode('utf-8')
                data = json.loads(json_string)
                if data['v'] > self.config['humidThreshold']:
                    response = requests.post(
                    url='https://api.telegram.org/bot{0}/{1}'.format(self.config['botToken'], 'sendMessage'),
                    data={'chat_id': self.config['chat_id'], 'text': f'Notice: Humidity is above {data["v"]} !!!'}
                    ).json()
                # send an alarm if humidity is above 80%
                # alaram can be a publisher through MQTT or a notification through email or SMS or to mobile app
                # self.sendDataToDB(data,self.findMicro('analytics'))
                # colorPrinter(f'Writing data to InfluxDB: {str(data)}', 'yellow')

            if "temperature" in topic:
                colorPrinter( f'sensor ${topic}:  ${payload}recieved','red')
                json_string = payload.decode('utf-8')
                data = json.loads(json_string)
                print(data)
                if data['v'] > self.config['tempThreshold']:
                    response = requests.post(
                    url='https://api.telegram.org/bot{0}/{1}'.format(self.config['botToken'], 'sendMessage'),
                    data={'chat_id': self.config['chat_id'], 'text': f'Notice: Temperature is above {data["v"]} !!!'}
                    ).json()
                #send an alarm if temperature is above 40
                # self.sendDataToDB(data, self.findMicro('analytics'))
                # colorPrinter(f'Writing data to InfluxDB: {str(data)}', 'yellow')
                
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

    #listen to everything
    customTopic = mqttInfo['common_topic']+ config['userId']+"/#"
    
    #listen only to specific user
    # customTopic = mqttInfo['common_topic']+config['userId']+"/#"
    
    #listen only to specific house
    # customTopic = mqttInfo['common_topic']+config['userId']+"/"+config['houseId']+"/#"

    #listen only to specific sensor
    # customTopic = mqttInfo['common_topic']+config['userId']+"/"+config['houseId']+"/"+config['sensorId']+"/#"

    #listen only to specific sensor with specific type
    # customTopic = mqttInfo['common_topic']+config['userId']+"/"+config['houseId']+"/"+config['sensorId']+"/"+temperature

    #listen to all sensors with the same type
    # customTopic = mqttInfo['common_topic']+"+/+/+/"+"/temperature"

    #listen to all sensors with the same type and user
    # customTopic = mqttInfo['common_topic']+config['userId']+"/+/+/"+"/temperature"

    
    subscriber = SensorsSubscriber(mqttInfo['clientId']+'notifSubscriber', mqttInfo['broker'], mqttInfo['subPort'], customTopic, mqttInfo, restInfo,config)

    subscriber.start()

    colorPrinter(f'Notif Subscriber Started', 'pink')
    colorPrinter(f'{subscriber.topic}', 'pink')
    colorPrinter(f'{subscriber.mqttClient.clientID}', 'pink')
    while True:
        time.sleep(1)