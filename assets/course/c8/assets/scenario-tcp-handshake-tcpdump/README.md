### Scenario: TCP handshake si teardown observate cu tcpdump

### Obiectiv
- Sa vezi in captura: SYN, SYN-ACK, ACK (3-way handshake)
- Sa vezi inchiderea controlata: FIN/ACK/FIN/ACK
- Sa observi portul client (ephemeral) vs portul server (fix)

### Cerinte
- Linux
- python3
- tcpdump (necesita sudo sau cap_net_raw/cap_net_admin)
- optional: tshark/wireshark pentru inspectie mai usoara

### Cum rulezi
1. Terminal 1: ruleaza scenariul (captura + client/server)
   - ./run.sh

2. Dupa rulare, fisierul captura este:
   - capture.pcap

### Ce cauti in captura
- Filtre utile in Wireshark:
  - tcp.port == 9090
  - tcp.flags.syn == 1
  - tcp.flags.fin == 1
- Observa:
  - SYN: client -> server (dst port 9090)
  - SYN,ACK: server -> client (src port 9090)
  - FIN apare la inchidere

### Curatare
- ./cleanup.sh
