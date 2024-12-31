# This Dockerfile defines the environment for the application.
# It sets up a Python environment, installs dependencies, and runs the application inside a Docker container.

# Use the Python 3.8 slim image to build the container
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container's working directory
COPY . /app

# Install dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 to allow communication with the container
EXPOSE 5000

# The command to run the application when the container starts
CMD ["python", "app/time_tracker.py"]
