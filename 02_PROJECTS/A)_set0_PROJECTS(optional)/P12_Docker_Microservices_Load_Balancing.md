# Project 12: Docker Microservices with Load Balancing

> **Course:** Computer Networks  
> **Programme:** Economic Informatics, Year 3, Semester 2  
> **Institution:** ASE Bucharest - CSIE  
> **Project type:** Main

> 📍 **Navigation:** [00PROJ](../README.md) → [PROJECTS](./README.md) → P12
> 
> **Related:** [P08 (Web Server)](P08_Web_Server_Reverse_Proxy.md) | [P10 (Docker Network)](P10_Docker_Network_Configuration.md)

---

## 📋 Assessment and Delivery Guide

### ⚠️ IMPORTANT: Assessment with Physical Attendance

**Common guides:** [Pair Programming](../docs/common/pair_programming_guide.md) | [Code Quality](../docs/common/code_quality_standards.md) | [Git Workflow](../docs/common/git_workflow_detailed.md) | [Troubleshooting](../docs/common/troubleshooting_common.md)

---

### 📅 Stage Calendar

| Stage | Week | Deadline | Deliverables | Score |
|-------|------|----------|--------------|-------|
| **E1** - Design | Week 5 | Week 5 (2026) | Specifications + Diagrams + Plan | 20% |
| **E2** - Prototype | Week 9 | Week 9 (2026) | Partial functional implementation | 25% |
| **E3** - Final | Week 13 | Week 13 (2026) | Complete version + Documentation | 35% |
| **E4** - Presentation | Week 14 | Week 14 (2026) | Live demo + Oral defence | 20% |

**Repository:** `https://github.com/[username]/retele-proiect-12`

---

### 📊 Assessment Rubric

#### Stage 1 — Design (100 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Complete specifications | 30 | Services, load balancing strategy, health checks |
| Architecture diagrams | 20 | Container topology, network flow |
| Implementation plan | 15 | Realistic timeline |
| Repository initialised | 15 | GitHub configured |
| MANIFEST.txt correct | 10 | Valid signature |
| Archive naming | 10 | Follows convention |

#### Stage 2 — Prototype (100 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Basic load balancer works | 35 | Round-robin distribution |
| Code quality | 25 | Clean, typed, documented |
| Docker Compose functional | 15 | Services start correctly |
| Progress report | 10 | Documents progress |
| MANIFEST.txt | 10 | Valid signature |
| On-time delivery | 5 | Meets deadline |

#### Stage 3 — Final Version (100 points + 10 bonus)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Complete implementation | 40 | LB + health checks + failover |
| Final code quality | 20 | Production-ready |
| Tests | 15 | Load testing + failover tests |
| Documentation | 10 | Complete docs |
| Performance analysis | 5 | Requests/sec, latency |
| MANIFEST.txt | 10 | Valid signature |
| **Bonus: Auto-scaling** | +10 | Dynamic container scaling (teams of 3) |

#### Stage 4 — Presentation (100 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Live demo functional | 35 | Load balancing visible |
| Technical presentation | 25 | Explains LB algorithms |
| Answers to questions | 20 | Demonstrates understanding |
| Team contribution | 15 | All members know code |
| Time management | 5 | 10-15 minutes |

---

### 👥 Team Size

| Team | Requirements |
|------|--------------|
| **1 person** | Round-robin LB + 3 backend containers |
| **2 persons** | + Health checks + weighted distribution |
| **3 persons** | + Auto-scaling + least connections algorithm |

---

## 📚 Project Description

Build a containerised microservices architecture with a custom load balancer that distributes traffic across multiple backend instances. Using Docker and Docker Compose, you'll implement health checking, automatic failover and demonstrate load distribution. This mirrors production deployment patterns used by major tech companies.

### 🎯 Learning Objectives

- **LO1:** Implement load balancing algorithms (round-robin, weighted, least-connections)
- **LO2:** Design health check mechanisms for backend services
- **LO3:** Configure Docker networks for service communication
- **LO4:** Handle backend failures with automatic failover
- **LO5:** Measure and analyse load distribution effectiveness
- **LO6:** Implement service discovery patterns

### 🛠️ Technologies and Tools

| Technology | Purpose | Documentation |
|------------|---------|---------------|
| **Docker** | Containerisation | [docs.docker.com](https://docs.docker.com) |
| **Docker Compose** | Multi-container orchestration | [docs.docker.com/compose](https://docs.docker.com/compose) |
| **Python Flask** | Backend services | [flask.palletsprojects.com](https://flask.palletsprojects.com) |
| **nginx** | Reference load balancer | [nginx.org](https://nginx.org) |
| **wrk/ab** | Load testing | [github.com/wg/wrk](https://github.com/wg/wrk) |

### 📖 Key Concepts

| Concept | Description |
|---------|-------------|
| **Load Balancer** | Distributes requests across multiple backends |
| **Round-Robin** | Rotate through backends sequentially |
| **Weighted** | Distribute based on capacity weights |
| **Least Connections** | Send to backend with fewest active connections |
| **Health Check** | Periodic verification of backend availability |
| **Failover** | Automatic routing away from failed backends |
| **Service Discovery** | Finding available service instances |
| **Horizontal Scaling** | Adding more instances (not bigger machines) |

---

## ⛔ Constraints (MUST/MUST NOT)

### MUST (Mandatory)
- [ ] MUST implement custom load balancer (not use nginx/HAProxy directly)
- [ ] MUST support at least 3 backend instances
- [ ] MUST implement health checks with configurable interval
- [ ] MUST handle backend failures gracefully
- [ ] MUST log all routing decisions
- [ ] MUST pass all smoke tests

### MUST NOT (Forbidden)
- [ ] MUST NOT use external load balancer services
- [ ] MUST NOT hardcode backend addresses (use discovery)
- [ ] MUST NOT crash when all backends fail (return error)
- [ ] MUST NOT ignore health check failures

### SHOULD (Recommended)
- [ ] SHOULD implement multiple LB algorithms
- [ ] SHOULD provide real-time statistics
- [ ] SHOULD support graceful shutdown

---

## 🎯 Concept Analogies

### Load Balancer = Supermarket Cashiers

🏠 **Real-World Analogy:**  
At a supermarket, multiple cashiers serve customers. A manager (load balancer) directs customers to available registers. If one cashier is busy or goes on break (fails), customers are directed elsewhere.

🖼️ **Visual Representation:**
```
Customers          MANAGER         Cashiers
    │                │               │
    ├──────►         │               │
    ├──────►    ┌────┴────┐         │
    ├──────►    │ Assign  │ ──────► Register 1 ✓
    ├──────►    │ Register│ ──────► Register 2 ✓
    └──────►    └────┬────┘ ──────► Register 3 ✗ (closed)
                     │
              (Tracks who's free)
```

💻 **Technical Mapping:**
- Customers = HTTP requests
- Manager = Load balancer
- Cashiers = Backend containers
- "On break" = Health check failure
- Register assignment = Routing decision

⚠️ **Where the analogy breaks:** Real cashiers have variable speed; in round-robin LB, all backends are assumed equal.

---

### Health Check = Roll Call

🏠 **Real-World Analogy:**  
A teacher takes attendance every class. Students who don't respond are marked absent and don't receive assignments. Similarly, backends that don't respond to health checks are removed from rotation.

💻 **Technical Mapping:**
- Roll call = Health check request (GET /health)
- "Present" = 200 OK response
- "Absent" = Timeout or error
- Marked absent = Removed from pool

---

## 🗳️ Peer Instruction Questions

### Question 1: Round-Robin Limitation

> 💭 **PREDICTION:** When does round-robin perform poorly?

**Options:**
- A) When backends have equal capacity
- B) When backends have different capacities ✓
- C) When there are many backends
- D) When traffic is bursty

**Correct answer:** B

**Explanation:** Round-robin sends equal traffic to each backend. If one backend is slower (less RAM, CPU), it becomes overloaded while faster backends are underutilised. Weighted round-robin solves this.

---

### Question 2: Health Check Interval

> 💭 **PREDICTION:** What's the downside of very frequent health checks?

**Options:**
- A) More accurate failure detection
- B) Increased network/CPU overhead ✓
- C) Faster failover
- D) Better load distribution

**Correct answer:** B

**Explanation:** Frequent health checks consume bandwidth and CPU on both load balancer and backends. Balance between detection speed and overhead — typically 5-30 seconds is reasonable.

---

### Question 3: Sticky Sessions

> 💭 **PREDICTION:** Why might you want requests from one user to always go to the same backend?

**Options:**
- A) For better load distribution
- B) To maintain session state (shopping cart) ✓
- C) For faster response times
- D) For security

**Correct answer:** B

**Explanation:** If session data is stored locally on a backend (not in shared cache), switching backends loses the session. Sticky sessions (session affinity) ensure continuity but reduce load distribution flexibility.

---

### Question 4: Connection Draining

> 💭 **PREDICTION:** What should happen when removing a backend for maintenance?

**Options:**
- A) Immediately stop all connections
- B) Let existing connections finish, reject new ones ✓
- C) Migrate connections to other backends
- D) Keep accepting traffic until restart

**Correct answer:** B

**Explanation:** Connection draining (graceful shutdown) stops new requests but lets in-flight requests complete. This prevents errors during deployments.

---

## ❌ Common Misconceptions

### 🚫 "More backends = faster responses"

**WRONG:** Adding backends always improves performance.

**CORRECT:** Each backend adds coordination overhead. If backends are underutilised, adding more won't help. Also, the load balancer itself can become a bottleneck.

---

### 🚫 "Load balancer eliminates single point of failure"

**WRONG:** Having a load balancer means high availability.

**CORRECT:** The load balancer itself becomes a single point of failure! Production systems use redundant load balancers with failover.

---

### 🚫 "Health checks guarantee availability"

**WRONG:** If health checks pass, the service works.

**CORRECT:** Health checks verify basic connectivity, not full functionality. A backend might respond to /health but fail on actual requests (e.g., database connection lost).

---

## 📖 Glossary

| Term | Definition |
|------|------------|
| **Load Balancer** | Server that distributes traffic across backends |
| **Backend** | Server that handles actual requests |
| **Round-Robin** | Rotate through backends in order |
| **Weighted** | Distribute proportionally to capacity |
| **Least Connections** | Prefer backend with fewest active connections |
| **Health Check** | Periodic test of backend availability |
| **Failover** | Automatic switch to backup when primary fails |
| **Connection Draining** | Graceful removal allowing in-flight completion |
| **Sticky Sessions** | Route same client to same backend |
| **Horizontal Scaling** | Adding more instances |

---

## 🔨 Implementation Example

```python
#!/usr/bin/env python3
"""Custom Load Balancer with Health Checks"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
from flask import Flask, request, Response
import requests
import threading
import time
from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum
import logging

# ═══════════════════════════════════════════════════════════════════════════════
# TYPES
# ═══════════════════════════════════════════════════════════════════════════════
class BackendStatus(Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"

@dataclass
class Backend:
    """Backend server definition."""
    host: str
    port: int
    weight: int = 1
    status: BackendStatus = BackendStatus.UNKNOWN
    active_connections: int = 0
    
    @property
    def url(self) -> str:
        return f"http://{self.host}:{self.port}"

# ═══════════════════════════════════════════════════════════════════════════════
# LOAD_BALANCER
# ═══════════════════════════════════════════════════════════════════════════════
class LoadBalancer:
    """
    Custom load balancer with multiple algorithms.
    
    # 💭 PREDICTION: Why track active_connections?
    # Answer: For least-connections algorithm
    """
    
    def __init__(self, backends: List[Backend], algorithm: str = "round_robin"):
        self.backends = backends
        self.algorithm = algorithm
        self.current_index = 0
        self.lock = threading.Lock()
        self.logger = logging.getLogger(__name__)
        
        # Start health checker
        self._start_health_checker()
    
    def get_backend(self) -> Optional[Backend]:
        """Select a backend based on algorithm."""
        healthy = [b for b in self.backends if b.status == BackendStatus.HEALTHY]
        
        if not healthy:
            self.logger.error("No healthy backends available!")
            return None
        
        if self.algorithm == "round_robin":
            return self._round_robin(healthy)
        elif self.algorithm == "least_connections":
            return self._least_connections(healthy)
        elif self.algorithm == "weighted":
            return self._weighted(healthy)
        
        return healthy[0]
    
    def _round_robin(self, backends: List[Backend]) -> Backend:
        """Round-robin selection."""
        with self.lock:
            backend = backends[self.current_index % len(backends)]
            self.current_index += 1
        return backend
    
    def _least_connections(self, backends: List[Backend]) -> Backend:
        """Select backend with fewest active connections."""
        return min(backends, key=lambda b: b.active_connections)
    
    def _weighted(self, backends: List[Backend]) -> Backend:
        """Weighted random selection."""
        import random
        total_weight = sum(b.weight for b in backends)
        r = random.uniform(0, total_weight)
        
        cumulative = 0
        for backend in backends:
            cumulative += backend.weight
            if r <= cumulative:
                return backend
        
        return backends[-1]
    
    def _start_health_checker(self, interval: int = 10):
        """Start background health check thread."""
        def check_loop():
            while True:
                for backend in self.backends:
                    try:
                        response = requests.get(
                            f"{backend.url}/health",
                            timeout=5
                        )
                        if response.status_code == 200:
                            if backend.status != BackendStatus.HEALTHY:
                                self.logger.info(f"Backend {backend.url} is now HEALTHY")
                            backend.status = BackendStatus.HEALTHY
                        else:
                            backend.status = BackendStatus.UNHEALTHY
                    except requests.RequestException:
                        if backend.status != BackendStatus.UNHEALTHY:
                            self.logger.warning(f"Backend {backend.url} is now UNHEALTHY")
                        backend.status = BackendStatus.UNHEALTHY
                
                time.sleep(interval)
        
        thread = threading.Thread(target=check_loop, daemon=True)
        thread.start()

# ═══════════════════════════════════════════════════════════════════════════════
# FLASK_APP
# ═══════════════════════════════════════════════════════════════════════════════
app = Flask(__name__)

# Initialise load balancer
backends = [
    Backend("backend1", 5001),
    Backend("backend2", 5002),
    Backend("backend3", 5003),
]
lb = LoadBalancer(backends, algorithm="round_robin")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    """Forward request to selected backend."""
    backend = lb.get_backend()
    
    if not backend:
        return Response("Service Unavailable", status=503)
    
    backend.active_connections += 1
    
    try:
        url = f"{backend.url}/{path}"
        response = requests.request(
            method=request.method,
            url=url,
            headers={k: v for k, v in request.headers if k != 'Host'},
            data=request.get_data(),
            timeout=30
        )
        
        return Response(
            response.content,
            status=response.status_code,
            headers=dict(response.headers)
        )
    finally:
        backend.active_connections -= 1
```

---

## 📋 Expected Outputs

### Scenario 1: Load Distribution

**Test with curl loop:**
```bash
for i in {1..10}; do curl http://localhost:8080/; done
```

**Expected output (round-robin):**
```
Response from backend1
Response from backend2
Response from backend3
Response from backend1
Response from backend2
...
```

### Scenario 2: Failover

**Stop one backend:**
```bash
docker stop backend2
```

**Expected log:**
```
[WARNING] Backend http://backend2:5002 is now UNHEALTHY
[INFO] Routing to backend1 (skipped unhealthy backend2)
```

---

## ❓ Frequently Asked Questions

**Q: How do I test load distribution?**

A: Use wrk or ab for load testing:
```bash
wrk -t4 -c100 -d30s http://localhost:8080/
```

**Q: Why doesn't Docker DNS resolve backend names?**

A: Ensure containers are on the same Docker network. Check with:
```bash
docker network inspect project_network
```

---

## 📚 Laboratory References

| Week | Folder | Relevant Content |
|------|--------|------------------|
| 10 | `10enWSL/` | Docker networking |
| 11 | `11enWSL/` | Load balancing concepts |
| 12 | `12enWSL/` | Distributed systems |

---

## 📚 Bibliography

1. **[OFFICIAL]** Docker Networking Documentation  
   URL: https://docs.docker.com/network/  
   Verified: 2026-01-24 ✓

2. **[OFFICIAL]** Flask Documentation  
   URL: https://flask.palletsprojects.com/  
   Verified: 2026-01-24 ✓

---

*Last update: January 2026 — Computer Networks, ASE Bucharest*
