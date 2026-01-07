# Architectural Decision Records (ADRs) for IOT-anomaly-detection

---

**ID: ADR-001**  
- **Title:** Use Apache ZooKeeper for configuration and service discovery  
- **Status:** Accepted  
- **Decision:** Use ZooKeeper as the central coordination and configuration service. It stores workflow definitions and service registration information under `/workflow/config` and `/services`.  
- **Consequence:**  
  - Provides a single source of truth for configuration.  
  - Enables dynamic service registration with ephemeral nodes.  
  - Introduces dependency on ZooKeeper availability.  
  - Requires understanding of znodes and watcher patterns.

---