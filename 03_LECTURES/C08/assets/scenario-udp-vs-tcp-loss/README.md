### Scenario: UDP vs TCP under packet loss using Mininet (TCLink)

### Objective
- UDP: some messages are lost (best-effort)
- TCP: the application sees the complete stream (retransmissions are transparent)

### Requirements
- Linux
- Mininet (sudo)
- python3

### Topology
h1 --- s1 --- h2
The h1-s1 and/or s1-h2 link has artificial loss (e.g. 20%)

### How to run
- `bash run.sh 20` (the script invokes the system Python with sudo)

The script:
- starts Mininet with the topology and loss
- runs UDP receiver on h2, UDP sender on h1
- runs TCP receiver on h2, TCP sender on h1
- displays results in the terminal

### What to observe
- UDP: the receiver reports missing messages
- TCP: the receiver reports the full line count

### Useful parameters
Set loss using `bash run.sh 5`, `bash run.sh 10` or `bash run.sh 20`. The runner now imports `build` from `topo.py`; optional link-delay changes belong in that function. Loss is applied separately on both links, so it is not a single end-to-end loss percentage. The UDP sender and receiver agree on sequence 0–199; missing packets at either edge are included.

## Files

| Name | Lines |
|------|-------|
| `run.sh` | 42 |
| `tcp_receiver.py` | 29 |
| `tcp_sender.py` | 20 |
| `topo.py` | 33 |
| `udp_receiver.py` | 45 |
| `udp_sender.py` | 16 |

## Cross-References

Parent lecture: [`C08/ — Transport Layer (TCP, UDP, TLS, QUIC)`](../../)
  
Lecture slides: [`c8-transport-layer.md`](../../c8-transport-layer.md)
  
Quiz: [`W08`](../../../../00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W08_Questions.md)

## Selective Clone

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set 03_LECTURES/C08/assets/scenario-udp-vs-tcp-loss
```

**Method B — Direct download**

Browse at: `https://github.com/antonioclim/COMPNET-EN/tree/main/03_LECTURES/C08/assets/scenario-udp-vs-tcp-loss`
