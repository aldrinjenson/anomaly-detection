# Base image
FROM python:3.9-slim-buster

# Set the working directory
WORKDIR /app

# Copy the script to the container

COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Start the script
CMD ["python", "injestion.py"]
