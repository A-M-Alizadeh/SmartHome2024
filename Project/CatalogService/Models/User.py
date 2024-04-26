from CatalogService.Models.House import House
from CatalogService.Utils.Utils import IdGenerator
import json
class User:
    def __init__(self, username, password, email, first_name='', last_name='', phone_number=''):
        self.user_id = IdGenerator()
        self.username = username
        self.password = password
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone_number
        self.houses = []

    def add_house(self, house:House):
        self.houses.append(house)

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=None)
    
    def __str__(self):
        return f"\033[93mUserId: {self.user_id}, Username: {self.username}, Password: {self.password}, Email: {self.email}, First Name: {self.first_name}, Last Name: {self.last_name}, Phone Number: {self.phone}, Houses: {len(self.houses)} {self.houses}\033[0m"