### Scenario: UDP with minimal state (token) + acknowledgement (ACK)

Idea:
- Client sends "HELLO"
- Server responds with "TOKEN:<id>"
- Client sends "MSG:<token>:<text>"
- Server responds with "ACK:<token>:<seq>"

Port: 9300

#### Running
Terminal 1:
- python3 server.py

Terminal 2:
- python3 client.py

#### Observations
- With UDP, session state and acknowledgements are handled at the application layer
