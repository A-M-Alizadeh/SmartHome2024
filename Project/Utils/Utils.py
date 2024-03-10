import uuid
import json
import os
import requests

# /Users/graybook/Documents/Projects/Polito/IOT/SmartHome2024/Project

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

def CatalogWriter(data):  # Write the Catalog.json file
    path = parentDir()
    with open(f'{path}/Catalog/Catalog.json', 'w') as outfile:
        outfile.write(json.dumps(data, indent=4, separators=(',', ':')))

#-------------------------------------------- CRUD --------------------------------------------
#-------------------------------------------- Create --------------------------------------------

#change this to read file and write file - file manipulation is done in manager - only get and set full json
def addUsertoCatalog(user): # Add a user to the Catalog.json file
    data = CatalogReader()
    data["users"].append(json.loads(user))
    colorPrinter(str(data), "blue")
    CatalogWriter(data)

def addUserHouseToCatalog(user_id, house): # Add a house to a user in the Catalog.json file
    data = CatalogReader()
    for user in data["users"]:
        if user["user_id"] == user_id:
            user["houses"].append(json.loads(house))
            # return
    CatalogWriter(data)

def addUserSensorToCatalog(user_id, house_id, sensor): # Add a sensor to a house in the Catalog.json file
    data = CatalogReader()
    for user in data["users"]:
        if user["user_id"] == user_id:
            for house in user["houses"]:
                if house["house_id"] == house_id:
                    house["sensors"].append(json.loads(sensor))
                    # return
    CatalogWriter(data)

#-------------------------------------------- Update --------------------------------------------
def updateUser(user_id, user): # Update a user in the Catalog.json file
    data = CatalogReader()
    for i in range(len(data["users"])):
        colorPrinter(str(i), "red")
        colorPrinter(str(data["users"][i]["user_id"]), "green")
        colorPrinter(str(user_id), "yellow")
        if data["users"][i]["user_id"] == user_id:
            user["houses"] = data["users"][i]["houses"]
            data["users"][i] = user
            CatalogWriter(data)
            return
    return None

def updateHouse(user_id, house_id, house): # Update a house in the Catalog.json file
    data = CatalogReader()
    for user in data["users"]:
        if user["user_id"] == user_id:
            for i in range(len(user["houses"])):
                if user["houses"][i]["house_id"] == house_id:
                    house["sensors"] = user["houses"][i]["sensors"]
                    user["houses"][i] = house
                    CatalogWriter(data)
                    return
    return None

def updateSensor(user_id, house_id, sensor_id, sensor): # Update a sensor in the Catalog.json file
    data = CatalogReader()
    for user in data["users"]:
        if user["user_id"] == user_id:
            for house in user["houses"]:
                if house["house_id"] == house_id:
                    for i in range(len(house["sensors"])):
                        if house["sensors"][i]["sensor_id"] == sensor_id:
                            house["sensors"][i] = sensor
                            CatalogWriter(data)
                            return
    return None

#-------------------------------------------- Delete --------------------------------------------
def deleteUser(user_id): # Delete a user from the Catalog.json file
    data = CatalogReader()
    for i in range(len(data["users"])):
        if data["users"][i]["user_id"] == user_id:
            del data["users"][i]
            if len(data["users"]) == 0:
                data["users"] = []
            CatalogWriter(data)
            return
    return None

def deleteHouse(user_id, house_id): # Delete a house from a user in the Catalog.json file
    data = CatalogReader()
    for user in data["users"]:
        if user["user_id"] == user_id:
            for i in range(len(user["houses"])):
                if user["houses"][i]["house_id"] == house_id:
                    colorPrinter(str(user["houses"]), "green")
                    del user["houses"][i]
                    if len(user["houses"]) == 0:
                        user["houses"] = []
                    CatalogWriter(data)
                    return
    return None

def deleteSensor(user_id, house_id, sensor_id): # Delete a sensor from a house in the Catalog.json file
    data = CatalogReader()
    for user in data["users"]:
        if user["user_id"] == user_id:
            for house in user["houses"]:
                if house["house_id"] == house_id:
                    for i in range(len(house["sensors"])):
                        if house["sensors"][i]["sensor_id"] == sensor_id:
                            del house["sensors"][i]
                            if len(house["sensors"]) == 0:
                                house["sensors"] = []
                            CatalogWriter(data)
                            return
    return None


#-------------------------------------------- Requests --------------------------------------------

def fetchMicroservicesConf(name): # Fetch the microservice configuration from the Catalog.json file using CatalogService - this is used in the microservices
    result = requests.get("http://localhost:8080?apiinfo=" + name)
    return {
        "url": result.json()["url"],
        "port": result.json()["port"]
        }

def requestUserById(id): # Get a user by id from the UserService - only accepts Integers - in futue it will be a UUID
    result = requests.get(f"http://localhost:8080?userId={id}")
    return result.json()