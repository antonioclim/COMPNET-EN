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

## Files

| Name | Lines |
|------|-------|
| `client-test.py` | 113 |
| `common.py` | 14 |
| `server-level0.py` | 49 |
| `server-level1.py` | 53 |
| `server-level2.py` | 55 |
| `server-level3.py` | 83 |

## Cross-References

Parent lecture: [`C10/ — HTTP(S), REST and WebSockets`](../../)
  
Lecture slides: [`c10-http-application-layer.md`](../../c10-http-application-layer.md)
  
Quiz: [`W10`](../../../../00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W10_Questions.md)

## Selective Clone

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set 03_LECTURES/C10/assets/scenario-rest-maturity
```

**Method B — Direct download**

Browse at: `https://github.com/antonioclim/COMPNET-EN/tree/main/03_LECTURES/C10/assets/scenario-rest-maturity`
