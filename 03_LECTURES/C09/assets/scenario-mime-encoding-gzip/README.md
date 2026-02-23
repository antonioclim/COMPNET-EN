### Scenario: MIME, charset and gzip inspection

### Objective
- Observe Content-Type (MIME) and charset
- Observe Content-Encoding (gzip)
- Compare a compressed response with an uncompressed one

### Requirements
- python3
- curl

### How to run
1) Start the server
- ./run.sh

2) In another terminal, test with curl

A) HTML (without gzip)
- curl -i http://127.0.0.1:8089/

B) JSON (without gzip)
- curl -i http://127.0.0.1:8089/data.json

C) With gzip (client announces gzip support)
- curl -i -H "Accept-Encoding: gzip" http://127.0.0.1:8089/
- curl -i -H "Accept-Encoding: gzip" http://127.0.0.1:8089/data.json

D) Download the compressed body to inspect the raw bytes
- curl -H "Accept-Encoding: gzip" -o out.gz http://127.0.0.1:8089/data.json
- file out.gz

### What to observe
- Content-Type: text/html; charset=utf-8
- Content-Type: application/json; charset=utf-8
- When Accept-Encoding includes gzip:
  - the server responds with Content-Encoding: gzip
