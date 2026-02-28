### Scenario: basic IoT (sensor and actuator over MQTT)

#### Components
- broker: eclipse-mosquitto
- sensor: publishes temperature to `sensors/temperature`
- actuator: subscribes and publishes `ON`/`OFF` to `actuators/fan` when the threshold is exceeded

#### Run (plaintext MQTT)
```bash
docker compose up --build
```

#### Optional: run via the Phase C lab runner
From the repository root:

```bash
python 00_TOOLS/lab_runner/lab_runner.py up c13-iot-basic --build
python 00_TOOLS/lab_runner/lab_runner.py logs c13-iot-basic --follow
python 00_TOOLS/lab_runner/lab_runner.py down c13-iot-basic
```

#### Run (optional TLS MQTT)
1) Generate demo certificates:
```bash
bash tls/generate_demo_certs.sh
```

2) Start the scenario with the TLS override:
```bash
docker compose -f docker-compose.yml -f docker-compose.tls.yml up --build
```

#### Observe
- the sensor prints published values
- the actuator prints received values and state transitions
- the command topic (`actuators/fan`) keeps the last state (topic retention may depend on broker configuration)

#### Optional checks
- Inspect broker logs:
  - `docker logs -f iot-broker`
- Subscribe from the host (requires `mosquitto-clients`):
  - `mosquitto_sub -h localhost -p 1883 -t "sensors/#" -v`
  - `mosquitto_sub -h localhost -p 1883 -t "actuators/#" -v`
- Use the built-in CLI container (no host install required):
  - Plaintext:
    ```bash
    docker compose -f docker-compose.yml -f docker-compose.cli.yml --profile cli \
      run --rm mqtt-cli \
      --mode subscribe --topic sensors/temperature --broker broker --port 1883
    ```
  - TLS:
    ```bash
    docker compose -f docker-compose.yml -f docker-compose.tls.yml -f docker-compose.cli.yml --profile cli \
      run --rm mqtt-cli \
      --mode subscribe --topic sensors/temperature --broker broker --port 8883 \
      --tls --cafile /certs/ca.crt
    ```

## Files

| Name | Notes |
|------|-------|
| `docker-compose.yml` | Base (plaintext) scenario |
| `docker-compose.tls.yml` | Optional TLS override (adds port 8883 + mounts certs) |
| `docker-compose.cli.yml` | Optional MQTT CLI client (profile `cli`) |
| `actuator/` | actuator container |
| `sensor/` | sensor container |
| `mosquitto/` | broker configuration (supports optional `conf.d/` snippets) |
| `tls/` | TLS assets and certificate generator |
| `client/` | MQTT CLI client container |

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
