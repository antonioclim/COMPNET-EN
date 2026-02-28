#!/usr/bin/env bash
set -euo pipefail

# generate_demo_certs.sh — generate a self-signed CA + server cert for Mosquitto
#
# Output (relative to this folder):
#   ca/ca.crt
#   private/ca.key
#   server/server.crt
#   server/server.key
#
# The server certificate includes SAN entries for:
#   DNS:broker     (Docker Compose service name)
#   DNS:localhost  (host access)
#   IP:127.0.0.1   (host access)
#
# Rationale: strict TLS clients verify hostnames against SAN.
# In this scenario, containers connect to the broker as "broker".

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${HERE}"

mkdir -p ca private server

CA_KEY="private/ca.key"
CA_CERT="ca/ca.crt"
SERVER_KEY="server/server.key"
SERVER_CERT="server/server.crt"
SERVER_CSR="server/server.csr"
EXTFILE="server/server_ext.cnf"

if ! command -v openssl >/dev/null 2>&1; then
  echo "[generate_demo_certs] ERROR: openssl not found" >&2
  exit 1
fi

echo "[generate_demo_certs] Generating demo CA (self-signed)…"
openssl req -x509 -newkey rsa:2048 -nodes \
  -keyout "${CA_KEY}" \
  -out "${CA_CERT}" \
  -days 365 \
  -subj "/CN=COMPNET-IoT-Demo-CA"

echo "[generate_demo_certs] Generating server key + CSR…"
openssl req -new -newkey rsa:2048 -nodes \
  -keyout "${SERVER_KEY}" \
  -out "${SERVER_CSR}" \
  -subj "/CN=broker"

cat > "${EXTFILE}" <<EOF
subjectAltName=DNS:broker,DNS:localhost,IP:127.0.0.1
EOF

echo "[generate_demo_certs] Signing server certificate with the demo CA…"
openssl x509 -req \
  -in "${SERVER_CSR}" \
  -CA "${CA_CERT}" \
  -CAkey "${CA_KEY}" \
  -CAcreateserial \
  -out "${SERVER_CERT}" \
  -days 365 \
  -sha256 \
  -extfile "${EXTFILE}"

# Clean up intermediate files (keep ca.srl; harmless).
rm -f "${SERVER_CSR}" "${EXTFILE}" || true

# Make files world-readable for container mounts (lab convenience).
# Mosquitto runs as a non-root user inside the container.
chmod 644 "${CA_CERT}" "${SERVER_CERT}" "${SERVER_KEY}"
chmod 600 "${CA_KEY}"

echo ""
echo "[generate_demo_certs] Done."
echo "  CA cert:     ${CA_CERT}"
echo "  CA key:      ${CA_KEY}  (keep private; host only)"
echo "  Server cert: ${SERVER_CERT}"
echo "  Server key:  ${SERVER_KEY}"
