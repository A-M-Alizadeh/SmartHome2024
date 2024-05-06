#!/bin/sh

catalog_path=$(pwd)"/CatalogService/Catalog/CatalogService.py"
db_path=$(pwd)"/DBService/DBConnector/dbServices.py"
command_path=$(pwd)"/CommandCenterService/CommandCenter/commandCenterService.py"
air_sub_path=$(pwd)"/AirConditionerSubscriber/pub/airConditionSubscriber.py"
auto_path=$(pwd)"/AutomaticCommand/CommandCenter/decisionMaker.py"
hum_pub_path=$(pwd)"/HumidityPublisher/pub/humidityPublisher.py"
temp_pub_path=$(pwd)"/TemperaturePublisher/pub/temperaturePublisher.py"
subs_path=$(pwd)"/DeviceSubscribers/sub/DeviceSubscribers.py"

air2_sub_path=$(pwd)"/AirConditionerSubscriber2/pub/airConditionSubscriber.py"
auto2_path=$(pwd)"/AutomaticCommand2/CommandCenter/decisionMaker.py"
hum2_pub_path=$(pwd)"/HumidityPublisher2/pub/humidityPublisher.py"
temp2_pub_path=$(pwd)"/TemperaturePublisher2/pub/temperaturePublisher.py"

osascript -e 'tell app "Terminal"
    do script "influxd"
end tell'

osascript -e 'tell app "Terminal"
    do script "python3 '$catalog_path'"
end tell'

sleep 3

osascript -e 'tell app "Terminal"
    do script "python3 '$db_path'"
end tell'
osascript -e 'tell app "Terminal"
    do script "python3 '$command_path'"
end tell'
osascript -e 'tell app "Terminal"
    do script "python3 '$air_sub_path'"
end tell'
osascript -e 'tell app "Terminal"
    do script "python3 '$auto_path'"
end tell'
osascript -e 'tell app "Terminal"
    do script "python3 '$hum_pub_path'"
end tell'
osascript -e 'tell app "Terminal"
    do script "python3 '$temp_pub_path'"
end tell'
osascript -e 'tell app "Terminal"
    do script "python3 '$subs_path'"
end tell'

# Second House
osascript -e 'tell app "Terminal"
    do script "python3 '$air2_sub_path'"
end tell'
osascript -e 'tell app "Terminal"
    do script "python3 '$auto2_path'"
end tell'
osascript -e 'tell app "Terminal"
    do script "python3 '$hum2_pub_path'"
end tell'
osascript -e 'tell app "Terminal"
    do script "python3 '$temp2_pub_path'"
end tell'

