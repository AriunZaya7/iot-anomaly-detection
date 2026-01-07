FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy all service code
COPY . .

# Expose metrics port
EXPOSE 8003

# Run the modular entry point
CMD ["python", "main.py"]
