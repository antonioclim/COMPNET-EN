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

## Files

| Name | Lines |
|------|-------|
| `client.py` | 27 |
| `server.py` | 30 |

## Cross-References

Parent lecture: [`C03/ — Network Programming (Sockets)`](../../)
  
Lecture slides: [`c3-intro-network-programming.md`](../../c3-intro-network-programming.md)
  
Quiz: [`W03`](../../../../00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W03_Questions.md)

## Selective Clone

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set 03_LECTURES/C03/assets/scenario-tcp-framing
```

**Method B — Direct download**

Browse at: `https://github.com/antonioclim/COMPNET-EN/tree/main/03_LECTURES/C03/assets/scenario-tcp-framing`
