import cherrypy
import json
from Utils.Utils import colorPrinter
import cherrypy_cors
from CommandCenter.commandPublisher import CommandPublisher
import requests
import os

class Server(object):
    exposed = True

    def GET(self, *uri, **params):
        return "Auth GET  Server !"
    
    def POST(self, *uri, **params):
        if "airConiditioner" in uri:
            colorPrinter("POST /airConiditioner", "yellow")
            data = json.loads(cherrypy.request.body.read())
            topiccc = 'smart_house/'+data['userId']+'/'+data['houseId']+'/'+data["sensorId"]+'/'+'air_conditioner'
            colorPrinter(str(data), "orange")
            if data["status"] == "OFF":
                print("Turning off the air conditioner") # this needs more work if we want to implement it
                commandPublisher.publish(0, 0, data["actionType"], data["status"], topiccc, data["sensorId"])
                return json.dumps({"status": "success", "message": "Air conditioner turned off successfully !", "data": data})
            else:
                commandPublisher.publish(data["temperature"], data["humidity"], data["actionType"], data["status"], topiccc, data["sensorId"])
                return json.dumps({"status": "success", "message": "Command received successfully 2 !", "data": data})
        return json.dumps({"status": "error", "message": "Invalid request !"})

    def PUT(self, *uri, **params):
        return "Auth PUT  Server !"

    def DELETE(self, *uri, **params):
        return "Auth DELET  Server !"
    
    #fixing cors preflight by OPTIONS method
    def OPTIONS(self, *args, **kwargs):
        cherrypy_cors.preflight(allowed_methods=['GET', 'POST'])

# -------------------------------------------- Main --------------------------------------------
if __name__ == '__main__':
    config = {}
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(f'{path}/CommandCenter/config.json') as json_file:
        config = json.load(json_file)

    response = requests.get(f'{config["baseUrl"]}{config["basePort"]}/public/mqtt')
    data = response.json()

    connectionInfo = data
    commandPublisher = CommandPublisher(connectionInfo['clientId']+"CC_Publisher_command", connectionInfo['broker'], connectionInfo['pubPort'], connectionInfo['common_topic'])#ids are unique for publisher and subscriber
    commandPublisher.readConfig()
    commandPublisher.getConnectionInfo()
    commandPublisher.getSensorData()
    commandPublisher.start()
    
    serverConf = requests.get(f"{config['baseUrl']}{config['basePort']}/public?apiinfo=command")
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
    cherrypy.tree.mount(Server(), '/command', conf)
    cherrypy_cors.install()
    cherrypy.config.update({'server.socket_host': '0.0.0.0','web.socket_ip': serverConf["url"], 'server.socket_port': serverConf["port"], 'cors.expose.on': True})
    cherrypy.engine.start()
    cherrypy.engine.block()