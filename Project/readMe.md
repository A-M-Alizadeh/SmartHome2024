
# Smart House (IoT)
python version = 3.11.6
influxDB version = 2.7.5

To properly set up the project and enable smooth importing of modules, follow these steps:

1. **Navigate to the Project Folder:**
```
cd /your/path/to/project
```
2. **Install the Project as an Editable Package:**
```
pip insstall cherrypy
pip install influxdb
pip install paho_mqtt
pip install pandas
pip install 'influxdb-client[ciso]' -- i think this one works
pip install pyjwt #or pip install jwt in case of error
pip install requests
pip install joblib
pip install statsmodels 0.14.1
pip install schedule
pip install cherrypy-cors
pip install schedule
pip install python-telegram-bot-21.1.1
pip install aiogram-3.6.0
pip install -e .
```

you might need to use `pip3` instead of `pip`
This command installs the project as an editable package, allowing you to import modules seamlessly from any script within the project.


3. **Run Your Scripts:**
- If your scripts are at the same level as the `project` folder:
  ```
  python script_name.py
  ```
Now, you can import your modules using clean and relative imports throughout your project.

diff
@@ No matter where the modules are, as long as you add __init__.py file inside the directory you can call it wherever you need. @@

---
i. **Authentication:**
- Authentication is Done implementing the Cherrypy Simple Authetication Mechanism. https://docs.cherrypy.dev/en/latest/basics.html#id28
``` bash
+ 1. `Basic Authentication`: CherryPy provides a basic authentication tool that can be used to require users to authenticate before accessing certain parts of your site.

+ 2. `SSL/TLS Encryption`:To secure the connection using SSL/TLS, you can use CherryPy's tools.https tool. You need to have an SSL certificate and private key.
```

ii. **Authorization:**
- Lorem Impsum sdfsdf asdfasd asdfasdf

iii. **Database:**
- `InfluxDB` is used In order to store the sensor records, InfluxDB is designed to store timeseries

---
**Project Structure**

```bash
project/
├───Auth/
│   ├───Authenticatio.py
│   └───__init__.py
├───Catalog/
│   ├───__pycache__/
│   │   ├───CatalogManager.cpython-39.pyc
│   │   └───__init__.cpython-39.pyc
│   ├───Catalog.json
│   ├───CatalogBackup.json
│   ├───CatalogManager.py
│   ├───CatalogService.py
│   └───__init__.py
├───DAO/
│   └───__init__.py
├───DB/
│   ├───Test.py
│   └───__init__.py
├───ML/
│   ├───MlModel.py
│   └───__init__.py
├───Microservices/
│   ├───MQTT/
│   │   └───__init__.py
│   ├───REST/
│   │   ├───UserService.py
│   │   ├───__init__.py
│   │   └───index.py
│   └───__init__.py
├───Models/
│   ├───__pycache__/
│   │   ├───House.cpython-39.pyc
│   │   ├───Sensor.cpython-39.pyc
│   │   ├───SensorTypes.cpython-39.pyc
│   │   ├───User.cpython-39.pyc
│   │   └───__init__.cpython-39.pyc
│   ├───House.py
│   ├───Sensor.py
│   ├───SensorTypes.py
│   ├───Test.py
│   ├───User.py
│   ├───__init__.py
│   └───tempCodeRunnerFile.py
├───Simulators/
│   ├───__pycache__/
│   │   ├───HumiditySim.cpython-39.pyc
│   │   └───TemperatureSim.cpython-39.pyc
│   ├───HumiditySim.py
│   ├───TemperatureSim.py
│   ├───Test.py
│   └───__init__.py
├───SmartHoseIOT.egg-info/
│   ├───PKG-INFO
│   ├───SOURCES.txt
│   ├───dependency_links.txt
│   └───top_level.txt
├───Utils/
│   ├───__pycache__/
│   │   ├───Utils.cpython-39.pyc
│   │   └───__init__.cpython-39.pyc
│   ├───Utils.py
│   └───__init__.py
├───__init__.py
├───readMe.md
└───setup.py
```
Tree Generated Using `tree-extended` needs to be installed via `npm install tree`

https://stackoverflow.com/questions/45368535/influxdb-single-or-multiple-measurement


Read this to dockerize: https://github.com/Lawouach/cherrypy-docker-hello-world/tree/master
don't forget cherrypy.config.update({'server.socket_host': '0.0.0.0', ...})

#docker build -t imagename:tag .
#docker run -p 8083:8083 imagename:tag
#docker run -p 8083:8083 -v /Users/rohit/Downloads/Project/CommandCenterService:/app imagename:tag
#docker start containerid or containername
#docker stop containerid or containername


docker exec -it 1978726fb19b bash
