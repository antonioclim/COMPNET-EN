### Scenario: TCP handshake and teardown observed with tcpdump

### Objective
- Observe the capture: SYN, SYN-ACK, ACK (3-way handshake)
- Observe the graceful closure: FIN/ACK/FIN/ACK
- Note the client port (ephemeral) vs the server port (fixed)

### Requirements
- Linux
- python3
- tcpdump (requires sudo or cap_net_raw/cap_net_admin)
- optional: tshark/wireshark for easier inspection

### How to run
1. Terminal 1: run the scenario (capture + client/server)
   - ./run.sh

2. After execution, the capture file is:
   - capture.pcap

### What to look for in the capture
- Useful Wireshark filters:
  - tcp.port == 9090
  - tcp.flags.syn == 1
  - tcp.flags.fin == 1
- Observe:
  - SYN: client -> server (dst port 9090)
  - SYN,ACK: server -> client (src port 9090)
  - FIN appears at closure

### Cleanup
- ./cleanup.sh

## Files

| Name | Lines |
|------|-------|
| `cleanup.sh` | 17 |
| `client.py` | 20 |
| `run.sh` | 39 |
| `server.py` | 29 |

## Cross-References

Parent lecture: [`C08/ — Transport Layer (TCP, UDP, TLS, QUIC)`](../../)
  
Lecture slides: [`c8-transport-layer.md`](../../c8-transport-layer.md)
  
Quiz: [`W08`](../../../../00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W08_Questions.md)

## Selective Clone

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set 03_LECTURES/C08/assets/scenario-tcp-handshake-tcpdump
```

**Method B — Direct download**

Browse at: `https://github.com/antonioclim/COMPNET-EN/tree/main/03_LECTURES/C08/assets/scenario-tcp-handshake-tcpdump`
