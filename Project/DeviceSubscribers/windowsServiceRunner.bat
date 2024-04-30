@echo off

set humidSubPath=%CD%\DeviceSubscribers\sub\humiditySubscriber.py
set tempSubPath=%CD%\DeviceSubscribers\sub\tempratureSubscriber.py

start cmd /k "python %humidSubPath%"
start cmd /k "python %tempSubPath%"