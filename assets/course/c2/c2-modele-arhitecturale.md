### Rețele de calculatoare
### Modele arhitecturale: OSI și TCP/IP

---

### Descriere generală
- De ce avem nevoie de modele arhitecturale
- Rolul straturilor în gestionarea complexității
- Legătura cu protocoalele reale

---

### Obiective
La finalul cursului, studentul poate:
- Explica scopul unui model arhitectural de rețea
- Descrie rolul fiecărui strat din modelul OSI
- Asocia protocoale concrete straturilor OSI și TCP/IP
- Compara modelul OSI cu modelul TCP/IP
- Urmări procesul de încapsulare pe straturi

---

### De ce modele arhitecturale?
- Rețelele sunt sisteme complexe
- Separarea pe straturi:
  - reduce complexitatea
  - permite interoperabilitate
  - permite dezvoltare independentă
- Un strat:
  - oferă servicii stratului superior
  - utilizează servicii de la stratul inferior

---

### Noțiuni-cheie (recapitulare din Curs 1)
- Protocol
- Stivă de protocoale
- Unitate de transfer
- Încapsulare

Acest curs formalizează aceste noțiuni.

---

### Modele istorice de rețea
- Diverse modele proprietare (ex: IPX/SPX)
- Lipsa interoperabilității
- Necesitatea unui model standardizat

---

### Modelul OSI – introducere
- OSI = Open Systems Interconnect
- Creat de ISO (International Organization for Standardization)
- Model teoretic
- Scop: descrierea completă a comunicării în rețea
- Independență față de hardware și sistem de operare

---

### Structura modelului OSI
- Model organizat în 7 straturi
- Granularitate mare
- Fiecare strat are un rol clar definit

[FIG] c2-assets/fig-osi-straturi.png

---

### Stratul 1 – Fizic
Rol:
- Transmiterea biților pe mediul fizic

Unitatea de transfer:
- Bit

Funcții:
- Modulare semnal
- Sincronizare la nivel de bit
- Controlul ratei de transmisie
- Configurarea mediului fizic

Exemple:
- Cablu Ethernet
- Semnal electric / optic / radio

---

### Stratul 2 – Legătură de date
Rol:
- Transfer de cadre între noduri direct conectate

Unitatea de transfer:
- Cadru (frame)

Funcții:
- Adresare fizică (MAC)
- Detectarea erorilor (CRC)
- Controlul fluxului
- Delimitarea cadrelor

Substraturi:
- MAC (Media Access Control)
- LLC (Logical Link Control)

---

### Stratul 3 – Rețea
Rol:
- Livrarea pachetelor între rețele diferite

Unitatea de transfer:
- Pachet

Funcții:
- Adresare logică (ierarhică)
- Rutare
- Fragmentare și reasamblare

Exemple:
- IP

---

### Stratul 4 – Transport
Rol:
- Comunicare proces-la-proces

Unitatea de transfer:
- Segment (TCP) / Datagramă (UDP)

Funcții:
- Porturi
- Controlul fluxului
- Controlul erorilor
- Reordonare
- Confirmări (pentru protocoale orientate pe conexiune)

---

### Stratul 5 – Sesiune
Rol:
- Gestionarea dialogului între aplicații

Funcții:
- Inițiere sesiune
- Menținere sesiune
- Terminare sesiune
- Controlul dialogului (half/full duplex)

Notă:
- Adesea implementat implicit în aplicații moderne

---

### Stratul 6 – Prezentare
Rol:
- Reprezentarea datelor

Funcții:
- Codificare / decodificare
- Conversii de format
- Compresie
- Criptare

Exemple:
- TLS (conceptual)
- UTF-8, JSON, ASN.1

---

### Stratul 7 – Aplicație
Rol:
- Interfața cu utilizatorul sau aplicația

Funcții:
- Transfer fișiere
- Poștă electronică
- Acces resurse la distanță

Exemple:
- HTTP
- FTP
- SMTP
- DNS

---

### Comunicarea între straturile OSI
- Straturile comunică doar cu stratul imediat adiacent
- Comunicare:
  - verticală (în interiorul unui sistem)
  - orizontală (între straturi omoloage)

[FIG] c2-assets/fig-osi-comunicare.png

---

### Încapsulare în modelul OSI
- Datele sunt încapsulate progresiv
- Fiecare strat adaugă propriul antet
- La recepție, procesul este invers

[FIG] c2-assets/fig-osi-incapsulare.png

---

### Localizarea implementării straturilor
- Straturi inferioare: hardware + driver
- Transport: sistem de operare
- Straturi superioare: aplicații

[FIG] c2-assets/fig-osi-implementare.png

---

### Limitele modelului OSI
- Model teoretic
- Implementare rară ca atare
- Unele straturi sunt dificil de separat în practică

---

### Modelul TCP/IP – introducere
- Modelul efectiv al Internetului
- Dezvoltat înainte de OSI
- Bazat pe protocoale reale, nu pe un model ideal

---

### Structura modelului TCP/IP
- 4 straturi principale

[FIG] c2-assets/fig-tcpip-straturi.png

---

### Stratul de acces la rețea (TCP/IP)
- Echivalent cu:
  - Fizic + Legătură de date (OSI)
- Asigură conectarea la rețea

Exemple:
- Ethernet
- Wi-Fi

---

### Stratul Internet (TCP/IP)
Rol:
- Livrarea pachetelor IP

Caracteristici:
- Protocol neorientat pe conexiune
- Fără garanții de livrare
- Rutare independentă

Protocoale:
- IP
- ICMP

---

### Stratul Transport (TCP/IP)
Protocoale fundamentale:
- TCP (orientat pe conexiune)
- UDP (neorientat pe conexiune)

TCP oferă:
- Confirmări
- Control flux
- Control erori
- Reordonare

UDP oferă:
- Simplitate
- Overhead minim
- Performanță

---

### Stratul Aplicație (TCP/IP)
- Combină:
  - Sesiune
  - Prezentare
  - Aplicație (OSI)

Exemple:
- HTTP
- DNS
- SMTP
- FTP
- SSH

---

### OSI vs TCP/IP – comparație
- OSI:
  - model teoretic
  - 7 straturi
  - separare strictă
- TCP/IP:
  - model practic
  - 4 straturi
  - separare flexibilă

---

### Echivalențe OSI – TCP/IP
[FIG] c2-assets/fig-osi-vs-tcpip.png

---

### De ce folosim ambele modele?
- OSI:
  - analiză
  - învățare
  - depanare conceptuală
- TCP/IP:
  - implementare reală
  - programare
  - Internet

---

### Legătura cu programarea de rețea
- Aplicațiile folosesc:
  - socket-uri
  - porturi
- Sistemul de operare implementează:
  - transport
  - IP
- Hardware-ul implementează:
  - accesul la rețea

---

### Recapitulare
- Rolul modelelor
- Straturile OSI
- Straturile TCP/IP
- Diferențe și echivalențe
- Încapsulare pe straturi

---

### Pregătire pentru Curs 3
- Programare de rețea
- Socket-uri
- TCP vs UDP în practică
