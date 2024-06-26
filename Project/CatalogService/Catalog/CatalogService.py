import cherrypy
import os
import json
from pathlib import Path
from Utils.Utils import ApiConfReader,colorPrinter, getFullServices
# from Catalog.CatalogManager import get_user_by_id, get_all_users, get_house_by_id, get_user_houses, get_all_sensors,\
#     get_sensor_by_id, find_sensor_only_by_id, find_house_only_by_id, new_sensor, new_house, new_user, full_register,\
#     update_user, update_sensor, update_house, delete_user, delete_sensor, delete_house, full_Sensors, getMqttInfo,\
#     login_user, register_user, logout_user, updateSensorStatus
from Catalog.DataManager import DataManager
from Auth.tools import check_jwt
import cherrypy_cors


class PublicServer(object):
    exposed =True
    def GET(self, *uri, **params):
        if "apiinfo" in params:
            return json.dumps(ApiConfReader(params.get("apiinfo")))
        if "fullsensors" in uri:
            return json.dumps(dataManager.full_Sensors())
        if "mqtt" in uri:
            return json.dumps(dataManager.getMqttInfo())
        if "fullservices" in uri:
            return json.dumps(getFullServices())
    def OPTIONS(self, *args, **kwargs):
        cherrypy_cors.preflight(allowed_methods=['GET', 'POST', 'PUT', 'DELETE'])
        
class UserServer(object):
    exposed = True
    @cherrypy.tools.check_jwt()
    def GET(self, *uri, **params):
        if "allusers" in uri:
            return json.dumps(dataManager.get_all_users())
        if "finduser" in uri:
            return json.dumps(dataManager.get_user_by_id(params.get("userId")))
        return "URL not found !"

    def POST(self, *uri, **params):
        # if "fullregister" in uri:
        #     return full_register(json.loads(cherrypy.request.body.read()))
        if "newuser" in uri:
            return dataManager.new_user(json.loads(cherrypy.request.body.read()))
    def PUT(self, *uri, **params):
        if "updateuser" in uri:
            updatedUser = dataManager.update_user(params.get("userId").replace('"', ''), json.loads(cherrypy.request.body.read()))
            return json.dumps(updatedUser)
        return "URL not found !"
    def DELETE(self, *uri, **params):
        if "deleteuser" in uri:
            return dataManager.delete_user(params.get("userId"))
        return "URL not found !"
    def OPTIONS(self, *args, **kwargs):
        cherrypy_cors.preflight(allowed_methods=['GET', 'POST', 'PUT', 'DELETE'])

class HouseServer(object):
    exposed = True
    @cherrypy.tools.check_jwt()
    def GET(self, *uri, **params):
        if "allhouses" in uri:
            return json.dumps(dataManager.get_user_houses(params.get("userId").replace('"', '')))
        if "findhouse" in uri:
            return json.dumps(dataManager.get_house_by_id(params.get("userId").replace('"', ''), params.get("houseId").replace('"', '')))
        if "findhouseonly" in uri:
            return json.dumps(dataManager.find_house_only_by_id(params.get("houseId").replace('"', '')))
        return "URL not found !"

    def POST(self, *uri, **params):
        if "newhouse" in uri:
            return dataManager.new_house(params.get("userId").replace('"', ''), json.loads(cherrypy.request.body.read()))
        return "URL not found !"
    def PUT(self, *uri, **params):
        if "updatehouse" in uri:
            return dataManager.update_house(params.get("userId").replace('"', ''), params.get("houseId").replace('"', ''), json.loads(cherrypy.request.body.read()))
        return "URL not found !"
    def DELETE(self, *uri, **params):
        if "deletehouse" in uri:
            return dataManager.delete_house(params.get("userId").replace('"', ''), params.get("houseId").replace('"', ''))
        return "URL not found !"
    
    def OPTIONS(self, *args, **kwargs):
        cherrypy_cors.preflight(allowed_methods=['GET', 'POST', 'PUT', 'DELETE'])
        

class DeviceServer(object):
    exposed = True
    @cherrypy.tools.check_jwt()
    def GET(self, *uri, **params):
        if "allsensors" in uri:
            return json.dumps(dataManager.get_all_sensors(params.get("userId").replace('"', ''), params.get("houseId").replace('"', '')))
        if "findsensor" in uri:
            return json.dumps(dataManager.get_sensor_by_id(params.get("userId").replace('"', ''), params.get("houseId").replace('"', ''), params.get("sensorId").replace('"', '')))
        if "findsensoronly" in uri:
              return json.dumps(dataManager.find_sensor_only_by_id(params.get("sensorId").replace('"', '')))
        return "URL not found !"
    def POST(self, *uri, **params):
        if "newsensor" in uri:
            return dataManager.new_sensor(params.get("userId").replace('"', ''), params.get("houseId").replace('"', ''), json.loads(cherrypy.request.body.read()))
        return "URL not found !"
        
    def PUT(self, *uri, **params):
        if "updatesensor" in uri:
            colorPrinter("updating sensor", "red")
            return dataManager.update_sensor(params.get("userId").replace('"', ''), params.get("houseId").replace('"', ''), params.get("sensorId").replace('"', ''), json.loads(cherrypy.request.body.read()))
        # if "updateStatus":
        #     return updateSensorStatus(params.get("userId").replace('"', ''), params.get("houseId").replace('"', ''), params.get("sensorId").replace('"', ''), json.loads(cherrypy.request.body.read()))
        return "URL not found !"
    
    def DELETE(self, *uri, **params):
        if "deletesensor" in uri:
            colorPrinter("deleting sensor", "red")
            return dataManager.delete_sensor(params.get("userId").replace('"', ''), params.get("houseId").replace('"', ''), params.get("sensorId").replace('"', ''))

    def OPTIONS(self, *args, **kwargs):
        cherrypy_cors.preflight(allowed_methods=['GET', 'POST', 'PUT', 'DELETE'])

# -------------------------------------------- Auth --------------------------------------------
class AuthServer(object):
    exposed = True

    def GET(self, *uri, **params):
        return "Auth GET  Server !"
    
    def POST(self, *uri, **params):
        if "login" in uri:
            return dataManager.login_user(json.loads(cherrypy.request.body.read()))
        if "register" in uri:
            return dataManager.register_user(json.loads(cherrypy.request.body.read()))
        if "fullRegister" in uri:
            result = dataManager.full_register(json.loads(cherrypy.request.body.read()))
            if result == False:
                raise cherrypy.HTTPError(400, "User already exists")
            return json.dumps(result)
        #TODO this one needs check_jwt
        if "logout" in uri:
            bearer = cherrypy.request.headers.get("Authorization").split(" ")[1]
            return dataManager.logout_user(bearer)
        return "Auth POST  Server !"

    def PUT(self, *uri, **params):
        return "Auth PUT  Server !"

    def DELETE(self, *uri, **params):
        return "Auth DELET  Server !"
    
    #fixing cors preflight by OPTIONS method
    def OPTIONS(self, *args, **kwargs):
        cherrypy_cors.preflight(allowed_methods=['GET', 'POST', 'PUT', 'DELETE'])


@staticmethod
def error_page_default(status, message, traceback, version):
    cherrypy.response.headers['Content-Type'] = 'application/json'
    # Customize error response based on status code
    if status == 400:
        return json.dumps({"error": {"code": status, "message": message}})
    else:
        return json.dumps({"error": {"code": status, "message": message}})

# Configure CherryPy to use the custom error handler globally
cherrypy.config.update({'error_page.default': error_page_default})

# -------------------------------------------- Main --------------------------------------------

if __name__ == '__main__':
    dataManager = DataManager()
    apiConf = ApiConfReader("catalog")
    headers = [('Access-Control-Allow-Origin', '*'), ('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')]
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': headers,
            'tools.sessions.on': True,
            # 'cors.expose.on': True,
        }
    }
    cherrypy.config.update(conf)
    cherrypy.tree.mount(UserServer(), '/user', conf)
    cherrypy.tree.mount(HouseServer(), '/house', conf)
    cherrypy.tree.mount(DeviceServer(), '/device', conf)
    cherrypy.tree.mount(PublicServer(), '/public', conf)
    cherrypy.tree.mount(AuthServer(), '/auth', conf)
    cherrypy.config.update({'server.socket_host': '0.0.0.0','web.socket_ip': apiConf["url"], 'server.socket_port': apiConf["port"]})
    cherrypy.engine.start()
    cherrypy.engine.block()