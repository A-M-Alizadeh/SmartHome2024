from setuptools import setup, find_packages
#This will automatically find all the packages in the project
#For this to work the packages should have a __init__.py file in them
#This file can be empty
#The __init__.py file is used to mark the directory as a package
#The __init__.py file can also be used to import specific modules from the package
#For example, in the __init__.py file of the Models package, we can import the House and Sensor modules
#This way we can import the House and Sensor modules from the Models package using the following import statement:
# from Models import House, Sensor

#You also need to run the following command in the terminal to install the package:
#pip install -e .

setup(name='SmartHoseIOT', version='1.0', packages=find_packages())
