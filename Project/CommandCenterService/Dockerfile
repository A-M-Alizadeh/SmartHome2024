# Use an official Python runtime as the base image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the project dependencies
RUN pip install -r requirements.txt

# Copy the project files into the container
COPY . .

# Install the project as a package
RUN pip install -e .

# Expose the port the app runs on
EXPOSE 8083 1883

CMD ["./dockerRunner.sh"]
# Set the entry point command to run the Python script
# RUN chmod +x serviceRunner.sh
# RUN ./serviceRunner.sh

