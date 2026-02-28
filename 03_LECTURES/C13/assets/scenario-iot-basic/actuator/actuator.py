import os
import time
from pathlib import Path

import paho.mqtt.client as mqtt

BROKER = os.getenv("BROKER", "broker")
PORT = int(os.getenv("MQTT_PORT", "1883"))
SENSOR_TOPIC = os.getenv("SENSOR_TOPIC", "sensors/temperature")
COMMAND_TOPIC = os.getenv("COMMAND_TOPIC", "actuators/fan")
THRESHOLD = float(os.getenv("THRESHOLD", "28.0"))

# Optional TLS toggles (default: off).
MQTT_TLS = os.getenv("MQTT_TLS", "0").strip().lower() in {"1", "true", "yes", "y", "on"}
MQTT_TLS_CA = os.getenv("MQTT_TLS_CA", "")
MQTT_TLS_INSECURE = os.getenv("MQTT_TLS_INSECURE", "0").strip().lower() in {"1", "true", "yes", "y", "on"}


def configure_tls(client: mqtt.Client) -> None:
    if not MQTT_TLS:
        return

    cafile = MQTT_TLS_CA.strip()
    if cafile and Path(cafile).exists():
        client.tls_set(ca_certs=cafile)
    else:
        client.tls_set()

    client.tls_insecure_set(MQTT_TLS_INSECURE)


def main():
    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)

    state = {"fan_on": False}

    def set_fan(on: bool):
        state["fan_on"] = on
        msg = "ON" if on else "OFF"
        client.publish(COMMAND_TOPIC, payload=msg)
        print(f"[actuator] FAN -> {msg} (published to {COMMAND_TOPIC})")

    def on_connect(_client, _userdata, _flags, reason_code, _properties=None):
        if reason_code == 0:
            print(f"[actuator] Connected to MQTT broker at {BROKER}:{PORT}")
            _client.subscribe(SENSOR_TOPIC)
            print(f"[actuator] Subscribed to {SENSOR_TOPIC}")
        else:
            print(f"[actuator] Connection failed: reason_code={reason_code}")

    def on_message(_client, _userdata, msg):
        try:
            payload = msg.payload.decode("utf-8", errors="replace")
            value = float(payload)
        except Exception:
            print(f"[actuator] Invalid sensor payload: {msg.payload!r}")
            return

        print(f"[actuator] sensor={value:.2f}°C threshold={THRESHOLD:.2f}°C")
        if value >= THRESHOLD and not state["fan_on"]:
            set_fan(True)
        elif value < THRESHOLD and state["fan_on"]:
            set_fan(False)

    client.on_connect = on_connect
    client.on_message = on_message

    configure_tls(client)

    if MQTT_TLS:
        print("[actuator] TLS enabled" + (" (insecure)" if MQTT_TLS_INSECURE else ""))
        if MQTT_TLS_CA:
            print(f"[actuator] Using CA file: {MQTT_TLS_CA}")

    client.connect(BROKER, PORT, keepalive=60)
    client.loop_forever()


if __name__ == "__main__":
    main()
