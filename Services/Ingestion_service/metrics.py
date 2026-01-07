"""
    metrics module for handling Prometheus metrics.
"""
from prometheus_client import Counter, start_http_server
from config import METRICS_PORT

# Counters
messages_consumed_total = Counter(
    "messages_consumed_total", "Total messages consumed from Kafka"
)
messages_forwarded_total = Counter(
    "messages_forwarded_total", "Total messages forwarded successfully"
)
messages_invalid_total = Counter(
    "messages_invalid_total", "Total messages that failed validation"
)


def start_metrics_server():
    """Start Prometheus metrics server."""
    start_http_server(METRICS_PORT)
    print(f"[Metrics] Prometheus metrics server started on port {METRICS_PORT}")
