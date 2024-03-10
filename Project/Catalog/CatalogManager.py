import uuid
import json
import os
import requests
from Utils.Utils import CatalogReader, colorPrinter, IdGenerator
from Models.Sensor import Sensor
from Models.House import House
from Models.User import User
from Models.SensorTypes import SensorTypes


#-------------------------------------------- Full --------------------------------------------\
def full_register(input):
    # colorPrinter(str(input), "green")
    user = input["user"]
    house = input["house"]
    sensors = input["sensors"]
    newUser = User(user["username"], user["password"], user["email"], user["first_name"], user["last_name"], user["phone"])
    newHouse = House(house["address"], house["title"])
    for sensor in sensors:
        newSensor = Sensor(SensorTypes[sensor["type"]])
        newHouse.add_sensor(newSensor)
    newUser.add_house(newHouse)
    return newUser.toJson()

#-------------------------------------------- User CRUD --------------------------------------------
def get_all_users():
    return CatalogReader()["users"]

def get_user_by_id(user_id):
    return next((user for user in CatalogReader()["users"] if user["user_id"] == user_id), None)

def new_user(user:User):
    newUser = User(user["username"], user["password"], user["email"], user["first_name"], user["last_name"], user["phone"])
    # CatalogReader()["users"].append(newUser)
    return newUser.toJson()

#-------------------------------------------- House CRUD --------------------------------------------
def get_user_houses(user_id):
    return next((user["houses"] for user in CatalogReader()["users"] if user["user_id"] == user_id), [])

def get_house_by_id(user_id, house_id):
    users = CatalogReader()["users"]
    for user in users:
        if user.get("user_id") == user_id:
            user_houses = user.get("houses", [])
            return next((house for house in user_houses if house.get("house_id") == house_id), None)
    return None

def find_house_only_by_id(house_id):
    users = CatalogReader()["users"]
    for user in users:
        user_houses = user.get("houses", [])
        return next((house for house in user_houses if house.get("house_id") == house_id), None)
    return None

def new_house(user_id, house:House):
    users = CatalogReader()["users"]
    for user in users:
        if user["user_id"] == user_id:
            newHouse = House(house["address"], house["title"])
            # user["houses"].append(newHouse)
            return newHouse.toJson()
    return None

#-------------------------------------------- Sensor CRUD --------------------------------------------
def get_all_sensors(user_id, house_id):
    users = CatalogReader()["users"]
    for user in users:
        if user["user_id"] == user_id:
            return next((house["sensors"] for house in user["houses"] if house["house_id"] == house_id), None)
    return None

def get_sensor_by_id(user_id, house_id, sensor_id):
    users = CatalogReader()["users"]
    for user in users:
        if user["user_id"] == user_id:
            return next((sensor for house in user["houses"] if house["house_id"] == house_id
                         for sensor in house["sensors"] if sensor["sensor_id"] == sensor_id), None)
    return None

def find_sensor_only_by_id(sensor_id):
    users = CatalogReader()["users"]
    for user in users:
        user_houses = user.get("houses", [])
        for house in user_houses:
            sensors = house.get("sensors", [])
            return next((sensor for sensor in sensors if sensor.get("sensor_id") == sensor_id), None)
    return None

def new_sensor(user_id, house_id, sensor):
    users = CatalogReader()["users"]
    for user in users:
        if user["user_id"] == user_id:
            for house in user["houses"]:
                if house["house_id"] == house_id:
                    newSensor = Sensor(SensorTypes[sensor["type"]])
                    # house["sensors"].append(newSensor)
                    return newSensor.toJson()
    return None

#-------------------------------------------- Sample Data --------------------------------------------

sampleSensor = {
    "sensor_id": 1,
    "name": "Temperature",
    "type": "Temperature",
    "value": 23.0,
    "unit": "Celsius"
}
sampleHouse= {
    "house_id": 1,
    "name": "House 1",
    "address": "Budapest",
    "sensors": [sampleSensor]
}
sampleUser = {
    "user_id": 1,
    "name": "User 1",
    "email": "aaa@a.com",
    "houses": [sampleHouse]
}

#-------------------------------------------- Main --------------------------------------------

if __name__ == '__main__':
    colorPrinter(str(get_all_users()), "green")
    colorPrinter(str(get_user_by_id(1)), "yellow")
    colorPrinter(str(get_user_houses(1)), "blue")
    colorPrinter(str(get_house_by_id(1, 1)), "purple")
    colorPrinter(str(get_all_sensors(1, 1)), "cyan")
    colorPrinter(str(get_sensor_by_id(1, 1, 1)), "red")