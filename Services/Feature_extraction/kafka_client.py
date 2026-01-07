# kafka_client.py
import json
import time
from kafka import KafkaConsumer, KafkaProducer, errors
from metrics import features_processed_total, feature_processing_seconds, start_metrics_server
import os

KAFKA_BROKER = os.environ.get("KAFKA_BROKER", "kafka:9092")
RAW_TOPIC = "raw-sensor-data"
FEATURES_TOPIC = "extracted-features"

# Start metrics server first
start_metrics_server()

# Connect to Kafka with retry
while True:
    try:
        consumer = KafkaConsumer(
            RAW_TOPIC,
            bootstrap_servers=KAFKA_BROKER,
            auto_offset_reset='earliest',
            group_id='feature-group'
        )
        print(f"[Feature Extraction] Connected to Kafka at {KAFKA_BROKER}")
        break
    except errors.NoBrokersAvailable:
        print(f"[Feature Extraction] Kafka not ready, retrying in 2s...")
        time.sleep(2)

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

print("[Feature Extraction] Listening for raw sensor data...")

# Main loop
for msg in consumer:
    start_time = time.time()
    try:
        data = json.loads(msg.value.decode("utf-8"))
        features = data["features"]

        temp = features["temperature"]
        humidity = features["humidity"]
        vibration = features["vibration"]

        extracted = {
            "sensor_id": data["sensor_id"],
            "timestamp": data["timestamp"],
            "location": data["location"],
            "features": {
                "temperature": temp,
                "humidity": humidity,
                "vibration": vibration,
                "temp_humidity_ratio": temp / (humidity + 0.01),
                "vibration_squared": vibration ** 2
            }
        }

        # Send extracted features
        producer.send(FEATURES_TOPIC, value=extracted)

        # Increment Prometheus metrics
        features_processed_total.inc()
        feature_processing_seconds.observe(time.time() - start_time)

        print(f"[Feature Extraction] Sent features: {extracted}")

    except Exception as e:
        print(f"[Feature Extraction] Failed to process message: {e}")
