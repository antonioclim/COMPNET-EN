# Project 15: MQTT IoT Client-Server Application

> **Course:** Computer Networks  
> **Programme:** Economic Informatics, Year 3, Semester 2  
> **Institution:** ASE Bucharest - CSIE  
> **Project type:** Main

> 📍 **Navigation:** [00PROJ](../README.md) → [PROJECTS](./README.md) → P15
> 
> **Related:** [P20 (IoT Security)](../RESERVE_individual/P20_IoT_Security_Privacy.md)

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

**Repository:** `https://github.com/[username]/retele-proiect-15`

---

### 📊 Assessment Rubric

#### Stage 1 — Design (100 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Complete specifications | 30 | Topic hierarchy, message formats |
| Architecture diagrams | 20 | Broker, publishers, subscribers |
| Implementation plan | 15 | Realistic timeline |
| Repository initialised | 15 | GitHub configured |
| MANIFEST.txt | 10 | Valid signature |
| Archive naming | 10 | Follows convention |

#### Stage 2 — Prototype (100 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Basic pub/sub working | 35 | Publish and subscribe functional |
| Code quality | 25 | Clean, typed, documented |
| Broker connectivity | 15 | Connects to broker correctly |
| Progress report | 10 | Documents progress |
| MANIFEST.txt | 10 | Valid signature |
| On-time delivery | 5 | Meets deadline |

#### Stage 3 — Final Version (100 points + 10 bonus)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Complete implementation | 40 | Multiple sensors + QoS + retain |
| Final code quality | 20 | Production-ready |
| Tests | 15 | Integration tests |
| Documentation | 10 | Complete docs |
| Simulated IoT scenario | 5 | Realistic use case |
| MANIFEST.txt | 10 | Valid signature |
| **Bonus: TLS security** | +10 | Encrypted MQTT (teams of 3) |

#### Stage 4 — Presentation (100 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Live demo functional | 35 | Real-time pub/sub visible |
| Technical presentation | 25 | Explains MQTT protocol |
| Answers to questions | 20 | Demonstrates understanding |
| Team contribution | 15 | All members know code |
| Time management | 5 | 10-15 minutes |

---

### 👥 Team Size

| Team | Requirements |
|------|--------------|
| **1 person** | 3 simulated sensors + 1 subscriber + QoS 0/1 |
| **2 persons** | + QoS 2 + retained messages + wildcard subscriptions |
| **3 persons** | + TLS security + persistence + dashboard |

---

## 📚 Project Description

Build an IoT application using MQTT (Message Queuing Telemetry Transport) protocol. Create simulated sensors that publish data (temperature, humidity, motion) and subscribers that receive and process this data. Demonstrate MQTT's publish-subscribe model, Quality of Service levels and retained messages.

MQTT is the de-facto standard for IoT communication due to its lightweight nature and support for unreliable networks.

### 🎯 Learning Objectives

- **LO1:** Implement MQTT publish-subscribe communication
- **LO2:** Design topic hierarchies for scalable IoT systems
- **LO3:** Use different QoS levels based on message importance
- **LO4:** Handle connection loss and reconnection gracefully
- **LO5:** Implement retained messages for initial state
- **LO6:** Process real-time sensor data streams

### 🛠️ Technologies and Tools

| Technology | Purpose | Documentation |
|------------|---------|---------------|
| **paho-mqtt** | MQTT client library | [eclipse.org/paho](https://eclipse.org/paho) |
| **Mosquitto** | MQTT broker | [mosquitto.org](https://mosquitto.org) |
| **MQTT Explorer** | GUI client for testing | [mqtt-explorer.com](http://mqtt-explorer.com) |
| **Docker** | Containerised broker | [docs.docker.com](https://docs.docker.com) |

### 📖 Key Concepts

| Concept | Description |
|---------|-------------|
| **MQTT** | Lightweight pub-sub messaging protocol |
| **Broker** | Central server routing messages |
| **Publisher** | Client sending messages |
| **Subscriber** | Client receiving messages |
| **Topic** | Message category (hierarchical) |
| **QoS 0** | At most once (fire and forget) |
| **QoS 1** | At least once (may duplicate) |
| **QoS 2** | Exactly once (guaranteed) |
| **Retained** | Last message stored for new subscribers |
| **LWT** | Last Will and Testament (disconnect message) |

---

## ⛔ Constraints (MUST/MUST NOT)

### MUST (Mandatory)
- [ ] MUST use MQTT protocol (not HTTP/WebSocket alternatives)
- [ ] MUST implement at least 3 different sensor types
- [ ] MUST demonstrate QoS 0, 1 and 2
- [ ] MUST use hierarchical topic structure
- [ ] MUST handle broker disconnection gracefully
- [ ] MUST pass all smoke tests

### MUST NOT (Forbidden)
- [ ] MUST NOT publish sensitive data unencrypted
- [ ] MUST NOT ignore connection errors
- [ ] MUST NOT use infinite loops without sleep
- [ ] MUST NOT hardcode broker address (use config)

### SHOULD (Recommended)
- [ ] SHOULD implement retained messages
- [ ] SHOULD use Last Will and Testament
- [ ] SHOULD implement message validation

---

## 🎯 Concept Analogies

### MQTT = Newspaper Subscription

🏠 **Real-World Analogy:**  
Newspapers don't send papers directly to everyone. Subscribers register interest in specific sections (Sports, Business). The newspaper (broker) delivers the relevant sections to each subscriber. Publishers (journalists) submit articles to topics.

🖼️ **Visual Representation:**
```
Publishers                BROKER              Subscribers
    │                        │                    │
[Weather]──── /sensors/temp ─┼───► [Dashboard]
[Motion] ──── /sensors/motion┼───► [Alarm System]
[Energy]──── /sensors/power ─┼───► [Analytics]
                             │
                      (Routes messages)
```

💻 **Technical Mapping:**
- Newspaper = MQTT Broker
- Journalist = Publisher
- Reader = Subscriber
- Section = Topic
- Subscription = Subscribe with topic filter
- Delivery = Message routing

⚠️ **Where the analogy breaks:** MQTT is real-time; newspapers are periodic. Also, MQTT supports wildcards (subscribe to all sports topics).

---

### QoS Levels = Mail Services

🏠 **Real-World Analogy:**  
- QoS 0 = Regular mail (might get lost, no confirmation)
- QoS 1 = Tracked mail (confirmation of delivery, might arrive twice if resent)
- QoS 2 = Certified mail with signature (exactly once delivery guaranteed)

💻 **Technical Mapping:**
- QoS 0: Publish and forget, no ACK
- QoS 1: PUBACK required, may retry
- QoS 2: 4-way handshake (PUBREC, PUBREL, PUBCOMP)

---

## 🗳️ Peer Instruction Questions

### Question 1: QoS Selection

> 💭 **PREDICTION:** Which QoS for temperature readings every second?

**Options:**
- A) QoS 0 (acceptable to lose some) ✓
- B) QoS 1 (ensure delivery)
- C) QoS 2 (exactly once)
- D) Depends on broker

**Correct answer:** A

**Explanation:** Frequent sensor readings are redundant; losing one reading is acceptable. QoS 0 reduces overhead. Use QoS 1/2 for critical events (alarms, commands).

---

### Question 2: Topic Design

> 💭 **PREDICTION:** Best topic structure for multi-building IoT?

**Options:**
- A) sensor/reading
- B) building/floor/room/sensor/type ✓
- C) buildingAfloor1room3tempSensor
- D) All topics flat

**Correct answer:** B

**Explanation:** Hierarchical topics enable wildcard subscriptions. building/+/+/temp subscribes to all temperature sensors. Flat structure loses this flexibility.

---

### Question 3: Retained Messages

> 💭 **PREDICTION:** Why use retained messages?

**Options:**
- A) To queue messages when subscriber offline
- B) To send last value to new subscribers ✓
- C) To guarantee delivery
- D) To reduce bandwidth

**Correct answer:** B

**Explanation:** Retained messages store the LAST message on a topic. When a new subscriber joins, it immediately receives the current state (last temperature) without waiting for next publish.

---

### Question 4: Last Will

> 💭 **PREDICTION:** What is Last Will and Testament (LWT)?

**Options:**
- A) Message sent when client disconnects gracefully
- B) Message broker publishes if client disconnects ungracefully ✓
- C) Final message from client before shutdown
- D) Acknowledgment of message receipt

**Correct answer:** B

**Explanation:** LWT is pre-registered by client. If client disconnects WITHOUT proper DISCONNECT packet (crash, network failure), broker publishes LWT. Used to announce "device offline."

---

## ❌ Common Misconceptions

### 🚫 "MQTT guarantees delivery"

**WRONG:** MQTT always delivers messages.

**CORRECT:** Only QoS 1/2 have delivery guarantees. QoS 0 is fire-and-forget. Even QoS 2 fails if broker crashes (no persistence).

---

### 🚫 "Topic = Queue"

**WRONG:** MQTT topics store messages like queues.

**CORRECT:** Topics are routing addresses, not storage. Without retained/persistent sessions, messages to topics with no subscribers are lost.

---

### 🚫 "More QoS = better"

**WRONG:** Always use QoS 2 for reliability.

**CORRECT:** QoS 2 has significant overhead (4 packets vs 1 for QoS 0). For high-frequency sensor data, this overhead is wasteful. Match QoS to message importance.

---

## 📖 Glossary

| Term | Definition |
|------|------------|
| **MQTT** | Message Queuing Telemetry Transport |
| **Broker** | Server routing messages between clients |
| **Topic** | Hierarchical message address |
| **Publish** | Send message to topic |
| **Subscribe** | Register interest in topic |
| **QoS** | Quality of Service level (0, 1, 2) |
| **Retained** | Message stored for new subscribers |
| **LWT** | Last Will and Testament |
| **Clean Session** | Don't restore previous subscriptions |
| **Wildcard** | + (single level) or # (multi-level) |

---

## 🔨 Implementation Example

```python
#!/usr/bin/env python3
"""MQTT IoT Sensor Simulator"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
import paho.mqtt.client as mqtt
import json
import time
import random
import logging
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
BROKER_HOST = "localhost"
BROKER_PORT = 1883
BASE_TOPIC = "building/floor1/room101"

# ═══════════════════════════════════════════════════════════════════════════════
# DATA_MODELS
# ═══════════════════════════════════════════════════════════════════════════════
@dataclass
class SensorReading:
    """Sensor data reading."""
    sensor_id: str
    sensor_type: str
    value: float
    unit: str
    timestamp: str

# ═══════════════════════════════════════════════════════════════════════════════
# SENSORS
# ═══════════════════════════════════════════════════════════════════════════════
class TemperatureSensor:
    """
    Simulated temperature sensor.
    
    # 💭 PREDICTION: What QoS for temperature readings?
    # Answer: QoS 0 - frequent readings, losing one is acceptable
    """
    
    def __init__(self, sensor_id: str, base_temp: float = 22.0):
        self.sensor_id = sensor_id
        self.base_temp = base_temp
    
    def read(self) -> SensorReading:
        """Generate temperature reading."""
        temp = self.base_temp + random.uniform(-2.0, 2.0)
        return SensorReading(
            sensor_id=self.sensor_id,
            sensor_type="temperature",
            value=round(temp, 2),
            unit="celsius",
            timestamp=datetime.now().isoformat()
        )


class MotionSensor:
    """Simulated motion sensor."""
    
    def __init__(self, sensor_id: str, detection_probability: float = 0.1):
        self.sensor_id = sensor_id
        self.detection_probability = detection_probability
    
    def read(self) -> Optional[SensorReading]:
        """Generate motion reading (only when detected)."""
        if random.random() < self.detection_probability:
            return SensorReading(
                sensor_id=self.sensor_id,
                sensor_type="motion",
                value=1.0,
                unit="boolean",
                timestamp=datetime.now().isoformat()
            )
        return None

# ═══════════════════════════════════════════════════════════════════════════════
# MQTT_PUBLISHER
# ═══════════════════════════════════════════════════════════════════════════════
class IoTPublisher:
    """MQTT publisher for IoT sensors."""
    
    def __init__(self, client_id: str, broker_host: str, broker_port: int):
        self.client = mqtt.Client(client_id=client_id)
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.connected = False
        self.logger = logging.getLogger(__name__)
        
        # Callbacks
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        
        # Last Will and Testament
        self.client.will_set(
            topic=f"{BASE_TOPIC}/status",
            payload=json.dumps({"status": "offline", "client_id": client_id}),
            qos=1,
            retain=True
        )
    
    def _on_connect(self, client, userdata, flags, rc):
        """Handle connection."""
        if rc == 0:
            self.connected = True
            self.logger.info("Connected to broker")
            
            # Publish online status (retained)
            self.client.publish(
                f"{BASE_TOPIC}/status",
                json.dumps({"status": "online"}),
                qos=1,
                retain=True
            )
        else:
            self.logger.error(f"Connection failed: {rc}")
    
    def _on_disconnect(self, client, userdata, rc):
        """Handle disconnection."""
        self.connected = False
        self.logger.warning(f"Disconnected: {rc}")
    
    def connect(self) -> None:
        """Connect to broker."""
        self.client.connect(self.broker_host, self.broker_port, keepalive=60)
        self.client.loop_start()
    
    def publish_reading(self, reading: SensorReading, qos: int = 0) -> None:
        """Publish sensor reading."""
        topic = f"{BASE_TOPIC}/{reading.sensor_type}/{reading.sensor_id}"
        payload = json.dumps(asdict(reading))
        
        result = self.client.publish(topic, payload, qos=qos)
        
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            self.logger.debug(f"Published to {topic}: {reading.value}{reading.unit}")
        else:
            self.logger.error(f"Publish failed: {result.rc}")
    
    def disconnect(self) -> None:
        """Disconnect gracefully."""
        self.client.loop_stop()
        self.client.disconnect()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    logging.basicConfig(level=logging.INFO)
    
    # Create sensors
    temp_sensor = TemperatureSensor("temp_001")
    motion_sensor = MotionSensor("motion_001")
    
    # Create publisher
    publisher = IoTPublisher("sensor_node_1", BROKER_HOST, BROKER_PORT)
    publisher.connect()
    
    time.sleep(1)  # Wait for connection
    
    try:
        while True:
            # Publish temperature (QoS 0 - frequent, loss acceptable)
            temp_reading = temp_sensor.read()
            publisher.publish_reading(temp_reading, qos=0)
            
            # Publish motion (QoS 1 - important event)
            motion_reading = motion_sensor.read()
            if motion_reading:
                publisher.publish_reading(motion_reading, qos=1)
            
            time.sleep(5)
    
    except KeyboardInterrupt:
        publisher.disconnect()

if __name__ == "__main__":
    main()
```

---

## 📋 Expected Outputs

### Scenario 1: Sensor Publishing

**Subscribe to see messages:**
```bash
mosquitto_sub -h localhost -t "building/#" -v
```

**Expected output:**
```
building/floor1/room101/temperature/temp_001 {"sensor_id":"temp_001","value":22.34,"unit":"celsius",...}
building/floor1/room101/motion/motion_001 {"sensor_id":"motion_001","value":1.0,"unit":"boolean",...}
```

### Scenario 2: Retained Status

**Subscribe to status after sensor started:**
```bash
mosquitto_sub -h localhost -t "building/+/+/status" -v
```

**Expected output (immediately, retained):**
```
building/floor1/room101/status {"status": "online"}
```

---

## ❓ Frequently Asked Questions

**Q: How do I run a local broker?**

A: Use Docker:
```bash
docker run -d -p 1883:1883 eclipse-mosquitto
```

**Q: How do I see all messages?**

A: Subscribe to all topics:
```bash
mosquitto_sub -h localhost -t "#" -v
```

---

## 📚 Laboratory References

| Week | Folder | Relevant Content |
|------|--------|------------------|
| 13 | `13enWSL/` | MQTT protocol, IoT |
| 14 | `14enWSL/` | IoT security |

---

## 📚 Bibliography

1. **[OFFICIAL]** Eclipse Paho Python Client  
   URL: https://eclipse.dev/paho/clients/python/  
   Verified: 2026-01-24 ✓

2. **[OFFICIAL]** MQTT Specification  
   URL: https://mqtt.org/mqtt-specification/  
   Verified: 2026-01-24 ✓

---

*Last update: January 2026 — Computer Networks, ASE Bucharest*
