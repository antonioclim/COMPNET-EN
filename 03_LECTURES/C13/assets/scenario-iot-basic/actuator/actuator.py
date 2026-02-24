import os
import time
import paho.mqtt.client as mqtt

BROKER = os.getenv("BROKER", "broker")
PORT = int(os.getenv("MQTT_PORT", "1883"))
SENSOR_TOPIC = os.getenv("SENSOR_TOPIC", "sensors/temperature")
COMMAND_TOPIC = os.getenv("COMMAND_TOPIC", "actuators/fan")
THRESHOLD = float(os.getenv("THRESHOLD", "28.0"))

state = {"fan_on": False}

def publish_command(client: mqtt.Client, on: bool) -> None:
    payload = "ON" if on else "OFF"
    client.publish(COMMAND_TOPIC, payload, retain=True)
    print(f"[actuator] command -> {COMMAND_TOPIC}: {payload}")

def on_message(client, userdata, msg):
    try:
        value = float(msg.payload.decode().strip())
    except Exception:
        print(f"[actuator] invalid payload: {msg.payload!r}")
        return

    print(f"[actuator] sensed {value} on {msg.topic}")

    if value >= THRESHOLD and not state["fan_on"]:
        state["fan_on"] = True
        print(f"[actuator] threshold exceeded ({THRESHOLD}), turning fan ON")
        publish_command(client, True)

    if value < THRESHOLD - 1.0 and state["fan_on"]:
        state["fan_on"] = False
        print(f"[actuator] temperature stabilized, turning fan OFF")
        publish_command(client, False)

client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message

while True:
    try:
        client.connect(BROKER, PORT, 60)
        client.subscribe(SENSOR_TOPIC)
        print(f"[actuator] subscribed to {SENSOR_TOPIC}, broker={BROKER}:{PORT}")
        break
    except Exception as e:
        print(f"[actuator] connect failed ({e}), retrying...")
        time.sleep(1)

client.loop_forever()
