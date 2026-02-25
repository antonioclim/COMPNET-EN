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

## Files

| Name | Lines |
|------|-------|
| `client.py` | 25 |
| `server.py` | 44 |

## Cross-References

Parent lecture: [`C03/ — Network Programming (Sockets)`](../../)
  
Lecture slides: [`c3-intro-network-programming.md`](../../c3-intro-network-programming.md)
  
Quiz: [`W03`](../../../../00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W03_Questions.md)

## Selective Clone

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set 03_LECTURES/C03/assets/scenario-udp-session-ack
```

**Method B — Direct download**

Browse at: `https://github.com/antonioclim/COMPNET-EN/tree/main/03_LECTURES/C03/assets/scenario-udp-session-ack`
