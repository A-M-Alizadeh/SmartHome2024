import uuid
import json
import os
import requests
import math
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
        "orange": "\033[33m",
        "pink": "\033[95m",
        "lightblue": "\033[94m",
        "end": "\033[0m"
    }
    print(colors[color] + text + colors["end"])

def colorPrinterdouble(text1, text2, color1, color2): # Print colored text- only accepts string and color
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "purple": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "orange": "\033[33m",
        "pink": "\033[95m",
        "lightblue": "\033[94m",
        "end": "\033[0m"
    }
    print(colors[color1] + text1 + colors["end"] + colors[color2] + text2 + colors["end"])

def printCircle(color):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "purple": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "orange": "\033[33m",
        "pink": "\033[95m",
        "lightblue": "\033[94m",
        "end": "\033[0m"
    }
    radius = 2
    for i in range(-radius,radius+1):
        for j in range(-radius, radius +1):
            if math.sqrt(i**2 + j**2) <= radius:
                print(colors[color] + "*" + colors["end"],end = " ")
            else:
                print(" ", end = ' ')
        print()
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

def getFullServices(): # Read the microservice configuration from the Catalog.json file
    data = CatalogReader()
    info = data["microservices"]
    return info

def CatalogWriter(data):  # Write the Catalog.json file
    path = parentDir()
    with open(f'{path}/Catalog/Catalog.json', 'w') as outfile:
        outfile.write(json.dumps(data, indent=4, separators=(',', ':')))



#-------------------------------------------- Auth --------------------------------------------
def newActiveSession(user_id, token): # Add a new active session to the Catalog.json file
    isActive = checkActiveSession(user_id)
    if isActive is not None:
        return isActive
    data = CatalogReader()
    data["activeSessions"].append({"user_id": user_id, "token": token})
    CatalogWriter(data)
    return token

def deleteActiveSession(token): # Delete an active session from the Catalog.json file
    data = CatalogReader()
    for i in range(len(data["activeSessions"])):
        if data["activeSessions"][i]["token"] == token:
            del data["activeSessions"][i]
            if len(data["activeSessions"]) == 0:
                data["activeSessions"] = []
            CatalogWriter(data)
            return "Session deleted"
    return None

def checkActiveSession(user_id): # Check if a session is active in the Catalog.json file
    data = CatalogReader()
    for i in range(len(data["activeSessions"])):
        if data["activeSessions"][i]["user_id"] == user_id:
            return data["activeSessions"][i]
    return None

def isValideToken(token): # Check if a token is valid in the Catalog.json file
    data = CatalogReader()
    for i in range(len(data["activeSessions"])):
        if data["activeSessions"][i]["token"] == token:
            colorPrinter(str(data["activeSessions"][i]), "green")
            return True
    return False

#-------------------------------------------- CRUD --------------------------------------------
#-------------------------------------------- Create --------------------------------------------

#change this to read file and write file - file manipulation is done in manager - only get and set full json
def addUsertoCatalog(user): # Add a user to the Catalog.json file
    data = CatalogReader()
    data["users"].append(json.loads(user))
    colorPrinter(str(data), "blue")
    CatalogWriter(data)
    return user

def addUserHouseToCatalog(user_id, house): # Add a house to a user in the Catalog.json file
    data = CatalogReader()
    for user in data["users"]:
        if user["user_id"] == user_id:
            user["houses"].append(json.loads(house))
            CatalogWriter(data)
            return house
    return None

def addUserSensorToCatalog(user_id, house_id, sensor): # Add a sensor to a house in the Catalog.json file
    data = CatalogReader()
    for user in data["users"]:
        if user["user_id"] == user_id:
            for house in user["houses"]:
                if house["house_id"] == house_id:
                    house["sensors"].append(json.loads(sensor))
                    CatalogWriter(data)
                    return sensor
    return None

#-------------------------------------------- Update --------------------------------------------
def updateUser(user_id, user): # Update a user in the Catalog.json file
    data = CatalogReader()
    for i in range(len(data["users"])):
        if data["users"][i]["user_id"] == user_id:
            user["houses"] = data["users"][i]["houses"]
            data["users"][i] = user
            CatalogWriter(data)
            return data["users"][i]
    return json.dumps({"error": "User not found"})

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
                            return json.dumps(house["sensors"][i])
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
    result = requests.get("http://localhost:8080/public?apiinfo=" + name)
    return {
        "url": result.json()["url"],
        "port": result.json()["port"]
        }

def requestUserById(id): # Get a user by id from the UserService - only accepts Integers - in futue it will be a UUID
    result = requests.get(f"http://localhost:8080?userId={id}")
    return result.json()