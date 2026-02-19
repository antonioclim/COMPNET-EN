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
