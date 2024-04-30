@echo off

set DBConnectorPath=%CD%\DBService\DBConnector\dbServices.py

start cmd /k "python %DBConnectorPath%"
