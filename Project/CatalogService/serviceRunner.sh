#!/bin/sh

#if you want to run this file then you need to remove this : /CatalogService from the path
#otherwise runn all modules from allServiceRunner.sh
catalogServicePath=$(pwd)"/CatalogService/Catalog/CatalogService.py"

# Run the Pub and Sub services for Humidity
osascript -e 'tell app "Terminal"
    do script "python3 '$catalogServicePath'"
end tell'