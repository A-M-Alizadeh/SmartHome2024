import cherrypy
import json
from Utils.Utils import fetchMicroservicesConf, colorPrinter
from Catalog.CatalogManager import login_user
import cherrypy_cors
from Microservices.MQTT.commandPublisher import commandPublisher
commandPublisher.start()

class Server(object):
    exposed = True

    def GET(self, *uri, **params):
        return "Auth GET  Server !"
    
    def POST(self, *uri, **params):
        if "airConiditioner" in uri:
            colorPrinter("POST /airConiditioner", "yellow")
            data = json.loads(cherrypy.request.body.read())
            colorPrinter(str(data), "orange")
            if data["status"] == "OFF":
                print("Turning off the air conditioner") # this needs more work if we want to implement it
                return json.dumps({"status": "success", "message": "Turning off the air conditioner !"})
            else:
                commandPublisher.publish(data["temperature"], data["humidity"], data["actionType"], data["status"])
                return json.dumps({"status": "success", "message": "Command received successfully 2 !"})
        return "Auth POST  Server !"

    def PUT(self, *uri, **params):
        return "Auth PUT  Server !"

    def DELETE(self, *uri, **params):
        return "Auth DELET  Server !"
    
    #fixing cors preflight by OPTIONS method
    def OPTIONS(self, *args, **kwargs):
        cherrypy_cors.preflight(allowed_methods=['GET', 'POST'])

# -------------------------------------------- Main --------------------------------------------
if __name__ == '__main__':
    serverConf = fetchMicroservicesConf("command")
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
    cherrypy.tree.mount(Server(), '/', conf)
    cherrypy_cors.install()
    cherrypy.config.update({'web.socket_ip': serverConf["url"], 'server.socket_port': serverConf["port"], 'cors.expose.on': True})
    cherrypy.engine.start()
    cherrypy.engine.block()