"""
    metrics module for handling Prometheus metrics.
"""

from prometheus_client import Counter, Histogram, start_http_server
from config import METRICS_PORT

# Counters
features_processed_total = Counter(
    "features_processed_total",
    "Total feature messages processed"
)

# Histogram
feature_processing_seconds = Histogram(
    "feature_processing_seconds",
    "Time spent processing feature extraction"
)


def start_metrics_server():
    """Start Prometheus metrics server."""
    start_http_server(METRICS_PORT)
    print(f"[Metrics] Prometheus metrics exposed on port {METRICS_PORT}")
