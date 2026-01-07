"""
    entry point for anomaly detection service
"""
"""
entry point for anomaly detection service
"""
import signal
import sys
from codecarbon import EmissionsTracker

from config import CARBON_PROJECT_NAME, CARBON_MEASURE_POWER_SECS
from metrics import carbon_emissions_kg
from pipeline import AnomalyPipeline

tracker = EmissionsTracker(
    project_name=CARBON_PROJECT_NAME,
    measure_power_secs=CARBON_MEASURE_POWER_SECS,
    log_level="error"
)

def shutdown_handler(sig, frame):
    total_co2 = tracker.stop()
    carbon_emissions_kg.set(total_co2)
    print(f"[Carbon] Total CO₂e: {total_co2:.8f} kg")
    sys.exit(0)

signal.signal(signal.SIGTERM, shutdown_handler)
signal.signal(signal.SIGINT, shutdown_handler)

if __name__ == "__main__":
    pipeline = AnomalyPipeline()
    pipeline.run()
