# Base image
FROM python:3.9-slim-buster

# Set the working directory
WORKDIR /app

# Copy the script to the container
COPY injestion.py .

# Install dependencies
RUN pip install --no-cache-dir requests python-dotenv

# Start the script
CMD ["python", "injestion.py"]
