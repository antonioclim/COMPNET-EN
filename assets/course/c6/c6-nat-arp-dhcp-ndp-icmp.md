### Nivelul rețea: mecanisme de alocare și suport
### NAT/PAT, ARP, DHCP/BOOTP, NDP, ICMP

---

### Obiective
La finalul cursului, studentul poate:
- Explica de ce IPv4 a dus la NAT/PAT și ce compromisuri introduce
- Distinge între NAT static, NAT dinamic și PAT (NAT overload)
- Înțelege la nivel conceptual cum funcționează tabela NAT
- Explica ARP și proxy ARP (IPv4) și echivalentul IPv6 prin NDP
- Explica pașii DHCP (DORA) și rolul DHCP Relay
- Explica rolul ICMP (ping/traceroute, mesaje de eroare)
- Înțelege rolul ICMPv6 în NDP

---

### Context: de ce e nevoie de aceste mecanisme?
- Adresare L3 (IPv4/IPv6) e globală/rutabilă
- În practică trebuie:
  - alocare automată (DHCP/NDP)
  - mapare IP<->MAC (ARP/NDP)
  - suport pentru diagnostic și control (ICMP)
  - compatibilitate cu lipsa adreselor IPv4 (NAT/PAT)

[FIG] c6-assets/fig-l3-support-map.png

---

### Epuizarea adreselor IPv4
- Problema majoră a IPv4: spațiu mic de adrese
- Soluții în timp:
  - adrese private reutilizabile (RFC1918)
  - NAT/PAT
  - tranziție IPv6 (lentă, dar continuă)

---

### Adrese private reutilizabile (RFC1918)
- 10.0.0.0/8
- 172.16.0.0/12
- 192.168.0.0/16
Notă: nu sunt rutabile global; trebuie traduse/încapsulate pentru Internet.

---

### Translatarea adreselor (NAT)
- În mod normal, ruterul forwardează fără să schimbe IP-urile
- NAT: modifică adresa sursă și/sau destinație
- Necesită mapare bidirecțională pentru a primi răspuns

[FIG] c6-assets/fig-nat-basic.png

---

### Tabela NAT (concept)
- Ruterul păstrează corespondențe intern <-> extern
- Statică (config) sau dinamică (pe trafic)
- Exemplu simplu:
  - 192.168.0.1 -> 166.14.133.3

---

### Tipuri de translatare
- NAT static (1:1)
- NAT dinamic (pool de adrese publice)
- PAT / NAT overload (mulți -> 1 public, diferențiere prin port)

---

### NAT static (1:1)
- Problemă: server intern privat trebuie accesibil din exterior
- Soluție: mapare fixă între IP privat și IP public

[FIG] c6-assets/fig-nat-static.png

---

### NAT dinamic (pool)
- Problemă: multe stații, puține IP-uri publice
- Soluție: pool de IP-uri publice alocate temporar (lease pe mapare)

[FIG] c6-assets/fig-nat-dynamic.png

---

### PAT (Port Address Translation)
- Problemă: multe stații, o singură adresă publică
- Soluție: mapare per-flux folosind porturi pe ruter

Exemplu tabelă:
- 192.168.0.1:80 -> 166.14.133.3:62101
- 192.168.0.2:80 -> 166.14.133.3:63105

[FIG] c6-assets/fig-pat.png

[SCENARIO] c6-assets/scenario-nat-linux/

---

### Dezavantaje NAT/PAT
- În PAT, conexiunile din Internet către interior sunt dificil de inițiat (fără port forwarding)
- Încălcarea ideii end-to-end
- Dependență de L4 (porturi) pentru o problemă de L3
- Probleme cu unele protocoale și cu UDP (mai ales fără keepalive)
- Îngreunează tuneluri / VPN / aplicații P2P

---

### ARP (IPv4) și de ce există
- În Ethernet trebuie MAC destinație pentru a trimite un cadru
- ARP: IP -> MAC în rețeaua locală
- ARP request: broadcast
- ARP reply: unicast

[FIG] c6-assets/fig-arp.png

[SCENARIO] c6-assets/scenario-arp-capture/

---

### Proxy ARP (concept)
- Dacă IP-ul căutat e în altă rețea
- Ruterul poate răspunde cu MAC-ul lui (în locul destinației reale)

[FIG] c6-assets/fig-proxy-arp.png

---

### BOOTP (istoric)
- Configurare IP prin server
- Nu suportă alocare dinamică reală
- DHCP este extensia practică; DHCP poate suporta clienți BOOTP (în general)

---

### DHCP: rol
- Alocare automată IP + parametri:
  - mască
  - default gateway
  - DNS
  - lease time

[FIG] c6-assets/fig-dhcp-dora.png

[SCENARIO] c6-assets/scenario-dhcp-capture/

---

### DHCP DORA (pași)
- Discover: client broadcast (UDP)
- Offer: server oferă IP + parametri
- Request: client acceptă (broadcast ca să notifice și alte servere)
- Acknowledge: server confirmă lease

---

### DHCP Relay
- Discover e broadcast (nu trece prin rutare)
- Relay pe ruter: transformă cererea și o trimite către serverul DHCP din altă rețea

[FIG] c6-assets/fig-dhcp-relay.png

---

### NDP (IPv6)
- În IPv6, multe roluri care în IPv4 sunt separate:
  - descoperire vecini (echivalent ARP)
  - descoperire router (gateway)
  - prefix discovery
  - DAD (duplicate address detection)
- Folosește ICMPv6

[FIG] c6-assets/fig-ndp.png

[SCENARIO] c6-assets/scenario-ndp-capture/

---

### Neighbor Solicitation / Advertisement
- NS: solicitare către multicast (în loc de broadcast)
- NA: răspuns (sau anunț nesolicitat)

---

### Autoconfigurare IPv6
- Stateless (SLAAC):
  - link-local + DAD
  - prefix din RA
  - adresa globală rezultă din prefix + interface ID (sau token random)
- Stateful:
  - DHCPv6 pentru parametri suplimentari (DNS etc), uneori și pentru adresă

---

### ICMP: de ce există
- Rețelele produc erori și au nevoie de feedback
- ICMP:
  - mesaje de control și eroare
  - ping / traceroute (instrumente construite peste ICMP)

[FIG] c6-assets/fig-icmp-role.png

[SCENARIO] c6-assets/scenario-icmp-traceroute/

---

### ICMPv6
- rol similar ICMP
- utilizat intens de NDP (de aceea filtrarea ICMPv6 “la grămadă” rupe IPv6)

---

### Recapitulare
- NAT/PAT: soluție practică pentru IPv4, cu compromisuri
- ARP: IP->MAC (IPv4)
- DHCP: configurare automată (IPv4)
- NDP: ARP + router/prefix discovery (IPv6)
- ICMP/ICMPv6: diagnostic + control

---

### Pregătire pentru Curs 7
- Rutare: RIP, OSPF (și ce înseamnă “tabele de rutare” în practică)
