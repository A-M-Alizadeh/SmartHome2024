#!/bin/sh

catalog_path=$(pwd)"/CatalogService/Catalog/CatalogService.py"
db_path=$(pwd)"/DBService/DBConnector/dbServices.py"
command_path=$(pwd)"/CommandCenterService/CommandCenter/commandCenterService.py"
air_sub_path=$(pwd)"/AirConditionerSubscriber/pub/airConditionSubscriber.py"
auto_path=$(pwd)"/AutomaticCommand/CommandCenter/analyticsSchedule.py"
hum_pub_path=$(pwd)"/HumidityPublisher/pub/humidityPublisher.py"
temp_pub_path=$(pwd)"/TemperaturePublisher/pub/temperaturePublisher.py"
subs_path=$(pwd)"/DeviceSubscribers/sub/DeviceSubscribers.py"

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

