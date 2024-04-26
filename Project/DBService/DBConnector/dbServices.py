import cherrypy
import json
from Utils.Utils import fetchMicroservicesConf, colorPrinter
import cherrypy_cors
from DBConnector.influx.influxUtil import InfluxDBManager

dbConnector = InfluxDBManager()
class AnalyticsServer(object):
    exposed = True

    def GET(self, *uri, **params):
        if "deleter" in uri:
            colorPrinter("Deleting data", "red")
            dbConnector.myDelete()
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
                .field("humidity", data['v']['humidity'])
                .field("temperature", data['v']['temperature'])
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
    serverConf = fetchMicroservicesConf("analytics")
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
    cherrypy.config.update({'web.socket_ip': serverConf["url"], 'server.socket_port': serverConf["port"]})
    cherrypy.engine.start()
    cherrypy.engine.block()