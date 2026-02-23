# Computer Networks — Week 9: Question Pool

#### Rețele de Calculatoare — Săptămâna 9: Banca de Întrebări

> OSI Session & Presentation Layers, FTP (Active/Passive), PASV, struct / Binary Protocols, CRC-32, Endianness
> 53 questions  •  Bilingual EN/RO

---


## §1.  Curs / Lecture   (28 questions)

### Q1. `Multiple Choice`
**OSI Layer Responsible for Dialogue Control and Checkpoints / Stratul OSI responsabil de controlul dialogului și punctele de sincronizare**

> Which OSI layer is responsible for managing dialogue control, authentication state, and synchronisation checkpoints between communicating applications? [Care strat OSI este responsabil de gestionarea controlului dialogului, a stării de autentificare și a punctelor de sincronizare între aplicațiile comunicante?]

- **a)  Layer 5 (Session) [Nivelul 5 (Sesiune)]**
- **b)  Layer 4 (Transport) [Nivelul 4 (Transport)]**
- **c)  Layer 6 (Presentation) [Nivelul 6 (Prezentare)]**
- **d)  Layer 7 (Application) [Nivelul 7 (Aplicație)]**

> 💡 **Feedback:** The Session Layer (Layer 5) manages logical dialogues, including authentication, checkpoint synchronisation, and dialogue control (half-duplex versus full-duplex). A common misconception is to confuse it with the Transport Layer (L4), which only provides reliable byte delivery without any concept of user identity or application state. [Stratul sesiune (nivelul 5) gestionează dialogurile logice, inclusiv autentificarea, sincronizarea prin puncte de control și controlul dialogului (half-duplex versus full-duplex). O concepție greșită frecventă este confuzia cu Stratul de transport (L4), care oferă doar livrarea fiabilă a octeților, fără nicio noțiune de identitate a utilizatorului sau stare a aplicației.]

---

### Q2. `Multiple Choice`
**FTP Session State After TCP Reconnection / Starea sesiunii FTP după reconectarea TCP**

> A user is authenticated on an FTP server, browsing /home/test/documents . The network cable is unplugged for 30 seconds and the TCP connection drops. After the cable is reconnected and a new TCP connection is established, what is the user's FTP session state? [Un utilizator este autentificat pe un server FTP, navigând în /home/test/documents . Cablul de rețea este deconectat timp de 30 de secunde, iar conexiunea TCP se pierde. După reconectarea cablului și stabilirea unei noi conexiuni TCP, care este starea sesiunii FTP a utilizatorului?]

- **a)  Session is lost — re-authentication with USER/PASS is required [Sesiunea este pierdută — reautentificarea cu USER/PASS este necesară]**
- **b)  Session is preserved — TCP handles reconnection transparently [Sesiunea este păstrată — TCP gestionează reconectarea transparent]**
- **c)  Session is cached by the server for 5 minutes by default [Sesiunea este reținută în cache de server timp de 5 minute implicit]**
- **d)  Authentication is preserved but the current working directory resets to / (root) [Autentificarea este păstrată, dar directorul curent de lucru revine la / (rădăcină)]**

> 💡 **Feedback:** FTP session state (authentication, current directory, transfer mode) is tied to the TCP connection. When TCP drops, all session state is lost and the user must re-authenticate. A common misconception is that TCP handles reconnection transparently, but TCP has no concept of "user" or "login" — these are Session Layer (L5) concerns maintained by the application protocol. [Starea sesiunii FTP (autentificare, directorul curent, modul de transfer) este legată de conexiunea TCP. Când conexiunea TCP se pierde, întreaga stare a sesiunii este pierdută, iar utilizatorul trebuie să se reautentifice. O concepție greșită frecventă este că TCP gestionează reconectarea în mod transparent, însă TCP nu are nicio noțiune de «utilizator» sau «autentificare» — acestea sunt preocupări ale Stratului sesiune (L5), menținute de protocolul aplicației.]

---

### Q3. `Multiple Choice`
**TCP Connection vs Session — Identity / Conexiune TCP vs. sesiune — identitate**

> What distinguishes Session Layer (L5) identity from Transport Layer (L4) identity? [Ce deosebește identitatea la Stratul sesiune (L5) de identitatea la Stratul de transport (L4)?]

- **a)  TCP uses IP:port pairs (anonymous); sessions use authenticated user-to-service identity [TCP folosește perechi IP:port (anonime); sesiunile folosesc identitatea autentificată utilizator-serviciu]**
- **b)  TCP uses MAC addresses; sessions use IP addresses [TCP folosește adrese MAC; sesiunile folosesc adrese IP]**
- **c)  Both use identical identification mechanisms [Ambele folosesc mecanisme de identificare identice]**
- **d)  TCP uses authenticated credentials for identification; sessions use anonymous port numbers without user context [TCP folosește credențiale autentificate pentru identificare; sesiunile folosesc numere de port anonime fără context de utilizator]**

> 💡 **Feedback:** TCP connections identify endpoints by IP:port pairs, which are anonymous, whereas sessions identify an authenticated user communicating with a service. A common misconception is that both layers use identical identification mechanisms, but TCP provides no authentication — it merely routes bytes between network addresses. [Conexiunile TCP identifică punctele terminale prin perechi IP:port, care sunt anonime, în timp ce sesiunile identifică un utilizator autentificat care comunică cu un serviciu. O concepție greșită frecventă este că ambele straturi folosesc mecanisme de identificare identice, însă TCP nu oferă autentificare — doar transportă octeți între adrese de rețea.]

---

### Q4. `True / False`
**Session Can Span Multiple TCP Connections / Sesiunea poate traversa mai multe conexiuni TCP**

> An application-level session (such as an HTTP session using cookies) can span multiple TCP connections. [O sesiune la nivel de aplicație (cum ar fi o sesiune HTTP care utilizează cookie-uri) poate traversa mai multe conexiuni TCP.]

- **a)  true**
- **b)  false**

> 💡 **Feedback:** True. HTTP sessions use cookies to maintain identity across multiple TCP connections. However, standard FTP does not support this — its session is tied to a single TCP control connection. A common misconception is assuming all protocols handle sessions identically; in reality, session persistence depends entirely on application-layer design. [Adevărat. Sesiunile HTTP folosesc cookie-uri pentru a menține identitatea peste mai multe conexiuni TCP. Cu toate acestea, protocolul FTP standard nu suportă acest lucru — sesiunea sa este legată de o singură conexiune TCP de control. O concepție greșită frecventă este presupunerea că toate protocoalele gestionează sesiunile la fel; în realitate, persistența sesiunii depinde în întregime de proiectarea la nivelul aplicației.]

---

### Q5. `Multiple Choice`
**Resume Point After Interrupted Transfer with Checkpoints / Punctul de reluare după un transfer întrerupt cu puncte de sincronizare**

> A 100 MB file transfer uses session-layer checkpointing. The connection drops after 35 MB have been sent. On reconnection, from what point does the transfer resume? [Un transfer de fișier de 100 MB utilizează puncte de sincronizare la Stratul sesiune. Conexiunea se pierde după ce s-au trimis 35 MB. La reconectare, din ce punct se reia transferul?]

- **a)  From the last confirmed checkpoint (e.g. 30 MB) [De la ultimul punct de sincronizare confirmat (de ex. 30 MB)]**
- **b)  From 0 MB — the entire file must be re-transferred [De la 0 MB — întregul fișier trebuie retransferat]**
- **c)  From exactly 35 MB — the exact interruption point [Exact de la 35 MB — punctul exact al întreruperii]**
- **d)  The transfer fails permanently and cannot be resumed [Transferul eșuează permanent și nu poate fi reluat]**

> 💡 **Feedback:** Checkpointing saves progress at defined intervals. The transfer resumes from the last confirmed checkpoint (e.g. 30 MB), not from the exact interruption point, because data after the last checkpoint was never confirmed received. A common misconception is that the transfer resumes from exactly 35 MB, but unconfirmed data between the last checkpoint and the interruption point cannot be trusted. [Punctele de sincronizare salvează progresul la intervale definite. Transferul se reia de la ultimul punct de sincronizare confirmat (de ex. 30 MB), nu de la punctul exact al întreruperii, deoarece datele de după ultimul punct de sincronizare nu au fost niciodată confirmate ca primite. O concepție greșită frecventă este că transferul se reia exact de la 35 MB, dar datele neconfirmate dintre ultimul punct de sincronizare și punctul întreruperii nu pot fi considerate fiabile.]

---

### Q6. `Multiple Choice`
**Synchronisation Points in the Session Layer / Puncte de sincronizare la Stratul sesiune**

> Which Session Layer mechanism allows a sender to confirm the receiver has successfully processed data before continuing the transfer? [Care mecanism al Stratului sesiune permite expeditorului să confirme că receptorul a procesat cu succes datele înainte de a continua transferul?]

- **a)  Synchronisation points (checkpoints) [Puncte de sincronizare (checkpoint-uri)]**
- **b)  Flow control via sliding window [Controlul fluxului prin fereastră glisantă]**
- **c)  Error correction (FEC) [Corecția erorilor (FEC)]**
- **d)  Multiplexing [Multiplexare]**

> 💡 **Feedback:** Synchronisation points (checkpoints) are Session Layer mechanisms marking confirmed progress. A common misconception is to confuse them with flow control (a Transport Layer function using the sliding window) or error correction (a Data Link/Transport function). Checkpoints operate at a higher abstraction level, tracking application-meaningful progress milestones. [Punctele de sincronizare (checkpoint-urile) sunt mecanisme ale Stratului sesiune care marchează progresul confirmat. O concepție greșită frecventă este confuzia cu controlul fluxului (o funcție a Stratului de transport care utilizează fereastra glisantă) sau cu corecția erorilor (funcție a Stratului legătură de date/Transport). Punctele de sincronizare operează la un nivel de abstractizare superior, urmărind jaloanele de progres semnificative pentru aplicație.]

---

### Q7. `Multiple Choice`
**Presentation Layer Responsibilities / Responsabilitățile Stratului prezentare**

> Which of the following is a primary responsibility of the Presentation Layer (Layer 6)? [Care dintre următoarele este o responsabilitate principală a Stratului prezentare (nivelul 6)?]

- **a)  Data serialisation, encoding, compression, and encryption [Serializarea datelor, codificarea, compresia și criptarea]**
- **b)  Routing packets between networks [Rutarea pachetelor între rețele]**
- **c)  Flow control and congestion management [Controlul fluxului și gestionarea congestiei]**
- **d)  Dialogue control and session checkpointing between applications [Controlul dialogului și punctele de sincronizare ale sesiunii între aplicații]**

> 💡 **Feedback:** The Presentation Layer handles data syntax transformations: serialisation, encoding (character sets), compression, and encryption. A common misconception is to confuse it with routing (Layer 3), flow control (Layer 4), or dialogue control (Layer 5). The Presentation Layer's role is ensuring that data exchanged between applications is in a mutually understood format. [Stratul prezentare se ocupă de transformările sintactice ale datelor: serializare, codificare (seturi de caractere), compresie și criptare. O concepție greșită frecventă este confuzia cu rutarea (nivelul 3), controlul fluxului (nivelul 4) sau controlul dialogului (nivelul 5). Rolul Stratului prezentare este de a asigura că datele schimbate între aplicații sunt într-un format reciproc inteligibil.]

---

### Q8. `Multiple Choice`
**Serialisation Format for High-Performance Typed Data / Format de serializare pentru date tipizate de înaltă performanță**

> Which serialisation format is a binary, typed, high-performance alternative to JSON, commonly used in gRPC? [Care format de serializare este o alternativă binară, tipizată și de înaltă performanță la JSON, folosită frecvent în gRPC?]

- **a)  Protocol Buffers (protobuf)**
- **b)  JSON (text-based, human-readable format) [JSON (format bazat pe text, lizibil)]**
- **c)  XML (hierarchical text-based markup) [XML (markup ierarhic bazat pe text)]**
- **d)  CSV (tabular plain-text data format) [CSV (format tabelar de date în text)]**

> 💡 **Feedback:** Protocol Buffers (protobuf) is a binary, typed serialisation format designed for high performance, commonly used with gRPC. A common misconception is that JSON is equally performant for all use cases, but JSON is text-based and requires parsing overhead. Protocol Buffers encode data in compact binary with strict schemas. [Protocol Buffers (protobuf) este un format de serializare binar, tipizat, proiectat pentru performanță ridicată, folosit frecvent cu gRPC. O concepție greșită frecventă este că JSON este la fel de performant în toate cazurile de utilizare, însă JSON este bazat pe text și necesită overhead de parsare. Protocol Buffers codifică datele în format binar compact cu scheme stricte.]

---

### Q9. `Multiple Choice`
**Variable-Length Data Encoding Approaches / Abordări de codificare a datelor cu lungime variabilă**

> A developer needs to transmit variable-length strings over a binary protocol. Which approach correctly handles arbitrary-length data in a Presentation Layer encoding scheme? [Un dezvoltator trebuie să transmită șiruri de caractere cu lungime variabilă printr-un protocol binar. Care abordare gestionează corect datele cu lungime arbitrară într-o schemă de codificare a Stratului prezentare?]

- **a)  Length-prefixed: a 4-byte integer indicating string length, then that many UTF-8 bytes [Cu prefix de lungime: un întreg pe 4 octeți indicând lungimea șirului, apoi acel număr de octeți UTF-8]**
- **b)  Fixed-width: pad all strings to 256 bytes regardless of actual length [Lățime fixă: completarea tuturor șirurilor la 256 de octeți indiferent de lungimea reală]**
- **c)  Delimiter-based: end every string with the reserved byte 0xFF, which cannot appear inside payload data [Bazat pe delimitator: terminarea fiecărui șir cu octetul rezervat 0xFF, care nu poate apărea în datele utile]**
- **d)  Implicit-length: the receiver infers the string length from the TCP segment size [Lungime implicită: receptorul deduce lungimea șirului din dimensiunea segmentului TCP]**

> 💡 **Feedback:** Length-prefixed encoding (e.g., a 4-byte length field followed by that many bytes of UTF-8 data) is the standard Presentation Layer approach for variable-length data. A common misconception is that inferring message length from the TCP segment size works — but TCP is a byte stream with no message boundaries, so segment sizes are unreliable indicators of application message length. [Codificarea cu prefix de lungime (de ex. un câmp de 4 octeți indicând lungimea, urmat de acel număr de octeți de date UTF-8) este abordarea standard a Stratului prezentare pentru date cu lungime variabilă. O concepție greșită frecventă este că lungimea mesajului poate fi dedusă din dimensiunea segmentului TCP — dar TCP este un flux de octeți fără delimitarea mesajelor, deci dimensiunile segmentelor nu sunt indicatori fiabili ai lungimii mesajelor aplicației.]

---

### Q10. `Multiple Choice`
**Number of TCP Connections in an FTP File Download / Numărul de conexiuni TCP la descărcarea unui fișier prin FTP**

> When a client connects to an FTP server and downloads a single file, how many separate TCP connections are used? [Când un client se conectează la un server FTP și descarcă un singur fișier, câte conexiuni TCP separate sunt utilizate?]

- **a)  2 — one control channel (port 21) and one data channel (dynamic) [2 — un canal de control (portul 21) și un canal de date (dinamic)]**
- **b)  1 — commands and data share a single connection like HTTP [1 — comenzile și datele partajează o singură conexiune ca la HTTP]**
- **c)  3 — one for authentication, one for control commands, and one for data transfer [3 — una pentru autentificare, una pentru comenzile de control, și una pentru transfer de date]**
- **d)  4 — a separate connection for each FTP command issued [4 — o conexiune separată pentru fiecare comandă FTP emisă]**

> 💡 **Feedback:** FTP uses exactly two TCP connections: a persistent control connection (port 21) for commands and responses, and a temporary data connection (dynamic port) for the file transfer. A common misconception is that FTP uses a single connection like HTTP. The dual-channel architecture is a defining characteristic of FTP that enables features like out-of-band control during transfer. [FTP folosește exact două conexiuni TCP: o conexiune de control persistentă (portul 21) pentru comenzi și răspunsuri, și o conexiune de date temporară (port dinamic) pentru transferul fișierului. O concepție greșită frecventă este că FTP folosește o singură conexiune ca HTTP. Arhitectura cu canal dublu este o caracteristică definitorie a FTP care permite funcționalități precum controlul în bandă separată (out-of-band) în timpul transferului.]

---

### Q11. `Multiple Choice`
**Who Initiates the Data Connection in FTP Passive Mode / Cine inițiază conexiunea de date în modul pasiv FTP**

> In FTP passive mode (PASV command), which party initiates the data connection, and why is this significant for NAT traversal? [În modul pasiv FTP (comanda PASV), care parte inițiază conexiunea de date și de ce este acest lucru semnificativ pentru traversarea NAT?]

- **a)  The client connects to the server's dynamic port — NAT-friendly because outbound connections pass [Clientul se conectează la portul dinamic al serverului — compatibil cu NAT deoarece conexiunile de ieșire trec]**
- **b)  The server opens a connection to the client on port 20 — "passive" refers to waiting for commands [Serverul deschide o conexiune către client pe portul 20 — «pasiv» se referă la așteptarea comenzilor]**
- **c)  Both sides open ports simultaneously using TCP simultaneous open [Ambele părți deschid porturi simultan folosind TCP simultaneous open]**
- **d)  The NAT firewall automatically creates a tunnel based on the PASV response [Firewall-ul NAT creează automat un tunel bazat pe răspunsul PASV]**

> 💡 **Feedback:** In passive mode, the client initiates the data connection to a server-specified port. This works through NAT because outbound connections from the client are typically allowed, whereas inbound connections (used in active mode) are blocked by NAT. A common misconception is that "passive" means the client does nothing — in reality, "passive" refers to the server's role (passively waiting), while the client actively connects. [În modul pasiv, clientul inițiază conexiunea de date către un port specificat de server. Acest lucru funcționează prin NAT deoarece conexiunile de ieșire de la client sunt de obicei permise, în timp ce conexiunile de intrare (folosite în modul activ) sunt blocate de NAT. O concepție greșită frecventă este că «pasiv» înseamnă că clientul nu face nimic — în realitate, «pasiv» se referă la rolul serverului (așteptare pasivă), în timp ce clientul se conectează activ.]

---

### Q12. `True / False`
**FTP Active Mode Is NAT-Friendly / Modul activ FTP este compatibil cu NAT**

> FTP active mode (PORT command) is NAT-friendly because the server initiates the data connection to the client. [Modul activ FTP (comanda PORT) este compatibil cu NAT deoarece serverul inițiază conexiunea de date către client.]

- **a)  true**
- **b)  false**

> 💡 **Feedback:** False. Active mode fails through NAT because the server attempts to connect inbound to the client's private IP, which NAT blocks. Passive mode is NAT-friendly because the client initiates the outbound data connection. A common misconception is that active and passive modes are interchangeable, but they differ fundamentally in who initiates the data connection, which determines NAT compatibility. [Fals. Modul activ eșuează prin NAT deoarece serverul încearcă să se conecteze la adresa IP privată a clientului, pe care NAT o blochează. Modul pasiv este compatibil cu NAT deoarece clientul inițiază conexiunea de date de ieșire. O concepție greșită frecventă este că modurile activ și pasiv sunt interschimbabile, dar ele diferă fundamental prin cine inițiază conexiunea de date, ceea ce determină compatibilitatea cu NAT.]

---

### Q13. `Multiple Choice`
**Why Active Mode FTP Fails Through NAT / De ce modul activ FTP eșuează prin NAT**

> A client behind a NAT firewall sends an FTP PORT command advertising its private IP address 192.168.1.100 and port 5000 . The server attempts to initiate the data connection. What happens? [Un client din spatele unui firewall NAT trimite o comandă FTP PORT publicând adresa sa IP privată 192.168.1.100 și portul 5000 . Serverul încearcă să inițieze conexiunea de date. Ce se întâmplă?]

- **a)  The connection fails — the server cannot reach the client's private IP through NAT [Conexiunea eșuează — serverul nu poate ajunge la IP-ul privat al clientului prin NAT]**
- **b)  The NAT automatically translates the private IP to the public IP and the connection succeeds [NAT traduce automat adresa IP privată în adresa IP publică și conexiunea reușește]**
- **c)  The server falls back to passive mode automatically when active mode fails [Serverul trece automat în modul pasiv când modul activ eșuează]**
- **d)  The data connection succeeds because port 20 is a well-known FTP data port that is automatically exempted from NAT filtering rules [Conexiunea de date reușește deoarece portul 20 este un port de date FTP bine-cunoscut exceptat automat de la regulile de filtrare NAT]**

> 💡 **Feedback:** In active mode, the server tries to connect inbound to the client's advertised address. Since 192.168.1.100 is a private IP behind NAT, the server cannot route to it from the Internet. NAT firewalls block unsolicited inbound connections, causing the data connection to fail. A common misconception is that NAT automatically translates the address or that port 20 is exempted from filtering. [În modul activ, serverul încearcă să se conecteze la adresa publicată de client. Deoarece 192.168.1.100 este o adresă IP privată din spatele NAT, serverul nu poate ruta către ea din Internet. Firewall-urile NAT blochează conexiunile de intrare nesolicitate, cauzând eșecul conexiunii de date. O concepție greșită frecventă este că NAT traduce automat adresa sau că portul 20 este exceptat de la filtrare.]

---

### Q14. `Multiple Choice`
**Session Layer vs Transport Layer Distinction / Distincția între stratul sesiune și stratul transport**

> Which statement best describes the fundamental difference between a TCP connection (Layer 4) and a session (Layer 5)? [Care afirmație descrie cel mai bine diferența fundamentală dintre o conexiune TCP (Nivelul 4) și o sesiune (Nivelul 5)?]

- **a)  TCP provides anonymous reliable delivery; a session adds authenticated user state spanning multiple connections [TCP oferă livrare fiabilă anonimă; o sesiune adaugă stare autentificată ce poate cuprinde mai multe conexiuni]**
- **b)  A session is just a synonym for a TCP connection that uses encryption [O sesiune este doar un sinonim pentru o conexiune TCP care folosește criptare]**
- **c)  TCP connections maintain user authentication while sessions handle only byte delivery between endpoints [Conexiunile TCP mențin autentificarea utilizatorului în timp ce sesiunile gestionează doar livrarea octeților între puncte]**
- **d)  Sessions operate at Layer 4 and provide reliability on top of TCP connections [Sesiunile operează la Nivelul 4 și oferă fiabilitate peste conexiunile TCP]**

> 💡 **Feedback:** A TCP connection is identified by a 4-tuple (source IP, source port, destination IP, destination port) and provides reliable byte delivery without any concept of user identity. A session adds application-level state — authentication, user preferences, working directory — that gives meaning to the connection from the user's perspective. Sessions may persist across multiple TCP connections (e.g., HTTP sessions with cookies) or be lost when a single TCP connection drops (e.g., FTP). The misconception that TCP connections and sessions are equivalent stems from conflating transport reliability with application state management. [O conexiune TCP este identificată printr-un 4-tuplu (IP sursă, port sursă, IP destinație, port destinație) și oferă livrarea fiabilă a octeților fără nicio noțiune de identitate a utilizatorului. O sesiune adaugă stare la nivel de aplicație — autentificare, preferințe ale utilizatorului, directorul de lucru — care dă sens conexiunii din perspectiva utilizatorului. Sesiunile pot persista pe parcursul mai multor conexiuni TCP (de ex. sesiuni HTTP cu cookie-uri) sau pot fi pierdute când o singură conexiune TCP cade (de ex. FTP). Concepția greșită că conexiunile TCP și sesiunile sunt echivalente provine din confuzia dintre fiabilitatea transportului și gestionarea stării aplicației.]

---

### Q15. `Multiple Choice`
**FTP Architecture — Control vs Data Channel / Arhitectura FTP — canal de control versus canal de date**

> A student captures FTP traffic in Wireshark and observes that the RETR document.pdf command appears on one TCP stream while the actual file bytes appear on a different TCP stream. What is the most accurate explanation for this observation? [Un student captează traficul FTP în Wireshark și observă că comanda RETR document.pdf apare pe un flux TCP în timp ce octeții fișierului propriu-zis apar pe un flux TCP diferit. Care este explicația cea mai corectă pentru această observație?]

- **a)  FTP uses separate control and data connections by design — commands on port 21, file data on a different port [FTP folosește conexiuni separate de control și date — comenzi pe portul 21, date pe alt port]**
- **b)  The capture shows a Wireshark display error — FTP always uses a single TCP connection [Captura arată o eroare de afișare Wireshark — FTP folosește întotdeauna o singură conexiune TCP]**
- **c)  The file was too large for one TCP segment so Wireshark automatically split it into a separate reassembled stream [Fișierul era prea mare pentru un singur segment TCP așa că Wireshark l-a împărțit automat într-un flux reasamblat separat]**
- **d)  The server opened a second connection due to packet loss on the original connection [Serverul a deschis o a doua conexiune din cauza pierderii de pachete pe conexiunea originală]**

> 💡 **Feedback:** FTP's defining architectural feature is its dual-channel design: a persistent control connection (port 21) carries text commands and response codes, while a separate temporary data connection (port 20 in active mode or a dynamic port in passive mode) carries file contents and directory listings. The RETR command is sent on the control channel, which instructs the server to send file data on the data channel. This separation enables features like out-of-band transfer control and simultaneous command processing during transfers. The misconception that this represents an error or packet loss is common among students who expect single-connection protocols like HTTP. [Caracteristica arhitecturală definitorie a FTP este designul cu dublu canal: o conexiune de control persistentă (portul 21) transportă comenzi text și coduri de răspuns, în timp ce o conexiune de date temporară separată (portul 20 în modul activ sau un port dinamic în modul pasiv) transportă conținutul fișierelor și listele de directoare.]

---

### Q16. `Multiple Choice`
**PASV Response Port Decoding / Decodificarea portului din răspunsul PASV**

> An FTP server sends: 227 Entering Passive Mode (172,16,0,10,156,64) . What is the correct data connection target? [Un server FTP trimite: 227 Entering Passive Mode (172,16,0,10,156,64) . Care este ținta corectă a conexiunii de date?]

- **a)  172.16.0.10 port 40000 (156 × 256 + 64) [172.16.0.10 portul 40000 (156 × 256 + 64)]**
- **b)  172.16.0.10 port 15664 (concatenation of 156 and 64) [172.16.0.10 portul 15664 (concatenarea lui 156 și 64)]**
- **c)  172.16.0.10 port 64 (only the second port number) [172.16.0.10 portul 64 (doar al doilea număr de port)]**
- **d)  172.16.0.10 port 156 (only the first port number) [172.16.0.10 portul 156 (doar primul număr de port)]**

> 💡 **Feedback:** The PASV response format is (h1,h2,h3,h4,p1,p2) . The IP is 172.16.0.10 and the port is p1 × 256 + p2 = 156 × 256 + 64 = 39936 + 64 = 40000 . A common mistake is treating the two port values as a concatenated string (15664) or using only p2 as the port. Understanding this encoding is essential for implementing FTP clients and debugging passive mode connections. [Formatul răspunsului PASV este (h1,h2,h3,h4,p1,p2) . IP-ul este 172.16.0.10 iar portul este p1 × 256 + p2 = 156 × 256 + 64 = 39936 + 64 = 40000 . O greșeală frecventă este tratarea celor două valori de port ca un șir concatenat (15664) sau utilizarea doar a lui p2 ca port.]

---

### Q17. `Multiple Choice`
**Serialisation Format Selection / Selectarea formatului de serializare**

> In the context of Presentation Layer data formats, which statement most accurately compares JSON and Protocol Buffers as serialisation formats? [În contextul formatelor de date ale Stratului prezentare, care afirmație compară cel mai exact JSON și Protocol Buffers ca formate de serializare?]

- **a)  JSON is text-based and human-readable; Protocol Buffers is binary and compact — the trade-off is debuggability vs performance [JSON este bazat pe text; Protocol Buffers este binar și compact — compromisul este depanabilitate vs performanță]**
- **b)  Both are binary formats but JSON uses fixed schemas while Protocol Buffers is schema-free [Ambele sunt formate binare dar JSON folosește scheme fixe în timp ce Protocol Buffers nu are schemă]**
- **c)  JSON provides built-in encryption while Protocol Buffers requires external encryption [JSON oferă criptare încorporată în timp ce Protocol Buffers necesită criptare externă]**
- **d)  Protocol Buffers is only for persistent file storage while JSON is the standard for network data transmission [Protocol Buffers este doar pentru stocarea persistentă în timp ce JSON este standardul pentru transmisia datelor în rețea]**

> 💡 **Feedback:** JSON is a text-based serialisation format that is human-readable but verbose, making it ideal for web APIs where debuggability matters. Protocol Buffers is a binary serialisation format that is compact and fast but not human-readable, making it suitable for high-performance inter-service communication. Both are Presentation Layer concerns — they define how data structures are represented in bytes for transmission. The choice depends on the trade-off between debuggability and performance. [JSON este un format de serializare bazat pe text, care este ușor de citit de oameni dar verbos, făcându-l ideal pentru API-uri web unde depanabilitatea contează. Protocol Buffers este un format de serializare binar, compact și rapid dar imposibil de citit de oameni, făcându-l potrivit pentru comunicarea de înaltă performanță între servicii.]

---

### Q18. `Multiple Choice`
**FTP Session Lifecycle — When Does Session Begin / Ciclul de viață al sesiunii FTP — când începe sesiunea**

> In a Wireshark capture of an FTP connection, you observe: (1) TCP three-way handshake, (2) server sends 220 FTP Server Ready , (3) client sends USER test , (4) server responds 331 Password required , (5) client sends PASS 12345 , (6) server responds 230 Login successful . At which point does the session layer become active? [Într-o captură Wireshark a unei conexiuni FTP, observați: (1) handshake TCP în trei pași, (2) serverul trimite 220 FTP Server Ready , (3) clientul trimite USER test , (4) serverul răspunde 331 Password required , (5) clientul trimite PASS 12345 , (6) serverul răspunde 230 Login successful . În ce moment devine activ stratul sesiune?]

- **a)  Step 3 — when USER test initiates the authentication dialogue [Pasul 3 — când USER test inițiază dialogul de autentificare]**
- **b)  Step 1 — when the TCP three-way handshake completes [Pasul 1 — când se completează handshake-ul TCP în trei pași]**
- **c)  Step 2 — when the server sends the 220 banner [Pasul 2 — când serverul trimite bannerul 220]**
- **d)  Step 6 — only after full authentication is confirmed with 230 [Pasul 6 — doar după ce autentificarea completă este confirmată cu 230]**

> 💡 **Feedback:** The Session Layer becomes active when the authentication dialogue begins — at step (3) when the client sends USER test . The TCP handshake (step 1) is Transport Layer (L4). The server banner (step 2) is application-level greeting but does not yet involve session state. The USER command initiates the authentication process, which is a defining Session Layer function: verifying identity and establishing a logical dialogue context. By step (6) the session is fully established with authenticated state. [Stratul sesiune devine activ când dialogul de autentificare începe — la pasul (3) când clientul trimite USER test . Handshake-ul TCP (pasul 1) este la Stratul de transport (L4). Bannerul serverului (pasul 2) este un salut la nivel de aplicație dar nu implică încă starea sesiunii. Comanda USER inițiază procesul de autentificare, care este o funcție definitorie a Stratului sesiune.]

---

### Q19. `Multiple Choice`
**TCP Does Not Preserve Message Boundaries / TCP nu păstrează delimitarea mesajelor**

> A sender calls send() with a 12-byte header followed by a 100-byte payload in two separate calls. How might the receiver's recv() calls return this data? [Un expeditor apelează send() cu un antet de 12 octeți urmat de o sarcină utilă (payload) de 100 de octeți în două apeluri separate. Cum ar putea apelurile recv() ale receptorului să returneze aceste date?]

- **a)  Any combination of recv() chunks — e.g. recv(8) + recv(4) + recv(100), or all recv(112) at once [Orice combinație de fragmente recv() — de ex. recv(8) + recv(4) + recv(100), sau tot recv(112) odată]**
- **b)  Exactly recv(12) then recv(100), matching the send() calls [Exact recv(12) apoi recv(100), corespunzând apelurilor send()]**
- **c)  Always exactly recv(112) as a single call because TCP combines adjacent socket writes into one [Întotdeauna exact recv(112) într-un singur apel deoarece TCP combină scrierile adiacente pe socket]**
- **d)  Exactly recv(1) repeated 112 times, one byte at a time [Exact recv(1) repetat de 112 ori, câte un octet pe rând]**

> 💡 **Feedback:** TCP is a byte stream protocol with no message boundaries. Data from multiple send() calls may arrive in any combination of chunks, requiring explicit framing (e.g., length-prefixed messages). A common misconception is that each send() maps to exactly one recv() , but TCP guarantees only ordered byte delivery, not message boundary preservation. [TCP este un protocol de tip flux de octeți fără delimitarea mesajelor. Datele din mai multe apeluri send() pot ajunge în orice combinație de fragmente, necesitând delimitare (framing) explicită (de ex. mesaje cu prefix de lungime). O concepție greșită frecventă este că fiecare send() corespunde exact unui recv() , dar TCP garantează doar livrarea ordonată a octeților, nu păstrarea delimitării mesajelor.]

---

### Q20. `Multiple Choice`
**TCP Byte Stream and Message Framing / Fluxul de octeți TCP și încadrarea mesajelor**

> A developer sends a 12-byte header followed by a 100-byte payload using two separate send() calls. The receiver calls recv(12) expecting to get exactly the header. Under what conditions might this fail? [Un dezvoltator trimite un antet de 12 octeți urmat de o sarcină utilă de 100 de octeți folosind două apeluri send() separate. Receptorul apelează recv(12) așteptând să primească exact antetul. În ce condiții ar putea eșua aceasta?]

- **a)  TCP may deliver fewer than 12 bytes in a single recv() — it is a byte stream with no message boundaries [TCP poate livra mai puțin de 12 octeți într-un recv() — este un flux de octeți fără delimitări de mesaje]**
- **b)  This can never fail because TCP guarantees delivery of complete application-level messages in order [Aceasta nu poate eșua niciodată deoarece TCP garantează livrarea mesajelor complete la nivel de aplicație în ordine]**
- **c)  It fails only when the network MTU is smaller than 12 bytes [Eșuează doar când MTU-ul rețelei este mai mic de 12 octeți]**
- **d)  It fails only if the header and payload are sent in different TCP segments [Eșuează doar dacă antetul și sarcina utilă sunt trimise în segmente TCP diferite]**

> 💡 **Feedback:** TCP is a byte stream protocol that does not preserve message boundaries. A single recv(12) may return fewer than 12 bytes (e.g., 8 bytes) if the data arrives in multiple TCP segments or if the kernel buffer contains only a partial message at the time of the call. The correct approach is to use a recv_exactly() function that loops until the full requested amount is received. This is one of the most common bugs in network programming. [TCP este un protocol de flux de octeți care nu păstrează delimitările mesajelor. Un singur apel recv(12) poate returna mai puțin de 12 octeți (de ex. 8 octeți) dacă datele sosesc în mai multe segmente TCP sau dacă bufferul nucleului conține doar un mesaj parțial în momentul apelului. Abordarea corectă este utilizarea unei funcții recv_exactly() care ciclează până când se primește întreaga cantitate solicitată.]

---

### Q21. `Multiple Choice`
**Why Binary Protocols Require a Length Field / De ce protocoalele binare necesită un câmp de lungime**

> A binary protocol is designed without a length field in its header. The developer assumes each recv() call will return exactly one complete message. What fundamental problem does this create? [Un protocol binar este proiectat fără câmp de lungime în antet. Dezvoltatorul presupune că fiecare apel recv() va returna exact un mesaj complet. Ce problemă fundamentală creează aceasta?]

- **a)  The receiver cannot determine message boundaries — TCP delivers partial or concatenated data in recv() [Receptorul nu poate determina delimitarea mesajelor — TCP livrează date parțiale sau concatenate în recv()]**
- **b)  The protocol cannot support variable payloads larger than the TCP maximum segment size (MSS) without fragmentation [Protocolul nu poate suporta sarcini utile variabile mai mari decât MSS-ul TCP fără fragmentare]**
- **c)  The CRC-32 checksum cannot be verified without knowing the message length in advance [Suma de control CRC-32 nu poate fi verificată fără a cunoaște lungimea mesajului în avans]**
- **d)  The operating system will reject messages that do not declare their size in the header [Sistemul de operare va respinge mesajele care nu își declară dimensiunea în antet]**

> 💡 **Feedback:** TCP is a byte stream with no message boundaries. Without a length field, the receiver cannot determine where one message ends and the next begins. A single recv() may return a partial message, multiple messages concatenated, or any combination. The length field enables explicit framing. A common misconception is that the operating system guarantees one-to-one mapping between send() and recv() calls. [TCP este un flux de octeți fără delimitarea mesajelor. Fără un câmp de lungime, receptorul nu poate determina unde se termină un mesaj și unde începe următorul. Un singur recv() poate returna un mesaj parțial, mai multe mesaje concatenate sau orice combinație. Câmpul de lungime permite delimitarea (framing-ul) explicită. O concepție greșită frecventă este că sistemul de operare garantează o corespondență unu-la-unu între apelurile send() și recv() .]

---

### Q22. `Multiple Choice`
**Network Byte Order Identification / Identificarea ordinii de octeți a rețelei**

> A developer uses struct.pack("<I", 0xAABBCCDD) to send a 32-bit integer over the network. A colleague on a different machine receives the bytes and unpacks them with struct.unpack("!I", data) . What is the most likely outcome? [Un dezvoltator folosește struct.pack("<I", 0xAABBCCDD) pentru a trimite un întreg de 32 de biți prin rețea. Un coleg pe un alt calculator primește octeții și îi despachetează cu struct.unpack("!I", data) . Care este rezultatul cel mai probabil?]

- **a)  The receiver gets the wrong value (0xDDCCBBAA) because the byte order is mismatched [Receptorul primește valoarea greșită (0xDDCCBBAA) deoarece ordinea octeților este nepotrivită]**
- **b)  The receiver correctly gets 0xAABBCCDD because TCP handles byte order conversion [Receptorul primește corect 0xAABBCCDD deoarece TCP gestionează conversia ordinii octeților]**
- **c)  A runtime error occurs because little-endian data cannot be transmitted over networks [Apare o eroare de execuție deoarece datele little-endian nu pot fi transmise prin rețea]**
- **d)  The CRC checksum detects the mismatch and triggers retransmission [Suma de control CRC detectează nepotrivirea și declanșează retransmisia]**

> 💡 **Feedback:** The sender packs with little-endian ( < ), producing bytes DD CC BB AA . The receiver unpacks with network byte order ( ! = big-endian), interpreting those bytes as 0xDDCCBBAA — the wrong value. Both sides must use the same byte order, preferably network byte order ( ! or > ). This byte-order mismatch is a classic bug that produces "silent data corruption" — the code runs without errors but produces incorrect values. The misconception that CRC or checksums would catch this is wrong because both sides independently compute checksums on their own (mismatched) interpretation of the data. [Expeditorul împachetează cu little-endian ( < ), producând octeții DD CC BB AA . Receptorul despachetează cu ordinea de rețea ( ! = big-endian), interpretând acei octeți ca 0xDDCCBBAA — valoarea greșită. Ambele părți trebuie să folosească aceeași ordine a octeților, preferabil ordinea de rețea ( ! sau > ). Această nepotrivire a ordinii octeților este o eroare clasică ce produce „corupere silențioasă a datelor" — codul rulează fără erori dar produce valori incorecte.]

---

### Q23. `Multiple Choice`
**Purpose of Magic Bytes in Binary Protocols / Scopul octeților magici în protocoalele binare**

> Why do binary network protocols typically include a fixed "magic number" at the beginning of each message? [De ce includ protocoalele binare de rețea de obicei un «număr magic» fix la începutul fiecărui mesaj?]

- **a)  To identify the protocol type and enable resynchronisation [Pentru a identifica tipul de protocol și a permite resincronizarea]**
- **b)  To encrypt the message header for confidentiality [Pentru a cripta antetul mesajului în scopul confidențialității]**
- **c)  To compress the payload data more efficiently [Pentru a comprima mai eficient datele utile din sarcina utilă]**
- **d)  To serve as a seed value for CRC-32 checksum calculation, improving error detection [Pentru a servi ca valoare inițială pentru calculul sumei de control CRC-32, îmbunătățind detectarea erorilor]**

> 💡 **Feedback:** Magic bytes serve to identify the protocol type (rejecting misrouted data) and to enable resynchronisation after stream corruption by scanning for the known byte sequence. A common misconception is that magic bytes provide encryption or compression; they serve purely as protocol identifiers and synchronisation markers. [Octeții magici servesc la identificarea tipului de protocol (respingând datele dirijate greșit) și la resincronizare după coruperea fluxului prin căutarea secvenței de octeți cunoscute. O concepție greșită frecventă este că octeții magici oferă criptare sau compresie; ei servesc exclusiv ca identificatori de protocol și marcatori de sincronizare.]

---

### Q24. `Multiple Choice`
**Binary Protocol Header Design Checklist / Lista de verificare pentru proiectarea antetului unui protocol binar**

> Which of the following is not typically part of a well-designed binary protocol header? [Care dintre următoarele nu face parte de obicei dintr-un antet bine proiectat al unui protocol binar?]

- **a)  Username string (application-level concern) [Șir cu numele utilizatorului (preocupare la nivel de aplicație)]**
- **b)  Magic bytes for protocol identification [Octeți magici pentru identificarea protocolului]**
- **c)  Length field for message framing [Câmp de lungime pentru delimitarea mesajelor]**
- **d)  CRC-32 checksum for integrity verification [Sumă de control (checksum) CRC-32 pentru verificarea integrității]**

> 💡 **Feedback:** Binary protocol headers typically include magic bytes, version, length, checksum, and flags. A username field belongs to the application/session layer payload, not the framing header. A common misconception is to conflate framing concerns (how to parse messages) with session concerns (who is communicating). [Antetele protocoalelor binare includ de obicei octeți magici, versiune, lungime, sumă de control și fanioane. Un câmp pentru numele utilizatorului aparține sarcinii utile (payload) a stratului aplicație/sesiune, nu antetului de delimitare. O concepție greșită frecventă este confuzia între preocupările de delimitare (cum se parsează mesajele) și preocupările de sesiune (cine comunică).]

---

### Q25. `True / False`
**Version Field Enables Protocol Evolution / Câmpul de versiune permite evoluția protocolului**

> Including a version field in a binary protocol header allows the receiver to determine which message format to expect, enabling backward-compatible protocol evolution. [Includerea unui câmp de versiune în antetul unui protocol binar permite receptorului să determine ce format de mesaj să aștepte, facilitând evoluția protocolului cu compatibilitate inversă.]

- **a)  true**
- **b)  false**

> 💡 **Feedback:** True. A version field is part of the binary protocol design checklist. It allows the receiver to select the correct parsing logic for different protocol versions, enabling gradual upgrades without breaking existing implementations. A common misconception is that protocols are static once deployed, but real-world protocols evolve and the version field is essential for managing this evolution. [Adevărat. Câmpul de versiune face parte din lista de verificare pentru proiectarea protocoalelor binare. Permite receptorului să selecteze logica corectă de parsare pentru diferite versiuni ale protocolului, facilitând actualizări graduale fără a afecta implementările existente. O concepție greșită frecventă este că protocoalele sunt statice odată implementate, dar protocoalele reale evoluează, iar câmpul de versiune este esențial pentru gestionarea acestei evoluții.]

---

### Q26. `True / False`
**CRC-32 Detects Single-Bit Errors / CRC-32 detectează erorile de un singur bit**

> CRC-32 is specifically designed to detect single-bit errors in transmitted data. [CRC-32 este proiectat special pentru a detecta erorile de un singur bit în datele transmise.]

- **a)  true**
- **b)  false**

> 💡 **Feedback:** True. CRC-32 reliably detects all single-bit errors, all double-bit errors, and all burst errors shorter than 32 bits. It is purpose-built for accidental error detection at the Presentation Layer. A common misconception is that CRC-32 also provides security against intentional tampering, but it only addresses random transmission errors. [Adevărat. CRC-32 detectează fiabil toate erorile de un singur bit, toate erorile de doi biți și toate erorile de tip rafală mai scurte de 32 de biți. Este construit special pentru detecția erorilor accidentale la Stratul prezentare. O concepție greșită frecventă este că CRC-32 oferă și securitate împotriva falsificării intenționate, dar abordează doar erorile aleatoare de transmisie.]

---

### Q27. `Multiple Choice`
**HMAC vs CRC-32 vs SHA-256 for Tamper Detection / HMAC vs. CRC-32 vs. SHA-256 pentru detectarea falsificării**

> Which mechanism provides actual tamper detection against an attacker who can modify both the data and the integrity value? [Care mecanism oferă detectare reală a falsificării împotriva unui atacator care poate modifica atât datele, cât și valoarea de integritate?]

- **a)  HMAC (e.g. HMAC-SHA256) — requires a shared secret key unknown to the attacker [HMAC (de ex. HMAC-SHA256) — necesită o cheie secretă necunoscută atacatorului]**
- **b)  CRC-32 — uses a polynomial that prevents forgery [CRC-32 — folosește un polinom care previne falsificarea]**
- **c)  SHA-256 — produces a 256-bit digest that cannot be recalculated [SHA-256 — produce un rezumat de 256 biți care nu poate fi recalculat]**
- **d)  MD5 — provides collision-resistance sufficient for tamper detection of data [MD5 — oferă rezistență la coliziuni suficientă pentru detectarea falsificării datelor]**

> 💡 **Feedback:** Only HMAC (keyed hash) provides tamper detection because the attacker would need the secret key to forge a valid MAC. Both CRC-32 and SHA-256 can be recalculated by anyone with access to the modified data. A common misconception is that SHA-256 prevents tampering — it provides collision resistance but without a secret key, an attacker can simply recompute the hash for modified data. [Doar HMAC (hash cu cheie) oferă detectarea falsificării deoarece atacatorul ar avea nevoie de cheia secretă pentru a falsifica un MAC valid. Atât CRC-32, cât și SHA-256 pot fi recalculate de oricine are acces la datele modificate. O concepție greșită frecventă este că SHA-256 previne falsificarea — oferă rezistență la coliziuni, dar fără o cheie secretă, un atacator poate pur și simplu recalcula hash-ul pentru datele modificate.]

---

### Q28. `Multiple Choice`
**CRC-32 Security Limitations / Limitările de securitate ale CRC-32**

> A student implements a file transfer protocol that includes CRC-32 verification and claims the protocol is "secure against tampering". What is the primary flaw in this reasoning? [Un student implementează un protocol de transfer de fișiere care include verificarea CRC-32 și susține că protocolul este „securizat împotriva falsificării". Care este deficiența principală în acest raționament?]

- **a)  CRC-32 has no secret key — an attacker can modify data and recalculate a valid CRC [CRC-32 nu are cheie secretă — un atacator poate modifica datele și recalcula un CRC valid]**
- **b)  CRC-32 only works on files smaller than 4 GB due to the 32-bit output size [CRC-32 funcționează doar pe fișiere mai mici de 4 GB din cauza dimensiunii de ieșire de 32 de biți]**
- **c)  CRC-32 is too slow for real-time verification during file transfer [CRC-32 este prea lent pentru verificarea în timp real în timpul transferului de fișiere]**
- **d)  The protocol is actually secure — CRC-32's polynomial prevents any modification [Protocolul este de fapt securizat — polinomul CRC-32 previne orice modificare]**

> 💡 **Feedback:** CRC-32 is a non-cryptographic error detection code designed to catch accidental transmission errors (bit flips, noise). Since CRC-32 is a public algorithm with no secret key component, an attacker who can modify the data can trivially recalculate the correct CRC-32 for the modified content and replace both. For actual tamper detection, a cryptographic mechanism is needed: either a cryptographic hash (SHA-256) combined with a secure channel, or a message authentication code (HMAC) using a shared secret key. The misconception confuses error detection (accidental) with integrity protection (intentional). [CRC-32 este un cod de detectare a erorilor non-criptografic proiectat să descopere erorile accidentale de transmisie (inversarea biților, zgomot). Deoarece CRC-32 este un algoritm public fără componentă de cheie secretă, un atacator care poate modifica datele poate recalcula trivial CRC-32-ul corect pentru conținutul modificat și poate înlocui ambele.]

---


## §2.  Laborator / Lab   (12 questions)

### Q29. `Multiple Choice`
**FTP Response Code 230 / Codul de răspuns FTP 230**

> In the FTP protocol, what does response code 230 indicate? [În protocolul FTP, ce indică codul de răspuns 230 ?]

- **a)  User logged in successfully [Utilizator autentificat cu succes]**
- **b)  Username accepted, password required [Nume de utilizator acceptat, parolă necesară]**
- **c)  Transfer complete [Transfer complet]**
- **d)  Service ready for new user [Serviciu pregătit pentru utilizator nou]**

> 💡 **Feedback:** FTP code 230 means "User logged in" — the authentication was successful and the session is established. A common misconception is to confuse 230 with 220 (service ready) or 226 (transfer complete). The 2xx series indicates positive completion, and 230 specifically confirms successful authentication. [Codul FTP 230 înseamnă «Utilizator autentificat» — autentificarea a reușit și sesiunea este stabilită. O concepție greșită frecventă este confuzia între 230 și 220 (serviciu pregătit) sau 226 (transfer complet). Seria 2xx indică finalizare cu succes, iar 230 confirmă specific autentificarea reușită.]

---

### Q30. `Multiple Choice`
**FTP Transfer Mode for Binary Files / Modul de transfer FTP pentru fișiere binare**

> Which FTP command sets the transfer mode appropriate for executables, images, and archives? [Care comandă FTP setează modul de transfer potrivit pentru executabile, imagini și arhive?]

- **a)  TYPE I (Binary mode) [TYPE I (mod binar)]**
- **b)  TYPE A (ASCII mode) [TYPE A (mod ASCII)]**
- **c)  MODE B (Block mode) [MODE B (mod Block)]**
- **d)  RETR (Retrieve file mode) [RETR (mod preluare fișier)]**

> 💡 **Feedback:** TYPE I sets binary (Image) transfer mode, which transfers files byte-for-byte without conversion. TYPE A (ASCII) performs line-ending conversion and is only suitable for text files. A common misconception is that MODE B (Block mode) is the binary equivalent, but TYPE I is the correct command — "I" stands for Image, not Integer. [TYPE I setează modul de transfer binar (Image), care transferă fișierele octet cu octet fără conversie. TYPE A (ASCII) efectuează conversia terminatorilor de linie și este potrivit doar pentru fișiere text. O concepție greșită frecventă este că MODE B (modul Block) este echivalentul binar, dar TYPE I este comanda corectă — «I» vine de la Image (Imagine), nu Integer.]

---

### Q31. `True / False`
**Closing FTP Control Channel Immediately Stops Data Transfer / Închiderea canalului de control FTP oprește imediat transferul de date**

> If the FTP control connection is closed during an active file download, the data transfer stops immediately. [Dacă conexiunea de control FTP este închisă în timpul unei descărcări active de fișier, transferul de date se oprește imediat.]

- **a)  true**
- **b)  false**

> 💡 **Feedback:** False. The data channel is a separate TCP connection with its own state. Closing the control channel does not immediately terminate an in-progress data transfer, though you lose the ability to receive the 226 completion confirmation or issue an ABOR command. A common misconception is that closing the control channel kills all associated connections, but TCP connections are independent at the transport level. [Fals. Canalul de date este o conexiune TCP separată cu propria stare. Închiderea canalului de control nu termină imediat un transfer de date în curs, deși pierdeți capacitatea de a primi confirmarea de finalizare 226 sau de a emite o comandă ABOR. O concepție greșită frecventă este că închiderea canalului de control oprește toate conexiunile asociate, dar conexiunile TCP sunt independente la nivelul de transport.]

---

### Q32. `Multiple Choice`
**Encoding a Port Number for PASV Response / Codificarea unui număr de port pentru răspunsul PASV**

> An FTP server wants to advertise port 50008 in its PASV response. What are the correct values for p1 and p2 in the response 227 Entering Passive Mode (h1,h2,h3,h4,p1,p2) ? [Un server FTP dorește să publice portul 50008 în răspunsul PASV. Care sunt valorile corecte pentru p1 și p2 în răspunsul 227 Entering Passive Mode (h1,h2,h3,h4,p1,p2) ?]

- **a)  p1 = 195, p2 = 88**
- **b)  p1 = 88, p2 = 195**
- **c)  p1 = 50, p2 = 8**
- **d)  p1 = 196, p2 = 72**

> 💡 **Feedback:** To encode port 50008: p1 = 50008 ÷ 256 = 195 (integer division), p2 = 50008 mod 256 = 88. Verification: 195 × 256 + 88 = 49920 + 88 = 50008. A common misconception is to simply split the decimal digits (p1=50, p2=8), but the encoding uses base-256, not base-10. [Pentru a codifica portul 50008: p1 = 50008 ÷ 256 = 195 (împărțire întreagă), p2 = 50008 mod 256 = 88. Verificare: 195 × 256 + 88 = 49920 + 88 = 50008. O concepție greșită frecventă este împărțirea simplă a cifrelor zecimale (p1=50, p2=8), dar codificarea folosește baza 256, nu baza 10.]

---

### Q33. `Multiple Choice`
**When Session Layer Becomes Active in a Wireshark Capture / Când devine activ Stratul sesiune într-o captură Wireshark**

> In a Wireshark capture of an FTP connection, you observe: Packet 1–3: TCP three-way handshake; Packet 4: "220 FTP Server Ready"; Packet 5: "USER test". At which packet does Session Layer activity begin? [Într-o captură Wireshark a unei conexiuni FTP, observați: Pachetele 1–3: handshake TCP în trei pași; Pachetul 4: «220 FTP Server Ready»; Pachetul 5: «USER test». La care pachet începe activitatea Stratului sesiune?]

- **a)  Packet 5 — when the USER command initiates authentication [Pachetul 5 — când comanda USER inițiază autentificarea]**
- **b)  Packet 1 — when the TCP SYN initiates the connection [Pachetul 1 — când TCP SYN inițiază conexiunea]**
- **c)  Packet 3 — when the TCP three-way handshake completes [Pachetul 3 — când se completează handshake-ul TCP în trei pași]**
- **d)  Packet 4 — when the FTP server sends its welcome banner [Pachetul 4 — când serverul FTP trimite banner-ul de întâmpinare]**

> 💡 **Feedback:** The TCP handshake (packets 1–3) is Transport Layer. The server banner (packet 4) is still transport-level data delivery. Session Layer activity begins with the USER command (packet 5), which initiates the authentication dialogue. A common misconception is that the TCP handshake constitutes session establishment, but TCP only establishes a transport connection — the session begins when application-level authentication starts. [Handshake-ul TCP (pachetele 1–3) este la Stratul de transport. Banner-ul serverului (pachetul 4) este încă livrare de date la nivel de transport. Activitatea Stratului sesiune începe cu comanda USER (pachetul 5), care inițiază dialogul de autentificare. O concepție greșită frecventă este că handshake-ul TCP constituie stabilirea sesiunii, dar TCP stabilește doar o conexiune de transport — sesiunea începe când pornește autentificarea la nivel de aplicație.]

---

### Q34. `Multiple Choice`
**Identifying FTP Control vs Data Channel in Wireshark / Identificarea canalului de control vs. canalul de date FTP în Wireshark**

> How can you distinguish an FTP control channel from a data channel in a Wireshark capture? [Cum puteți distinge canalul de control FTP de canalul de date într-o captură Wireshark?]

- **a)  Control channel carries ASCII FTP commands on a fixed port; data channel carries file content on dynamic ports [Canalul de control transportă comenzi FTP ASCII pe un port fix; canalul de date transportă conținut pe porturi dinamice]**
- **b)  Control channel uses UDP; data channel uses TCP [Canalul de control folosește UDP; canalul de date folosește TCP]**
- **c)  Both channels are identical and cannot be distinguished [Ambele canale sunt identice și nu pot fi distinse]**
- **d)  Control channel uses encrypted TLS for FTP commands while the data channel transmits file content as plaintext [Canalul de control folosește TLS criptat pentru comenzile FTP iar canalul de date transmite conținutul fișierelor ca text clar]**

> 💡 **Feedback:** The control channel carries ASCII text commands (USER, PASS, LIST, RETR) on port 21/2121, while data channels carry binary or text file contents on dynamic ports (e.g. 60000–60010). A common misconception is that the control channel uses UDP while the data channel uses TCP, but both channels use TCP. [Canalul de control transportă comenzi text ASCII (USER, PASS, LIST, RETR) pe portul 21/2121, în timp ce canalele de date transportă conținut de fișiere binar sau text pe porturi dinamice (de ex. 60000–60010). O concepție greșită frecventă este că canalul de control folosește UDP în timp ce canalul de date folosește TCP, dar ambele canale folosesc TCP.]

---

### Q35. `Multiple Choice`
**Identifying a Passive Data Transfer in Wireshark / Identificarea unui transfer de date pasiv în Wireshark**

> In a Wireshark capture, you see: (1) a "227 Entering Passive Mode (172,29,9,10,234,120)" response on port 2121, followed by (2) a new TCP SYN to port 60024 on the same server IP. What does the second TCP connection represent? [Într-o captură Wireshark, observați: (1) un răspuns «227 Entering Passive Mode (172,29,9,10,234,120)» pe portul 2121, urmat de (2) un nou TCP SYN către portul 60024 pe aceeași adresă IP a serverului. Ce reprezintă a doua conexiune TCP?]

- **a)  The FTP passive-mode data connection — the client connects to the PASV-advertised port (234×256+120 = 60024) [Conexiunea de date FTP în modul pasiv — clientul se conectează la portul publicat prin PASV (234×256+120 = 60024)]**
- **b)  A second control connection for parallel FTP command processing [O a doua conexiune de control pentru procesarea paralelă a comenzilor FTP]**
- **c)  A TLS handshake upgrading the FTP connection to FTPS [Un handshake TLS care actualizează conexiunea FTP la FTPS]**
- **d)  An unrelated TCP connection — the destination port numbers do not correspond to the PASV response calculation [O conexiune TCP fără legătură — numerele porturilor de destinație nu corespund calculului din răspunsul PASV]**

> 💡 **Feedback:** The PASV response tells the client to connect to port 234 × 256 + 120 = 60024. The new TCP SYN to that port is the client initiating the passive-mode data connection. A common misconception is that this is a TLS handshake or a second control connection, but it is the FTP data channel established via the PASV mechanism. [Răspunsul PASV indică clientului să se conecteze la portul 234 × 256 + 120 = 60024. Noul TCP SYN către acel port este clientul care inițiază conexiunea de date în modul pasiv. O concepție greșită frecventă este că aceasta ar fi un handshake TLS sau o a doua conexiune de control, dar este canalul de date FTP stabilit prin mecanismul PASV.]

---

### Q36. `Multiple Choice`
**Correct recv_exactly Implementation / Implementarea corectă a funcției recv_exactly**

> Which implementation correctly receives exactly n bytes from a TCP socket, handling partial reads? [Care implementare primește corect exact n octeți de la un socket TCP, gestionând citirile parțiale?]

- **a)  Loop calling sock.recv(n - len(data)) until n bytes are accumulated, raising on empty recv [Iterare apelând sock.recv(n - len(data)) până la n octeți acumulați, eroare la recv gol]**
- **b)  A single call to sock.recv(n) which always returns exactly n bytes [Un singur apel la sock.recv(n) care returnează întotdeauna exact n octeți]**
- **c)  Calling sock.recv(1) in a loop n times and concatenating one-byte results into the buffer [Apelarea sock.recv(1) într-o buclă de n ori și concatenarea rezultatelor de un octet în buffer]**
- **d)  Calling sock.recv(n * 2) and truncating to n bytes [Apelarea sock.recv(n * 2) și trunchierea la n octeți]**

> 💡 **Feedback:** Because TCP may return fewer bytes than requested, a correct implementation must loop, accumulating data until exactly n bytes have been received, and detect connection closure when recv returns empty bytes. A common misconception is that a single sock.recv(n) always returns exactly n bytes — TCP may deliver any amount up to n bytes per call. [Deoarece TCP poate returna mai puțini octeți decât cei solicitați, o implementare corectă trebuie să itereze, acumulând date până când exact n octeți au fost primiți, și să detecteze închiderea conexiunii când recv returnează octeți goi. O concepție greșită frecventă este că un singur sock.recv(n) returnează întotdeauna exact n octeți — TCP poate livra orice cantitate până la n octeți per apel.]

---

### Q37. `Multiple Choice`
**Output of struct.pack("&lt;H", 0x1234) / Rezultatul struct.pack("&lt;H", 0x1234)**

> What byte sequence does the following Python code produce? [Ce secvență de octeți produce următorul cod Python?]import struct
data = struct.pack("

- **a)  34 12**
- **b)  12 34**
- **c)  00 12 34**
- **d)  34 12 00 00**

> 💡 **Feedback:** The format "

---

### Q38. `Multiple Choice`
**Result of Unpacking Big-Endian Data as Little-Endian / Rezultatul despachetării datelor big-endian ca little-endian**

> The value 0xCAFEBABE is packed using big-endian format, producing bytes CA FE BA BE . If these same bytes are then unpacked using little-endian format, what integer value results? [Valoarea 0xCAFEBABE este împachetată folosind formatul big-endian, producând octeții CA FE BA BE . Dacă aceiași octeți sunt apoi despachetați folosind formatul little-endian, ce valoare întreagă rezultă?]

- **a)  0xBEBAFECA**
- **b)  0xCAFEBABE (unchanged) [0xCAFEBABE (neschimbat)]**
- **c)  0xEFACEBAB**
- **d)  0xBABECAFE**

> 💡 **Feedback:** When big-endian bytes CA FE BA BE are read in little-endian order, the least significant byte (CA) is at the lowest address, producing 0xBEBAFECA. This demonstrates why endianness mismatch causes data corruption — the same bytes yield completely different integer values. A common misconception is that the value remains unchanged regardless of byte order interpretation. [Când octeții big-endian CA FE BA BE sunt citiți în ordinea little-endian, cel mai puțin semnificativ octet (CA) este la adresa cea mai mică, producând 0xBEBAFECA. Aceasta demonstrează de ce nepotrivirea ordinii octeților (endianness) cauzează coruperea datelor — aceiași octeți produc valori întregi complet diferite. O concepție greșită frecventă este că valoarea rămâne neschimbată indiferent de interpretarea ordinii octeților.]

---

### Q39. `Multiple Choice`
**Meaning of "!" Prefix in Python struct Format / Semnificația prefixului «!» în formatul struct din Python**

> In Python's struct module, what does the ! byte-order prefix specify? [În modulul struct al Python, ce specifică prefixul de ordine a octeților ! ?]

- **a)  Network byte order (big-endian) [Ordinea octeților de rețea (big-endian)]**
- **b)  Native byte order of the host machine [Ordinea nativă a octeților a calculatorului gazdă]**
- **c)  Little-endian byte order [Ordinea octeților little-endian]**
- **d)  No byte order conversion (raw bytes) [Fără conversie a ordinii octeților (octeți brut)]**

> 💡 **Feedback:** The "!" prefix specifies network byte order, which is defined as big-endian. It is functionally equivalent to ">" for standard sizes. A common misconception is that "!" specifies the native byte order of the host machine, but "=" is the prefix for native byte order. [Prefixul «!» specifică ordinea octeților de rețea, care este definită ca big-endian. Este funcțional echivalent cu «>» pentru dimensiuni standard. O concepție greșită frecventă este că «!» specifică ordinea nativă a octeților a calculatorului gazdă, dar «=» este prefixul pentru ordinea nativă a octeților.]

---

### Q40. `Multiple Choice`
**CRC-32 Mask in Python / Masca CRC-32 în Python**

> When computing CRC-32 in Python with zlib.crc32(data) , why is the result masked with & 0xFFFFFFFF ? [Când se calculează CRC-32 în Python cu zlib.crc32(data) , de ce se aplică masca & 0xFFFFFFFF asupra rezultatului?]

- **a)  To ensure the result is unsigned 32-bit, since some platforms return a signed integer [Pentru a asigura un rezultat fără semn pe 32 de biți, deoarece unele platforme returnează un întreg cu semn]**
- **b)  To truncate the CRC from 64 bits to 32 bits for efficiency [Pentru a trunchia CRC-ul de la 64 biți la 32 biți pentru eficiență]**
- **c)  To add cryptographic security to the checksum [Pentru a adăuga securitate criptografică sumei de control]**
- **d)  To convert the CRC-32 checksum from big-endian network order to little-endian host format [Pentru a converti suma de control CRC-32 din ordinea de rețea big-endian în formatul little-endian al gazdei]**

> 💡 **Feedback:** On some Python versions, zlib.crc32() may return a signed integer. Masking with 0xFFFFFFFF ensures a consistent unsigned 32-bit result across all platforms. A common misconception is that this mask adds cryptographic security or performs byte-order conversion — it is purely a cross-platform compatibility measure. [Pe unele versiuni Python, zlib.crc32() poate returna un întreg cu semn. Mascarea cu 0xFFFFFFFF asigură un rezultat consistent fără semn pe 32 de biți pe toate platformele. O concepție greșită frecventă este că această mască adaugă securitate criptografică sau efectuează conversia ordinii octeților — este pur și simplu o măsură de compatibilitate între platforme.]

---


## §3.  Numerical (Răspuns numeric)   (13 questions)

### Q41. `Numerical`
**PASV Port Calculation / Calculul portului PASV**

> An FTP server responds with: 227 Entering Passive Mode (10,0,0,5,195,130) . What is the port number the client should connect to? [Un server FTP răspunde cu: 227 Entering Passive Mode (10,0,0,5,195,130) . Care este numărul de port la care trebuie să se conecteze clientul?]

> 🔑 *Hint: Hint: answer format — digits only (no units). If decimals are needed, use '.' as the decimal separator. [Indiciu: format răspuns — doar cifre (fără unități). Dacă sunt necesare zecimale, folosiți '.' ca separator.]*


> 💡 **Feedback:** The PASV response encodes the port as two octets: p1 and p2. The port is calculated as p1 × 256 + p2 = 195 × 256 + 130 = 49920 + 130 = (...). A common mistake is to concatenate the numbers (195130) or use only one of them. [Răspunsul PASV codifică portul ca doi octeți: p1 și p2. Portul se calculează ca p1 × 256 + p2 = 195 × 256 + 130 = 49920 + 130 = (...). O greșeală frecventă este concatenarea numerelor (195130) sau utilizarea doar a unuia dintre ele.]

---

### Q42. `Numerical`
**PASV Port Calculation — High Byte Dominant / Calculul portului PASV — Octet superior dominant**

> An FTP server responds with 227 Entering Passive Mode (172,29,9,10,195,88) . Calculate the passive data port number using the formula port = p1 × 256 + p2. [Un server FTP răspunde cu 227 Entering Passive Mode (172,29,9,10,195,88) . Calculați numărul portului de date pasiv folosind formula port = p1 × 256 + p2.]

> 🔑 *Hint: Hint: answer format — digits only (no units). If decimals are needed, use '.' as the decimal separator. [Indiciu: format răspuns — doar cifre (fără unități). Dacă sunt necesare zecimale, folosiți '.' ca separator.]*


> 💡 **Feedback:** Port = 195 × 256 + 88 = 49920 + 88 = (...). The two-byte port encoding splits the 16-bit port number into a high byte (p1) and low byte (p2). [Port = 195 × 256 + 88 = 49920 + 88 = (...). Codificarea portului pe doi octeți împarte numărul de port pe 16 biți în octetul superior (p1) și octetul inferior (p2).]

---

### Q43. `Numerical`
**PASV Port with Small Values / Port PASV cu valori mici**

> An FTP server in the laboratory responds with 227 Entering Passive Mode (10,0,0,1,0,21) . Using the formula port = p1 × 256 + p2, what is the passive data port? [Un server FTP din laborator răspunde cu 227 Entering Passive Mode (10,0,0,1,0,21) . Folosind formula port = p1 × 256 + p2, care este portul de date pasiv?]

> 🔑 *Hint: Hint: answer format — digits only (no units). If decimals are needed, use '.' as the decimal separator. [Indiciu: format răspuns — doar cifre (fără unități). Dacă sunt necesare zecimale, folosiți '.' ca separator.]*


> 💡 **Feedback:** Port = 0 × 256 + (...) = (...). When p1 is 0, the port equals p2 directly. This particular case yields port (...), which is the standard FTP control port — an unusual but valid configuration for the data channel. [Port = 0 × 256 + (...) = (...). Când p1 este 0, portul este egal direct cu p2. Acest caz particular dă portul (...), care este portul standard de control FTP — o configurație neobișnuită dar validă pentru canalul de date.]

---

### Q44. `Numerical`
**Calculate PASV Port from (192,168,1,5,234,100) / Calcularea portului PASV din (192,168,1,5,234,100)**

> An FTP server responds with: 227 Entering Passive Mode (192,168,1,5,234,100) . What port number should the client connect to for the data transfer? [Un server FTP răspunde cu: 227 Entering Passive Mode (192,168,1,5,234,100) . La ce număr de port ar trebui să se conecteze clientul pentru transferul de date?]

> 🔑 *Hint: Hint: answer format — digits only (no units). If decimals are needed, use '.' as the decimal separator. [Indiciu: format răspuns — doar cifre (fără unități). Dacă sunt necesare zecimale, folosiți '.' ca separator.]*


> 💡 **Feedback:** The PASV port is calculated as (p1 × 256) + p2 = (234 × 256) + 100 = 59904 + 100 = (...). A common misconception is that the port number is simply the last number in the response (100), but the FTP PASV encoding uses two octets: port = p1 × 256 + p2. [Portul PASV se calculează ca (p1 × 256) + p2 = (234 × 256) + 100 = 59904 + 100 = (...). O concepție greșită frecventă este că numărul portului este pur și simplu ultimul număr din răspuns (100), dar codificarea FTP PASV folosește doi octeți: port = p1 × 256 + p2.]

---

### Q45. `Numerical`
**Calculate PASV Port from (10,0,0,1,0,21) / Calcularea portului PASV din (10,0,0,1,0,21)**

> An FTP PASV response contains the values (10,0,0,1,0,21) . What is the data channel port number? [Un răspuns FTP PASV conține valorile (10,0,0,1,0,21) . Care este numărul portului canalului de date?]

> 🔑 *Hint: Hint: answer format — digits only (no units). If decimals are needed, use '.' as the decimal separator. [Indiciu: format răspuns — doar cifre (fără unități). Dacă sunt necesare zecimale, folosiți '.' ca separator.]*


> 💡 **Feedback:** Port = (0 × 256) + (...) = (...). This happens to coincide with the standard FTP control port number. A common misconception is that port (...) cannot be used for data, but any valid port number can be the result of the PASV calculation. [Port = (0 × 256) + (...) = (...). Aceasta coincide cu numărul portului standard de control FTP. O concepție greșită frecventă este că portul (...) nu poate fi folosit pentru date, dar orice număr de port valid poate fi rezultatul calculului PASV.]

---

### Q46. `Numerical`
**Calculate PASV Port from (172,29,9,10,195,88) / Calcularea portului PASV din (172,29,9,10,195,88)**

> An FTP PASV response contains the values (172,29,9,10,195,88) . Calculate the data channel port number. [Un răspuns FTP PASV conține valorile (172,29,9,10,195,88) . Calculați numărul portului canalului de date.]

> 🔑 *Hint: Hint: answer format — digits only (no units). If decimals are needed, use '.' as the decimal separator. [Indiciu: format răspuns — doar cifre (fără unități). Dacă sunt necesare zecimale, folosiți '.' ca separator.]*


> 💡 **Feedback:** Port = (195 × 256) + 88 = 49920 + 88 = (...). The formula port = p1 × 256 + p2 must be applied consistently. A common misconception is to reverse p1 and p2, yielding an incorrect port of (88 × 256) + 195 = 22723. [Port = (195 × 256) + 88 = 49920 + 88 = (...). Formula port = p1 × 256 + p2 trebuie aplicată consecvent. O concepție greșită frecventă este inversarea p1 și p2, obținând un port incorect de (88 × 256) + 195 = 22723.]

---

### Q47. `Numerical`
**Calculate PASV Port from (10,0,0,5,156,64) / Calcularea portului PASV din (10,0,0,5,156,64)**

> An FTP PASV response contains the values (10,0,0,5,156,64) . Calculate the data channel port number using the formula port = p1 × 256 + p2. [Un răspuns FTP PASV conține valorile (10,0,0,5,156,64) . Calculați numărul portului canalului de date folosind formula port = p1 × 256 + p2.]

> 🔑 *Hint: Hint: answer format — digits only (no units). If decimals are needed, use '.' as the decimal separator. [Indiciu: format răspuns — doar cifre (fără unități). Dacă sunt necesare zecimale, folosiți '.' ca separator.]*


> 💡 **Feedback:** Port = (156 × 256) + 64 = 39936 + 64 = (...). The IP address would be 10.0.0.5. A common misconception is to add all six numbers together instead of applying the two-octet formula to only the last two values. [Port = (156 × 256) + 64 = 39936 + 64 = (...). Adresa IP ar fi 10.0.0.5. O concepție greșită frecventă este adunarea tuturor celor șase numere în loc de aplicarea formulei cu doi octeți doar asupra ultimelor două valori.]

---

### Q48. `Numerical`
**CRC-32 Output Size in Bits / Dimensiunea ieșirii CRC-32 în biți**

> CRC-32 produces a fixed-size output regardless of the input data size. How many bits does a CRC-32 checksum contain? [CRC-32 produce o ieșire de dimensiune fixă indiferent de dimensiunea datelor de intrare. Câți biți conține o sumă de control (checksum) CRC-32?]

> 🔑 *Hint: Hint: answer format — digits only (no units). If decimals are needed, use '.' as the decimal separator. [Indiciu: format răspuns — doar cifre (fără unități). Dacă sunt necesare zecimale, folosiți '.' ca separator.]*


> 💡 **Feedback:** CRC-(...) always produces a (...)-bit (4-byte) checksum. The "(...)" in the name directly indicates the output size, with the value ranging from 0 to 2^(...) - 1 (0x00000000 to 0xFFFFFFFF). A common misconception is to confuse the output size with input size limitations — CRC-(...) can process inputs of any length but always produces exactly (...) bits. [CRC-(...) produce întotdeauna o sumă de control de (...) de biți (4 octeți). Cifra «(...)» din nume indică direct dimensiunea ieșirii, cu valoarea variind de la 0 la 2^(...) - 1 (0x00000000 la 0xFFFFFFFF). O concepție greșită frecventă este confuzia între dimensiunea ieșirii și limitările dimensiunii intrării — CRC-(...) poate procesa intrări de orice lungime, dar produce întotdeauna exact (...) de biți.]

---

### Q49. `Numerical`
**struct.calcsize for Protocol Header / struct.calcsize pentru antetul protocolului**

> What is the result of struct.calcsize(">4sIII") ? Answer in bytes. [Care este rezultatul struct.calcsize(">4sIII") ? Răspundeți în octeți.]

> 🔑 *Hint: Hint: answer format — digits only (no units). If decimals are needed, use '.' as the decimal separator. [Indiciu: format răspuns — doar cifre (fără unități). Dacă sunt necesare zecimale, folosiți '.' ca separator.]*


> 💡 **Feedback:** The format >4sIII breaks down as: 4s = 4 bytes (magic), I = 4 bytes (length), I = 4 bytes (CRC), I = 4 bytes (flags). Total: 4 + 4 + 4 + 4 = (...) bytes. The > prefix specifies big-endian and does not contribute to the size. [Formatul >4sIII se descompune astfel: 4s = 4 octeți (magic), I = 4 octeți (lungime), I = 4 octeți (CRC), I = 4 octeți (flaguri). Total: 4 + 4 + 4 + 4 = (...) octeți. Prefixul > specifică big-endian și nu contribuie la dimensiune.]

---

### Q50. `Numerical`
**Total Message Size with Header and Payload / Dimensiunea totală a mesajului cu antet și sarcină utilă**

> A binary protocol uses a 12-byte header (format "!2sBBII" ) followed by a payload. If the payload is the UTF-8 encoding of the ASCII string "Hello" (5 bytes), what is the total message size in bytes? [Un protocol binar folosește un antet de 12 octeți (format "!2sBBII" ) urmat de o sarcină utilă. Dacă sarcina utilă este codificarea UTF-8 a șirului ASCII „Hello" (5 octeți), care este dimensiunea totală a mesajului în octeți?]

> 🔑 *Hint: Hint: answer format — digits only (no units). If decimals are needed, use '.' as the decimal separator. [Indiciu: format răspuns — doar cifre (fără unități). Dacă sunt necesare zecimale, folosiți '.' ca separator.]*


> 💡 **Feedback:** Total = header (12 bytes) + payload (5 bytes) = (...) bytes. The header size is fixed regardless of payload content; the length field inside the header stores the value 5. [Total = antet (12 octeți) + sarcină utilă (5 octeți) = (...) octeți. Dimensiunea antetului este fixă indiferent de conținutul sarcinii utile; câmpul lungime din antet stochează valoarea 5.]

---

### Q51. `Numerical`
**Wrong Endianness Value / Valoarea la ordinea greșită a octeților**

> The 4-byte big-endian representation of the integer 5 is 00 00 00 05 . If these bytes are mistakenly interpreted as a little-endian unsigned 32-bit integer, what decimal value results? [Reprezentarea big-endian pe 4 octeți a întregului 5 este 00 00 00 05 . Dacă acești octeți sunt interpretați greșit ca un întreg fără semn pe 32 de biți în little-endian, ce valoare zecimală rezultă?]

> 🔑 *Hint: Hint: answer format — digits only (no units). If decimals are needed, use '.' as the decimal separator. [Indiciu: format răspuns — doar cifre (fără unități). Dacă sunt necesare zecimale, folosiți '.' ca separator.]*


> 💡 **Feedback:** In little-endian, the bytes 00 00 00 05 are read with the first byte as LSB: 0×1 + 0×256 + 0×65536 + 5×16777216 = (...). This demonstrates why using the wrong byte order causes catastrophic misinterpretation. [În little-endian, octeții 00 00 00 05 sunt citiți cu primul octet ca LSB: 0×1 + 0×256 + 0×65536 + 5×16777216 = (...). Aceasta demonstrează de ce utilizarea ordinii greșite a octeților cauzează o interpretare greșită catastrofală.]

---

### Q52. `Numerical`
**struct.calcsize for Protocol Header "&gt;4sBBII" / struct.calcsize pentru antetul de protocol «&gt;4sBBII»**

> A binary protocol header uses the struct format ">4sBBII" , which consists of: magic (4-byte string), type (unsigned byte), flags (unsigned byte), length (unsigned int), and CRC (unsigned int). How many bytes does struct.calcsize(">4sBBII") return? [Un antet de protocol binar folosește formatul struct «>4sBBII» , compus din: magic (șir de 4 octeți), tip (octet fără semn), fanioane (octet fără semn), lungime (întreg fără semn) și CRC (întreg fără semn). Câți octeți returnează struct.calcsize(">4sBBII") ?]

> 🔑 *Hint: Hint: answer format — digits only (no units). If decimals are needed, use '.' as the decimal separator. [Indiciu: format răspuns — doar cifre (fără unități). Dacă sunt necesare zecimale, folosiți '.' ca separator.]*


> 💡 **Feedback:** The calculation: 4s = 4 bytes, B = 1 byte, B = 1 byte, I = 4 bytes, I = 4 bytes. Total = 4 + 1 + 1 + 4 + 4 = (...) bytes. A common misconception is to assume padding is inserted between fields, but with the ">" prefix (standard sizes), no padding is added. [Calculul: 4s = 4 octeți, B = 1 octet, B = 1 octet, I = 4 octeți, I = 4 octeți. Total = 4 + 1 + 1 + 4 + 4 = (...) octeți. O concepție greșită frecventă este presupunerea că se inserează spațiere (padding) între câmpuri, dar cu prefixul «>» (dimensiuni standard), nu se adaugă padding.]

---

### Q53. `Numerical`
**Total Message Size — 12-byte Header Plus 5-byte Payload / Dimensiunea totală a mesajului — antet de 12 octeți plus sarcină utilă de 5 octeți**

> A protocol uses a 12-byte header (format ">2sBBII" : magic 2B, version 1B, flags 1B, length 4B, CRC 4B) followed by a payload. If the payload is the string "Hello" (5 bytes), what is the total message size in bytes? [Un protocol folosește un antet de 12 octeți (format «>2sBBII» : magic 2O, versiune 1O, fanioane 1O, lungime 4O, CRC 4O) urmat de o sarcină utilă (payload). Dacă sarcina utilă este șirul «Hello» (5 octeți), care este dimensiunea totală a mesajului în octeți?]

> 🔑 *Hint: Hint: answer format — digits only (no units). If decimals are needed, use '.' as the decimal separator. [Indiciu: format răspuns — doar cifre (fără unități). Dacă sunt necesare zecimale, folosiți '.' ca separator.]*


> 💡 **Feedback:** Header = 2+1+1+4+4 = 12 bytes. Payload = 5 bytes ("Hello"). Total = 12 + 5 = (...) bytes. A common misconception is to assume padding is added to align the total to a power of 2, but binary protocols typically use exact sizes without padding. [Antet = 2+1+1+4+4 = 12 octeți. Sarcină utilă = 5 octeți («Hello»). Total = 12 + 5 = (...) octeți. O concepție greșită frecventă este presupunerea că se adaugă spațiere (padding) pentru a alinia totalul la o putere a lui 2, dar protocoalele binare folosesc de obicei dimensiuni exacte fără padding.]

---
