#!/usr/bin/env bash
set -euo pipefail

HOST=127.0.0.1
PORT=9443

echo "[client] connecting to $HOST:$PORT using openssl s_client"
openssl s_client \
  -connect "$HOST:$PORT" \
  -tls1_3 \
  -servername localhost \
  -showcerts \
  </dev/null
