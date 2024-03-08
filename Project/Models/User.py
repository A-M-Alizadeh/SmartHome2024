from House import House
from Utils.Utils import IdGenerator
class User:
    def __init__(self, username, email, first_name='', last_name='', phone_number=''):
        self.user_id = IdGenerator()
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.houses = []

    def add_house(self, house:House):
        self.houses.append(house)
    
    def __str__(self):
        return f"\033[93mUserId: {self.user_id}, Username: {self.username}, Email: {self.email}, First Name: {self.first_name}, Last Name: {self.last_name}, Phone Number: {self.phone_number}, Houses: {len(self.houses)} {self.houses}\033[0m"