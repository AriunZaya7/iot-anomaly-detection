# Architectural Decision Records (ADRs) for IOT-anomaly-detection

---

**ID: ADR-001**  
- **Title:** Use Kafka as message transfer between services. 
- **Status:** Accepted  
- **Decision:** Adopt **Apache Kafka** as the primary event streaming platform for transferring messages between all 
services in the IoT anomaly detection system, including anomaly_detection, feature_extraction, infrastructure, and ingestion_service. 
Kafka is used as the **central asynchronous communication layer**, with services publishing and consuming events via 
well-defined topics. 
- **Alternatives considered:**
  - MQTT Broker such as Mosquitto
  - HTTP REST
  - Cloud-native such as AWS
  - Kafka
- **Trade-offs:**
  - **MQTT**
    - Pros: Lightweight, simple pub/sub semantics.
    - Cons: Might be limited in message replay and not designed for backend stream analytics. 
  - **HTTP REST**
    - Pros: Simple and widely used, maybe easy debugging. 
    - Cons: No built-in buffering or replay, maybe not good fit for streaming workloads. 
  - **Cloud-native**
    - Pros: reduces overhead, and managed scalability
    - Cons: Dependent on vendor
  - **Kafka**
    - Pros: High throughput and low latency, durable message storage and replayability, enables event-driven microservices, 
supports stream processing. 
    - Cons: Operational complexity, requires topic management. 
- **Consequence:**  
  - Services are decoupled and scalable. 
  - Supports real-time batch processing simultaneously. 
  - Enables easier debugging, model retraining and backtesting anomaly detectors. 
- **Reasoning:**
An IoT anomaly detection system is inherently **event-driven** and **stream-oriented**.  
Kafka provides the necessary guarantees (durability, ordering, replayability) to support:

- Real-time anomaly detection
- Historical reprocessing
- Model evolution over time
- Fault-tolerant service communication

Kafka is therefore chosen as the **central nervous system** of the architecture, enabling scalable and resilient
inter-service communication.


--- 

**ID: ADR-002**  
- **Title:** Use Prometheus for system and service monitoring  
- **Status:** Accepted  
- **Decision:** Adopt Prometheus as the primary monitoring and metrics collection system for all services in the IoT 
anomaly detection platform. Services will expose metrics endpoints scraped by Prometheus for alerting and observability.  
- **Alternatives considered:**  
  1. InfluxDB + Telegraf for metrics collection  
  2. Cloud-native monitoring solutions (e.g., AWS CloudWatch, GCP Monitoring)  
  3. Custom logging and ad-hoc metrics collection  
- **Trade-offs:**  
  - **Prometheus:** Lightweight, open-source, widely adopted, strong ecosystem, pull-based scraping model. Requires 
infrastructure management and careful retention configuration.  
  - **InfluxDB:** Full-featured; higher operational complexity and need for agents.  
  - **Cloud-native:** Vendor lock-in and less control.  
  - **Custom logging:** Minimal dependencies; poor querying and alerting capabilities.  
- **Consequence:**  
  - Services must expose Prometheus-compatible metrics endpoints.  
  - Enables reliable alerting and time-series analysis of system health and IoT telemetry.  
- **Reasoning:**  
Prometheus provides standardized, extensible monitoring that aligns with the event-driven microservices architecture. 
It ensures early detection of bottlenecks, service failures, and anomalies in the telemetry pipeline.

---

**ID: ADR-003**  
- **Title:** Use Grafana for metrics visualization and dashboards  
- **Status:** Accepted  
- **Decision:** Adopt Grafana as the primary dashboarding and visualization tool, connecting primarily to Prometheus to 
visualize service and metrics across the IoT anomaly detection platform.  
- **Alternatives considered:**  
  1. Kibana (for log-based dashboards)  
  2. Cloud-native dashboards (AWS CloudWatch, GCP Stackdriver)  
  3. Custom dashboard solutions using libraries like Plotly or D3  
- **Trade-offs:**  
  - **Grafana:** Easy integration with Prometheus, rich visualizations, supports alerting and annotations; requires 
separate server infrastructure and manual dashboard setup.  
  - **Kibana:** Excellent for log analytics, but weaker for time-series metrics.  
  - **Cloud-native dashboards:** Managed; less flexible, vendor lock-in.  
  - **Custom dashboards:** Fully tailored; high development and maintenance effort.  
- **Consequence:**  
  - Requires Grafana infrastructure and access control.  
  - Provides unified visualization of system metrics and telemetry trends.  
  - Enables correlation between system health and detected anomalies.  
- **Reasoning:**  
Grafana, combined with Prometheus, provides a complete observability stack. It allows operators and developers to 
monitor, debug, and correlate system-level and telemetry anomalies efficiently.

--- 

**ID: ADR-004**  
- **Title:** Use a synthetic sensor simulator for IoT anomaly data generation.
- **Status:** Accepted  
- **Decision:** Implement a software-based sensor simulator to generate synthetic multi-feature IoT telemetry instead of
relying on real hardware during early development.  
- **Alternatives considered:**
  - Real IOT sensors
  - Public available datasets
  - Synthetic sensor simulator
- **Trade-offs:**
  - Real sensors not available
  - Public datasets easy to use but cannot simulate streaming behaviour. 
  - Synthetic sensor simulator easier iteration and controllable anomaly injection. But may not capture real-world noise.
- **Consequence:**  
  - Enables rapid testing of ingestion, preprocessing, and anomaly detection pipelines.
  - Requires later validation against real sensor data.  
- **Reasoning:**
  - Anomaly detection systems must be tested under controlled abnormal conditions. This is difficult to do and unsafe 
to reproduce with real devices. A simulator supports architectural validation before hardware integration. 

---

**ID: ADR-005**  
- **Title:** Simulate multiple feature sensors per device
- **Status:** Accepted  
- **Decision:** Each simulated sensor emits multiple correlated features rather than a single mteric. 
- **Alternatives considered:**
  - Single feature sensors
  - Multi-feauture sensors
- **Trade-offs:**
  - **Single feature sensors**
    - Pros: Simplicity
    - Cons: Unrealistc for IoT use cases.
  - **Multi-feature sensors**
    - Pros: Enable multivariate anomaly detection and correlation-based failures.
    - Cons: Increased preprocessing and model complexity. 
- **Consequence:**  
  - Supports multivariate anomaly detection models. 
  - Requires handling features, missing values, null values. 
- **Reasoning:**
  - Many real-world anomalies occur when there are complex relationships between metrics. Not just from a single value crossing a threshold. 

---

**ID: ADR-006**  
- **Title:** Use probabilistic anomaly injection
- **Status:** Accepted  
- **Decision:** Control anomlay injection using probabilities rather than deterministic schedules. 
- **Alternatives considered:**
  - Fixed time based anomaly injection
  - Probabilistic anomaly injection
- **Trade-offs:**
  - **Deterministic**
    - Pros: Reproducible.
    - Cons: Unrealistic temporal patterns. 
  - **Probabilistic**
    - Pros: Realistic. 
    - Cons: Less deterministic and maybe hard to test.  
- **Consequence:**  
  - Better approximates real-world unpredictability. 
  - Requires more control to be able to be reproducible.
- **Reasoning:**
  - Anomaly detection must operate under uncertainty.  

---

**ID: ADR-007**  
- **Title:** Explicitly simulate missing and null sensor data. 
- **Status:** Accepted  
- **Decision:** Simulate missing features and null values as a part of normal sensor behaviour. 
- **Alternatives considered:**
  - Assume complete perfect data. 
  - Simulate missing and null values. 
- **Trade-offs:**
  - **Assume perfect data**
    - Pros: Simplicity
    - Cons: Unrealistc and fragile
  - **Simulated data loss**
    - Pros: Improves robustness and fault tolerance testing.
    - Cons: Adds more preprocessing complexity. 
- **Consequence:**  
  - Forces downstream validation and preprocessing logic to be able to handle missing data.
  - Improve resilience of anomaly detection pipeline. 
- **Reasoning:**
  - In real life data is not perfect, especially sensor data. There could be network issues and faulty sensors that 
cause partial payloads in real IoT systems. 

---

**ID: ADR-008**  
- **Title:** Stream-based anomaly detection with Isolation Forest  
- **Status:** Accepted  
- **Decision:** Implement anomaly detection as a **streaming service** that consumes feature messages from Kafka, 
maintains a warm-up buffer, and predicts anomalies using Isolation Forest.  
- **Alternatives considered:**  
  1. Batch processing of features  
  2. Streaming detection with Isolation Forest  
  3. Streaming detection with neural network or deep learning model  
- **Trade-offs:**  
  - **Batch:** Simple, but high latency; unsuitable for real-time alerts.  
  - **Streaming + Isolation Forest:** Low-latency detection; interpretable and lightweight; may not capture complex 
  temporal patterns.  
  - **Streaming + deep learning:** Potentially more accurate for complex patterns; higher compute cost and latency.  
- **Consequence:**  
  - Continuous anomaly scoring in near real-time.  
  - Initial warm-up phase to train the model before predictions.  
  - Requires careful memory management for the feature buffer.  
- **Reasoning:**  
  Isolation Forest is lightweight, unsupervised, and interpretable, making it a good trade-off between accuracy and 
operational simplicity for IoT multivariate anomaly detection streams.

---
**ID: ADR-009**  
- **Title:** Implement warm-up phase for model training  
- **Status:** Accepted  
- **Decision:** Maintain a buffer of `MIN_TRAINING_SAMPLES` before fitting the Isolation Forest model to ensure a sufficient baseline for anomaly detection.  
- **Alternatives considered:**  
  1. Fit model immediately on first messages  
  2. Buffer messages until minimum training size achieved  
- **Trade-offs:**  
  - **Immediate fit:** Low latency, but unreliable predictions due to insufficient data.  
  - **Warm-up buffer:** Reliable initial model; introduces initial delay before predictions.  
- **Consequence:**  
  - Early messages are not scored until sufficient baseline data is collected.  
  - Predictable initial model behavior.  
- **Reasoning:**  
  Isolation Forest requires a representative dataset to compute anomaly thresholds. Warm-up ensures meaningful predictions and avoids false positives during system startup.

---

**ID: ADR-010**  
- **Title:** Stream-based data ingestion service  
- **Status:** Accepted  
- **Decision:** Implement data ingestion as a **streaming service** that consumes raw sensor telemetry from Kafka, 
validates messages, and forwards valid messages downstream for preprocessing or anomaly detection.  
- **Alternatives considered:**  
  1. Batch ingestion of sensor data  
  2. Stream ingestion using Kafka consumer  
  3. HTTP-based ingestion (sensors POST directly)  
- **Trade-offs:**  
  - **Batch:** Simpler, but higher latency; unsuitable for real-time monitoring.  
  - **Streaming with Kafka:** Low-latency, replayable, scalable; requires Kafka infrastructure.  
  - **HTTP ingestion:** Simple; tightly coupled with producers, no replay or durability guarantees.  
- **Consequence:**  
  - Near real-time forwarding of valid sensor data.  
  - Invalid or incomplete messages are dropped and counted in metrics.  
  - Requires operational monitoring to ensure Kafka availability.  
- **Reasoning:**  
  Streaming ingestion aligns with the event-driven IoT architecture. Kafka ensures durability, replayability, and decouples producers from downstream services.

---

**ID: ADR-011**  
- **Title:** Stream-based feature extraction service  
- **Status:** Accepted  
- **Decision:** Implement feature extraction as a **streaming service** consuming raw sensor data from Kafka, 
performing feature engineering, and publishing enriched feature messages to a downstream Kafka topic (`extracted-features`).  
- **Alternatives considered:**  
  1. Batch feature extraction  
  2. Streaming extraction with Kafka  
  3. Direct extraction in producers before publishing  
- **Trade-offs:**  
  - **Batch:** Simpler; higher latency; not suitable for real-time anomaly detection.  
  - **Streaming:** Near real-time processing; more complex; requires Kafka infrastructure.  
  - **Producer-side extraction:** Offloads work from service; tight coupling; harder to maintain consistent logic.  
- **Consequence:**  
  - Supports downstream services like anomaly detection and dashboards with enriched features.  
  - Allows consistent feature engineering applied centrally.  
- **Reasoning:**  
  Centralized streaming feature extraction provides **low-latency, standardized inputs** for all downstream analytics and anomaly detection, avoiding inconsistencies from distributed preprocessing.


---

**ID: ADR-012**  
- **Title:** Apply simple derived features during extraction  
- **Status:** Accepted  
- **Decision:** Compute additional features from raw sensor data, including:  
  - `temp_humidity_ratio = temperature / (humidity + 0.01)`  
  - `vibration_squared = vibration ** 2`  
- **Alternatives considered:**  
  1. Use only raw features  
  2. Compute derived features (ratios, squares, moving averages)  
  3. Use complex feature transformations (e.g., PCA, FFT)  
- **Trade-offs:**  
  - **Raw features only:** Simple; may miss patterns or correlations.  
  - **Derived features:** Lightweight; captures simple nonlinear relationships.  
  - **Complex transformations:** More information; higher computation cost; harder to maintain.  
- **Consequence:**  
  - Downstream anomaly detection receives richer, more informative inputs.  
  - Feature consistency is centralized and reproducible.  
- **Reasoning:**  
  Adding lightweight derived features improves anomaly detection accuracy while keeping computational overhead low 
for real-time streams.
