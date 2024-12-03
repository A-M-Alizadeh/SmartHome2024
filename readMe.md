Promo: https://youtu.be/yrzlZDTjVYI

Demonstration: https://youtu.be/HB25DsqmRJo

Slides: https://www.canva.com/design/DAGFUAekRl8/rK_VpgdL51GZ_64KQpuhAg/edit?utm_content=DAGFUAekRl8&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton


[![Watch the demo](https://img.youtube.com/vi/VIDEO_ID/0.jpg)](https://youtu.be/HB25DsqmRJo) 

# Smart House (IoT)
This project aims to make any home smart using two sensors namely Humidity and Temperature. It is composed of 3 main parts : 
- core - backend
- web dashboard
- mobile Application
- Telegram Bot

>>Needs to be mentioned that the data is not aquired using raspberry-pi and real sensors and instead is Emulated using python.
---
**Backend:**
Implemented with Microservice Pattern which makes the project modular and maitenance more convenient. it consists of:
- MQTT Microservices (Paho-Mqtt)[publish/subscribe paradigm]
- REST Api (CherryPy)[request/response paradigm]
- Database (InfluxDB)

**Web Dashboard:**
Enabling users to register and add house and related sensors

**Mobile Application:**
Enables users to track the environment conditions and send Direct Command to air-conditioning devices

**Telegram Bot:**
Provides limited features of Mobile Application

## Diagram of the Project
![Project Diagram](https://github.com/A-M-Alizadeh/SmartHome2024/blob/main/Proposal/IOT-PoposalDiagram.png)

## Screenshots
![Project Diagram](https://via.placeholder.com/468x300?text=App+Screenshot+Here)

