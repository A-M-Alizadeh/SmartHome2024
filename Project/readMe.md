# Smart Home (IoT)

This project creates a smart home system using the Internet of Things (IoT) to automate tasks and enhance convenience.

Setting Up the Project
To ensure smooth module imports, follow these steps:

Navigate to the Project Folder:

Bash
cd /your/path/to/project
Use code with caution.
Install Required Packages:

Bash
pip install -e .  # Installs project as an editable package
pip install cherrypy requests  # Installs dependencies
Use code with caution.
pip install -e . allows importing modules seamlessly from anywhere within the project.
cherrypy and requests are external libraries used for authentication and communication.
Run Your Scripts:

If scripts are in the same level as the project folder:

Bash
python script_name.py
Use code with caution.
Now you can import modules using clear relative paths within your project.

Note: You can add __init__.py files to directories to make them Python packages, allowing imports from anywhere in the project structure.

Authentication
This project implements authentication using CherryPy's mechanisms:

Basic Authentication:

Users are prompted for credentials before accessing specific website parts.
Refer to CherryPy documentation for details: https://docs.cherrypy.dev/en/latest/basics.html#id28
SSL/TLS Encryption:

Secure connections using CherryPy's tools.https tool.
Requires an SSL certificate and private key.
Database
Sensor data is stored in InfluxDB, a time-series database optimized for handling large amounts of sensor readings.

Project Structure
(Utilizing colorful code blocks for better readability)

project/
├── Auth/
│   ├── __init__.py
│   └── Authentication.py  # Handles authentication logic
├── Catalog/
│   ├── __init__.py
├── DAO/  # Data Access Object layer (may not be used yet)
│   ├── __init__.py
├── DB/
│   ├── __init__.py  # Database configuration and interaction
├── Microservices/  # Potential future microservices architecture
│   ├── __init__.py
├── ML/  # Machine Learning for potential data analysis
│   ├── __init__.py
│   └── MIModel.py  # (placeholder for future ML model)
├── Models/
│   ├── __init__.py
│   ├── House.py  # Defines the House model
│   ├── Sensor.py  # Defines the Sensor model
│   ├── SensorTypes.py  # Defines different sensor types
│   ├── Test.py  # Unit tests for models (optional)
│   └── User.py  # Defines the User model
├── Simulators/
│   ├── __init__.py
│   ├── HumiditySim.py  # Simulates humidity data (for testing)
│   ├── TemperatureSim.py  # Simulates temperature data (for testing)
│   ├── Test.py  # Unit tests for simulators (optional)
│   ├── SmartHoselOT.egg-info/  # Generated files for packaging
│       ├── dependency_links.txt
│       ├── PKG-INFO
│       ├── SOURCES.txt
│       └── top_level.txt
│   └── Utils/
│       ├── __init__.py
│       └── Utils.py  # Utility functions
├── Utils/
│   ├── __init__.py
│   └── Utils.py  # General utility functions
├── __init__.py  # Makes the project folder a Python package
├── README.md  # This file (project documentation)
└── setup.py  # Configuration for packaging the project