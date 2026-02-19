#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"

mkdir -p certs

openssl req \
  -x509 -newkey rsa:2048 \
  -keyout certs/key.pem \
  -out certs/cert.pem \
  -days 7 \
  -nodes \
  -subj "/CN=localhost"

echo "[gen_certs] generated certs/cert.pem and certs/key.pem"
