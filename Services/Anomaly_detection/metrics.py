"""
    metrics module for handling Prometheus metrics.
"""
from prometheus_client import Counter, Histogram, start_http_server, Gauge
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

# ---------------- Carbon Metrics ----------------
carbon_emissions_kg = Gauge(
    "anomaly_detection_co2e_kg",
    "Total estimated CO2e emissions (kg)"
)

carbon_per_message_kg = Gauge(
    "anomaly_detection_co2e_per_message_kg",
    "Average CO2e per processed message (kg)"
)


def start_metrics_server():
    """Start Prometheus metrics server."""
    start_http_server(METRICS_PORT)
    print(f"[Metrics] Prometheus metrics exposed on port {METRICS_PORT}")

