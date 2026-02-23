# Week 14 — Computer Networks
### *Rețele de Calculatoare — Săptămâna 14*

> Question Pool — Practice Set

---

## 📚 W14 — Curs / Lecture   (32 questions)

---

### Q1. `N14.C01.Q01`
**OSI Layer for IP Addressing / Stratul OSI pentru adresarea IP**

*Multiple Choice*

> At which layer of the OSI model does logical addressing using IP take place? [La ce strat al modelului OSI are loc adresarea logică folosind IP?]

- **a)** Network (Layer 3) [Rețea (Layer 3)]
- **b)** Data Link (Layer 2) [Legătură de date (Layer 2)]
- **c)** Transport (Layer 4) [Transport (Layer 4)]
- **d)** Application (Layer 7) [Aplicație (Layer 7)]

<details><summary>💡 Feedback</summary>

The Network Layer handles logical addressing via IP, enabling routing between different networks. MAC addresses operate at Layer 2, port numbers at Layer 4. [Stratul de rețea gestionează adresarea logică prin IP, permițând rutarea între rețele diferite. Adresele MAC operează la Layer 2, numerele de port la Layer 4.]

</details>

---

### Q2. `N14.C01.Q02`
**TCP PDU Designation / Denumirea PDU-ului TCP**

*Multiple Choice*

> What is the protocol data unit (PDU) at the Transport layer when using TCP? [Care este unitatea de date de protocol (PDU) la stratul de transport când se utilizează TCP?]

- **a)** Segment [Segment]
- **b)** Frame [Cadru] [Cadru]
- **c)** Packet [Pachet] [Pachet]
- **d)** Datagram [Datagramă] [Datagramă]

<details><summary>💡 Feedback</summary>

TCP divides application data into segments at the Transport layer. UDP uses datagrams, frames belong to the Data Link layer, and packets to the Network layer. [TCP împarte datele aplicației în segmente la stratul de transport. UDP folosește datagrame, cadrele aparțin stratului legătură de date, iar pachetele stratului de rețea.]

</details>

---

### Q3. `N14.C01.Q03`
**IP and MAC Interchangeability / Interschimbabilitatea IP și MAC**

*True / False*

> IP addresses and MAC addresses are interchangeable because both identify devices on a network. [Adresele IP și adresele MAC sunt interschimbabile deoarece ambele identifică dispozitive într-o rețea.]

- **a)** true
- **b)** false

<details><summary>💡 Feedback</summary>

MAC addresses identify physical interfaces for local communication, whilst IP addresses provide logical addressing for routing. A packet needs both: MAC for the next hop, IP for the final destination. [Adresele MAC identifică interfețele fizice pentru comunicarea locală, în timp ce adresele IP asigură adresarea logică pentru rutare. Un pachet are nevoie de ambele: MAC pentru următorul salt, IP pentru destinația finală.]

</details>

---

### Q4. `N14.C01.Q04`
**Encapsulation Order / Ordinea încapsulării**

*Multiple Choice*

> When application data travels down the TCP/IP stack, what is the correct order of encapsulation? [Când datele aplicației coboară prin stiva TCP/IP, care este ordinea corectă a încapsulării?]

- **a)** Data → Segment → Packet → Frame [Date → Segment → Pachet → Cadru]
- **b)** Data → Packet → Segment → Frame [Date → Pachet → Segment → Cadru]
- **c)** Data → Frame → Packet → Segment [Date → Cadru → Pachet → Segment]
- **d)** Frame → Packet → Segment → Data [Cadru → Pachet → Segment → Date]

<details><summary>💡 Feedback</summary>

Each layer adds its own header as data descends: Transport adds TCP/UDP header creating a segment, Network adds IP header creating a packet, Data Link adds Ethernet header and trailer creating a frame. [Fiecare strat adaugă propriul antet pe măsură ce datele coboară: Transportul adaugă antetul TCP/UDP creând un segment, Rețeaua adaugă antetul IP creând un pachet, Legătura de date adaugă antetul și trailer-ul Ethernet creând un cadru.]

</details>

---

### Q5. `N14.C01.Q05`
**Transport Layer Primary Function / Funcția principală a stratului de transport**

*Multiple Choice*

> What is the primary function of the Transport layer in the TCP/IP model? [Care este funcția principală a stratului de transport în modelul TCP/IP?]

- **a)** End-to-end communication between applications using port numbers [Comunicarea capăt-la-capăt între aplicații utilizând numere de port]
- **b)** Routing packets between networks using IP addresses [Rutarea pachetelor între rețele folosind adrese IP]
- **c)** Physical transmission of bits over cables and signals [Transmiterea fizică a biților prin cabluri și semnale]
- **d)** Domain name resolution and application-level data formatting for end users [Rezoluția numelor de domeniu și formatarea datelor la nivel de aplicație pentru utilizatorii finali]

<details><summary>💡 Feedback</summary>

The Transport layer provides end-to-end communication between applications. TCP offers reliable streams and UDP offers datagrams. Routing between networks is a Network layer responsibility. [Stratul de transport asigură comunicarea capăt-la-capăt între aplicații. TCP oferă fluxuri fiabile, iar UDP oferă datagrame. Rutarea între rețele este responsabilitatea stratului de rețea.]

</details>

---

### Q6. `N14.C01.Q06`
**Protocol for IP-to-MAC Resolution / Protocolul pentru rezoluția IP-la-MAC**

*Multiple Choice*

> Which protocol resolves an IP address to a MAC address within a local network segment? [Care protocol rezolvă o adresă IP într-o adresă MAC în cadrul unui segment de rețea locală?]

- **a)** ARP (Address Resolution Protocol) maps IP addresses to MAC addresses within a local network segment [ARP (Address Resolution Protocol) mapează adresele IP la adresele MAC în cadrul unui segment de rețea locală]
- **b)** DNS (Domain Name System) [DNS (Domain Name System)]
- **c)** DHCP (Dynamic Host Configuration Protocol) [DHCP (Dynamic Host Configuration Protocol)]
- **d)** ICMP (Internet Control Message Protocol) [ICMP (Internet Control Message Protocol)]

<details><summary>💡 Feedback</summary>

ARP maps IP addresses to MAC addresses on the local network. DNS resolves domain names to IPs, DHCP assigns IPs automatically, and ICMP handles diagnostics like ping. [ARP mapează adresele IP la adrese MAC în rețeaua locală. DNS rezolvă nume de domeniu la IP-uri, DHCP atribuie IP-uri automat, iar ICMP gestionează diagnosticarea, precum ping.]

</details>

---

### Q7. `N14.C02.Q01`
**TCP Handshake Sequence / Secvența handshake-ului TCP**

*Multiple Choice*

> What is the correct sequence of TCP flag combinations during the three-way handshake? [Care este secvența corectă a combinațiilor de fanioane TCP în timpul handshake-ului în trei pași?]

- **a)** SYN → SYN-ACK → ACK [SYN → SYN-ACK → ACK]
- **b)** SYN → ACK → SYN-ACK [SYN → ACK → SYN-ACK]
- **c)** SYN → SYN → ACK [SYN → SYN → ACK]
- **d)** ACK → SYN-ACK → SYN [ACK → SYN-ACK → SYN]

<details><summary>💡 Feedback</summary>

TCP establishment requires three packets: client sends SYN, server replies SYN-ACK (one packet with both flags set), client confirms with ACK. [Stabilirea TCP necesită trei pachete: clientul trimite SYN, serverul răspunde SYN-ACK (un pachet cu ambele fanioane setate), clientul confirmă cu ACK.]

</details>

---

### Q8. `N14.C02.Q02`
**TCP vs UDP Core Difference / Diferența fundamentală TCP vs UDP**

*Multiple Choice*

> What is the fundamental difference between TCP and UDP at the transport layer? [Care este diferența fundamentală între TCP și UDP la stratul de transport?]

- **a)** TCP provides reliable, ordered delivery; UDP provides best-effort delivery without guarantees [TCP oferă livrare fiabilă și ordonată; UDP oferă livrare best-effort fără garanții]
- **b)** TCP encrypts data automatically while UDP transmits in plaintext only [TCP criptează datele automat, în timp ce UDP transmite doar în text clar]
- **c)** UDP operates at Layer 3 while TCP functions at Layer 4 of the OSI model [UDP operează la Layer 3, în timp ce TCP funcționează la Layer 4 al modelului OSI]
- **d)** UDP provides fast connectionless delivery without acknowledgements or retransmissions, suitable for latency-sensitive applications like streaming and DNS queries [UDP asigură livrare rapidă fără conexiune, fără confirmări sau retransmisii, potrivită pentru aplicații sensibile la latență precum streaming și interogări DNS]

<details><summary>💡 Feedback</summary>

TCP is connection-oriented with reliability through ACKs and retransmissions. UDP is connectionless and best-effort. The distinction concerns delivery guarantees, not speed alone. [TCP este orientat pe conexiune cu fiabilitate prin confirmări (ACK) și retransmisii. UDP este fără conexiune și de tip best-effort. Distincția privește garanțiile de livrare, nu doar viteza.]

</details>

---

### Q9. `N14.C02.Q03`
**TCP Four-Way Termination Count / Numărul de pachete la terminarea TCP**

*Multiple Choice*

> How many packets are exchanged during a graceful TCP connection termination? [Câte pachete se schimbă în timpul terminării grațioase a unei conexiuni TCP?]

- **a)** 4 (FIN, ACK, FIN, ACK) [4 (FIN, ACK, FIN, ACK)]
- **b)** 2 (FIN, ACK) [2 (FIN, ACK)]
- **c)** 3 — FIN, ACK, FIN-ACK exchange in total [3 — schimb FIN, ACK, FIN-ACK în total]
- **d)** 1 (RST) [1 (RST)]

<details><summary>💡 Feedback</summary>

Graceful termination uses four packets: FIN from initiator, ACK from receiver, FIN from receiver, ACK from initiator. Each side independently closes its half of the connection. [Terminarea grațioasă folosește patru pachete: FIN de la inițiator, ACK de la receptor, FIN de la receptor, ACK de la inițiator. Fiecare parte își închide independent jumătatea de conexiune.]

</details>

---

### Q10. `N14.C02.Q05`
**HTTP Persistent Connections / Conexiunile HTTP persistente**

*True / False*

> Every individual HTTP request requires a new TCP three-way handshake. [Fiecare cerere HTTP individuală necesită un nou handshake TCP în trei pași.]

- **a)** true
- **b)** false

<details><summary>💡 Feedback</summary>

HTTP/1.1 introduced keep-alive connections. A new handshake is needed only when the connection is closed or times out. [HTTP/1.1 a introdus conexiunile keep-alive. Un nou handshake este necesar doar când conexiunea este închisă sau expiră.]

</details>

---

### Q11. `N14.C03.Q01`
**HTTP 502 Bad Gateway in Reverse Proxy / HTTP 502 Bad Gateway la proxy invers**

*Multiple Choice*

> In a reverse proxy architecture like the Week 14 lab, what does HTTP 502 Bad Gateway indicate? [Într-o arhitectură de proxy invers precum laboratorul din săptămâna 14, ce indică HTTP 502 Bad Gateway?]

- **a)** The reverse proxy received an invalid response or no response from a backend server [Proxy-ul invers a primit un răspuns invalid sau niciun răspuns de la un server backend]
- **b)** The client sent a syntactically malformed HTTP request that the proxy could not parse or forward correctly [Clientul a trimis o cerere HTTP malformată sintactic pe care proxy-ul nu a putut-o analiza sau redirecționa corect]
- **c)** The reverse proxy itself crashed and cannot process any incoming HTTP requests [Proxy-ul invers s-a blocat și nu poate procesa nicio cerere HTTP de intrare]
- **d)** The requested resource does not exist on any of the configured backend servers [Resursa solicitată nu există pe niciunul dintre serverele backend configurate]

<details><summary>💡 Feedback</summary>

HTTP 502 means the proxy (acting as gateway) received a bad response from an upstream server. In Week 14, this occurs when a backend container (app1/app2) is down or unresponsive. [HTTP 502 înseamnă că proxy-ul (acționând ca poartă de acces) a primit un răspuns eronat de la un server din amonte. În săptămâna 14, aceasta apare când un container backend (app1/app2) este oprit sau nu răspunde.]

</details>

---

### Q12. `N14.C03.Q02`
**HTTP Request Structure Components / Componentele structurii cererii HTTP**

*Multiple Choice*

> An HTTP/1.1 request sent by curl to the Week 14 load balancer contains which mandatory first line? [O cerere HTTP/1.1 trimisă de curl către echilibratorul de sarcină din săptămâna 14 conține ce primă linie obligatorie?]

- **a)** GET / HTTP/1.1 (method, path, and protocol version) [GET / HTTP/1.1 (metodă, cale și versiune de protocol)]
- **b)** HTTP/1.1 200 OK (protocol version and status code) [HTTP/1.1 200 OK (versiune de protocol și cod de stare)]
- **c)** Host: localhost:8080 (the Host header field) [Host: localhost:8080 (câmpul antet Host)]
- **d)** Content-Type: text/html (the content type header) [Content-Type: text/html (antetul tip de conținut)]

<details><summary>💡 Feedback</summary>

An HTTP request begins with the request line: method (GET), path (/), and version (HTTP/1.1). The Host header is mandatory in HTTP/1.1 but is a header, not the first line. Status codes appear in responses. [O cerere HTTP începe cu linia de cerere: metoda (GET), calea (/), și versiunea (HTTP/1.1). Antetul Host este obligatoriu în HTTP/1.1, dar este un antet, nu prima linie. Codurile de stare apar în răspunsuri.]

</details>

---

### Q13. `N14.C03.Q03`
**X-Backend Header Purpose / Scopul antetului X-Backend**

*Multiple Choice*

> In the Week 14 load balancer response, the X-Backend header serves what purpose? [În răspunsul echilibratorului de sarcină din săptămâna 14, antetul X-Backend servește ce scop?]

- **a)** It identifies which backend server (app1 or app2) processed the request [Identifică ce server backend (app1 sau app2) a procesat cererea]
- **b)** It encrypts the backend address to prevent information disclosure [Criptează adresa backend pentru a preveni divulgarea informațiilor]
- **c)** It specifies the load balancing algorithm currently in use by the proxy [Specifică algoritmul de echilibrare a sarcinii utilizat curent de proxy]
- **d)** It provides authentication credentials for the backend service access [Furnizează credențiale de autentificare pentru accesul la serviciul backend]

<details><summary>💡 Feedback</summary>

The lb_proxy.py code adds X-Backend header with the backend's address (e.g., 172.20.0.2:8001) so clients and administrators can track which backend handled each request. [Codul lb_proxy.py adaugă antetul X-Backend cu adresa backend-ului (de ex., 172.20.0.2:8001) astfel încât clienții și administratorii pot urmări ce backend a gestionat fiecare cerere.]

</details>

---

### Q14. `N14.C03.Q04`
**HTTP Status Code Categories / Categoriile codurilor de stare HTTP**

*Multiple Choice*

> To which category do status codes 500, 502, and 503 belong? [Cărei categorii aparțin codurile de stare 500, 502 și 503?]

- **a)** 5xx Server Error — the server failed to fulfil a valid request [5xx Eroare de server — serverul nu a reușit să îndeplinească o cerere validă]
- **b)** 4xx Client Error — the request contains incorrect syntax or parameters [4xx Eroare de client — cererea conține sintaxă sau parametri incorecți]
- **c)** 3xx Redirection — further action is needed to complete the original request [3xx Redirecționare — sunt necesare acțiuni suplimentare pentru a completa cererea]
- **d)** 2xx Success — the request was received, understood, and processed correctly [2xx Succes — cererea a fost primită, înțeleasă și procesată corect]

<details><summary>💡 Feedback</summary>

5xx codes indicate server-side failures. 500 is a general server error, 502 indicates a bad response from an upstream server, and 503 means the service is temporarily unavailable. [Codurile 5xx indică erori pe partea serverului. 500 este o eroare generală, 502 indică un răspuns eronat de la un server din amonte, iar 503 înseamnă că serviciul este temporar indisponibil.]

</details>

---

### Q15. `N14.C03.Q05`
**HTTP 200 vs 201 Distinction / Distincția HTTP 200 vs 201**

*True / False*

> HTTP status codes 200 (OK) and 201 (Created) both indicate successful operations, but 201 specifically signals that a new resource was created as a result of the request. [Codurile de stare HTTP 200 (OK) și 201 (Created) indică ambele operații reușite, dar 201 semnalează specific că o nouă resursă a fost creată ca rezultat al cererii.]

- **a)** true
- **b)** false

<details><summary>💡 Feedback</summary>

HTTP 2xx codes all indicate success. 200 OK is the general response, while 201 Created specifically confirms a new resource was generated, typically in response to POST. [Codurile HTTP 2xx indică toate succes. 200 OK este răspunsul general, în timp ce 201 Created confirmă specific că o resursă nouă a fost generată, de obicei ca răspuns la POST.]

</details>

---

### Q16. `N14.C04.Q01`
**Round-Robin Distribution Pattern / Modelul de distribuție Round-Robin**

*Multiple Choice*

> With round-robin scheduling and two healthy backends (app1, app2), what pattern results from four sequential requests? [Cu planificarea round-robin și două backend-uri sănătoase (app1, app2), ce model rezultă din patru cereri secvențiale?]

- **a)** app1, app2, app1, app2 — requests alternate deterministically [app1, app2, app1, app2 — cererile alternează determinist]
- **b)** Random distribution — any backend may handle each request unpredictably [Distribuție aleatorie — orice backend poate gestiona fiecare cerere imprevizibil]
- **c)** app1, app1, app2, app2 — first two go to app1, then two go to app2 [app1, app1, app2, app2 — primele două merg la app1, apoi două la app2]
- **d)** All four go to app1 — the load balancer selects one preferred server [Toate patru merg la app1 — echilibratorul alege un server preferat]

<details><summary>💡 Feedback</summary>

Round-robin is deterministic and sequential, not random. With N backends, request K goes to backend (K mod N). The Week 14 lab demonstrates this with the X-Backend response header. [Round-robin este determinist și secvențial, nu aleatoriu. Cu N backend-uri, cererea K merge la backend-ul (K mod N). Laboratorul din săptămâna 14 demonstrează aceasta prin antetul de răspuns X-Backend.]

</details>

---

### Q17. `N14.C04.Q02`
**Load Balancers Detect Failures Instantly / Echilibratoarele detectează eșecurile instantaneu**

*True / False*

> A load balancer immediately stops sending traffic to a backend server the moment it fails. [Un echilibrator de sarcină oprește imediat trimiterea traficului către un server backend în momentul în care acesta eșuează.]

- **a)** true
- **b)** false

<details><summary>💡 Feedback</summary>

Health checks run periodically. During the detection interval, the LB may still route to a failed backend, causing temporary 502 errors. The Week 14 lb_proxy.py marks a backend unhealthy after 3 consecutive failures. [Verificările de sănătate se execută periodic. În intervalul de detectare, echilibratorul poate ruta în continuare către un backend eșuat, cauzând erori temporare 502. Codul lb_proxy.py din săptămâna 14 marchează un backend ca nesănătos după 3 eșecuri consecutive.]

</details>

---

### Q18. `N14.C04.Q03`
**Reverse Proxy Forwarding Headers / Antetele de redirecționare ale proxy-ului invers**

*Multiple Choice*

> The Week 14 load balancer adds X-Forwarded-For and X-Real-IP headers. Why are these necessary? [Echilibratorul de sarcină din săptămâna 14 adaugă antetele X-Forwarded-For și X-Real-IP. De ce sunt acestea necesare?]

- **a)** To preserve the original client IP address, which would otherwise be replaced by the proxy's address [Pentru a păstra adresa IP originală a clientului, care altfel ar fi înlocuită cu adresa proxy-ului]
- **b)** X-Forwarded-For and X-Real-IP headers preserve the original client IP address, allowing backend servers to identify the true source of each proxied request [Antetele X-Forwarded-For și X-Real-IP păstrează adresa IP originală a clientului, permițând serverelor backend să identifice sursa reală a fiecărei cereri proximate]
- **c)** To authenticate the load balancer identity to the backend application servers [Pentru a autentifica identitatea echilibratorului de sarcină la serverele backend]
- **d)** To specify which load balancing algorithm should be applied to the request [Pentru a specifica ce algoritm de echilibrare a sarcinii ar trebui aplicat cererii]

<details><summary>💡 Feedback</summary>

When a reverse proxy forwards a request, the backend sees the proxy's IP as the source. X-Forwarded-For preserves the original client IP through the forwarding chain. [Când un proxy invers redirecționează o cerere, backend-ul vede IP-ul proxy-ului ca sursă. X-Forwarded-For păstrează IP-ul original al clientului prin lanțul de redirecționare.]

</details>

---

### Q19. `N14.C04.Q04`
**Weighted Round-Robin Behaviour / Comportamentul Round-Robin ponderat**

*Multiple Choice*

> If a weighted round-robin balancer is configured with weights A=3 and B=1, what is the expected request sequence? [Dacă un echilibrator round-robin ponderat este configurat cu ponderile A=3 și B=1, care este secvența așteptată a cererilor?]

- **a)** A, A, A, B, A, A, A, B, ... — proportional to configured weights [A, A, A, B, A, A, A, B, ... — proporțional cu ponderile configurate]
- **b)** A, B, A, B, A, B, ... — strict alternation regardless of any weight setting [A, B, A, B, A, B, ... — alternanță strictă indiferent de setarea ponderilor]
- **c)** B, B, B, A, B, B, B, A, ... — inverse proportional to configured weights [B, B, B, A, B, B, B, A, ... — invers proporțional cu ponderile configurate]
- **d)** Random distribution with 75% probability for A and 25% for B over time [Distribuție aleatorie cu 75% probabilitate pentru A și 25% pentru B în timp]

<details><summary>💡 Feedback</summary>

Weighted round-robin distributes requests proportionally to assigned weights. With A=3, B=1, backend A receives three requests for every one that B receives, in a deterministic cycle. [Round-robin ponderat distribuie cererile proporțional cu ponderile atribuite. Cu A=3, B=1, backend-ul A primește trei cereri pentru fiecare cerere primită de B, într-un ciclu determinist.]

</details>

---

### Q20. `N14.C04.Q05`
**Health Check Failure Threshold / Pragul de eșec al verificării de sănătate**

*Multiple Choice*

> In the Week 14 lb_proxy.py code, after how many consecutive failures does the load balancer mark a backend as unhealthy? [În codul lb_proxy.py din săptămâna 14, după câte eșecuri consecutive marchează echilibratorul de sarcină un backend ca nesănătos?]

- **a)** 3 consecutive failures trigger the unhealthy state [3 eșecuri consecutive declanșează starea de nesănătos]
- **b)** 1 failure immediately marks the backend as permanently unavailable [1 eșec marchează imediat backend-ul ca permanent indisponibil]
- **c)** 5 failures are needed before the backend health status changes [5 eșecuri sunt necesare înainte ca starea de sănătate a backend-ului să se schimbe]
- **d)** 10 consecutive timeouts within a one-minute window are required [10 timeout-uri consecutive în cadrul unei ferestre de un minut sunt necesare]

<details><summary>💡 Feedback</summary>

The Backend.mark_failure() method increments consecutive_failures. When this counter reaches 3 (self.consecutive_failures >= 3), the backend's healthy flag is set to False. [Metoda Backend.mark_failure() incrementează consecutive_failures. Când acest contor ajunge la 3 (self.consecutive_failures >= 3), fanionul healthy al backend-ului este setat la False.]

</details>

---

### Q21. `N14.T00.Q01`
**Scenario: Backend Failure Detection / Scenariu: Detectarea eșecului backend**

*Multiple Choice*

> A student runs 20 sequential curl requests to http://localhost:8080/. The first 8 alternate between app1 and app2. Requests 9-12 return 502 errors. Requests 13-20 all go to app2. What happened? [Un student execută 20 cereri curl secvențiale la http://localhost:8080/. Primele 8 alternează între app1 și app2. Cererile 9-12 returnează erori 502. Cererile 13-20 merg toate la app2. Ce s-a întâmplat?]

- **a)** app1 failed between requests 8 and 9; the LB detected the failure after 3 retries and routed all subsequent traffic to app2 [app1 a eșuat între cererile 8 și 9; echilibratorul a detectat eșecul după 3 reîncercări și a direcționat tot traficul ulterior către app2]
- **b)** The load balancer switched to weighted round-robin mode after detecting uneven response times [Echilibratorul a trecut la modul round-robin ponderat după detectarea timpilor de răspuns inegali]
- **c)** app2 was added as a new backend and the LB redistributed all traffic to the newest server [app2 a fost adăugat ca backend nou și echilibratorul a redistribuit tot traficul către cel mai nou server]
- **d)** The load balancer requires three consecutive health check failures (approximately 30 seconds with 10-second intervals) before marking the backend as unhealthy, during which temporary 502 Bad Gateway errors are returned to clients [Echilibratorul necesită trei eșecuri consecutive ale verificării de sănătate (aproximativ 30 de secunde cu intervale de 10 secunde) înainte de a marca backend-ul ca nesănătos, timp în care erori temporare 502 Bad Gateway sunt returnate clienților]

<details><summary>💡 Feedback</summary>

The pattern shows: normal round-robin (1-8), transition with 502s during health check detection (9-12, 3 failures needed), then single-backend routing (13-20). [Modelul arată: round-robin normal (1-8), tranziție cu 502 în timpul detectării verificării de sănătate (9-12, 3 eșecuri necesare), apoi rutare cu un singur backend (13-20).]

</details>

---

### Q22. `N14.T00.Q03`
**Scenario: Docker Network Troubleshooting / Scenariu: Depanarea rețelei Docker**

*Multiple Choice*

> A student runs docker exec week14_client ping 172.20.0.2 and gets 'Network is unreachable'. All containers show as running. What is the root cause? [Un student execută docker exec week14_client ping 172.20.0.2 și primește 'Network is unreachable'. Toate containerele sunt afișate ca active. Care este cauza de bază?]

- **a)** The client is on frontend_net (172.21.0.0/24) and cannot route to backend_net (172.20.0.0/24) directly [Clientul este pe frontend_net (172.21.0.0/24) și nu poate ruta direct către backend_net (172.20.0.0/24)]
- **b)** The ping utility is not installed inside the client container's Docker image [Utilitarul ping nu este instalat în imaginea Docker a containerului client]
- **c)** Containers on different Docker networks are completely isolated and cannot communicate directly; the load balancer bridges both networks as an intermediary [Containerele pe rețele Docker diferite sunt complet izolate și nu pot comunica direct; echilibratorul de sarcină face legătura între ambele rețele ca intermediar]
- **d)** The app1 container has crashed and its IP address was released back to DHCP [Containerul app1 s-a blocat și adresa sa IP a fost eliberată înapoi către DHCP]

<details><summary>💡 Feedback</summary>

Docker network isolation: client (frontend_net only) has no route to backend_net addresses. The LB bridges both networks; direct client-to-backend communication is by design impossible. [Izolarea rețelei Docker: clientul (doar pe frontend_net) nu are rută către adresele backend_net. Echilibratorul face punte între ambele rețele; comunicarea directă client-backend este imposibilă prin design.]

</details>

---

### Q23. `N14.T00.Q04`
**Scenario: Code Tracing RoundRobin with Failure / Scenariu: Trasarea codului RoundRobin cu eșec**

*Multiple Choice*

> The Week 14 LoadBalancer has backends [A, B]. Backend A is marked unhealthy. What does get_next_backend() return for 3 consecutive calls? [Echilibratorul LoadBalancer din săptămâna 14 are backend-urile [A, B]. Backend-ul A este marcat ca nesănătos. Ce returnează get_next_backend() pentru 3 apeluri consecutive?]

- **a)** B, B, B — only healthy backends are in the selection pool [B, B, B — doar backend-urile sănătoase sunt în grupul de selecție]
- **b)** A, B, A — round-robin continues regardless of health status [A, B, A — round-robin continuă indiferent de starea de sănătate]
- **c)** B, A, B — unhealthy backends are tried every other request for recovery [B, A, B — backend-urile nesănătoase sunt încercate la fiecare a doua cerere pentru recuperare]
- **d)** None, B, None — the method returns None for the unhealthy backend position [None, B, None — metoda returnează None pentru poziția backend-ului nesănătos]

<details><summary>💡 Feedback</summary>

get_next_backend() filters to healthy_backends first. With only B healthy, the list has one element and all calls return B. [get_next_backend() filtrează mai întâi la healthy_backends. Cu doar B sănătos, lista are un singur element și toate apelurile returnează B.]

</details>

---

### Q24. `N14.T00.Q05`
**Scenario: HTTP Header Chain Analysis / Scenariu: Analiza lanțului de antete HTTP**

*Multiple Choice*

> A Wireshark capture shows: client (172.21.0.2) → lb (172.21.0.10:8080) with a GET /. Then lb (172.20.0.10) → app1 (172.20.0.2:8001) with the same GET / plus X-Forwarded-For: 172.21.0.2. Why does the LB use different source IPs? [O captură Wireshark arată: client (172.21.0.2) → lb (172.21.0.10:8080) cu un GET /. Apoi lb (172.20.0.10) → app1 (172.20.0.2:8001) cu același GET / plus X-Forwarded-For: 172.21.0.2. De ce folosește echilibratorul IP-uri sursă diferite?]

- **a)** The LB has separate interfaces on each network: 172.21.0.10 on frontend, 172.20.0.10 on backend [Echilibratorul are interfețe separate pe fiecare rețea: 172.21.0.10 pe frontend, 172.20.0.10 pe backend]
- **b)** The X-Forwarded-For header preserves the original client IP address as the request passes through each proxy layer in the reverse proxy forwarding chain [Antetul X-Forwarded-For păstrează adresa IP originală a clientului pe măsură ce cererea traversează fiecare strat de proxy din lanțul de redirecționare al proxy-ului invers]
- **c)** Docker automatically assigns random source IPs per outgoing connection from containers [Docker atribuie automat IP-uri sursă aleatorii per conexiune de ieșire din containere]
- **d)** The capture contains an error; the same IP should appear in both connection traces [Captura conține o eroare; același IP ar trebui să apară în ambele trasări de conexiune]

<details><summary>💡 Feedback</summary>

The LB container is multi-homed: connected to frontend_net (172.21.0.10) and backend_net (172.20.0.10). Traffic to backends uses the backend interface IP as source. [Containerul echilibratorului este multi-homed: conectat la frontend_net (172.21.0.10) și backend_net (172.20.0.10). Traficul către backend-uri folosește IP-ul interfeței backend ca sursă.]

</details>

---

### Q25. `N14.T00.Q07`
**Scenario: Echo Server Message Integrity / Scenariu: Integritatea mesajelor serverului echo**

*Multiple Choice*

> A student sends a 4096-byte message to the echo server and receives only 2048 bytes back. The socket code uses recv(4096) once. Why? [Un student trimite un mesaj de 4096 de octeți la serverul echo și primește înapoi doar 2048 de octeți. Codul socket folosește recv(4096) o singură dată. De ce?]

- **a)** TCP is a byte stream; recv() may return less than the requested amount in a single call [TCP este un flux de octeți; recv() poate returna mai puțin decât cantitatea cerută într-un singur apel]
- **b)** The echo server has a 2048-byte internal buffer size limit that truncates all messages [Serverul echo are o limită internă de 2048 octeți care trunchiază toate mesajele]
- **c)** Network congestion dropped half of the TCP segments during transmission [Congestia rețelei a eliminat jumătate din segmentele TCP în timpul transmisiei]
- **d)** The operating system kernel enforces a hard limit on socket receive buffers, capping them at exactly 2048 bytes per call [Nucleul sistemului de operare impune o limită strictă pentru bufferele de primire socket, plafonându-le la exact 2048 de octeți per apel]

<details><summary>💡 Feedback</summary>

TCP does not preserve message boundaries. recv(N) returns up to N bytes, potentially requiring multiple calls. The echo server uses recv(4096) in a loop, but the client should also loop. [TCP nu păstrează granițele mesajelor. recv(N) returnează până la N octeți, necesitând potențial apeluri multiple. Serverul echo folosește recv(4096) într-o buclă, dar și clientul ar trebui să folosească o buclă.]

</details>

---

### Q26. `N14.T00.Q10`
**Scenario: Verify Test Design Strategy / Scenariu: Strategia de proiectare a verificării**

*Multiple Choice*

> You are designing a verification harness for the Week 14 lab. The most reliable strategy to confirm round-robin distribution is: [Proiectați un harness de verificare pentru laboratorul din săptămâna 14. Strategia cea mai fiabilă pentru a confirma distribuția round-robin este:]

- **a)** Send N requests, parse the X-Backend header from each response, and verify the alternating A-B-A-B pattern [Trimiteți N cereri, analizați antetul X-Backend din fiecare răspuns și verificați modelul alternant A-B-A-B]
- **b)** Send one request and check that the response comes from app1 as the first backend [Trimiteți o cerere și verificați că răspunsul vine de la app1 ca prim backend]
- **c)** Compare response times between requests to determine which backend is faster [Comparați timpii de răspuns între cereri pentru a determina care backend este mai rapid]
- **d)** Testing a single request is insufficient because it cannot verify the round-robin distribution pattern; a proper verification harness must send multiple sequential requests and check the X-Backend header varies [Testarea unei singure cereri este insuficientă deoarece nu poate verifica modelul de distribuție round-robin; un harness de verificare adecvat trebuie să trimită multiple cereri secvențiale și să verifice că antetul X-Backend variază]

<details><summary>💡 Feedback</summary>

The X-Backend header provides definitive proof of which backend handled each request. Multiple requests reveal the distribution pattern. This is exactly what http_client.py implements. [Antetul X-Backend oferă dovada definitivă a backend-ului care a gestionat fiecare cerere. Cereri multiple dezvăluie modelul de distribuție. Aceasta este exact ceea ce implementează http_client.py.]

</details>

---

### Q27. `N14.T00.Q12`
**Scenario: Designing a Monitoring Dashboard / Scenariu: Proiectarea unui tablou de bord de monitorizare**

*Multiple Choice*

> To build a real-time monitoring tool for the Week 14 setup, which combination of endpoints and commands provides the most comprehensive view? [Pentru a construi un instrument de monitorizare în timp real pentru configurația din săptămâna 14, ce combinație de endpoint-uri și comenzi oferă viziunea cea mai cuprinzătoare?]

- **a)** Poll /lb-status for backend stats, /health on each backend directly, and docker stats for resource usage [Interogați /lb-status pentru statistici backend, /health pe fiecare backend direct, și docker stats pentru utilizarea resurselor]
- **b)** Implement periodic HTTP health checks to the /health endpoint at configurable intervals, combined with automated log analysis and threshold-based alerting when backend response times exceed acceptable limits [Implementați verificări periodice HTTP de sănătate la endpoint-ul /health la intervale configurabile, combinate cu analiza automată a jurnalelor și alertare bazată pe praguri când timpii de răspuns ai backend-urilor depășesc limitele acceptabile]
- **c)** Run docker ps in a loop and parse the STATUS column for health indicators continuously [Executați docker ps într-o buclă și analizați coloana STATUS pentru indicatori de sănătate continuu]
- **d)** Use Wireshark continuous capture and parse PCAP files to extract service availability data [Folosiți captură continuă Wireshark și analizați fișierele PCAP pentru a extrage date de disponibilitate]

<details><summary>💡 Feedback</summary>

Comprehensive monitoring requires multiple data sources: /lb-status for traffic distribution, /health for individual service liveness, and docker stats for system-level metrics (CPU, memory, network). [Monitorizarea cuprinzătoare necesită surse multiple de date: /lb-status pentru distribuția traficului, /health pentru viabilitatea serviciilor individuale, și docker stats pentru metrici la nivel de sistem (CPU, memorie, rețea).]

</details>

---

### Q28. `N14.C02.Q06`
**Connection Refused vs Timeout / Connection Refused vs Timeout**

*Multiple Choice*

> A student runs nc -zv localhost 9999 and receives 'Connection refused'. What can they definitively conclude? [Un student execută nc -zv localhost 9999 și primește 'Connection refused'. Ce poate concluziona cu certitudine?]

- **a)** The host is reachable but no service listens on port 9999 [Gazda este accesibilă, dar niciun serviciu nu ascultă pe portul 9999]
- **b)** A firewall rule is actively blocking TCP traffic to port 9999 [O regulă de firewall blochează activ traficul TCP către portul 9999]
- **c)** The network path between client and server is completely broken [Calea de rețea între client și server este complet întreruptă]
- **d)** The DNS resolution failed and the hostname could not be resolved [Rezoluția DNS a eșuat și numele gazdei nu a putut fi rezolvat]

<details><summary>💡 Feedback</summary>

'Connection refused' means a TCP RST was received, confirming network reachability. Firewall blocking would cause timeout, not refusal. DNS failure produces a different error message. ['Connection refused' înseamnă că s-a primit un TCP RST, confirmând accesibilitatea rețelei. Blocarea de firewall ar cauza timeout, nu refuz. Eșecul DNS produce un mesaj de eroare diferit.]

</details>

---

### Q29. `N14.T00.Q09`
**Scenario: Multi-Layer Packet Identification / Scenariu: Identificarea pachetelor multi-strat**

*Multiple Choice*

> In a Wireshark capture of curl http://localhost:8080/, you examine a single HTTP GET packet. This packet simultaneously contains headers from which layers? [Într-o captură Wireshark a curl http://localhost:8080/, examinați un singur pachet HTTP GET. Acest pachet conține simultan antete de la ce straturi?]

- **a)** Data Link (Ethernet), Network (IP), Transport (TCP), and Application (HTTP) — encapsulation is visible [Legătura de date (Ethernet), Rețea (IP), Transport (TCP) și Aplicație (HTTP) — încapsularea este vizibilă]
- **b)** The Layer 2 frame contains the Ethernet header with MAC addresses for local delivery, the Layer 3 packet carries the IP header with source and destination addresses, and the Layer 4 segment holds TCP ports [Cadrul Layer 2 conține antetul Ethernet cu adrese MAC pentru livrare locală, pachetul Layer 3 transportă antetul IP cu adresele sursă și destinație, iar segmentul Layer 4 deține porturile TCP]
- **c)** Network and Transport only — Ethernet headers are removed by the network interface [Doar Rețea și Transport — antetele Ethernet sunt eliminate de interfața de rețea]
- **d)** Transport and Application only — IP headers are consumed by the operating system [Doar Transport și Aplicație — antetele IP sunt consumate de sistemul de operare]

<details><summary>💡 Feedback</summary>

Wireshark captures complete frames including all encapsulation layers. An HTTP packet contains Ethernet + IP + TCP + HTTP headers, demonstrating the full encapsulation stack. [Wireshark capturează cadre complete incluzând toate straturile de încapsulare. Un pachet HTTP conține antete Ethernet + IP + TCP + HTTP, demonstrând stiva completă de încapsulare.]

</details>

---

### Q30. `N14.T00.Q11`
**Scenario: localhost vs 127.0.0.1 Issue / Scenariu: Problema localhost vs 127.0.0.1**

*Multiple Choice*

> A student's Python script connects to ('localhost', 8080) and fails, but connecting to ('127.0.0.1', 8080) works. The most likely explanation is: [Scriptul Python al unui student se conectează la ('localhost', 8080) și eșuează, dar conectarea la ('127.0.0.1', 8080) funcționează. Explicația cea mai probabilă este:]

- **a)** localhost resolves to IPv6 ::1 on this system, but the service listens only on IPv4 127.0.0.1 [localhost se rezolvă la IPv6 ::1 pe acest sistem, dar serviciul ascultă doar pe IPv4 127.0.0.1]
- **b)** The service requires authentication and localhost is not in the allowed hosts list [Serviciul necesită autentificare și localhost nu este în lista gazdelor permise]
- **c)** DNS is not working correctly and cannot resolve the localhost hostname to any IP [DNS nu funcționează corect și nu poate rezolva numele de gazdă localhost la niciun IP]
- **d)** Port 8080 is blocked by the firewall for hostname-based connections but explicitly allowed for direct IP address connections [Portul 8080 este blocat de firewall pentru conexiuni bazate pe nume de gazdă, dar permis explicit pentru conexiuni directe prin adresă IP]

<details><summary>💡 Feedback</summary>

localhost resolution depends on /etc/hosts and system config. If it resolves to ::1 (IPv6) but the server binds only to 127.0.0.1 (IPv4), the connection fails. Using 127.0.0.1 explicitly forces IPv4. [Rezoluția localhost depinde de /etc/hosts și configurația sistemului. Dacă se rezolvă la ::1 (IPv6) dar serverul se leagă doar la 127.0.0.1 (IPv4), conexiunea eșuează. Folosirea explicită a 127.0.0.1 forțează IPv4.]

</details>

---

### Q31. `N14.C02.Q04`
**RST Flag After SYN Meaning / Semnificația RST după SYN**

*Multiple Choice*

> In a Wireshark capture you observe a TCP RST packet sent from a server immediately after a client's SYN. What does this indicate? [Într-o captură Wireshark observați un pachet TCP RST trimis de server imediat după SYN-ul clientului. Ce indică acest lucru?]

- **a)** No service is listening on the destination port; the connection is refused [Niciun serviciu nu ascultă pe portul destinație; conexiunea este refuzată]
- **b)** The connection was established and then immediately terminated by the server application due to resource exhaustion [Conexiunea a fost stabilită și apoi terminată imediat de aplicația server din cauza epuizării resurselor]
- **c)** The connection was established and is now being gracefully terminated [Conexiunea a fost stabilită și este acum terminată grațios]
- **d)** The server acknowledges the SYN and requests a data retransmission [Serverul confirmă SYN-ul și solicită o retransmisie de date]

<details><summary>💡 Feedback</summary>

TCP RST in response to SYN means no service listens on that port, producing 'Connection refused'. Firewall blocking causes timeout (no response at all). Receiving RST confirms the host is reachable. [TCP RST ca răspuns la SYN înseamnă că niciun serviciu nu ascultă pe acel port, producând eroarea 'Connection refused'. Blocarea de firewall cauzează timeout (niciun răspuns). Primirea RST confirmă că gazda este accesibilă.]

</details>

---

### Q32. `N14.T00.Q02`
**Scenario: Wireshark Packet Analysis / Scenariu: Analiza pachetelor Wireshark**

*Multiple Choice*

> You capture 30 seconds of traffic and apply tcp.flags.syn == 1 && tcp.flags.ack == 0. You see 10 packets. What can you conclude? [Capturați 30 de secunde de trafic și aplicați tcp.flags.syn == 1 && tcp.flags.ack == 0. Vedeți 10 pachete. Ce puteți concluziona?]

- **a)** 10 new TCP connections were initiated during the capture period [10 conexiuni TCP noi au fost inițiate în perioada de captură]
- **b)** 10 HTTP requests were completed successfully through the load balancer [10 cereri HTTP au fost completate cu succes prin echilibratorul de sarcină]
- **c)** 10 packets were dropped by the firewall before reaching any destination [10 pachete au fost eliminate de firewall înainte de a ajunge la orice destinație]
- **d)** The network experienced 10 connection errors and all were retransmitted [Rețeaua a experimentat 10 erori de conexiune și toate au fost retransmise]

<details><summary>💡 Feedback</summary>

SYN-only packets (SYN=1, ACK=0) represent the first packet of each new TCP connection. 10 such packets = 10 connection attempts. Each may carry multiple HTTP requests via keep-alive. [Pachetele doar SYN (SYN=1, ACK=0) reprezintă primul pachet al fiecărei conexiuni TCP noi. 10 astfel de pachete = 10 încercări de conexiune. Fiecare poate transporta mai multe cereri HTTP prin keep-alive.]

</details>

---

## 📚 W14 — Laborator / Lab   (22 questions)

---

### Q33. `N14.S01.Q01`
**Docker Port Mapping Format / Formatul mapării porturilor Docker**

*Multiple Choice*

> In the Week 14 docker-compose.yml, the line "8002:8001" under app2 ports means what? [În docker-compose.yml din săptămâna 14, linia "8002:8001" sub porturile app2 înseamnă ce?]

- **a)** Host port 8002 forwards to container port 8001 (HOST:CONTAINER format) [Portul gazdă 8002 redirecționează către portul container 8001 (formatul HOST:CONTAINER)]
- **b)** Container port 8002 forwards to host port 8001 (CONTAINER:HOST format) [Portul container 8002 redirecționează către portul gazdă 8001 (formatul CONTAINER:HOST)]
- **c)** Both the host and container listen on port 8002 for incoming connections [Atât gazda, cât și containerul ascultă pe portul 8002 pentru conexiuni de intrare]
- **d)** A TCP tunnel is established between port 8002 and port 8001 bidirectionally [Un tunel TCP este stabilit între portul 8002 și portul 8001 bidirecțional]

<details><summary>💡 Feedback</summary>

Docker port mapping uses HOST:CONTAINER format. In Week 14, app2 internally listens on port 8001 but is accessible from the host at port 8002. [Maparea porturilor Docker folosește formatul HOST:CONTAINER. În săptămâna 14, app2 ascultă intern pe portul 8001, dar este accesibil de la gazdă pe portul 8002.]

</details>

---

### Q34. `N14.S01.Q02`
**Docker Network Isolation / Izolarea rețelei Docker**

*Multiple Choice*

> The Week 14 client container is only on frontend_net (172.21.0.0/24). Can it directly ping app1 at 172.20.0.2 on backend_net? [Containerul client din săptămâna 14 este doar pe frontend_net (172.21.0.0/24). Poate face ping direct la app1 pe 172.20.0.2 din backend_net?]

- **a)** No — containers on different Docker networks cannot communicate directly [Nu — containerele pe rețele Docker diferite nu pot comunica direct]
- **b)** Yes — all Docker containers share a global routing table by default [Da — toate containerele Docker partajează implicit un tabel de rutare global]
- **c)** Yes — but only if promiscuous mode is enabled on the bridge interface [Da — dar doar dacă modul promiscuu este activat pe interfața bridge]
- **d)** No — but the reason is that ICMP is disabled inside Docker by default [Nu — dar motivul este că ICMP este dezactivat implicit în Docker]

<details><summary>💡 Feedback</summary>

Docker networks provide isolation. The client reaches app1 only through the load balancer (lb), which is connected to both frontend_net and backend_net. [Rețelele Docker asigură izolarea. Clientul ajunge la app1 doar prin echilibratorul de sarcină (lb), care este conectat atât la frontend_net, cât și la backend_net.]

</details>

---

### Q35. `N14.S01.Q03`
**Listing Running Containers / Listarea containerelor active**

*Multiple Choice*

> Which command shows only the Week 14 running containers with their status and ports? [Ce comandă afișează doar containerele active din săptămâna 14 cu starea și porturile lor?]

- **a)** docker ps — lists all currently running containers with their names, status, port mappings and image information in a formatted table [listează toate containerele active cu numele, starea, mapările de porturi și informațiile despre imagine într-un tabel formatat]
- **b)** docker ps -a — shows all containers including stopped ones, not filtered [docker ps -a — afișează toate containerele inclusiv cele oprite, nefiltrat]
- **c)** docker images | grep week14 — lists images, not running containers [docker images | grep week14 — listează imaginile, nu containerele active]
- **d)** docker network inspect week14_backend_net — shows network details only [docker network inspect week14_backend_net — afișează doar detaliile rețelei]

<details><summary>💡 Feedback</summary>

The --filter flag narrows docker ps output. Using name=week14 shows only containers whose names match the prefix, with their status and port mappings. [Fanionul --filter restrânge rezultatul docker ps. Folosind name=week14 se afișează doar containerele ale căror nume corespund prefixului, cu starea și mapările de porturi.]

</details>

---

### Q36. `N14.S01.Q04`
**Container Running Equals Service Working / Container activ = serviciu funcțional**

*True / False*

> If docker ps shows a container with status 'Up', the service inside is guaranteed to be working correctly. [Dacă docker ps afișează un container cu starea 'Up', serviciul din interior este garantat să funcționeze corect.]

- **a)** true
- **b)** false

<details><summary>💡 Feedback</summary>

docker ps confirms the container process is running, not that the application is healthy. Always verify with: docker logs, curl to health endpoint, or Docker HEALTHCHECK. [docker ps confirmă că procesul containerului este activ, nu că aplicația este sănătoasă. Verificați întotdeauna cu: docker logs, curl la endpoint-ul de sănătate sau HEALTHCHECK Docker.]

</details>

---

### Q37. `N14.S01.Q05`
**Docker Compose Down vs Stop / Docker Compose Down vs Stop**

*Multiple Choice*

> What is the difference between docker compose down and docker compose stop? [Care este diferența între docker compose down și docker compose stop?]

- **a)** down removes containers and networks; stop only halts the containers without removing them [down elimină containerele și rețelele; stop doar oprește containerele fără a le elimina]
- **b)** down stops containers; stop removes them completely from Docker along with images [down oprește containerele; stop le elimină complet din Docker împreună cu imaginile]
- **c)** Both commands are identical aliases that stop all running containers gracefully [Ambele comenzi sunt alias-uri identice care opresc toate containerele active grațios]
- **d)** docker compose stop halts all containers without removing them or their associated network configurations from the system [docker compose stop oprește toate containerele fără a le elimina pe ele sau configurațiile lor de rețea asociate din sistem]

<details><summary>💡 Feedback</summary>

docker compose stop pauses containers (preserving state), while docker compose down stops and removes containers and associated networks. Adding -v also removes volumes. [docker compose stop pune în pauză containerele (păstrând starea), în timp ce docker compose down oprește și elimină containerele și rețelele asociate. Adăugarea -v elimină și volumele.]

</details>

---

### Q38. `N14.S02.Q04`
**tshark Conversation Statistics / Statisticile conversațiilor tshark**

*Multiple Choice*

> Which tshark command generates TCP conversation statistics from a capture file? [Ce comandă tshark generează statistici ale conversațiilor TCP dintr-un fișier de captură?]

- **a)** tshark -r capture.pcap -q -z conv,tcp — produces a statistical summary table of all TCP conversations captured in the file [produce un tabel sumar statistic cu toate conversațiile TCP capturate în fișier]
- **b)** tshark -r capture.pcap -Y http.request — filters HTTP requests only [tshark -r capture.pcap -Y http.request — filtrează doar cererile HTTP]
- **c)** tshark -r capture.pcap -q -z io,phs — displays protocol hierarchy distribution statistics across all captured frames, not individual conversation summaries [tshark -r capture.pcap -q -z io,phs — afișează statisticile distribuției ierarhiei de protocoale din toate cadrele capturate, nu rezumate ale conversațiilor individuale]
- **d)** tshark -i any -w output.pcap — captures live traffic to a new file [tshark -i any -w output.pcap — capturează trafic live într-un fișier nou]

<details><summary>💡 Feedback</summary>

The -z conv,tcp flag generates conversation statistics for TCP. The -q flag suppresses per-packet output, showing only the summary. [Fanionul -z conv,tcp generează statistici ale conversațiilor TCP. Fanionul -q suprimă afișarea per-pachet, arătând doar sumarul.]

</details>

---

### Q39. `N14.S02.Q05`
**Wireshark Filter for Backend Traffic / Filtru Wireshark pentru traficul backend**

*Multiple Choice*

> To see traffic to/from both Week 14 backends in Wireshark, which display filter is correct? [Pentru a vedea traficul către/de la ambele backend-uri din săptămâna 14 în Wireshark, care filtru de afișare este corect?]

- **a)** ip.addr == 172.20.0.2 || ip.addr == 172.20.0.3 — this Wireshark display filter matches packets to or from either backend server address [acest filtru de afișare Wireshark se potrivește pachetelor către sau de la oricare adresă de server backend]
- **b)** ip.addr == 172.21.0.2 — filters only client traffic on frontend network [ip.addr == 172.21.0.2 — filtrează doar traficul clientului pe rețeaua frontend]
- **c)** tcp.port == 9090 — filters TCP echo server traffic instead of HTTP backends [tcp.port == 9090 — filtrează traficul serverului TCP echo în loc de backend-urile HTTP]
- **d)** http contains X-Backend — shows only responses with that header, not all traffic [http contains X-Backend — arată doar răspunsurile cu acel antet, nu tot traficul]

<details><summary>💡 Feedback</summary>

Backend app1 is at 172.20.0.2 and app2 at 172.20.0.3 on the backend_net. The || operator combines both addresses in a single display filter. [Backend-ul app1 este la 172.20.0.2 și app2 la 172.20.0.3 pe backend_net. Operatorul || combină ambele adrese într-un singur filtru de afișare.]

</details>

---

### Q40. `N14.S03.Q01`
**Diagnosing 502 Errors / Diagnosticarea erorilor 502**

*Multiple Choice*

> The load balancer returns intermittent 502 errors. The first diagnostic step should be: [Echilibratorul de sarcină returnează erori 502 intermitente. Primul pas de diagnosticare ar trebui să fie:]

- **a)** Check if both backends are running with docker ps --filter name=week14_app [Verificați dacă ambele backend-uri sunt active cu docker ps --filter name=week14_app]
- **b)** Immediately restart the load balancer container to clear its internal error state [Reporniți imediat containerul echilibratorului de sarcină pentru a-i curăța starea de eroare internă]
- **c)** Reinstall Docker completely and rebuild all Week 14 images from the Dockerfile [Reinstalați Docker complet și reconstruiți toate imaginile din săptămâna 14 din Dockerfile]
- **d)** Restart the relevant service (e.g., the reverse proxy or backend) and re-check logs before changing configuration. [Reporniți serviciul relevant (de ex., proxy-ul invers sau backend-ul) și verificați logurile înainte de a schimba configurația.]

<details><summary>💡 Feedback</summary>

Systematic troubleshooting starts with identifying which component is failing. Since 502 means a backend error, checking backend container status is the logical first step. [Depanarea sistematică începe cu identificarea componentei care eșuează. Deoarece 502 înseamnă o eroare backend, verificarea stării containerelor backend este primul pas logic.]

</details>

---

### Q41. `N14.S03.Q02`
**Docker Logs for Debugging / Logurile Docker pentru depanare**

*Multiple Choice*

> To view the last 50 log lines from the load balancer container in real-time, which command is correct? [Pentru a vizualiza ultimele 50 de linii de log de la containerul echilibratorului de sarcină în timp real, care comandă este corectă?]

- **a)** docker logs week14_lb — displays the load balancer container output showing proxy routing decisions, backend selections and error messages [afișează ieșirea containerului echilibratorului arătând deciziile de rutare proxy, selecțiile backend și mesajele de eroare]
- **b)** docker logs week14_lb > lb.log — redirects to file, no real-time following [docker logs week14_lb > lb.log — redirecționează în fișier, fără urmărire în timp real]
- **c)** docker inspect week14_lb — shows container config, not application logs [docker inspect week14_lb — afișează configurația containerului, nu logurile aplicației]
- **d)** docker exec week14_lb cat /var/log/syslog — checks system log, not app output [docker exec week14_lb cat /var/log/syslog — verifică logul de sistem, nu output-ul aplicației]

<details><summary>💡 Feedback</summary>

The -f flag follows the log output in real time (like tail -f). The --tail N flag limits initial output to the last N lines. Both combined provide real-time monitoring with reasonable context. [Fanionul -f urmărește output-ul logului în timp real (precum tail -f). Fanionul --tail N limitează output-ul inițial la ultimele N linii. Ambele combinate asigură monitorizare în timp real cu context rezonabil.]

</details>

---

### Q42. `N14.S03.Q03`
**Testing Backend Health Directly / Testarea directă a sănătății backend-ului**

*Multiple Choice*

> To verify that backend app1 is responding correctly, bypassing the load balancer, which curl command is appropriate? [Pentru a verifica că backend-ul app1 răspunde corect, ocolind echilibratorul de sarcină, care comandă curl este adecvată?]

- **a)** curl http://localhost:8001/health — sends a direct GET request to Backend 1 bypassing the load balancer, confirming backend availability independently [trimite o cerere GET directă către Backend 1 ocolind echilibratorul, confirmând disponibilitatea backend-ului independent]
- **b)** curl http://localhost:8080/health — goes through the load balancer, not direct [curl http://localhost:8080/health — trece prin echilibratorul de sarcină, nu direct]
- **c)** curl http://172.20.0.2:8001/health — container IP unreachable from host directly [curl http://172.20.0.2:8001/health — IP-ul containerului inaccesibil direct de la gazdă]
- **d)** curl http://localhost:9090/health — connects to the TCP echo server instead [curl http://localhost:9090/health — se conectează la serverul TCP echo în schimb]

<details><summary>💡 Feedback</summary>

Port 8001 is mapped directly to app1 (8001:8001). Port 8002 maps to app2 (8002:8001). Using these host ports bypasses the load balancer for direct testing. [Portul 8001 este mapat direct la app1 (8001:8001). Portul 8002 se mapează la app2 (8002:8001). Folosirea acestor porturi gazdă ocolește echilibratorul de sarcină pentru testare directă.]

</details>

---

### Q43. `N14.S03.Q04`
**Port Conflict Resolution / Rezolvarea conflictelor de porturi**

*Multiple Choice*

> A container fails to start with 'address already in use' on port 8080. What diagnostic command identifies the conflicting process? [Un container nu reușește să pornească cu 'address already in use' pe portul 8080. Ce comandă de diagnosticare identifică procesul conflictual?]

- **a)** netstat -tlnp | grep  or ss -tlnp | grep  — identifies the process occupying a specific port, showing PID and program name for resolution [identifică procesul care ocupă un port specific, afișând PID-ul și numele programului pentru rezolvare]
- **b)** docker ps | grep 8080 — shows Docker containers but not non-Docker processes [docker ps | grep 8080 — afișează containerele Docker, dar nu procesele non-Docker]
- **c)** ping localhost — tests network connectivity, irrelevant to port conflicts [ping localhost — testează conectivitatea rețelei, irelevant pentru conflictele de porturi]
- **d)** docker network ls — lists Docker networks, unrelated to port binding issues [docker network ls — listează rețelele Docker, fără legătură cu problemele de legare a porturilor]

<details><summary>💡 Feedback</summary>

ss -tlnp shows all TCP listening sockets with process names. Grep for the specific port reveals which process (Docker or otherwise) is already bound to it. [ss -tlnp afișează toate socket-urile TCP care ascultă cu numele proceselor. Grep pentru portul specific dezvăluie ce proces (Docker sau altul) este deja legat de acesta.]

</details>

---

### Q44. `N14.S03.Q05`
**Wireshark Shows All Network Traffic / Wireshark arată tot traficul de rețea**

*True / False*

> Wireshark captures all network traffic occurring on the entire network, regardless of the selected interface. [Wireshark capturează tot traficul de rețea care are loc în întreaga rețea, indiferent de interfața selectată.]

- **a)** true
- **b)** false

<details><summary>💡 Feedback</summary>

Wireshark captures what the selected interface sees. On modern switched networks, this means only traffic to/from your machine or broadcast/multicast. Encrypted HTTPS payloads are also not readable. [Wireshark capturează ceea ce vede interfața selectată. Pe rețelele moderne cu switch-uri, aceasta înseamnă doar traficul către/de la mașina proprie sau broadcast/multicast. Sarcinile utile HTTPS criptate nu sunt nici ele citibile.]

</details>

---

### Q45. `N14.S04.Q01`
**Failover Behaviour After Backend Stop / Comportamentul de failover după oprirea backend-ului**

*Multiple Choice*

> In the Week 14 failover demo, after docker stop week14_app1, what happens to subsequent requests? [În demonstrația de failover din săptămâna 14, după docker stop week14_app1, ce se întâmplă cu cererile ulterioare?]

- **a)** After the health check detects the failure, all requests route to app2 only [După ce verificarea de sănătate detectează eșecul, toate cererile sunt direcționate doar către app2]
- **b)** All requests immediately fail with 502 until app1 is restarted manually [Toate cererile eșuează imediat cu 502 până când app1 este repornit manual]
- **c)** The load balancer restarts app1 automatically and resumes normal distribution [Echilibratorul de sarcină repornește app1 automat și reia distribuția normală]
- **d)** The load balancer detects the failure within one health check interval and automatically reroutes all subsequent client requests to the surviving backend [Echilibratorul detectează defecțiunea în cadrul unui interval de verificare a sănătății și redirecționează automat toate cererile ulterioare către backend-ul supraviețuitor]

<details><summary>💡 Feedback</summary>

The LB detects the failure through health checks (after up to 3 consecutive failures). During detection, some 502 errors may occur. Once marked unhealthy, all traffic goes to remaining healthy backends. [Echilibratorul detectează eșecul prin verificări de sănătate (după până la 3 eșecuri consecutive). În timpul detectării, pot apărea unele erori 502. Odată marcat ca nesănătos, tot traficul merge către backend-urile sănătoase rămase.]

</details>

---

### Q46. `N14.S04.Q02`
**Distinguishing Error Types / Distingerea tipurilor de erori**

*Multiple Choice*

> A student encounters 'Connection timed out' when trying curl http://10.255.255.1:8080/. What does this most likely indicate? [Un student întâlnește 'Connection timed out' când încearcă curl http://10.255.255.1:8080/. Ce indică cel mai probabil acest lucru?]

- **a)** The network path to the destination is broken — packets are lost or blocked by a firewall [Calea de rețea către destinație este întreruptă — pachetele sunt pierdute sau blocate de un firewall]
- **b)** Connection timeout indicates the network path is blocked by a firewall or the destination host is unreachable, meaning no TCP RST is received and the client waits until the timer expires [Timeout-ul conexiunii indică faptul că ruta de rețea este blocată de un firewall sau gazda destinație este inaccesibilă, adică nu se primește TCP RST și clientul așteaptă până expiră cronometrul]
- **c)** DNS resolution failed for the IP address 10.255.255.1 [Rezoluția DNS a eșuat pentru adresa IP 10.255.255.1]
- **d)** The server actively refused the connection by sending a TCP RST packet [Serverul a refuzat activ conexiunea trimițând un pachet TCP RST]

<details><summary>💡 Feedback</summary>

Timeout means no response was received at all. The network path is unavailable (firewall, routing issue, or unreachable host). 'Connection refused' would indicate the host is reachable but no service listens. [Timeout înseamnă că nu s-a primit niciun răspuns. Calea de rețea este indisponibilă (firewall, problemă de rutare sau gazdă inaccesibilă). 'Connection refused' ar indica că gazda este accesibilă, dar niciun serviciu nu ascultă.]

</details>

---

### Q47. `N14.S04.Q03`
**Backend Recovery After Restart / Recuperarea backend-ului după repornire**

*Multiple Choice*

> After restarting a previously stopped backend with docker start week14_app1, what must happen before the LB sends traffic to it again? [După repornirea unui backend oprit anterior cu docker start week14_app1, ce trebuie să se întâmple înainte ca echilibratorul să îi trimită din nou trafic?]

- **a)** The backend must pass a health check; then the LB marks it healthy and includes it in rotation [Backend-ul trebuie să treacă o verificare de sănătate; apoi echilibratorul îl marchează ca sănătos și îl include în rotație]
- **b)** The restarted backend needs to pass three consecutive successful health checks before the load balancer marks it as healthy again and resumes sending traffic to it [Backend-ul repornit trebuie să treacă trei verificări de sănătate consecutive reușite înainte ca echilibratorul să îl marcheze din nou ca sănătos și să reia trimiterea traficului către el]
- **c)** The entire docker-compose stack must be torn down and rebuilt from scratch [Întreaga stivă docker-compose trebuie demontată și reconstruită de la zero]
- **d)** Traffic resumes immediately with no delay once the container process starts [Traficul se reia imediat fără întârziere odată ce procesul containerului pornește]

<details><summary>💡 Feedback</summary>

In lb_proxy.py, a successful response (Backend.mark_success()) resets consecutive_failures to 0 and sets healthy to True. The backend re-enters the round-robin pool at the next selection. [În lb_proxy.py, un răspuns reușit (Backend.mark_success()) resetează consecutive_failures la 0 și setează healthy la True. Backend-ul reintra în grupul round-robin la următoarea selecție.]

</details>

---

### Q48. `N14.S05.Q01`
**RoundRobinBalancer.get_next() with 3 Backends / RoundRobinBalancer.get_next() cu 3 backend-uri**

*Multiple Choice*

> Given lb = RoundRobinBalancer(["app1", "app2", "app3"]), what does the fifth call to lb.get_next() return? [Dat fiind lb = RoundRobinBalancer(["app1", "app2", "app3"]), ce returnează al cincilea apel la lb.get_next()?]

- **a)** "app2" — because index wraps around: calls return app1, app2, app3, app1, app2 ["app2" — deoarece indexul se înfășoară: apelurile returnează app1, app2, app3, app1, app2]
- **b)** "app2" — the modulo operation wraps the index back, causing the second backend in the list to be selected for the sixth sequential call [„app2" — operația modulo readuce indexul la început, determinând selectarea celui de-al doilea backend din listă pentru al șaselea apel secvențial]
- **c)** "app1" — the counter resets to zero after reaching the end of the list ["app1" — contorul se resetează la zero după ce atinge sfârșitul listei]
- **d)** None — an IndexError occurs because the list has only three elements [None — apare un IndexError deoarece lista are doar trei elemente]

<details><summary>💡 Feedback</summary>

The modulo operator (%) wraps the index: 0%3=0(app1), 1%3=1(app2), 2%3=2(app3), 3%3=0(app1), 4%3=1(app2). After 5 calls, lb.index equals 2. [Operatorul modulo (%) înfășoară indexul: 0%3=0(app1), 1%3=1(app2), 2%3=2(app3), 3%3=0(app1), 4%3=1(app2). După 5 apeluri, lb.index este egal cu 2.]

</details>

---

### Q49. `N14.S05.Q02`
**HTTP Response Parser Output / Rezultatul analizatorului de răspuns HTTP**

*Multiple Choice*

> Given the code tracing exercise T2 with input "HTTP/1.1 200 OK\r\nX-Backend: app1\r\n\r\nHello", what is result["headers"]["X-Backend"]? [Dat fiind exercițiul de trasare T2 cu intrarea "HTTP/1.1 200 OK\r\nX-Backend: app1\r\n\r\nHello", care este result["headers"]["X-Backend"]?]

- **a)** "app1" — the header value parsed after the colon-space separator ["app1" — valoarea antetului analizată după separatorul două-puncte-spațiu]
- **b)** "X-Backend: app1" — the entire header line including the key portion ["X-Backend: app1" — întreaga linie de antet inclusiv porțiunea cheie]
- **c)** "200" — the status code from the response status line instead ["200" — codul de stare din linia de stare a răspunsului]
- **d)** KeyError — because the parser does not handle custom X- headers correctly [KeyError — deoarece analizatorul nu gestionează corect antetele personalizate X-]

<details><summary>💡 Feedback</summary>

The parser splits each header line on ": " (colon-space). For "X-Backend: app1", key becomes "X-Backend" and value becomes "app1". [Analizatorul împarte fiecare linie de antet la ": " (două-puncte-spațiu). Pentru "X-Backend: app1", cheia devine "X-Backend" și valoarea devine "app1".]

</details>

---

### Q50. `N14.S05.Q03`
**Socket Connection to Unreachable Host / Conexiune socket către gazdă inaccesibilă**

*Multiple Choice*

> In code tracing exercise T1, calling connect_to_server("10.255.255.1", 80) where the IP is unreachable results in: [În exercițiul de trasare T1, apelul connect_to_server("10.255.255.1", 80) unde IP-ul este inaccesibil rezultă în:]

- **a)** "timeout" — the socket.timeout exception is caught after 5 seconds ["timeout" — excepția socket.timeout este capturată după 5 secunde]
- **b)** "connected" — the connection succeeds despite the unreachable IP address ["connected" — conexiunea reușește în ciuda adresei IP inaccesibile]
- **c)** "refused" — a ConnectionRefusedError is raised by the operating system ["refused" — o excepție ConnectionRefusedError este ridicată de sistemul de operare]
- **d)** "error: Network is unreachable" — an OSError exception occurs immediately ["error: Network is unreachable" — o excepție OSError apare imediat]

<details><summary>💡 Feedback</summary>

An unreachable IP causes no response. With sock.settimeout(5), a socket.timeout exception fires after 5 seconds. The except clause catches it and returns 'timeout'. [Un IP inaccesibil nu cauzează niciun răspuns. Cu sock.settimeout(5), excepția socket.timeout se declanșează după 5 secunde. Clauza except o capturează și returnează 'timeout'.]

</details>

---

### Q51. `N14.S05.Q04`
**Packet Counter analyse_traffic Output / Rezultatul contorului de pachete analyse_traffic**

*Multiple Choice*

> Given the T5 code tracing with 5 packets (3 HTTP on port 80, 1 HTTPS on port 443, 1 UDP/DNS on port 53), what is result["http"]? [Dat fiind trasarea codului T5 cu 5 pachete (3 HTTP pe portul 80, 1 HTTPS pe portul 443, 1 UDP/DNS pe portul 53), care este result["http"]?]

- **a)** result["by_port"][80] equals 3, since three packets in the input list have dst_port=80 and the counter accumulates each occurrence in the dictionary [result["by_port"][80] este egal cu 3, deoarece trei pachete din lista de intrare au dst_port=80 și contorul acumulează fiecare apariție în dicționar]
- **b)** 5 — all packets regardless of protocol type are counted in the HTTP field [5 — toate pachetele indiferent de tipul protocolului sunt numărate în câmpul HTTP]
- **c)** 4 — both HTTP and HTTPS packets are counted together as HTTP traffic [4 — atât pachetele HTTP, cât și HTTPS sunt numărate împreună ca trafic HTTP]
- **d)** 0 — the function only counts TCP and UDP protocols, not application-layer HTTP [0 — funcția numără doar protocoalele TCP și UDP, nu HTTP de la stratul aplicație]

<details><summary>💡 Feedback</summary>

The analyse_traffic function checks pkt.get("http") for each packet. Only packets where this key is truthy increment stats["http"]. The HTTPS packet has http=False. [Funcția analyse_traffic verifică pkt.get("http") pentru fiecare pachet. Doar pachetele unde această cheie este adevărată incrementează stats["http"]. Pachetul HTTPS are http=False.]

</details>

---

### Q52. `N14.S05.Q05`
**Container Health Check Logic / Logica verificării de sănătate a containerului**

*Multiple Choice*

> In code tracing T4, what does check_container("app99") return for a non-existent container? [În trasarea codului T4, ce returnează check_container("app99") pentru un container inexistent?]

- **a)** result1["running"] is True and result1["ip"] is "172.20.0.2" because the container is active and has a network IP assigned by Docker [result1["running"] este True și result1["ip"] este "172.20.0.2" deoarece containerul este activ și are un IP de rețea atribuit de Docker]
- **b)** {"name": "app99", "running": True, "ip": "0.0.0.0"} [{"name": "app99", "running": True, "ip": "0.0.0.0"}]
- **c)** An empty dictionary {} because the function returns early on error [Un dicționar gol {} deoarece funcția returnează devreme la eroare]
- **d)** A subprocess.CalledProcessError exception is raised and not caught [O excepție subprocess.CalledProcessError este ridicată și nu este capturată]

<details><summary>💡 Feedback</summary>

docker ps -q -f name=app99 returns empty stdout (no matching container). The if ps_result.stdout.strip() check is False, so running stays False and ip stays None. [docker ps -q -f name=app99 returnează stdout gol (niciun container corespunzător). Verificarea if ps_result.stdout.strip() este False, deci running rămâne False și ip rămâne None.]

</details>

---

### Q53. `N14.S02.Q02`
**Display Filter for TCP SYN Only / Filtru de afișare pentru doar TCP SYN**

*Multiple Choice*

> Which Wireshark display filter shows only TCP connection initiation packets (initial SYN, not SYN-ACK)? [Ce filtru de afișare Wireshark arată doar pachetele de inițiere a conexiunii TCP (SYN inițial, nu SYN-ACK)?]

- **a)** tcp.flags.syn == 1 && tcp.flags.ack == 0 — isolates only TCP SYN packets that initiate new connections [izolează doar pachetele TCP SYN care inițiază conexiuni noi]
- **b)** tcp.flags.syn == 1 — includes SYN-ACK packets as well [tcp.flags.syn == 1 — include și pachetele SYN-ACK]
- **c)** tcp.port == 80 — filters by port, not by TCP flags at all [tcp.port == 80 — filtrează după port, nu după fanioanele TCP]
- **d)** http.request — shows only application-layer HTTP request messages, not lower-level TCP handshake synchronisation packets [http.request — arată doar mesajele HTTP de la nivelul aplicație, nu pachetele de sincronizare handshake TCP de nivel inferior]

<details><summary>💡 Feedback</summary>

SYN-only packets have SYN=1 and ACK=0. Using tcp.flags.syn == 1 alone also matches SYN-ACK (where both flags are set). The compound filter isolates the initial connection request. [Pachetele doar SYN au SYN=1 și ACK=0. Folosind doar tcp.flags.syn == 1 se potrivesc și SYN-ACK (unde ambele fanioane sunt setate). Filtrul compus izolează cererea inițială de conexiune.]

</details>

---

### Q54. `N14.S02.Q03`
**Capture vs Display Filters / Filtre de captură vs de afișare**

*Multiple Choice*

> What is the key difference between Wireshark capture filters and display filters? [Care este diferența cheie între filtrele de captură și filtrele de afișare Wireshark?]

- **a)** Capture filters use BPF syntax and are applied during recording; display filters use Wireshark syntax and are applied to already-captured data [Filtrele de captură folosesc sintaxa BPF și se aplică în timpul înregistrării; filtrele de afișare folosesc sintaxa Wireshark și se aplică datelor deja capturate]
- **b)** Capture filters use BPF syntax and are applied during packet capture to reduce file size. They run before packets reach the analysis engine, making them efficient for high-volume scenarios but unable to be modified during a live session. [Filtrele de captură folosesc sintaxa BPF și se aplică în timpul capturării pachetelor pentru a reduce dimensiunea fișierului. Rulează înainte ca pachetele să ajungă la motorul de analiză, fiind eficiente pentru scenarii cu volum mare, dar nu pot fi modificate în timpul unei sesiuni active.]
- **c)** Capture filters apply to HTTP traffic only; display filters work with any protocol type [Filtrele de captură se aplică doar traficului HTTP; filtrele de afișare funcționează cu orice tip de protocol]
- **d)** Both filter types use identical syntax but are applied at different stages of analysis [Ambele tipuri de filtre folosesc sintaxă identică, dar se aplică în etape diferite ale analizei]

<details><summary>💡 Feedback</summary>

Capture filters (BPF: 'port 8080') reduce data saved to disk. Display filters ('tcp.port == 8080') filter the view without removing packets. Their syntax differs. [Filtrele de captură (BPF: 'port 8080') reduc datele salvate pe disc. Filtrele de afișare ('tcp.port == 8080') filtrează vizualizarea fără a elimina pachetele. Sintaxa lor diferă.]

</details>

---

## 📚 W14 — Numerical   (9 questions)

---

### Q55. `N14.C01.Q07`
**Usable Hosts in /24 Subnet / Gazde utilizabile în subrețeaua /24**

*Numerical*

> How many usable host IP addresses are available in a /24 subnet (excluding network and broadcast addresses)? The Week 14 lab uses 172.20.0.0/24 for the backend network. [Câte adrese IP de gazdă utilizabile sunt disponibile într-o subrețea /24 (excluzând adresele de rețea și de broadcast)? Laboratorul din săptămâna 14 folosește 172.20.0.0/24 pentru rețeaua backend.]


<details><summary>💡 Feedback</summary>

A /24 subnet has 2^8 = 256 total addresses. Two are reserved: the network address (.0) and the broadcast address (.255), leaving (...) usable host addresses. [O subrețea /24 are 2^8 = 256 de adrese în total. Două sunt rezervate: adresa de rețea (.0) și adresa de broadcast (.255), rămânând (...) de adrese de gazdă utilizabile.]

</details>

---

### Q56. `N14.D03.Q01`
**Week 14 Docker Service Count / Numărul de servicii Docker din săptămâna 14**

*Numerical*

> How many services are defined in the Week 14 docker-compose.yml file? Count all service blocks (app1, app2, lb, client, echo). [Câte servicii sunt definite în fișierul docker-compose.yml al săptămânii 14? Numărați toate blocurile de servicii (app1, app2, lb, client, echo).]


<details><summary>💡 Feedback</summary>

The docker-compose.yml defines exactly (...) services: app1 (backend 1), app2 (backend 2), lb (load balancer / reverse proxy), client (testing container), and echo (TCP echo server). [Fișierul docker-compose.yml definește exact (...) servicii: app1 (backend 1), app2 (backend 2), lb (echilibrator de sarcină / proxy invers), client (container de testare) și echo (server TCP echo).]

</details>

---

### Q57. `N14.D03.Q02`
**TCP Three-Way Handshake Packet Count / Numărul de pachete din handshake-ul TCP**

*Numerical*

> How many packets are exchanged during a TCP three-way handshake? [Câte pachete se schimbă în timpul unui handshake TCP în trei pași?]


<details><summary>💡 Feedback</summary>

SYN, SYN-ACK, ACK = (...) packets. [SYN, SYN-ACK, ACK = (...) pachete.]

</details>

---

### Q58. `N14.D03.Q03`
**TCP Termination Packet Count / Numărul de pachete la terminarea TCP**

*Numerical*

> How many packets are exchanged during a graceful TCP four-way termination? [Câte pachete se schimbă în timpul terminării grațioase TCP în patru pași?]


<details><summary>💡 Feedback</summary>

FIN, ACK, FIN, ACK = (...) packets. [FIN, ACK, FIN, ACK = (...) pachete.]

</details>

---

### Q59. `N14.D03.Q04`
**MAC Address Bit Length / Lungimea în biți a adresei MAC**

*Numerical*

> How many bits does a MAC address contain? [Câți biți conține o adresă MAC?]


<details><summary>💡 Feedback</summary>

MAC addresses are (...) bits (6 bytes). [Adresele MAC au (...) de biți (6 octeți).]

</details>

---

### Q60. `N14.D03.Q05`
**IPv4 Address Bit Length / Lungimea în biți a adresei IPv4**

*Numerical*

> How many bits does an IPv4 address contain? [Câți biți conține o adresă IPv4?]


<details><summary>💡 Feedback</summary>

IPv4 uses (...)-bit addresses. [IPv4 folosește adrese pe (...) de biți.]

</details>

---

### Q61. `N14.D03.Q06`
**Week 14 Backend Container Count / Numărul de containere backend din săptămâna 14**

*Numerical*

> How many backend HTTP server containers are defined in the Week 14 docker-compose.yml? [Câte containere server HTTP backend sunt definite în docker-compose.yml din săptămâna 14?]


<details><summary>💡 Feedback</summary>

Two backends: app1 and app(...). [Două backend-uri: app1 și app(...).]

</details>

---

### Q62. `N14.D03.Q07`
**LB Unhealthy Threshold / Pragul de nesănătos al echilibratorului**

*Numerical*

> After how many consecutive failures does the Week 14 load balancer mark a backend unhealthy? [După câte eșecuri consecutive marchează echilibratorul din săptămâna 14 un backend ca nesănătos?]


<details><summary>💡 Feedback</summary>

Backend.mark_failure() sets healthy=False when consecutive_failures >= (...). [Backend.mark_failure() setează healthy=False când consecutive_failures >= (...).]

</details>

---

### Q63. `N14.D03.Q08`
**Total Distinct Networks in Week 14 / Total rețele distincte în săptămâna 14**

*Numerical*

> How many distinct Docker networks are defined in the Week 14 docker-compose.yml (not counting the default)? [Câte rețele Docker distincte sunt definite în docker-compose.yml din săptămâna 14 (fără cea implicită)?]


<details><summary>💡 Feedback</summary>

Two networks: backend_net (17(...).(...)0.0.0/(...)4) and frontend_net (17(...).(...)1.0.0/(...)4). [Două rețele: backend_net (17(...).(...)0.0.0/(...)4) și frontend_net (17(...).(...)1.0.0/(...)4).]

</details>

---

## 📚 W14 — Drag & Drop   (8 questions)

---

### Q64. `N14.D05.Q01`
**TCP Handshake Sequence / Secvența handshake-ului TCP**

*Drag & Drop into Text*

> Complete the TCP three-way handshake sequence. [Completați secvența handshake-ului TCP în trei pași.]
> Client sends [[1]] → Server replies [[2]] → Client confirms [[3]]

📋 Available choices / Variante disponibile: SYN  |  SYN-ACK  |  ACK  |  FIN  |  RST  |  NACK


<details><summary>💡 Feedback</summary>

The three-way handshake: SYN, SYN-ACK, ACK. [Handshake-ul în trei pași: SYN, SYN-ACK, ACK.]

</details>

---

### Q65. `N14.D05.Q02`
**Docker Port Mapping Syntax / Sintaxa mapării porturilor Docker**

*Drag & Drop into Text*

> Complete the Docker port mapping. [Completați maparea porturilor Docker.]
> -p [[1]]:[[2]] maps from the [[3]] port to the [[4]] port.

📋 Available choices / Variante disponibile: HOST_PORT  |  CONTAINER_PORT  |  host  |  container  |  network  |  bridge


<details><summary>💡 Feedback</summary>

Docker port mapping: -p HOST_PORT:CONTAINER_PORT. [Maparea porturilor Docker: -p HOST_PORT:CONTAINER_PORT.]

</details>

---

### Q66. `N14.D05.Q03`
**curl Command for LB Testing / Comanda curl pentru testarea echilibratorului**

*Drag & Drop into Text*

> Complete the command to test the load balancer. [Completați comanda pentru testarea echilibratorului de sarcină.]

```
[[1]] http://[[2]]:[[3]]/
```

📋 Available choices / Variante disponibile: curl  |  localhost  |  8080  |  wget  |  172.20.0.10  |  9090


<details><summary>💡 Feedback</summary>

curl http://localhost:8080/ accesses the load balancer from the host. [curl http://localhost:8080/ accesează echilibratorul de sarcină de la gazdă.]

</details>

---

### Q67. `N14.D05.Q05`
**Docker Compose Down Command / Comanda Docker Compose Down**

*Drag & Drop into Text*

> Complete the command to stop and remove all Week 14 containers. [Completați comanda pentru oprirea și eliminarea tuturor containerelor din săptămâna 14.]

```
[[1]] [[2]] -f docker/docker-compose.yml [[3]]
```

📋 Available choices / Variante disponibile: docker  |  compose  |  down  |  stop  |  up  |  rm


<details><summary>💡 Feedback</summary>

docker compose -f docker/docker-compose.yml down stops and removes containers and networks. [docker compose -f docker/docker-compose.yml down oprește și elimină containerele și rețelele.]

</details>

---

### Q68. `N14.D05.Q06`
**Encapsulation Order / Ordinea încapsulării**

*Drag & Drop into Text*

> Order the encapsulation from top to bottom of the TCP/IP stack. [Ordonați încapsularea de sus în jos a stivei TCP/IP.]

```
[[1]] → [[2]] → [[3]] → [[4]]
```

📋 Available choices / Variante disponibile: Data  |  Segment  |  Packet  |  Frame  |  Bit  |  Signal


<details><summary>💡 Feedback</summary>

Top-down: Data (Application) → Segment (Transport) → Packet (Network) → Frame (Data Link). [De sus în jos: Date (Aplicație) → Segment (Transport) → Pachet (Rețea) → Cadru (Legătura de date).]

</details>

---

### Q69. `N14.D05.Q08`
**Docker Exec Interactive Shell / Docker Exec Shell interactiv**

*Drag & Drop into Text*

> Complete the command to open an interactive shell in the client container. [Completați comanda pentru deschiderea unui shell interactiv în containerul client.]
> docker [[1]] [[2]] week14_client [[3]]

📋 Available choices / Variante disponibile: exec  |  -it  |  bash  |  run  |  -d  |  sh


<details><summary>💡 Feedback</summary>

docker exec -it week14_client bash opens an interactive terminal inside the container. [docker exec -it week14_client bash deschide un terminal interactiv în container.]

</details>

---

### Q70. `N14.D05.Q04`
**Wireshark Display Filter for HTTP GET / Filtru de afișare Wireshark pentru HTTP GET**

*Drag & Drop into Text*

> Complete the Wireshark display filter. [Completați filtrul de afișare Wireshark.]

```
[[1]].[[2]].[[3]] == "GET"
```

📋 Available choices / Variante disponibile: http  |  request  |  method  |  response  |  port  |  code


<details><summary>💡 Feedback</summary>

http.request.method == "GET" filters HTTP GET requests in Wireshark. [http.request.method == "GET" filtrează cererile HTTP GET în Wireshark.]

</details>

---

### Q71. `N14.D05.Q07`
**tshark Conversation Command / Comanda tshark pentru conversații**

*Drag & Drop into Text*

> Complete the tshark command for TCP conversation statistics. [Completați comanda tshark pentru statisticile conversațiilor TCP.]

```
[[1]] -r capture.pcap -q -z [[2]],[[3]]
```

📋 Available choices / Variante disponibile: tshark  |  conv  |  tcp  |  tcpdump  |  io  |  udp


<details><summary>💡 Feedback</summary>

tshark -r file.pcap -q -z conv,tcp shows TCP conversation statistics. [tshark -r fișier.pcap -q -z conv,tcp afișează statisticile conversațiilor TCP.]

</details>

---

## 📚 W14 — Gap Select   (8 questions)

---

### Q72. `N14.D10.Q01`
**Layer to Address Type / Strat la tip de adresă**

*Gap Select*

> The [[1]] layer uses IP addresses for routing, while the [[2]] layer uses MAC addresses for local delivery. [Stratul de ___ folosește adrese IP pentru rutare, în timp ce stratul ___ folosește adrese MAC pentru livrarea locală.]

📋 Available choices / Variante disponibile: Network  |  Data Link  |  Transport  |  Application


<details><summary>💡 Feedback</summary>

Network (L3) = IP addressing. Data Link (L2) = MAC addressing. [Rețea (L3) = adresare IP. Legătura de date (L2) = adresare MAC.]

</details>

---

### Q73. `N14.D10.Q02`
**TCP Reliability Mechanism / Mecanismul de fiabilitate TCP**

*Gap Select*

> TCP ensures reliable delivery through [[1]] and [[2]]. UDP does not provide these guarantees. [TCP asigură livrarea fiabilă prin ___ și ___. UDP nu oferă aceste garanții.]

📋 Available choices / Variante disponibile: acknowledgements  |  retransmissions  |  encryption  |  compression


<details><summary>💡 Feedback</summary>

TCP reliability: ACKs confirm receipt; lost segments are retransmitted. [Fiabilitatea TCP: ACK-urile confirmă primirea; segmentele pierdute sunt retransmise.]

</details>

---

### Q74. `N14.D10.Q03`
**Docker Compose Service Roles / Rolurile serviciilor Docker Compose**

*Gap Select*

> In Week 14, the [[1]] container distributes HTTP requests, while the [[2]] container provides TCP echo functionality. [În săptămâna 14, containerul ___ distribuie cererile HTTP, iar containerul ___ oferă funcționalitatea TCP echo.]

📋 Available choices / Variante disponibile: lb  |  echo  |  client  |  app1


<details><summary>💡 Feedback</summary>

lb = load balancer (HTTP distribution). echo = TCP echo server. [lb = echilibrator de sarcină (distribuție HTTP). echo = server TCP echo.]

</details>

---

### Q75. `N14.D10.Q04`
**Health Check vs Endpoint / Verificare de sănătate vs endpoint**

*Gap Select*

> The /[[1]] endpoint returns "OK" for health monitoring, while /[[2]] returns JSON with uptime and request statistics. [Endpoint-ul /___ returnează "OK" pentru monitorizarea sănătății, în timp ce /___ returnează JSON cu statistici.]

📋 Available choices / Variante disponibile: health  |  info  |  status  |  lb-status


<details><summary>💡 Feedback</summary>

/health returns simple OK for liveness checks. /info returns detailed JSON. [/health returnează OK simplu pentru verificări de viață. /info returnează JSON detaliat.]

</details>

---

### Q76. `N14.D10.Q05`
**Network Subnet Assignment / Atribuirea subrețelei**

*Gap Select*

> The frontend network uses subnet [[1]] and the backend network uses subnet [[2]]. [Rețeaua frontend folosește subrețeaua ___, iar rețeaua backend folosește subrețeaua ___.]

📋 Available choices / Variante disponibile: 172.21.0.0/24  |  172.20.0.0/24  |  192.168.0.0/24  |  10.0.0.0/24


<details><summary>💡 Feedback</summary>

Frontend: 172.21.0.0/24. Backend: 172.20.0.0/24. [Frontend: 172.21.0.0/24. Backend: 172.20.0.0/24.]

</details>

---

### Q77. `N14.D10.Q07`
**Failover Sequence / Secvența de failover**

*Gap Select*

> When a backend fails, the LB initially returns [[1]] errors until the [[2]] detects the failure. [Când un backend eșuează, echilibratorul returnează inițial erori ___ până când ___ detectează eșecul.]

📋 Available choices / Variante disponibile: 502  |  health check  |  404  |  firewall


<details><summary>💡 Feedback</summary>

502 during detection interval. Health check marks backend unhealthy. [502 în intervalul de detectare. Verificarea de sănătate marchează backend-ul ca nesănătos.]

</details>

---

### Q78. `N14.D10.Q08`
**Port Mapping Direction / Direcția mapării porturilor**

*Gap Select*

> In -p 8002:8001, [[1]] is the host-side port and [[2]] is the container-side port. [În -p 8002:8001, ___ este portul pe partea gazdei, iar ___ este portul pe partea containerului.]

📋 Available choices / Variante disponibile: 8002  |  8001  |  80  |  443


<details><summary>💡 Feedback</summary>

Format: HOST:CONTAINER. 8002 = host, 8001 = container. [Format: HOST:CONTAINER. 8002 = gazdă, 8001 = container.]

</details>

---

### Q79. `N14.D10.Q06`
**Capture vs Display Filter Application / Aplicarea filtrelor de captură vs afișare**

*Gap Select*

> Wireshark [[1]] filters are applied during recording, while [[2]] filters are applied to already-captured data. [Filtrele de ___ Wireshark se aplică în timpul înregistrării, în timp ce filtrele de ___ se aplică datelor deja capturate.]

📋 Available choices / Variante disponibile: capture  |  display  |  protocol  |  packet


<details><summary>💡 Feedback</summary>

Capture filters reduce recorded data. Display filters filter the view post-capture. [Filtrele de captură reduc datele înregistrate. Filtrele de afișare filtrează vizualizarea post-captură.]

</details>

---
