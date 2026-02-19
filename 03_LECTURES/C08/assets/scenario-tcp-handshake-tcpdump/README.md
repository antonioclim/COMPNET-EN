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
