#!/usr/bin/env bash
set -euo pipefail

PROJECT_CODE="${PROJECT_CODE:-}"
PCAP_PATH="${PCAP_PATH:-/artifacts/pcap/traffic_e2.pcap}"

if [[ -z "${PROJECT_CODE}" ]]; then
  echo "[tester] ERROR: PROJECT_CODE is not set (e.g. S01)." >&2
  exit 2
fi

mkdir -p "$(dirname "${PCAP_PATH}")"

echo "[tester] Starting PCAP capture: ${PCAP_PATH}"
tcpdump -i any -w "${PCAP_PATH}" >/dev/null 2>&1 &
TCPDUMP_PID=$!

# Small delay so we do not miss the handshake
sleep 1

echo "[tester] Running smoke tests (pytest -m e2)..."
pytest -m e2
TEST_RC=$?

echo "[tester] Stopping tcpdump (PID=${TCPDUMP_PID})"
# SIGINT for flush
kill -2 "${TCPDUMP_PID}" 2>/dev/null || true
wait "${TCPDUMP_PID}" 2>/dev/null || true

echo "[tester] PCAP validation (tshark) for ${PROJECT_CODE}"
python tools/validate_pcap.py --project "${PROJECT_CODE}" --pcap "${PCAP_PATH}"

exit "${TEST_RC}"
