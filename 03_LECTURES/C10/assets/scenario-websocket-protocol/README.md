### Scenario: WebSocket and a minimal custom protocol

Aim:
- Observe the WebSocket upgrade handshake (HTTP to WS)
- Implement a minimal application protocol on top of WS frames:
  - join a room
  - message
  - acknowledgement (ack)
  - error

Core lesson:
- WebSocket provides framing and bidirectional transport
- Semantics such as ordering, acknowledgements and room membership are application protocol responsibilities

Run:
- python -m venv .venv
- source .venv/bin/activate
- pip install flask flask-sock
- python server.py
- open http://127.0.0.1:9000 in two tabs

Exercises:
1) Join a room and send messages
2) Observe acknowledgement ids increasing
3) Implement a client-side rule: ignore messages from other rooms
4) Discuss what TCP already guarantees and what this protocol adds
