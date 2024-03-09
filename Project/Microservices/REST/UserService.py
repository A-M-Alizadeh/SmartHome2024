import cherrypy
import os
import json
from pathlib import Path
from Utils.Utils import ApiConfReader, fetchMicroservicesConf, getAllUsers, getUserById, colorPrinter
import requests

# http://localhost:8080?apiinfo=user this fills the param like this: {'apiinfo': 'user'}
# http://localhost:8080/apiinfo/user this fills the uri like this: ('apiinfo', 'user')

class Server(object):
    exposed = True

    def GET(self, *uri, **params):
        if "userId" in params:
            return json.dumps(getUserById(int(params.get("userId"))))
        else:
            return json.dumps(getAllUsers())

    def POST(self, *uri, **params):
        return "User POST  Server !"

    def PUT(self, *uri, **params):
        return "User PUT  Server !"

    def DELETE(self, *uri, **params):
        return "User DELET  Server !"


# -------------------------------------------- Main --------------------------------------------
if __name__ == '__main__':
    serverConf = fetchMicroservicesConf("user")
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