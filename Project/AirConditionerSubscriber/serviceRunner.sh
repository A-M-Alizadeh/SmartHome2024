#!/bin/sh

airCondSubPath=$(pwd)"/DevicePublishers/pub/airConditionSubscriber.py"
humidPubPath=$(pwd)"/DevicePublishers/pub/humidityPublisher.py"
tempPubPath=$(pwd)"/DevicePublishers/pub/temperaturePublisher.py"


# Run the Pub and Sub services for Humidity
osascript -e 'tell app "Terminal"
    do script "python3 '$airCondSubPath'"
end tell'

osascript -e 'tell app "Terminal"
    do script "python3 '$humidPubPath'"
end tell'

osascript -e 'tell app "Terminal"
    do script "python3 '$tempPubPath'"
end tell'