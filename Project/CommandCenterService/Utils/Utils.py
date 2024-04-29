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

#-------------------------------------------- Requests --------------------------------------------

def fetchMicroservicesConf(name): # Fetch the microservice configuration from the Catalog.json file using CatalogService - this is used in the microservices
    cat_data = {}
    with open(parentDir() + "../CommandCenter/config.json") as f:
        cat_data = json.load(f)
    result = requests.get(f"{cat_data['baseUrl']}{cat_data['basePort']}/public?apiinfo=" + name)
    return {
        "url": result.json()["url"],
        "port": result.json()["port"]
        }

def requestUserById(id): # Get a user by id from the UserService - only accepts Integers - in futue it will be a UUID
    cat_data = {}
    with open(parentDir() + "../CommandCenter/config.json") as f:
        cat_data = json.load(f)
    result = requests.get(f"{cat_data['baseUrl']}{cat_data['basePort']}?userId={id}")
    return result.json()