### Scenario: concurrent TCP server (one thread per client)

Port: 9200

#### Running
Terminal 1:
- python3 server.py

Terminals 2, 3, 4 (start 2–3 instances):
- python3 client.py

#### Observe
- The server processes clients concurrently
- Each client receives its own response
