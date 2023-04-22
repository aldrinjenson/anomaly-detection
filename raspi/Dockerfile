# Base image
FROM python:3.9-slim-buster

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y libglib2.0-0 libsm6 libxext6 libxrender-dev

# Copy the script to the container
COPY injestion.py .

# Install dependencies
RUN pip install -r requirements.txt

# Start the script
CMD ["python", "injestion.py"]
