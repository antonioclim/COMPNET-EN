import os
import time
import random
from pathlib import Path

import paho.mqtt.client as mqtt

BROKER = os.getenv("BROKER", "broker")
PORT = int(os.getenv("MQTT_PORT", "1883"))
TOPIC = os.getenv("TOPIC", "sensors/temperature")
INTERVAL_SEC = float(os.getenv("INTERVAL_SEC", "1"))

# Optional TLS toggles (default: off).
MQTT_TLS = os.getenv("MQTT_TLS", "0").strip().lower() in {"1", "true", "yes", "y", "on"}
MQTT_TLS_CA = os.getenv("MQTT_TLS_CA", "")
MQTT_TLS_INSECURE = os.getenv("MQTT_TLS_INSECURE", "0").strip().lower() in {"1", "true", "yes", "y", "on"}


def make_temperature() -> float:
    base = 24.0
    noise = random.uniform(-0.8, 0.8)
    spike = 0.0
    if random.random() < 0.08:
        spike = random.uniform(3.0, 6.0)
    return base + noise + spike


def configure_tls(client: mqtt.Client) -> None:
    """
    Configure TLS when MQTT_TLS=1.

    The recommended configuration is to mount the demo CA and set:
      MQTT_TLS_CA=/certs/ca.crt
      MQTT_TLS_INSECURE=0
    """
    if not MQTT_TLS:
        return

    cafile = MQTT_TLS_CA.strip()
    if cafile and Path(cafile).exists():
        client.tls_set(ca_certs=cafile)
    else:
        # Fallback: system CA store (won't validate the demo self-signed cert),
        # but allows MQTT_TLS_INSECURE=1 to work.
        client.tls_set()

    client.tls_insecure_set(MQTT_TLS_INSECURE)


def main():
    # paho-mqtt 2.x requires explicit callback API version.
    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)

    def on_connect(_client, _userdata, _flags, reason_code, _properties=None):
        if reason_code == 0:
            print(f"[sensor] Connected to MQTT broker at {BROKER}:{PORT}")
        else:
            print(f"[sensor] Connection failed: reason_code={reason_code}")

    client.on_connect = on_connect

    configure_tls(client)

    if MQTT_TLS:
        print("[sensor] TLS enabled" + (" (insecure)" if MQTT_TLS_INSECURE else ""))
        if MQTT_TLS_CA:
            print(f"[sensor] Using CA file: {MQTT_TLS_CA}")

    client.connect(BROKER, PORT, keepalive=60)
    client.loop_start()

    print(f"[sensor] Publishing to topic: {TOPIC} every {INTERVAL_SEC} sec")
    while True:
        temp = make_temperature()
        payload = f"{temp:.2f}"
        client.publish(TOPIC, payload=payload)
        print(f"[sensor] published {payload} to {TOPIC}")
        time.sleep(INTERVAL_SEC)


if __name__ == "__main__":
    main()
