### Minimal WS protocol (JSON messages)

All messages are JSON objects.

Client -> Server:
- join
  { "type": "join", "room": "networks", "name": "alice" }

- msg
  { "type": "msg", "room": "networks", "text": "hello" }

Server -> Client:
- joined
  { "type": "joined", "room": "networks", "you": "alice" }

- deliver
  { "type": "deliver", "room": "networks", "from": "alice", "text": "hello", "id": 42 }

- ack
  { "type": "ack", "id": 42 }

- error
  { "type": "error", "message": "..." }

Rules:
- Client must join before sending msg
- Server assigns increasing integer ids per room (monotonic)
- Server sends ack after delivering
