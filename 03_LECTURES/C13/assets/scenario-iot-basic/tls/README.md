# Optional MQTT TLS (IoT scenario)

This folder contains **optional** assets to enable TLS for the MQTT broker in
`scenario-iot-basic`.

## Why this exists

The default scenario uses plaintext MQTT on port **1883** for simplicity.

TLS is added as an *optional* extension because it introduces extra concepts:

- CA trust and certificate verification
- certificate subjectAltName (SAN) / hostnames
- distinguishing **broker port** (1883 vs 8883)

## Quick start (TLS mode)

1) Generate demo certificates (self-signed CA):

```bash
bash tls/generate_demo_certs.sh
```

2) Start the scenario with the TLS override:

```bash
docker compose -f docker-compose.yml -f docker-compose.tls.yml up --build
```

3) Run the optional CLI client (subscribe example):

```bash
docker compose -f docker-compose.yml -f docker-compose.tls.yml -f docker-compose.cli.yml --profile cli \
  run --rm mqtt-cli \
  --mode subscribe --topic sensors/temperature --broker broker --port 8883 \
  --tls --cafile /certs/ca.crt
```

## Security warning

The generated keys/certificates are for **demonstration** only.

- The CA private key is stored under `tls/private/` on the host.
- Do not reuse these assets outside the lab.
