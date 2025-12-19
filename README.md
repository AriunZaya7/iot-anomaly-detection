# AI-Architecture-and-Cloud-Computing
http://localhost:8000/health
http://localhost:9090/query
http://localhost:3000/login admin/admin

# Project Definition: 
## IOT-Anomaly-Detection-Platform:
This project implements a cloud-native, microservice-based IoT data processing pipeline that simulates sensor data,
ingests it using Apache Kafka, performs feature extraction, and detects anomalies using machine learning. 
The system is observable using Prometheus and Grafana and is deployable via Docker Compose or Kubernetes.

## Architecture Overview: 
System consists of microservices that communicate using Kafka topics. 
**Microservices:**
- Simulate Sensor
- Ingestion Service
- Feature Extraction
- Anomaly Detection
- Infrastructure:
  - Kafka
  - Kubernetes
  - Monitoring: 
    - prometheus
    - grafana

## Use cases: 
| Use Case ID | Name                          | Description                                                                                                                                                                                      |
| ----------- |-------------------------------| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| UC1         | Simulate Sensor               | Simulated IoT sensors generate realistic environmental data (e.g., temperature, humidity, vibration) at configurable intervals and publish the readings as structured messages to a Kafka topic. |
| UC2         | Data Ingestion and Validation | The ingestion service consumes raw sensor data from Kafka, validates message structure and format, tracks ingestion metrics, and forwards valid messages for downstream processing.              |
| UC3         | Feature Extraction            | The feature extraction service transforms raw sensor readings into engineered features such as ratios and squared values, and publishes the enriched data to a dedicated Kafka topic.            |
| UC4         | Anomaly Detection             | The anomaly detection service applies a machine learning model to extracted features to classify sensor behavior as normal or anomalous, and publishes labeled results for further consumption.  |
| UC5         | Monitoring and Observability  | The system exposes operational and sustainability metrics, which are collected by Prometheus and visualized in Grafana dashboards to monitor performance, anomalies, and system health.          |


## Application scaffolding: 
- simulator/: Sensor data generation
- ingestion-service/: Kafka consumer + FastAPI
- feature-extraction/: Feature engineering pipeline
- anomaly-detection/: ML-based anomaly detection (Isolation Forest)
- monitoring/: Prometheus , Grafana
- k8s/: Kubernetes deployment manifests??



