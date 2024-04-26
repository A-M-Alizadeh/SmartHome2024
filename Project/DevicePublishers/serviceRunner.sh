#!/bin/sh

airCondSubPath=$(pwd)"/pub/airConditionSubscriber.py"
humidPubPath=$(pwd)"/pub/humidityPublisher.py"
tempPubPath=$(pwd)"/pub/temperaturePublisher.py"


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