#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"

PORT=9443

echo "[server] starting openssl s_server on port $PORT"
echo "[server] press Ctrl+C to stop"
openssl s_server \
  -accept "$PORT" \
  -cert certs/cert.pem \
  -key certs/key.pem \
  -tls1_3 \
  -www
