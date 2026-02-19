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
- sudo ./run.sh

The script:
- starts Mininet with the topology and loss
- runs UDP receiver on h2, UDP sender on h1
- runs TCP receiver on h2, TCP sender on h1
- displays results in the terminal

### What to observe
- UDP: the receiver reports missing messages
- TCP: the receiver reports the full line count

### Useful parameters
In topo.py you can modify:
- loss (e.g. 5, 10, 20)
- delay (optional)
