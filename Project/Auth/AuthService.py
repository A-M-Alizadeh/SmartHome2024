import cherrypy
import json
import jwt
import requests
from Utils.Utils import fetchMicroservicesConf, colorPrinter
from tools import check_jwt
from Auth.config import SECRET_KEY
from Catalog.CatalogManager import register_user, login_user, logout_user

# http://localhost:8080?apiinfo=user this fills the param like this: {'apiinfo': 'user'}
# http://localhost:8080/apiinfo/user this fills the uri like this: ('apiinfo', 'user')

class Server(object):
    exposed = True

    def GET(self, *uri, **params):
        return "Auth GET  Server !"
    
    # @cherrypy.tools.check_jwt()
    def POST(self, *uri, **params):
        if "login" in uri:
            colorPrinter("Login Called", "red")
            return login_user(json.loads(cherrypy.request.body.read()))
        if "register" in uri:
            return register_user(json.loads(cherrypy.request.body.read()))
        #this one needs check_jwt
        if "logout" in uri:
            bearer = cherrypy.request.headers.get("Authorization").split(" ")[1]
            return logout_user(bearer)
        return "Auth POST  Server !"

    def PUT(self, *uri, **params):
        return "Auth PUT  Server !"

    def DELETE(self, *uri, **params):
        return "Auth DELET  Server !"


# -------------------------------------------- Main --------------------------------------------
if __name__ == '__main__':
    serverConf = fetchMicroservicesConf("auth")
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Access-Control-Allow-Origin', '*')],
            'tools.sessions.on': True,
        }
    }
    cherrypy.config.update(conf)
    cherrypy.tree.mount(Server(), '/', conf)
    cherrypy.config.update({'web.socket_ip': serverConf["url"], 'server.socket_port': serverConf["port"]})

    cherrypy.engine.start()
    cherrypy.engine.block()