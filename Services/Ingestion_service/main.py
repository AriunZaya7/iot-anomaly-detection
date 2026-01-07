"""
    entry point for ingestion service
"""
from fastapi import FastAPI
import threading
from pipeline import IngestionPipeline
from metrics import start_metrics_server
from config import API_HOST, API_PORT

app = FastAPI()
pipeline = IngestionPipeline()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.on_event("startup")
def startup_event():
    """Start metrics server and Kafka ingestion pipeline in background threads."""
    print("[Ingestion] Starting metrics and Kafka ingestion threads...")
    threading.Thread(target=start_metrics_server, daemon=True).start()
    threading.Thread(target=pipeline.run, daemon=True).start()


if __name__ == "__main__":
    import uvicorn
    print("[Ingestion] Starting FastAPI server...")
    uvicorn.run(app, host=API_HOST, port=API_PORT)
