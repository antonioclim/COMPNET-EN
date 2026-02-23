import os
import time
import random
import paho.mqtt.client as mqtt

BROKER = os.getenv("BROKER", "broker")
PORT = int(os.getenv("MQTT_PORT", "1883"))
TOPIC = os.getenv("TOPIC", "sensors/temperature")
INTERVAL_SEC = float(os.getenv("INTERVAL_SEC", "1"))

def make_temperature() -> float:
    base = 24.0
    noise = random.uniform(-0.8, 0.8)
    spike = 0.0
    if random.random() < 0.08:
        spike = random.uniform(3.0, 7.0)
    return round(base + noise + spike, 2)

client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)

while True:
    try:
        client.connect(BROKER, PORT, 60)
        break
    except Exception as e:
        print(f"[sensor] connect failed ({e}), retrying...")
        time.sleep(1)

client.loop_start()
print(f"[sensor] publishing to {TOPIC} via {BROKER}:{PORT}")

while True:
    value = make_temperature()
    payload = f"{value}"
    client.publish(TOPIC, payload)
    print(f"[sensor] {TOPIC}: {payload}")
    time.sleep(INTERVAL_SEC)
