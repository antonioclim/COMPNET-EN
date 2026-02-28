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

    # paho 2.x requires explicit callback API version.
    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)

    stop = {"flag": False}

    def on_connect(_client, _userdata, _flags, reason_code, _properties=None):
        if reason_code == 0:
            print(f"[OK] Connected to {args.broker}:{args.port}")
            if args.mode == "subscribe":
                _client.subscribe(args.topic, qos=args.qos)
                print(f"[OK] Subscribed to: {args.topic} (qos={args.qos})")
            else:
                result = _client.publish(args.topic, payload=args.message, qos=args.qos)
                if result.rc == mqtt.MQTT_ERR_SUCCESS:
                    print(f"[OK] Published to {args.topic}: {args.message!r}")
                else:
                    print(f"[WARN] Publish failed: rc={result.rc}")
                stop["flag"] = True
        else:
            print(f"[ERROR] Connection failed: reason_code={reason_code}", file=sys.stderr)
            stop["flag"] = True

    def on_message(_client, _userdata, msg):
        try:
            payload = msg.payload.decode("utf-8", errors="replace")
        except Exception:
            payload = repr(msg.payload)
        print(f"[MSG] {msg.topic}: {payload}")

    client.on_connect = on_connect
    client.on_message = on_message

    if args.tls:
        configure_tls(client, cafile=args.cafile, insecure=args.insecure)
        print("[INFO] TLS enabled" + (" (insecure)" if args.insecure else ""))

    def handle_sigint(_sig, _frame):
        stop["flag"] = True

    signal.signal(signal.SIGINT, handle_sigint)

    client.connect(args.broker, args.port, keepalive=args.keepalive)
    client.loop_start()

    # For publish mode we stop after publishing once.
    # For subscribe mode we keep running until Ctrl+C.
    while not stop["flag"]:
        time.sleep(0.2)

    client.loop_stop()
    client.disconnect()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
