### Scenario: REST maturity levels (0–3) in practice

Goal:
- Compare the same business capability implemented at REST Level 0, 1, 2 and 3
- Observe how the client changes and where coupling appears
- Practise reasoning about HTTP semantics, resources and discoverability

Business domain:
- Users (id, name)
- Minimal operations: read user, create user, update user name, delete user

How to run (each level separately):
- python -m venv .venv
- source .venv/bin/activate
- pip install flask requests
- python server-level0.py
  (or server-level1.py / server-level2.py / server-level3.py)

Test:
- python client-test.py --level 0
- python client-test.py --level 1
- python client-test.py --level 2
- python client-test.py --level 3

What to observe:
- Which parts of the protocol are "semantic" (verbs, status codes, Location)
- Where actions leak into payloads (Level 0)
- When URLs identify resources (Level 1+)
- When hypermedia guides the client (Level 3)
