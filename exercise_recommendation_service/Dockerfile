FROM python:3.8-slim

WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the CSV file into the container
COPY gym_members_exercise_tracking.csv /app/gym_members_exercise_tracking.csv


# Copy all other project files into the container's /app directory
COPY . /app/

EXPOSE 5003


# Run the application
CMD ["python", "exercise_service.py"]

