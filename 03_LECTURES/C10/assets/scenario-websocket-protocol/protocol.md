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

## Acknowledgement and validation rules

Each input must be a JSON object. `join.room`, `join.name` and `msg.text` must
be non-empty strings; messages must name the room joined by that connection.
Invalid messages receive an `error` response and the connection can continue.

An `ack` confirms that the server accepted the message and assigned its room ID.
It does not confirm that every recipient received or displayed it. A recipient
that disconnects during a broadcast is removed; other recipients and the sender
continue. IDs are allocated atomically per room. With concurrent senders, clients
must not assume that arrival order is always ID order; applications requiring
ordered display need buffering or a serial per-room delivery queue.
