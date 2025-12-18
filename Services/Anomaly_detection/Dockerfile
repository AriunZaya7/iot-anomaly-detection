FROM python:3.11-slim
WORKDIR /app
COPY anomaly_detection.py requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "anomaly_detection.py"]
