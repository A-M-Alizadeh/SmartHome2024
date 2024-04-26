#!/bin/sh

humidSubPath=$(pwd)"/sub/humiditySubscriber.py"
tempSubPath=$(pwd)"/sub/tempratureSubscriber.py"


# Run the Pub and Sub services for Humidity
osascript -e 'tell app "Terminal"
    do script "python3 '$humidSubPath'"
end tell'

osascript -e 'tell app "Terminal"
    do script "python3 '$tempSubPath'"
end tell'