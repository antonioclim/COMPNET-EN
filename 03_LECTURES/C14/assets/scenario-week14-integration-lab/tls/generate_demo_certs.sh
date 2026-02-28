#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

CA_DIR="$ROOT_DIR/ca"
SERVER_DIR="$ROOT_DIR/server"
PRIVATE_DIR="$ROOT_DIR/private"

mkdir -p "$CA_DIR" "$SERVER_DIR" "$PRIVATE_DIR"

CA_KEY="$PRIVATE_DIR/ca.key"
CA_CERT="$CA_DIR/ca.crt"

SERVER_KEY="$SERVER_DIR/server.key"
SERVER_CSR="$SERVER_DIR/server.csr"
SERVER_CERT="$SERVER_DIR/server.crt"

if ! command -v openssl >/dev/null 2>&1; then
  echo "ERROR: openssl is required to generate demo certificates." >&2
  exit 1
fi

# Clean up previous artefacts (safe in a teaching lab)
rm -f "$SERVER_CSR" "$SERVER_CERT" "$SERVER_DIR/ca.srl" || true

# 1) Demo CA
if [[ ! -f "$CA_KEY" || ! -f "$CA_CERT" ]]; then
  echo "[1/3] Generating demo CA"
  openssl genrsa -out "$CA_KEY" 2048
  openssl req -x509 -new -nodes -key "$CA_KEY" -sha256 -days 365 \
    -out "$CA_CERT" -subj "/CN=week14-demo-ca"
else
  echo "[1/3] Reusing existing demo CA: $CA_CERT"
fi

# 2) Server key + CSR (SAN)
TMP_CONF="$(mktemp)"
cat > "$TMP_CONF" <<CONF
[ req ]
default_bits       = 2048
distinguished_name = dn
req_extensions     = req_ext
prompt             = no

[ dn ]
CN = www.week14.local

[ req_ext ]
subjectAltName = @alt_names

[ alt_names ]
DNS.1 = www.week14.local
DNS.2 = api.week14.local
CONF

echo "[2/3] Generating server key + CSR"
openssl genrsa -out "$SERVER_KEY" 2048
openssl req -new -key "$SERVER_KEY" -out "$SERVER_CSR" -config "$TMP_CONF"

# 3) Sign server certificate
echo "[3/3] Signing server certificate with demo CA"
openssl x509 -req -in "$SERVER_CSR" -CA "$CA_CERT" -CAkey "$CA_KEY" -CAcreateserial \
  -out "$SERVER_CERT" -days 365 -sha256 -extfile "$TMP_CONF" -extensions req_ext

rm -f "$TMP_CONF"

# Verify
openssl verify -CAfile "$CA_CERT" "$SERVER_CERT" >/dev/null

echo "OK"
echo "  CA cert:      $CA_CERT"
echo "  Server cert:  $SERVER_CERT"
echo "  Server key:   $SERVER_KEY"
