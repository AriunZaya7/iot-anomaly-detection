from fastapi import FastAPI
from kafka import KafkaConsumer, KafkaProducer, errors
from prometheus_client import Counter, start_http_server
import threading
import time
import json
import os

# -------- CONFIG --------
KAFKA_BROKER = os.environ.get("KAFKA_BROKER", "kafka:9092")
TOPIC = "raw-sensor-data"

# -------- PROMETHEUS METRICS --------
messages_consumed_total = Counter("messages_consumed_total", "Total messages consumed from Kafka")
messages_forwarded_total = Counter("messages_forwarded_total", "Total messages forwarded successfully")
messages_invalid_total = Counter("messages_invalid_total", "Total messages that failed processing")

# -------- FASTAPI --------
app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

# -------- KAFKA CONSUMER FUNCTION --------
def consume_and_forward():
    print("[Ingestion] Starting Kafka consumer thread...")
    while True:
        try:
            consumer = KafkaConsumer(
                TOPIC,
                bootstrap_servers=KAFKA_BROKER,
                auto_offset_reset='earliest',
                group_id='ingestion-group'
            )
            print(f"[Ingestion] Connected to Kafka broker at {KAFKA_BROKER}")
            break
        except errors.NoBrokersAvailable as e:
            print(f"[Ingestion] Waiting for Kafka broker... {e}")
            time.sleep(2)

    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )

    for message in consumer:
        messages_consumed_total.inc()
        try:
            data = json.loads(message.value.decode('utf-8'))
            # Forward message (for now we just send it back to the same topic)
            producer.send(TOPIC, value=data)
            messages_forwarded_total.inc()
            print(f"[Ingestion] Consumed and forwarded message: {data}")
        except Exception as e:
            print(f"[Ingestion] Failed to process message: {e}")
            messages_invalid_total.inc()

# -------- PROMETHEUS METRICS FUNCTION --------
def start_metrics_server():
    start_http_server(8001)
    print("[Metrics] Prometheus metrics server started on port 8001")

# -------- START THREADS USING FASTAPI STARTUP EVENT --------
@app.on_event("startup")
def startup_event():
    print("[Ingestion] Starting metrics and Kafka threads...")
    threading.Thread(target=start_metrics_server, daemon=True).start()
    threading.Thread(target=consume_and_forward, daemon=True).start()

# -------- RUN UVICORN --------
if __name__ == "__main__":
    import uvicorn
    print("[Ingestion] Starting FastAPI server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
