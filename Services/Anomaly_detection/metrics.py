"""
    metrics module for handling Prometheus metrics.
"""
from prometheus_client import Counter, Histogram, start_http_server
from config import METRICS_PORT

# Counters
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

# Histogram
anomaly_processing_seconds = Histogram(
    "anomaly_processing_seconds",
    "Time spent processing anomaly detection messages"
)


def start_metrics_server():
    """Start Prometheus metrics server."""
    start_http_server(METRICS_PORT)
    print(f"[Metrics] Prometheus metrics exposed on port {METRICS_PORT}")

