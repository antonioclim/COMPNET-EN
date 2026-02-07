### Scenario IoT basic: sensor + actuator (MQTT)

#### Setup
- broker: eclipse-mosquitto
- sensor: publishes temperature to sensors/temperature
- actuator: subscribes and publishes ON/OFF to actuators/fan based on threshold

#### Run
1) docker compose up --build

#### Observe
- sensor prints published values
- actuator prints received values and transitions
- retained command topic (actuators/fan) keeps last state

#### Optional checks
- Inspect broker logs:
  docker logs -f iot-broker
- Subscribe from host if you have mosquitto-clients:
  mosquitto_sub -h localhost -p 1883 -t "sensors/#" -v
  mosquitto_sub -h localhost -p 1883 -t "actuators/#" -v
