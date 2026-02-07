### Seminar 7 – Interceptarea pachetelor TCP si UDP

In acest seminar vom lucra cu:
- socket-uri RAW pentru a intercepta pachete la nivel IP
- filtre de pachete implementate in Python
- un mini port-scanner
- un script simplu de detectare a scanarilor de porturi

Scopul este sa intelegeti cum arata pachetele TCP/UDP la nivel jos si cum puteti construi unelte similare, la nivel de baza, cu tcpdump sau Wireshark.

---

### Ce inseamna interceptarea pachetelor

Cand rulati un sniffer de pachete pe masina voastra:

- deschideti un socket special (RAW) care poate primi pachete IP brute
- sistemul de operare livreaza aplicatiei voastre copii ale pachetelor care trec prin interfata de retea
- puteti inspecta header-ele IP, TCP, UDP, ICMP etc.

Diferenta fata de socket-urile obisnuite (TCP/UDP):

- un socket TCP vede doar fluxul de date pentru conexiunea lui (stream)
- un socket UDP vede doar datagramele pentru portul lui
- un socket RAW vede pachete brute pentru mai multe conexiuni, eventual pentru toate

In mod normal, pentru socket-uri RAW este nevoie de privilegii ridicate (root).

---

### Mod promiscuous si capturi la nivel de retea

In mod normal, o interfata de retea accepta doar pachete adresate catre ea.

In mod promiscuous:
- placa de retea accepta toate pachetele care trec prin mediu
- soferul de retea le livreaza catre stack-ul de retea al sistemului
- un sniffer (tcpdump, Wireshark) le poate vedea pe toate

In laboratorul nostru:
- ne concentram pe capturi locale, pe masina de laborator sau pe hosturi Mininet
- nu incercam sa interceptam trafic al altora in productie
- exercitiile sunt strict educationale

---

### Cum fac tcpdump si Wireshark capturi

Tcpdump si Wireshark:
- folosesc de obicei libpcap pentru capturi eficiente in kernel
- pot aplica filtre BPF (Berkeley Packet Filter) direct in kernel, pentru performanta
- decodeaza protocoale complexe (HTTP, DNS, TLS etc.)

In acest seminar:
- vom implementa variante simplificate, in Python
- vom lucra direct cu socket-uri RAW si vom decoda manual header-ele de baza:
  - IP (IPv4)
  - TCP
  - UDP

Nu vom ajunge la nivelul de detaliu al Wireshark, dar vom intelege structura de baza a pachetelor.

---

### De ce avem nevoie de aceste cunostinte

Aceste cunostinte sunt utile pentru:

- debug de retea low-level (cand ping si traceroute nu sunt suficiente)
- intelegerea functionarii firewall-urilor si a sistemelor IDS/IPS
- analiza traficului pentru securitate (detectarea scanarilor de porturi)
- intelegerea practica a header-elor si a campurilor din protocoalele de retea

In restul seminarului veti:
- scrie un sniffer simplu (cu template dat)
- adauga un filtru de pachete
- implementa un mini port-scanner
- implementa un mini detector de scanare

Urmatorul fisier va contine primul template de cod pentru un sniffer simplu.
