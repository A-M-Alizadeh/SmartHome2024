
from User import User
from House import House
from Sensor import TemperatureSensor, HumiditySensor
from SensorTypes import SensorTypes
from Utils.Utils import IdGenerator

usr1 = User(IdGenerator(), "Johny01", "JohnDoe@gmail.com", "John", "Doe", "123456789")
usr2 = User("Jane", "Doe", "a@a.com")

house2 = House(IdGenerator(), "Corso Traiano","Ali's House")
house1 = House(IdGenerator(), "Corso Francia","John's House")

temp_sensor = TemperatureSensor(IdGenerator(), SensorTypes.TEMPERATURE)
hum_sensor = HumiditySensor(IdGenerator(), SensorTypes.HUMIDITY)

temp_sensor2 = TemperatureSensor(IdGenerator(), SensorTypes.TEMPERATURE)
hum_sensor2 = HumiditySensor(IdGenerator(), SensorTypes.HUMIDITY)

usr1.add_house(house1)
usr2.add_house(house2)

house1.add_sensor(temp_sensor)
house1.add_sensor(hum_sensor)

house2.add_sensor(temp_sensor2)
house2.add_sensor(hum_sensor2)

# print(usr1)
# print(usr2)
# print(house1)
# print(house2)
# print(temp_sensor)
print(hum_sensor)
print(temp_sensor2)


