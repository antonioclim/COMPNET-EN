# Week 04 — Computer Networks
### *Rețele de Calculatoare — Săptămâna 4*

> Question Pool — Practice Set

---

## 📚 Curs / Lecture (28 questions)

### Q1. `N01.C05.Q03` — Transmission Delay vs Propagation Delay / Întârzierea de transmisie vs întârzierea de propagare

*[Multiple Choice]*

What is the fundamental difference between transmission delay and propagation delay? [Care este diferența fundamentală între întârzierea de transmisie și întârzierea de propagare?]

- **a)** Transmission depends on packet size and link rate; propagation depends on physical distance and signal speed [Transmisia depinde de dimensiunea pachetului și rata legăturii; propagarea depinde de distanța fizică și viteza semnalului]
- **b)** Transmission occurs only in fibre-optic links; propagation occurs only in copper cable connections [Transmisia are loc doar în legături cu fibră optică; propagarea are loc doar în conexiuni prin cablu de cupru]
- **c)** Propagation delay is always larger than transmission delay regardless of link speed or physical distance between endpoints [Întârzierea de propagare este întotdeauna mai mare decât întârzierea de transmisie indiferent de viteza legăturii sau distanța fizică dintre punctele finale]

> 💡 **Feedback:**
> *Transmission delay = time to push all bits of a packet onto the wire (depends on packet size and link rate). Propagation delay = time for a bit to travel from sender to receiver (depends on physical distance and signal speed). They are independent of each other. [Întârzierea de transmisie = timpul pentru a împinge toți biții unui pachet pe fir (depinde de dimensiunea pachetului și rata legăturii). Întârzierea de propagare = timpul necesar unui bit să călătorească de la emițător la receptor (depinde de distanța fizică și viteza semnalului). Sunt independente una de cealaltă.]*


---

### Q2. `N02.C02.Q07` — Characteristic NOT belonging to TCP / Caracteristică ce NU aparține TCP

*[Multiple Choice]*

Which of the following is **NOT** a characteristic of TCP? [Care dintre următoarele **NU** este o caracteristică a TCP?]

- **a)** Minimal overhead (8-byte header) [Overhead minim (antet de 8 octeți)]
- **b)** Reliable delivery with acknowledgements [Livrare fiabilă cu confirmări (ACK)]
- **c)** In-order delivery via sequence numbers [Livrare în ordine prin numere de secvență]
- **d)** Flow control via sliding window [Controlul fluxului prin fereastră glisantă]

> 💡 **Feedback:**
> *TCP guarantees in-order delivery and reliability, but does not provide minimal overhead. Its headers are at least 20 bytes compared to UDP's 8 bytes, and it adds handshake, acknowledgement (ACK), and flow control overhead. A common misconception is assuming TCP is always the better choice because it provides more features; however, these features come at the cost of additional latency and bandwidth usage, which makes UDP preferable for real-time applications. [TCP garantează livrarea în ordine și fiabilitatea, dar nu oferă overhead minim. Antetele sale au minimum 20 de octeți comparativ cu 8 octeți pentru UDP și adaugă overhead de handshake, confirmare (ACK) și controlul fluxului. O concepție greșită frecventă este presupunerea că TCP este întotdeauna alegerea mai bună deoarece oferă mai multe funcționalități; totuși, aceste funcționalități implică un cost suplimentar de latență și lățime de bandă, ceea ce face UDP preferabil pentru aplicațiile în timp real.]*


---

### Q3. `N03.C02.Q06` — Ethernet Broadcast Frame / Cadrul broadcast Ethernet

*[Multiple Choice]*

At the Ethernet (Layer 2) level, what destination MAC address indicates a broadcast frame that all NICs on the segment must process? [La nivelul Ethernet (Nivelul 2), care adresă MAC de destinație indică un cadru broadcast pe care toate plăcile de rețea din segment trebuie să îl prelucreze?]

- **a)** ff:ff:ff:ff:ff:ff
- **b)** 00:00:00:00:00:00
- **c)** 01:00:5e:00:00:01
- **d)** ff:ff:ff:ff:ff:00

> 💡 **Feedback:**
> *The all-ones MAC address ff:ff:ff:ff:ff:ff signals every NIC to accept and process the frame. Wireshark can filter for this using eth.dst == ff:ff:ff:ff:ff:ff. All other listed addresses serve different roles — 00:00:00:00:00:00 is unspecified, 01:00:5e:xx:xx:xx is multicast OUI. [Adresa MAC formată numai din 1, ff:ff:ff:ff:ff:ff, semnalează fiecărei plăci de rețea să accepte și să prelucreze cadrul. Wireshark poate filtra acest lucru folosind eth.dst == ff:ff:ff:ff:ff:ff. Celelalte adrese enumerate au roluri diferite — 00:00:00:00:00:00 este nespecificată, 01:00:5e:xx:xx:xx este OUI multicast.]*


---

### Q4. `N03.C05.Q06` — Tunnel Use Cases / Cazuri de utilizare ale tunelului

*[Multiple Choice]*

The TCP tunnel pattern demonstrated in Week 3 is foundational to several production technologies. Which of the following is a **direct** application of this pattern? [Modelul de tunel TCP demonstrat în Săptămâna 3 este fundamental pentru mai multe tehnologii de producție. Care dintre următoarele este o aplicare **directă** a acestui model?]

- **a)** Reverse proxy servers that accept incoming connections and relay traffic to upstream backends [Servere proxy inversate care acceptă conexiuni primite și redirecționează traficul către backend-uri]
- **b)** DNS recursive resolution where a resolver queries multiple authoritative nameservers [Rezoluția DNS recursivă unde un resolver interogare mai multe servere de nume autoritative]
- **c)** ARP protocol mapping between Layer 3 IP addresses and Layer 2 MAC addresses [Protocolul ARP de mapare între adresele IP de Nivel 3 și adresele MAC de Nivel 2]
- **d)** Ethernet switch MAC address table learning from incoming frame source addresses in practice [Învățarea tabelei de adrese MAC a comutatorului Ethernet din adresele sursă ale cadrelor primite în practică]

> 💡 **Feedback:**
> *A reverse proxy (e.g. Nginx) accepts client connections and opens new connections to backend servers, forwarding traffic bidirectionally — identical to the tunnel pattern. DNS resolution, ARP resolution, and Ethernet switching operate at different layers and do not use TCP connection relaying. [Un proxy invers (ex. Nginx) acceptă conexiuni de la clienți și deschide conexiuni noi către serverele backend, redirecționând traficul bidirecțional — identic cu modelul tunelului. Rezoluția DNS, rezoluția ARP și comutarea Ethernet funcționează la niveluri diferite și nu folosesc releu-ul conexiunilor TCP.]*


---

### Q5. `N04.C01.Q01` — Primary responsibility of the Physical Layer / Responsabilitatea principală a stratului fizic

*[Multiple Choice]*

What constitutes the primary responsibility of the Physical Layer (Layer 1) in the OSI model? [Care este responsabilitatea principală a stratului fizic (nivelul 1) din modelul OSI?]

- **a)** Transmitting raw bit streams over a physical medium [Transmisia fluxurilor brute de biți printr-un mediu fizic]
- **b)** Controlling access to the shared transmission medium [Controlul accesului la mediul de transmisie partajat]
- **c)** Routing packets between different networks using IP [Rutarea pachetelor între rețele diferite folosind IP]
- **d)** Encrypting data before forwarding to the next hop [Criptarea datelor înainte de retransmitere la următorul nod]

> 💡 **Feedback:**
> *The Physical Layer is the lowest stratum of the OSI model. It handles the raw transmission of unstructured bit streams across a physical medium, defining electrical, optical, or radio specifications. Media access control belongs to the MAC sublayer at Layer 2. [Stratul fizic este cel mai de jos nivel al modelului OSI. Acesta gestionează transmisia brută a fluxurilor nestructurate de biți prin mediul fizic, definind specificațiile electrice, optice sau radio. Controlul accesului la mediu aparține substratului MAC de la nivelul 2.]*


---

### Q6. `N04.C01.Q03` — Signal impairment causing interference between adjacent wires / Deteriorarea semnalului care provoacă interferențe între conductoare adiacente

*[Multiple Choice]*

In twisted-pair cabling, electromagnetic coupling between adjacent conductor pairs degrades signal quality. What is the standard term for this impairment? [La cablurile cu perechi torsadate, cuplajul electromagnetic între perechile adiacente de conductoare degradează calitatea semnalului. Care este termenul standard pentru această deteriorare?]

- **a)** Crosstalk — electromagnetic coupling between wire pairs [Diafonie (crosstalk) — cuplaj electromagnetic între perechi]
- **b)** Attenuation — signal strength loss over increasing distance [Atenuare — pierderea puterii semnalului odată cu distanța]
- **c)** Dispersion — signal spreading in fibre optic transmission [Dispersie — răspândirea semnalului în transmisia pe fibră optică]
- **d)** Jitter — variation in signal arrival timing between bits [Fluctuație (jitter) — variația timpului de sosire între biți]

> 💡 **Feedback:**
> *Crosstalk is the interference that occurs between adjacent wire pairs in a cable. Twisted-pair construction reduces crosstalk by cancelling electromagnetic fields. Attenuation is signal strength loss over distance; dispersion is signal spreading in fibre optics. [Diafonia (crosstalk) este interferența dintre perechile adiacente de conductoare dintr-un cablu. Torsadarea perechilor reduce diafonia prin anularea câmpurilor electromagnetice. Atenuarea este pierderea puterii semnalului pe distanță; dispersia este răspândirea semnalului în fibra optică.]*


---

### Q7. `N04.C01.Q04` — Optical fibre exceeds 100 km at speeds above 100 Gbps / Fibra optică depășește 100 km la viteze de peste 100 Gbps

*[True / False]*

Optical fibre can support transmission distances exceeding 100 km at data rates above 100 Gbps. [Fibra optică poate suporta distanțe de transmisie ce depășesc 100 km la rate de transfer de peste 100 Gbps.]

- **a)** true
- **b)** false

> 💡 **Feedback:**
> *Optical fibre transmits modulated light through glass or plastic fibres. Modern single-mode fibre supports distances well over 100 km and speeds of hundreds of Gbps. [Fibra optică transmite lumină modulată prin fibre de sticlă sau plastic. Fibra single-mode modernă suportă distanțe de peste 100 km și viteze de sute de Gbps.]*


---

### Q8. `N04.C01.Q05` — PAM-4 encoding bits per symbol / Biți per simbol în codarea PAM-4

*[Multiple Choice]*

PAM-4 (Pulse Amplitude Modulation with 4 levels) encodes how many bits per symbol? [PAM-4 (modulație de amplitudine a pulsului cu 4 niveluri) codifică câți biți per simbol?]

- **a)** 2 bits per symbol, since four amplitude levels encode log₂(4) bits [2 biți per simbol, deoarece patru niveluri codifică log₂(4) biți]
- **b)** 1 bit per symbol, identical to standard NRZ encoding [1 bit per simbol, identic cu codarea NRZ standard]
- **c)** 4 bits per symbol, wrongly assuming one bit per amplitude level [4 biți per simbol, presupunând eronat un bit per nivel de amplitudine]
- **d)** 8 bits per symbol, similar to 8B/10B encoding scheme [8 biți per simbol, similar schemei de codare 8B/10B]

> 💡 **Feedback:**
> *With four distinct amplitude levels, PAM-4 represents two bits per symbol (since 2²=4). This doubles the data rate relative to NRZ at the same baud rate, and is used in 400G Ethernet. [Cu patru niveluri distincte de amplitudine, PAM-4 reprezintă doi biți per simbol (deoarece 2²=4). Aceasta dublează rata de date față de NRZ la aceeași rată baud și este utilizată în 400G Ethernet.]*


---

### Q9. `N04.C02.Q02` — IEEE 802 sublayer division of Data Link Layer / Împărțirea IEEE 802 a stratului legătură de date în substraturi

*[Multiple Choice]*

According to the IEEE 802 standards, the Data Link Layer is divided into which two sublayers? [Conform standardelor IEEE 802, stratul legătură de date este împărțit în care două substraturi?]

- **a)** LLC (Logical Link Control) and MAC (Media Access Control) [LLC (controlul legăturii logice) și MAC (controlul accesului la mediu)]
- **b)** Physical and Logical sublayers for signal encoding tasks [Substraturile fizic și logic pentru operațiuni de codare a semnalului]
- **c)** Transport and Session sublayers for connection management [Substraturile de transport și sesiune pentru gestionarea conexiunilor]
- **d)** Control and Data sublayers for flow regulation purposes [Substraturile de control și date pentru reglarea fluxului]

> 💡 **Feedback:**
> *IEEE 802 divides the Data Link Layer into LLC (Logical Link Control, IEEE 802.2) and MAC (Media Access Control, e.g. IEEE 802.3 for Ethernet). LLC provides the interface to the Network Layer; MAC handles physical addressing and medium access. [IEEE 802 împarte stratul legătură de date în LLC (controlul legăturii logice, IEEE 802.2) și MAC (controlul accesului la mediu, de ex. IEEE 802.3 pentru Ethernet). LLC oferă interfața cu stratul de rețea; MAC gestionează adresarea fizică și accesul la mediu.]*


---

### Q10. `N04.C02.Q03` — Bit stuffing framing mechanism / Mecanismul de cadraj prin inserție de biți

*[Multiple Choice]*

In bit stuffing, a fixed pattern such as 01111110 marks frame boundaries. What action is taken when five consecutive 1-bits appear inside the frame payload? [La inserția de biți (bit stuffing), un model fix precum 01111110 marchează limitele cadrului. Ce acțiune se ia când apar cinci biți consecutivi de 1 în sarcina utilă a cadrului?]

- **a)** A 0-bit is inserted after the fifth consecutive 1-bit by the sender [Un bit 0 este inserat de emițător după al cincilea bit 1 consecutiv]
- **b)** The entire frame is retransmitted using a different encoding scheme [Întregul cadru este retransmis folosind o schemă de codare diferită]
- **c)** An escape character byte is prepended before the matching pattern [Un octet caracter de evitare este adăugat înaintea modelului potrivit]
- **d)** The frame is split into two smaller fragments at that exact position [Cadrul este împărțit în două fragmente mai mici la acea poziție exactă]

> 💡 **Feedback:**
> *The transmitter inserts a 0 after any sequence of five consecutive 1-bits in the payload. The receiver removes these stuffed 0s. This prevents the flag pattern 01111110 from appearing inside data, preserving frame boundaries. [Emițătorul inserează un 0 după orice secvență de cinci biți consecutivi de 1 din sarcina utilă. Receptorul elimină acești biți 0 inserați. Aceasta previne apariția modelului steag 01111110 în interiorul datelor, păstrând delimitarea cadrelor.]*


---

### Q11. `N04.C02.Q04` — Ethernet MTU is 1500 bytes / MTU-ul Ethernet este de 1500 de octeți

*[True / False]*

The Maximum Transmission Unit (MTU) for standard Ethernet frames is 1500 bytes. [Unitatea maximă de transmisie (MTU) pentru cadrele Ethernet standard este de 1500 de octeți.]

- **a)** true
- **b)** false

> 💡 **Feedback:**
> *The standard Ethernet MTU is 1500 bytes. The total frame ranges from 64 bytes (minimum, including headers and FCS) to 1518 bytes (maximum). [MTU-ul Ethernet standard este de 1500 de octeți. Cadrul total variază de la 64 de octeți (minim, incluzând antete și FCS) la 1518 de octeți (maxim).]*


---

### Q12. `N04.C02.Q05` — CSMA/CD versus CSMA/CA deployment / CSMA/CD versus CSMA/CA — implementare

*[Multiple Choice]*

CSMA/CD and CSMA/CA are both random-access media access control protocols. Which pairing of technology and protocol variant is correct? [CSMA/CD și CSMA/CA sunt ambele protocoale de acces la mediu de tip acces aleatoriu. Care asociere dintre tehnologie și varianta de protocol este corectă?]

- **a)** CSMA/CD for wired Ethernet; CSMA/CA for Wi-Fi (IEEE 802.11) [CSMA/CD pentru Ethernet cu fir; CSMA/CA pentru Wi-Fi (IEEE 802.11)]
- **b)** CSMA/CA for wired Ethernet; CSMA/CD for Wi-Fi (IEEE 802.11) [CSMA/CA pentru Ethernet cu fir; CSMA/CD pentru Wi-Fi (IEEE 802.11)]
- **c)** CSMA/CD for both wired Ethernet and Wi-Fi simultaneously [CSMA/CD atât pentru Ethernet cu fir cât și pentru Wi-Fi simultan]
- **d)** Token passing for Ethernet; CSMA/CA for fibre optic links [Transmitere cu jeton pentru Ethernet; CSMA/CA pentru legături de fibră]

> 💡 **Feedback:**
> *CSMA/CD (Collision Detection) is used in wired Ethernet — the sender detects collisions and terminates early. CSMA/CA (Collision Avoidance) is used in Wi-Fi (IEEE 802.11) — collisions cannot be detected in wireless, so stations use acknowledgements to avoid them. [CSMA/CD (detecția coliziunilor) se folosește în Ethernet cu fir — emițătorul detectează coliziunile și oprește transmisia. CSMA/CA (evitarea coliziunilor) se folosește în Wi-Fi (IEEE 802.11) — coliziunile nu pot fi detectate în wireless, astfel că stațiile folosesc confirmări pentru a le evita.]*


---

### Q13. `N04.C03.Q01` — TCP byte stream property / Proprietatea TCP de flux de octeți

*[Multiple Choice]*

A client calls sock.send(b'HELLO') immediately followed by sock.send(b'WORLD'). On the server side, sock.recv(1024) is invoked once. What is the most likely output? [Un client apelează sock.send(b'HELLO') urmat imediat de sock.send(b'WORLD'). Pe partea de server, sock.recv(1024) este apelat o singură dată. Care este rezultatul cel mai probabil?]

- **a)** b'HELLOWORLD' — TCP may coalesce both sends into a single segment [b'HELLOWORLD' — TCP poate uni ambele trimiteri într-un singur segment]
- **b)** b'HELLO' alone, with b'WORLD' arriving in the subsequent recv() call [b'HELLO' singur, cu b'WORLD' sosind la următorul apel recv()]
- **c)** b'HELLO WORLD' with an automatic space separator inserted by TCP [b'HELLO WORLD' cu un separator de spațiu inserat automat de TCP]
- **d)** A ConnectionError because two rapid send() calls overload the buffer [O ConnectionError deoarece două apeluri send() rapide supraîncarcă buffer-ul]

> 💡 **Feedback:**
> *TCP is a byte stream protocol with no inherent message boundaries. Consecutive send() calls may be coalesced into a single segment. The receiver sees b'HELLOWORLD' without any delimiter indicating where one message ends. Applications must implement framing (length-prefix or delimiter) to recover boundaries. [TCP este un protocol de flux de octeți fără delimitări inerente ale mesajelor. Apelurile consecutive send() pot fi unite într-un singur segment. Receptorul vede b'HELLOWORLD' fără niciun delimitator. Aplicațiile trebuie să implementeze cadraj (prefix de lungime sau delimitator) pentru a recupera limitele.]*


---

### Q14. `N04.C03.Q02` — Advantage of text protocols for debugging / Avantajul protocoalelor text pentru depanare

*[Multiple Choice]*

During a network issue investigation, an engineer needs to inspect live protocol exchanges with minimal tooling. Why are text protocols advantageous in this scenario? [În timpul investigării unei probleme de rețea, un inginer trebuie să inspecteze schimburile de protocol în direct cu instrumente minime. De ce sunt avantajoase protocoalele text în acest scenariu?]

- **a)** Messages are human-readable and inspectable with telnet, curl, or grep [Mesajele sunt lizibile de oameni și pot fi inspectate cu telnet, curl sau grep]
- **b)** Text protocols always consume less bandwidth than binary counterparts [Protocoalele text consumă întotdeauna mai puțină lățime de bandă decât cele binare]
- **c)** Text protocols offer built-in encryption that binary protocols lack [Protocoalele text oferă criptare integrată pe care cele binare nu o au]
- **d)** Parsing text is computationally cheaper than parsing fixed-width fields [Parsarea textului este computațional mai ieftină decât parsarea câmpurilor fixe]

> 💡 **Feedback:**
> *Text protocols are human-readable, so engineers can use standard tools such as telnet, curl, or grep to observe and test exchanges directly. Binary protocols require specialised decoders or hex dump analysis, increasing debugging complexity. [Protocoalele text sunt lizibile de către oameni, astfel încât inginerii pot folosi instrumente standard precum telnet, curl sau grep pentru a observa și testa schimburile direct. Protocoalele binare necesită decodoare specializate sau analiză de dump hexazecimal.]*


---

### Q15. `N04.C03.Q03` — Endianness mismatch consequence for value 1000 / Consecința nepotrivirii ordinii octeților pentru valoarea 1000

*[Multiple Choice]*

A sender packs the integer 1000 as a 2-byte big-endian unsigned short. The receiver incorrectly interprets the bytes as little-endian. What decimal value does the receiver obtain? [Un emițător împachetează întregul 1000 ca unsigned short big-endian pe 2 octeți. Receptorul interpretează incorect octeții ca little-endian. Ce valoare zecimală obține receptorul?]

- **a)** 59395, because bytes 03 E8 read in reverse order yield 0xE803 [59395, deoarece octeții 03 E8 citiți în ordine inversă dau 0xE803]
- **b)** 1000, since endianness does not affect 2-byte integer values [1000, deoarece ordinea octeților nu afectează valorile întregi pe 2 octeți]
- **c)** 0, because the receiver detects a mismatch and resets the value [0, deoarece receptorul detectează o nepotrivire și resetează valoarea]
- **d)** 256000, from multiplying each byte position by different powers [256000, din multiplicarea fiecărei poziții de octet cu puteri diferite]

> 💡 **Feedback:**
> *1000 decimal = 0x03E8. In big-endian: [03][E8]. Read as little-endian, the bytes become 0xE803 = 59395. This silent data corruption is a common source of interoperability bugs when mixing byte orders. [1000 zecimal = 0x03E8. În big-endian: [03][E8]. Citit ca little-endian, octeții devin 0xE803 = 59395. Această corupere silențioasă a datelor este o sursă frecventă de erori de interoperabilitate la amestecarea ordinilor de octeți.]*


---

### Q16. `N04.C04.Q01` — CRC-32 burst error detection guarantee / Garanția detecției erorilor de rafală a CRC-32

*[Multiple Choice]*

CRC-32 is mathematically guaranteed to detect which categories of transmission errors? [CRC-32 are garanția matematică de a detecta care categorii de erori de transmisie?]

- **a)** All single-bit, double-bit, odd-count, and burst errors up to 32 bits [Toate erorile de un bit, doi biți, număr impar și erorile de rafală de până la 32 biți]
- **b)** Only single-bit errors; multi-bit corruption requires Reed-Solomon codes [Doar erorile de un bit; coruperea multi-bit necesită coduri Reed-Solomon]
- **c)** All possible errors without exception, providing absolute data integrity [Toate erorile posibile fără excepție, oferind integritate absolută a datelor]
- **d)** All errors and also corrects them, functioning as forward error correction [Toate erorile și le corectează, funcționând ca și corecție de erori proactivă]

> 💡 **Feedback:**
> *CRC-32 detects all single-bit errors, all double-bit errors, all odd numbers of bit errors, and all burst errors of 32 bits or fewer. For longer bursts, detection probability is approximately 99.99999998%. CRC detects but does not correct errors. [CRC-32 detectează toate erorile de un bit, toate erorile de doi biți, toate erorile cu un număr impar de biți și toate erorile de rafală de 32 de biți sau mai puțin. Pentru rafale mai lungi, probabilitatea de detecție este aproximativ 99,99999998%. CRC detectează dar nu corectează erorile.]*


---

### Q17. `N04.C04.Q04` — Appropriate integrity mechanism for financial data / Mecanism de integritate adecvat pentru date financiare

*[Multiple Choice]*

A system transmits financial transaction data that must be protected against both accidental corruption and intentional tampering. Which integrity mechanism is most appropriate? [Un sistem transmite date de tranzacții financiare care trebuie protejate atât împotriva coruperii accidentale, cât și a falsificării intenționate. Care mecanism de integritate este cel mai adecvat?]

- **a)** HMAC-SHA256, which provides both error detection and cryptographic tamper resistance [HMAC-SHA256, care oferă atât detecție de erori cât și rezistență criptografică la falsificare]
- **b)** CRC-32, since it detects all burst errors up to 32 bits reliably [CRC-32, deoarece detectează fiabil toate erorile de rafală de până la 32 biți]
- **c)** Even parity, as it is the simplest and most efficient method available [Paritate pară, deoarece este cea mai simplă și eficientă metodă disponibilă]
- **d)** A simple additive checksum, because it is very fast to compute at sender and receiver [O sumă de control aditivă simplă, deoarece este foarte rapidă de calculat la emițător și receptor]

> 💡 **Feedback:**
> *Financial data requires protection against adversaries, not just noise. HMAC-SHA256 provides both error detection and cryptographic tamper resistance. CRC-32 detects accidental errors but is trivially forgeable; parity detects only single-bit errors. [Datele financiare necesită protecție împotriva adversarilor, nu doar a zgomotului. HMAC-SHA256 oferă atât detecție de erori cât și rezistență criptografică la falsificare. CRC-32 detectează erori accidentale dar poate fi falsificat trivial; paritatea detectează doar erori de un bit.]*


---

### Q18. `N04.C04.Q05` — Parity bit limitation / Limitarea bitului de paritate

*[Multiple Choice]*

Even parity appends a bit so that the total number of 1-bits is even. What is a key limitation of this method? [Paritatea pară adaugă un bit astfel încât numărul total de biți 1 să fie par. Care este o limitare cheie a acestei metode?]

- **a)** It fails to detect any even number of simultaneous bit errors [Nu reușește să detecteze niciun număr par de erori simultane de biți]
- **b)** It cannot detect single-bit errors in the payload at all [Nu poate detecta deloc erori de un singur bit în sarcina utilă]
- **c)** It requires more computational resources than CRC-32 calculation [Necesită mai multe resurse computaționale decât calculul CRC-32]
- **d)** It adds 32 bits of overhead to every transmitted frame [Adaugă 32 de biți de overhead la fiecare cadru transmis]

> 💡 **Feedback:**
> *Even parity can detect all single-bit errors and any odd number of bit errors, but it fails to detect even numbers of bit errors (e.g. two flipped bits cancel each other out). CRC provides far superior detection capabilities. [Paritatea pară poate detecta toate erorile de un bit și orice număr impar de erori de biți, dar nu reușește să detecteze un număr par de erori de biți (de ex. două biți inversați se anulează reciproc). CRC oferă capacități de detecție mult superioare.]*


---

### Q19. `N04.C05.Q01` — Binary vs text overhead for integer 1000000 / Overhead binar vs text pentru întregul 1000000

*[Multiple Choice]*

Transmitting the integer 1000000: a text representation uses 7 ASCII characters (7 bytes), while a binary unsigned 32-bit integer uses 4 bytes. What is the bandwidth saving when using the binary representation? [Transmiterea întregului 1000000: o reprezentare text folosește 7 caractere ASCII (7 octeți), în timp ce un întreg fără semn pe 32 de biți folosește 4 octeți. Care este economia de lățime de bandă la utilizarea reprezentării binare?]

- **a)** Approximately 43%, reducing from 7 bytes to 4 bytes per integer field [Aproximativ 43%, reducând de la 7 octeți la 4 octeți per câmp întreg]
- **b)** Exactly 75%, because binary always uses one quarter the space of text [Exact 75%, deoarece binarul folosește întotdeauna un sfert din spațiul textului]
- **c)** Zero savings, since modern compression eliminates any size difference [Zero economii, deoarece compresia modernă elimină orice diferență de dimensiune]
- **d)** Approximately 10%, a negligible improvement not worth the complexity [Aproximativ 10%, o îmbunătățire neglijabilă care nu merită complexitatea]

> 💡 **Feedback:**
> *Binary saves (7−4)/7 × 100 ≈ 43% bandwidth for this single field. For high-frequency sensor data with many numeric values, this compounds significantly. However, text protocols offer easier debugging and tooling. [Binar economisește (7−4)/7 × 100 ≈ 43% lățime de bandă pentru acest singur câmp. Pentru date de senzori cu frecvență ridicată cu multe valori numerice, aceasta se acumulează semnificativ. Totuși, protocoalele text oferă depanare și instrumente mai ușoare.]*


---

### Q20. `N04.C05.Q04` — Sequence numbers alone do not prevent duplicates / Numerele de secvență singure nu previn duplicatele

*[Multiple Choice]*

A developer adds monotonically increasing sequence numbers to a binary protocol but does not implement any duplicate detection logic. What risk remains? [Un dezvoltator adaugă numere de secvență crescătoare monoton la un protocol binar dar nu implementează nicio logică de detecție a duplicatelor. Ce risc rămâne?]

- **a)** Duplicate messages can still be processed, since sequence numbers require explicit checking logic [Mesajele duplicate pot fi procesate, deoarece numerele de secvență necesită logică explicită de verificare]
- **b)** No risk remains — sequence numbers automatically discard duplicate messages at the transport layer [Nu rămâne niciun risc — numerele de secvență elimină automat mesajele duplicate la stratul de transport]
- **c)** The only risk is integer overflow, which can be solved by using 64-bit counters instead [Singurul risc este depășirea de întreg, rezolvabilă prin utilizarea contoarelor de 64 biți]
- **d)** Messages arrive in wrong order, but duplicate detection is inherently handled by TCP itself [Mesajele sosesc în ordine greșită, dar detecția duplicatelor este gestionată inerent de TCP]

> 💡 **Feedback:**
> *Sequence numbers are a tool, not a solution. Without application-level logic to check for and discard already-processed sequence numbers (using a sliding window or seen-set), duplicate messages from retransmissions or replay can still be processed twice. [Numerele de secvență sunt un instrument, nu o soluție. Fără logică la nivel de aplicație pentru a verifica și elimina numerele de secvență deja procesate (folosind o fereastră glisantă sau un set de văzute), mesajele duplicate din retransmisii pot fi procesate de două ori.]*


---

### Q21. `N04.C05.Q05` — Stop-and-wait inefficiency on high BDP links / Ineficiența stop-and-wait pe legăturile cu BDP ridicat

*[Multiple Choice]*

Stop-and-wait flow control transmits one frame and waits for acknowledgement before sending the next. Why is this scheme particularly inefficient on links with high bandwidth-delay product? [Controlul fluxului stop-and-wait transmite un cadru și așteaptă confirmarea înainte de a trimite următorul. De ce este această schemă deosebit de ineficientă pe legături cu produs lățime de bandă-întârziere ridicat?]

- **a)** The sender idles while waiting, leaving most of the link capacity unused [Emițătorul este inactiv în timpul așteptării, lăsând neutilizată cea mai mare parte a capacității legăturii]
- **b)** Acknowledgements get lost frequently on links with high bandwidth values [Confirmările se pierd frecvent pe legături cu valori ridicate ale lățimii de bandă]
- **c)** The receiver cannot process incoming frames fast enough on a wide-bandwidth link [Receptorul nu poate procesa cadrele primite suficient de rapid pe o legătură cu lățime de bandă mare]
- **d)** Frame corruption increases proportionally with the distance between nodes [Coruperea cadrelor crește proporțional cu distanța dintre noduri]

> 💡 **Feedback:**
> *On high bandwidth-delay product links, the sender spends most of its time idle waiting for acknowledgements. The sliding window protocol allows multiple frames to be in flight simultaneously, utilising the link far more efficiently: efficiency = W / (1 + 2a). [Pe legături cu produs lățime de bandă-întârziere ridicat, emițătorul petrece cea mai mare parte a timpului inactiv așteptând confirmări. Protocolul cu fereastră glisantă permite trimiterea simultană a mai multor cadre, utilizând legătura mult mai eficient: eficiență = W / (1 + 2a).]*


---

### Q22. `N04.T00.Q01` — TCP byte stream and application framing / Fluxul de octeți TCP și cadrajul aplicației

*[Multiple Choice]*

A developer writes a chat application where the client sends messages using sock.send(). During local testing, each message arrives separately. In production, messages frequently arrive merged. What fundamental property of TCP explains this behaviour, and what must the application implement? [Un dezvoltator creează o aplicație de chat unde clientul trimite mesaje folosind sock.send(). În testarea locală, fiecare mesaj ajunge separat. În producție, mesajele ajung frecvent unite. Ce proprietate fundamentală a TCP explică acest comportament și ce trebuie să implementeze aplicația?]

- **a)** TCP provides a byte stream without message boundaries; the application must add framing [TCP oferă un flux de octeți fără limite de mesaje; aplicația trebuie să adauge cadraj]
- **b)** TCP has a bug that merges messages under high load conditions on the network [TCP are un bug care unește mesajele sub condiții de încărcare ridicată pe rețea]
- **c)** The production network uses different MTU settings causing packet fragmentation [Rețeaua de producție folosește setări MTU diferite care provoacă fragmentarea pachetelor]
- **d)** TCP buffers are too small in production, causing messages to be truncated [Buffer-ele TCP sunt prea mici în producție, provocând trunchierea mesajelor]

> 💡 **Feedback:**
> *TCP is a byte stream — it makes no guarantees about preserving send() boundaries. The application must implement framing (length-prefix or delimiter) to delineate individual messages within the continuous byte stream. [TCP este un flux de octeți — nu oferă garanții privind păstrarea limitelor send(). Aplicația trebuie să implementeze cadraj (prefix de lungime sau delimitator) pentru a delimita mesajele individuale în fluxul continuu de octeți.]*


---

### Q23. `N04.T00.Q02` — Purpose of magic bytes in binary protocols / Scopul octeților magici în protocoalele binare

*[Multiple Choice]*

The Week 4 BINARY protocol begins each message with the bytes b'NP'. If a receiver reads a header where the first two bytes are not b'NP', what should it do and why? [Protocolul BINAR din Săptămâna 4 începe fiecare mesaj cu octeții b'NP'. Dacă un receptor citește un antet unde primii doi octeți nu sunt b'NP', ce ar trebui să facă și de ce?]

- **a)** Reject the message — magic mismatch indicates corruption or wrong protocol [Respingerea mesajului — nepotrivirea magic-ului indică corupere sau protocol greșit]
- **b)** Process the message normally since magic bytes are optional identification data [Procesarea mesajului normal deoarece octeții magici sunt date opționale de identificare]
- **c)** Swap the bytes to fix potential endianness issues and continue parsing [Interschimbarea octeților pentru a rezolva posibilele probleme de endianness și continuarea parsării]
- **d)** Buffer the bytes and wait for more data since the header may be incomplete [Stocarea octeților și așteptarea mai multor date deoarece antetul poate fi incomplet]

> 💡 **Feedback:**
> *Magic bytes serve as a protocol identifier and synchronisation marker. Mismatched magic indicates either a corrupt message, wrong protocol version, or stream desynchronisation. The receiver should reject the message and potentially reset the connection. [Octeții magici servesc ca identificator de protocol și marcator de sincronizare. Un magic nepotrivit indică fie un mesaj corupt, fie o versiune greșită de protocol, fie desincronizarea fluxului. Receptorul ar trebui să respingă mesajul și, potențial, să reseteze conexiunea.]*


---

### Q24. `N04.T00.Q03` — CRC detection versus correction / Detecția CRC versus corecție

*[Multiple Choice]*

A student claims: 'Our binary protocol uses CRC-32, so if a packet arrives corrupted, the server can fix the error automatically.' Is this claim correct? [Un student afirmă: 'Protocolul nostru binar folosește CRC-32, deci dacă un pachet ajunge corupt, serverul poate repara automat eroarea.' Este corectă această afirmație?]

- **a)** Incorrect — CRC-32 detects errors but cannot correct them; the packet must be retransmitted [Incorect — CRC-32 detectează erori dar nu le poate corecta; pachetul trebuie retransmis]
- **b)** Correct — CRC-32 includes enough redundancy to fix single-bit errors automatically [Corect — CRC-32 include suficientă redundanță pentru a repara automat erorile pe un singur bit]
- **c)** Partially correct — CRC-32 can fix burst errors up to 16 bits in length only [Parțial corect — CRC-32 poate repara erori de rafală de până la 16 biți lungime]
- **d)** Correct — all modern error detection mechanisms include automatic error correction [Corect — toate mecanismele moderne de detecție a erorilor includ corecție automată]

> 💡 **Feedback:**
> *The claim is incorrect. CRC-32 is an error detection mechanism only — it can identify that corruption occurred but cannot determine which bits changed. Error correction requires FEC codes like Reed-Solomon or Hamming codes. When CRC fails, the appropriate action is to discard and request retransmission. [Afirmația este incorectă. CRC-32 este doar un mecanism de detecție a erorilor — poate identifica faptul că a avut loc coruperea dar nu poate determina ce biți s-au schimbat. Corecția erorilor necesită coduri FEC precum Reed-Solomon sau Hamming. Când CRC eșuează, acțiunea adecvată este eliminarea și cererea de retransmisie.]*


---

### Q25. `N04.T00.Q05` — Endianness impact on sensor readings / Impactul endianness asupra citirilor senzorilor

*[Multiple Choice]*

A UDP sensor client sends temperature 23.5°C using big-endian float. A misconfigured receiver reads it as little-endian. The displayed temperature is a nonsensical value. What fundamental principle has been violated? [Un client senzor UDP trimite temperatura 23.5°C folosind float big-endian. Un receptor configurat greșit o citește ca little-endian. Temperatura afișată este o valoare fără sens. Ce principiu fundamental a fost violat?]

- **a)** Network byte order (big-endian) convention was violated — both endpoints must match [Convenția ordinii octeților în rețea (big-endian) a fost încălcată — ambele capete trebuie să corespundă]
- **b)** The temperature sensor hardware is faulty and producing incorrect readings [Hardware-ul senzorului de temperatură este defect și produce citiri incorecte]
- **c)** UDP lost some bytes during transmission, corrupting the temperature field [UDP a pierdut câțiva octeți în timpul transmisiei, corupând câmpul de temperatură]
- **d)** The CRC check should have caught this error before the receiver processed the data [Verificarea CRC ar fi trebuit să detecteze această eroare înainte ca receptorul să proceseze datele]

> 💡 **Feedback:**
> *Network byte order convention requires big-endian for all protocol fields. When the receiver applies little-endian interpretation to big-endian data, the IEEE 754 float bytes are reversed, producing a completely different floating-point value. Both endpoints must agree on byte order. [Convenția ordinii octeților în rețea necesită big-endian pentru toate câmpurile de protocol. Când receptorul aplică interpretare little-endian datelor big-endian, octeții float IEEE 754 sunt inversați, producând o valoare cu virgulă mobilă complet diferită. Ambele capete trebuie să fie de acord asupra ordinii octeților.]*


---

### Q26. `N04.T00.Q08` — CSMA/CD versus CSMA/CA rationale / Motivația CSMA/CD versus CSMA/CA

*[Multiple Choice]*

Wired Ethernet uses CSMA/CD while Wi-Fi uses CSMA/CA. Why cannot CSMA/CD be used in wireless networks? [Ethernet cu fir folosește CSMA/CD iar Wi-Fi folosește CSMA/CA. De ce nu poate fi folosit CSMA/CD în rețelele wireless?]

- **a)** Wireless stations cannot detect collisions while transmitting (hidden terminal problem) [Stațiile wireless nu pot detecta coliziunile în timpul transmisiei (problema terminalului ascuns)]
- **b)** Wi-Fi operates at lower physical-layer speeds where collision detection is computationally infeasible [Wi-Fi operează la viteze fizice mai mici unde detecția coliziunilor este imposibilă din punct de vedere computațional]
- **c)** The IEEE 802.11 standard deliberately chose CA over CD for marketing differentiation purposes [Standardul IEEE 802.11 a ales deliberat CA în locul CD în scopuri de diferențiere de marketing]
- **d)** CSMA/CD requires dedicated hardware only available in wired network adapters [CSMA/CD necesită hardware dedicat disponibil doar în adaptoarele de rețea cu fir]

> 💡 **Feedback:**
> *In wireless networks, a station cannot simultaneously transmit and listen for collisions (the hidden terminal problem). The transmitted signal is much stronger than any received collision signal. CSMA/CA avoids collisions proactively using RTS/CTS handshakes and acknowledgements. [În rețelele wireless, o stație nu poate transmite și asculta simultan pentru coliziuni (problema terminalului ascuns). Semnalul transmis este mult mai puternic decât orice semnal de coliziune recepționat. CSMA/CA evită coliziunile proactiv folosind handshake-uri RTS/CTS și confirmări.]*


---

### Q27. `N04.T00.Q09` — Sequence number duplicate detection gap / Lacuna detecției duplicatelor cu numere de secvență

*[Multiple Choice]*

A binary protocol has monotonically increasing 4-byte sequence numbers but no duplicate detection logic. In what specific scenario could this cause data corruption? [Un protocol binar are numere de secvență crescătoare monoton pe 4 octeți dar fără logică de detecție a duplicatelor. În ce scenariu specific ar putea cauza coruperea datelor?]

- **a)** Retransmitted messages get processed twice — harmful for non-idempotent operations [Mesajele retransmise se procesează de două ori — dăunător pentru operațiile non-idempotente]
- **b)** The 4-byte counter will overflow after approximately 4 billion messages sent [Contorul pe 4 octeți va depăși după aproximativ 4 miliarde de mesaje trimise]
- **c)** Messages arrive out of order and the receiver processes them in the wrong sequence order [Mesajele ajung în ordine greșită și receptorul le procesează în ordinea secvenței greșite]
- **d)** The sequence number field consumes 4 bytes of header space that could carry application payload instead [Câmpul numărului de secvență consumă 4 octeți din spațiul antetului care ar putea transporta date utile]

> 💡 **Feedback:**
> *If a PUT_REQ (key='balance', value='1000') is retransmitted due to network timeout but the original was already processed, the operation executes twice. For idempotent operations this is harmless, but for non-idempotent operations (like INCR) it causes silent data corruption. [Dacă un PUT_REQ (key='balance', value='1000') este retransmis din cauza timeout-ului de rețea dar originalul fusese deja procesat, operația se execută de două ori. Pentru operații idempotente acest lucru este inofensiv, dar pentru operații non-idempotente (precum INCR) provoacă corupere silențioasă a datelor.]*


---

### Q28. `N04.T00.Q10` — Protocol overhead analysis scenario / Scenariu de analiză a overhead-ului protocoalelor

*[Multiple Choice]*

A system sends the command 'SET counter 42' (14 bytes) using both TEXT and BINARY protocols. TEXT adds a length-prefix frame ('14 SET counter 42' = 17 bytes). BINARY uses a 14-byte header plus the payload (14+14 = 28 bytes). Which protocol is more efficient for this specific message, and when does the comparison reverse? [Un sistem trimite comanda 'SET counter 42' (14 octeți) folosind ambele protocoale TEXT și BINAR. TEXT adaugă un cadru cu prefix de lungime ('14 SET counter 42' = 17 octeți). BINAR folosește un antet de 14 octeți plus sarcina utilă (14+14 = 28 octeți). Care protocol este mai eficient pentru acest mesaj specific și când se inversează comparația?]

- **a)** TEXT is more efficient here (17 vs 28 bytes); BINARY wins for large or numeric-heavy payloads [TEXT este mai eficient aici (17 vs 28 octeți); BINAR câștigă pentru sarcini utile mari sau cu multe date numerice]
- **b)** BINARY is always more efficient regardless of payload size due to its fixed-width header [BINAR este întotdeauna mai eficient indiferent de dimensiunea sarcinii utile datorită antetului cu lățime fixă]
- **c)** TEXT and BINARY have identical overhead because both transmit the same application data [TEXT și BINAR au overhead identic deoarece ambele transmit aceleași date de aplicație]
- **d)** The overhead comparison is irrelevant since modern networks have unlimited bandwidth [Comparația overhead-ului este irelevantă deoarece rețelele moderne au lățime de bandă nelimitată]

> 💡 **Feedback:**
> *For this small payload, TEXT is more efficient (17 vs 28 bytes). The BINARY protocol's 14-byte fixed header dominates. The comparison reverses for large payloads: as payload grows, the fixed 14 bytes becomes a smaller percentage of total, and binary values are more compact than their ASCII text equivalents. [Pentru această sarcină utilă mică, TEXT este mai eficient (17 vs 28 octeți). Antetul fix de 14 octeți al protocolului BINAR domină. Comparația se inversează pentru sarcini utile mari: pe măsură ce sarcina utilă crește, cei 14 octeți fixi devin un procent mai mic din total, iar valorile binare sunt mai compacte decât echivalentele lor text ASCII.]*


---

## 🔬 Laborator / Lab (18 questions)


---

### Q29. `N04.S01.Q03` — TEXT protocol frame format / Formatul cadrului protocolului TEXT

*[Multiple Choice]*

In the Week 4 TEXT protocol, the frame format is " " where LENGTH is an ASCII decimal number. For the command "SET name Alice" (13 bytes), what is the complete frame transmitted? [În protocolul TEXT din Săptămâna 4, formatul cadrului este " " unde LENGTH este un număr zecimal ASCII. Pentru comanda "SET name Alice" (13 octeți), care este cadrul complet transmis?]

- **a)** "13 SET name Alice" — ASCII length prefix, space separator, then payload ["13 SET name Alice" — prefix de lungime ASCII, separator spațiu, apoi sarcina utilă]
- **b)** "SET name Alice\\r\\n" — the payload followed by a CRLF delimiter at the end ["SET name Alice\\r\\n" — sarcina utilă urmată de un delimitator CRLF la final]
- **c)** "\\x00\\x0dSET name Alice" — 2-byte binary length prefix in big-endian ["\\x00\\x0dSET name Alice" — prefix de lungime binar pe 2 octeți în big-endian]
- **d)** "SET name Alice" — raw payload without any framing or length prefix ["SET name Alice" — sarcina utilă brută fără cadraj sau prefix de lungime]

> 💡 **Feedback:**
> *The frame consists of the ASCII string "13" followed by a space separator and then the 13-byte payload. Total: "13 SET name Alice" — a 16-byte frame (2 digits + 1 space + 13 payload). [Cadrul constă din șirul ASCII "13" urmat de un separator spațiu și apoi sarcina utilă de 13 octeți. Total: "13 SET name Alice" — un cadru de 16 octeți (2 cifre + 1 spațiu + 13 sarcină utilă).]*


---

### Q30. `N04.S01.Q05` — TEXT protocol supported commands / Comenzile suportate de protocolul TEXT

*[Multiple Choice]*

The TEXT protocol server in Exercise 4.01 supports several commands. Which set correctly lists valid commands? [Serverul protocolului TEXT din Exercițiul 4.01 suportă mai multe comenzi. Care set listează corect comenzile valide?]

- **a)** PING, SET, GET, DEL, COUNT, KEYS, QUIT [PING, SET, GET, DEL, COUNT, KEYS, QUIT]
- **b)** CONNECT, SEND, RECEIVE, CLOSE, STATUS [CONNECT, SEND, RECEIVE, CLOSE, STATUS]
- **c)** PUT, POST, DELETE, PATCH, OPTIONS, HEAD [PUT, POST, DELETE, PATCH, OPTIONS, HEAD]
- **d)** HELO, MAIL FROM, RCPT TO, DATA, QUIT [HELO, MAIL FROM, RCPT TO, DATA, QUIT]

> 💡 **Feedback:**
> *The TEXT server supports: PING (connectivity test), SET key value (store), GET key (retrieve), DEL key (delete), COUNT (number of keys), KEYS (list all), and QUIT (close connection). [Serverul TEXT suportă: PING (test de conectivitate), SET key value (stocare), GET key (recuperare), DEL key (ștergere), COUNT (număr de chei), KEYS (listare toate) și QUIT (închidere conexiune).]*


---

### Q31. `N04.S02.Q01` — struct.pack output for big-endian 1000 / Rezultatul struct.pack pentru 1000 big-endian

*[Multiple Choice]*

What hex string does struct.pack('\>H', 1000).hex() produce in Python? [Ce șir hexazecimal produce struct.pack('\>H', 1000).hex() în Python?]

- **a)** '03e8' — big-endian places the most significant byte 0x03 first ['03e8' — big-endian plasează octetul cel mai semnificativ 0x03 primul]
- **b)** 'e803' — this would be the little-endian representation with LSB first ['e803' — aceasta ar fi reprezentarea little-endian cu LSB-ul primul]
- **c)** '1000' — the decimal digits are not the same as the hex encoding ['1000' — cifrele zecimale nu sunt identice cu codarea hexazecimală]
- **d)** '03e80000' — this would require a 4-byte unsigned integer format I ['03e80000' — aceasta ar necesita formatul de întreg fără semn pe 4 octeți I]

> 💡 **Feedback:**
> *1000 decimal = 0x03E8 hexadecimal. The format '\>H' means big-endian unsigned short (2 bytes). Big-endian places the MSB first: 03 then E8. Result: '03e8'. [1000 zecimal = 0x03E8 hexazecimal. Formatul '\>H' înseamnă unsigned short big-endian (2 octeți). Big-endian plasează MSB-ul primul: 03 apoi E8. Rezultat: '03e8'.]*


---

### Q32. `N04.S02.Q02` — Binary header total size calculation / Calculul dimensiunii totale a antetului binar

*[Multiple Choice]*

The BINARY protocol header uses format '\>2sBBHII'. What is the total header size in bytes? [Antetul protocolului BINAR folosește formatul '\>2sBBHII'. Care este dimensiunea totală a antetului în octeți?]

- **a)** 14 bytes: 2(magic) + 1(version) + 1(type) + 2(length) + 4(seq) + 4(CRC) [14 octeți: 2(magic) + 1(versiune) + 1(tip) + 2(lungime) + 4(seq) + 4(CRC)]
- **b)** 10 bytes: the same calculation without the 4-byte CRC32 checksum field [10 octeți: același calcul fără câmpul de sumă de control CRC32 de 4 octeți]
- **c)** 16 bytes: with 2-byte alignment padding added after the version field [16 octeți: cu completare de aliniere de 2 octeți adăugată după câmpul versiune]
- **d)** 20 bytes: including an additional 6-byte reserved field for extensions [20 octeți: incluzând un câmp suplimentar de 6 octeți rezervat pentru extensii]

> 💡 **Feedback:**
> *Calculation: 2s = 2 bytes (magic), B = 1 byte (version), B = 1 byte (type), H = 2 bytes (payload_len), I = 4 bytes (seq), I = 4 bytes (CRC32). Total: 2+1+1+2+4+4 = 14 bytes. [Calcul: 2s = 2 octeți (magic), B = 1 octet (versiune), B = 1 octet (tip), H = 2 octeți (payload_len), I = 4 octeți (seq), I = 4 octeți (CRC32). Total: 2+1+1+2+4+4 = 14 octeți.]*


---

### Q33. `N04.S02.Q05` — struct format '\>' versus '\<' meaning / Semnificația '\>' versus '\<' în formatul struct

*[Multiple Choice]*

In a struct.pack() call, the prefix character '\>' and '' și '\<' controlează ordinea octeților. Ce specifică ele?]

- **a)** '\>' is big-endian (MSB first); '' este big-endian (MSB primul); '\<' este little-endian (LSB primul)]
- **b)** '\>' compresses the output data; '' comprimă datele; '\<' decomprimă datele binare împachetate]
- **c)** '\>' adds field padding bytes; '' adaugă octeți de completare; '\<' elimină completarea de aliniere]
- **d)** '\>' enables signed integer values; '' activează valori de întregi cu semn; '\<' forțează interpretarea fără semn]

> 💡 **Feedback:**
> *'\>' means big-endian (network byte order, MSB first). '' (network order). Using native order ('@' or '=') risks interoperability issues. ['\>' înseamnă big-endian (ordinea octeților în rețea, MSB primul). '' (ordinea rețelei). Folosirea ordinii native ('@' sau '=') riscă probleme de interoperabilitate.]*


---

### Q34. `N04.S03.Q03` — CRC computation scope in binary header / Domeniul de calcul CRC în antetul binar

*[Multiple Choice]*

When building a BINARY protocol message, over which data is the CRC-32 checksum calculated? [La construirea unui mesaj de protocol BINAR, peste ce date se calculează suma de control CRC-32?]

- **a)** Over the header without the CRC field (10 bytes) plus the entire payload [Peste antetul fără câmpul CRC (10 octeți) plus întreaga sarcină utilă]
- **b)** Over the payload only, excluding all header fields from the calculation [Doar peste sarcina utilă, excluzând toate câmpurile antetului din calcul]
- **c)** Over the complete 14-byte header including the CRC field set to zero [Peste antetul complet de 14 octeți inclusiv câmpul CRC setat la zero]
- **d)** Over the magic and version fields only, as a protocol identification check [Doar peste câmpurile magic și versiune, ca verificare de identificare a protocolului]

> 💡 **Feedback:**
> *CRC is calculated over the header (WITHOUT the CRC field itself) concatenated with the payload. The header is first packed without CRC (10 bytes), then CRC is computed over those 10 bytes + payload, and finally the full 14-byte header is assembled with the CRC included. [CRC-ul se calculează peste antetul (FĂRĂ câmpul CRC în sine) concatenat cu sarcina utilă. Antetul este mai întâi împachetat fără CRC (10 octeți), apoi CRC-ul se calculează peste acei 10 octeți + sarcina utilă, iar în final antetul complet de 14 octeți este asamblat cu CRC-ul inclus.]*


---

### Q35. `N04.S03.Q04` — Hex representation of NP magic bytes / Reprezentarea hexazecimală a octeților magici NP

*[Multiple Choice]*

The BINARY protocol magic bytes are b'NP'. What is their hexadecimal representation? [Octeții magici ai protocolului BINAR sunt b'NP'. Care este reprezentarea lor hexazecimală?]

- **a)** 4e50 — N is 0x4E (78 decimal), P is 0x50 (80 decimal) [4e50 — N este 0x4E (78 zecimal), P este 0x50 (80 zecimal)]
- **b)** 4e70 — confusing 'P' (0x50) with 'p' (0x70) lowercase ASCII [4e70 — confuzie între 'P' (0x50) și 'p' (0x70) ASCII minusculă]
- **c)** 4f51 — applying an off-by-one error to both bytes [4f51 — aplicând o eroare off-by-one ambilor octeți]
- **d)** 0d0a — CR LF line-ending bytes, not NP magic bytes [0d0a — octeți CR LF de terminare linie, nu octeții magici NP]

> 💡 **Feedback:**
> *In ASCII: 'N' = 0x4E (78 decimal), 'P' = 0x50 (80 decimal). Therefore b'NP' in hex is 4e50. This can be verified with b'NP'.hex() in Python. [În ASCII: 'N' = 0x4E (78 zecimal), 'P' = 0x50 (80 zecimal). Prin urmare, b'NP' în hex este 4e50. Se poate verifica cu b'NP'.hex() în Python.]*


---

### Q36. `N04.S03.Q05` — Sequence number purpose in binary protocol / Scopul numărului de secvență în protocolul binar

*[Multiple Choice]*

Each BINARY protocol message contains a 4-byte sequence number. What primary purpose does it serve? [Fiecare mesaj de protocol BINAR conține un număr de secvență pe 4 octeți. Ce scop principal servește?]

- **a)** Correlating requests with responses and detecting duplicates or lost messages [Corelarea cererilor cu răspunsurile și detectarea duplicatelor sau mesajelor pierdute]
- **b)** Encrypting the payload using the sequence number as a cryptographic key [Criptarea sarcinii utile folosind numărul de secvență ca o cheie criptografică]
- **c)** Controlling flow by limiting transmission to one message per sequence step [Controlul fluxului prin limitarea transmisiei la un mesaj per pas de secvență]
- **d)** Compressing repeated fields by referencing previously sent sequence values [Comprimarea câmpurilor repetate prin referirea valorilor de secvență trimise anterior]

> 💡 **Feedback:**
> *Sequence numbers correlate requests with their corresponding responses (request-response matching) and enable detection of duplicate or lost messages. The number is monotonically increasing and allows a receiver to identify gaps or replays. [Numerele de secvență corelează cererile cu răspunsurile corespunzătoare (potrivirea cerere-răspuns) și permit detectarea mesajelor duplicate sau pierdute. Numărul este crescător monoton și permite receptorului să identifice goluri sau reluări.]*


---

### Q37. `N04.S04.Q01` — UDP sensor datagram size / Dimensiunea datagramei senzorului UDP

*[Multiple Choice]*

The UDP sensor protocol datagram structure has fields: version(1B), sensor_id(4B), temperature(4B float), location(10B), CRC32(4B). What is the total datagram size? [Structura datagramei protocolului senzorului UDP are câmpurile: version(1O), sensor_id(4O), temperature(4O float), location(10O), CRC32(4O). Care este dimensiunea totală a datagramei?]

- **a)** 23 bytes: 1(version) + 4(sensor_id) + 4(temp) + 10(location) + 4(CRC32) [23 octeți: 1(versiune) + 4(sensor_id) + 4(temp) + 10(locație) + 4(CRC32)]
- **b)** 19 bytes: the same calculation but without the 4-byte CRC32 field [19 octeți: același calcul dar fără câmpul CRC32 de 4 octeți]
- **c)** 32 bytes: including 9 bytes of alignment padding for word boundaries [32 octeți: incluzând 9 octeți de completare de aliniere pentru limite de cuvânt]
- **d)** 14 bytes: matching the size of the BINARY protocol TCP header exactly [14 octeți: egalând exact dimensiunea antetului TCP al protocolului BINAR]

> 💡 **Feedback:**
> *Sum of all fields: 1 + 4 + 4 + 10 + 4 = 23 bytes. This compact, fixed-size format is ideal for high-frequency sensor transmissions over UDP. [Suma tuturor câmpurilor: 1 + 4 + 4 + 10 + 4 = 23 octeți. Acest format compact de dimensiune fixă este ideal pentru transmisii de senzori de frecvență ridicată peste UDP.]*


---

### Q38. `N04.S04.Q02` — ECHO_REQ message type code / Codul tipului de mesaj ECHO_REQ

*[Multiple Choice]*

In the BINARY protocol, message types are encoded as single-byte integers. What numeric value corresponds to ECHO_REQ? [În protocolul BINAR, tipurile de mesaje sunt codificate ca întregi pe un singur octet. Ce valoare numerică corespunde tipului ECHO_REQ?]

- **a)** 1 — ECHO_REQ is assigned type code 1, with ECHO_RESP being type code 2 [1 — ECHO_REQ are codul de tip 1, cu ECHO_RESP fiind codul de tip 2]
- **b)** 0 — type codes start from zero for the first defined message type [0 — codurile de tip pornesc de la zero pentru primul tip de mesaj definit]
- **c)** 255 — this value is reserved for ERROR responses, not echo requests [255 — această valoare este rezervată pentru răspunsuri ERROR, nu cereri echo]
- **d)** 3 — this is the code for PUT_REQ, not for echo request messages [3 — acesta este codul pentru PUT_REQ, nu pentru mesajele de cerere echo]

> 💡 **Feedback:**
> *TYPE_ECHO_REQ = 1, TYPE_ECHO_RESP = 2, TYPE_PUT_REQ = 3, TYPE_PUT_RESP = 4, TYPE_GET_REQ = 5, TYPE_GET_RESP = 6, TYPE_ERROR = 255. Response types are always request type + 1. [TYPE_ECHO_REQ = 1, TYPE_ECHO_RESP = 2, TYPE_PUT_REQ = 3, TYPE_PUT_RESP = 4, TYPE_GET_REQ = 5, TYPE_GET_RESP = 6, TYPE_ERROR = 255. Tipurile de răspuns sunt întotdeauna tipul cererii + 1.]*


---

### Q39. `N04.S05.Q04` — Wireshark filter for TEXT protocol port / Filtru Wireshark pentru portul protocolului TEXT

*[Multiple Choice]*

Which Wireshark display filter isolates traffic for the Week 4 TEXT protocol server? [Care filtru de afișare Wireshark izolează traficul pentru serverul protocolului TEXT din Săptămâna 4?]

- **a)** tcp.port == 3333 [tcp.port == 3333]
- **b)** udp.port == 3333 [udp.port == 3333]
- **c)** port 3333 [port 3333]
- **d)** tcp.port == 5401 [tcp.port == 5401]

> 💡 **Feedback:**
> *The TEXT protocol server listens on TCP port 3333. The display filter tcp.port == 3333 matches all packets (source or destination) on that port. To see only data packets, add tcp.len \> 0. [Serverul protocolului TEXT ascultă pe portul TCP 3333. Filtrul de afișare tcp.port == 3333 potrivește toate pachetele (sursă sau destinație) de pe acel port. Pentru a vedea doar pachetele de date, adăugați tcp.len \> 0.]*


---

### Q40. `N04.S05.Q06` — tcpdump command for TEXT protocol traffic / Comanda tcpdump pentru traficul protocolului TEXT

*[Multiple Choice]*

Which tcpdump command captures TEXT protocol packets on TCP port 3333 in ASCII mode without resolving hostnames? [Care comandă tcpdump capturează pachetele protocolului TEXT pe portul TCP 3333 în mod ASCII fără rezoluția numelor de gazdă?]

- **a)** sudo tcpdump -i eth0 -nn -A 'tcp port 3333' [sudo tcpdump -i eth0 -nn -A 'tcp port 3333']
- **b)** tcpdump -i eth0 -verbose port 3333 \--ascii [tcpdump -i eth0 -verbose port 3333 \--ascii]
- **c)** sudo tcpdump -i eth0 -XX 'udp port 3333' [sudo tcpdump -i eth0 -XX 'udp port 3333']
- **d)** tcpdump -capture -port 3333 -format text [tcpdump -capture -port 3333 -format text]

> 💡 **Feedback:**
> *sudo tcpdump -i eth0 -nn -A 'tcp port 3333' — the -nn flag disables host and port name resolution, -A shows ASCII content, and the BPF filter 'tcp port 3333' isolates the TEXT protocol traffic. [sudo tcpdump -i eth0 -nn -A 'tcp port 3333' — indicatorul -nn dezactivează rezoluția numelor de gazdă și port, -A arată conținutul ASCII, iar filtrul BPF 'tcp port 3333' izolează traficul protocolului TEXT.]*


---

### Q41. `N04.S05.Q01` — Wireshark filter for SYN packets / Filtru Wireshark pentru pachete SYN

*[Multiple Choice]*

Which Wireshark display filter shows only TCP SYN packets (connection initiation)? [Care filtru de afișare Wireshark arată doar pachetele TCP SYN (inițierea conexiunii)?]

- **a)** tcp.flags.syn == 1 [tcp.flags.syn == 1]
- **b)** tcp.syn == true [tcp.syn == true]
- **c)** filter syn packets [filter syn packets]
- **d)** tcp.handshake == start [tcp.handshake == start]

> 💡 **Feedback:**
> *The filter tcp.flags.syn == 1 matches packets with the SYN flag set. To see only initial SYN (not SYN-ACK), use tcp.flags.syn == 1 && tcp.flags.ack == 0. [Filtrul tcp.flags.syn == 1 potrivește pachetele cu indicatorul SYN setat. Pentru a vedea doar SYN inițial (nu SYN-ACK), folosiți tcp.flags.syn == 1 && tcp.flags.ack == 0.]*


---

### Q42. `N04.S05.Q03` — tcpdump hex and ASCII dump flag / Indicatorul tcpdump pentru dump hex și ASCII

*[Multiple Choice]*

Which tcpdump flag displays both hexadecimal and ASCII content of captured packets? [Care indicator tcpdump afișează atât conținutul hexazecimal cât și ASCII al pachetelor capturate?]

- **a)** -XX — displays hex and ASCII dump including link-layer header bytes [-XX — afișează dump hex și ASCII inclusiv octeții antetului stratului de legătură]
- **b)** -A — this flag shows only ASCII content without hexadecimal output [-A — acest indicator arată doar conținut ASCII fără ieșire hexazecimală]
- **c)** -v — this flag increases verbosity of protocol header information [-v — acest indicator crește verbozitatea informațiilor de antet de protocol]
- **d)** -n — this flag disables hostname resolution for IP addresses shown [-n — acest indicator dezactivează rezoluția numelor de gazdă pentru adresele IP afișate]

> 💡 **Feedback:**
> *The -XX flag shows hex and ASCII dump of each packet including the link-layer header. -X shows hex+ASCII without link-layer header. -A shows only ASCII content. [Indicatorul -XX afișează dump-ul hex și ASCII al fiecărui pachet inclusiv antetul stratului de legătură. -X arată hex+ASCII fără antetul de legătură. -A arată doar conținut ASCII.]*


---

### Q43. `N04.S01.Q02` — recv_exact() loop rationale / Rațiunea buclei recv_exact()

*[Multiple Choice]*

The function recv_exact(sock, n) uses a while loop that accumulates chunks until exactly n bytes are received. Why is a single sock.recv(n) call insufficient? [Funcția recv_exact(sock, n) folosește o buclă while care acumulează fragmente până când exact n octeți sunt primiți. De ce un singur apel sock.recv(n) este insuficient?]

- **a)** recv(n) may return fewer than n bytes due to TCP segmentation or buffering [recv(n) poate returna mai puțin de n octeți din cauza segmentării TCP sau a buffering-ului]
- **b)** recv(n) blocks indefinitely unless called in a loop with a timeout value [recv(n) blochează nedefinit dacă nu este apelat într-o buclă cu o valoare de timeout]
- **c)** A single recv(n) call always raises an exception for any value of n above 1024 [Un singur apel recv(n) ridică întotdeauna o excepție pentru orice valoare a lui n peste 1024]
- **d)** The operating system requires multiple recv calls to release the socket buffer [Sistemul de operare necesită mai multe apeluri recv pentru a elibera buffer-ul socket-ului]

> 💡 **Feedback:**
> *sock.recv(n) returns up to n bytes but may deliver fewer due to TCP segmentation, network conditions, or OS buffer management. In production, packets frequently fragment, causing partial reads that a single call cannot handle. [sock.recv(n) returnează până la n octeți dar poate livra mai puțini din cauza segmentării TCP, condițiilor de rețea sau gestionării buffer-ului de SO. În producție, pachetele se fragmentează frecvent, provocând citiri parțiale pe care un singur apel nu le poate gestiona.]*


---

### Q44. `N04.S04.Q04` — sendto() for UDP datagrams / sendto() pentru datagrame UDP

*[Multiple Choice]*

Which Python socket method is used to transmit a UDP datagram to a specific destination address? [Ce metodă a socket-ului Python se folosește pentru a transmite o datagramă UDP la o adresă de destinație specifică?]

- **a)** sock.sendto(data, (host, port)) — transmits datagram to the specified address [sock.sendto(data, (host, port)) — transmite datagrama la adresa specificată]
- **b)** sock.send(data) — transmits data over a previously established connection [sock.send(data) — transmite date peste o conexiune stabilită anterior]
- **c)** sock.connect(data, (host, port)) — this method establishes connections only [sock.connect(data, (host, port)) — această metodă doar stabilește conexiuni]
- **d)** sock.write(data, address) — write() is for file I/O, not socket operations [sock.write(data, address) — write() este pentru I/O fișiere, nu operații socket]

> 💡 **Feedback:**
> *sock.sendto(data, (host, port)) transmits a datagram to the specified address without establishing a connection. Unlike TCP's send(), sendto() includes the destination address in each call since UDP is connectionless. [sock.sendto(data, (host, port)) transmite o datagramă la adresa specificată fără a stabili o conexiune. Spre deosebire de send() al TCP, sendto() include adresa de destinație în fiecare apel deoarece UDP este fără conexiune.]*


---

### Q45. `N04.S01.Q01` — Purpose of SO_REUSEADDR / Scopul opțiunii SO_REUSEADDR

*[Multiple Choice]*

Before calling bind(), the TEXT protocol server sets SO_REUSEADDR on the socket. What problem does this solve? [Înainte de a apela bind(), serverul protocolului TEXT setează SO_REUSEADDR pe socket. Ce problemă rezolvă aceasta?]

- **a)** It permits immediate rebinding to a port with lingering TIME_WAIT connections [Permite reasocierea imediată la un port cu conexiuni TIME_WAIT persistente]
- **b)** It increases the maximum number of simultaneous client connections allowed [Crește numărul maxim de conexiuni simultane de clienți permise]
- **c)** It enables TLS encryption on the socket for secure data transmission [Activează criptarea TLS pe socket pentru transmisia securizată a datelor]
- **d)** It reduces network latency by bypassing the TCP Nagle buffering algorithm [Reduce latența rețelei prin ocolirea algoritmului de buffering Nagle TCP]

> 💡 **Feedback:**
> *SO_REUSEADDR allows immediate rebinding to a port that has connections in TIME_WAIT state from a previous server instance. Without it, restarting the server quickly after a crash would fail with 'Address already in use'. [SO_REUSEADDR permite reasocierea imediată la un port care are conexiuni în starea TIME_WAIT de la o instanță anterioară a serverului. Fără aceasta, repornirea rapidă a serverului după o cădere ar eșua cu 'Address already in use'.]*


---

### Q46. `N04.S04.Q03` — Location field padding in UDP datagram / Completarea câmpului locație în datagrama UDP

*[Multiple Choice]*

The UDP sensor datagram allocates exactly 10 bytes for the location field. If the location string is 'Lab1' (4 bytes), how is it stored? [Datagrama senzorului UDP alocă exact 10 octeți pentru câmpul locație. Dacă șirul de locație este 'Lab1' (4 octeți), cum este stocat?]

- **a)** Left-justified, padded with null bytes (\\x00) to exactly 10 bytes total [Aliniată la stânga, completată cu octeți nuli (\\x00) la exact 10 octeți total]
- **b)** Right-justified, padded with space characters (0x20) on the left side [Aliniată la dreapta, completată cu caractere spațiu (0x20) pe partea stângă]
- **c)** Truncated to 4 bytes and the remaining 6 bytes are simply not transmitted [Trunchiată la 4 octeți iar restul de 6 octeți pur și simplu nu se transmit]
- **d)** Base64-encoded and then stored, expanding from 4 to approximately 8 bytes [Codificată Base64 și apoi stocată, expandându-se de la 4 la aproximativ 8 octeți]

> 💡 **Feedback:**
> *The location is left-justified and padded with null bytes (\\x00) to fill the 10-byte field: b'Lab1\\x00\\x00\\x00\\x00\\x00\\x00'. This is implemented with location.encode('utf-8').ljust(10)[:10]. [Locația este aliniată la stânga și completată cu octeți nuli (\\x00) pentru a umple câmpul de 10 octeți: b'Lab1\\x00\\x00\\x00\\x00\\x00\\x00'. Se implementează cu location.encode('utf-8').ljust(10)[:10].]*


---

## 🔬 Numerical (20 questions)


---

### Q47. `N01.C03.Q04` — UDP Header Size in Bytes / Dimensiunea antetului UDP în octeți

*[Numerical]*

What is the size of the UDP header in bytes? Enter just the number. [Care este dimensiunea antetului UDP în octeți? Introduceți doar numărul.]

> 💡 **Feedback:**
> *The UDP header is exactly (\...) bytes and contains four fields: source port (2 bytes), destination port (2 bytes), length (2 bytes), and checksum (2 bytes). By contrast, the TCP header is at least 20 bytes. [Antetul UDP are exact (\...) octeți și conține patru câmpuri: port sursă (2 octeți), port destinație (2 octeți), lungime (2 octeți) și sumă de control (2 octeți). Prin contrast, antetul TCP are cel puțin 20 de octeți.]*


---

### Q48. `N01.D03.Q04` — Bits in 1500 Bytes / Biți în 1500 octeți

*[Numerical]*

How many bits are in a 1500-byte Ethernet frame payload? Enter just the number. [Câți biți are un payload de cadru Ethernet de 1500 octeți? Introduceți doar numărul.]

> 💡 **Feedback:**
> *1500 bytes × 8 bits/byte = (\...) bits. This is the standard MTU for Ethernet. [1500 octeți × 8 biți/octet = (\...) biți. Aceasta este MTU-ul standard pentru Ethernet.]*


---

### Q49. `N01.D04.Q01` — Transmission Delay for Variable Packet / Întârzierea de transmisie pentru pachet variabil

*[Calculated]*

A packet of {packet_size} bytes is sent over a link with a capacity of {rate} Mbps. What is the transmission delay in microseconds? [Un pachet de {packet_size} octeți este trimis pe o legătură cu capacitatea de {rate} Mbps. Care este întârzierea de transmisie în microsecunde?]

> 💡 **Feedback:**
> *Transmission delay = (packet_size × 8) / (rate × 10⁶) × 10⁶ µs. This is the time to push all bits onto the wire, not the propagation time. [Întârzierea de transmisie = (packet_size × 8) / (rate × 10⁶) × 10⁶ µs. Aceasta este durata de plasare a tuturor biților pe mediu, nu timpul de propagare.]*


---

### Q50. `N01.D04.Q02` — Packet Size in Bits / Dimensiunea pachetului în biți

*[Calculated]*

An Ethernet frame carries a payload of {payload} bytes. The total frame (with {overhead} bytes of headers and trailer) is transmitted on the link. How many bits does the complete frame contain? [Un cadru Ethernet transportă o sarcină utilă de {payload} octeți. Cadrul total (cu {overhead} octeți de antet și trailer) este transmis pe legătură. Câți biți conține cadrul complet?]

> 💡 **Feedback:**
> *Total bits = (payload + overhead) × 8. Remember: 1 byte = 8 bits. [Biți totali = (payload + overhead) × 8. Rețineți: 1 octet = 8 biți.]*


---

### Q51. `N01.D04.Q06` — File Transfer Time / Durata transferului de fișier

*[Calculated]*

A file of {file_kb} KB is transferred over a link running at {rate} Mbps. Ignoring propagation delay and protocol overhead, how many milliseconds does the transmission take? [Un fișier de {file_kb} KB este transferat pe o legătură care funcționează la {rate} Mbps. Ignorând întârzierea de propagare și overhead-ul protocolului, câte milisecunde durează transmisia?]

> 💡 **Feedback:**
> *Time (ms) = (file_kb × 1024 × 8) / (rate × 10⁶) × 1000 = file_kb × 8.192 / rate. [Timp (ms) = (file_kb × 1024 × 8) / (rate × 10⁶) × 1000 = file_kb × 8,192 / rate.]*


---

### Q52. `N02.C02.Q05` — UDP header size in bytes / Dimensiunea antetului UDP în octeți

*[Numerical]*

What is the size of a UDP header in bytes? [Care este dimensiunea antetului UDP în octeți?]

> 💡 **Feedback:**
> *The UDP header is exactly (\...) bytes, containing four fields: source port, destination port, length, and checksum (each 2 bytes). In contrast, TCP headers are at least 20 bytes due to additional fields for sequence numbers, acknowledgements, and flow control. A common error is answering "20" — which is the minimum TCP header size, not UDP's. [Antetul UDP are exact (\...) octeți, conținând patru câmpuri: port sursă, port destinație, lungime și sumă de control (checksum) — fiecare de 2 octeți. Prin contrast, antetele TCP au minimum 20 de octeți datorită câmpurilor suplimentare pentru numere de secvență, confirmări (ACK) și controlul fluxului. O eroare frecventă este răspunsul „20" — aceasta fiind dimensiunea minimă a antetului TCP, nu a celui UDP.]*


---

### Q53. `N04.D03.Q01` — Binary header size in bytes / Dimensiunea antetului binar în octeți

*[Numerical]*

The BINARY protocol header format is '\>2sBBHII'. How many bytes is the total header? Enter a whole number. [Formatul antetului protocolului BINAR este '\>2sBBHII'. Câți octeți are antetul total? Introduceți un număr întreg.]

> 💡 **Feedback:**
> *2(2s) + 1(B) + 1(B) + 2(H) + 4(I) + 4(I) = (\...) bytes. [2(2s) + 1(B) + 1(B) + 2(H) + 4(I) + 4(I) = (\...) octeți.]*


---

### Q54. `N04.D03.Q02` — UDP sensor datagram size / Dimensiunea datagramei senzorului UDP

*[Numerical]*

The UDP sensor datagram has fields: version(1B), sensor_id(4B), temp(4B), location(10B), CRC32(4B). Total size in bytes? [Datagrama senzorului UDP are câmpurile: version(1O), sensor_id(4O), temp(4O), location(10O), CRC32(4O). Dimensiunea totală în octeți?]

> 💡 **Feedback:**
> *1 + 4 + 4 + 10 + 4 = (\...) bytes. [1 + 4 + 4 + 10 + 4 = (\...) octeți.]*


---

### Q55. `N04.D03.Q03` — Endianness misinterpretation of 1000 / Interpretarea greșită a 1000 din cauza endianness

*[Numerical]*

Value 1000 is packed as big-endian unsigned short ('\>H'). If the receiver reads it as little-endian ('H'). Dacă receptorul o citește ca little-endian ('\<H'), ce valoare zecimală rezultă?]

> 💡 **Feedback:**
> *1000 = 0x03E8. Big-endian: [03][E8]. Read as little-endian: 0xE803 = 232\*3 + 8\*256 = (\...). [1000 = 0x03E8. Big-endian: [03][E8]. Citit ca little-endian: 0xE803 = (\...).]*


---

### Q56. `N04.D03.Q04` — TEXT protocol frame size for 13-byte payload / Dimensiunea cadrului TEXT pentru sarcină utilă de 13 octeți

*[Numerical]*

The TEXT protocol uses " " framing where LENGTH is ASCII decimal. For payload "SET key value" (13 bytes), how many bytes is the complete frame? [Protocolul TEXT folosește cadrajul " " unde LUNGIME este zecimal ASCII. Pentru sarcina utilă "SET key value" (13 octeți), câți octeți are cadrul complet?]

> 💡 **Feedback:**
> *"13 SET key value" = 2 (ASCII digits "13") + 1 (space) + 13 (payload) = (\...) bytes total. ["13 SET key value" = 2 (cifrele ASCII "13") + 1 (spațiu) + 13 (sarcină utilă) = (\...) octeți total.]*


---

### Q57. `N04.D03.Q06` — struct.pack header without CRC size / Dimensiunea antetului struct.pack fără CRC

*[Numerical]*

The header without CRC is packed with format '\>2sBBHI'. How many bytes does this produce? [Antetul fără CRC este împachetat cu formatul '\>2sBBHI'. Câți octeți produce?]

> 💡 **Feedback:**
> *2(2s) + 1(B) + 1(B) + 2(H) + 4(I) = (\...) bytes. [2(2s) + 1(B) + 1(B) + 2(H) + 4(I) = (\...) octeți.]*


---

### Q58. `N04.D03.Q08` — PAM-4 bits per symbol / Biți per simbol PAM-4

*[Numerical]*

PAM-4 uses 4 amplitude levels. How many bits does each symbol encode? [PAM-4 folosește 4 niveluri de amplitudine. Câți biți codifică fiecare simbol?]

> 💡 **Feedback:**
> *log₂(4) = (\...) bits per symbol. [log₂(4) = (\...) biți per simbol.]*


---

### Q59. `N04.D04.Q01` — Binary header total size / Dimensiunea totală a antetului binar

*[Calculated]*

A binary protocol header contains: magic ({a} bytes), version (1 byte), type (1 byte), payload_length ({b} bytes), sequence ({c} bytes), and CRC32 (4 bytes). What is the total header size in bytes? [Un antet de protocol binar conține: magic ({a} octeți), versiune (1 octet), tip (1 octet), lungime_payload ({b} octeți), secvență ({c} octeți) și CRC32 (4 octeți). Care este dimensiunea totală a antetului în octeți?]

> 💡 **Feedback:**
> *Total = {a} + 1 + 1 + {b} + {c} + 4. For the Week 4 binary protocol (magic=2, payload_len=2, seq=4), total = 14 bytes. [Total = {a} + 1 + 1 + {b} + {c} + 4. Pentru protocolul binar din Săptămâna 4 (magic=2, payload_len=2, seq=4), total = 14 octeți.]*


---

### Q60. `N04.D04.Q02` — Frame overhead percentage / Procentul de overhead al cadrului

*[Calculated]*

A protocol frame has a fixed header of 14 bytes and a payload of {a} bytes. What is the overhead percentage? Round to one decimal place. (Formula: overhead = header / (header + payload) × 100) [Un cadru de protocol are un antet fix de 14 octeți și un payload de {a} octeți. Care este procentul de overhead? Rotunjiți la o zecimală. (Formula: overhead = antet / (antet + payload) × 100)]

> 💡 **Feedback:**
> *Overhead = 14 / (14 + {a}) × 100. Smaller payloads yield higher overhead, which is why binary protocols are preferred for frequent small messages. [Overhead = 14 / (14 + {a}) × 100. Payloadurile mai mici generează overhead mai mare, motiv pentru care protocoalele binare sunt preferate pentru mesaje mici frecvente.]*


---

### Q61. `N04.D04.Q03` — Endianness misinterpretation / Interpretare greșită a endianness-ului

*[Calculated]*

A sender packs the value {a} as a 2-byte big-endian unsigned short. The receiver mistakenly unpacks it as little-endian. What decimal value does the receiver obtain? (Hint: swap the two bytes of the 16-bit representation.) [Expeditorul împachetează valoarea {a} ca un unsigned short de 2 octeți big-endian. Receptorul dezarhivează greșit ca little-endian. Ce valoare zecimală obține receptorul? (Indiciu: inversați cei doi octeți ai reprezentării pe 16 biți.)]

> 💡 **Feedback:**
> *For value V in [256..65279], the big-endian bytes are [V\>\>8, V&0xFF]. Reading as little-endian gives (V&0xFF)×256 + (V\>\>8). This demonstrates why network byte order consistency is critical. [Pentru valoarea V în [256..65279], octeții big-endian sunt [V\>\>8, V&0xFF]. Citirea ca little-endian dă (V&0xFF)×256 + (V\>\>8). Aceasta demonstrează de ce consistența ordinii octeților de rețea este critică.]*


---

### Q62. `N04.D04.Q04` — Text frame total size / Dimensiunea totală a cadrului text

*[Calculated]*

In the TEXT protocol, a message is framed as " ". If the payload is "{a} SET key value" ({a} characters), the length prefix is the ASCII representation of {a} followed by a space. How many bytes is the complete frame? (Length prefix chars + 1 space + payload bytes) [În protocolul TEXT, un mesaj este încadrat ca " ". Dacă payloadul este "{a} SET key value" ({a} caractere), prefixul de lungime este reprezentarea ASCII a lui {a} urmată de un spațiu. Câți octeți are cadrul complet? (Caractere prefix lungime + 1 spațiu + octeți payload)]

> 💡 **Feedback:**
> *The length prefix "{a}" is ceil(log10({a}+1)) ASCII digits, plus 1 space, plus {a} payload bytes. For a two-digit length like 13: "13 " (3 bytes) + 13 bytes = 16 total. [Prefixul de lungime "{a}" este ceil(log10({a}+1)) cifre ASCII, plus 1 spațiu, plus {a} octeți payload. Pentru o lungime de două cifre ca 13: "13 " (3 octeți) + 13 octeți = 16 total.]*


---

### Q63. `N04.D04.Q05` — Binary message total bytes / Total octeți mesaj binar

*[Calculated]*

A binary protocol message consists of a 14-byte header followed by the payload. If the key is {a} characters and the value is {b} characters, and the payload encoding uses 1 byte for key_length + key + value, how many total bytes does the entire message occupy? [Un mesaj de protocol binar constă dintr-un antet de 14 octeți urmat de payload. Dacă cheia are {a} caractere și valoarea are {b} caractere, iar codificarea payload-ului folosește 1 octet pentru lungime_cheie + cheie + valoare, câți octeți totali ocupă întregul mesaj?]

> 💡 **Feedback:**
> *Total = 14 (header) + 1 (key_length byte) + {a} (key) + {b} (value) = 15 + {a} + {b}. The key_length field uses 1 byte (struct 'B') as defined in proto_common.py encode_kv(). [Total = 14 (antet) + 1 (octet lungime_cheie) + {a} (cheie) + {b} (valoare) = 15 + {a} + {b}. Câmpul lungime_cheie folosește 1 octet (struct 'B') conform definiției din proto_common.py encode_kv().]*


---

### Q64. `N04.D04.Q06` — UDP sensor useful data ratio / Raportul datelor utile senzor UDP

*[Calculated]*

The UDP sensor datagram is 23 bytes total. The useful data fields are: sensor_id (4 bytes) and temperature ({a} bytes). The remaining fields (version, location, CRC32) are protocol overhead. What percentage of the datagram carries useful sensor readings? Round to one decimal. [Datagrama senzorului UDP are 23 de octeți în total. Câmpurile de date utile sunt: sensor_id (4 octeți) și temperatură ({a} octeți). Câmpurile rămase (versiune, locație, CRC32) sunt overhead de protocol. Ce procent din datagramă transportă citiri utile ale senzorilor? Rotunjiți la o zecimală.]

> 💡 **Feedback:**
> *Useful = 4 + {a} bytes. Percentage = (4 + {a}) / 23 × 100. For the standard 4-byte float: (4+4)/23 × 100 = 34.8%. The location field (10B) and CRC (4B) are overhead necessary for identification and integrity. [Util = 4 + {a} octeți. Procent = (4 + {a}) / 23 × 100. Pentru float-ul standard de 4 octeți: (4+4)/23 × 100 = 34.8%. Câmpul locație (10B) și CRC (4B) sunt overhead necesar pentru identificare și integritate.]*


---

### Q65. `N04.D04.Q07` — struct.pack output size / Dimensiunea ieșirii struct.pack

*[Calculated]*

Given the struct format string '\>{a}sBBHI', how many bytes does struct.pack() produce? (Recall: s=1 byte per char, B=1 byte, H=2 bytes, I=4 bytes) [Dată fiind secvența de format struct '\>{a}sBBHI', câți octeți produce struct.pack()? (Amintiți-vă: s=1 octet/caracter, B=1 octet, H=2 octeți, I=4 octeți)]

> 💡 **Feedback:**
> *Total = {a} (from {a}s) + 1 (B) + 1 (B) + 2 (H) + 4 (I) = {a} + 8 bytes. The struct module calculates sizes based on format characters; the '\>' prefix specifies big-endian but adds no bytes. [Total = {a} (din {a}s) + 1 (B) + 1 (B) + 2 (H) + 4 (I) = {a} + 8 octeți. Modulul struct calculează dimensiunile pe baza caracterelor de format; prefixul '\>' specifică big-endian, dar nu adaugă octeți.]*


---

### Q66. `N04.D04.Q08` — Bandwidth savings binary vs text / Economie lățime de bandă binar vs text

*[Calculated]*

A sensor sends {a} readings per minute. The text protocol frame is 35 bytes per reading (length prefix + ASCII payload). The binary protocol frame is 23 bytes per reading (fixed datagram). Over one hour, how many kilobytes of bandwidth does the binary protocol save compared to text? (Answer as integer KB, where 1 KB = 1024 bytes.) [Un senzor trimite {a} citiri pe minut. Cadrul protocolului text are 35 de octeți pe citire (prefix lungime + payload ASCII). Cadrul protocolului binar are 23 de octeți pe citire (datagramă fixă). Pe parcursul unei ore, câți kiloocteți de lățime de bandă economisește protocolul binar față de cel text? (Răspundeți ca KB întreg, unde 1 KB = 1024 octeți.)]

> 💡 **Feedback:**
> *Readings/hour = {a} × 60. Text total = {a}×60×35 bytes. Binary total = {a}×60×23 bytes. Savings = {a}×60×(35-23) = {a}×60×12 bytes. In KB = {a}×720/1024. This illustrates why binary protocols matter for high-frequency IoT data. [Citiri/oră = {a} × 60. Total text = {a}×60×35 octeți. Total binar = {a}×60×23 octeți. Economie = {a}×60×(35-23) = {a}×60×12 octeți. În KB = {a}×720/1024. Aceasta ilustrează de ce protocoalele binare contează pentru date IoT de frecvență mare.]*


---

## 🔬 Drag & Drop (4 questions)


---

### Q67. `N04.D05.Q03` — Complete struct.pack call for binary header / Completați apelul struct.pack pentru antetul binar

*[Drag & Drop into Text]*

Complete the struct.pack() call to build the binary header with CRC: [Completați apelul struct.pack() pentru a construi antetul binar cu CRC:]
header = struct.pack('[[1]]2sBBHII', MAGIC, VERSION, msg_type, payload_len, seq, [[2]])
*Available choices / Variante disponibile:* \> | crc | \< | seq | ! | version

> 💡 **Feedback:**
> *The format prefix '\>' specifies big-endian (network byte order). The last field is the CRC32 value. Format: \>2sBBHII = magic(2) + ver(1) + type(1) + len(2) + seq(4) + crc(4) = 14 bytes. [Prefixul de format '\>' specifică big-endian (ordinea octeților în rețea). Ultimul câmp este valoarea CRC32. Format: \>2sBBHII = magic(2) + ver(1) + tip(1) + lungime(2) + seq(4) + crc(4) = 14 octeți.]*


---

### Q68. `N04.D05.Q06` — Complete UDP sensor pack call / Completați apelul de împachetare al senzorului UDP

*[Drag & Drop into Text]*

Complete the struct.pack for the UDP sensor datagram (without CRC): [Completați struct.pack pentru datagrama senzorului UDP (fără CRC):]
payload = struct.pack('\>[[1]][[2]]f[[3]]', VERSION, sensor_id, temp, location_bytes)
*Available choices / Variante disponibile:* B | I | 10s | H | Q | 4s

> 💡 **Feedback:**
> *Format: \>BIf10s — B for version (1 byte), I for sensor_id (4 bytes unsigned int), f for temperature (4 bytes float), 10s for location (10 bytes string). [Format: \>BIf10s — B pentru versiune (1 octet), I pentru sensor_id (4 octeți unsigned int), f pentru temperatură (4 octeți float), 10s pentru locație (10 octeți șir).]*


---

### Q69. `N04.D05.Q01` — Build tcpdump command for binary protocol / Construiți comanda tcpdump pentru protocolul binar

*[Drag & Drop into Text]*

Build the tcpdump command that captures BINARY protocol traffic in hex dump mode without hostname resolution: [Construiți comanda tcpdump care capturează traficul protocolului BINAR în mod hex dump fără rezoluție de nume de gazdă:]
sudo [[1]] -i eth0 [[2]] [[3]] 'tcp port [[4]]'
*Available choices / Variante disponibile:* tcpdump | -nn | -XX | 5401 | curl | -A | 3333 | 5402

> 💡 **Feedback:**
> *tcpdump -nn -XX captures TCP port 5401 traffic in hex+ASCII mode without name resolution. -nn disables both host and port resolution. [tcpdump -nn -XX capturează traficul TCP portul 5401 în mod hex+ASCII fără rezoluție de nume. -nn dezactivează rezoluția numelor de gazdă și port.]*


---

### Q70. `N04.D05.Q05` — Build recv_exact function call / Construiți apelul funcției recv_exact

*[Drag & Drop into Text]*

Complete the recv_exact helper to receive exactly n bytes: [Completați helper-ul recv_exact pentru a primi exact n octeți:]

```python
while len(data) < n:
    chunk = sock.[[1]](n - [[2]](data))
    if not chunk:
        raise [[3]]("closed")
```

*Available choices / Variante disponibile:* recv | len | ConnectionError | send | size | ValueError

> 💡 **Feedback:**
> *sock.recv(n - len(data)) requests at most the remaining bytes needed. An empty chunk (not chunk) means the peer closed the connection, raising ConnectionError. [sock.recv(n - len(data)) solicită cel mult octeții rămași necesari. Un fragment gol (not chunk) înseamnă că partenerul a închis conexiunea, ridicând ConnectionError.]*


---

## 🔬 Gap Select (5 questions)


---

### Q71. `N04.D10.Q01` — Physical Layer converts / Stratul fizic convertește

*[Gap Select]*

The Physical Layer converts [[1]] into [[2]] for transmission across a physical medium. [Stratul fizic convertește ___ în ___ pentru transmisia prin mediul fizic.]
*Available choices / Variante disponibile:* bits | frames | packets | signals | segments | datagrams

> 💡 **Feedback:**
> *The Physical Layer (L1) transforms digital bits into physical signals — electrical, optical, or radio. [Stratul fizic (L1) transformă biții digitali în semnale fizice — electrice, optice sau radio.]*


---

### Q72. `N04.D10.Q03` — TCP stream property / Proprietatea fluxului TCP

*[Gap Select]*

TCP is a [[1]] protocol that does not preserve message [[2]]. Applications must implement their own [[3]] mechanism. [TCP este un protocol ___ care nu păstrează ___ mesajelor. Aplicațiile trebuie să implementeze propriul mecanism de ___.]
*Available choices / Variante disponibile:* byte stream | datagram | message-oriented | boundaries | checksums | ports | framing | routing | encryption

> 💡 **Feedback:**
> *TCP provides a reliable byte stream with no concept of message boundaries. Length-prefix framing is one common solution used in the Week 4 TEXT and BINARY protocols. [TCP oferă un flux fiabil de octeți fără conceptul de limite ale mesajelor. Încadrarea cu prefix de lungime este o soluție comună, utilizată în protocoalele TEXT și BINAR din Săptămâna 4.]*


---

### Q73. `N04.D10.Q05` — Manchester encoding clock / Ceasul codării Manchester

*[Gap Select]*

Manchester encoding embeds [[1]] information by requiring a [[2]] in the middle of each bit period. [Codarea Manchester înglobează informațiile de ___ prin necesitatea unei ___ la mijlocul fiecărei perioade de bit.]
*Available choices / Variante disponibile:* clock | error | routing | transition | collision | retransmission

> 💡 **Feedback:**
> *Manchester encoding guarantees at least one transition per bit, enabling receiver clock recovery. [Codarea Manchester garantează cel puțin o tranziție per bit, permițând recuperarea ceasului la receptor.]*


---

### Q74. `N04.D10.Q06` — CSMA/CD vs CSMA/CA / CSMA/CD vs CSMA/CA

*[Gap Select]*

Wired Ethernet uses CSMA/[[1]] for collision [[2]], whilst Wi-Fi uses CSMA/[[3]] for collision [[4]]. [Ethernet-ul cablat folosește CSMA/___ pentru ___ coliziunilor, în timp ce Wi-Fi folosește CSMA/___ pentru ___ coliziunilor.]
*Available choices / Variante disponibile:* CD | CA | CR | detection | correction | compression | CA | CD | CT | avoidance | detection | prevention

> 💡 **Feedback:**
> *CSMA/CD (Collision Detection) terminates transmission on collision; CSMA/CA (Collision Avoidance) tries to prevent collisions before they occur. [CSMA/CD (detectarea coliziunilor) termină transmisia la coliziune; CSMA/CA (evitarea coliziunilor) încearcă prevenirea coliziunilor înainte să apară.]*


---

### Q75. `N04.D10.Q07` — UDP datagram boundaries / Limitele datagramelor UDP

*[Gap Select]*

Unlike TCP, UDP preserves message [[1]] because each send produces exactly one [[2]]. [Spre deosebire de TCP, UDP păstrează ___ mesajelor deoarece fiecare trimitere produce exact o ___.]
*Available choices / Variante disponibile:* boundaries | checksums | headers | datagram | segment | frame

> 💡 **Feedback:**
> *UDP datagrams are discrete units — each sendto() creates one datagram that is delivered atomically. [Datagramele UDP sunt unități discrete — fiecare sendto() creează o datagramă livrată atomic.]*
