"""
    pipeline module to orchestrate feature extraction workflow.
"""
import time
import json
from kafka_client import connect_kafka
from extractor import FeatureExtractor
from metrics import features_processed_total, feature_processing_seconds, start_metrics_server
from config import FEATURES_TOPIC


class FeaturePipeline:
    """Orchestrates Kafka consumption, feature extraction, and result emission."""

    def __init__(self):
        self.consumer, self.producer = connect_kafka()
        self.extractor = FeatureExtractor()

    def run(self):
        """Start metrics server and listen for raw sensor messages."""
        start_metrics_server()
        print("[Pipeline] Listening for raw sensor data...")

        for msg in self.consumer:
            self.process_message(msg)

    def process_message(self, msg):
        """Process a single Kafka message."""
        start_time = time.time()
        try:
            raw_data = json.loads(msg.value.decode("utf-8"))
            extracted = self.extractor.extract_features(raw_data)
            self.producer.send(FEATURES_TOPIC, value=extracted)
            features_processed_total.inc()
            print(f"[Pipeline] Sent features: {extracted}")

        except Exception as e:
            print(f"[Pipeline] Failed to process message: {e}")

        finally:
            feature_processing_seconds.observe(time.time() - start_time)
