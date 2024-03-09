import uuid
import json
import os
import requests

def parentDir():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def IdGenerator():
    return str(uuid.uuid4())

def CatalogReader():
    path = parentDir()
    print(path)
    with open(f'{path}/Catalog/Catalog.json') as json_file:
        data = json.load(json_file)
        return data

def ApiConfReader(name):
    data = CatalogReader()
    info = data["microservices"]["micros"]
    for i in info:
        if i["name"] == name:
            return i
    return None

def fetchMicroservicesConf(name):
    result = requests.get("http://localhost:8080?apiinfo=" + name)
    return {
        "url": result.json()["url"],
        "port": result.json()["port"]
        }

# if __name__ == '__main__':
#     print(ApiConfReader("catalog"))
#     print(fetchMicroservicesConf("user"))
#     print(IdGenerator())