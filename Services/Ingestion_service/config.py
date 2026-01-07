"""
    config.py contains all configuration constants for kafka, metric ports and api constants.
"""
import os

# ---------------- Kafka ----------------
KAFKA_BROKER = os.environ.get("KAFKA_BROKER", "kafka:9092")
TOPIC = "raw-sensor-data"
REQUIRED_FEATURES = ["temperature", "humidity", "vibration"]

# ---------------- Metrics ----------------
METRICS_PORT = 8001

# ---------------- API ----------------
API_HOST = "0.0.0.0"
API_PORT = 8000
