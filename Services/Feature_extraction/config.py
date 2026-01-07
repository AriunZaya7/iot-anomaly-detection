"""
    config.py contains all configuration constants for kafka and metrics ports.
"""

import os

# ---------------- Kafka ----------------
KAFKA_BROKER = os.environ.get("KAFKA_BROKER", "kafka:9092")
RAW_TOPIC = "raw-sensor-data"
FEATURES_TOPIC = "extracted-features"

# ---------------- Metrics ----------------
METRICS_PORT = 8002
