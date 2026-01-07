"""
    pipeline module to orchestrate ingestion service workflow
"""
import json
from kafka_client import create_consumer, create_producer
from metrics import (
    messages_consumed_total,
    messages_forwarded_total,
    messages_invalid_total
)
from validator import MessageValidator
from config import TOPIC


class IngestionPipeline:
    """Consumes, validates, and forwards Kafka messages."""

    def __init__(self):
        self.consumer = create_consumer()
        self.producer = create_producer()
        self.validator = MessageValidator()

    def run(self):
        """Start consuming messages from Kafka and forward valid messages."""
        print("[Pipeline] Starting Kafka ingestion loop...")
        for message in self.consumer:
            self.process_message(message)

    def process_message(self, message):
        """Process a single Kafka message."""
        messages_consumed_total.inc()
        try:
            data = json.loads(message.value.decode("utf-8"))

            if not self.validator.is_valid_message(data):
                messages_invalid_total.inc()
                print(f"[Pipeline] Invalid message dropped: {data}")
                return

            self.producer.send(TOPIC, value=data)
            messages_forwarded_total.inc()
            print(f"[Pipeline] Valid message forwarded: {data}")

        except Exception as e:
            messages_invalid_total.inc()
            print(f"[Pipeline] Failed to process message: {e}")
