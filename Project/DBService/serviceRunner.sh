#!/bin/sh

DBConnectorPath=$(pwd)"/DBService/DBConnector/dbServices.py"

# Run the Pub and Sub services for Humidity
osascript -e 'tell app "Terminal"
    do script "python3 '$DBConnectorPath'"
end tell'