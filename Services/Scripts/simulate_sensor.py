"""
    Goals for simulate_sensor.py
    Simulate multiple IoT sensors (temperature, humidity, vibration, etc.)
    1. Generate realistic readings over time
    2. Optionally inject anomalies (spikes, drops)
    3. Publish messages to Kafka (or MQTT)
    4. Configurable for:
    5. Number of sensors
    6. Frequency of data
    7. Anomaly probability
"""

import time
import json
import random
from kafka import KafkaProducer
import numpy as np
import math

# -------- CONFIGURATION --------
NUM_SENSORS = 5
PUBLISH_INTERVAL = 1.0  # seconds
ANOMALY_PROB = 0.05  # point anomaly probability
DRIFT_PROB = 0.01  # drift anomaly probability
KAFKA_TOPIC = "raw-sensor-data"
KAFKA_BROKER = "localhost:9092"

# Sensor metadata options
LOCATIONS = ["Room A", "Room B", "Room C", "Factory Floor", "Warehouse"]

# -------- SETUP KAFKA --------
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)


# -------- SENSOR SIMULATION --------
class Sensor:
    def __init__(self, sensor_id):
        self.sensor_id = sensor_id
        self.location = random.choice(LOCATIONS)
        self.time_counter = 0

        # Base values for each feature
        self.base_temp = random.uniform(20, 25)
        self.base_humidity = random.uniform(30, 60)
        self.base_vibration = random.uniform(0, 1)

        # Drift offsets
        self.temp_drift = 0
        self.humidity_drift = 0
        self.vibration_drift = 0

    def read_features(self):
        self.time_counter += 1

        # Simulate normal readings
        temp = self.base_temp + np.random.normal(0, 0.5) + self.temp_drift
        humidity = self.base_humidity + random.uniform(-2, 2) + self.humidity_drift
        vibration = self.base_vibration + 2 * math.sin(0.2 * self.time_counter) + self.vibration_drift

        # Inject drift anomalies occasionally
        if random.random() < DRIFT_PROB:
            self.temp_drift += random.uniform(-0.5, 0.5)
            self.humidity_drift += random.uniform(-1, 1)
            self.vibration_drift += random.uniform(-0.1, 0.1)

        # Inject point anomalies
        if random.random() < ANOMALY_PROB:
            temp += random.choice([-10, -5, 5, 10])
        if random.random() < ANOMALY_PROB:
            humidity += random.choice([-20, -10, 10, 20])
        if random.random() < ANOMALY_PROB:
            vibration += random.choice([-2, -1, 1, 2])

        return {
            "temperature": round(temp, 2),
            "humidity": round(humidity, 2),
            "vibration": round(vibration, 2)
        }


# -------- MAIN LOOP --------
sensors = [Sensor(f"sensor-{i + 1}") for i in range(NUM_SENSORS)]

print("Starting multi-feature sensor simulation... Press Ctrl+C to stop.")

try:
    while True:
        timestamp = int(time.time())
        for sensor in sensors:
            features = sensor.read_features()
            message = {
                "sensor_id": sensor.sensor_id,
                "timestamp": timestamp,
                "features": features,
                "location": sensor.location
            }

            producer.send(KAFKA_TOPIC, value=message)
            print(f"Sent: {message}")

        producer.flush()
        time.sleep(PUBLISH_INTERVAL)

except KeyboardInterrupt:
    print("Simulation stopped.")
