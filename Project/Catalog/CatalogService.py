import cherrypy
import os
import json
from pathlib import Path
from Utils.Utils import ApiConfReader

# http://localhost:8080?apiinfo=user this fills the param like this: {'apiinfo': 'user'}
# http://localhost:8080/apiinfo/user this fills the uri like this: ('apiinfo', 'user')

class Server(object):
    exposed = True

    def GET(self, *uri, **params):
        print(params.get("apiinfo"))
        if params:
            if params.get("apiinfo"):
              return json.dumps(ApiConfReader(params.get("apiinfo")))
        print(uri)
        print(params)
        return "Catalog GET  Server !"

    def POST(self, *uri, **params):
        return "Catalog POST  Server !"

    def PUT(self, *uri, **params):
        return "Catalog PUT  Server !"

    def DELETE(self, *uri, **params):
        return "Catalog DELET  Server !"


# -------------------------------------------- Main --------------------------------------------
if __name__ == '__main__':
    apiConf = ApiConfReader("catalog")
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
    cherrypy.config.update({'web.socket_ip': apiConf["url"], 'server.socket_port': apiConf["port"]})

    cherrypy.engine.start()
    cherrypy.engine.block()