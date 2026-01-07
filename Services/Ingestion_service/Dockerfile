FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy all service code
COPY . .

# Expose FastAPI and metrics ports
EXPOSE 8000 8001

# Run the modular entry point
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
