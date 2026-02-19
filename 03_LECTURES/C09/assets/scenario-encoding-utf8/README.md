### Scenario: Encoding pitfall (UTF-8 vs header charset)

### Objective
- Demonstrate that text rendering depends on the declared charset
- Show a typical error: body encoded as UTF-8, but the header declares a different charset

### Requirements
- python3
- curl

### How to run
- ./run.sh

### Tests with curl
1) Correct response (UTF-8 declared properly)
- curl -i http://127.0.0.1:8090/ok

2) Incorrect response (body is UTF-8, header declares ISO-8859-1)
- curl -i http://127.0.0.1:8090/bad

3) Inspect the raw bytes (optional)
- curl -s http://127.0.0.1:8090/ok | xxd | head
- curl -s http://127.0.0.1:8090/bad | xxd | head

### What to observe
- The body is identical (UTF-8)
- Only the charset in the header differs
- A browser might render the characters incorrectly for the /bad endpoint
