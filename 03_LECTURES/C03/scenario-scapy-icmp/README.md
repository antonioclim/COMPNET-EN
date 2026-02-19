### Scenario: Scapy – ICMP echo (requires root/admin)

#### Requirements
- Linux (recommended)
- Scapy installed: `pip install scapy`
- Run with elevated privileges (root/admin): `sudo`

#### Running
- sudo python3 icmp-ping.py 1.1.1.1

#### Observations
- You construct an IP/ICMP packet at the application layer
- You receive a reply (or a timeout)
