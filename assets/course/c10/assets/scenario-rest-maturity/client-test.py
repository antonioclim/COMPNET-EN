from __future__ import annotations

import argparse
import requests

LEVEL_PORT = {
    0: 5000,
    1: 5001,
    2: 5002,
    3: 5003,
}

def p(title: str, r: requests.Response):
    print(f"\n=== {title} ===")
    print("Status:", r.status_code)
    if r.headers.get("Location"):
        print("Location:", r.headers["Location"])
    ct = r.headers.get("Content-Type")
    if ct:
        print("Content-Type:", ct)
    try:
        print(r.json())
    except Exception:
        print(r.text)

def run_level0(base: str):
    r = requests.post(f"{base}/api", json={"action": "get_user", "user_id": 1})
    p("L0 get_user", r)

    r = requests.post(f"{base}/api", json={"action": "create_user", "name": "Carol"})
    p("L0 create_user", r)
    created = r.json()["id"]

    r = requests.post(f"{base}/api", json={"action": "update_user", "user_id": created, "name": "Carol Updated"})
    p("L0 update_user", r)

    r = requests.post(f"{base}/api", json={"action": "delete_user", "user_id": created})
    p("L0 delete_user", r)

def run_level1(base: str):
    r = requests.post(f"{base}/users/1", json={"action": "get"})
    p("L1 get user", r)

    r = requests.post(f"{base}/users", json={"action": "create", "name": "Carol"})
    p("L1 create user", r)
    created = r.json()["id"]

    r = requests.post(f"{base}/users/{created}", json={"action": "update", "name": "Carol Updated"})
    p("L1 update user", r)

    r = requests.post(f"{base}/users/{created}", json={"action": "delete"})
    p("L1 delete user", r)

def run_level2(base: str):
    r = requests.get(f"{base}/users")
    p("L2 list users", r)

    r = requests.post(f"{base}/users", json={"name": "Carol"})
    p("L2 create user", r)
    created = r.json()["id"]

    r = requests.get(f"{base}/users/{created}")
    p("L2 get user", r)

    r = requests.put(f"{base}/users/{created}", json={"name": "Carol Updated"})
    p("L2 put user", r)

    r = requests.delete(f"{base}/users/{created}")
    p("L2 delete user", r)

def run_level3(base: str):
    r = requests.get(f"{base}/")
    p("L3 entrypoint", r)
    users_url = r.json()["links"]["users"]
    create_url = r.json()["links"]["create_user"]

    r = requests.get(f"{base}{users_url}")
    p("L3 list users", r)

    r = requests.post(f"{base}{create_url}", json={"name": "Carol"})
    p("L3 create user", r)
    created_self = r.json()["links"]["self"]

    r = requests.get(f"{base}{created_self}")
    p("L3 get created user", r)

    update_url = r.json()["links"]["update"]
    r = requests.put(f"{base}{update_url}", json={"name": "Carol Updated"})
    p("L3 update via link", r)

    delete_url = r.json()["links"]["delete"]
    r = requests.delete(f"{base}{delete_url}")
    p("L3 delete via link", r)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--level", type=int, choices=[0, 1, 2, 3], required=True)
    args = ap.parse_args()

    port = LEVEL_PORT[args.level]
    base = f"http://127.0.0.1:{port}"

    if args.level == 0:
        run_level0(base)
    elif args.level == 1:
        run_level1(base)
    elif args.level == 2:
        run_level2(base)
    elif args.level == 3:
        run_level3(base)

if __name__ == "__main__":
    main()
