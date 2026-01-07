FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy all code in current folder
COPY . .

# Set working directory
WORKDIR /app

# Run entry point
CMD ["python", "main.py"]
