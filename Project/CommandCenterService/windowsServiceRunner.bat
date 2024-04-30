@echo off

set commandCenterPath=%CD%\CommandCenterService\CommandCenter\commandCenterService.py
set autoCommandPath=%CD%\CommandCenterService\CommandCenter\analyticsSchedule.py

start cmd /k "python %commandCenterPath%"
start cmd /k "python %autoCommandPath%"