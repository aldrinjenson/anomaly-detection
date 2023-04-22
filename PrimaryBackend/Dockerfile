# Base image
FROM python:3.9-slim-buster

# Set the working directory
WORKDIR /app

# Copy the app files to the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that the app will run on
EXPOSE 5000

# Start the app
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]
