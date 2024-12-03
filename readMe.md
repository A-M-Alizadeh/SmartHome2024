# Smart House (IoT)

This project aims to transform any home into a smart home using two sensors: Humidity and Temperature. The system is composed of four main parts:  
- **Core** - Backend  
- **Web Dashboard**  
- **Mobile Application**  
- **Telegram Bot**

**Note:** The data is emulated using Python, not acquired via Raspberry Pi or real sensors.

---

## 🚀 Project Overview  
The Smart House IoT system integrates the following components:  
- **Backend:** Implements the Microservice Pattern for modularity and easy maintenance.  
- **Web Dashboard:** Allows users to register, add houses, and manage related sensors.  
- **Mobile Application:** Enables users to monitor environment conditions and send commands to air-conditioning devices.  
- **Telegram Bot:** Provides essential features of the Mobile Application.

### 🔗 Demo and Promo Links  
- **Promo Video:** [Watch on YouTube](https://youtu.be/yrzlZDTjVYI)  
- **Demonstration Video:** [Watch on YouTube](https://youtu.be/HB25DsqmRJo)  
- **Slides:** [View on Canva](https://www.canva.com/design/DAGFUAekRl8/rK_VpgdL51GZ_64KQpuhAg/edit?utm_content=DAGFUAekRl8&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)

---

## ⚙️ Technical Architecture  
### **Backend:**
- Built with the **Microservice Pattern** to ensure scalability and ease of maintenance.  
- **MQTT Microservices (Paho-Mqtt):** Implements the publish/subscribe paradigm for real-time data exchange.  
- **REST API (CherryPy):** Enables communication using the request/response paradigm.  
- **Database (InfluxDB):** Stores environmental data for historical analysis.

### **Web Dashboard:**
- Allows users to manage home data and sensor configuration.  
- Built with a user-friendly interface for easy interaction.

### **Mobile Application:**
- Enables users to track environmental conditions and send commands to air-conditioning devices.  
- Built for Android using **React Native** for cross-platform compatibility.

### **Telegram Bot:**
- Provides access to some mobile app features directly through Telegram, for quick and easy interaction.

---

## 📊 Project Diagram  
![Project Diagram](https://github.com/A-M-Alizadeh/SmartHome2024/blob/main/Proposal/IOT-PoposalDiagram.png)  

---

## 📸 Screenshots  
### Web Dashboard:  
![Web Dashboard](https://via.placeholder.com/468x300?text=App+Screenshot+Here)  

### Mobile App:  
![Mobile App](https://via.placeholder.com/468x300?text=App+Screenshot+Here)

---

## 🛠️ Tech Stack  
- **Python:** Backend services and sensor emulation.  
- **MQTT:** Real-time messaging protocol.  
- **REST API (CherryPy):** Web service for communication.  
- **InfluxDB:** Time-series database.  
- **React Native:** Mobile app development.  
- **Telegram Bot API:** For bot integration.

---

## 🚀 Installation  
1. Clone the repository:  
   ```bash  
   git clone https://github.com/yourusername/smart-house-iot.git  
