#!/bin/sh

Cat_path=$(pwd)"/Catalog/CatalogService.py"
Auth_path=$(pwd)"/Auth/AuthService.py"
Command_path=$(pwd)"/Microservices/REST/commandCenterService.py"
Analytics_path=$(pwd)"/Microservices/REST/analyticsService.py"
automatic_command_pah=$(pwd)"/Microservices/REST/analyticsSchedule.py"
# Run Catalog Service --- this will run in a new terminal ***This is the first service to run***
# This is because the Every Service depends on the Catalog service
osascript -e 'tell app "Terminal"
    do script "python3 '$Cat_path'"
end tell'

# Wait for 2 seconds before running the Auth Service
sleep 2

# Run Auth Service --- this will run in a new terminal
# osascript -e 'tell app "Terminal"
#     do script "python3 '$Auth_path'"
# end tell'

# sleep 2

# Run Auth Service --- this will run in a new terminal
osascript -e 'tell app "Terminal"
    do script "python3 '$Command_path'"
end tell'

# sleep 2

# Run Auth Service --- this will run in a new terminal
osascript -e 'tell app "Terminal"
    do script "python3 '$Analytics_path'"
end tell'

sleep 2
# Run the automatic command
osascript -e 'tell app "Terminal"
    do script "python3 '$automatic_command_pah'"
end tell'
