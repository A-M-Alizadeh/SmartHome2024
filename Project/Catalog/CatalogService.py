import cherrypy
import os
import json
from pathlib import Path
from Utils.Utils import ApiConfReader,colorPrinter
from Catalog.CatalogManager import get_user_by_id, get_all_users, get_house_by_id, get_user_houses, get_all_sensors,\
    get_sensor_by_id, find_sensor_only_by_id, find_house_only_by_id, new_sensor, new_house, new_user, full_register

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
            return json.dumps(get_user_houses(int(params.get("userId"))))
        if "allsensors" in uri:
            return json.dumps(get_all_sensors(int(params.get("userId")), int(params.get("houseId"))))
        # -------------------------------------------- Find By Id --------------------------------------------
        if "finduser" in uri:
            return json.dumps(get_user_by_id(int(params.get("userId"))))
        if "findhouse" in uri:
            return json.dumps(get_house_by_id(int(params.get("userId")), int(params.get("houseId"))))
        if "findsensor" in uri:
            return json.dumps(get_sensor_by_id(int(params.get("userId")), int(params.get("houseId")), int(params.get("sensorId"))))
        # -------------------------------------------- Find Only By Id --------------------------------------------
        if "findhouseonly" in uri:
            return json.dumps(find_house_only_by_id(int(params.get("houseId"))))
        if "findsensoronly" in uri:
            return json.dumps(find_sensor_only_by_id(int(params.get("sensorId"))))
        
        return "URL not found !"

# -------------------------------------------- Create --------------------------------------------
    def POST(self, *uri, **params):
        if "fullregister" in uri:
            return full_register(json.loads(cherrypy.request.body.read()))
        if "newuser" in uri:
            return new_user(json.loads(cherrypy.request.body.read()))
        if "newhouse" in uri:
            return new_house(int(params.get("userId")), json.loads(cherrypy.request.body.read()))
        if "newsensor" in uri:
            return new_sensor(int(params.get("userId")), int(params.get("houseId")), json.loads(cherrypy.request.body.read()))
        return "URL not found !"

# -------------------------------------------- Update --------------------------------------------
    def PUT(self, *uri, **params):
        if "updateUser" in uri:
            return "update User PUT  Server !"
        if "updateHouse" in uri:
            return "update House PUT  Server !"
        if "updateSensor" in uri:
            return "update Sensor PUT  Server !"
        return "URL not found !"

# -------------------------------------------- Delete --------------------------------------------
    def DELETE(self, *uri, **params):
        if "deleteUser" in uri:
            return "delete User DELET  Server !"
        if "deleteHouse" in uri:
            return "delete House DELET  Server !"
        if "deleteSensor" in uri:
            return "delete Sensor DELET  Server !"
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