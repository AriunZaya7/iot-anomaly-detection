# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy simulator code
COPY simulate_sensor.py .

# Install dependencies
RUN pip install --no-cache-dir kafka-python numpy

# Default command
CMD ["python", "simulate_sensor.py"]
