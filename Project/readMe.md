# Smart House (IoT)

To properly set up the project and enable smooth importing of modules, follow these steps:

1. **Navigate to the Project Folder:**
```
cd /your/path/to/project
```
2. **Install the Project as an Editable Package:**
```
pip install -e .
pip insstall cherrypy
pip install requests
```

This command installs the project as an editable package, allowing you to import modules seamlessly from any script within the project.


3. **Run Your Scripts:**
- If your scripts are at the same level as the `project` folder:
  ```
  python script_name.py
  ```
Now, you can import your modules using clean and relative imports throughout your project.

diff@@ No matter where the modules are, as long as you add __init__.py file inside the directory you can call it wherever you need. @@

**Authentication:**
- Authentication is Done implementing the Cherrypy Simple Authetication Mechanism. https://docs.cherrypy.dev/en/latest/basics.html#id28
```
+ 1. Basic Authentication: CherryPy provides a basic authentication tool that can be used to require users to authenticate before accessing certain parts of your site.

+ 2. SSL/TLS Encryption:To secure the connection using SSL/TLS, you can use CherryPy's tools.https tool. You need to have an SSL certificate and private key.
```

**Database:**
- InfluxDB is used In order to store the sensor records, InfluxDB is designed to store timeseries



**Project Structure**

project/
├── Auth/
│   ├── init.py
│   └── Authentication.py  # Handles authentication logic
├── Catalog/
│   ├── init.py
├── DAO/  # Data Access Object layer (may not be used yet)
│   ├── init.py
├── DB/
│   ├── init.py  # Database configuration and interaction
├── Microservices/  # Potential future microservices architecture
│   ├── init.py
├── ML/  # Machine Learning for potential data analysis
│   ├── init.py
│   └── MIModel.py  # (placeholder for future ML model)
├── Models/
│   ├── init.py
│   ├── House.py  # Defines the House model
│   ├── Sensor.py  # Defines the Sensor model
│   ├── SensorTypes.py  # Defines different sensor types
│   ├── Test.py  # Unit tests for models (optional)
│   └── User.py  # Defines the User model
├── Simulators/
│   ├── init.py
│   ├── HumiditySim.py  # Simulates humidity data (for testing)
│   ├── TemperatureSim.py  # Simulates temperature data (for testing)
│   ├── Test.py  # Unit tests for simulators (optional)
│   ├── SmartHoselOT.egg-info/  # Generated files for packaging
│       ├── dependency_links.txt
│       ├── PKG-INFO
│       ├── SOURCES.txt
│       └── top_level.txt
│   └── Utils/
│       ├── init.py
│       └── Utils.py  # Utility functions
├── Utils/
│   ├── init.py
│   └── Utils.py  # General utility functions
├── init.py  # Makes the project folder a Python package
├── README.md  # This file (project documentation)
└── setup.py  # Configuration for packaging the project