### Scenario: ARP capture

Wireshark filter:
- arp

tcpdump:
- sudo tcpdump -i any -n arp

Generate ARP:
- ping the local gateway (e.g. 192.168.1.1)

Observe:
- request broadcast
- reply unicast
