# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy the requirements.txt into the container
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Set the environment variable for Flask
ENV FLASK_APP=bmi_service.py

# Copy the current directory contents into the container
COPY . /app/

COPY bmi_service.py /app/
WORKDIR /app


# Expose the port the app runs on
EXPOSE 5002

# Define the command to run the app
CMD ["python", "bmi_service.py"]
