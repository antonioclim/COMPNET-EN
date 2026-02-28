#!/usr/bin/env python3
"""HTTP/HTTPS probe (stdlib only).

Examples (inside client container):
  python http_probe.py http://www.week14.local/app/
  python http_probe.py https://www.week14.local/app/ --cafile /client/certs/ca.crt

"""

from __future__ import annotations

import argparse
import ssl
import urllib.error
import urllib.request


def main() -> int:
    ap = argparse.ArgumentParser(description="HTTP/HTTPS probe")
    ap.add_argument("url")
    ap.add_argument("--cafile", default=None, help="CA file for TLS verification")
    ap.add_argument("--timeout", type=float, default=3.0)
    args = ap.parse_args()

    ctx = None
    if args.url.lower().startswith("https://"):
        ctx = ssl.create_default_context(cafile=args.cafile) if args.cafile else ssl._create_unverified_context()

    req = urllib.request.Request(args.url, method="GET")

    try:
        with urllib.request.urlopen(req, timeout=args.timeout, context=ctx) as resp:
            body = resp.read(512)
            print("STATUS:", resp.status)
            print("HEADERS:")
            for k, v in resp.headers.items():
                print(f"  {k}: {v}")
            print("BODY (first 512 bytes):")
            print(body.decode("utf-8", errors="replace"))
            return 0
    except urllib.error.HTTPError as e:
        print("STATUS:", e.code)
        print("HEADERS:")
        for k, v in e.headers.items():
            print(f"  {k}: {v}")
        body = e.read(512)
        print("BODY (first 512 bytes):")
        print(body.decode("utf-8", errors="replace"))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
