import cherrypy
import json
from Utils.Utils import colorPrinter
import cherrypy_cors
from DBConnector.influx.influxUtil import InfluxDBManager
import requests
import os
from DBConnector.DeviceSubscribers import SensorsSubscriber
import time

class AnalyticsServer(object):
    exposed = True

    def GET(self, *uri, **params):
        return "Analytics GET  Server !"
    
    def POST(self, *uri, **params):
        if "analytics" in uri:
            print(params)
            data = json.loads(cherrypy.request.body.read())
            return json.dumps(dbConnector.readSensorData(data["sensorId"], data["period"]))
        if "fullAnalytics" in uri:
            print(params)
            data = json.loads(cherrypy.request.body.read())
            return json.dumps(dbConnector.readAllSensorsData(data["sensorIds"], data["period"]))
        if "commandAnalytics" in uri:
            print(params)
            data = json.loads(cherrypy.request.body.read())
            return json.dumps(dbConnector.readCommands(data["sensorId"], data["period"])) #this one does not work properly
        # if "customPeriod" in uri:
        #write a function to get data from influxdb with custom period with start and end time

    def PUT(self, *uri, **params):
        return "Analytics PUT  Server !"

    def DELETE(self, *uri, **params):
        return "Analytics DELET  Server !"
    
    #fixing cors preflight by OPTIONS method
    def OPTIONS(self, *args, **kwargs):
        cherrypy_cors.preflight(allowed_methods=['GET', 'POST'])

class DBConnectorServer(object):
    exposed = True

    def GET(self, *uri, **params):
        return "DBConnector GET  Server !"
    
    def POST(self, *uri, **params):
        if "measurement" in uri:
            reqBody = cherrypy.request.body.read()
            data = json.loads(reqBody)
            print('=====>',data)
            point = (
                dbConnector.Point("Measurement")
                .tag("sensorId", data['bn'])
                .tag("unit", data['u'])
                .tag("type", data['n'])
                .field("value", data['v'])
            )
            dbConnector.writeData(point)
            return json.dumps({"message": "work on progress"})
        if "command" in uri:
            colorPrinter("Command data", "pink")
            reqBody = cherrypy.request.body.read()
            data = json.loads(reqBody)
            print('=====>',data)
            point = (
                dbConnector.Point("Command")
                .tag("sensorId", data['bn'])
                .tag("unit", data['u'])
                .tag("type", data['n'])
                .tag("status", data['v']['status'])
                .tag("actionType", data['v']['actionType'])
                .field("humidity", float(data['v']['humidity']))
                .field("temperature", float(data['v']['temperature']))
            )
            dbConnector.writeData(point)
            return json.dumps({"message": "work on progress"})

    def PUT(self, *uri, **params):
        return "DBConnector PUT  Server !"

    def DELETE(self, *uri, **params):
        return "DBConnector DELET  Server !"
    
    #fixing cors preflight by OPTIONS method
    def OPTIONS(self, *args, **kwargs):
        cherrypy_cors.preflight(allowed_methods=['GET', 'POST'])

# -------------------------------------------- Main --------------------------------------------
if __name__ == '__main__':

    config = {}
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(f'{path}/DBConnector/config.json') as json_file:
        config = json.load(json_file)

    response = requests.get(f'{config["baseUrl"]}{config["basePort"]}/public/fullservices')
    connectionInfo = response.json()
    mqttInfo = connectionInfo['mqtt']
    restInfo = connectionInfo['micros']

    dbConnector = InfluxDBManager()
    serverConf = requests.get(f"{config['baseUrl']}{config['basePort']}/public?apiinfo=analytics")
    serverConf = serverConf.json()
    headers = [('Access-Control-Allow-Origin', '*'), ('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')]
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': headers,
            'tools.sessions.on': True,
        }
    }
    cherrypy.config.update(conf)
    cherrypy.tree.mount(AnalyticsServer(), '/analytic', conf)
    cherrypy.tree.mount(DBConnectorServer(), '/db', conf)
    cherrypy_cors.install()
    cherrypy.config.update({'server.socket_host': '0.0.0.0','web.socket_ip': serverConf["url"], 'server.socket_port': serverConf["port"]})
    cherrypy.engine.start()
    # cherrypy.engine.block() #this line blocks the main thread and the code below will not be executed :)


# -------------------------------------------- MQTT Subscriber --------------------------------------------
    customTopic = mqttInfo['common_topic']+"#"
    subscriber = SensorsSubscriber(mqttInfo['clientId']+'dbSubscriber', mqttInfo['broker'], mqttInfo['subPort'], customTopic, mqttInfo, restInfo, dbConnector)
    subscriber.start()

    colorPrinter(f'HUMIDITY Subscriber Started', 'pink')
    colorPrinter(f'{subscriber.topic}', 'pink')
    colorPrinter(f'{subscriber.mqttClient.clientID}', 'pink')
    while True:
        time.sleep(1)