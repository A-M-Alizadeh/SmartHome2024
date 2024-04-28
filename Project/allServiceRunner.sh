#!/bin/sh

(bash $(pwd)"/CatalogService/serviceRunner.sh")

osascript -e 'tell app "Terminal"
    do script "influxd"
end tell'

sleep 3
(bash $(pwd)"/CommandCenterService/serviceRunner.sh")
(bash $(pwd)"/DBService/serviceRunner.sh")
(bash $(pwd)"/DevicePublishers/serviceRunner.sh")
(bash $(pwd)"/DeviceSubscribers/serviceRunner.sh")
