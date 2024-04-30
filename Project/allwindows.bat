@echo off

rem Run CatalogService
call CatalogService\windowsServiceRunner.bat

rem Start InfluxDB
start "InfluxDB" influxd

rem Wait for InfluxDB to start (adjust the delay as needed)
timeout /t 3 >nul

rem Run CommandCenterService
call CommandCenterService\windowsServiceRunner.bat

rem Run DBService
call DBService\windowsServiceRunner.bat

rem Run DevicePublishers
call DevicePublishers\windowsServiceRunner.bat

rem Run DeviceSubscribers
call DeviceSubscribers\windowsServiceRunner.bat