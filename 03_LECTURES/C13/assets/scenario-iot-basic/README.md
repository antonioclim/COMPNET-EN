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
