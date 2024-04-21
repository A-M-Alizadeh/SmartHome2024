#!/bin/sh

hum_Pub_path=$(pwd)"/Microservices/MQTT/humidityPublisher.py"
hum_Sub_path=$(pwd)"/Microservices/MQTT/humiditySubscriber.py"

temp_Pub_path=$(pwd)"/Microservices/MQTT/temperaturePublisher.py"
temp_Sub_path=$(pwd)"/Microservices/MQTT/tempratureSubscriber.py"

air_Sub_path=$(pwd)"/Microservices/MQTT/airConditionSubscriber.py"
# command_Pub_path=$(pwd)"/Microservices/MQTT/commandPublisher.py"

full_sub_path=$(pwd)"/Microservices/MQTT/fullSubscriber.py"

# Run Catalog Service --- this will run in a new terminal ***This is the first service to run***

# Run the Pub and Sub services for Humidity
osascript -e 'tell app "Terminal"
    do scrip "python3 '$hum_Pub_path'"
end tell'
osascript -e 'tell app "Terminal"
    do scrip "python3 '$hum_Sub_path'"
end tell'

# Run the Pub and Sub services for Temperature
osascript -e 'tell app "Terminal"
    do scrip "python3 '$temp_Pub_path'"
end tell'
osascript -e 'tell app "Terminal"
    do scrip "python3 '$temp_Sub_path'"
end tell'
# Run the Pub and Sub services for Air Condition

osascript -e 'tell app "Terminal"
    do scrip "python3 '$air_Sub_path'"
end tell'
# osascript -e 'tell app "Terminal"
#     do script "python3 '$command_Pub_path'"
# end tell'

# Run the full subscriber
osascript -e 'tell app "Terminal"
    do scrip "python3 '$full_sub_path'"
end tell'
