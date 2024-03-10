import uuid
import json
import os
import requests
from Utils.Utils import CatalogReader, colorPrinter, addUsertoCatalog, addUserHouseToCatalog, addUserSensorToCatalog,\
    updateUser, updateHouse, updateSensor, deleteHouse, deleteSensor, deleteUser
from Models.Sensor import Sensor
from Models.House import House
from Models.User import User
from Models.SensorTypes import SensorTypes

#-------------------------------------------- Update Json File --------------------------------------------

#-------------------------------------------- Full --------------------------------------------\
def full_register(input):
    user = input["user"]
    house = input["house"]
    sensors = input["sensors"]
    newUser = User(user["username"], user["password"], user["email"], user["first_name"], user["last_name"], user["phone"])
    newHouse = House(house["address"], house["title"])
    for sensor in sensors:
        newSensor = Sensor(SensorTypes[sensor["type"]])
        newHouse.add_sensor(newSensor)
    newUser.add_house(newHouse)
    addUsertoCatalog(newUser.toJson())
    return newUser.toJson()

#-------------------------------------------- User CRUD --------------------------------------------
def get_all_users():
    return CatalogReader()["users"]

def get_user_by_id(user_id):
    return next((user for user in CatalogReader()["users"] if user["user_id"] == user_id), None)

def new_user(user:User):
    newUser = User(user["username"], user["password"], user["email"], user["first_name"], user["last_name"], user["phone"])
    addUsertoCatalog(newUser.toJson())
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
        for house in user_houses:
            if house.get("house_id") == house_id:
                return house
    return None

def new_house(user_id, house:House):
    users = CatalogReader()["users"]
    for user in users:
        if user["user_id"] == user_id:
            newHouse = House(house["address"], house["title"])
            addUserHouseToCatalog(user_id, newHouse.toJson())
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
            for sensor in sensors:
                if sensor.get("sensor_id") == sensor_id:
                    return sensor
    return None

def new_sensor(user_id, house_id, sensor):
    users = CatalogReader()["users"]
    for user in users:
        if user["user_id"] == user_id:
            for house in user["houses"]:
                if house["house_id"] == house_id:
                    newSensor = Sensor(SensorTypes[sensor["type"]])
                    addUserSensorToCatalog(user_id, house_id, newSensor.toJson())
                    return newSensor.toJson()
    return None

#-------------------------------------------- Update --------------------------------------------
def update_user(user_id, user):
    return updateUser(user_id, user)

def update_house(user_id, house_id, house):
    return updateHouse(user_id, house_id, house)

def update_sensor(user_id, house_id, sensor_id, sensor):
    return updateSensor(user_id, house_id, sensor_id, sensor)

#-------------------------------------------- Delete --------------------------------------------
def delete_user(user_id):
    return deleteUser(user_id)

def delete_house(user_id, house_id):
    return deleteHouse(user_id, house_id)

def delete_sensor(user_id, house_id, sensor_id):
    return deleteSensor(user_id, house_id, sensor_id)



#-------------------------------------------- Main --------------------------------------------

if __name__ == '__main__':
    colorPrinter(str(get_all_users()), "green")
    colorPrinter(str(get_user_by_id(1)), "yellow")
    colorPrinter(str(get_user_houses(1)), "blue")
    colorPrinter(str(get_house_by_id(1, 1)), "purple")
    colorPrinter(str(get_all_sensors(1, 1)), "cyan")
    colorPrinter(str(get_sensor_by_id(1, 1, 1)), "red")