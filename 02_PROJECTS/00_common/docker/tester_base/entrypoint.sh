#!/usr/bin/env bash
set -euo pipefail

PROJECT_CODE="${PROJECT_CODE:-}"
PCAP_PATH="${PCAP_PATH:-/artifacts/pcap/traffic_e2.pcap}"
TCPDUMP_PID=""
CAPTURE_RC=0

stop_capture() {
  [[ -n "$TCPDUMP_PID" ]] || return 0
  kill -INT "$TCPDUMP_PID" 2>/dev/null || true
  # Bound cleanup even when the capture process does not respond to SIGINT.
  for _ in {1..30}; do
    kill -0 "$TCPDUMP_PID" 2>/dev/null || break
    sleep 0.1
  done
  kill -TERM "$TCPDUMP_PID" 2>/dev/null || true
  for _ in {1..20}; do
    kill -0 "$TCPDUMP_PID" 2>/dev/null || break
    sleep 0.1
  done
  kill -KILL "$TCPDUMP_PID" 2>/dev/null || true
  if wait "$TCPDUMP_PID"; then
    CAPTURE_RC=0
  else
    CAPTURE_RC=$?
    [[ $CAPTURE_RC -ne 130 ]] || CAPTURE_RC=0
  fi
  TCPDUMP_PID=""
  return 0
}
trap stop_capture EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

if [[ -z "$PROJECT_CODE" ]]; then
  echo "[tester] ERROR: PROJECT_CODE is not set (e.g. S01)." >&2
  exit 2
fi

mkdir -p "$(dirname "$PCAP_PATH")"
echo "[tester] Starting PCAP capture: $PCAP_PATH"
tcpdump -i any -w "$PCAP_PATH" &
TCPDUMP_PID=$!
sleep 1
if ! kill -0 "$TCPDUMP_PID" 2>/dev/null; then
  stop_capture
  echo "[tester] ERROR: capture did not start." >&2
  exit 2
fi

echo "[tester] Running smoke tests (pytest -m e2)..."
TEST_RC=0
pytest -m e2 || TEST_RC=$?

stop_capture
echo "[tester] PCAP validation (tshark) for $PROJECT_CODE"
VALIDATION_RC=0
python tools/validate_pcap.py --project "$PROJECT_CODE" --pcap "$PCAP_PATH" || VALIDATION_RC=$?
echo "[tester] pytest=$TEST_RC capture=$CAPTURE_RC pcap_validation=$VALIDATION_RC"

# Retain the test failure while still flushing and validating its evidence.
[[ $TEST_RC -eq 0 ]] || exit "$TEST_RC"
[[ $CAPTURE_RC -eq 0 ]] || exit 2
exit "$VALIDATION_RC"
