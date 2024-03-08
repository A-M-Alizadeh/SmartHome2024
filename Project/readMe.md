# Smart House (IoT)

To properly set up the project and enable smooth importing of modules, follow these steps:

1. **Navigate to the Project Folder:**
```
cd /your/path/to/project
```
2. **Install the Project as an Editable Package:**
```
pip install -e .
pip install requests
```

This command installs the project as an editable package, allowing you to import modules seamlessly from any script within the project.


3. **Run Your Scripts:**
- If your scripts are at the same level as the `project` folder:
  ```
  python script_name.py
  ```

<span style="color:red;">- No matter where the modules are, as long as you add __init__.py file inside the directory you can call it wherever you need.</span>
<font color="red">This line is red.</font>

Now, you can import your modules using clean and relative imports throughout your project.
