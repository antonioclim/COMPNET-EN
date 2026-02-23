# Computer Networks — Week 2
### *Rețele de calculatoare — Săptămâna 2*

> Practice Questions / Întrebări de practică

---

## 📚 Lecture Questions / Întrebări de curs

### Q1. `N01.C04.Q02` — Socket State After bind() and listen() / Starea socket-ului după bind() și listen()

*[Multiple Choice — Alegere multiplă]*

After a TCP server executes bind() and listen(), what socket state will ss -tln display for that port? [După ce un server TCP execută bind() și listen(), ce stare a socket-ului va afișa ss -tln pentru acel port?]

- **a)** LISTEN - the socket is passively waiting for incoming connections [LISTEN - socket-ul așteaptă pasiv conexiuni de intrare]
- **b)** ESTABLISHED - the socket is actively transferring data with a connected peer [ESTABLISHED - socket-ul transferă activ date cu un partener conectat]
- **c)** SYN_SENT - the socket has initiated a connection attempt to a remote host [SYN_SENT - socket-ul a inițiat o tentativă de conexiune către o gazdă la distanță]
- **d)** CLOSED - the socket exists but has not started any network operations yet [CLOSED - socket-ul există, dar nu a început nicio operațiune de rețea]

> 💡 **Feedback:**
> *After bind() and listen(), the socket enters the LISTEN state - it is waiting for incoming connection requests. Data transfer only occurs in the ESTABLISHED state, which requires a client to connect via the three-way handshake. [După bind() și listen(), socket-ul intră în starea LISTEN - așteaptă cereri de conexiune. Transferul de date are loc doar în starea ESTABLISHED, care necesită conectarea unui client prin handshake-ul în trei pași.]*


---

### Q2. `N01.C04.Q06` — TIME_WAIT State Purpose / Scopul stării TIME_WAIT

*[Multiple Choice — Alegere multiplă]*

After a TCP connection is closed, the initiating side enters the TIME_WAIT state. What is the primary purpose of this state? [După închiderea unei conexiuni TCP, partea care inițiază intră în starea TIME_WAIT. Care este scopul principal al acestei stări?]

- **a)** To allow delayed duplicate segments from the old connection to expire before port reuse [Pentru a permite segmentelor duplicate întârziate de la vechea conexiune să expire înainte de reutilizarea portului]
- **b)** To keep the port reserved indefinitely so no other application can bind to it [Pentru a păstra portul rezervat pe termen nedefinit, astfel încât nicio altă aplicație să nu se poată lega de el]
- **c)** To immediately free kernel memory associated with the closed socket descriptor [Pentru a elibera imediat memoria kernel asociată cu descriptorul de socket închis]

> 💡 **Feedback:**
> *TIME_WAIT lasts 2×MSL (Maximum Segment Lifetime) to ensure any delayed duplicate segments from the old connection expire before a new connection reuses the same port pair. Without TIME_WAIT, a new connection could receive stale data from the previous one. [TIME_WAIT durează 2×MSL (durata maximă de viață a segmentului) pentru a asigura că orice segmente duplicate întârziate de la vechea conexiune expiră înainte ca o nouă conexiune să refolosească aceeași pereche de porturi. Fără TIME_WAIT, o nouă conexiune ar putea primi date învechite de la cea anterioară.]*


---

### Q3. `N01.T00.Q07` — Scenario - Why ss Over netstat / Scenariu - De ce ss în loc de netstat

*[Multiple Choice — Alegere multiplă]*

A student instructor recommends using ss instead of netstat for socket inspection. Which technical justification best supports this recommendation? [Instructorul unui student recomandă utilizarea ss în loc de netstat pentru inspecția socket-urilor. Ce justificare tehnică susține cel mai bine această recomandare?]

- **a)** ss uses netlink to query the kernel directly, making it faster and more detailed than netstat's /proc parsing [ss folosește netlink pentru a interoga kernelul direct, făcându-l mai rapid și mai detaliat decât analiza /proc a netstat]
- **b)** ss provides built-in packet capture functionality that netstat does not support at all [ss oferă funcționalitate de captură de pachete încorporată pe care netstat nu o suportă deloc]
- **c)** netstat requires root privileges for all operations while ss can run as a regular unprivileged user [netstat necesită privilegii root pentru toate operațiunile, în timp ce ss poate rula ca utilizator obișnuit neprivilegiat]

> 💡 **Feedback:**
> *ss queries the kernel directly via netlink sockets, which is significantly faster than netstat's approach of reading /proc filesystem entries. Additionally, ss is actively maintained while netstat is being removed from modern distributions. [ss interoghează kernelul direct prin socket-uri netlink, ceea ce este semnificativ mai rapid decât abordarea netstat de citire a intrărilor din sistemul de fișiere /proc. În plus, ss este întreținut activ, în timp ce netstat este eliminat din distribuțiile moderne.]*


---

### Q4. `N01.T00.Q14` — Evaluating Socket Timeout Design / Evaluarea designului de timeout al socket-ului

*[Multiple Choice — Alegere multiplă]*

The ex_1_02_tcp_server_client.py exercise in the Week 1 lab uses a blocking recv(1024) without a timeout. A colleague proposes adding socket.settimeout(5) to both server and client. Which statement best evaluates this proposal? [Exercițiul ex_1_02_tcp_server_client.py din laboratorul Săptămânii 1 folosește un recv(1024) blocant fără timeout. Un coleg propune adăugarea socket.settimeout(5) atât la server, cât și la client. Care afirmație evaluează cel mai bine această propunere?]

- **a)** Server timeout is beneficial (prevents hang on client disconnect), but client timeout should be calibrated independently — a fixed 5 s may be too short under server load [Timeout-ul serverului este benefic (previne blocarea la deconectarea clientului), dar timeout-ul clientului ar trebui calibrat independent — 5 s fixe pot fi prea puțin sub sarcină]
- **b)** The proposal is entirely correct — both server and client should always share the same timeout value to ensure symmetrical behaviour across the connection [Propunerea este complet corectă — atât serverul, cât și clientul ar trebui să partajeze întotdeauna aceeași valoare de timeout pentru comportament simetric]
- **c)** Timeouts should never be added to socket code because they cause socket.timeout exceptions that crash the programme if not caught in a try-except block [Timeout-urile nu ar trebui niciodată adăugate la codul de socket deoarece cauzează excepții socket.timeout care opresc programul dacă nu sunt prinse]
- **d)** The proposal is unnecessary because TCP's built-in keepalive mechanism automatically detects dead connections and closes them within seconds on loopback [Propunerea este inutilă deoarece mecanismul keepalive TCP detectează automat conexiunile moarte și le închide în câteva secunde pe loopback]

> 💡 **Feedback:**
> *A 5-second timeout on the server's accept/recv is beneficial — it prevents indefinite hangs when clients disconnect unexpectedly. However, applying the same timeout to the client is risky if the server takes longer than 5 seconds to respond under load. The correct approach differentiates: server timeout prevents resource leaks; client timeout should be calibrated to expected response time. [Un timeout de 5 secunde pe accept/recv la server este benefic — previne blocările indefinite. Dar aplicarea aceluiași timeout la client este riscantă dacă serverul necesită mai mult timp sub sarcină.]*


---

### Q5. `N02.C01.Q01` — Number of layers in the OSI reference model / Numărul de straturi din modelul de referință OSI

*[Multiple Choice — Alegere multiplă]*

The Open Systems Interconnection (OSI) reference model, developed by ISO in the 1980s, divides network communication into how many distinct layers? [Modelul de referință OSI (Open Systems Interconnection), dezvoltat de ISO în anii 1980, împarte comunicația în rețea în câte straturi distincte?]

- **a)** 7
- **b)** 4
- **c)** 5
- **d)** 6

> 💡 **Feedback:**
> *The OSI model defines exactly seven layers: Physical, Data Link, Network, Transport, Session, Presentation, and Application. A common misconception is confusing the OSI model with the TCP/IP model, which has only 4 layers — students often answer "4" because they conflate the two models. [Modelul OSI definește exact șapte straturi: Fizic, Legătură de date, Rețea, Transport, Sesiune, Prezentare și Aplicație. O concepție greșită frecventă este confundarea modelului OSI cu modelul TCP/IP, care are doar 4 straturi — studenții răspund adesea „4" deoarece confundă cele două modele.]*


---

### Q6. `N02.C01.Q04` — OSI layer where IP addressing operates / Stratul OSI unde operează adresarea IP

*[Multiple Choice — Alegere multiplă]*

At which layer of the OSI model does IP (Internet Protocol) addressing and routing take place? [La ce strat al modelului OSI au loc adresarea și rutarea IP (Internet Protocol)?]

- **a)** Layer 3 — Network [Stratul 3 — Rețea]
- **b)** Layer 2 — Data Link [Stratul 2 — Legătură de date]
- **c)** Layer 4 — Transport [Stratul 4 — Transport]
- **d)** Layer 5 — Session [Stratul 5 — Sesiune]

> 💡 **Feedback:**
> *IP operates at Layer 3 (Network layer), which is responsible for logical addressing and routing packets between networks. A common misconception is placing IP at the Data Link Layer (Layer 2), which handles physical (MAC) addressing within a single network segment, not logical inter-network routing. [IP operează la Stratul 3 (Stratul de rețea), responsabil pentru adresarea logică și rutarea pachetelor între rețele. O concepție greșită frecventă este plasarea IP la Stratul legătură de date (Stratul 2), care se ocupă de adresarea fizică (MAC) în cadrul unui singur segment de rețea, nu de rutarea logică între rețele.]*


---

### Q7. `N02.C01.Q05` — TCP/IP Application layer maps to which OSI layers / Stratul Aplicație TCP/IP corespunde căror straturi OSI

*[Multiple Choice — Alegere multiplă]*

Which OSI layers are consolidated into the single Application layer of the TCP/IP model? [Care straturi OSI sunt consolidate în unicul strat Aplicație al modelului TCP/IP?]

- **a)** Layers 5, 6, and 7 [Straturile 5, 6 și 7]
- **b)** Layer 7 only [Doar Stratul 7]
- **c)** Layers 6 and 7 [Straturile 6 și 7]
- **d)** Layers 4, 5, 6, and 7 [Straturile 4, 5, 6 și 7]

> 💡 **Feedback:**
> *The TCP/IP Application layer combines OSI Layers 5 (Session), 6 (Presentation), and 7 (Application) into a single layer. This is one of the key simplifications of the TCP/IP model. A common error is selecting "Layer 7 only," which ignores the consolidation of session management and data representation functions that OSI separates into distinct layers. [Stratul Aplicație TCP/IP combină straturile OSI 5 (Sesiune), 6 (Prezentare) și 7 (Aplicație) într-un singur strat. Aceasta este una dintre simplificările esențiale ale modelului TCP/IP. O eroare frecventă este selectarea „doar Stratul 7", care ignoră consolidarea funcțiilor de gestionare a sesiunii și de reprezentare a datelor, pe care OSI le separă în straturi distincte.]*


---

### Q8. `N02.C01.Q06` — Encapsulation process in the protocol stack / Procesul de încapsulare în stiva de protocoale

*[Multiple Choice — Alegere multiplă]*

What is the term for the process by which each layer of the protocol stack adds its own header (and sometimes trailer) to the data received from the layer above? [Care este termenul pentru procesul prin care fiecare strat al stivei de protocoale adaugă propriul antet (și uneori trailer) datelor primite de la stratul superior?]

- **a)** Encapsulation [Încapsulare]
- **b)** Decapsulation [Decapsulare]
- **c)** Multiplexing [Multiplexare]
- **d)** Fragmentation [Fragmentare]

> 💡 **Feedback:**
> *Encapsulation is the process of wrapping data with protocol headers at each layer: application data becomes a segment (at the Transport Layer), then a packet (at the Network Layer), then a frame (at the Data Link Layer). A common misconception is confusing encapsulation with multiplexing; multiplexing combines multiple data streams into one channel, whereas encapsulation adds layer-specific control information around the data. [Încapsularea este procesul de împachetare a datelor cu antete de protocol la fiecare strat: datele aplicației devin segment (la Stratul de transport), apoi pachet (la Stratul de rețea), apoi cadru (la Stratul legătură de date). O concepție greșită frecventă este confundarea încapsulării cu multiplexarea; multiplexarea combină mai multe fluxuri de date într-un singur canal, în timp ce încapsularea adaugă informații de control specifice stratului în jurul datelor.]*


---

### Q9. `N02.C02.Q04` — TCP preserves application message boundaries / TCP păstrează delimitarea mesajelor aplicației

*[True/False — Adevărat/Fals]*

TCP guarantees that if a sender calls send(b"Hello") followed by send(b"World"), the receiver will receive them as two separate messages in two recv() calls. [TCP garantează că, dacă un expeditor apelează send(b"Hello") urmat de send(b"World"), receptorul le va primi ca două mesaje separate în două apeluri recv().]

- **a)** True / Adevărat
- **b)** False / Fals

> 💡 **Feedback:**
> *This is false. TCP is a byte-stream protocol with no concept of message boundaries. The receiver might get "HelloWorld" in one recv() call, or "Hel" then "loWorld," or any other split of the bytes. Applications must implement their own framing (length prefix, delimiter, or fixed size). This is the most critical misconception in socket programming (Misconception #1): on localhost, small messages often arrive intact due to minimal latency, creating a false sense of guaranteed boundaries. [Fals. TCP este un protocol de tip flux de octeți, fără conceptul de delimitare a mesajelor. Receptorul ar putea primi „HelloWorld" într-un singur apel recv(), sau „Hel" apoi „loWorld", sau orice altă împărțire a octeților. Aplicațiile trebuie să implementeze propria delimitare (prefix de lungime, delimiter sau dimensiune fixă). Aceasta este cea mai critică concepție greșită în programarea cu socket-uri (Concepția greșită nr. 1): pe localhost, mesajele mici ajung adesea intacte datorită latenței minime, creând o falsă impresie de delimitare garantată.]*


---

### Q10. `N02.C03.Q02` — Ephemeral port range / Intervalul de porturi efemere

*[Multiple Choice — Alegere multiplă]*

Which range of port numbers are classified as ephemeral ports, dynamically assigned by the operating system to client sockets? [Care interval de numere de port este clasificat ca porturi efemere, atribuite dinamic de sistemul de operare socket-urilor client?]

- **a)** 49152--65535
- **b)** 0--1023
- **c)** 1024--49151
- **d)** 1024--65535

> 💡 **Feedback:**
> *Ephemeral ports span 49152--65535 (as defined by IANA). Well-known ports are 0--1023, and registered ports are 1024--49151. A common error is selecting 1024--65535, which incorrectly merges the registered and ephemeral ranges into a single category. The three-tier port classification is important for understanding which ports require administrative privileges. [Porturile efemere acoperă intervalul 49152--65535 (conform definiției IANA). Porturile bine-cunoscute sunt 0--1023, iar porturile înregistrate sunt 1024--49151. O eroare frecventă este selectarea intervalului 1024--65535, care îmbină incorect intervalele de porturi înregistrate și efemere într-o singură categorie. Clasificarea în trei niveluri a porturilor este importantă pentru înțelegerea porturilor care necesită privilegii administrative.]*


---

### Q11. `N02.C04.Q01` — Python socket type constant for TCP / Constanta Python pentru tipul de socket TCP

*[Multiple Choice — Alegere multiplă]*

Which Python socket type constant creates a reliable, connection-oriented byte stream socket (i.e., a TCP socket)? [Care constantă Python de tip socket creează un socket fiabil, orientat pe conexiune, de tip flux de octeți (adică un socket TCP)?]

- **a)** SOCK_STREAM
- **b)** SOCK_DGRAM
- **c)** SOCK_RAW
- **d)** SOCK_TCP

> 💡 **Feedback:**
> *SOCK_STREAM provides a reliable byte-stream abstraction and corresponds to TCP. SOCK_DGRAM corresponds to UDP datagrams. A common misconception is assuming a constant named SOCK_TCP exists; in reality, socket types are specified abstractly as "stream" or "datagram" rather than by protocol name. [SOCK_STREAM oferă o abstracție fiabilă de flux de octeți și corespunde protocolului TCP. SOCK_DGRAM corespunde datagramelor UDP. O concepție greșită frecventă este presupunerea că există o constantă numită SOCK_TCP; în realitate, tipurile de socket sunt specificate abstract ca „stream" sau „datagram", nu prin numele protocolului.]*


---

### Q12. `N02.C04.Q03` — Operations NOT required for a UDP server / Operații care NU sunt necesare pentru un server UDP

*[Multiple Choice — Alegere multiplă]*

Which of the following socket operations are not used by a UDP server? [Care dintre următoarele operații pe socket nu sunt utilizate de un server UDP?]

- **a)** listen() and accept() [listen() și accept()]
- **b)** bind() and recvfrom() [bind() și recvfrom()]
- **c)** socket() and bind() [socket() și bind()]
- **d)** sendto() and close() [sendto() și close()]

> 💡 **Feedback:**
> *listen() and accept() are TCP-only operations. A UDP server simply creates a socket, binds it, and uses recvfrom()/sendto() in a loop — no connection establishment is needed. A common misconception is that all servers must call listen(); this is only true for TCP servers, since UDP has no connection queue concept. [listen() și accept() sunt operații exclusiv TCP. Un server UDP creează pur și simplu un socket, îl asociază prin bind() și folosește recvfrom()/sendto() într-o buclă — nu este necesară stabilirea unei conexiuni. O concepție greșită frecventă este că toate serverele trebuie să apeleze listen(); acest lucru este valabil doar pentru serverele TCP, deoarece UDP nu are conceptul de coadă de conexiuni.]*


---

### Q13. `N02.C04.Q04` — Purpose of bind() vs connect() / Scopul funcțiilor bind() versus connect()

*[Multiple Choice — Alegere multiplă]*

What is the fundamental difference between bind() and connect() in socket programming? [Care este diferența fundamentală între bind() și connect() în programarea cu socket-uri?]

- **a)** bind() assigns a local address; connect() initiates a connection to a remote address [bind() asociază o adresă locală; connect() inițiază o conexiune la o adresă la distanță]
- **b)** They both associate a socket with an address; only the port number differs [Ambele asociază un socket cu o adresă; diferă doar numărul de port, ceea ce le face funcțional interschimbabile în proiectarea client-server]
- **c)** bind() is for TCP and connect() is for UDP [bind() este pentru TCP, iar connect() este pentru UDP]
- **d)** bind() sends a SYN packet; connect() sends a SYN-ACK packet [bind() trimite un pachet SYN; connect() trimite un pachet SYN-ACK]

> 💡 **Feedback:**
> *bind() assigns a local address (IP:port) to a socket, telling the OS where to listen. connect() initiates communication toward a remote address. They serve opposite purposes (Misconception #5). The phone analogy clarifies: bind() is "this is my phone number," whereas connect() is "I am calling this number." [bind() asociază o adresă locală (IP:port) unui socket, indicând sistemului de operare unde să asculte. connect() inițiază comunicarea către o adresă la distanță. Cele două funcții servesc scopuri opuse (Concepția greșită nr. 5). Analogia telefonică clarifică: bind() este „acesta este numărul meu de telefon", în timp ce connect() este „sun la acest număr".]*


---

### Q14. `N02.C04.Q06` — What accept() returns on a TCP server / Ce returnează accept() pe un server TCP

*[Multiple Choice — Alegere multiplă]*

When a TCP server calls sock.accept(), what does it return? [Când un server TCP apelează sock.accept(), ce returnează acesta?]

- **a)** A tuple of (new_socket, client_address) for the accepted connection [Un tuplu de forma (socket_nou, adresa_clientului) pentru conexiunea acceptată]
- **b)** The received data bytes from the client [Octeții de date primiți de la client]
- **c)** A boolean indicating whether the connection was successful [O valoare booleană indicând dacă conexiunea a reușit, permițând serverului să verifice starea înainte de a iniția transferul de date]
- **d)** The same listening socket, now connected to the client [Același socket de ascultare, acum conectat la client]

> 💡 **Feedback:**
> *accept() extracts the first pending connection from the queue and returns a new socket object dedicated to that client, along with the client's address tuple. The original listening socket continues to accept further connections. A common misconception is that accept() transforms the listening socket into a connected socket; in reality, it creates a separate new socket for each client. [accept() extrage prima conexiune în așteptare din coadă și returnează un nou obiect socket dedicat acelui client, împreună cu tuplul de adresă al clientului. Socket-ul original de ascultare continuă să accepte conexiuni ulterioare. O concepție greșită frecventă este că accept() transformă socket-ul de ascultare într-un socket conectat; în realitate, creează un socket nou separat pentru fiecare client.]*


---

### Q15. `N02.C05.Q01` — Iterative vs threaded server total time for 10 clients / Timpul total server iterativ versus server cu fire de execuție pentru 10 clienți

*[Multiple Choice — Alegere multiplă]*

Ten clients connect simultaneously to a server. Each request takes 100 ms to process. What is the approximate total time until all clients receive responses for an iterative server vs. a threaded server? [Zece clienți se conectează simultan la un server. Fiecare cerere necesită 100 ms pentru procesare. Care este timpul total aproximativ până când toți clienții primesc răspunsuri pentru un server iterativ versus un server cu fire de execuție?]

- **a)** Iterative: \~1000 ms; Threaded: \~100 ms [Iterativ: \~1000 ms; Cu fire: \~100 ms]
- **b)** Iterative: \~100 ms; Threaded: \~100 ms [Iterativ: \~100 ms; Cu fire: \~100 ms]
- **c)** Iterative: \~1000 ms; Threaded: \~1000 ms [Iterativ: \~1000 ms; Cu fire: \~1000 ms]
- **d)** Iterative: \~100 ms; Threaded: \~1000 ms [Iterativ: \~100 ms; Cu fire: \~1000 ms]

> 💡 **Feedback:**
> *An iterative server processes clients one at a time (10 x 100 ms = 1000 ms total). A threaded server handles all 10 in parallel, completing in approximately 100 ms plus minor thread overhead. A common misconception (Misconception #4) is that threading always improves performance; for a single short-lived client, threading adds unnecessary overhead. [Un server iterativ procesează clienții pe rând (10 x 100 ms = 1000 ms total). Un server cu fire de execuție gestionează toți cei 10 în paralel, finalizând în aproximativ 100 ms plus overhead minor de fire. O concepție greșită frecventă (Concepția greșită nr. 4) este că firele de execuție îmbunătățesc întotdeauna performanța; pentru un singur client cu cerere scurtă, firele adaugă overhead inutil.]*


---

### Q16. `N02.T00.Q08` — Understanding what accept() returns on a TCP server / Înțelegerea valorii returnate de accept() pe un server TCP

*[Multiple Choice — Alegere multiplă]*

On a TCP server, the code conn, addr = sock.accept() returns two values. In the context of handling multiple clients, what is the primary purpose of the conn object? [Pe un server TCP, codul conn, addr = sock.accept() returnează două valori. În contextul gestionării mai multor clienți, care este scopul principal al obiectului conn?]

- **a)** A new socket dedicated to the specific client, separate from the listening socket which remains available for more connections. [Un socket nou dedicat clientului specific, separat de socket-ul de ascultare care rămâne disponibil pentru mai multe conexiuni.]
- **b)** A reference to the same listening socket, configured to communicate with the specific client who connected. [O referință la același socket de ascultare, configurat pentru a comunica cu clientul specific care s-a conectat.]
- **c)** A copy of the listening socket that replaces the original; the server must call listen() again after each accept(). [O copie a socket-ului de ascultare care înlocuiește originalul; serverul trebuie să apeleze listen() din nou după fiecare accept().]
- **d)** A UDP datagram socket automatically created to handle the client's data more efficiently. [Un socket de tip datagramă UDP creat automat pentru a gestiona datele clientului mai eficient.]

> 💡 **Feedback:**
> *accept() creates and returns a brand new socket (conn) that is exclusively dedicated to communicating with the client who just connected. The original listening socket (sock) remains open and continues to accept new connections. This separation is what enables a server to handle multiple clients simultaneously — each client gets its own dedicated socket while the listening socket keeps accepting. The addr tuple contains the client's IP address and ephemeral port number. [accept() creează și returnează un socket complet nou (conn) care este dedicat exclusiv comunicării cu clientul care tocmai s-a conectat. Socket-ul de ascultare original (sock) rămâne deschis și continuă să accepte conexiuni noi. Această separare este ceea ce permite unui server să gestioneze mai mulți clienți simultan — fiecare client primește propriul socket dedicat în timp ce socket-ul de ascultare continuă să accepte. Tuplul addr conține adresa IP a clientului și numărul de port efemer.]*


---

### Q17. `N02.T00.Q10` — Code tracing — socket resource management with context managers / Trasarea codului — gestionarea resurselor socket cu manageri de context

*[Multiple Choice — Alegere multiplă]*

A student writes a server loop that creates a new socket for each client but forgets to close them. After serving approximately 1000 clients, the server crashes with "Too many open files". Which statement best explains the underlying resource management issue and the recommended solution? [Un student scrie o buclă de server care creează un socket nou pentru fiecare client dar uită să le închidă. După deservirea a aproximativ 1000 de clienți, serverul se blochează cu „Too many open files". Care afirmație explică cel mai bine problema de gestionare a resurselor și soluția recomandată?]

- **a)** Sockets consume file descriptors which are limited by the OS; use context managers (with statement) to guarantee automatic cleanup. [Socket-urile consumă descriptori de fișier care sunt limitați de sistemul de operare; folosiți manageri de context (instrucțiunea with) pentru a garanta curățarea automată.]
- **b)** Python's garbage collector should handle socket cleanup automatically; the error is caused by the OS running out of memory instead. [Colectorul de gunoi Python ar trebui să gestioneze automat curățarea socket-urilor; eroarea este cauzată de epuizarea memoriei de către sistemul de operare.]
- **c)** The solution is to increase the OS file descriptor limit rather than changing the code. [Soluția este creșterea limitei de descriptori de fișier a sistemului de operare, nu modificarea codului.]
- **d)** The error occurs because TCP sockets cannot be reused; switching to UDP would avoid the file descriptor exhaustion. [Eroarea apare deoarece socket-urile TCP nu pot fi reutilizate; trecerea la UDP ar evita epuizarea descriptorilor de fișier.]

> 💡 **Feedback:**
> *Each socket consumes a file descriptor — a limited OS resource (typically 1024 by default on Linux). Without explicit close() or a context manager (with statement), sockets accumulate even after the client disconnects. Python's garbage collector may eventually reclaim them, but this is non-deterministic and far too slow for a server handling many connections. The recommended solution is using context managers: with socket.socket() as sock: guarantees the socket is closed when the block exits, even if an exception occurs. This pattern should be enforced for both the listening socket and each client connection socket. [Fiecare socket consumă un descriptor de fișier — o resursă limitată a sistemului de operare (de obicei 1024 implicit pe Linux). Fără close() explicit sau un manager de context (instrucțiunea with), socket-urile se acumulează chiar și după ce clientul se deconectează. Colectorul de gunoi Python le poate recupera eventual, dar aceasta este nedeterministă și prea lentă pentru un server care gestionează multe conexiuni. Soluția recomandată este utilizarea managerilor de context: with socket.socket() as sock: garantează că socket-ul este închis când blocul se termină, chiar dacă apare o excepție. Acest model ar trebui aplicat atât pentru socket-ul de ascultare cât și pentru fiecare socket de conexiune cu clientul.]*


---

### Q18. `N02.C01.Q03` — PDU at the Transport Layer for TCP / Unitatea PDU la Stratul de transport pentru TCP

*[Multiple Choice — Alegere multiplă]*

What is the Protocol Data Unit (PDU) at the Transport Layer when TCP is used? [Care este unitatea de date a protocolului (PDU) la Stratul de transport când se utilizează TCP?]

- **a)** Segment [Segment]
- **b)** Packet [Pachet]
- **c)** Frame [Cadru]
- **d)** Bit [Bit]

> 💡 **Feedback:**
> *The Transport Layer PDU for TCP is called a segment. Each layer has its own specific PDU name: UDP uses datagrams, the Network Layer uses packets, and the Data Link Layer uses frames. A common misconception is using "packet" generically for all layers, but strictly speaking, "packet" refers only to the Network Layer (Layer 3) PDU. [Unitatea PDU a Stratului de transport pentru TCP se numește segment. Fiecare strat are propria denumire specifică de PDU: UDP folosește datagrame, Stratul de rețea folosește pachete, iar Stratul legătură de date folosește cadre. O concepție greșită frecventă este utilizarea termenului „pachet" generic pentru toate straturile, dar, strict vorbind, „pachet" se referă doar la unitatea PDU de la Stratul de rețea (Stratul 3).]*


---

### Q19. `N02.T00.Q04` — Identifying TCP handshake completion in a Wireshark capture / Identificarea finalizării handshake-ului TCP într-o captură Wireshark

*[Multiple Choice — Alegere multiplă]*

A student captures traffic between a client and server using Wireshark. The student observes the following packet sequence:\
(1) SYN from client,\
(2) SYN-ACK from server,\
(3) ACK from client,\
(4) PSH-ACK from client carrying data. At which point is the TCP connection fully established? [Un student captează traficul între un client și un server folosind Wireshark. Studentul observă următoarea secvență de pachete: (1) SYN de la client,\
(2) SYN-ACK de la server,\
(3) ACK de la client,\
(4) PSH-ACK de la client cu date. În ce moment este conexiunea TCP complet stabilită?]

- **a)** After packet 3 (the client's ACK completing the three-way handshake). [După pachetul 3 (ACK-ul clientului care completează handshake-ul în trei pași).]
- **b)** After packet 2 (the server's SYN-ACK acknowledging the client's SYN). [După pachetul 2 (SYN-ACK-ul serverului care confirmă SYN-ul clientului).]
- **c)** After packet 4 (the first data packet confirms the connection works). [După pachetul 4 (primul pachet de date confirmă că conexiunea funcționează).]
- **d)** After packet 1 (the client's SYN initiates the ESTABLISHED state). [După pachetul 1 (SYN-ul clientului inițiază starea ESTABLISHED).]

> 💡 **Feedback:**
> *The TCP connection is fully established (ESTABLISHED state on both sides) after packet 3, the final ACK of the three-way handshake. Packet 4 is already application data transfer. The three-way handshake ensures both sides have synchronised their sequence numbers and agreed on connection parameters (window size, MSS, etc.). The PSH flag in packet 4 tells the receiving OS to push data to the application immediately rather than buffering. [Conexiunea TCP este complet stabilită (starea ESTABLISHED pe ambele părți) după pachetul 3, ACK-ul final al handshake-ului în trei pași. Pachetul 4 este deja transfer de date al aplicației. Handshake-ul în trei pași asigură că ambele părți și-au sincronizat numerele de secvență și au convenit asupra parametrilor conexiunii (dimensiunea ferestrei, MSS etc.). Indicatorul PSH din pachetul 4 spune sistemului de operare receptor să livreze datele aplicației imediat, fără a le stoca în buffer.]*


---

### Q20. `N02.T00.Q07` — Socket close() and TIME_WAIT state implications / Implicațiile close() și stării TIME_WAIT ale socket-ului

*[Multiple Choice — Alegere multiplă]*

A student restarts a TCP server immediately after stopping it and receives the error "Address already in use" on the bind() call. What is the primary cause and the most appropriate fix for development? [Un student repornește un server TCP imediat după oprirea lui și primește eroarea „Address already in use" la apelul bind(). Care este cauza principală și soluția cea mai potrivită pentru dezvoltare?]

- **a)** The previous socket is in TIME_WAIT state; set SO_REUSEADDR before bind() to allow rebinding. [Socket-ul anterior este în starea TIME_WAIT; setați SO_REUSEADDR înainte de bind() pentru a permite reasocierea.]
- **b)** Another process has taken over the port; use kill -9 to forcefully terminate it before rebinding. [Un alt proces a preluat portul; folosiți kill -9 pentru a-l termina forțat înainte de reasociere.]
- **c)** The OS permanently blocks the port after use; choose a different port number each time. [Sistemul de operare blochează permanent portul după utilizare; alegeți un număr de port diferit de fiecare dată.]
- **d)** The error occurs because the server used a well-known port; switching to an ephemeral port avoids it. [Eroarea apare deoarece serverul a folosit un port bine-cunoscut; trecerea la un port efemer o evită.]

> 💡 **Feedback:**
> *After a TCP connection is closed, the socket enters TIME_WAIT state for approximately 2×MSL (Maximum Segment Lifetime, typically 60 seconds total). During TIME_WAIT, the OS reserves the port to handle any delayed packets from the previous connection. The SO_REUSEADDR socket option tells the OS to allow rebinding to a port in TIME_WAIT — essential during development when frequent restarts are needed. This is NOT a bug; TIME_WAIT is a deliberate TCP design feature to prevent packet confusion between old and new connections. [După închiderea unei conexiuni TCP, socket-ul intră în starea TIME_WAIT pentru aproximativ 2×MSL (Maximum Segment Lifetime, de obicei 60 de secunde în total). În timpul TIME_WAIT, sistemul de operare rezervă portul pentru a gestiona pachetele întârziate de la conexiunea anterioară. Opțiunea de socket SO_REUSEADDR spune sistemului de operare să permită reasocierea la un port în TIME_WAIT — esențial în timpul dezvoltării când repornirile frecvente sunt necesare. Aceasta NU este o eroare; TIME_WAIT este o caracteristică deliberată de proiectare TCP pentru a preveni confuzia între pachetele conexiunilor vechi și noi.]*


---

### Q21. `N02.T00.Q09` — OSI to TCP/IP layer mapping / Maparea straturilor OSI la TCP/IP

*[Multiple Choice — Alegere multiplă]*

The TCP/IP model combines several OSI layers into fewer layers. Which statement most accurately describes how the TCP/IP Application Layer relates to the OSI model? [Modelul TCP/IP combină mai multe straturi OSI în mai puține straturi. Care afirmație descrie cel mai precis cum se raportează Stratul Aplicație TCP/IP la modelul OSI?]

- **a)** The TCP/IP Application Layer combines OSI Layers 5 (Session), 6 (Presentation), and 7 (Application) into one layer. [Stratul Aplicație TCP/IP combină Straturile OSI 5 (Sesiune), 6 (Prezentare) și 7 (Aplicație) într-un singur strat.]
- **b)** The TCP/IP Application Layer maps directly to OSI Layer 7 only, ignoring Sessions and Presentation. [Stratul Aplicație TCP/IP se mapează direct doar pe Stratul 7 OSI, ignorând Sesiunea și Prezentarea.]
- **c)** The TCP/IP Application Layer combines OSI Layers 4 (Transport) and 7 (Application) into one layer. [Stratul Aplicație TCP/IP combină Straturile OSI 4 (Transport) și 7 (Aplicație) într-un singur strat.]
- **d)** The TCP/IP Application Layer corresponds to OSI Layers 6 and 7, while Layer 5 maps to TCP/IP Transport. [Stratul Aplicație TCP/IP corespunde Straturilor OSI 6 și 7, în timp ce Stratul 5 se mapează pe Transport TCP/IP.]

> 💡 **Feedback:**
> *The TCP/IP Application Layer merges OSI Layers 5 (Session), 6 (Presentation), and 7 (Application) into a single layer. This means application protocols like HTTP handle not only user-facing functionality but also session management and data formatting — responsibilities that the OSI model distributes across three separate layers. This consolidation reflects the pragmatic nature of TCP/IP: in practice, most applications handle these concerns themselves. A common error is confusing the 4-layer TCP/IP model with the 5-layer hybrid model found in some textbooks. [Stratul Aplicație TCP/IP unește Straturile OSI 5 (Sesiune), 6 (Prezentare) și 7 (Aplicație) într-un singur strat. Aceasta înseamnă că protocoalele de aplicație precum HTTP gestionează nu doar funcționalitatea orientată către utilizator, ci și managementul sesiunii și formatarea datelor — responsabilități pe care modelul OSI le distribuie în trei straturi separate. Această consolidare reflectă natura pragmatică a TCP/IP: în practică, majoritatea aplicațiilor gestionează aceste aspecte ele însele. O eroare frecventă este confundarea modelului TCP/IP cu 4 straturi cu modelul hibrid cu 5 straturi din unele manuale.]*


---

## 🔬 Lab Questions / Întrebări de laborator


---

### Q22. `N01.S05.Q01` — socket.AF_INET Meaning / Semnificația socket.AF_INET

*[Multiple Choice — Alegere multiplă]*

In Python's socket module, what does socket.AF_INET specify when creating a socket? [În modulul socket din Python, ce specifică socket.AF_INET la crearea unui socket?]

- **a)** The IPv4 address family (Internet Protocol version 4) [Familia de adrese IPv4 (Internet Protocol versiunea 4)]
- **b)** The TCP transport protocol (Transmission Control Protocol) [Protocolul de transport TCP (Transmission Control Protocol)]
- **c)** A raw socket mode for direct Layer 2 frame access [Un mod socket brut pentru acces direct la cadre de Nivel 2]
- **d)** The maximum buffer size for incoming data reception [Dimensiunea maximă a bufferului pentru recepția datelor de intrare]

> 💡 **Feedback:**
> *AF_INET specifies the IPv4 address family. Combined with SOCK_STREAM it creates a TCP/IPv4 socket; with SOCK_DGRAM it creates a UDP/IPv4 socket. For IPv6, one would use AF_INET6. [AF_INET specifică familia de adrese IPv4. Combinat cu SOCK_STREAM creează un socket TCP/IPv4; cu SOCK_DGRAM creează un socket UDP/IPv4. Pentru IPv6, s-ar folosi AF_INET6.]*


---

### Q23. `N01.S05.Q02` — SOCK_STREAM vs SOCK_DGRAM / SOCK_STREAM versus SOCK_DGRAM

*[Multiple Choice — Alegere multiplă]*

What is the fundamental difference between socket.SOCK_STREAM and socket.SOCK_DGRAM? [Care este diferența fundamentală între socket.SOCK_STREAM și socket.SOCK_DGRAM?]

- **a)** SOCK_STREAM provides a reliable ordered byte stream (TCP); SOCK_DGRAM sends independent unreliable datagrams (UDP) [SOCK_STREAM oferă un flux de octeți ordonat fiabil (TCP); SOCK_DGRAM trimite datagrame independente nefiabile (UDP)]
- **b)** SOCK_STREAM uses IPv4 addressing exclusively for all socket operations; SOCK_DGRAM uses IPv6 addressing for all communications [SOCK_STREAM folosește adresarea IPv4 exclusiv pentru toate operațiunile de socket; SOCK_DGRAM folosește adresarea IPv6 pentru toate comunicațiile]
- **c)** SOCK_DGRAM is encrypted by default for secure data exchange; SOCK_STREAM transmits in plaintext [SOCK_DGRAM este criptat implicit pentru schimb securizat de date; SOCK_STREAM transmite în text clar]

> 💡 **Feedback:**
> *SOCK_STREAM creates a TCP socket (connection-oriented, reliable, ordered byte stream). SOCK_DGRAM creates a UDP socket (connectionless, unreliable, message-oriented datagrams). [SOCK_STREAM creează un socket TCP (orientat pe conexiune, fiabil, flux de octeți ordonat). SOCK_DGRAM creează un socket UDP (fără conexiune, nefiabil, datagrame orientate pe mesaj).]*


---

### Q24. `N01.S05.Q03` — connect_ex() Return Value / Valoarea returnată de connect_ex()

*[Multiple Choice — Alegere multiplă]*

In the code tracing exercise, socket.connect_ex((host, port)) is used to check if a port is open. What does it return when the connection fails because no server is listening? [În exercițiul de urmărire a codului, socket.connect_ex((host, port)) este folosit pentru a verifica dacă un port este deschis. Ce returnează când conexiunea eșuează deoarece niciun server nu ascultă?]

- **a)** A non-zero error code (e.g. 111 for ECONNREFUSED) - zero indicates success [Un cod de eroare diferit de zero (de ex. 111 pentru ECONNREFUSED) - zero indică succes]
- **b)** It returns None and sets an internal errno attribute on the socket object [Returnează None și setează un atribut errno intern pe obiectul socket]
- **c)** It raises a ConnectionRefusedError exception that must be caught with try-except [Aruncă o excepție ConnectionRefusedError care trebuie prinsă cu try-except]

> 💡 **Feedback:**
> *connect_ex() returns 0 on success and an error code otherwise. Error 111 (ECONNREFUSED) means no server is listening on that port. Unlike connect(), it does not raise an exception on failure. [connect_ex() returnează 0 la succes și un cod de eroare în caz contrar. Eroarea 111 (ECONNREFUSED) înseamnă că niciun server nu ascultă pe acel port. Spre deosebire de connect(), nu aruncă o excepție la eșec.]*


---

### Q25. `N01.S05.Q04` — TCP Server Socket Sequence / Secvența socket-ului server TCP

*[Multiple Choice — Alegere multiplă]*

In Python, what is the correct sequence of method calls to set up a TCP server socket that accepts one client? [În Python, care este secvența corectă de apeluri de metode pentru a configura un socket server TCP care acceptă un client?]

- **a)** socket() → bind() → listen() → accept()
- **b)** socket() → listen() → bind() → accept()
- **c)** socket() → connect() → bind() → listen()
- **d)** socket() → accept() → bind() → listen()

> 💡 **Feedback:**
> *The canonical TCP server sequence is: socket() → bind() → listen() → accept(). bind() assigns the address, listen() marks it as passive, and accept() blocks until a client connects. [Secvența canonică a serverului TCP este: socket() → bind() → listen() → accept(). bind() atribuie adresa, listen() îl marchează ca pasiv, iar accept() blochează până când un client se conectează.]*


---

### Q26. `N02.S01.Q01` — Socket option to allow immediate rebind after restart / Opțiunea de socket pentru reconectare imediată după repornire

*[Multiple Choice — Alegere multiplă]*

Which socket option should be set on a server socket to allow immediate rebinding to a port that is still in TIME_WAIT state after a previous server instance was stopped? [Care opțiune de socket trebuie setată pe un socket de server pentru a permite reconectarea imediată la un port aflat încă în starea TIME_WAIT după oprirea unei instanțe anterioare a serverului?]

- **a)** SO_REUSEADDR
- **b)** SO_KEEPALIVE
- **c)** SO_BROADCAST
- **d)** SO_LINGER

> 💡 **Feedback:**
> *SO_REUSEADDR allows binding to a port in TIME_WAIT state, preventing the common "Address already in use" error during development and server restarts. Without this option, you must wait approximately 60 seconds (the TIME_WAIT duration) before the port becomes available again. A common misconception (Misconception #10) is that close() immediately frees the port; in reality, TIME_WAIT persists to handle delayed packets from the old connection. [SO_REUSEADDR permite asocierea la un port aflat în starea TIME_WAIT, prevenind eroarea frecventă „Address already in use" în timpul dezvoltării și repornirilor de server. Fără această opțiune, trebuie să așteptați aproximativ 60 de secunde (durata TIME_WAIT) înainte ca portul să devină disponibil. O concepție greșită frecventă (Concepția greșită nr. 10) este că close() eliberează imediat portul; în realitate, TIME_WAIT persistă pentru a gestiona pachetele întârziate de la vechea conexiune.]*


---

### Q27. `N02.S01.Q03` — Correct TCP server socket call order / Ordinea corectă a apelurilor socket pentru server TCP

*[Multiple Choice — Alegere multiplă]*

What is the correct order of socket API calls to set up a TCP server that accepts connections? [Care este ordinea corectă a apelurilor API socket pentru a configura un server TCP care acceptă conexiuni?]

- **a)** socket() → bind() → listen() → accept()
- **b)** socket() → listen() → bind() → accept()
- **c)** socket() → bind() → accept() → listen()
- **d)** socket() → connect() → listen() → accept()

> 💡 **Feedback:**
> *A TCP server must create a socket, bind it to a local address, call listen() to mark it as passive, then accept() to extract pending connections from the queue. Calling listen() before bind() would fail because the socket has no local address yet. A common error is inserting connect() instead of listen(), confusing the server-side and client-side API flows. [Un server TCP trebuie să creeze un socket, să-l asocieze la o adresă locală prin bind(), să apeleze listen() pentru a-l marca ca pasiv, apoi accept() pentru a extrage conexiunile în așteptare din coadă. Apelarea listen() înainte de bind() ar eșua deoarece socket-ul nu are încă o adresă locală. O eroare frecventă este inserarea connect() în locul listen(), confundând fluxurile API pe partea de server și pe partea de client.]*


---

### Q28. `N02.S01.Q04` — Threading target function reference vs call / Referință versus apel de funcție în target-ul Thread

*[Multiple Choice — Alegere multiplă]*

When creating a thread to handle a client, what is wrong with the following code? [Când se creează un fir de execuție pentru a gestiona un client, ce este greșit în următorul cod?]t = threading.Thread(target=handle_client(conn, addr))

- **a)** It calls the function immediately in the current thread instead of passing the function reference to the new thread [Apelează funcția imediat în firul curent în loc să transmită referința funcției către noul fir de execuție]
- **b)** The Thread class does not accept a target parameter [Clasa Thread nu acceptă un parametru target]
- **c)** Threads cannot accept arguments — only global variables accessible to all running threads within the current module can be used [Firele de execuție nu pot accepta argumente — doar variabilele globale pot fi utilizate, ceea ce necesită gestionarea stării partajate prin structuri de date accesibile tuturor firelor din modulul curent]
- **d)** The parentheses are required; this code is correct [Parantezele sunt obligatorii; acest cod este corect]

> 💡 **Feedback:**
> *Using target=handle_client(conn, addr) immediately calls the function and passes its return value as target. The correct form is target=handle_client, args=(conn, addr) which passes the function object itself. This is a Python-specific pitfall: parentheses after a function name invoke it, while omitting parentheses references the function as a first-class object. [Utilizarea target=handle_client(conn, addr) apelează imediat funcția și transmite valoarea returnată ca target. Forma corectă este target=handle_client, args=(conn, addr), care transmite obiectul funcției în sine. Aceasta este o capcană specifică Python: parantezele după numele unei funcții o invocă, în timp ce omiterea parantezelor referențiază funcția ca obiect de primă clasă.]*


---

### Q29. `N02.S02.Q01` — Code output for SOCK_DGRAM type comparison / Rezultatul codului pentru comparația tipului SOCK_DGRAM

*[Multiple Choice — Alegere multiplă]*

What does the following Python code print? [Ce afișează următorul cod Python?]import socket\
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)\
print(s.type == socket.SOCK_STREAM)

- **a)** False
- **b)** True
- **c)** None
- **d)** An error is raised [Se ridică o eroare]

> 💡 **Feedback:**
> *The socket was created with SOCK_DGRAM (UDP). Comparing its type to SOCK_STREAM (TCP) returns False because they are different constants. This is a code-tracing exercise testing whether students can identify which socket type was used at creation time. A common error is confusing the constants, not realising that SOCK_DGRAM and SOCK_STREAM represent fundamentally different transport semantics. [Socket-ul a fost creat cu SOCK_DGRAM (UDP). Compararea tipului său cu SOCK_STREAM (TCP) returnează False deoarece sunt constante diferite. Acesta este un exercițiu de trasare a codului care testează dacă studenții pot identifica ce tip de socket a fost folosit la creare. O eroare frecventă este confundarea constantelor, fără a realiza că SOCK_DGRAM și SOCK_STREAM reprezintă semantici de transport fundamental diferite.]*


---

### Q30. `N02.S02.Q02` — UDP application protocol response to "ping" command / Răspunsul protocolului de aplicație UDP la comanda „ping"

*[Multiple Choice — Alegere multiplă]*

In the Week 2 UDP server exercise, what does the server respond when a client sends the command "ping"? [În exercițiul cu serverul UDP din Săptămâna 2, ce răspunde serverul când un client trimite comanda "ping"?]

- **a)** PONG
- **b)** OK
- **c)** ping
- **d)** ACK

> 💡 **Feedback:**
> *The UDP exercise application protocol defines the "ping" command as a connectivity test that returns "PONG". This demonstrates that even though UDP is connectionless, a request-response pattern is perfectly viable — the same socket both sends and receives (addressing Misconception #2). [Protocolul aplicației din exercițiul UDP definește comanda „ping" ca un test de conectivitate care returnează „PONG". Aceasta demonstrează că, deși UDP este fără conexiune, un model cerere-răspuns este perfect viabil — același socket atât trimite, cât și primește (abordând Concepția greșită nr. 2).]*


---

### Q31. `N02.S04.Q02` — Command to identify process using a port / Comanda pentru identificarea procesului care folosește un port

*[Multiple Choice — Alegere multiplă]*

You encounter the error OSError: [Errno 98] Address already in use when starting your server on port 12345. Which command best identifies the process currently occupying that port? [Întâlniți eroarea OSError: [Errno 98] Address already in use la pornirea serverului pe portul 12345. Care comandă identifică cel mai bine procesul care ocupă în prezent acel port?]

- **a)** lsof -i :12345
- **b)** netstat -r
- **c)** ifconfig -a
- **d)** ping 127.0.0.1

> 💡 **Feedback:**
> *The command lsof -i :12345 lists all open file descriptors (including sockets) associated with port 12345, showing the responsible process ID and name. This error typically occurs because a previous server instance was not properly closed and the socket is in TIME_WAIT state (Misconception #10), or because another application is using the same port. [Comanda lsof -i :12345 listează toți descriptorii de fișiere deschise (inclusiv socket-uri) asociați cu portul 12345, afișând ID-ul și numele procesului responsabil. Această eroare apare de obicei deoarece o instanță anterioară a serverului nu a fost închisă corespunzător și socket-ul se află în starea TIME_WAIT (Concepția greșită nr. 10), sau deoarece altă aplicație folosește același port.]*


---

### Q32. `N02.S04.Q04` — bind() sends packets on the network / bind() trimite pachete în rețea

*[True/False — Adevărat/Fals]*

Calling sock.bind(("0.0.0.0", 12345)) on a TCP server socket causes packets to be sent over the network. [Apelarea sock.bind(("0.0.0.0", 12345)) pe un socket de server TCP provoacă trimiterea de pachete în rețea.]

- **a)** True / Adevărat
- **b)** False / Fals

> 💡 **Feedback:**
> *False. bind() is a purely local operation that assigns an address to a socket within the kernel. No network traffic is generated. The first network traffic appears when a client calls connect(), triggering the three-way handshake. A common misconception is confusing bind() with connect(); only connect() generates network packets (SYN). [Fals. bind() este o operație pur locală care asociază o adresă unui socket în cadrul nucleului. Nu se generează trafic de rețea. Primul trafic de rețea apare când un client apelează connect(), declanșând handshake-ul în trei pași. O concepție greșită frecventă este confundarea bind() cu connect(); doar connect() generează pachete de rețea (SYN).]*


---

### Q33. `N02.S04.Q08` — Closing a socket immediately frees the port / Închiderea unui socket eliberează imediat portul

*[True/False — Adevărat/Fals]*

After calling sock.close() on a TCP server socket, the port is immediately available for another process to bind to. [După apelarea sock.close() pe un socket de server TCP, portul este imediat disponibil pentru ca alt proces să facă bind la el.]

- **a)** True / Adevărat
- **b)** False / Fals

> 💡 **Feedback:**
> *False. TCP sockets enter TIME_WAIT state (typically 60 seconds) after closing to handle any delayed packets still in transit. Use SO_REUSEADDR to allow rebinding during development, or wait for the timeout to expire. This is a critical practical issue (Misconception #10): students frequently encounter "Address already in use" when restarting servers during development, and the solution is to set SO_REUSEADDR before calling bind(). [Fals. Socket-urile TCP intră în starea TIME_WAIT (de obicei 60 de secunde) după închidere pentru a gestiona pachetele întârziate aflate încă în tranzit. Utilizați SO_REUSEADDR pentru a permite reconectarea în timpul dezvoltării, sau așteptați expirarea timeout-ului. Aceasta este o problemă practică critică (Concepția greșită nr. 10): studenții întâlnesc frecvent eroarea „Address already in use" la repornirea serverelor în timpul dezvoltării, iar soluția este setarea SO_REUSEADDR înainte de apelul bind().]*


---

### Q34. `N02.S03.Q02` — TCP vs UDP minimum packet count for single exchange / Numărul minim de pachete TCP versus UDP pentru un singur schimb

*[Multiple Choice — Alegere multiplă]*

A client sends one message and receives one response, then disconnects. Approximately how many minimum packets would be visible in Wireshark for TCP vs. UDP? [Un client trimite un mesaj și primește un răspuns, apoi se deconectează. Aproximativ câte pachete minime ar fi vizibile în Wireshark pentru TCP versus UDP?]

- **a)** TCP: \~10 packets; UDP: 2 packets [TCP: \~10 pachete; UDP: 2 pachete]
- **b)** TCP: 2 packets; UDP: 2 packets [TCP: 2 pachete; UDP: 2 pachete]
- **c)** TCP: \~10 packets; UDP: \~10 packets [TCP: \~10 pachete; UDP: \~10 pachete]
- **d)** TCP: 3 packets; UDP: 2 packets [TCP: 3 pachete; UDP: 2 pachete]

> 💡 **Feedback:**
> *TCP requires approximately 10 packets (3 handshake + 2 data + 2 ACKs + 3 teardown), while UDP requires only 2 packets (one request datagram, one response datagram) with no setup or teardown overhead. This stark difference illustrates why UDP is preferred for simple query-response protocols like DNS. A common error is underestimating TCP's overhead by forgetting the handshake and teardown phases. [TCP necesită aproximativ 10 pachete (3 handshake + 2 date + 2 confirmări ACK + 3 terminare), în timp ce UDP necesită doar 2 pachete (o datagramă de cerere, o datagramă de răspuns) fără overhead de stabilire sau terminare. Această diferență marcantă ilustrează de ce UDP este preferat pentru protocoale simple de tip cerere-răspuns precum DNS. O eroare frecventă este subestimarea overhead-ului TCP prin uitarea fazelor de handshake și terminare.]*


---

### Q35. `N02.S04.Q05` — listen() generates network packets / listen() generează pachete de rețea

*[True/False — Adevărat/Fals]*

Calling sock.listen(5) on a TCP server socket generates network packets visible in Wireshark. [Apelarea sock.listen(5) pe un socket de server TCP generează pachete de rețea vizibile în Wireshark.]

- **a)** True / Adevărat
- **b)** False / Fals

> 💡 **Feedback:**
> *False. listen() is a local operation that marks the socket as passive and sets the connection backlog queue size. No packets are sent — packets only appear when clients initiate connections with connect(). Both bind() and listen() are purely local kernel configurations; only connect(), send(), and close() generate actual network traffic. [Fals. listen() este o operație locală care marchează socket-ul ca pasiv și stabilește dimensiunea cozii de conexiuni în așteptare. Nu se trimit pachete — pachetele apar doar când clienții inițiază conexiuni cu connect(). Atât bind(), cât și listen() sunt configurări pur locale ale nucleului; doar connect(), send() și close() generează trafic de rețea efectiv.]*
