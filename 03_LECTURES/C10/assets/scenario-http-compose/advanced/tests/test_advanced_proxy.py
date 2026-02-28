#!/usr/bin/env python3
"""Host-side smoke tests for the C10 advanced proxy overlay.

Run AFTER the stack is up:
  docker compose -f docker-compose.yml -f advanced/docker-compose.advanced.yml up --build

Then:
  python advanced/tests/test_advanced_proxy.py

This is deliberately dependency-free (stdlib only).
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request

BASE = "http://localhost:8080"


def http_get(path: str, timeout: float = 3.0):
    url = BASE + path
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read()
            return resp.status, dict(resp.headers), body
    except urllib.error.HTTPError as e:
        body = e.read()
        return e.code, dict(e.headers), body


def main() -> int:
    failures = []

    # 1) Load balancing evidence
    instances = set()
    for _ in range(10):
        status, headers, _ = http_get("/app/")
        if status != 200:
            failures.append(f"/app/ expected 200, got {status}")
            break
        inst = headers.get("X-Web-Instance")
        if inst:
            instances.add(inst)
        time.sleep(0.05)

    if len(instances) < 2:
        failures.append(
            "Load balancing not observed: expected >=2 distinct X-Web-Instance values. "
            f"Got: {sorted(instances) or 'NONE'}"
        )

    # 2) API reachable + forwarded headers visible
    status, headers, body = http_get("/api/users")
    if status != 200:
        failures.append(f"/api/users expected 200, got {status}")
    else:
        try:
            payload = json.loads(body.decode("utf-8", errors="replace"))
            xff = payload.get("debug", {}).get("x_forwarded_for")
            if not xff:
                failures.append("API debug.x_forwarded_for is empty (expected a value)")
        except json.JSONDecodeError:
            failures.append("/api/users did not return JSON")

    # 3) Cache behaviour (MISS -> HIT)
    s1, h1, _ = http_get("/api/users")
    s2, h2, _ = http_get("/api/users")
    c1 = h1.get("X-Cache-Status")
    c2 = h2.get("X-Cache-Status")
    if s1 == 200 and s2 == 200:
        if not (c1 and c2):
            failures.append("Missing X-Cache-Status header (expected caching to be enabled)")
        elif not (c1.upper() in {"MISS", "BYPASS", "EXPIRED"} and c2.upper() in {"HIT", "REVALIDATED", "UPDATING"}):
            failures.append(f"Unexpected cache sequence: first={c1!r}, second={c2!r}")

    # 4) Rate limiting evidence (expect at least one 429)
    too_many = 0
    for _ in range(12):
        status, _, _ = http_get("/api/users")
        if status == 429:
            too_many += 1
        time.sleep(0.02)

    if too_many == 0:
        failures.append("Rate limiting not observed: no 429 responses detected")

    if failures:
        print("FAILED")
        for f in failures:
            print(" -", f)
        return 2

    print("OK")
    print("Observed X-Web-Instance values:", ", ".join(sorted(instances)))
    print("Cache sequence:", c1, "->", c2)
    print("429 count:", too_many)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
