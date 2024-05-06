import datetime
import json
import os


config = {}
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(f'{path}/CommandCenter/config.json') as json_file:
        config = json.load(json_file)

def checker(current_hour = datetime.datetime.now().hour):
    is_off_hours = False
    for key, value in config["offHours"].items():
        start_hour = value["start"]
        end_hour = value["end"]
        
        # Handling the case where the period spans across two days
        if start_hour > end_hour:
            if current_hour >= start_hour or current_hour < end_hour:
                is_off_hours = True
                break
        # Handling the case where the period is within the same day
        else:
            if start_hour <= current_hour <= end_hour:
                is_off_hours = True
                break
    print(f'Current hour: {current_hour}')
    print(f'Is off hours: {is_off_hours}')


if __name__ == '__main__':
     for i in range(0, 24):
         checker(i)



# -----------------AIR-CONDITIONER STATUS-----------------
#     *     
#   * * *   
# * * * * * 
#   * * *   
#     *     
# AIR-CONDITIONER STATUS:    ON
# IDEAL HUMIDITY:            44.53 %
# IDEAL TEMPERATURE:         33.39 c