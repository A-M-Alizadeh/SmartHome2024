#!/bin/sh

commandCenterPath=$(pwd)"/CommandCenterService/CommandCenter/commandCenterService.py"
autoCommandPath=$(pwd)"/CommandCenterService/CommandCenter/analyticsSchedule.py"

# Run the Pub and Sub services for Humidity
osascript -e 'tell app "Terminal"
    do script "python3 '$commandCenterPath'"
end tell'

osascript -e 'tell app "Terminal"
    do script "python3 '$autoCommandPath'"
end tell'