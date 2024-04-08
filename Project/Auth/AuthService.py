import cherrypy
import json
from Utils.Utils import fetchMicroservicesConf, colorPrinter
from Catalog.CatalogManager import register_user, login_user, logout_user, full_register
# http://localhost:8080?apiinfo=user this fills the param like this: {'apiinfo': 'user'}
# http://localhost:8080/apiinfo/user this fills the uri like this: ('apiinfo', 'user')
import cherrypy_cors

class Server(object):
    exposed = True

    def GET(self, *uri, **params):
        return "Auth GET  Server !"
    
    def POST(self, *uri, **params):
        if "login" in uri:
            return login_user(json.loads(cherrypy.request.body.read()))
        if "register" in uri:
            return register_user(json.loads(cherrypy.request.body.read()))
        if "fullRegister" in uri:
            return full_register(json.loads(cherrypy.request.body.read()))
        #TODO this one needs check_jwt
        if "logout" in uri:
            bearer = cherrypy.request.headers.get("Authorization").split(" ")[1]
            return logout_user(bearer)
        return "Auth POST  Server !"

    def PUT(self, *uri, **params):
        return "Auth PUT  Server !"

    def DELETE(self, *uri, **params):
        return "Auth DELET  Server !"
    
    #fixing cors preflight by OPTIONS method
    def OPTIONS(self, *args, **kwargs):
        cherrypy_cors.preflight(allowed_methods=['GET', 'POST'])

# -------------------------------------------- Main --------------------------------------------
origins = ['http://127.0.0.1', 'http://127.0.0.1:5173','localhost:5173','loaclhost']
if __name__ == '__main__':
    serverConf = fetchMicroservicesConf("auth")
    headers = [('Access-Control-Allow-Origin', '*'), ('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')]
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': headers,
            'tools.sessions.on': True,
            # 'cors.expose.on': True,
            # 'cors.preflight.origins': True,
            # 'cors.expose.origins': origins,
            # 'cors.preflight.origins': origins,
        }
    }
    cherrypy.config.update(conf)
    cherrypy.tree.mount(Server(), '/', conf)
    cherrypy_cors.install()
    cherrypy.config.update({'web.socket_ip': serverConf["url"], 'server.socket_port': serverConf["port"], 'cors.expose.on': True})
    cherrypy.engine.start()
    cherrypy.engine.block()