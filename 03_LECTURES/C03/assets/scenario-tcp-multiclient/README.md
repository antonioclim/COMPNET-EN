### Scenario: concurrent TCP server (one thread per client)

Port: 9200

#### Running
Terminal 1:
- python3 server.py

Terminals 2, 3, 4 (start 2–3 instances):
- python3 client.py

#### Observe
- The server processes clients concurrently
- Each client receives its own response

## Files

| Name | Lines |
|------|-------|
| `client.py` | 17 |
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
git sparse-checkout set 03_LECTURES/C03/assets/scenario-tcp-multiclient
```

**Method B — Direct download**

Browse at: `https://github.com/antonioclim/COMPNET-EN/tree/main/03_LECTURES/C03/assets/scenario-tcp-multiclient`
