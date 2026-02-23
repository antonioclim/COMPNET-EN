from __future__ import annotations

import time
import requests

BASE = "http://127.0.0.1:7000"

def main():
    r = requests.post(f"{BASE}/jobs", json={"n": 15})
    print("POST /jobs:", r.status_code)
    print("Location:", r.headers.get("Location"))
    job_url = r.headers["Location"]

    while True:
        s = requests.get(f"{BASE}{job_url}")
        data = s.json()
        print("status:", data["status"], "progress:", data["progress"])
        if data["status"] == "done":
            break
        time.sleep(0.3)

    res = requests.get(f"{BASE}{data['links']['result']}")
    print("GET result:", res.status_code, res.json())

if __name__ == "__main__":
    main()
