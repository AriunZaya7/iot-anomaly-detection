"""
    kafka_client module for handling kafka connectivity.
"""

import time
import json
from kafka import KafkaConsumer, KafkaProducer, errors
from config import KAFKA_BROKER, TOPIC


def create_consumer():
    """Create a Kafka consumer and wait for broker if unavailable."""
    while True:
        try:
            consumer = KafkaConsumer(
                TOPIC,
                bootstrap_servers=KAFKA_BROKER,
                auto_offset_reset="earliest",
                group_id="ingestion-group"
            )
            print(f"[Kafka] Connected consumer to broker at {KAFKA_BROKER}")
            return consumer
        except errors.NoBrokersAvailable:
            print("[Kafka] Waiting for broker...")
            time.sleep(2)


def create_producer():
    """Create a Kafka producer."""
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )
    print(f"[Kafka] Producer ready at {KAFKA_BROKER}")
    return producer
