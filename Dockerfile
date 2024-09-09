# Use an official Python runtime as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files into the container
COPY . .

VOLUME /department_store_new.sqlite
# Expose the port the app runs on
EXPOSE 8080 8501

# Run the Flask app
CMD ["python", "main.py"]
