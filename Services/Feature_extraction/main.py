"""
    entry point for feature extraction service.
"""
from pipeline import FeaturePipeline

if __name__ == "__main__":
    pipeline = FeaturePipeline()
    pipeline.run()
