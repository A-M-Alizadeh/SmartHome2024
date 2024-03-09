import uuid
import json
import os
import requests
from Utils.Utils import CatalogReader, colorPrinter


#-------------------------------------------- User CRUD --------------------------------------------
def get_all_users():
    return CatalogReader()["users"]

def get_user_by_id(user_id):
    return next((user for user in CatalogReader()["users"] if user["user_id"] == user_id), None)


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



if __name__ == '__main__':
    colorPrinter(str(get_all_users()), "green")
    colorPrinter(str(get_user_by_id(1)), "yellow")
    colorPrinter(str(get_user_houses(1)), "blue")
    colorPrinter(str(get_house_by_id(1, 1)), "purple")
    colorPrinter(str(get_all_sensors(1, 1)), "cyan")
    colorPrinter(str(get_sensor_by_id(1, 1, 1)), "red")