# Project 20: IoT Smart Home Network with Security

> **Course:** Computer Networks | **Institution:** ASE Bucharest - CSIE | **Project type:** Reserve (Individual)

**Common guides:** [Pair Programming](../docs/common/pair_programming_guide.md) | [Code Quality](../docs/common/code_quality_standards.md) | [Git Workflow](../docs/common/git_workflow_detailed.md)

### 📅 Stage Calendar
| Stage | Week | Deliverables | Score |
|-------|------|--------------|-------|
| **E1** - Design | Week 5 | Network diagram + security plan | 20% |
| **E2** - Prototype | Week 9 | Basic IoT communication | 25% |
| **E3** - Final | Week 13 | Security implementation | 35% |
| **E4** - Presentation | Week 14 | Live demo | 20% |

**Repository:** `https://github.com/[username]/retele-proiect-20`

---

## 📚 Project Description

Design and simulate a smart home IoT network with security measures. Implement device communication using MQTT/CoAP, add authentication, encryption and demonstrate secure device management.

### 🎯 Learning Objectives
- **Design** IoT network architecture
- **Implement** secure device communication
- **Configure** authentication mechanisms
- **Demonstrate** security best practices

---

## 🎯 Concept Analogies

### IoT Network = Smart Building
🏠 **Analogy:** A smart building has sensors (IoT devices), a control room (gateway/hub) and communication lines (network). Security means controlling who can enter and what they can do.

💻 **Technical:** Devices → Gateway → Cloud, with authentication at each step.

### Device Authentication = Building Access Cards
🏠 **Analogy:** Each employee has a card (certificate/token) that proves identity and grants specific access levels.

---

## 🗳️ Peer Instruction Questions

### Question 1: IoT Protocols
**Question:** Why is MQTT popular for IoT?
- A) High bandwidth
- B) Low overhead, publish/subscribe model ✓
- C) Built-in encryption
- D) Requires no broker

### Question 2: Security Challenge
**Question:** What makes IoT security difficult?
- A) Devices are expensive
- B) Limited resources for crypto, diverse vendors, hard to update ✓
- C) Too much bandwidth
- D) Simple protocols

---

## ❌ Common Misconceptions

### 🚫 "IoT devices are too simple to hack"
**CORRECT:** Simple devices often have weak security, making them easy targets and entry points.

### 🚫 "Home network firewall protects IoT"
**CORRECT:** Compromised internal devices can attack from inside. Need device-level security too.

---

## 📖 Glossary
| Term | Definition |
|------|------------|
| **IoT** | Internet of Things |
| **MQTT** | Lightweight pub/sub protocol |
| **CoAP** | Constrained Application Protocol |
| **TLS** | Transport Layer Security |
| **Device Certificate** | X.509 cert for device identity |
| **Firmware OTA** | Over-the-air updates |

---

## 🔨 Implementation Example

```python
#!/usr/bin/env python3
"""Secure IoT Device Simulator"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
import paho.mqtt.client as mqtt
import ssl
import json
import time

# ═══════════════════════════════════════════════════════════════════════════════
# SECURE_MQTT_CLIENT
# ═══════════════════════════════════════════════════════════════════════════════
class SecureIoTDevice:
    """IoT device with TLS and authentication."""
    
    def __init__(self, device_id: str, broker: str):
        self.device_id = device_id
        self.broker = broker
        self.client = mqtt.Client(client_id=device_id)
        
        # 💭 PREDICTION: What happens without TLS?
        # Answer: Credentials and data sent in plaintext!
        
        # Configure TLS
        self.client.tls_set(
            ca_certs="ca.crt",
            certfile=f"{device_id}.crt",
            keyfile=f"{device_id}.key",
            tls_version=ssl.PROTOCOL_TLS
        )
        
        # Username/password authentication
        self.client.username_pw_set(device_id, "device_secret")
        
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
    
    def _on_connect(self, client, userdata, flags, rc):
        """Handle connection."""
        if rc == 0:
            print(f"[{self.device_id}] Connected securely")
            # Subscribe to commands for this device
            client.subscribe(f"home/{self.device_id}/cmd")
        else:
            print(f"[{self.device_id}] Connection failed: {rc}")
    
    def _on_message(self, client, userdata, msg):
        """Handle incoming commands."""
        payload = json.loads(msg.payload)
        print(f"[{self.device_id}] Received: {payload}")
    
    def connect(self):
        """Connect to broker with TLS."""
        self.client.connect(self.broker, 8883)  # TLS port
        self.client.loop_start()
    
    def publish_status(self, status: dict):
        """Publish device status."""
        topic = f"home/{self.device_id}/status"
        self.client.publish(topic, json.dumps(status), qos=1)
```

```yaml
# docker-compose.yml for secure IoT stack
services:
  mosquitto:
    image: eclipse-mosquitto:2
    ports:
      - "8883:8883"  # TLS port
    volumes:
      - ./mosquitto/config:/mosquitto/config
      - ./mosquitto/certs:/mosquitto/certs
```

---

## 📚 Laboratory References

Consult these resources from **netENwsl** (https://github.com/antonioclim/netENwsl):

| Week | Folder | Relevant Content |
|------|--------|------------------|
| 13 | `13enWSL/` | IoT with MQTT, Mosquitto broker |
| 9 | `09enWSL/` | TLS/SSL for secure channels |

---

*Last update: January 2026 — Computer Networks, ASE Bucharest*
