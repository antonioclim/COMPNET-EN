# Week 08 — Computer Networks
### *Rețele de Calculatoare — Săptămâna 8*

> Question Pool — Practice Set

---


## W08 — Curs / Lecture   (26 questions)

### 1. `Multiple Choice`
**N01.C04.Q01: Three-Way Handshake Sequence / Secvența handshake-ului în trei pași**

> What is the correct sequence of flag exchanges during a TCP three-way handshake? [Care este secvența corectă de schimburi de steaguri în timpul unui handshake TCP în trei pași?]

- **a) SYN -> SYN-ACK -> ACK**
- **b) SYN -> ACK -> SYN-ACK**
- **c) ACK -> SYN -> SYN-ACK**
- **d) SYN-ACK -> SYN -> ACK**

> 💡 **Feedback:** The client sends a SYN, the server responds with SYN-ACK (acknowledging the client's SYN while sending its own), and the client completes with an ACK. After these three segments, the connection is ESTABLISHED on both sides. [Clientul trimite un SYN, serverul răspunde cu SYN-ACK (confirmând SYN-ul clientului în timp ce trimite propriul SYN), iar clientul completează cu un ACK. După aceste trei segmente, conexiunea este ESTABLISHED pe ambele părți.]

---

### 2. `Multiple Choice`
**N01.C04.Q04: Purpose of FIN Flag / Scopul steagului FIN**

> In TCP, what does the FIN flag signal when sent by a host? [În TCP, ce semnalează steagul FIN când este trimis de o gazdă?]

- **a) The sender has finished transmitting and wants to close its side of the connection [Emițătorul a terminat de transmis și dorește să închidă partea sa de conexiune]**
- **b) The sender detected a fatal error and is forcibly aborting the TCP connection [Emițătorul a detectat o eroare fatală și anulează forțat conexiunea TCP]**
- **c) The sender is requesting that the receiver flush its buffers and process all pending data [Emițătorul solicită receptorului să golească bufferele și să proceseze toate datele în așteptare]**

> 💡 **Feedback:** FIN (Finish) indicates the sender has no more data to transmit and wishes to close its half of the connection. The peer must acknowledge the FIN and may continue sending data until it also sends its own FIN. This is called a half-close. [FIN (Finish) indică faptul că emițătorul nu mai are date de transmis și dorește să închidă jumătatea sa de conexiune. Partenerul trebuie să confirme FIN-ul și poate continua să trimită date până când trimite și el propriul FIN. Aceasta se numește semi-închidere.]

---

### 3. `Multiple Choice`
**N02.C02.Q06: Number of handshakes when client sends 10 messages / Numărul de handshake-uri când clientul trimite 10 mesaje**

> A TCP client calls connect(), sends 10 messages with send(), then calls close(). How many three-way handshakes (SYN → SYN-ACK → ACK) occur during this entire session? [Un client TCP apelează connect(), trimite 10 mesaje cu send(), apoi apelează close(). Câte handshake-uri în trei pași (SYN → SYN-ACK → ACK) au loc în timpul întregii sesiuni?]

- **a) 1**
- **b) 10**
- **c) 11**
- **d) 12**

> 💡 **Feedback:** The three-way handshake occurs only once, at the time connect() is called. After that, the connection remains open for all data transfers until close() initiates the FIN teardown sequence. A common misconception (Misconception #7) is that each send() triggers a new handshake, similar to how each HTTP request in HTTP/(...).0 required a new connection. In reality, TCP maintains a persistent connection. [Handshake-ul în trei pași are loc o singură dată, în momentul apelului connect(). După aceea, conexiunea rămâne deschisă pentru toate transferurile de date până când close() inițiază secvența de terminare cu FIN. O concepție greșită frecventă (Concepția greșită nr. 7) este că fiecare send() declanșează un nou handshake, similar modului în care fiecare cerere HTTP în HTTP/(...).0 necesita o nouă conexiune. În realitate, TCP menține o conexiune persistentă.]

---

### 4. `Multiple Choice`
**N07.C01.Q05: Purpose of TCP FIN Flag / Scopul flagului TCP FIN**

> After data transfer completes, a TCP endpoint sends a segment with the FIN flag set. What does this flag signal? [După finalizarea transferului de date, un punct terminal TCP trimite un segment cu flagul FIN setat. Ce semnalează acest flag?]

- **a) It initiates a graceful connection close, indicating the sender has finished transmitting data [Inițiază o închidere grațioasă a conexiunii, indicând că expeditorul a terminat de transmis date]**
- **b) It abruptly terminates the connection without allowing the peer to finish sending its own data [Termină brusc conexiunea fără a permite celeilalte părți să termine de trimis propriile date]**
- **c) It requests the receiver to retransmit all unacknowledged segments from the current window [Solicită receptorului să retransmită toate segmentele neconfirmate din fereastra curentă]**
- **d) It resets the sequence numbers to zero so a new data stream can begin on the same port [Resetează numerele de secvență la zero astfel încât un nou flux de date să poată începe pe același port]**

> 💡 **Feedback:** FIN (Finish) signals graceful shutdown — the sender has no more data but the peer can still transmit. This contrasts with RST, which forces an abrupt termination without negotiation. Confusing FIN with RST is a common mistake. [FIN (Finish) semnalează oprirea grațioasă — expeditorul nu mai are date, dar cealaltă parte poate încă transmite. Aceasta contrastează cu RST, care forțează o terminare abruptă fără negociere. Confundarea FIN cu RST este o greșeală frecventă.]

---

### 5. `Multiple Choice`
**N07.C05.Q02: Debugging Advantage of REJECT / Avantajul REJECT pentru depanare**

> For an internal development server where rapid troubleshooting is the priority, which firewall action is more appropriate and why? [Pentru un server intern de dezvoltare unde depanarea rapidă este prioritatea, care acțiune de firewall este mai potrivită și de ce?]

- **a) REJECT — it provides immediate "connection refused" feedback, reducing diagnostic time from minutes to milliseconds [REJECT — oferă feedback imediat 'conexiune refuzată', reducând timpul de diagnostic de la minute la milisecunde]**
- **b) DROP — the security benefit of hiding the firewall outweighs the slower diagnosis even on internal networks [DROP — beneficiul de securitate al ascunderii paravanului de protecție depășește diagnosticul mai lent chiar și pe rețelele interne]**
- **c) Neither — internal servers should have no firewall rules at all to maximise developer productivity [Niciunul — serverele interne nu ar trebui să aibă deloc reguli de firewall pentru a maximiza productivitatea dezvoltatorilor]**
- **d) ACCEPT — the best debugging approach is to disable all filtering until the problem is resolved [ACCEPT — cea mai bună abordare de depanare este dezactivarea întregii filtrări până la rezolvarea problemei]**

> 💡 **Feedback:** On internal networks where security reconnaissance is not a concern, REJECT saves substantial diagnostic time. A developer immediately sees "Connection refused" instead of waiting through a timeout, which can take 30 seconds or more with TCP retransmissions. [Pe rețelele interne unde recunoașterea de securitate nu este o preocupare, REJECT economisește timp substanțial de diagnostic. Un dezvoltator vede imediat 'Conexiune refuzată' în loc să aștepte un timeout, care poate dura 30 de secunde sau mai mult cu retransmisiile TCP.]

---

### 6. `Multiple Choice`
**N07.T00.Q01: TCP Connection Establishment / Stabilirea conexiunii TCP**

> How many distinct packets are exchanged during a successful TCP three-way handshake? [Câte pachete distincte sunt schimbate în timpul unei negocieri TCP în trei pași reușite?]

- **a) Three (SYN, SYN-ACK, ACK) [Trei (SYN, SYN-ACK, ACK)]**
- **b) Two (SYN, ACK) [Două (SYN, ACK)]**
- **c) Four (SYN, SYN-ACK, ACK, DATA) [Patru (SYN, SYN-ACK, ACK, DATE)]**
- **d) One (combined SYN-ACK-DATA) [Unul (SYN-ACK-DATE combinat)]**

> 💡 **Feedback:** The TCP three-way handshake requires exactly 3 packets: SYN (client → server), SYN-ACK (server → client), ACK (client → server). Data transfer begins only after all three complete. [Negocierea TCP în trei pași necesită exact 3 pachete: SYN (client → server), SYN-ACK (server → client), ACK (client → server). Transferul de date începe doar după finalizarea tuturor celor trei.]

---

### 7. `Multiple Choice`
**N08.C02.Q01: Correct flag sequence during TCP handshake / Secvența corectă de fanioane la handshake-ul TCP**

> What is the correct order of TCP flags during the three-way handshake? [Care este ordinea corectă a fanioanelor TCP în timpul handshake-ului în trei pași?]

- **a) SYN → SYN-ACK → ACK, establishing bidirectional communication [SYN → SYN-ACK → ACK, stabilind comunicarea bidirecțională]**
- **b) ACK → SYN → SYN-ACK, starting with the acknowledgement phase [ACK → SYN → SYN-ACK, începând cu faza de confirmare]**
- **c) SYN → ACK → SYN-ACK, with separated synchronisation and confirmation [SYN → ACK → SYN-ACK, cu sincronizare și confirmare separate]**
- **d) SYN-ACK → SYN → ACK, with the server initiating the exchange [SYN-ACK → SYN → ACK, cu serverul inițiind schimbul]**

> 💡 **Feedback:** The client initiates with SYN, the server responds with SYN-ACK (combining its own synchronisation with acknowledgement), and the client confirms with ACK. [Clientul inițiază cu SYN, serverul răspunde cu SYN-ACK (combinând propria sincronizare cu confirmarea), iar clientul confirmă cu ACK.]

---

### 8. `Multiple Choice`
**N08.C03.Q01: HTTP line terminator sequence / Secvența de terminare a liniei HTTP**

> What character sequence terminates each line in an HTTP/1.1 message? [Ce secvență de caractere termină fiecare linie într-un mesaj HTTP/1.1?]

- **a) CRLF (\r\n) — carriage return followed by line feed as mandated by the RFC [CRLF (\r\n) — retur de car urmat de linie nouă conform specificației RFC]**
- **b) LF only (\n) — a single newline character as in Unix text files [Doar LF (\n) — un singur caracter de linie nouă ca în fișierele text Unix]**
- **c) CR only (\r) — a single carriage return as in legacy Mac systems [Doar CR (\r) — un singur retur de car ca în sistemele Mac vechi]**
- **d) Two space characters followed by a newline for alignment purposes [Două caractere spațiu urmate de o linie nouă pentru aliniere]**

> 💡 **Feedback:** HTTP/1.1 (RFC 9112) mandates CRLF line endings. The end of headers is marked by a blank line: CRLF CRLF. [HTTP/1.1 (RFC 9112) impune terminații de linie CRLF. Sfârșitul antetelor este marcat de o linie goală: CRLF CRLF.]

---

### 9. `Multiple Choice`
**N08.C03.Q02: Behaviour of HTTP HEAD method / Comportamentul metodei HTTP HEAD**

> What does an HTTP server return in response to a HEAD request? [Ce returnează un server HTTP ca răspuns la o cerere HEAD?]

- **a) The same headers that a GET request would produce, but without any response body [Aceleași antete pe care o cerere GET le-ar produce, dar fără niciun corp al răspunsului]**
- **b) Only the first 1 KB of the response body as a truncated preview of the resource [Doar primii 1 KO din corpul răspunsului ca previzualizare trunchiată a resursei]**
- **c) Metadata about the HEAD request itself, such as processing time and server load [Metadate despre cererea HEAD în sine, precum timpul de procesare și încărcarea serverului]**
- **d) A list of all HTTP methods the server supports for the requested resource [O listă a tuturor metodelor HTTP pe care serverul le acceptă pentru resursa cerută]**

> 💡 **Feedback:** HEAD is identical to GET in every way except the server MUST NOT return a body. Content-Length still reports the size a GET would produce. Useful for cache validation and link checking. [HEAD este identic cu GET în orice privință, cu excepția că serverul NU TREBUIE să returneze un corp. Content-Length raportează totuși dimensiunea pe care GET ar produce-o. Util pentru validarea cache-ului și verificarea linkurilor.]

---

### 10. `Multiple Choice`
**N08.C03.Q04: HTTP request line components / Componentele liniei de cerere HTTP**

> In the request line GET /index.html HTTP/1.1, which three components appear in order, separated by a single space? [În linia de cerere GET /index.html HTTP/1.1, care sunt cele trei componente care apar în ordine, separate de un singur spațiu?]

- **a) Method, request-target (path), and HTTP version — the three mandatory fields [Metoda, ținta cererii (calea) și versiunea HTTP — cele trei câmpuri obligatorii]**
- **b) Host, method, and request-target — with the host always appearing first [Gazda, metoda și ținta cererii — cu gazda apărând întotdeauna prima]**
- **c) HTTP version, method, and request-target — version always precedes the method [Versiunea HTTP, metoda și ținta cererii — versiunea precedă întotdeauna metoda]**
- **d) Method, HTTP version, and Content-Type — defining both action and format [Metoda, versiunea HTTP și Content-Type — definind atât acțiunea, cât și formatul]**

> 💡 **Feedback:** The request line follows METHOD SP REQUEST-TARGET SP HTTP-VERSION CRLF. For example: GET /index.html HTTP/1.1. The Host header is separate, not part of the request line. [Linia de cerere urmează schema METODA SP ȚINTA-CERERII SP VERSIUNE-HTTP CRLF. De exemplu: GET /index.html HTTP/1.1. Antetul Host este separat, nu face parte din linia de cerere.]

---

### 11. `Multiple Choice`
**N08.C03.Q05: Status code for unsupported HTTP method / Codul de stare pentru o metodă HTTP neacceptată**

> A client sends a DELETE request to an HTTP server that only implements GET and HEAD. What status code should the server return? [Un client trimite o cerere DELETE către un server HTTP care implementează doar GET și HEAD. Ce cod de stare ar trebui să returneze serverul?]

- **a) 405 Method Not Allowed — the method is recognised but not supported for this resource [405 Method Not Allowed — metoda este recunoscută, dar nu este acceptată pentru această resursă]**
- **b) 400 Bad Request — the server cannot understand what the client is asking [400 Bad Request — serverul nu poate înțelege ce cere clientul]**
- **c) 404 Not Found — the DELETE endpoint does not exist on this server [404 Not Found — endpoint-ul DELETE nu există pe acest server]**
- **d) 501 Not Implemented — the server does not recognise the DELETE method at all, and the server logs the attempt as a protocol violation before closing the connection [501 Not Implemented — serverul nu recunoaște deloc metoda DELETE, iar serverul înregistrează încercarea ca o violare de protocol înainte de a închide conexiunea]**

> 💡 **Feedback:** 405 indicates the server knows the method but the target resource does not support it. The response SHOULD include an Allow header listing accepted methods (e.g., Allow: GET, HEAD). [405 indică faptul că serverul cunoaște metoda, dar resursa țintă nu o acceptă. Răspunsul AR TREBUI să includă un antet Allow care listează metodele acceptate (de ex., Allow: GET, HEAD).]

---

### 12. `True / False`
**N08.C04.Q01: HTTP/1.1 connections are persistent by default / Conexiunile HTTP/1.1 sunt persistente implicit**

> HTTP/1.1 uses persistent connections (keep-alive) by default, meaning multiple request-response pairs can share a single TCP connection without re-handshaking. [HTTP/1.1 utilizează conexiuni persistente (keep-alive) implicit, ceea ce înseamnă că mai multe perechi cerere-răspuns pot partaja o singură conexiune TCP fără re-handshake.]

- **a) true**
- **b) false**

> 💡 **Feedback:** HTTP/1.0 opened a new TCP connection per request. HTTP/1.1 changed the default to persistent connections, significantly reducing handshake overhead. [HTTP/1.0 deschidea o nouă conexiune TCP per cerere. HTTP/1.1 a schimbat implicit la conexiuni persistente, reducând semnificativ overhead-ul de handshake.]

---

### 13. `Multiple Choice`
**N08.C04.Q02: Request serialisation in HTTP/1.1 keep-alive / Serializarea cererilor în HTTP/1.1 keep-alive**

> A browser fetches an HTML page with 5 images from an HTTP/1.1 server using keep-alive. How does connection reuse work? [Un browser preia o pagină HTML cu 5 imagini de la un server HTTP/1.1 folosind keep-alive. Cum funcționează reutilizarea conexiunii?]

- **a) One or more persistent TCP connections carry serialised requests, avoiding repeated handshakes [Una sau mai multe conexiuni TCP persistente transportă cereri serializate, evitând handshake-uri repetate]**
- **b) Six separate TCP connections are established, one per resource, each with its own handshake [Șase conexiuni TCP separate sunt stabilite, una per resursă, fiecare cu propriul handshake]**
- **c) All six requests are multiplexed concurrently on a single TCP connection using HTTP/1.1 streams [Toate cele șase cereri sunt multiplexate concurent pe o singură conexiune TCP folosind fluxuri HTTP/1.1]**
- **d) The connection closes after the HTML response; new connections open for each image separately [Conexiunea se închide după răspunsul HTML; conexiuni noi se deschid pentru fiecare imagine separat]**

> 💡 **Feedback:** HTTP/1.1 keep-alive reuses connections but serialises requests per connection. Browsers open 6–8 parallel persistent connections to achieve some concurrency. True multiplexing is HTTP/2. [HTTP/1.1 keep-alive reutilizează conexiunile, dar serializează cererile per conexiune. Browserele deschid 6–8 conexiuni persistente paralele. Multiplexarea reală este o caracteristică HTTP/2.]

---

### 14. `Multiple Choice`
**N08.C04.Q03: HTTP/2 improvement over HTTP/1.1 pipelining / Îmbunătățirea HTTP/2 față de pipelining-ul HTTP/1.1**

> What problem does HTTP/2 multiplexing solve that HTTP/1.1 persistent connections cannot? [Ce problemă rezolvă multiplexarea HTTP/2 pe care conexiunile persistente HTTP/1.1 nu o pot rezolva?]

- **a) Head-of-line blocking — HTTP/2 interleaves multiple streams on one connection without waiting [Blocajul head-of-line — HTTP/2 intercalează mai multe fluxuri pe o conexiune fără a aștepta]**
- **b) Packet loss — HTTP/2 eliminates TCP retransmissions through application-level recovery [Pierderea pachetelor — HTTP/2 elimină retransmisiile TCP prin recuperare la nivel de aplicație]**
- **c) DNS latency — HTTP/2 resolves domain names faster by bundling lookups with requests [Latența DNS — HTTP/2 rezolvă numele de domenii mai rapid combinând căutările cu cererile]**
- **d) Encryption overhead — HTTP/2 removes the need for TLS by using built-in encryption [Overhead-ul de criptare — HTTP/2 elimină necesitatea TLS folosind criptare încorporată]**

> 💡 **Feedback:** HTTP/1.1 serialises requests per connection. HTTP/2 multiplexes concurrent streams on one connection. However, TCP-level head-of-line blocking persists, which HTTP/3 (QUIC) addresses. [HTTP/1.1 serializează cererile per conexiune. HTTP/2 multiplexează fluxuri concurente pe o conexiune. Cu toate acestea, blocajul head-of-line la nivel TCP persistă, pe care HTTP/3 (QUIC) îl adresează.]

---

### 15. `Multiple Choice`
**N08.C04.Q04: HTTP/3 transport protocol / Protocolul de transport al HTTP/3**

> HTTP/3 replaces TCP with a different transport protocol. Which protocol does HTTP/3 use? [HTTP/3 înlocuiește TCP cu un protocol de transport diferit. Ce protocol folosește HTTP/3?]

- **a) QUIC — a UDP-based protocol providing native stream multiplexing and reduced latency [QUIC — un protocol bazat pe UDP care oferă multiplexare nativă a fluxurilor și latență redusă]**
- **b) SCTP — a multi-homing protocol designed for telephony signalling networks [SCTP — un protocol multi-homing proiectat pentru rețele de semnalizare telefonică]**
- **c) Raw UDP — HTTP/3 sends messages directly as UDP datagrams without any reliability layer [UDP brut — HTTP/3 trimite mesaje direct ca datagrame UDP fără niciun strat de fiabilitate]**
- **d) DCCP — a congestion-controlled protocol for real-time multimedia streaming [DCCP — un protocol cu control al congestiei pentru streaming multimedia în timp real]**

> 💡 **Feedback:** QUIC (RFC 9000) runs over UDP, providing TLS 1.3 encryption by default, independent streams (no head-of-line blocking), and faster connection establishment (0-RTT or 1-RTT). [QUIC (RFC 9000) rulează peste UDP, oferind criptare TLS 1.3 implicit, fluxuri independente (fără blocaj head-of-line) și stabilire mai rapidă a conexiunii (0-RTT sau 1-RTT).]

---

### 16. `Multiple Choice`
**N08.C04.Q05: Header indicating HTTP body length / Antetul care indică lungimea corpului HTTP**

> Which HTTP header tells the receiver exactly how many bytes to read for the message body? [Ce antet HTTP spune receptorului exact câți octeți să citească pentru corpul mesajului?]

- **a) Content-Length — specifies the body size in bytes as a decimal integer [Content-Length — specifică dimensiunea corpului în octeți ca un întreg zecimal]**
- **b) Content-Type — describes the MIME type of the body, not its size in bytes [Content-Type — descrie tipul MIME al corpului, nu dimensiunea sa în octeți]**
- **c) Transfer-Encoding — specifies how the body is encoded, not its total length [Transfer-Encoding — specifică cum este codificat corpul, nu lungimea sa totală]**
- **d) Host — identifies the target server hostname, unrelated to body measurements [Host — identifică numele gazdei serverului țintă, fără legătură cu dimensiunile corpului]**

> 💡 **Feedback:** Content-Length: N tells the receiver to read exactly N bytes after the blank line. Without it, chunked transfer encoding or connection close signals the end of body. [Content-Length: N indică receptorului să citească exact N octeți după linia goală. Fără acesta, codificarea de transfer fragmentată sau închiderea conexiunii semnalează sfârșitul corpului.]

---

### 17. `Multiple Choice`
**N08.C05.Q01: Distinguishing reverse proxy from forward proxy / Distincția dintre reverse proxy și forward proxy**

> What is the primary architectural difference between a forward proxy and a reverse proxy? [Care este diferența arhitecturală principală dintre un forward proxy și un reverse proxy?]

- **a) A forward proxy acts on behalf of clients (who configure it); a reverse proxy acts on behalf of servers (transparent to clients) [Un forward proxy acționează în numele clienților (care îl configurează); un reverse proxy acționează în numele serverelor (transparent pentru clienți)]**
- **b) A forward proxy uses HTTPS while a reverse proxy only supports unencrypted HTTP traffic [Un forward proxy folosește HTTPS, iar un reverse proxy suportă doar trafic HTTP necriptat]**
- **c) A forward proxy operates at Layer 3 while a reverse proxy operates at Layer 7 exclusively [Un forward proxy operează la stratul 3, iar un reverse proxy operează exclusiv la stratul 7]**
- **d) There is no functional difference; the terms describe the same proxy deployed in different locations — both intercept traffic identically at the transport layer [Nu există nicio diferență funcțională; termenii descriu același proxy implementat în locații diferite — ambele interceptează traficul identic la stratul de transport]**

> 💡 **Feedback:** Forward proxy: client-configured, hides client from server (corporate firewalls). Reverse proxy: server-deployed, hides servers from client (nginx in front of backends). [Forward proxy: configurat de client, ascunde clientul de server (firewall-uri corporative). Reverse proxy: implementat de server, ascunde serverele de client (nginx în fața backend-urilor).]

---

### 18. `Multiple Choice`
**N08.C05.Q03: Purpose of X-Forwarded-For in proxy architecture / Rolul X-Forwarded-For în arhitectura proxy**

> What is the purpose of the X-Forwarded-For header when a reverse proxy forwards a request to a backend? [Care este scopul antetului X-Forwarded-For când un reverse proxy redirecționează o cerere către un backend?]

- **a) It preserves the original client IP address, since the backend only sees the proxy's IP in the TCP connection [Conservă adresa IP originală a clientului, deoarece backend-ul vede doar IP-ul proxy-ului în conexiunea TCP]**
- **b) It specifies which backend server the proxy selected for load-balancing purposes [Specifică ce server backend a selectat proxy-ul în scopuri de echilibrare a încărcăturii]**
- **c) It encrypts the client's IP address for privacy before transmitting to the backend using the TLS session key [Criptează adresa IP a clientului pentru confidențialitate înainte de transmiterea către backend folosind cheia de sesiune TLS]**
- **d) It tells the backend server which port the client is using for the response path [Indică serverului backend ce port folosește clientul pentru calea de răspuns]**

> 💡 **Feedback:** The proxy terminates the client's TCP connection and opens a new one to the backend. Without X-Forwarded-For, the backend only sees the proxy's address as the source. [Proxy-ul termină conexiunea TCP a clientului și deschide una nouă către backend. Fără X-Forwarded-For, backend-ul vede doar adresa proxy-ului ca sursă.]

---

### 19. `Multiple Choice`
**N08.T00.Q01: TCP handshake purpose and rationale / Scopul și rațiunea handshake-ului TCP**

> A student claims the three-way handshake is unnecessary because the first SYN already proves the client wants to connect. Why does TCP require all three steps? [Un student susține că handshake-ul în trei pași este inutil deoarece primul SYN dovedește deja că clientul dorește să se conecteze. De ce necesită TCP toți cei trei pași?]

- **a) Both directions must be proven functional — SYN tests client-to-server, SYN-ACK tests server-to-client, and ACK confirms both paths work [Ambele direcții trebuie dovedite funcționale — SYN testează client-la-server, SYN-ACK testează server-la-client, iar ACK confirmă funcționarea ambelor căi]**
- **b) The three steps are needed to negotiate encryption keys before any application data can be transmitted securely [Cei trei pași sunt necesari pentru a negocia cheile de criptare înainte ca datele aplicației să poată fi transmise în siguranță]**
- **c) Each step assigns a different port number to the connection, requiring three messages to set up source and destination ports before data transfer begins [Fiecare pas atribuie un număr de port diferit conexiunii, necesitând trei mesaje pentru a configura porturile sursă și destinație înainte ca transferul de date să înceapă]**
- **d) The operating system requires three distinct system calls to transition the socket from CLOSED to ESTABLISHED state [Sistemul de operare necesită trei apeluri de sistem distincte pentru a tranziționa socket-ul din starea CLOSED în ESTABLISHED]**

> 💡 **Feedback:** The handshake proves bidirectional capability: SYN (C->S reachable), SYN-ACK (S->C reachable, S agrees), ACK (C confirms S->C path). Without the third step, server stays in SYN_RCVD. [Handshake-ul dovedește capacitatea bidirecțională: SYN (C->S accesibil), SYN-ACK (S->C accesibil, S acceptă), ACK (C confirmă calea S->C). Fără al treilea pas, serverul rămâne în SYN_RCVD.]

---

### 20. `Multiple Choice`
**N08.T00.Q07: HTTP/2 multiplexing advantage / Avantajul multiplexării HTTP/2**

> HTTP/1.1 processes requests sequentially on each connection, causing head-of-line blocking. How does HTTP/2 solve this specific problem? [HTTP/1.1 procesează cererile secvențial pe fiecare conexiune, cauzând blocarea capului de linie. Cum rezolvă HTTP/2 această problemă specifică?]

- **a) HTTP/2 multiplexes multiple request-response streams over a single TCP connection, so one slow response does not block others [HTTP/2 multiplexează mai multe fluxuri cerere-răspuns pe o singură conexiune TCP, astfel încât un răspuns lent nu le blochează pe celelalte]**
- **b) HTTP/2 opens 20 parallel TCP connections per server instead of the 6-8 used by HTTP/1.1 browsers [HTTP/2 deschide 20 de conexiuni TCP paralele per server în loc de 6-8 folosite de browserele HTTP/1.1]**
- **c) HTTP/2 compresses the entire response body to zero bytes, eliminating transfer time entirely [HTTP/2 comprimă întregul corp al răspunsului la zero octeți, eliminând complet timpul de transfer]**
- **d) HTTP/2 replaces TCP with UDP at the transport layer to avoid connection-oriented overhead completely, relying on application-level acknowledgements [HTTP/2 înlocuiește TCP cu UDP la stratul de transport pentru a evita complet suprasarcina orientată pe conexiune, bazându-se pe confirmări la nivel de aplicație]**

> 💡 **Feedback:** HTTP/2 uses stream multiplexing: multiple logical streams share one TCP connection. Each stream is independent, so a slow resource does not delay others. HTTP/3 goes further with QUIC over UDP. [HTTP/2 folosește multiplexarea fluxurilor: mai multe fluxuri logice partajează o singură conexiune TCP. Fiecare flux este independent, deci o resursă lentă nu le întârzie pe celelalte. HTTP/3 merge mai departe cu QUIC peste UDP.]

---

### 21. `Multiple Choice`
**N08.T00.Q09: Content-Length header necessity / Necesitatea antetului Content-Length**

> In the exercise HTTP server, the Content-Length header is included in every response. A student asks: why not let the client just read until the connection closes? [În serverul HTTP din exercițiu, antetul Content-Length este inclus în fiecare răspuns. Un student întreabă: de ce să nu lăsăm clientul să citească până când conexiunea se închide?]

- **a) Persistent connections keep the socket open for multiple requests — without Content-Length, the client cannot determine where one response ends and the next begins [Conexiunile persistente păstrează socket-ul deschis pentru cereri multiple — fără Content-Length, clientul nu poate determina unde se termină un răspuns și unde începe următorul]**
- **b) Content-Length triggers gzip compression in the browser, which is disabled when the header is absent from the response [Content-Length declanșează compresia gzip în browser, care este dezactivată când antetul lipsește din răspuns]**
- **c) The HTTP specification requires Content-Length on every response — omitting it causes a 400 Bad Request error at the client, and proxies along the chain will strip the body if this header is missing [Specificația HTTP necesită Content-Length la fiecare răspuns — omiterea cauzează o eroare 400 Bad Request la client, iar proxy-urile din lanț vor elimina corpul dacă acest antet lipsește]**
- **d) Without Content-Length, the TCP checksum cannot verify the integrity of the response body bytes [Fără Content-Length, suma de control TCP nu poate verifica integritatea octeților corpului răspunsului]**

> 💡 **Feedback:** HTTP/1.1 defaults to persistent connections. The client reuses the same TCP socket for multiple request-response cycles. Content-Length tells the client exactly how many body bytes to read before the next response. [HTTP/1.1 folosește implicit conexiuni persistente. Clientul reutilizează același socket TCP pentru cicluri multiple cerere-răspuns. Content-Length spune clientului exact câți octeți de corp să citească înainte de răspunsul următor.]

---

### 22. `Multiple Choice`
**N08.C01.Q03: OS demultiplexing of incoming datagrams / Demultiplexarea datagramelor de către sistemul de operare**

> When a UDP datagram arrives with destination port 53, how does the operating system determine which process should receive it? [Când o datagramă UDP ajunge cu portul destinație 53, cum determină sistemul de operare ce proces ar trebui să o primească?]

- **a) It consults an internal kernel table mapping port numbers to sockets [Consultă o tabelă internă a nucleului care asociază numerele de port cu socket-urile]**
- **b) It reads the process ID embedded in the UDP header fields [Citește identificatorul procesului încorporat în câmpurile antetului UDP]**
- **c) It broadcasts the datagram to all running application processes [Difuzează datagrama tuturor proceselor aplicație în execuție]**
- **d) It uses the source IP address to identify the destination process rather than the port number [Utilizează adresa IP sursă pentru a identifica procesul destinație în loc de numărul de port]**

> 💡 **Feedback:** The kernel maintains a socket table mapping ports to processes. No PID exists in transport headers. This is why binding two processes to the same port triggers "Address already in use". [Nucleul menține o tabelă de socket-uri ce asociază porturile cu procesele. Niciun PID nu există în antetele de transport. De aceea legarea a două procese la același port declanșează eroarea 'Address already in use'.]

---

### 23. `Multiple Choice`
**N08.C02.Q02: Rationale for three messages in connection setup / Justificarea celor trei mesaje la stabilirea conexiunii**

> Why does TCP require exactly three packets for connection establishment rather than two? [De ce TCP necesită exact trei pachete pentru stabilirea conexiunii și nu două?]

- **a) Both endpoints must confirm they can send AND receive, proving bidirectional capability [Ambele endpoint-uri trebuie să confirme că pot trimite ȘI primi, dovedind capacitatea bidirecțională]**
- **b) Two packets would suffice, but the third reduces latency by piggybacking initial data [Două pachete ar fi suficiente, dar al treilea reduce latența transportând date inițiale]**
- **c) The third packet carries the first application data payload as an optimisation [Al treilea pachet transportă primul payload de date ale aplicației ca optimizare]**
- **d) Four packets would be needed for full reliability, but TCP trades reliability for speed [Patru pachete ar fi necesare pentru fiabilitate completă, dar TCP sacrifică fiabilitatea pentru viteză]**

> 💡 **Feedback:** SYN proves the client can send. SYN-ACK proves the server can send and receive. ACK proves the client can receive. Two messages would only confirm one direction of communication. [SYN dovedește că clientul poate trimite. SYN-ACK dovedește că serverul poate trimite și primi. ACK dovedește că clientul poate primi. Două mesaje ar confirma doar o direcție de comunicare.]

---

### 24. `Multiple Choice`
**N08.C02.Q04: Server state without receiving third ACK / Starea serverului fără primirea celui de-al treilea ACK**

> If a client sends SYN and receives SYN-ACK but never sends the third ACK, what state does the server remain in? [Dacă un client trimite SYN și primește SYN-ACK, dar nu trimite niciodată al treilea ACK, în ce stare rămâne serverul?]

- **a) SYN_RCVD — the server waits for the final ACK and eventually times out [SYN_RCVD — serverul așteaptă ACK-ul final și în cele din urmă expiră]**
- **b) ESTABLISHED — the server proceeds as soon as it sends SYN-ACK [ESTABLISHED — serverul continuă de îndată ce trimite SYN-ACK]**
- **c) LISTEN — the server returns to passive state after detecting the failure [LISTEN — serverul revine la starea pasivă după detectarea eșecului]**
- **d) CLOSED — the server immediately closes because the handshake was incomplete [CLOSED — serverul se închide imediat deoarece handshake-ul a fost incomplet]**

> 💡 **Feedback:** Without the third ACK, the server's half-open connection remains in SYN_RCVD. This is exploited in SYN flood attacks, where many half-open connections exhaust server resources. [Fără al treilea ACK, conexiunea semi-deschisă a serverului rămâne în SYN_RCVD. Aceasta este exploatată în atacurile SYN flood, unde multe conexiuni semi-deschise epuizează resursele serverului.]

---

### 25. `Multiple Choice`
**N08.C06.Q05: Token bucket rate limiting parameters / Parametrii limitării ratei cu token bucket**

> A token bucket rate limiter has capacity 10 tokens and refill rate 1 token/second. If 15 requests arrive simultaneously, what happens? [Un limitator de rată token bucket are capacitatea de 10 jetoane și rata de reumplere de 1 jeton/secundă. Dacă 15 cereri sosesc simultan, ce se întâmplă?]

- **a) 10 requests are processed immediately; 5 requests receive 429 Too Many Requests and must retry later [10 cereri sunt procesate imediat; 5 cereri primesc 429 Too Many Requests și trebuie să reîncerce mai târziu]**
- **b) All 15 requests are queued and processed at the rate of 1 per second over 15 seconds total without any drops [Toate cele 15 cereri sunt puse în coadă și procesate cu rata de 1 pe secundă pe parcursul a 15 secunde fără nicio eliminare]**
- **c) All 15 requests are dropped because the burst exceeds the bucket capacity entirely [Toate cele 15 cereri sunt aruncate deoarece rafala depășește complet capacitatea găleții]**
- **d) 15 requests are processed immediately because the bucket borrows from future token allocations [15 cereri sunt procesate imediat deoarece galeata împrumută din alocările viitoare de jetoane]**

> 💡 **Feedback:** The bucket starts full with 10 tokens. The first 10 requests each consume one token and succeed. The remaining 5 find an empty bucket and are rejected with 429. [Galeata începe plină cu 10 jetoane. Primele 10 cereri consumă câte un jeton și reușesc. Celelalte 5 găsesc galeata goală și sunt respinse cu 429.]

---

### 26. `Multiple Choice`
**N08.T00.Q06: SYN flood attack mechanism / Mecanismul atacului SYN flood**

> An attacker sends thousands of SYN packets to a server but never completes any handshake with the final ACK. What resource does this exhaust on the server? [Un atacator trimite mii de pachete SYN către un server dar nu completează niciodată vreun handshake cu ACK-ul final. Ce resursă epuizează aceasta pe server?]

- **a) The server's half-open connection table — each SYN creates a SYN_RCVD entry that consumes memory until it times out [Tabela de conexiuni pe jumătate deschise a serverului — fiecare SYN creează o intrare SYN_RCVD care consumă memorie până la expirare]**
- **b) The server's disk space — each SYN packet is logged to a file that grows until the filesystem is full and swap partition [Spațiul pe disc al serverului — fiecare pachet SYN este înregistrat într-un fișier care crește până se umple sistemul de fișiere și partiția de swap]**
- **c) The network bandwidth — SYN packets are extremely large and saturate the physical link capacity [Lățimea de bandă a rețelei — pachetele SYN sunt extrem de mari și saturează capacitatea legăturii fizice]**
- **d) The server's CPU — computing the checksum for each SYN requires intensive cryptographic operations [CPU-ul serverului — calcularea sumei de control pentru fiecare SYN necesită operații criptografice intensive]**

> 💡 **Feedback:** SYN flood fills the server's half-open connection table. Each unanswered SYN leaves the server in SYN_RCVD state, consuming memory. SYN cookies are a mitigation. [Inundația SYN umple tabela de conexiuni pe jumătate deschise a serverului. Fiecare SYN fără răspuns lasă serverul în starea SYN_RCVD, consumând memorie. Cookie-urile SYN sunt o atenuare.]

---


## W08 — Laborator / Lab   (9 questions)

### 27. `Multiple Choice`
**N01.S05.Q06: Python Built-in HTTP Server / Serverul HTTP încorporat Python**

> What command starts Python's built-in HTTP server on port 8000? [Ce comandă pornește serverul HTTP încorporat din Python pe portul 8000?]

- **a) python -m http.server 8000 (uses the built-in module to serve the current directory on port 8000) [python -m http.server 8000 (modulul încorporat pe portul 8000)]**
- **b) python -c 'import http; http.serve(8000)' (this is not valid Python syntax) [python -c 'import http; http.serve(8000)' (aceasta nu este sintaxă Python validă)]**
- **c) python3 httpd.py --port 8000 (there is no standard httpd.py script) [python3 httpd.py --port 8000 (nu există un script standard httpd.py)]**

> 💡 **Feedback:** The python -m http.server 8000 command starts a simple HTTP server serving files from the current directory on port 8000. The --directory flag can specify a different directory. [Comanda python -m http.server 8000 pornește un server HTTP simplu care servește fișiere din directorul curent pe portul 8000. Steagul --directory poate specifica un alt director.]

---

### 28. `Multiple Choice`
**N08.S01.Q02: Purpose of SO_REUSEADDR socket option / Scopul opțiunii de socket SO_REUSEADDR**

> Why is server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) called before bind() in the lab exercise? [De ce se apelează server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) înainte de bind() în exercițiul de laborator?]

- **a) It allows the server to reuse the port immediately after restart, preventing 'Address already in use' errors [Permite serverului să reutilizeze portul imediat după repornire, prevenind erorile 'Address already in use']**
- **b) It enables multiple processes to bind to the same port simultaneously for load distribution [Permite mai multor procese să se lege la același port simultan pentru distribuirea sarcinii]**
- **c) It increases the socket buffer size to handle higher throughput from concurrent clients connecting simultaneously [Mărește dimensiunea buffer-ului socket-ului pentru a gestiona un debit mai mare de la clienți concurenți care se conectează simultan]**
- **d) It forces the socket to use IPv4 exclusively, preventing conflicts with IPv6 bindings [Forțează socket-ul să folosească exclusiv IPv4, prevenind conflicte cu legăturile IPv6]**

> 💡 **Feedback:** After a server closes, its port may linger in TIME_WAIT state for up to 2×MSL. SO_REUSEADDR lets a new server bind to that port immediately, which is essential during development. [După închiderea unui server, portul său poate persista în starea TIME_WAIT până la 2×MSL. SO_REUSEADDR permite unui nou server să se lege la acel port imediat, ceea ce este esențial în dezvoltare.]

---

### 29. `Multiple Choice`
**N08.S01.Q05: TCP server lifecycle order in Python / Ordinea ciclului de viață al serverului TCP în Python**

> What is the correct order of socket calls to create a TCP server? [Care este ordinea corectă a apelurilor socket pentru a crea un server TCP?]

- **a) socket() → setsockopt() → bind() → listen() → accept() — options must precede bind [socket() → setsockopt() → bind() → listen() → accept() — opțiunile trebuie să preceadă bind]**
- **b) socket() → bind() → setsockopt() → listen() → accept() — options can follow bind [socket() → bind() → setsockopt() → listen() → accept() — opțiunile pot urma bind]**
- **c) socket() → listen() → bind() → accept() → setsockopt() — listen before bind [socket() → listen() → bind() → accept() → setsockopt() — listen înainte de bind]**
- **d) socket() → connect() → bind() → listen() → accept() — connect initialises the server [socket() → connect() → bind() → listen() → accept() — connect inițializează serverul]**

> 💡 **Feedback:** SO_REUSEADDR must be set before bind() to take effect. connect() is for clients, not servers. The sequence matches the Parsons problem P1 from the lab materials. [SO_REUSEADDR trebuie setat înainte de bind() pentru a avea efect. connect() este pentru clienți, nu pentru servere. Secvența corespunde problemei Parsons P1 din materialele de laborator.]

---

### 30. `Multiple Choice`
**N08.S02.Q03: HEAD vs GET response difference in implementation / Diferența răspunsului HEAD vs GET în implementare**

> In the exercise HTTP server, how does a HEAD response differ from a GET response for the same resource? [În serverul HTTP al exercițiului, cum diferă un răspuns HEAD de un răspuns GET pentru aceeași resursă?]

- **a) Headers are identical (including Content-Length for the full body size), but the response body is empty [Antetele sunt identice (inclusiv Content-Length pentru dimensiunea completă a corpului), dar corpul răspunsului este gol]**
- **b) The server returns only the Content-Type header and excludes Content-Length entirely, as the specification mandates fewer headers for HEAD [Serverul returnează doar antetul Content-Type și exclude complet Content-Length, deoarece specificația impune mai puține antete pentru HEAD]**
- **c) Both the headers and body are identical, with HEAD being merely an alias for GET [Atât antetele cât și corpul sunt identice, HEAD fiind doar un alias pentru GET]**
- **d) The server omits all headers and returns only the status line for HEAD requests [Serverul omite toate antetele și returnează doar linia de stare pentru cererile HEAD]**

> 💡 **Feedback:** The exercise code computes headers including Content-Length from the file, then sets response_body = b'' for HEAD. This matches RFC 9110 which requires identical headers but no body. [Codul exercițiului calculează antetele inclusiv Content-Length din fișier, apoi setează response_body = b'' pentru HEAD. Aceasta respectă RFC 9110 care necesită antete identice dar fără corp.]

---

### 31. `Multiple Choice`
**N08.S02.Q05: Blank line separating headers from body / Linia goală care separă antetele de corp**

> In the response building code, what marks the boundary between HTTP headers and the response body? [În codul de construire a răspunsului, ce marchează granița dintre antetele HTTP și corpul răspunsului?]

- **a) An empty line (\r\n\r\n) — a CRLF immediately following the last header's CRLF [O linie goală (\r\n\r\n) — un CRLF imediat după CRLF-ul ultimului antet]**
- **b) A Content-Length header — the parser switches to body mode after reading it [Un antet Content-Length — parser-ul trece în modul corp după ce îl citește]**
- **c) A NULL byte (0x00) — signalling the end of text-based header content [Un octet NULL (0x00) — semnalând sfârșitul conținutului text al antetelor]**
- **d) The string END-HEADERS — an explicit delimiter defined in the HTTP specification [Șirul END-HEADERS — un delimitator explicit definit în specificația HTTP]**

> 💡 **Feedback:** The blank line (CRLF after headers + one more CRLF) is the only way HTTP/1.1 delineates headers from body. The exercise code appends '\r\n' after the last header line. [Linia goală (CRLF după antete + încă un CRLF) este singura modalitate prin care HTTP/1.1 delimitează antetele de corp. Codul exercițiului adaugă '\r\n' după ultima linie de antet.]

---

### 32. `Multiple Choice`
**N08.S03.Q03: X-Forwarded-For header chain construction / Construcția lanțului antetului X-Forwarded-For**

> If a request already has X-Forwarded-For: 10.0.0.1 and the proxy adds the current client IP 192.168.1.100, what is the resulting header value? [Dacă o cerere are deja X-Forwarded-For: 10.0.0.1 și proxy-ul adaugă IP-ul clientului curent 192.168.1.100, care este valoarea antetului rezultat?]

- **a) 10.0.0.1, 192.168.1.100 — the new IP is appended to the existing chain with a comma separator [10.0.0.1, 192.168.1.100 — noul IP este adăugat la lanțul existent cu un separator virgulă]**
- **b) 192.168.1.100 — the proxy replaces the existing header entirely with only the latest IP [192.168.1.100 — proxy-ul înlocuiește antetul existent complet doar cu ultimul IP]**
- **c) 10.0.0.1 — the original value is preserved unchanged because the header already exists in the request [10.0.0.1 — valoarea originală este păstrată neschimbată deoarece antetul există deja în cerere]**
- **d) 192.168.1.100, 10.0.0.1 — the new IP is prepended before the existing addresses [192.168.1.100, 10.0.0.1 — noul IP este adăugat înainte de adresele existente]**

> 💡 **Feedback:** X-Forwarded-For forms an ordered chain. Each proxy appends the client IP it received from. The rightmost IP is the most recently added (and most trusted if you control that proxy). [X-Forwarded-For formează un lanț ordonat. Fiecare proxy adaugă IP-ul clientului de la care a primit. IP-ul cel mai din dreapta este cel mai recent adăugat (și cel mai de încredere dacă controlezi acel proxy).]

---

### 33. `Multiple Choice`
**N08.S04.Q05: Wireshark filter for HTTP error responses / Filtrul Wireshark pentru răspunsuri HTTP de eroare**

> Which Wireshark display filter shows only HTTP responses with status codes indicating errors (4xx and 5xx)? [Ce filtru de afișare Wireshark arată doar răspunsurile HTTP cu coduri de stare care indică erori (4xx și 5xx)?]

- **a) http.response.code >= 400 — matching all client errors (4xx) and server errors (5xx) [http.response.code >= 400 — potrivind toate erorile client (4xx) și erorile server (5xx)]**
- **b) http.response.code == 404 — only matching the specific Not Found status, missing all other errors [http.response.code == 404 — potrivind doar starea specifică Not Found, omițând toate celelalte erori]**
- **c) http.error — not a valid Wireshark display filter field name for HTTP responses [http.error — nu este un nume valid de câmp de filtru de afișare Wireshark pentru răspunsuri HTTP]**
- **d) http.response == error — invalid filter syntax that does not match Wireshark's grammar [http.response == error — sintaxă de filtru invalidă care nu corespunde gramaticii Wireshark]**

> 💡 **Feedback:** Status codes 400-599 cover all error categories. The >= operator efficiently captures the entire range without listing individual codes. [Codurile de stare 400-599 acoperă toate categoriile de erori. Operatorul >= capturează eficient întregul interval fără a lista coduri individuale.]

---

### 34. `Multiple Choice`
**N08.S04.Q01: Wireshark filter for pure SYN packets only / Filtrul Wireshark doar pentru pachete SYN pure**

> Which Wireshark display filter shows TCP SYN packets but excludes SYN-ACK packets? [Ce filtru de afișare Wireshark arată pachetele TCP SYN, dar exclude pachetele SYN-ACK?]

- **a) tcp.flags.syn == 1 && tcp.flags.ack == 0 — SYN set, ACK clear [tcp.flags.syn == 1 && tcp.flags.ack == 0 — SYN setat, ACK neselectat]**
- **b) tcp.flags.syn == 1 — this also matches SYN-ACK because both have SYN set [tcp.flags.syn == 1 — aceasta potrivește și SYN-ACK deoarece ambele au SYN setat]**
- **c) tcp contains SYN — an invalid Wireshark filter syntax that produces an error [tcp contains SYN — o sintaxă de filtru Wireshark invalidă care produce o eroare]**
- **d) tcp.syn — a boolean shorthand that is not a valid Wireshark display filter expression [tcp.syn — o prescurtare booleană care nu este o expresie validă de filtru de afișare Wireshark]**

> 💡 **Feedback:** SYN-ACK packets have both SYN=1 and ACK=1. To isolate pure SYN (connection initiation), you must also require ACK=0. [Pachetele SYN-ACK au atât SYN=1 cât și ACK=1. Pentru a izola SYN pur (inițierea conexiunii), trebuie să cereți și ACK=0.]

---

### 35. `Multiple Choice`
**N08.S01.Q01: Socket type for TCP server in Python / Tipul de socket pentru un server TCP în Python**

> Which socket constant creates a TCP socket in Python? [Ce constantă socket creează un socket TCP în Python?]

- **a) socket.SOCK_STREAM — the stream-oriented type used by TCP for reliable byte delivery [socket.SOCK_STREAM — tipul orientat pe flux utilizat de TCP pentru livrare fiabilă de octeți]**
- **b) socket.SOCK_DGRAM — the datagram type used by UDP for connectionless communication [socket.SOCK_DGRAM — tipul datagramă utilizat de UDP pentru comunicare fără conexiune]**
- **c) socket.SOCK_RAW — providing direct access to lower-level protocols below transport [socket.SOCK_RAW — oferind acces direct la protocoalele de nivel inferior sub transport]**
- **d) socket.SOCK_TCP — a named constant explicitly referencing the TCP protocol [socket.SOCK_TCP — o constantă numită referind explicit protocolul TCP]**

> 💡 **Feedback:** SOCK_STREAM maps to TCP (reliable, ordered byte stream). SOCK_DGRAM maps to UDP (unreliable datagrams). SOCK_TCP does not exist in Python's socket module. [SOCK_STREAM corespunde TCP (flux de octeți fiabil, ordonat). SOCK_DGRAM corespunde UDP (datagrame nefiabile). SOCK_TCP nu există în modulul socket al Python.]

---


## W08 — Numerical   (8 questions)

### 36. `Numerical`
**N08.D03.Q07: ACK number in TCP handshake / Numărul ACK în handshake-ul TCP**

> During a TCP three-way handshake, the client sends SYN with sequence number 1000. The server replies SYN-ACK with its own sequence number 5000 and acknowledges the client. What acknowledgement number does the server place in the SYN-ACK segment? [În timpul unui handshake TCP în trei pași, clientul trimite SYN cu numărul de secvență 1000. Serverul răspunde cu SYN-ACK cu propriul număr de secvență 5000 și confirmă clientul. Ce număr de confirmare plasează serverul în segmentul SYN-ACK?]


> 💡 **Feedback:** The ACK number = peer's sequence number + 1. The client sent seq=1000, so the server acknowledges with ack=(...). [Numărul ACK = numărul de secvență al partenerului + 1. Clientul a trimis seq=1000, deci serverul confirmă cu ack=(...).]

---

### 37. `Calculated`
**N08.D04.Q06: HTTP response total bytes / Numărul total de octeți al răspunsului HTTP**

> An HTTP response consists of a status line of {status_len} bytes, headers totalling {header_len} bytes, a blank line separator of 2 bytes (CRLF), and a body of {body_len} bytes. Each header line already includes its trailing CRLF, and the status line includes its trailing CRLF. What is the total response size in bytes? [Un răspuns HTTP constă dintr-o linie de stare de {status_len} octeți, antete cu un total de {header_len} octeți, un separator de linie goală de 2 octeți (CRLF) și un corp de {body_len} octeți. Fiecare linie de antet include deja CRLF-ul final, iar linia de stare include CRLF-ul final. Care este dimensiunea totală a răspunsului în octeți?]


> 💡 **Feedback:** Total = status_line + headers + blank_line_CRLF + body = {status_len} + {header_len} + 2 + {body_len}. The blank CRLF separating headers from body is the critical delimiter — without it, the client cannot determine where headers end. [Total = linie_stare + antete + CRLF_linie_goală + corp = {status_len} + {header_len} + 2 + {body_len}. CRLF-ul gol care separă antetele de corp este delimitatorul critic — fără el, clientul nu poate determina unde se termină antetele.]

---

### 38. `Calculated`
**N08.D04.Q08: TCP acknowledgement number after data transfer / Numărul de confirmare TCP după transferul de date**

> During a TCP connection, the server sends a segment with sequence number {seq} carrying {data_len} bytes of HTTP response data. What acknowledgement number should the client send in its next ACK? [În timpul unei conexiuni TCP, serverul trimite un segment cu numărul de secvență {seq} care transportă {data_len} octeți de date de răspuns HTTP. Ce număr de confirmare ar trebui să trimită clientul în următorul ACK?]


> 💡 **Feedback:** The acknowledgement number = sequence number + data length. This indicates the next byte the receiver expects. ACK = {seq} + {data_len}. TCP uses cumulative acknowledgements based on byte positions, not segment counts. [Numărul de confirmare = numărul de secvență + lungimea datelor. Aceasta indică următorul octet pe care receptorul îl așteaptă. ACK = {seq} + {data_len}. TCP folosește confirmări cumulative bazate pe pozițiile octeților, nu pe numărul de segmente.]

---

### 39. `Numerical`
**N08.C01.Q02: Maximum valid port number / Numărul maxim valid de port**

> What is the highest valid port number that a TCP or UDP socket can bind to? Enter a whole number. [Care este cel mai mare număr valid de port la care un socket TCP sau UDP se poate lega? Introduceți un număr întreg.]


> 💡 **Feedback:** Port numbers are 16-bit unsigned integers (0 to (...)). The value 65536 is a common misconception — it represents the total count of possible values, not the maximum value. [Numerele de port sunt întregi fără semn pe 16 biți (0 până la (...)). Valoarea 65536 este o concepție greșită frecventă — aceasta reprezintă numărul total de valori posibile, nu valoarea maximă.]

---

### 40. `Numerical`
**N08.C01.Q05: TCP header minimum size in bytes / Dimensiunea minimă a antetului TCP în octeți**

> What is the minimum size, in bytes, of a TCP header without options? Enter a whole number. [Care este dimensiunea minimă, în octeți, a unui antet TCP fără opțiuni? Introduceți un număr întreg.]


> 💡 **Feedback:** The TCP header has a minimum of (...) bytes (160 bits): source port (2B), destination port (2B), sequence number (4B), acknowledgement number (4B), data offset + flags (2B), window size (2B), checksum (2B), urgent pointer (2B). [Antetul TCP are minim (...) de octeți (160 biți): port sursă (2O), port destinație (2O), număr de secvență (4O), număr de confirmare (4O), offset date + fanioane (2O), dimensiune fereastră (2O), sumă de control (2O), pointer urgent (2O).]

---

### 41. `Numerical`
**N08.C01.Q06: UDP header size in bytes / Dimensiunea antetului UDP în octeți**

> What is the fixed size, in bytes, of a UDP header? Enter a whole number. [Care este dimensiunea fixă, în octeți, a unui antet UDP? Introduceți un număr întreg.]


> 💡 **Feedback:** The UDP header is exactly (...) bytes: source port (2B), destination port (2B), length (2B), checksum (2B). This minimal overhead makes UDP suitable for latency-sensitive applications. [Antetul UDP are exact (...) octeți: port sursă (2O), port destinație (2O), lungime (2O), sumă de control (2O). Acest overhead minimal face UDP potrivit pentru aplicații sensibile la latență.]

---

### 42. `Numerical`
**N08.D03.Q03: UDP header fixed size in bytes / Dimensiunea fixă a antetului UDP în octeți**

> The UDP header has exactly four fields, each 2 bytes wide. What is the total UDP header size in bytes? [Antetul UDP are exact patru câmpuri, fiecare cu lățimea de 2 octeți. Care este dimensiunea totală a antetului UDP în octeți?]


> 💡 **Feedback:** UDP header = 4 fields * 2 bytes = (...) bytes. Fields: Source Port, Destination Port, Length, Checksum. [Antetul UDP = 4 câmpuri * 2 octeți = (...) octeți. Câmpuri: Port Sursă, Port Destinație, Lungime, Sumă de control.]

---

### 43. `Calculated`
**N08.D04.Q02: Maximum TCP segment payload with standard MSS / Sarcina utilă maximă a segmentului TCP cu MSS standard**

> An Ethernet frame has an MTU of {mtu} bytes. The IP header is 20 bytes and the TCP header is 20 bytes (no options). What is the Maximum Segment Size (MSS) — the largest TCP payload — in bytes? [Un cadru Ethernet are un MTU de {mtu} octeți. Antetul IP este de 20 de octeți, iar antetul TCP este de 20 de octeți (fără opțiuni). Care este dimensiunea maximă a segmentului (MSS) — cea mai mare sarcină utilă TCP — în octeți?]


> 💡 **Feedback:** MSS = MTU − IP_header − TCP_header = {mtu} − 20 − 20 = {mtu}−40. For standard Ethernet (MTU=1500), MSS=1460. [MSS = MTU − antet_IP − antet_TCP = {mtu} − 20 − 20 = {mtu}−40. Pentru Ethernet standard (MTU=1500), MSS=1460.]

---


## W08 — Drag & Drop   (6 questions)

### 44. `Drag & Drop into Text`
**N02.D05.Q05: Arrange the TCP three-way handshake flag sequence / Aranjați secvența indicatorilor din handshake-ul TCP în trei pași**

> Place the TCP flags in the correct order of the three-way handshake. [Plasați indicatorii TCP în ordinea corectă a handshake-ului în trei pași.]

```
Step 1 (Client → Server): [[1]]
```

```
Step 2 (Server → Client): [[2]]
```

```
Step 3 (Client → Server): [[3]]
```

**Available choices / Variante disponibile: SYN  |  SYN-ACK  |  ACK  |  FIN  |  RST  |  PSH**


> 💡 **Feedback:** The TCP three-way handshake sequence is SYN → SYN-ACK → ACK. The client initiates with SYN, the server responds with SYN-ACK, and the client completes with ACK. [Secvența handshake-ului TCP în trei pași este SYN → SYN-ACK → ACK. Clientul inițiază cu SYN, serverul răspunde cu SYN-ACK, iar clientul finalizează cu ACK.]

---

### 45. `Drag & Drop into Text`
**N08.D05.Q01: HTTP request line structure / Structura liniei de cerere HTTP**

> Arrange the components of an HTTP/1.1 request line in their correct order, separated by single spaces. [Aranjați componentele unei linii de cerere HTTP/1.1 în ordinea corectă, separate prin spații singulare.]

```
[[1]] [[2]] [[3]]
```

**Available choices / Variante disponibile: GET  |  /index.html  |  HTTP/1.1  |  POST  |  HTTP/2  |  /api/data**


> 💡 **Feedback:** The HTTP request line format is: METHOD SP REQUEST-TARGET SP HTTP-VERSION. For example: GET /index.html HTTP/1.1 [Formatul liniei de cerere HTTP este: METHOD SP REQUEST-TARGET SP HTTP-VERSION. De exemplu: GET /index.html HTTP/1.1]

---

### 46. `Drag & Drop into Text`
**N08.D05.Q02: TCP server socket lifecycle / Ciclul de viață al socket-ului server TCP**

> Complete the correct order of socket calls to set up a TCP server in 3b_socket-http-server_example.py. [Completați ordinea corectă a apelurilor socket pentru configurarea unui server TCP în 3b_socket-http-server_example.py.]

> s = socket.socket(AF_INET, SOCK_STREAM)

> s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

```
s.[[1]]((host, port))
```

```
s.[[2]](backlog)
```

```
conn, addr = s.[[3]]()
```

**Available choices / Variante disponibile: bind  |  listen  |  accept  |  connect  |  recv  |  send**


> 💡 **Feedback:** TCP server lifecycle: socket() -> setsockopt() -> bind() -> listen() -> accept(). bind() assigns the address, listen() marks passive, accept() waits for clients. [Ciclul de viață al serverului TCP: socket() -> setsockopt() -> bind() -> listen() -> accept(). bind() atribuie adresa, listen() marchează pasiv, accept() așteaptă clienți.]

---

### 47. `Drag & Drop into Text`
**N08.D05.Q05: X-Forwarded-For header construction / Construcția antetului X-Forwarded-For**

> When a reverse proxy forwards a request from client IP 10.0.0.5, it appends a header to preserve the original client address. Complete the header line. [Când un proxy invers retransmite o cerere de la IP-ul client 10.0.0.5, adaugă un antet pentru a păstra adresa originală a clientului. Completați linia de antet.]

```
[[1]]: [[2]]
```

**Available choices / Variante disponibile: X-Forwarded-For  |  10.0.0.5  |  X-Real-IP  |  172.28.8.10  |  Via  |  127.0.0.1**


> 💡 **Feedback:** X-Forwarded-For carries the chain of client IPs through proxies. Each proxy appends the requesting IP. The format is: X-Forwarded-For: client_ip[, proxy1_ip, ...] [X-Forwarded-For transportă lanțul de IP-uri client prin proxy-uri. Fiecare proxy adaugă IP-ul solicitant. Formatul este: X-Forwarded-For: ip_client[, ip_proxy1, ...]]

---

### 48. `Drag & Drop into Text`
**N08.D05.Q06: HTTP response status line components / Componentele liniei de stare a răspunsului HTTP**

> Arrange the components of a successful HTTP response status line. [Aranjați componentele unei linii de stare a unui răspuns HTTP reușit.]

```
[[1]] [[2]] [[3]]
```

**Available choices / Variante disponibile: HTTP/1.1  |  200  |  OK  |  GET  |  404  |  Not Found**


> 💡 **Feedback:** The HTTP response status line format is: HTTP-VERSION SP STATUS-CODE SP REASON-PHRASE. Example: HTTP/1.1 200 OK [Formatul liniei de stare a răspunsului HTTP este: HTTP-VERSION SP STATUS-CODE SP REASON-PHRASE. Exemplu: HTTP/1.1 200 OK]

---

### 49. `Drag & Drop into Text`
**N08.D05.Q03: Wireshark filter for pure SYN packets / Filtru Wireshark pentru pachete SYN pure**

> Build the Wireshark display filter that captures only pure SYN packets (connection initiation, not SYN-ACK). [Construiți filtrul de afișare Wireshark care captează doar pachete SYN pure (inițiere conexiune, nu SYN-ACK).]

```
[[1]]==1 && [[2]]==0
```

**Available choices / Variante disponibile: tcp.flags.syn  |  tcp.flags.ack  |  tcp.flags.fin  |  tcp.flags.rst**


> 💡 **Feedback:** tcp.flags.syn==1 && tcp.flags.ack==0 matches only the initial SYN segment, excluding SYN-ACK responses which have both flags set. [tcp.flags.syn==1 && tcp.flags.ack==0 captează doar segmentul SYN inițial, excluzând răspunsurile SYN-ACK care au ambele flaguri setate.]

---


## W08 — Gap Select   (6 questions)

### 50. `Gap Select`
**N01.D10.Q02: Transport Protocol Assignment / Atribuirea protocolului de transport**

```
For web browsing, the transport protocol is [[1]]. For live video streaming, the preferred transport protocol is [[2]]. [Pentru navigarea web, protocolul de transport este ___. Pentru streaming video în direct, protocolul de transport preferat este ___.]
```

**Available choices / Variante disponibile: TCP  |  UDP  |  ICMP  |  ARP  |  UDP  |  TCP  |  ICMP  |  ARP**


> 💡 **Feedback:** HTTP uses TCP (reliability needed). Live streaming prefers UDP (low latency needed). [HTTP folosește TCP (fiabilitate necesară). Streaming-ul în direct preferă UDP (latență scăzută necesară).]

---

### 51. `Gap Select`
**N01.D10.Q08: Three-Way Handshake Flags / Steagurile handshake-ului în trei pași**

```
In the TCP handshake, the client first sends [[1]], the server responds with [[2]], and the client confirms with [[3]]. [În handshake-ul TCP, clientul trimite mai întâi ___, serverul răspunde cu ___, iar clientul confirmă cu ___.]
```

**Available choices / Variante disponibile: SYN  |  SYN-ACK  |  ACK  |  FIN  |  RST  |  FIN-ACK**


> 💡 **Feedback:** Handshake: SYN -> SYN-ACK -> ACK. Three segments exchanged total. [Handshake: SYN -> SYN-ACK -> ACK. Trei segmente schimbate în total.]

---

### 52. `Gap Select`
**N08.D10.Q02: Socket option preventing address reuse errors / Opțiunea de socket care previne erorile de reutilizare a adresei**

```
Before calling bind(), the exercise sets the [[1]] socket option to value [[2]] to prevent port reuse errors after server restart. [Înainte de apelul bind(), exercițiul setează opțiunea de socket ___ la valoarea ___ pentru a preveni erorile de reutilizare a portului după repornirea serverului.]
```

**Available choices / Variante disponibile: SO_REUSEADDR  |  1  |  SO_KEEPALIVE  |  0**


> 💡 **Feedback:** SO_REUSEADDR with value 1 allows immediate port reuse. Without it, the port stays in TIME_WAIT state after server shutdown. [SO_REUSEADDR cu valoarea 1 permite reutilizarea imediată a portului. Fără ea, portul rămâne în starea TIME_WAIT după oprirea serverului.]

---

### 53. `Gap Select`
**N08.D10.Q03: HTTP message separator / Separatorul mesajelor HTTP**

```
HTTP headers are separated from the body by a blank line, which consists of two consecutive [[1]] sequences, forming the pattern [[2]]. [Antetele HTTP sunt separate de corp printr-o linie goală, care constă din două secvențe ___ consecutive, formând modelul ___.]
```

**Available choices / Variante disponibile: CRLF  |  \r\n\r\n  |  LF  |  \n\n**


> 💡 **Feedback:** Headers end with CRLF, then the blank line is another CRLF, making \r\n\r\n the boundary between headers and body. [Antetele se termină cu CRLF, apoi linia goală este un alt CRLF, făcând \r\n\r\n limita dintre antete și corp.]

---

### 54. `Gap Select`
**N08.D10.Q04: Reverse proxy header for client IP / Antetul proxy-ului invers pentru IP-ul clientului**

```
When nginx forwards a request, it adds the [[1]] header containing the original [[2]] address. [Când nginx retransmite o cerere, adaugă antetul ___ care conține adresa ___ originală.]
```

**Available choices / Variante disponibile: X-Forwarded-For  |  client IP  |  X-Real-IP  |  server MAC**


> 💡 **Feedback:** X-Forwarded-For carries the client's IP through the proxy chain. Each proxy appends the IP of the requester it received the connection from. [X-Forwarded-For transportă IP-ul clientului prin lanțul de proxy-uri. Fiecare proxy adaugă IP-ul solicitantului de la care a primit conexiunea.]

---

### 55. `Gap Select`
**N08.D10.Q05: TCP handshake step identification / Identificarea pașilor handshake-ului TCP**

```
In the three-way handshake, the client first sends [[1]], the server responds with [[2]], and the client completes with [[3]]. [În handshake-ul în trei pași, clientul trimite mai întâi ___, serverul răspunde cu ___, iar clientul completează cu ___.]
```

**Available choices / Variante disponibile: SYN  |  SYN-ACK  |  ACK  |  FIN  |  RST-ACK  |  PSH**


> 💡 **Feedback:** Three-way handshake: SYN (client initiates) -> SYN-ACK (server acknowledges and synchronises) -> ACK (client confirms, connection established). [Handshake în trei pași: SYN (clientul inițiază) -> SYN-ACK (serverul confirmă și sincronizează) -> ACK (clientul confirmă, conexiunea este stabilită).]

---
