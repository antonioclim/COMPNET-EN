### Scenariu: NAT (masquerade) in Linux cu namespaces

#### Cerinte
- Linux
- root (sudo)
- iproute2 (ip), iptables sau nftables
- nu necesita internet real: putem demonstra SNAT catre un "uplink" namespace

#### Ce demonstreaza
- host privat -> router -> uplink
- SNAT (masquerade) pe router
- observi schimbarea adresei sursa cu tcpdump

#### Rulare
- sudo bash nat_demo.sh

#### Curatare
Scriptul curata la final namespaces si link-urile.
