start cmd /k "$(pwd)/CatalogService/serviceRunner.bat"
start cmd /k influxd
timeout /t 3
start cmd /k "$(pwd)/CommandCenterService/serviceRunner.bat"
start cmd /k "$(pwd)/DBService/serviceRunner.bat"
start cmd /k "$(pwd)/DevicePublishers/serviceRunner.bat"
start cmd /k "$(pwd)/DeviceSubscribers/serviceRunner.bat"