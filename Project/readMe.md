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
diff + 1. Basic Authentication: CherryPy provides a basic authentication tool that can be used to require users to authenticate before accessing certain parts of your site.

diff + 2. SSL/TLS Encryption:To secure the connection using SSL/TLS, you can use CherryPy's tools.https tool. You need to have an SSL certificate and private key.
```

**Database:**
- InfluxDB is used In order to store the sensor records, InfluxDB is designed to store timeseries