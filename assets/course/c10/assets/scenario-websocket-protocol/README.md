### Scenario: WebSockets + minimal custom protocol

Goal:
- Observe WebSocket upgrade handshake (HTTP -> WS)
- Implement a minimal application protocol on top of WS frames:
  - join room
  - message
  - ack
  - error

Core lesson:
- WebSocket gives framing + bidirectional transport
- Semantics (ordering, ack, room membership) are application protocol responsibilities

Run:
- python -m venv .venv
- source .venv/bin/activate
- pip install flask flask-sock
- python server.py
- open http://127.0.0.1:9000 in two tabs

Exercises:
1) Join a room and send messages
2) Observe ack ids increasing
3) Implement a client-side rule: ignore messages from other rooms
4) Discuss: what guarantees does TCP already give and what this protocol adds
