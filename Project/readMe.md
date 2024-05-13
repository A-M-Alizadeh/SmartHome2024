
Promo: https://youtu.be/yrzlZDTjVYI
# Smart House (IoT)
python version = 3.11.6

influxDB version = 2.7.5

**To Run The Dockerized Version:**
```
Switch to dockerMain branch
cd Project
docker-compose up
```
**To Run Manually switch to main branch and do the following steps:**

To properly set up the project and enable smooth importing of modules, follow these steps:

1. **Navigate to the Project Folder:**
```
cd /your/path/to/project
```
1. **Navigate to each Folder Inside:**
```
cd /your/path/to/Module
```
3. **Install These Libraries and then the Module as Editable Package:**
```
pip insstall cherrypy
pip install influxdb
pip install paho_mqtt
pip install pandas
pip install influxdb-client[ciso]
pip install pyjwt #or pip install jwt in case of error
pip install requests
pip install joblib
pip install statsmodels 0.14.1
pip install schedule
pip install cherrypy-cors
pip install schedule
pip install python-telegram-bot-21.1.1
pip install -e .
```
```
cd /to/Project/Folder
sh allServiceRunner.sh
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
```
iii. **Database:**
- `InfluxDB` is used In order to store the sensor records, InfluxDB is designed to store timeseries

---
**Project Structure**

```bash
project/
├───AirConditionerSubscriber/
│   ├───PubService.egg-info/
│   ├───Utils/
│   ├───pub/
│   ├───Dockerfile
│   ├───__init__.py
│   ├───dockerRunner.sh
│   ├───requirements.txt
│   └───setup.py
├───AirConditionerSubscriber2/
│   ├───PubService.egg-info/
│   ├───Utils/
│   ├───pub/
│   ├───Dockerfile
│   ├───__init__.py
│   ├───dockerRunner.sh
│   ├───requirements.txt
│   └───setup.py
├───AutomaticCommand/
│   ├───CommandCenter/
│   ├───CommandCenterService.egg-info/
│   ├───Utils/
│   ├───Dockerfile
│   ├───__init__.py
│   ├───dockerRunner.sh
│   ├───requirements.txt
│   └───setup.py
├───CatalogService/
│   ├───Auth/
│   ├───Catalog/
│   ├───CatalogService.egg-info/
│   ├───Models/
│   ├───Utils/
│   ├───Dockerfile
│   ├───__init__.py
│   ├───dockerRunner.sh
│   ├───requirements.txt
│   └───setup.py
├───CommandCenterService/
│   ├───CommandCenter/
│   ├───CommandCenterService.egg-info/
│   ├───Simulators/
│   ├───Utils/
│   ├───Dockerfile
│   ├───__init__.py
│   ├───dockerRunner.sh
│   ├───requirements.txt
│   └───setup.py
├───DBService/
│   ├───DBConnector/
│   ├───DBService.egg-info/
│   ├───Utils/
│   ├───Dockerfile
│   ├───__init__.py
│   ├───dockerRunner.sh
│   ├───requirements.txt
│   └───setup.py
├───DeviceSubscribers/
│   ├───SubService.egg-info/
│   ├───Utils/
│   ├───sub/
│   ├───Dockerfile
│   ├───__init__.py
│   ├───dockerRunner.sh
│   ├───requirements.txt
│   └───setup.py
├───HumidityPublisher/
│   ├───PubService.egg-info/
│   ├───Simulators/
│   ├───Utils/
│   ├───pub/
│   ├───Dockerfile
│   ├───__init__.py
│   ├───dockerRunner.sh
│   ├───requirements.txt
│   └───setup.py
├───HumidityPublisher2/
│   ├───PubService.egg-info/
│   ├───Simulators/
│   ├───Utils/
│   ├───pub/
│   ├───Dockerfile
│   ├───__init__.py
│   ├───dockerRunner.sh
│   ├───requirements.txt
│   └───setup.py
├───TemperaturePublisher/
│   ├───PubService.egg-info/
│   ├───Simulators/
│   ├───Utils/
│   ├───pub/
│   ├───Dockerfile
│   ├───__init__.py
│   ├───dockerRunner.sh
│   ├───requirements.txt
│   └───setup.py
├───TemperaturePublisher2/
│   ├───PubService.egg-info/
│   ├───Simulators/
│   ├───Utils/
│   ├───pub/
│   ├───Dockerfile
│   ├───__init__.py
│   ├───dockerRunner.sh
│   ├───requirements.txt
│   └───setup.py
├───smartTelegramBot/
│   ├───__pycache__/
│   ├───Dockerfile
│   ├───backup.py
│   ├───config.json
│   ├───dockerRunner.sh
│   ├───main.py
│   ├───requirements.txt
│   └───sample.py
├───web/
│   ├───node_modules/
│   ├───public/
│   ├───src/
│   ├───.DS_Store
│   ├───.eslintrc.cjs
│   ├───.gitignore
│   ├───Dockerfile
│   ├───README.md
│   ├───index.html
│   ├───package-lock.json
│   ├───package.json
│   ├───requirements.txt
│   └───vite.config.js
├───.DS_Store
├───.env
├───allServiceRunner.sh
├───docker-compose.yaml
├───entrypoint.sh
└───readMe.md
```
Tree Generated Using `tree-extended` needs to be installed via `npm install tree`

https://stackoverflow.com/questions/45368535/influxdb-single-or-multiple-measurement


Read this to dockerize: https://github.com/Lawouach/cherrypy-docker-hello-world/tree/master
```
don't forget cherrypy.config.update({'server.socket_host': '0.0.0.0', ...})
also do the same for react app for vite to set the host to 0.0.0.0
```
```
#docker build -t imagename:tag .
#docker run -p 8083:8083 imagename:tag
#docker run -p 8083:8083 -v Project/CommandCenterService:/app imagename:tag
#docker start containerid or containername
#docker stop containerid or containername
docker exec -it 1978726fb19b bash
```