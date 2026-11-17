"""
mqtt_cli.py — small MQTT CLI client for the IoT scenario (optional)

This script is designed to be run inside the provided Docker Compose network:

Plaintext mode example (subscribe):
  docker compose -f docker-compose.yml -f docker-compose.cli.yml --profile cli \
    run --rm mqtt-cli \
    --mode subscribe --topic sensors/temperature --broker broker --port 1883

TLS mode example (subscribe):
  docker compose -f docker-compose.yml -f docker-compose.tls.yml -f docker-compose.cli.yml --profile cli \
    run --rm mqtt-cli \
    --mode subscribe --topic sensors/temperature --broker broker --port 8883 \
    --tls --cafile /certs/ca.crt

Notes
-----
- The default broker is the Docker Compose service name: 'broker'
- This is a teaching tool: it is intentionally minimal, but does support TLS.
"""

from __future__ import annotations

import argparse
import os
import signal
import ssl
import sys
import time
import threading
from typing import Optional

import paho.mqtt.client as mqtt


def env_bool(name: str, default: bool = False) -> bool:
    v = os.getenv(name)
    if v is None:
        return default
    return v.strip().lower() in {"1", "true", "yes", "y", "on"}


def configure_tls(client: mqtt.Client, cafile: Optional[str], insecure: bool) -> None:
    if cafile:
        client.tls_set(ca_certs=cafile)
    else:
        # Use system CAs (won't validate self-signed demo certs unless insecure=True)
        client.tls_set()
    client.tls_insecure_set(insecure)


def main() -> int:
    ap = argparse.ArgumentParser(description="MQTT CLI client (IoT scenario)")
    ap.add_argument("--mode", choices=["publish", "subscribe"], required=True)
    ap.add_argument("--topic", required=True)
    ap.add_argument("--message", default="hello")
    ap.add_argument("--broker", default=os.getenv("BROKER", "broker"))
    ap.add_argument("--port", type=int, default=int(os.getenv("MQTT_PORT", "1883")))
    ap.add_argument("--qos", type=int, default=0, choices=[0, 1, 2])
    ap.add_argument("--tls", action="store_true", help="Enable TLS")
    ap.add_argument("--cafile", default=os.getenv("MQTT_TLS_CA", None), help="CA certificate path (TLS)")
    ap.add_argument("--insecure", action="store_true", help="Disable certificate hostname verification (TLS)")
    ap.add_argument("--keepalive", type=int, default=60)
    args = ap.parse_args()

    # MQTT 5 lets the CLI report negative publish/subscription acknowledgements.
    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
                         protocol=mqtt.MQTTv5)
    connected = threading.Event()
    acknowledged = threading.Event()
    stop = threading.Event()
    outcome = {"code": 1, "connected": False}

    def on_connect(_client, _userdata, _flags, reason_code, _properties=None):
        outcome["connected"] = reason_code == 0
        if reason_code != 0:
            print(f"[ERROR] Connection refused: {reason_code}", file=sys.stderr)
        connected.set()

    def on_publish(_client, _userdata, _mid, reason_code, _properties=None):
        outcome["code"] = 1 if reason_code.is_failure else 0
        if reason_code.is_failure:
            print(f"[ERROR] Publish rejected: {reason_code}", file=sys.stderr)
        acknowledged.set()

    def on_subscribe(_client, _userdata, _mid, reason_codes, _properties=None):
        outcome["code"] = 1 if any(code.is_failure for code in reason_codes) else 0
        acknowledged.set()

    def on_disconnect(_client, _userdata, _flags, reason_code, _properties=None):
        if not stop.is_set():
            outcome["code"] = 1
            print(f"[ERROR] Disconnected: {reason_code}", file=sys.stderr)
            stop.set()

    def on_message(_client, _userdata, msg):
        print(f"[MSG] {msg.topic}: {msg.payload.decode('utf-8', errors='replace')}")

    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_subscribe = on_subscribe
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    if args.tls:
        configure_tls(client, cafile=args.cafile, insecure=args.insecure)
    signal.signal(signal.SIGINT, lambda *_: stop.set())
    loop_started = False
    try:
        client.connect(args.broker, args.port, keepalive=args.keepalive)
        client.loop_start()
        loop_started = True
        if not connected.wait(10) or not outcome["connected"]:
            print("[ERROR] No successful CONNACK within 10 seconds", file=sys.stderr)
            return 1
        print(f"[OK] Connected to {args.broker}:{args.port}")
        if args.mode == "publish":
            result = client.publish(args.topic, payload=args.message, qos=args.qos)
            if result.rc != mqtt.MQTT_ERR_SUCCESS:
                print(f"[ERROR] Publish failed: rc={result.rc}", file=sys.stderr)
                return 1
            if not acknowledged.wait(10):
                print("[ERROR] Publish did not complete within 10 seconds", file=sys.stderr)
                return 1
            if outcome["code"] == 0:
                print(f"[OK] Publish completed (QoS {args.qos}): {args.topic}")
                if args.qos == 0:
                    print("[INFO] QoS 0 confirms a local send, not broker acceptance or subscriber delivery.")
            return outcome["code"]
        rc, _mid = client.subscribe(args.topic, qos=args.qos)
        if rc != mqtt.MQTT_ERR_SUCCESS or not acknowledged.wait(10) or outcome["code"]:
            print("[ERROR] Subscription was not accepted", file=sys.stderr)
            return 1
        print(f"[OK] Subscribed to {args.topic}")
        while not stop.wait(0.2):
            pass
        return outcome["code"]
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1
    finally:
        stop.set()
        client.disconnect()
        if loop_started:
            client.loop_stop()


if __name__ == "__main__":
    raise SystemExit(main())
