# docker ps
# docker exec -it 1978726fb19b bash
# cd some/places
# python some_script.py



# -------------------------------------------------------------------step1-----------------------------------------------------
# run influxd
# ------------------------------------------------- step2 already works if you run containers ---------------------------------
# run Docker shit
# here some services run:
# in Catalog:
#   - catalogService
# in CommandCenter:
#   - commandCenterService
# in DBService:
#   - dbService
# in DevicePubs:
#   - tempPub
# in DeviceSubs:
#   - tempSub
# --------------------------------------------------- step3 Run Manually in interactive mode ----------------------------------
# in commandCenter:
# cd CommandCenter
#  - analyticsSchedule.py

# in DevicePublishers:
# cd pub
#  - humidityPublisher.py
#  - airConditionSubscriber.py

# in DeviceSubscribers:
# cd sub
#   - humiditySubscriber.py