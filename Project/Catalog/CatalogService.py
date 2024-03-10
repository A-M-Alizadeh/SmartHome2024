import cherrypy
import os
import json
from pathlib import Path
from Utils.Utils import ApiConfReader,colorPrinter
from Catalog.CatalogManager import get_user_by_id, get_all_users, get_house_by_id, get_user_houses, get_all_sensors,\
    get_sensor_by_id, find_sensor_only_by_id, find_house_only_by_id, new_sensor, new_house, new_user, full_register,\
    update_user, update_sensor, update_house, delete_user, delete_sensor, delete_house

# http://localhost:8080?apiinfo=user this fills the param like this: {'apiinfo': 'user'}
# http://localhost:8080/apiinfo/user this fills the uri like this: ('apiinfo', 'user')

class Server(object):
    exposed = True

# -------------------------------------------- CRUD --------------------------------------------
# -------------------------------------------- Read --------------------------------------------
    def GET(self, *uri, **params):
        if "apiinfo" in params:
              return json.dumps(ApiConfReader(params.get("apiinfo")))
        # -------------------------------------------- Full --------------------------------------------
        if "allusers" in uri:
            return json.dumps(get_all_users())
        if "allhouses" in uri:
            return json.dumps(get_user_houses(params.get("userId")))
        if "allsensors" in uri:
            return json.dumps(get_all_sensors(params.get("userId")), params.get("houseId"))
        # -------------------------------------------- Find By Id --------------------------------------------
        if "finduser" in uri:
            return json.dumps(get_user_by_id(params.get("userId")))
        if "findhouse" in uri:
            return json.dumps(get_house_by_id(params.get("userId"), params.get("houseId")))
        if "findsensor" in uri:
            return json.dumps(get_sensor_by_id(params.get("userId"), params.get("houseId")), params.get("sensorId"))
        # -------------------------------------------- Find Only By Id --------------------------------------------
        if "findhouseonly" in uri:
            return json.dumps(find_house_only_by_id(params.get("houseId")))
        if "findsensoronly" in uri:
            return json.dumps(find_sensor_only_by_id(params.get("sensorId")))
        
        return "URL not found !"

# -------------------------------------------- Create --------------------------------------------
    def POST(self, *uri, **params):
        if "fullregister" in uri:
            return full_register(json.loads(cherrypy.request.body.read()))
        if "newuser" in uri:
            return new_user(json.loads(cherrypy.request.body.read()))
        if "newhouse" in uri:
            return new_house(params.get("userId"), json.loads(cherrypy.request.body.read()))
        if "newsensor" in uri:
            return new_sensor(params.get("userId"), params.get("houseId"), json.loads(cherrypy.request.body.read()))
        return "URL not found !"

# -------------------------------------------- Update --------------------------------------------
    def PUT(self, *uri, **params):
        if "updateuser" in uri:
            return update_user(params.get("userId"), json.loads(cherrypy.request.body.read()))
        if "updatehouse" in uri:
            return update_house(params.get("userId"), params.get("houseId"), json.loads(cherrypy.request.body.read()))
        if "updatesensor" in uri:
            return update_sensor(params.get("userId"), params.get("houseId"), params.get("sensorId"), json.loads(cherrypy.request.body.read()))
        return "URL not found !"

# -------------------------------------------- Delete --------------------------------------------
    def DELETE(self, *uri, **params):
        if "deleteuser" in uri:
            return delete_user(params.get("userId"))
        if "deletehouse" in uri:
            return delete_house(params.get("userId"), params.get("houseId"))
        if "deletesensor" in uri:
            return delete_sensor(params.get("userId"), params.get("houseId"), params.get("sensorId"))
        return "URL not found !"


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