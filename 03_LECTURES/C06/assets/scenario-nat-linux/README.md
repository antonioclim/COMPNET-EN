### Scenario: NAT (masquerade) on Linux with namespaces

#### Requirements
- Linux
- root privileges (sudo)
- iproute2 (ip), iptables or nftables
- external internet access is not required: the script demonstrates SNAT towards an isolated uplink namespace

#### Demonstrates
- private host -> router -> uplink
- SNAT (masquerade) on the router
- source address rewriting observed with tcpdump

#### Running
- sudo bash nat-demo.sh

#### Cleanup
The script removes namespaces and links on exit.
