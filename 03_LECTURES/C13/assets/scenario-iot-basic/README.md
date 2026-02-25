### Scenario: basic IoT (sensor and actuator over MQTT)

#### Components
- broker: eclipse-mosquitto
- sensor: publishes temperature to sensors/temperature
- actuator: subscribes and publishes ON/OFF to actuators/fan when the threshold is exceeded

#### Run
1) docker compose up --build

#### Observe
- the sensor prints published values
- the actuator prints received values and state transitions
- the retained command topic (actuators/fan) keeps the last state

#### Optional checks
- Inspect broker logs:
  - docker logs -f iot-broker
- Subscribe from the host (requires mosquitto-clients):
  - mosquitto_sub -h localhost -p 1883 -t "sensors/#" -v
  - mosquitto_sub -h localhost -p 1883 -t "actuators/#" -v

## Files

| Name | Lines |
|------|-------|
| `docker-compose.yml` | 33 |
| `actuator/` | 2 files |
| `mosquitto/` | 1 files |
| `sensor/` | 2 files |

## Cross-References

Parent lecture: [`C13/ — IoT and Network Security`](../../)
  
Lecture slides: [`c13-iot-security.md`](../../c13-iot-security.md)
  
Quiz: [`W13`](../../../../00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W13_Questions.md)

## Selective Clone

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set 03_LECTURES/C13/assets/scenario-iot-basic
```

**Method B — Direct download**

Browse at: `https://github.com/antonioclim/COMPNET-EN/tree/main/03_LECTURES/C13/assets/scenario-iot-basic`
