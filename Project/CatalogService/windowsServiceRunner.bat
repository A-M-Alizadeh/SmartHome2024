@echo off

rem Define the path to the CatalogService.py script
set "catalogServicePath=%CD%\CatalogService\Catalog\CatalogService.py"

rem Run the Python script for the CatalogService in a new PowerShell window
start powershell -NoExit -Command "python '%catalogServicePath%'"