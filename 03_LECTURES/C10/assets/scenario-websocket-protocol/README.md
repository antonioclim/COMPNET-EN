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

## Files

| Name | Lines |
|------|-------|
| `index.html` | 65 |
| `protocol.md` | 28 |
| `server.py` | 102 |

## Cross-References

Parent lecture: [`C10/ — HTTP(S), REST and WebSockets`](../../)
  
Lecture slides: [`c10-http-application-layer.md`](../../c10-http-application-layer.md)
  
Quiz: [`W10`](../../../../00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W10_Questions.md)

## Selective Clone

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set 03_LECTURES/C10/assets/scenario-websocket-protocol
```

**Method B — Direct download**

Browse at: `https://github.com/antonioclim/COMPNET-EN/tree/main/03_LECTURES/C10/assets/scenario-websocket-protocol`
