"""
    config.py contains all configuration constants for kafka, for the anomaly detection ml model, and metrics ports.
"""
import os
# ---------------- Kafka ----------------
KAFKA_BROKER = os.environ.get("KAFKA_BROKER", "kafka:9092")
INPUT_TOPIC = "extracted-features"
OUTPUT_TOPIC = "anomaly-results"

# ---------------- Model ----------------
MIN_TRAINING_SAMPLES = 100
ISOLATION_FOREST_PARAMS = {
    "n_estimators": 100,
    "contamination": 0.05,
    "random_state": 42
}

# ---------------- Metrics ----------------
METRICS_PORT = 8003
