import uuid
import json
import os
import requests

#-------------------------------------------- Utils --------------------------------------------
def parentDir(): # Get the parent directory of the current file
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def IdGenerator(): # Generate a unique id
    return str(uuid.uuid4())

def colorPrinter(text, color): # Print colored text- only accepts string and color
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "purple": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "end": "\033[0m"
    }
    print(colors[color] + text + colors["end"])
#-------------------------------------------- Catalog --------------------------------------------
def CatalogReader(): # Read the Catalog.json file / path in each file is different so we need to use the parentDir() function in one file
    path = parentDir()
    print(path)
    with open(f'{path}/Catalog/Catalog.json') as json_file:
        data = json.load(json_file)
        return data

def ApiConfReader(name): # Read the microservice configuration from the Catalog.json file
    data = CatalogReader()
    info = data["microservices"]["micros"]
    for i in info:
        if i["name"] == name:
            return i
    return None

def fetchMicroservicesConf(name): # Fetch the microservice configuration from the Catalog.json file using CatalogService - this is used in the microservices
    result = requests.get("http://localhost:8080?apiinfo=" + name)
    return {
        "url": result.json()["url"],
        "port": result.json()["port"]
        }

#-------------------------------------------- User --------------------------------------------
def getAllUsers(): # Get all users from the Catalog.json file
    result = CatalogReader()
    return result["users"]

def getUserById(id): # Get a user by id from the Catalog.json file - only accepts Integers - in futue it will be a UUID
    result = CatalogReader()
    users = result["users"]
    for user in users:
        # colorPrinter(user["user_id"], "green")
        if user["user_id"] == id:
            return user
    return None

