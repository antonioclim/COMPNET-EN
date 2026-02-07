### Nivelul fizic si nivelul legatura de date

---

### Obiective
La finalul cursului, studentul poate:
- Descrie rolul nivelului fizic si limitarile lui
- Enumera tipuri de medii de transmisie si proprietati relevante
- Explica pe scurt codarea pe linie (NRZ, NRZI, Manchester) si de ce exista
- Intelege ideea de modulatie (ASK, FSK, PSK, QAM) la nivel conceptual
- Explica rolul LLC si MAC si structura unui cadru (frame)
- Intelege Ethernet: adrese MAC, format cadru, coliziuni, CSMA/CD
- Intelege WiFi la nivel 2: canale, tipuri de cadre, CSMA/CA, moduri placa
- Intelege rolul switch-ului: CAM learning, flooding, aging
- Explica VLAN si de ce reduce domeniul de broadcast

---

### Unde suntem in stiva
- Nivel fizic: semnal si biti
- Nivel legatura: cadre, MAC, acces la mediu

[FIG] c4-assets/fig-l1-l2-context.png

---

### Nivelul fizic: rol
- Transferul fizic al bitilor pe mediu
- Defineste semnalul: electric, optic, radio
- Defineste parametrii: rate, sincronizare, conectori, distante

---

### Medii de transmisie (grosier)
- Ghidate:
  - cupru: coaxial, torsadat (UTP/STP)
  - fibra optica: single-mode, multi-mode
- Neghidate:
  - radio: WiFi, LTE, etc

[FIG] c4-assets/fig-transfer-media.png

---

### Proprietati relevante ale mediului
- atenuare (scade amplitudinea)
- zgomot (interferente)
- latime de banda (Hz) vs bitrate (biti/s)
- diafonie (cupru), reflexii (impedanta)
- distanta maxima practica

---

### Codare pe linie (line coding): de ce?
- vrem sincronizare si tranzitii
- vrem sa evitam componenta DC prelungita
- vrem detectie de erori simple (uneori)
- exemple: NRZ, NRZI, Manchester

[FIG] c4-assets/fig-line-coding-overview.png

[SCENARIO] c4-assets/scenario-line-coding/

---

### NRZ (concept)
- 1 si 0 sunt nivele constante
- problema: secvente lungi fara tranzitii -> sincronizare dificila

---

### NRZI (concept)
- 1 produce tranzitie, 0 nu (sau invers, dupa conventie)
- imbunatateste sincronizarea pentru anumite date

---

### Manchester (concept)
- tranzitie in mijlocul bitului
- sincronizare buna, dar rata semnalului creste (cost in banda)

---

### Modulatie (concept)
- variem o purtatoare:
  - ASK: amplitudine
  - FSK: frecventa
  - PSK: faza
  - QAM: combinatie amplitudine + faza

[FIG] c4-assets/fig-modulation.png

---

### De la semnal la cadru
- L1 livreaza un flux de biti
- L2 construieste cadre: delimitare, adresare, CRC

---

### Limitarile nivelului fizic (tranzitie catre L2)
- Nivelul fizic nu poate comunica direct cu software
- Nivelul fizic nu suporta adresare
- Gestioneaza fluxuri simple de biti
- Nivelul legatura de date:
  - permite adresare
  - unitate structurata: cadru (frame)
  - servicii de acces la mediu pentru straturile superioare

---

### Structura nivelului de legatura de date
- Doua subniveluri:
  - LLC (Logical Link Control): interfata spre software
  - MAC (Media Access Control): interfata spre hardware

[FIG] c4-assets/fig-llc-mac.png

---

### LLC
- IEEE 802.2
- independent de mediul fizic
- control flux (unde e cazul)
- multiplexare pentru protocoale superioare

---

### MAC
- control acces la mediu
- construieste cadrele efective
- dependenta de tehnologie (Ethernet vs WiFi)

---

### Functii MAC
- delimitare cadre
- adresare sursa/destinatie (MAC)
- transfer transparent al PDU-urilor LLC
- detectie erori (CRC)
- control acces la mediu

---

### Incapsulare la nivel 2
- impachetarea datelor in cadru (frame)
- formatul depinde de tehnologie, dar campurile sunt similare

[FIG] c4-assets/fig-l2-encapsulation.png

---

### Campuri tipice intr-un cadru
- start cadru (preambul / delimitator)
- adrese MAC sursa si destinatie
- tip/lungime
- date (payload)
- CRC / FCS

---

### Ethernet
- cel mai raspandit nivel 2 (IEEE 802.3)
- mediu: cupru (istoric coaxial, apoi torsadat), si fibra in multe scenarii
- variante: 10BaseT, 100BaseT, 1000BaseT etc

---

### Formatul cadrului Ethernet
[FIG] c4-assets/fig-ethernet-frame.png

---

### Adrese MAC (48 biti)
- OUI (24 biti) + identificator interfata (24 biti)
- broadcast local: FF:FF:FF:FF:FF:FF
- adrese local-administered: bit specific setat in primul octet

[SCENARIO] c4-assets/scenario-mac-arp-ethernet/

---

### Coliziuni in Ethernet (istoric si concept)
- apar cand doua noduri transmit simultan pe acelasi mediu partajat
- CSMA/CD: asculta mediul, detecteaza coliziuni, backoff
- in full-duplex cu switch: coliziunile dispar practic

[FIG] c4-assets/fig-csma-cd.png

---

### Alte probleme la nivel 2 (Ethernet)
- switching loops -> broadcast storms (nu exista TTL la L2)
- jabber (cadre prea mari)
- runt frames (cadre prea mici)

---

### WiFi (IEEE 802.11)
- mediu: aer (unde radio)
- benzi uzuale: 2.4 GHz, 5 GHz
- canale: pot fi suprapuse sau ne-suprapuse

[FIG] c4-assets/fig-wifi-channels-24ghz.png

---

### Cadre WiFi (tipuri)
- control
- management
- date

---

### Structura cadrului WiFi (concept)
- control: versiune, tip, subtip
- ToDS/FromDS
- 4 adrese (in functie de scenariu)
- FCS la final

[FIG] c4-assets/fig-wifi-frame-concept.png

---

### Coliziuni in WiFi si CSMA/CA
- coliziuni exista frecvent (mediul e partajat)
- CSMA/CA: asculta, asteapta random, optional RTS/CTS, apoi asteapta confirmare

[FIG] c4-assets/fig-csma-ca.png

---

### Moduri de functionare ale placilor WiFi
- managed (client)
- AP (access point)
- AP cu VLAN tagging (AP-tag)
- WiFi P2P
- monitor (sniffing la nivel 2)

---

### Autentificare in WiFi (high level)
- WEP (depasit)
- WPA (depasit)
- WPA2 (foarte raspandit)
- WPA3 (adoptie)

---

### Switch-uri: repetor vs bridge vs switch
- repetor: amplifica semnalul
- bridge: filtreaza minim, decizii simple
- switch: comutare pe baza de MAC (circuite virtuale)

---

### CAM (MAC learning)
- tabela: MAC -> port
- invata din sursa cadrelor
- daca nu stie destinatia: flooding pe toate porturile

[FIG] c4-assets/fig-switch-cam-learning.png

---

### CAM aging
- intrarile expira daca nu sunt folosite
- previne asocierea gresita dupa mutarea unui host

---

### VLAN
- imparte o retea fizica in retele logice
- fiecare VLAN = domeniu de broadcast distinct
- tagging (802.1Q) pe trunk

[FIG] c4-assets/fig-vlan.png

---

### Recapitulare
- L1: mediu, semnal, codare, modulatie
- L2: cadre, MAC/LLC, CRC, acces la mediu
- Ethernet vs WiFi: CSMA/CD vs CSMA/CA
- Switch: CAM learning + flooding + aging
- VLAN: segmentare si broadcast domain

---

### Pregatire pentru Curs 5
- Nivelul retea: IP, adresare, subnetting
- Diferenta: MAC (flat) vs IP (ierarhic)
