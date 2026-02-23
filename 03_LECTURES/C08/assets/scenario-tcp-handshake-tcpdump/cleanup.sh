#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"

if [ -f tcpdump.pid ]; then
  sudo kill "$(cat tcpdump.pid)" 2>/dev/null || true
  rm -f tcpdump.pid
fi

if [ -f server.pid ]; then
  kill "$(cat server.pid)" 2>/dev/null || true
  rm -f server.pid
fi

echo "[cleanup] ok"
