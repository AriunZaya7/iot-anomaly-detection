"""
    kafka_client module for handling kafka connectivity.
"""
import time
import json
from kafka import KafkaConsumer, KafkaProducer, errors
from config import KAFKA_BROKER, INPUT_TOPIC, OUTPUT_TOPIC


def connect_kafka():
    """
    Connects to Kafka and returns consumer and producer.

    Returns:
        tuple: (KafkaConsumer, KafkaProducer)
    """
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
            print(f"[Kafka] Connected to broker at {KAFKA_BROKER}")
            return consumer, producer
        except errors.NoBrokersAvailable:
            print("[Kafka] Waiting for broker...")
            time.sleep(2)
