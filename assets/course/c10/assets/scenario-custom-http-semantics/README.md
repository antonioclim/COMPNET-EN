### Scenario: custom HTTP semantics - async jobs with 202 Accepted

Goal:
- Implement a "long running" operation without blocking the client
- Use 202 Accepted + Location to a job resource
- Poll job status until completed, then fetch result

Endpoints:
- POST /jobs
  - returns 202 + Location: /jobs/<id>
- GET /jobs/<id>
  - returns status: pending|running|done|failed
- GET /jobs/<id>/result
  - returns result only if done

Exercises:
1) Start server and create a job
2) Poll status until done
3) Fetch result
4) Discuss: where is "session"? what is "state"? (resource state, not transport session)

Run:
- python -m venv .venv
- source .venv/bin/activate
- pip install flask requests
- python server.py
- python client.py
