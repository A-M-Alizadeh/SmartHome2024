from User import User
from House import House
from Sensor import Sensor
from SensorTypes import SensorTypes

usr1 = User("Johny01", "JohnDoe@gmail.com", "John", "Doe", "123456789")
usr2 = User("Jane", "Doe", "a@a.com")

house2 = House( "Corso Traiano","Ali's House")
house1 = House( "Corso Francia","John's House")
house3 = House( "Corso Tarantino","John's House")

temp_sensor = Sensor( SensorTypes.TEMPERATURE)
hum_sensor = Sensor( SensorTypes.HUMIDITY)
temp_sensor2 = Sensor( SensorTypes.TEMPERATURE)
hum_sensor2 = Sensor( SensorTypes.HUMIDITY)

usr1.add_house(house1)
usr2.add_house(house2)
usr1.add_house(house3)

house1.add_sensor(temp_sensor)
house1.add_sensor(hum_sensor)

house2.add_sensor(temp_sensor2)
house2.add_sensor(hum_sensor2)

print(usr1)
print(usr2)
print("-----------------------------------------------------------------------------------------------")
print(house1)
print(house2)
print("-----------------------------------------------------------------------------------------------")
print(temp_sensor)
print(hum_sensor)
print(temp_sensor2)
print(hum_sensor2)


