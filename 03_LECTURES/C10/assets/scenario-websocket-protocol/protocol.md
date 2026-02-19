### Minimal WebSocket protocol (JSON messages)

Each message is a JSON object.

Client -> server:
- join
  { "type": "join", "room": "networks", "name": "alice" }

- msg
  { "type": "msg", "room": "networks", "text": "hello" }

Server -> client:
- joined
  { "type": "joined", "room": "networks", "you": "alice" }

- deliver
  { "type": "deliver", "room": "networks", "from": "alice", "text": "hello", "id": 42 }

- ack
  { "type": "ack", "id": 42 }

- error
  { "type": "error", "message": "..." }

Rules:
- The client must join before sending `msg`
- The server assigns increasing integer ids per room (monotonic)
- The server sends `ack` after delivering
