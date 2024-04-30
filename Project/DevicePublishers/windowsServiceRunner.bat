@echo off

set airCondSubPath=%CD%\DevicePublishers\pub\airConditionSubscriber.py
set humidPubPath=%CD%\DevicePublishers\pub\humidityPublisher.py
set tempPubPath=%CD%\DevicePublishers\pub\temperaturePublisher.py

start cmd /k "python %airCondSubPath%"
start cmd /k "python %humidPubPath%"
start cmd /k "python %tempPubPath%"