### Scenario: TCP framing (stream → messages)

#### Objective
Demonstrate that TCP is a byte stream; messages must be delimited at the application layer.

Delimiter used: newline (\n)

Port: 9100

#### Running
Terminal 1:
- python3 server.py

Terminal 2:
- python3 client.py

#### Observations
- The server reads chunks and reconstructs messages based on the newline delimiter
- If messages are sent in rapid succession, several may arrive concatenated in a single recv() call
