#!/usr/bin/env bash
set -euo pipefail
umask 077
COMP_NET_TLS_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)/tls"
mkdir -p "$COMP_NET_TLS_DIR"
cd "$COMP_NET_TLS_DIR"
if [[ -e ca.key || -e server.key || -e server.crt ]]; then
  echo "Certificate files already exist. Reuse them, or deliberately archive tls/ before regeneration." >&2
  exit 1
fi
openssl req -x509 -newkey rsa:2048 -nodes -days 365 -sha256   -keyout ca.key -out ca.crt -subj '/CN=COMPNET local mail teaching CA'   -addext 'basicConstraints=critical,CA:TRUE' -addext 'keyUsage=critical,keyCertSign,cRLSign'
openssl req -new -newkey rsa:2048 -nodes -keyout server.key -out server.csr -subj '/CN=mail.example.test'
cat > server.ext <<'CERT_EXT'
basicConstraints=critical,CA:FALSE
keyUsage=critical,digitalSignature,keyEncipherment
extendedKeyUsage=serverAuth
subjectAltName=DNS:mail.example.test,DNS:mail,DNS:localhost,IP:127.0.0.1
CERT_EXT
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial   -out server.crt -days 365 -sha256 -extfile server.ext
chmod 644 ca.crt server.crt
openssl verify -CAfile ca.crt -verify_hostname localhost server.crt
