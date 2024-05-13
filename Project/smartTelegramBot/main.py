import logging
from typing import Any, Dict, Tuple

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Bot
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackContext,
)
import os, json, requests
import time
import paho.mqtt.client as PahoMQTT

class MyMQTT:
    def __init__(self, clientID, broker, port, notifier):
        self.broker = broker
        self.port = port
        self.notifier = notifier
        self.clientID = clientID # this can be sensorId
        self._topic = ""
        self._isSubscriber = False
        # create an instance of paho.mqtt.client
        self._paho_mqtt = PahoMQTT.Client(PahoMQTT.CallbackAPIVersion.VERSION1,clientID, True)
        # register the callback
        self._paho_mqtt.on_connect = self.myOnConnect
        self._paho_mqtt.on_message = self.myOnMessageReceived

    def myOnConnect(self, paho_mqtt, userdata, flags, rc):
        print("Connected to %s with result code: %d" % (self.broker, rc))

    def myOnMessageReceived(self, paho_mqtt, userdata, msg):
        # A new message is received
        self.notifier.notify(msg.topic, msg.payload)


    def myPublish(self, topic, msg):
        # publish a message with a certain topic
        self._paho_mqtt.publish(topic, json.dumps(msg), 2)

    def mySubscribe(self, topic):

        # subscribe for a topic
        self._paho_mqtt.subscribe(topic, 2)
        # just to remember that it works also as a subscriber
        self._isSubscriber = True
        self._topic = topic
        print("subscribed to %s" % (topic))

    def start(self):
        # manage connection to broker
        self._paho_mqtt.connect(self.broker, self.port)
        self._paho_mqtt.loop_start()

    def unsubscribe(self):
        if (self._isSubscriber):
            # remember to unsuscribe if it is working also as subscriber
            self._paho_mqtt.unsubscribe(self._topic)

    def stop(self):
        if (self._isSubscriber):
            # remember to unsuscribe if it is working also as subscriber
            self._paho_mqtt.unsubscribe(self._topic)

        self._paho_mqtt.loop_stop()
        self._paho_mqtt.disconnect()

class SensorsSubscriber:
    def __init__(self,clientID, broker, port, topic, telegramBot, chat_id):
        self.mqttClient = MyMQTT(clientID, broker, port, self)
        self.topic = topic
        self.telegramBot = telegramBot
        self.chat_id = chat_id
    
    def notify(self, topic, payload): #use senML
        print("TELBOT ??? ", self.telegramBot, self.chat_id)
        try:
            if "humidity" in topic:
                print( f'sensor ${topic}:  ${payload}recieved')
                json_string = payload.decode('utf-8')
                data = json.loads(json_string)
                self.telegramBot.send_message(chat_id=self.chat_id, text=f'Humidity: ')
                # send an alarm if humidity is above 80%
                # self.sendDataToDB(data,self.findMicro('analytics'))
                # print(f'Writing data to InfluxDB: {str(data)}', 'yellow')

            if "temperature" in topic:
                print( f'sensor ${topic}:  ${payload}recieved')
                json_string = payload.decode('utf-8')
                data = json.loads(json_string)
                self.telegramBot.send_message(chat_id=self.chat_id, text=f'Temperature:')
                #send an alarm if temperature is above 40
                # self.sendDataToDB(data, self.findMicro('analytics'))
                # print(f'Writing data to InfluxDB: {str(data)}', 'yellow')
                
        except Exception as e:
            print(f'Error in Sending the message {str(e)}')

    def start(self):
        self.mqttClient.start()
        self.mqttClient.mySubscribe(self. topic)
        
    def stop(self):
        self.mqttClient.stop()

#Description of the prcoess of the bot
#here is a link to look at a sample to understand the process of the bot https://docs.python-telegram-bot.org/en/stable/examples.nestedconversationbot.html
#user the userData variable to simulate the data that will be received from the api
#The bot is a simple bot that allows the user to get the status of sensors of his houses

#The process of the bot is as follows:
#1- First there is a login button, the user has to login to the system
#2- when the user clicks on the button two other buttons called username and password will appear
#3- the user has to enter his username and password
#4- the bot will save the username password ina variable called credentials
#5- userData is read from a json file and saved in a variable called userData
#6- user sees a button called Houses and when it is clicked users sees a list of buttons of the houses names
#7- the user will click on the house he wants to get the status of the sensors
#8- the user will see the list of sensors of the house
#9- when a sensor is clicked the user will get the status of the sensor
#10- the user can click on the back button to go back to the list of sensors
#11- the user can click on the back button to go back to the list of houses
#12- the user can click on the logout button to logout from the system
#13 in each step the data will be saved in a variable

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(f'./config.json') as json_file: #{path}smartTelegramBot/config.json
    config = json.load(json_file)

def findMicro(microName, microsInfo):
    for micro in microsInfo:
        if micro['name'] == microName:
            return micro
    return None
# //apis
# //login
async def authenticate(username: str, password: str) -> Dict[str, Any]:
    response = requests.post(f'{config["baseUrl"]}{config["basePort"]}/auth/login', json={"username": username, "password": password})
    return response.json()

async def getSensorsHistoricalData(restInfo, sensorIds: str, userData) -> Dict[str, Any]:
    url = f'{findMicro("analytics", restInfo)["url"]}{findMicro("analytics", restInfo)["port"]}/analytic/fullAnalytics'
    print("URL => ", url)
    print("JSON => ", {"sensorIds": sensorIds, "period": "5m"})
    response = requests.post(url, json={"sensorIds": sensorIds, "period": "5m"})
    return response.json()


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# State definitions for top level conversation
SELECTING_ACTION, TYPING_REPLY, SELECTING_HOUSE, SELECTING_SENSOR, SELECTING_SENSOR_DETTAILS = range(5)

# Map the state to a human readable string
state_map = {
    SELECTING_ACTION: "SELECTING_ACTION",
    TYPING_REPLY: "TYPING_REPLY",
    SELECTING_HOUSE: "SELECTING_HOUSE",
    SELECTING_SENSOR: "SELECTING_SENSOR",
}

# Callback data
(
    SELECT_HOUSE,
    SELECT_SENSOR,
    SELECT_SENSOR_DETTAILS,
    BACK,
    BACK_TO_PREVIOUS,
    LOGOUT,
    LOGIN,
    USERNAME,
    PASSWORD,
    DONE,
    SENSOR,
) = map(str, range(11))


class TeleBot:
    def __init__(self, token):
        self.token = token
        self.bot = Bot(token)
        self.chat_id = None

    # Define the different keyboard states
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Start the conversation and ask user for action."""

        response = requests.get(f'{config["baseUrl"]}{config["basePort"]}/public/fullservices')
        connectionInfo = response.json()
        print("RESPONSE ================================> ", connectionInfo)
        mqttInfo = connectionInfo['mqtt']
        restInfo = connectionInfo['micros']
        context.user_data["mqttInfo"] = connectionInfo
        context.user_data["restInfo"] = restInfo

        chat_id = update.message.chat_id
        print("CHAT ID =================================> ", chat_id)
        config["chat_id"] = chat_id

        reply_keyboard = [
            [InlineKeyboardButton("Login", callback_data=LOGIN)],
        ]

        await update.message.reply_text(
            "Hi! I'm your house sensor bot. I can provide you with the status of your sensors. "
            "To start, please click on the login button.",
            reply_markup=InlineKeyboardMarkup(reply_keyboard),
        )

        return SELECTING_ACTION

    def start_over(self,update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Starts the conversation over"""
        return self.start(update, context)

    async def login(self,update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Prompt user to login"""

        result = await authenticate(config["username"], config["password"])
        print("RESULT ==========================>>> ", result)
        context.user_data["userData"] = result

        reply_keyboard = [
            [InlineKeyboardButton("Username", callback_data=USERNAME), InlineKeyboardButton("Password", callback_data=PASSWORD)],
            [InlineKeyboardButton("Show Houses", callback_data=DONE)],
            [InlineKeyboardButton("Back", callback_data=BACK)],
        ]

        message = update.message or update.callback_query.message

        await message.reply_text(
            "Please enter your username and password.",
            reply_markup=InlineKeyboardMarkup(reply_keyboard),
        )

        return SELECTING_ACTION


    async def username(self,update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Prompt user to enter username"""
        message = update.message or update.callback_query.message
        username = message.text  # Get the entered username
        context.user_data["username"] = username  # Store the username in user_data

        await message.reply_text("Please enter your password.")

        return TYPING_REPLY


    async def password(self,update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Prompt user to enter password"""
        message = update.message or update.callback_query.message
        password = message.text  # Get the entered password
        context.user_data["password"] = password  # Store the password in user_data

        await message.reply_text("Trying to login...")

        return TYPING_REPLY

    async def done(self,update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Prompt user to enter password"""
        message = update.message or update.callback_query.message
        await message.reply_text("Trying to login...")

        return TYPING_REPLY


    async def fillHousesData(self,update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Fill the houses data"""
        # houses = userData["houses"]
        houses = context.user_data["userData"]["houses"]
        reply_keyboard = [
            [InlineKeyboardButton(house["title"], callback_data=f"{SELECT_HOUSE}:{house['house_id']}")] 
            for house in houses
        ]
        reply_keyboard.append([InlineKeyboardButton("Logout", callback_data=LOGOUT)])
        message = update.message or update.callback_query.message

        await message.reply_text(
            "Please select a house:", reply_markup=InlineKeyboardMarkup(reply_keyboard)
        )

        return SELECTING_HOUSE


    async def fillSensorsData(self,update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Fill the sensors data when a house is selected"""
        callback_data = update.callback_query.data.split(":")

        house_id = callback_data[1]  # Extract the house_id from the callback data
        house = next((house for house in context.user_data["userData"]["houses"] if house["house_id"] == house_id), None)  

        # if house is None:
        #     await update.callback_query.answer("Invalid house selected.")
        #     return SELECTING_HOUSE


        sensors = [sensor for sensor in house["sensors"] if sensor["type"] != "AIR_CONDITIONER"] # Get the sensors of the selected house

        result = await getSensorsHistoricalData(context.user_data["restInfo"], [sensor["sensor_id"] for sensor in sensors], context.user_data["userData"])
        context.user_data["sensorsStats"] = result

        for sensor in sensors:
            sensor["stats"] = next((stat for stat in result if stat["sensorId"] == sensor["sensor_id"]), None)

        print("SENSOR => ", sensor)
        
        print("RESULT => ", result)
        reply_keyboard = [[InlineKeyboardButton(f'{sensor["type"]}        Min:{round(sensor["stats"]["min"],1)}, Max:{round(sensor["stats"]["max"],1)}, Mean: {round(sensor["stats"]["mean"],1)}, last:{round(sensor["stats"]["lastValue"],1)}', callback_data=f"{SELECT_SENSOR}:{sensor['sensor_id']}")] for sensor in sensors]
        reply_keyboard.append([InlineKeyboardButton("Back", callback_data=BACK_TO_PREVIOUS)])

        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            "Please select a sensor:", reply_markup=InlineKeyboardMarkup(reply_keyboard)
        )

        return SELECTING_SENSOR

    async def fetchAllData(self,update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Prompt user to select a house"""
        # Here you would call fillHousesData instead of calling fillSensorsData directly
        return await self.fillHousesData(update, context)

    async def select_sensor(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Prompt user to select a sensor"""
        # Here you would call fillSensorsData instead of calling fillSensorDetails directly
        return await self.fillSensorsData(update, context)
    
    async def logout(self,update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Logout user"""
        reply_keyboard = [
            [InlineKeyboardButton("Login", callback_data=LOGIN)],
        ]

        await update.message.reply_text(
            "You have been logged out. Please click on the login button to login again.",
            reply_markup=InlineKeyboardMarkup(reply_keyboard),
        )

        return SELECTING_ACTION

    async def end(self,update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """End conversation from inline button"""
        await update.callback_query.answer()
        await update.callback_query.edit_message_text("Goodbye!")

        return ConversationHandler.END

    async def backToPrevious(self,update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """End conversation from inline button"""
        await update.callback_query.answer()
        await update.callback_query.edit_message_text("Selecting house...")

        return SELECTING_HOUSE



    def error(self,update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Log Errors caused by Updates."""
        logger.warning('Update "%s" caused error "%s"', update, context.error)

        return ConversationHandler.END


    def main(self) -> None:
        # """Run the bot."""
        # # Create the Application
        app = Application.builder().token(config["TOKEN"]).build()

        # Add the command handlers
        app.add_handler(CommandHandler("start", self.start))
        app.add_handler(CommandHandler("stop", self.end))

        # Add the callback query handlers
        app.add_handler(CallbackQueryHandler(self.login, pattern=f"^{LOGIN}$"))
        app.add_handler(CallbackQueryHandler(self.username, pattern=f"^{USERNAME}$"))
        app.add_handler(CallbackQueryHandler(self.password, pattern=f"^{PASSWORD}$"))
        app.add_handler(CallbackQueryHandler(self.fillHousesData, pattern=f"^{DONE}$")) #this should be done
        app.add_handler(CallbackQueryHandler(self.fillSensorsData, pattern=f"^{SELECT_SENSOR}$"))
        app.add_handler(CallbackQueryHandler(self.end, pattern=f"^{LOGOUT}$"))
        app.add_handler(CallbackQueryHandler(self.backToPrevious, pattern=f"^{BACK_TO_PREVIOUS}$"))
        app.add_handler(CallbackQueryHandler(self.end, pattern=f"^{BACK}$"))
        # app.add_handler(CallbackQueryHandler(backToPrevious, pattern=f"^{BACK}$"))
        # app.add_handler(CallbackQueryHandler(fetchAllData, pattern=f"^{BACK}$"))
        # app.add_handler(CallbackQueryHandler(backToPrevious, pattern=f"^{BACK}$"))

        # # Add the callback query handler for selecting a house
        app.add_handler(CallbackQueryHandler(self.fillSensorsData))

        # Add the message handler
        app.add_handler(MessageHandler(filters.Text, self.start))

        # Add the error handler
        app.add_error_handler(self.error)

        # Start the MQTT Subscriber
        # myBot = Bot(config["TOKEN"])
        myBot = app.bot
        customTopic = "smart_house"+"/"+config['userId']+"/#"
        print("CUSTOM TOPIC===========> ", customTopic)
        subscriber = SensorsSubscriber("smartHouse"+'teleBotSubscriber', "test.mosquitto.org", 1883, customTopic, myBot, "34026780")
        subscriber.start()
        # while True:
        #     time.sleep(1)

        # Start the Bot
        app.run_polling()


if __name__ == "__main__":
    telBot = TeleBot(config["TOKEN"])
    telBot.main()