#!/bin/sh

hum_Pub_path=$(pwd)"/Microservices/MQTT/humidityPublisher.py"
hum_Sub_path=$(pwd)"/Microservices/MQTT/humiditySubscriber.py"

temp_Pub_path=$(pwd)"/Microservices/MQTT/temperaturePublisher.py"
temp_Sub_path=$(pwd)"/Microservices/MQTT/tempratureSubscriber.py"

air_Sub_path=$(pwd)"/Microservices/MQTT/airConditionSubscriber.py"

# Run the Pub and Sub services for Humidity
osascript -e 'tell app "Terminal"
    do script "python3 '$hum_Pub_path'"
end tell'
osascript -e 'tell app "Terminal"
    do script "python3 '$hum_Sub_path'"
end tell'

# Run the Pub and Sub services for Temperature
osascript -e 'tell app "Terminal"
    do script "python3 '$temp_Pub_path'"
end tell'
osascript -e 'tell app "Terminal"
    do script "python3 '$temp_Sub_path'"
end tell'
# Run the Pub and Sub services for Air Condition

sleep 2

osascript -e 'tell app "Terminal"
    do script "python3 '$air_Sub_path'"
end tell'