### Introducere

În această etapă vom utiliza **Wireshark** pentru a capta și analiza traficul generat de conexiunile create cu `netcat`. Scopul este să înțelegem cum arată traficul TCP și UDP la nivel de pachete, precum și modul în care folosim cele două tipuri de filtre din Wireshark:

* **PCAP (capture) filters** – se aplică *înainte* de captură și limitează ce pachete sunt înregistrate.
* **Vizualization (display) filters** – se aplică *după* captură și ne ajută să filtrăm pachetele afișate.

---

### Capturarea traficului pentru un server TCP netcat

#### 1. Porniți Wireshark și selectați interfața rețelei

Alegeți interfața prin care va trece traficul (de ex. `eth0`, `wlan0`).

#### 2. Configurați un **capture filter** pentru a capta doar traficul către portul TCP 9200

În câmpul *Capture Filter* introduceți:

```
tcp port 9200
```

Apoi începeți captura.

#### 3. Porniți serverul TCP netcat pe portul 9200

```
nc -l -p 9200
```

#### 4. Conectați clientul la server

```
nc 127.0.0.1 9200
```

Trimiteți câteva mesaje și observați pachetele în Wireshark.

---

### Analiza traficului în Wireshark

Observați:

* secvența TCP (SYN → SYN-ACK → ACK),
* pachetele ce conțin payload,
* eventualele retransmisii dacă întrerupeți conexiunea.

După captură, aplicați un **display filter**:

```
tcp.stream eq 0
```

Acesta izolează conversația TCP specifică.

---

### Capturarea traficului pentru UDP netcat

#### 1. Configurați un **capture filter** pentru portul UDP 9201

```
udp port 9201
```

Pornirea capturii va înregistra doar pachetele UDP relevante.

#### 2. Server UDP netcat

```
nc -u -l -p 9201
```

#### 3. Trimiterea unui mesaj UDP

```
echo "UDP test" | nc -u 127.0.0.1 9201
```

Observați în Wireshark că:

* nu există handshake,
* nu există stream-uri TCP,
* fiecare mesaj este un pachet independent.

După captură aplicați un display filter:

```
udp.port == 9201
```

---

### Observații

Notă că:

* **Capture filters** sunt restricții pentru Wireshark la nivelul libpcap; nu pot fi modificate după începerea capturii.
* **Display filters** pot fi schimbate oricând și permit explorarea în profunzime a conversațiilor capturate.
* Traficul TCP are stare (handshake, acknowledgements, seq/ack numbers).
* Traficul UDP apare ca pachete individuale, fără stabilirea unei conexiuni.
