"""
    entry point for anomaly detection service
"""
from pipeline import AnomalyPipeline

if __name__ == "__main__":
    pipeline = AnomalyPipeline()
    pipeline.run()
