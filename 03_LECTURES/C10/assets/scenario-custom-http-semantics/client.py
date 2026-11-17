from __future__ import annotations

import time
import requests

BASE = "http://127.0.0.1:7000"

def main():
    r = requests.post(f"{BASE}/jobs", json={"n": 15}, timeout=5)
    r.raise_for_status()
    if r.status_code != 202 or not r.headers.get("Location", "").startswith("/jobs/"):
        raise SystemExit("Expected 202 Accepted and a /jobs/ Location header")
    print("POST /jobs:", r.status_code)
    print("Location:", r.headers.get("Location"))
    job_url = r.headers["Location"]

    deadline = time.monotonic() + 60
    while time.monotonic() < deadline:
        s = requests.get(f"{BASE}{job_url}", timeout=5)
        s.raise_for_status()
        data = s.json()
        print("status:", data["status"], "progress:", data["progress"])
        if data["status"] == "failed":
            raise SystemExit(f"Job failed: {data.get('error', 'no details')}")
        if data["status"] == "done":
            break
        time.sleep(0.3)

    else:
        raise SystemExit("Job did not finish within 60 seconds")

    res = requests.get(f"{BASE}{data['links']['result']}", timeout=5)
    res.raise_for_status()
    print("GET result:", res.status_code, res.json())

if __name__ == "__main__":
    main()
