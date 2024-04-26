#!/bin/sh

catalogServicePath=$(pwd)"/Catalog/CatalogService.py"

# Run the Pub and Sub services for Humidity
osascript -e 'tell app "Terminal"
    do script "python3 '$catalogServicePath'"
end tell'