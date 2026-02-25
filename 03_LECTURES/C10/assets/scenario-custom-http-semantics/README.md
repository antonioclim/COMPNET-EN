### Scenario: custom HTTP semantics: asynchronous jobs with 202 Accepted

Aim:
- Implement a long-running operation without blocking the client
- Use `202 Accepted` with a `Location` header that points to a job resource
- Poll job status until completion and then fetch the result

Endpoints:
- POST /jobs
  - returns 202 + Location: /jobs/<id>
- GET /jobs/<id>
  - returns status: pending|running|done|failed
- GET /jobs/<id>/result
  - returns result only if done

Exercises:
1) Start the server and create a job
2) Poll job status until it is done
3) Fetch the result
4) Discuss where the session concept appears and what state means in this context (resource state rather than a transport session)

Run:
- python -m venv .venv
- source .venv/bin/activate
- pip install flask requests
- python server.py
- python client.py

## Files

| Name | Lines |
|------|-------|
| `client.py` | 26 |
| `server.py` | 92 |

## Cross-References

Parent lecture: [`C10/ — HTTP(S), REST and WebSockets`](../../)
  
Lecture slides: [`c10-http-application-layer.md`](../../c10-http-application-layer.md)
  
Quiz: [`W10`](../../../../00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W10_Questions.md)

## Selective Clone

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set 03_LECTURES/C10/assets/scenario-custom-http-semantics
```

**Method B — Direct download**

Browse at: `https://github.com/antonioclim/COMPNET-EN/tree/main/03_LECTURES/C10/assets/scenario-custom-http-semantics`
