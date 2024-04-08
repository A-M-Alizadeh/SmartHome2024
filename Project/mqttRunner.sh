#!/bin/sh

hum_Pub_path=$(pwd)"/Microservices/MQTT/humidityPublisher.py"
temp_pub_path=$(pwd)"/Microservices/MQTT/temperaturePublisher.py"
sub_path=$(pwd)"/Microservices/MQTT/Subscriber.py"

# Run Catalog Service --- this will run in a new terminal ***This is the first service to run***
# This is because the Every Service depends on the Catalog service
osascript -e 'tell app "Terminal"
    do script "python '$hum_Pub_path'"
end tell'

# Run Auth Service --- this will run in a new terminal
osascript -e 'tell app "Terminal"
    do script "python '$temp_pub_path'"
end tell'

# Wait for 2 seconds before running the Auth Service
sleep 2

# Run Auth Service --- this will run in a new terminal
osascript -e 'tell app "Terminal"
    do script "python '$sub_path'"
end tell'