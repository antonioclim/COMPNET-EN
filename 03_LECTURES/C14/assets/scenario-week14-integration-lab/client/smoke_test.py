#!/usr/bin/env python3
"""End-to-end smoke test for the Week 14 integration lab.

Run inside the client container.

- Default (HTTP variant):
    python smoke_test.py

- TLS variant (after generating certs + starting with docker-compose.tls.yml):
    python smoke_test.py --tls --cafile /client/certs/ca.crt

"""

from __future__ import annotations

import argparse
import json
import socket
import ssl
import urllib.error
import urllib.request


def must_resolve(name: str) -> list[str]:
    addrs = socket.getaddrinfo(name, None)
    ips = sorted({a[4][0] for a in addrs})
    if not ips:
        raise RuntimeError(f"DNS resolution failed for {name}")
    return ips


def http_get(url: str, ctx: ssl.SSLContext | None = None, timeout: float = 3.0):
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            body = resp.read()
            return resp.status, dict(resp.headers), body
    except urllib.error.HTTPError as e:
        body = e.read()
        return e.code, dict(e.headers), body


def main() -> int:
    ap = argparse.ArgumentParser(description="Week 14 lab smoke test")
    ap.add_argument("--tls", action="store_true", help="Use HTTPS endpoints")
    ap.add_argument("--cafile", default=None, help="CA file for TLS verification")
    args = ap.parse_args()

    failures: list[str] = []

    # 1) DNS
    ips = must_resolve("www.week14.local")
    if "10.14.0.80" not in ips:
        failures.append(f"DNS A record mismatch: expected 10.14.0.80, got {ips}")

    # 2) HTTP vs HTTPS mode
    if args.tls:
        if not args.cafile:
            failures.append("TLS mode requires --cafile (CA certificate)")
            ctx = None
        else:
            ctx = ssl.create_default_context(cafile=args.cafile)
        base = "https://www.week14.local"
    else:
        ctx = None
        base = "http://www.week14.local"

    # 3) Root redirect
    status, headers, _ = http_get(base + "/", ctx=ctx)
    if args.tls:
        # In TLS mode the HTTP listener redirects to HTTPS. On HTTPS itself we still do 302 to /app/.
        if status not in (200, 301, 302):
            failures.append(f"Unexpected status for / in TLS mode: {status}")
    else:
        if status != 302:
            failures.append(f"Expected 302 for /, got {status}")

    # 4) /app/
    status, headers, body = http_get(base + "/app/", ctx=ctx)
    if status != 200:
        failures.append(f"Expected 200 for /app/, got {status}")
    if "X-Debug-Proxy" not in headers:
        failures.append("Missing X-Debug-Proxy header (nginx not in path?)")

    # 5) /api/users
    status, headers, body = http_get(base + "/api/users", ctx=ctx)
    if status != 200:
        failures.append(f"Expected 200 for /api/users, got {status}")
    else:
        try:
            payload = json.loads(body.decode("utf-8", errors="replace"))
            xff = payload.get("debug", {}).get("x_forwarded_for")
            if not xff:
                failures.append("debug.x_forwarded_for missing/empty")
        except json.JSONDecodeError:
            failures.append("/api/users did not return JSON")

    if failures:
        print("FAILED")
        for f in failures:
            print(" -", f)
        return 2

    print("OK")
    print("DNS IPs:", ", ".join(ips))
    print("Mode:", "TLS" if args.tls else "HTTP")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
