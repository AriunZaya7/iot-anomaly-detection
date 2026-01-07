"""
    pipeline module to orchestrate the anomaly detection workflow.
"""
import time
import json
from kafka_client import connect_kafka
from model import AnomalyDetector
from metrics import (
    start_metrics_server,
    anomaly_messages_consumed_total,
    anomalies_emitted_total,
    anomaly_errors_total,
    anomaly_processing_seconds
)


class AnomalyPipeline:
    """Orchestrates message consumption, anomaly detection, and result emission."""

    def __init__(self):
        self.consumer, self.producer = connect_kafka()
        self.detector = AnomalyDetector()

    def run(self):
        """Start the pipeline: metrics + Kafka consumption + anomaly detection."""
        start_metrics_server()
        print("[Pipeline] Listening for messages...")
        for msg in self.consumer:
            self.process_message(msg)

    def process_message(self, msg):
        """Process a single Kafka message."""
        start_time = time.time()
        anomaly_messages_consumed_total.inc()

        try:
            data = json.loads(msg.value.decode("utf-8"))
            vector = self.detector.add_features(data["features"])

            self.detector.fit_if_ready()
            if not self.detector.model_fitted:
                print(f"[Pipeline] Warming up ({len(self.detector.feature_buffer)}/100)")
                return

            prediction = self.detector.predict(vector)
            result = {
                "sensor_id": str(data["sensor_id"]),
                "timestamp": int(data["timestamp"]),
                "location": str(data["location"]),
                "features": {k: float(v) for k, v in data["features"].items()},
                "anomaly": prediction
            }

            self.producer.send("anomaly-results", value=result)
            anomalies_emitted_total.inc()
            print(f"[Pipeline] Sent result: {result}")

        except Exception as e:
            anomaly_errors_total.inc()
            print(f"[Pipeline] Failed to process message: {e}")

        finally:
            anomaly_processing_seconds.observe(time.time() - start_time)
