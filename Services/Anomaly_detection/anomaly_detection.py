import json
import os
import time
import numpy as np
from kafka import KafkaConsumer, KafkaProducer, errors
from sklearn.ensemble import IsolationForest
from prometheus_client import Counter, Histogram, start_http_server

# ---------------- CONFIG ----------------
KAFKA_BROKER = os.environ.get("KAFKA_BROKER", "kafka:9092")
INPUT_TOPIC = "extracted-features"
OUTPUT_TOPIC = "anomaly-results"

MIN_TRAINING_SAMPLES = 100   # warm-up size

# ---------------- PROMETHEUS METRICS ----------------
anomaly_messages_consumed_total = Counter(
    "anomaly_messages_consumed_total",
    "Total messages consumed by anomaly detection"
)

anomalies_emitted_total = Counter(
    "anomalies_emitted_total",
    "Total anomaly results produced"
)

anomaly_errors_total = Counter(
    "anomaly_errors_total",
    "Total errors during anomaly detection"
)

anomaly_processing_seconds = Histogram(
    "anomaly_processing_seconds",
    "Time spent processing anomaly detection messages"
)



# ---------------- MODEL ----------------
model = IsolationForest(
    n_estimators=100,
    contamination=0.05,
    random_state=42
)

feature_buffer = []
model_fitted = False

start_http_server(8003)
print("[Metrics] Anomaly detection metrics on port 8003")

# ---------------- WAIT FOR KAFKA ----------------
while True:
    try:
        consumer = KafkaConsumer(
            INPUT_TOPIC,
            bootstrap_servers=KAFKA_BROKER,
            auto_offset_reset="earliest",
            group_id="anomaly-group"
        )

        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER,
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )

        print(f"[Anomaly Detection] Connected to Kafka at {KAFKA_BROKER}")
        break

    except errors.NoBrokersAvailable:
        print("[Anomaly Detection] Waiting for Kafka broker...")
        time.sleep(2)

# ---------------- PROCESS STREAM ----------------
print("[Anomaly Detection] Listening for extracted features...")

for msg in consumer:
    start_time = time.time()
    anomaly_messages_consumed_total.inc()
    try:
        data = json.loads(msg.value.decode("utf-8"))
        features = data["features"]

        # Convert features to numeric vector
        vector = np.array([
            float(features["temperature"]),
            float(features["humidity"]),
            float(features["vibration"]),
            float(features["temp_humidity_ratio"]),
            float(features["vibration_squared"])
        ]).reshape(1, -1)

        # Collect baseline data
        feature_buffer.append(vector.flatten())

        if not model_fitted:
            if len(feature_buffer) < MIN_TRAINING_SAMPLES:
                print(f"[Anomaly Detection] Warming up ({len(feature_buffer)}/{MIN_TRAINING_SAMPLES})")
                continue

            model.fit(np.array(feature_buffer))
            model_fitted = True
            print("[Anomaly Detection] Model trained successfully")

        # Predict anomaly
        prediction = int(model.predict(vector)[0])  # -1 or 1

        result = {
            "sensor_id": str(data["sensor_id"]),
            "timestamp": int(data["timestamp"]),
            "location": str(data["location"]),
            "features": {k: float(v) for k, v in features.items()},
            "anomaly": prediction
        }

        producer.send(OUTPUT_TOPIC, value=result)
        anomalies_emitted_total.inc()
        print(f"[Anomaly Detection] Sent result: {result}")

    except Exception as e:
        print(f"[Anomaly Detection] Failed to process message: {e}")

    finally:
        anomaly_processing_seconds.observe(time.time() - start_time)
