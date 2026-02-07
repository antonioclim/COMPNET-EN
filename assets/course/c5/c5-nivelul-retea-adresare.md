### Nivelul rețea
### IP, IPv4/IPv6, CIDR, Subnetting, VLSM

---

### Obiective
La finalul cursului, studentul poate:
- Explica rolul nivelului rețea și diferența MAC vs IP
- Identifica tipuri de protocoale la nivel rețea (rutabile vs rutare)
- Explica structura de bază a IPv4 și IPv6 și câmpuri cheie (TTL/Hop Limit, Next Header)
- Lucra cu CIDR (prefix /n) și calcula: rețea, broadcast, interval host
- Face subnetting cu mască fixă (FLSM) și cu mască variabilă (VLSM) în IPv4
- Identifica tipuri de adrese și tipuri de comunicare (unicast, multicast, broadcast/anycast)
- Înțelege noțiuni esențiale IPv6: link-local, global, multicast, prescurtări

---

### Funcțiile nivelului rețea
- Fragmentarea datagramelor (unde e cazul) și reasamblarea la destinație
- Rutarea pachetelor de la sursă la destinație

[FIG] c5-assets/fig-l3-role.png

---

### Tipuri de protocoale de nivel rețea
- Protocoale rutabile
  - transportă date de la niveluri superioare (ex: IP)
- Protocoale de rutare
  - ajută la determinarea rutei (ex: OSPF, RIP) (doar mențiune aici)

---

### De ce IP și nu MAC?
- MAC (nivel 2): semnificație locală (într-un domeniu L2)
- IP (nivel 3): semnificație ierarhică (rețea + host), rutabil global

[FIG] c5-assets/fig-mac-vs-ip.png

---

### IP: ideea de bază
- Protocolul fundamental al Internetului
- Best effort (nu garantează livrare)
- Adrese logice + rutare

---

### Versiuni IP
- IPv4: 32 biți, foarte răspândit
- IPv6: 128 biți, spațiu mare de adrese + simplificări

---

### IPv4 vs IPv6 (comparare rapidă)
| IPv4 | IPv6 |
|---|---|
| 32 biți | 128 biți |
| header variabil + checksum header | header fix (extensii) + fără checksum header |
| broadcast există | broadcast nu există (înlocuit prin multicast) |
| fragmentare posibilă în rețea | fragmentare doar la sursă (prin extensii) |
| NAT des întâlnit în practică | permite din nou end-to-end (în principiu) |

---

### Tipuri de comunicare IPv4
- Unicast: un host -> un host
- Multicast: un host -> grup
- Broadcast: un host -> toate host-urile dintr-un segment

---

### Format pachet IPv4 (câmpuri cheie)
[FIG] c5-assets/fig-ipv4-header.png

---

### IPv4: câmpuri esențiale (partea 1)
- Version (4): 4
- IHL: lungimea header-ului
- DSCP/ECN: QoS și congestion notification (conceptual)
- Total Length: header + date

---

### IPv4: câmpuri esențiale (partea 2)
- Identification + Flags (DF/MF) + Fragment Offset: fragmentare
- TTL: scade la fiecare hop, previne bucle infinite
- Protocol: ce e încapsulat (TCP=6, UDP=17, ICMP=1)

---

### IPv4: câmpuri esențiale (partea 3)
- Header Checksum: doar pentru header
- Source / Destination Address: 32 biți
- Options: rare în practică

---

### Format IPv6 (header fix + extensii)
[FIG] c5-assets/fig-ipv6-header.png

---

### IPv6: câmpuri esențiale
- Version: 6
- Traffic Class + Flow Label
- Payload Length
- Next Header (analog “Protocol”, dar și extensii)
- Hop Limit (analog TTL)
- Source/Destination: 128 biți

---

### Adresare IPv4: rețea + host
- O adresă IPv4 are:
  - partea de rețea (prefix)
  - partea de host
- Masca/prefixul separă cele două părți

[FIG] c5-assets/fig-prefix-mask.png

---

### Clase IPv4 (istoric, pentru context)
- Model vechi, înlocuit de CIDR
- Clase A/B/C, D multicast, E rezervat
Notă: în practică lucrăm cu CIDR, nu cu clase.

---

### CIDR
- Alocare fără clase
- Notație /n = număr biți 1 în mască
- Exemplu: 255.255.0.0 = /16

[SCENARIO] c5-assets/scenario-cidr-basics/

---

### Subnetting IPv4 (FLSM)
- Împărțim o rețea în subrețele egale
- Luăm biți din partea de host și îi mutăm în prefix

[SCENARIO] c5-assets/scenario-subnetting-flsm/

---

### VLSM (IPv4)
- Subrețele cu mărimi diferite, alocate eficient
- Pași tipici:
  1) sortezi cerințele descrescător (hosts)
  2) aloci blocuri de puteri ale lui 2
  3) verifici alinierea la prefix

[SCENARIO] c5-assets/scenario-vlsm/

---

### Adrese speciale IPv4
- 0.0.0.0 (default / “toate interfețele” în bind)
- 255.255.255.255 (broadcast limitat)
- loopback: 127.0.0.0/8 (uzual 127.0.0.1)
- link-local: 169.254.0.0/16
- private: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16

---

### IPv6: reprezentare și prescurtare
- scriere hex, 8 grupuri
- eliminare zerouri la început de grup
- o singură compresie cu :: pentru cea mai lungă secvență de 0

[SCENARIO] c5-assets/scenario-ipv6-shortening/

---

### IPv6: tipuri uzuale de adrese
- loopback: ::1
- global unicast: 2000::/3
- link-local: fe80::/10
- multicast: ff00::/8
- default route: ::/0

---

### Tipuri de comunicare IPv6
- unicast
- multicast
- anycast (aceeași adresă pe mai multe noduri, ajunge la “cel mai apropiat”)

---

### IPv6 scopes (ideea)
- link-local: doar pe link
- unique local: intern (de obicei)
- global: rutabil global
- multicast: scope inclus în adresă (conceptual)

---

### Subnetting în IPv6 (practic)
- primești un prefix (ex: /48)
- aloci subrețele prin extinderea prefixului (frecvent /64 pentru LAN)
- numărul de subrețele din /48 în /64 este 2^(64-48)=65536

---

### IPv6 în URL-uri
- [2001:db8::1]
- cu port: [2001:db8::1]:8080

---

### Recapitulare
- rol L3: adresare + rutare + TTL/Hop Limit
- IPv4: CIDR + subnetting + VLSM
- IPv6: tipuri de adrese + prescurtare + prefixe

---

### Pregătire pentru Curs 6
- NAT/PAT, ICMP, DHCP, BOOTP
- legătura între L2 (ARP) și L3 (IP), apoi L3->L4 (porturi)
