import json
import time
from kafka import KafkaConsumer, KafkaProducer, errors
import numpy as np
import os

KAFKA_BROKER = os.environ.get("KAFKA_BROKER", "kafka:9092")
RAW_TOPIC = "raw-sensor-data"
FEATURES_TOPIC = "extracted-features"


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

for msg in consumer:
    try:
        data = json.loads(msg.value.decode("utf-8"))
        features = data["features"]

        # Example feature engineering
        temp = features["temperature"]
        humidity = features["humidity"]
        vibration = features["vibration"]

        # Simple features: add moving averages or normalized values
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

        producer.send(FEATURES_TOPIC, value=extracted)
        print(f"[Feature Extraction] Sent features: {extracted}")

    except Exception as e:
        print(f"[Feature Extraction] Failed to process message: {e}")
