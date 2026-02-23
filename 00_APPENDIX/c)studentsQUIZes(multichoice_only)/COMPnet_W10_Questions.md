# Computer Networks – Week 10

#### Rețele de calculatoare – Săptămâna 10

> Practice Questions / Întrebări de practică

---


## Lecture Questions / Întrebări de curs

### 1. `Multiple Choice – Alegere multiplă`
**N10.C01.Q02: Purpose of asymmetric cryptography in TLS / Rolul criptografiei asimetrice în TLS**

> During a TLS 1.3 handshake, asymmetric cryptography (public/private keys) is used. What is its primary role? [În timpul unui handshake TLS 1.3, se utilizează criptografia asimetrică (chei publice/private). Care este rolul său principal?]

- **a) To authenticate the server and establish a shared symmetric key [Pentru a autentifica serverul și a stabili o cheie simetrică comună]**
- **b) To encrypt all application data between client and server, which is a common but technically inaccurate interpretation of the protocol [Pentru a cripta toate datele aplicației între client și server, ceea ce este o interpretare frecventă dar incorectă din punct de vedere tehnic al protocolului]**
- **c) To compress data before transmission for efficiency [Pentru a comprima datele înainte de transmitere în scopul eficienței]**
- **d) To verify the integrity of each individual packet [Pentru a verifica integritatea fiecărui pachet individual]**

> 💡 **Feedback:** Asymmetric cryptography authenticates the server and facilitates deriving a shared symmetric key. Symmetric encryption (AES, ChaCha20) then handles bulk data because it is roughly 1000× faster. A common misconception is that asymmetric encryption is used for all data transfer, but in reality it is computationally too expensive for bulk encryption and serves only the initial key exchange and authentication. [Criptografia asimetrică autentifică serverul și facilitează derivarea unei chei simetrice comune. Criptarea simetrică (AES, ChaCha20) gestionează apoi datele în masă, fiind de aproximativ 1000 de ori mai rapidă. O concepție greșită frecventă este că criptarea asimetrică este folosită pentru tot transferul de date, dar în realitate este prea costisitoare computațional pentru criptarea în masă și servește doar la schimbul inițial de chei și la autentificare.]

---

### 2. `True/False – Adevărat/Fals`
**N10.C01.Q03: HTTPS guarantees website trustworthiness / HTTPS garantează fiabilitatea unui site web**

> A website displaying the HTTPS padlock icon in the browser guarantees that the website operator is trustworthy and will not misuse user data. [Un site web care afișează iconița lacătului HTTPS în browser garantează că operatorul site-ului este de încredere și nu va utiliza abuziv datele utilizatorilor.]

- **a) True / Adevărat**
- **b) False / Fals**

> 💡 **Feedback:** HTTPS only encrypts the connection in transit and authenticates the server identity via its certificate. It does not guarantee the honesty or integrity of the website operator — phishing sites routinely use valid HTTPS certificates obtained from free certificate authorities such as Let's Encrypt. A common misconception is that the padlock icon signifies overall website safety, when it merely confirms transport-layer criptare. [HTTPS criptează doar conexiunea în tranzit și autentifică identitatea serverului prin certificatul său. Nu garantează onestitatea sau integritatea operatorului site-ului — site-urile de phishing folosesc în mod curent certificate HTTPS valide obținute de la autorități de certificare gratuite precum Let's Encrypt. O concepție greșită frecventă este că iconița lacătului semnifică siguranța generală a site-ului, când de fapt confirmă doar criptarea la nivelul stratului de transport.]

---

### 3. `Multiple Choice – Alegere multiplă`
**N10.C01.Q04: Three security properties provided by TLS / Cele trei proprietăți de securitate oferite de TLS**

> HTTPS wraps HTTP inside TLS. Which set of security properties does TLS provide? [HTTPS încapsulează HTTP în TLS. Ce set de proprietăți de securitate oferă TLS?]

- **a) Authentication, confidentiality, and integrity [Autentificare, confidențialitate și integritate]**
- **b) Authentication, compression, and routing [Autentificare, compresie și rutare]**
- **c) Confidentiality, load balancing, and caching [Confidențialitate, echilibrarea încărcării și memorare în cache]**
- **d) Integrity, anonymity, and non-repudiation [Integritate, anonimat și nerepudiere]**

> 💡 **Feedback:** TLS provides authentication (via X.509 certificates), confidentiality (via symmetric encryption such as AES), and integrity (via MACs — Message Authentication Codes). A common misconception is that TLS also provides anonymity, but TLS does not hide metadata such as connection endpoints or the domain name transmitted via SNI. [TLS oferă autentificare (prin certificate X.509), confidențialitate (prin criptare simetrică precum AES) și integritate (prin MAC-uri — coduri de autentificare a mesajelor). O concepție greșită frecventă este că TLS oferă și anonimat, dar TLS nu ascunde metadatele precum punctele terminale ale conexiunii sau numele de domeniu transmis prin SNI.]

---

### 4. `Multiple Choice – Alegere multiplă`
**N10.C01.Q05: TLS handshake step ordering / Ordinea pașilor handshake-ului TLS**

> Which sequence correctly describes the TLS handshake steps? [Care secvență descrie corect pașii handshake-ului TLS?]

- **a) Client Hello → Server Hello + Certificate → Key Exchange → Encrypted Data [Client Hello → Server Hello + Certificat → Schimb de chei → Date criptate]**
- **b) Key Exchange → Client Hello → Server Hello → Encrypted Data — an assertion that does not align with the actual specification requirements [Schimb de chei → Client Hello → Server Hello → Date criptate — o afirmație ce nu corespunde cerințelor reale ale specificației]**
- **c) Server Hello → Client Hello → Encrypted Data → Key Exchange [Server Hello → Client Hello → Date criptate → Schimb de chei]**
- **d) Client Hello → Encrypted Data → Server Hello → Key Exchange [Client Hello → Date criptate → Server Hello → Schimb de chei]**

> 💡 **Feedback:** The TLS handshake proceeds: Client Hello (offering cipher suites) → Server Hello (choosing cipher suite and sending certificate) → Key exchange (deriving symmetric key) → Encrypted data begins. A common misconception is that encryption starts immediately or that the key exchange occurs before the hello messages, but the hello phase must first negotiate parameters before any cryptographic material is exchanged. [Handshake-ul TLS se desfășoară astfel: Client Hello (propunând suite de cifrare) → Server Hello (alegând suita de cifrare și trimițând certificatul) → Schimb de chei (derivând cheia simetrică) → Încep datele criptate. O concepție greșită frecventă este că criptarea începe imediat sau că schimbul de chei are loc înaintea mesajelor hello, dar faza hello trebuie să negocieze mai întâi parametrii înainte de schimbul oricărui material criptografic.]

---

### 5. `Multiple Choice – Alegere multiplă`
**N10.C01.Q07: What HTTPS encrypts versus what remains visible / Ce criptează HTTPS și ce rămâne vizibil**

> Which of the following is encrypted when using HTTPS? [Care dintre următoarele este criptat(ă) la utilizarea HTTPS?]

- **a) The URL path and HTTP request/response body [Calea URL și corpul cererii/răspunsului HTTP]**
- **b) The destination IP address [Adresa IP de destinație]**
- **c) The domain name sent via SNI [Numele de domeniu trimis prin SNI]**
- **d) The TCP port number used for the connection [Numărul de port TCP folosit pentru conexiune]**

> 💡 **Feedback:** HTTPS encrypts the URL path, query parameters, HTTP headers, and body. The domain name (via SNI) and destination IP address remain visible to network observers. A common misconception is that the destination IP address is encrypted, but IP addresses must be in plaintext for network routing to function. [HTTPS criptează calea URL, parametrii de interogare, antetele HTTP și corpul mesajului. Numele de domeniu (prin SNI) și adresa IP de destinație rămân vizibile observatorilor din rețea. O concepție greșită frecventă este că adresa IP de destinație este criptată, dar adresele IP trebuie să fie în text clar pentru ca rutarea în rețea să funcționeze.]

---

### 6. `True/False – Adevărat/Fals`
**N10.C01.Q08: HTTP/2 specification requires TLS / Specificația HTTP/2 necesită TLS**

> The HTTP/2 specification (RFC 7540) mandates that all HTTP/2 connections must use TLS encryption. [Specificația HTTP/2 (RFC 7540) impune ca toate conexiunile HTTP/2 să utilizeze criptare TLS.]

- **a) True / Adevărat**
- **b) False / Fals**

> 💡 **Feedback:** The HTTP/2 specification supports both encrypted (h2) and cleartext (h2c) modes. However, all major browsers only implement HTTP/2 over TLS — this is a browser policy choice, not a protocol requirement. Server-to-server communication can use h2c without TLS. A common misconception is that the protocol itself mandates encryption, confusing browser implementation policy with protocol specification. [Specificația HTTP/2 acceptă atât modul criptat (h2), cât și modul în text clar (h2c). Cu toate acestea, toate browserele majore implementează HTTP/2 doar prin TLS — aceasta este o decizie de politică a browserului, nu o cerință a protocolului. Comunicarea server-la-server poate folosi h2c fără TLS. O concepție greșită frecventă este că protocolul în sine impune criptarea, confundând politica de implementare a browserelor cu specificația protocolului.]

---

### 7. `True/False – Adevărat/Fals`
**N10.C02.Q01: REST is a protocol / REST este un protocol**

> REST (Representational State Transfer) is a network protocol, similar to HTTP or FTP. [REST (Representational State Transfer) este un protocol de rețea, similar cu HTTP sau FTP.]

- **a) True / Adevărat**
- **b) False / Fals**

> 💡 **Feedback:** REST is an architectural style defining constraints for distributed systems (client-server separation, statelessness, uniform interface, cacheability, layered system), not a protocol. It typically uses HTTP as its transfer protocol. A common misconception is treating REST as a protocol on the same level as HTTP or FTP, when in fact it is a set of design principles that can be implemented over various protocols. [REST este un stil arhitectural care definește constrângeri pentru sistemele distribuite (separarea client-server, lipsa stării, interfața uniformă, posibilitatea de memorare în cache, sistem stratificat), nu un protocol. De obicei folosește HTTP ca protocol de transfer. O concepție greșită frecventă este tratarea REST ca un protocol de același nivel cu HTTP sau FTP, când de fapt este un set de principii de proiectare ce pot fi implementate peste diverse protocoale.]

---

### 8. `Multiple Choice – Alegere multiplă`
**N10.C02.Q02: Identifying Richardson Maturity Level for action-style endpoints / Identificarea nivelului de maturitate Richardson pentru endpoint-uri cu acțiuni în cale**

> An API exposes the endpoint POST /api/users/123/delete. According to the Richardson Maturity Model, which level does this represent? [Un API expune endpoint-ul POST /api/users/123/delete. Conform Modelului de Maturitate Richardson, ce nivel reprezintă?]

- **a) Level 1 — Resources with URIs but action-style naming [Nivelul 1 — Resurse cu URI-uri, dar denumire de tip acțiune]**
- **b) Level 0 — RPC-style single endpoint [Nivelul 0 — Endpoint unic în stil RPC]**
- **c) Level 2 — Proper HTTP verbs with semantic status codes and resource-oriented URIs [Nivelul 2 — Verbe HTTP corecte cu coduri de stare semantice și URI-uri orientate pe resurse]**
- **d) Level 3 — Full HATEOAS compliance [Nivelul 3 — Conformitate HATEOAS completă]**

> 💡 **Feedback:** The endpoint uses resource URIs (/api/users/123) but encodes the action in the URL path (/delete) instead of using the HTTP DELETE verb. This is characteristic of Level 1, where resources are identified but HTTP verbs are not used semantically. A common misconception is placing this at Level 2, but Level 2 requires proper use of HTTP verbs (DELETE instead of POST with /delete in the path). [Endpoint-ul folosește URI-uri de resurse (/api/users/123), dar codifică acțiunea în calea URL (/delete) în loc să utilizeze verbul HTTP DELETE. Aceasta este caracteristic Nivelului 1, unde resursele sunt identificate, dar verbele HTTP nu sunt utilizate semantic. O concepție greșită frecventă este plasarea acestuia la Nivelul 2, dar Nivelul 2 necesită utilizarea corectă a verbelor HTTP (DELETE în loc de POST cu /delete în cale).]

---

### 9. `Multiple Choice – Alegere multiplă`
**N10.C02.Q03: HTTP status code for successful resource creation / Codul de stare HTTP pentru crearea cu succes a unei resurse**

> In a REST Level 2 API, a client sends POST /api/resources with a valid JSON body and a new resource is created. What HTTP status code should the server return? [Într-un API REST de Nivelul 2, un client trimite POST /api/resources cu un corp JSON valid și o nouă resursă este creată. Ce cod de stare HTTP ar trebui să returneze serverul?]

- **a) 201 Created**
- **b) 200 OK**
- **c) 204 No Content**
- **d) 301 Moved Permanently**

> 💡 **Feedback:** HTTP 201 Created is the semantically correct status code for successful resource creation. 200 OK is used for successful GET/PUT, and 204 No Content is typically used for DELETE. A common misconception is using 200 OK for all successful operations, but REST Level 2 requires using specific status codes that convey precise semantics about the outcome. [HTTP 201 Created este codul de stare semantic corect pentru crearea cu succes a unei resurse. 200 OK se folosește pentru GET/PUT reușite, iar 204 No Content se folosește de obicei pentru DELETE. O concepție greșită frecventă este utilizarea 200 OK pentru toate operațiunile reușite, dar REST de Nivelul 2 necesită utilizarea codurilor de stare specifice care transmit semantici precise despre rezultat.]

---

### 10. `Multiple Choice – Alegere multiplă`
**N10.C02.Q04: What HATEOAS adds to a Level 2 API / Ce adaugă HATEOAS unui API de Nivelul 2**

> What is the defining characteristic that elevates a REST API from Richardson Level 2 to Level 3? [Care este caracteristica definitorie care ridică un API REST de la Nivelul Richardson 2 la Nivelul 3?]

- **a) Responses include hypermedia links to related resources and available actions [Răspunsurile includ legături hypermedia către resursele asociate și acțiunile disponibile]**
- **b) The API uses JSON instead of XML as the response format [API-ul folosește JSON în loc de XML ca format de răspuns]**
- **c) All endpoints require OAuth 2.0 authentication [Toate endpoint-urile necesită autentificare OAuth 2.0]**
- **d) The API supports real-time WebSocket push connections alongside standard request-response patterns [API-ul acceptă conexiuni WebSocket în timp real alături de modelele standard cerere-răspuns]**

> 💡 **Feedback:** Level 3 adds HATEOAS — responses include hypermedia links (e.g., _links) that tell the client what actions and related resources are available, enabling discovery without hardcoded URLs. A common misconception is that using JSON as the response format or adding authentication qualifies as Level 3, but HATEOAS specifically requires navigable hypermedia links in every response. [Nivelul 3 adaugă HATEOAS — răspunsurile includ legături hypermedia (de ex., _links) care informează clientul despre acțiunile și resursele asociate disponibile, permițând descoperirea fără URL-uri codificate fix. O concepție greșită frecventă este că utilizarea JSON ca format de răspuns sau adăugarea autentificării califică un API la Nivelul 3, dar HATEOAS necesită în mod specific legături hypermedia navigabile în fiecare răspuns.]

---

### 11. `Multiple Choice – Alegere multiplă`
**N10.C02.Q05: Idempotency of HTTP methods / Idempotența metodelor HTTP**

> Which HTTP method is not idempotent, meaning multiple identical requests may produce different results each time? [Care metodă HTTP nu este idempotentă, ceea ce înseamnă că mai multe cereri identice pot produce rezultate diferite de fiecare dată?]

- **a) POST**
- **b) GET**
- **c) PUT**
- **d) DELETE**

> 💡 **Feedback:** POST is not idempotent — sending the same POST request twice creates two separate resources. GET, PUT, and DELETE are all idempotent: repeating them yields the same outcome. A common misconception is that PUT and POST are interchangeable, but PUT is idempotent (replacing a resource at a specific URI produces the same result regardless of repetition) while POST is not. [POST nu este idempotent — trimiterea aceleiași cereri POST de două ori creează două resurse separate. GET, PUT și DELETE sunt toate idempotente: repetarea lor produce același rezultat. O concepție greșită frecventă este că PUT și POST sunt interschimbabile, dar PUT este idempotent (înlocuirea unei resurse la un URI specific produce același rezultat indiferent de repetare), în timp ce POST nu este.]

---

### 12. `Multiple Choice – Alegere multiplă`
**N10.C02.Q06: Richardson Level 0 characteristics / Caracteristicile Nivelului Richardson 0**

> A developer sends all API requests as POST /api/service with a JSON body like {"action": "list_users"}. Which Richardson Maturity level does this design represent? [Un dezvoltator trimite toate cererile API ca POST /api/service cu un corp JSON precum {"action": "list_users"}. Ce nivel de maturitate Richardson reprezintă acest design?]

- **a) Level 0 — single endpoint, RPC-style [Nivelul 0 — endpoint unic, în stil RPC]**
- **b) Level 1 — resource-oriented URIs [Nivelul 1 — URI-uri orientate pe resurse]**
- **c) Level 2 — semantic HTTP verbs [Nivelul 2 — verbe HTTP semantice]**
- **d) Level 3 — hypermedia controls [Nivelul 3 — controale hypermedia]**

> 💡 **Feedback:** Level 0 (The Swamp of POX) treats HTTP merely as a transport tunnel for RPC-style calls — a single URI handles all operations, with the action specified in the request body. A common misconception is that any API returning JSON qualifies as RESTful, but REST compliance depends on resource-oriented URIs and proper HTTP verb semantics, not on the data format. [Nivelul 0 (The Swamp of POX) tratează HTTP doar ca un tunel de transport pentru apeluri în stil RPC — un singur URI gestionează toate operațiunile, cu acțiunea specificată în corpul cererii. O concepție greșită frecventă este că orice API care returnează JSON se califică drept RESTful, dar conformitatea REST depinde de URI-uri orientate pe resurse și de semantica corectă a verbelor HTTP, nu de formatul datelor.]

---

### 13. `True/False – Adevărat/Fals`
**N10.C02.Q07: Any JSON API qualifies as RESTful / Orice API JSON se califică drept RESTful**

> An API that returns JSON responses is automatically considered RESTful. [Un API care returnează răspunsuri JSON este considerat automat RESTful.]

- **a) True / Adevărat**
- **b) False / Fals**

> 💡 **Feedback:** REST compliance depends on resource-oriented URIs, proper HTTP verb semantics, and appropriate status codes — not on the data format. A JSON API using RPC-style endpoints (e.g., POST /api/service with action in body) is not RESTful. A common misconception is equating JSON usage with REST compliance, confusing the data serialisation format with the architectural constraints that define REST. [Conformitatea REST depinde de URI-uri orientate pe resurse, semantica corectă a verbelor HTTP și coduri de stare adecvate — nu de formatul datelor. Un API JSON care folosește endpoint-uri în stil RPC (de ex., POST /api/service cu acțiunea în corp) nu este RESTful. O concepție greșită frecventă este echivalarea utilizării JSON cu conformitatea REST, confundând formatul de serializare a datelor cu constrângerile arhitecturale care definesc REST.]

---

### 14. `Multiple Choice – Alegere multiplă`
**N10.C02.Q09: CRUD to HTTP verb mapping / Corespondența CRUD cu verbele HTTP**

> In a RESTful API, the CRUD operations map to HTTP verbs. Which mapping is correct? [Într-un API RESTful, operațiunile CRUD corespund verbelor HTTP. Care corespondență este corectă?]

- **a) Create → POST, Read → GET, Update → PUT, Delete → DELETE**
- **b) Create → PUT, Read → GET, Update → POST, Delete → DELETE**
- **c) Create → POST, Read → HEAD, Update → PATCH, Delete → OPTIONS**
- **d) Create → GET, Read → POST, Update → DELETE, Delete → PUT**

> 💡 **Feedback:** The standard CRUD-to-HTTP mapping is: Create → POST, Read → GET, Update → PUT (full replacement) or PATCH (partial), Delete → DELETE. A common misconception is reversing Create and Update verbs or confusing PUT with POST, but POST creates new resources (non-idempotent) while PUT replaces an entire resource at a specific URI (idempotent). [Corespondența standard CRUD-HTTP este: Create → POST, Read → GET, Update → PUT (înlocuire completă) sau PATCH (parțial), Delete → DELETE. O concepție greșită frecventă este inversarea verbelor Create și Update sau confundarea PUT cu POST, dar POST creează resurse noi (non-idempotent), în timp ce PUT înlocuiește o resursă întreagă la un URI specific (idempotent).]

---

### 15. `Multiple Choice – Alegere multiplă`
**N10.C03.Q01: DNS transport protocols / Protocoalele de transport DNS**

> Which transport protocol(s) does DNS use on port 53? [Ce protocol(oale) de transport folosește DNS pe portul 53?]

- **a) Both UDP and TCP, depending on response size and transfer type [Atât UDP cât și TCP, în funcție de dimensiunea răspunsului și tipul transferului]**
- **b) UDP only on port 53 for all queries and zone transfers regardless of size [Doar UDP pe portul 53 pentru toate interogările și transferurile de zonă indiferent de dimensiune]**
- **c) TCP only for reliability [Doar TCP pentru fiabilitate]**
- **d) UDP on port 53 for standard queries with TCP on port 80 for larger responses [UDP pe portul 53 pentru interogări standard cu TCP pe portul 80 pentru răspunsuri mai mari]**

> 💡 **Feedback:** DNS uses both UDP (for standard queries, efficient for small responses) and TCP (for large responses exceeding 512 bytes, zone transfers via AXFR/IXFR, and when the TC bit is set). A common misconception is that DNS uses only UDP, but TCP is essential for zone transfers and large responses such as those with DNSSEC records. [DNS folosește atât UDP (pentru interogări standard, eficient pentru răspunsuri mici), cât și TCP (pentru răspunsuri mari care depășesc 512 de octeți, transferuri de zonă prin AXFR/IXFR și când bitul TC este setat). O concepție greșită frecventă este că DNS folosește doar UDP, dar TCP este esențial pentru transferurile de zonă și răspunsurile mari, precum cele cu înregistrări DNSSEC.]

---

### 16. `Multiple Choice – Alegere multiplă`
**N10.C03.Q02: DNS TC (truncation) bit client behaviour / Comportamentul clientului la bitul TC (trunchiere) DNS**

> A DNS client receives a response with the TC (truncation) bit set. What is the correct next step? [Un client DNS primește un răspuns cu bitul TC (trunchiere) setat. Care este pasul corect următor?]

- **a) Retry the same query using TCP instead of UDP [Reîncercarea aceleiași interogări folosind TCP în loc de UDP]**
- **b) Accept the truncated response as final [Acceptarea răspunsului trunchiat ca definitiv]**
- **c) Switch to a different DNS server [Schimbarea la un alt server DNS]**
- **d) Increase the local UDP buffer size and retry over UDP [Mărirea dimensiunii buffer-ului UDP local și reîncercarea prin UDP]**

> 💡 **Feedback:** The TC bit signals that the UDP response was too large and was truncated. The client should retry the same query over TCP, which has no practical size limit for DNS responses. A common misconception is that the truncated response should be accepted as-is or that changing the DNS server resolves the issue, but the correct procedure is to retry via TCP to receive the complete response. [Bitul TC semnalează că răspunsul UDP a fost prea mare și a fost trunchiat. Clientul trebuie să reîncerce aceeași interogare prin TCP, care nu are o limită practică de dimensiune pentru răspunsurile DNS. O concepție greșită frecventă este că răspunsul trunchiat ar trebui acceptat ca atare sau că schimbarea serverului DNS rezolvă problema, dar procedura corectă este reîncercarea prin TCP pentru a primi răspunsul complet.]

---

### 17. `Multiple Choice – Alegere multiplă`
**N10.C03.Q03: DNS record type for mapping domain to IPv4 / Tipul de înregistrare DNS pentru asocierea unui domeniu cu IPv4**

> Which DNS record type maps a domain name to an IPv4 address? [Ce tip de înregistrare DNS asociază un nume de domeniu cu o adresă IPv4?]

- **a) A record [Înregistrare A]**
- **b) AAAA record [Înregistrare AAAA]**
- **c) CNAME record [Înregistrare CNAME]**
- **d) MX record [Înregistrare MX]**

> 💡 **Feedback:** The A record maps a domain to an IPv4 address. AAAA maps to IPv6, CNAME creates an alias, and MX specifies mail exchangers. A common misconception is confusing A and AAAA records, but A is exclusively for IPv4 (32-bit addresses) while AAAA is for IPv6 (128-bit addresses). [Înregistrarea A asociază un domeniu cu o adresă IPv4. AAAA asociază cu IPv6, CNAME creează un alias, iar MX specifică serverele de e-mail. O concepție greșită frecventă este confundarea înregistrărilor A și AAAA, dar A este exclusiv pentru IPv4 (adrese pe 32 de biți), în timp ce AAAA este pentru IPv6 (adrese pe 128 de biți).]

---

### 18. `Multiple Choice – Alegere multiplă`
**N10.C03.Q04: DNS response status for non-existent domain / Starea răspunsului DNS pentru un domeniu inexistent**

> When querying a DNS server for a domain that does not exist, what status code appears in the response header? [La interogarea unui server DNS pentru un domeniu care nu există, ce cod de stare apare în antetul răspunsului?]

- **a) NXDOMAIN**
- **b) NOERROR**
- **c) SERVFAIL**
- **d) REFUSED**

> 💡 **Feedback:** NXDOMAIN (Non-Existent Domain) is the DNS response code indicating that the queried domain name does not exist in the DNS system. A common misconception is confusing NXDOMAIN with SERVFAIL — SERVFAIL indicates the DNS server encountered an error processing the query, whereas NXDOMAIN definitively states the domain does not exist. [NXDOMAIN (Non-Existent Domain) este codul de răspuns DNS care indică faptul că numele de domeniu interogat nu există în sistemul DNS. O concepție greșită frecventă este confundarea NXDOMAIN cu SERVFAIL — SERVFAIL indică faptul că serverul DNS a întâmpinat o eroare la procesarea interogării, în timp ce NXDOMAIN afirmă definitiv că domeniul nu există.]

---

### 19. `True/False – Adevărat/Fals`
**N10.C03.Q05: DNS caching improves privacy / Memorarea în cache DNS îmbunătățește confidențialitatea**

> Using a local DNS cache protects user privacy because queries are answered locally. [Utilizarea unui cache DNS local protejează confidențialitatea utilizatorului deoarece interogările primesc răspuns local.]

- **a) True / Adevărat**
- **b) False / Fals**

> 💡 **Feedback:** DNS caching reduces query frequency but does not improve privacy. Initial queries still go to upstream resolvers in plaintext, and cached results reveal browsing patterns if examined. Actual DNS privacy requires DoH (DNS over HTTPS) or DoT (DNS over TLS). A common misconception is that fewer queries mean better privacy, but the initial lookup still exposes the domain name to the upstream resolver. [Memorarea în cache DNS reduce frecvența interogărilor, dar nu îmbunătățește confidențialitatea. Interogările inițiale ajung în continuare la rezolvoarele din amonte în text clar, iar rezultatele din cache dezvăluie tiparele de navigare dacă sunt examinate. Confidențialitatea DNS reală necesită DoH (DNS over HTTPS) sau DoT (DNS over TLS). O concepție greșită frecventă este că mai puține interogări înseamnă confidențialitate mai bună, dar interogarea inițială expune în continuare numele de domeniu către rezolvorul din amonte.]

---

### 20. `Multiple Choice – Alegere multiplă`
**N10.C04.Q03: SSH key authentication versus password authentication / Autentificarea SSH prin chei versus autentificarea prin parolă**

> Why is SSH key authentication considered more secure than password authentication? [De ce este autentificarea SSH prin chei considerată mai sigură decât autentificarea prin parolă?]

- **a) SSH keys are much longer (2048+ bits) and the private key is never sent to the server [Cheile SSH sunt mult mai lungi (2048+ biți) și cheia privată nu este niciodată trimisă serverului]**
- **b) SSH keys use symmetric encryption exclusively throughout the session, which provides inherently greater computational security [Cheile SSH folosesc criptare simetrică exclusiv pe parcursul întregii sesiuni, ceea ce oferă o securitate computațională inerent mai mare]**
- **c) SSH keys automatically expire after 30 days, reducing exposure [Cheile SSH expiră automat după 30 de zile, reducând expunerea]**
- **d) SSH keys encrypt the entire session including all commands, while passwords only protect the initial authentication exchange [Cheile SSH criptează întreaga sesiune inclusiv toate comenzile, în timp ce parolele protejează doar schimbul inițial de autentificare]**

> 💡 **Feedback:** SSH keys provide 2048+ bits of entropy, are resistant to brute-force attacks, and the private key never leaves the client machine — eliminating phishing and network-exposure risks inherent to passwords. A common misconception is that SSH key authentication is less secure than passwords because keys can be copied, but the private key is protected locally and never transmitted over the network, unlike passwords. [Cheile SSH oferă peste 2048 de biți de entropie, sunt rezistente la atacuri de tip forță brută, iar cheia privată nu părăsește niciodată mașina clientului — eliminând riscurile de phishing și de expunere în rețea inerente parolelor. O concepție greșită frecventă este că autentificarea prin chei SSH este mai puțin sigură decât parolele deoarece cheile pot fi copiate, dar cheia privată este protejată local și nu este niciodată transmisă prin rețea, spre deosebire de parole.]

---

### 21. `True/False – Adevărat/Fals`
**N10.C04.Q04: SSH and SSL/TLS are the same protocol / SSH și SSL/TLS sunt același protocol**

> SSH and SSL/TLS are fundamentally the same protocol, with SSH being a specialised version of TLS for remote shell access. [SSH și SSL/TLS sunt fundamental același protocol, SSH fiind o versiune specializată a TLS pentru acces la distanță la shell.]

- **a) True / Adevărat**
- **b) False / Fals**

> 💡 **Feedback:** SSH and SSL/TLS are completely separate protocols with different designs, ports (SSH: 22, HTTPS: 443), and authentication mechanisms (SSH: password/public key; TLS: certificates). They share similar cryptographic concepts but are independently developed. A common misconception is that SSH uses SSL for encryption, but these are entirely distinct protocol stacks with different histories and architectures. [SSH și SSL/TLS sunt protocoale complet separate cu design-uri diferite, porturi diferite (SSH: 22, HTTPS: 443) și mecanisme de autentificare diferite (SSH: parolă/cheie publică; TLS: certificate). Împărtășesc concepte criptografice similare, dar sunt dezvoltate independent. O concepție greșită frecventă este că SSH folosește SSL pentru criptare, dar acestea sunt stive de protocoale complet distincte cu istorii și arhitecturi diferite.]

---

### 22. `Multiple Choice – Alegere multiplă`
**N10.C04.Q05: SSH protocol layers / Straturile protocolului SSH**

> SSH consists of three protocol layers. Which correctly lists them? [SSH este compus din trei straturi de protocol. Care le enumeră corect?]

- **a) Transport Layer, User Authentication Layer, Connection Layer [Stratul de transport, Stratul de autentificare a utilizatorului, Stratul de conexiune]**
- **b) Encryption Layer, Session Layer, Application Layer [Stratul de criptare, Stratul sesiune, Stratul aplicație]**
- **c) Handshake Layer, Data Layer, Control Layer [Stratul handshake, Stratul de date, Stratul de control]**
- **d) Key Exchange Layer, Cipher Layer, Command Layer — non-standard layer names [Stratul de schimb de chei, Stratul de cifrare, Stratul de comandă — denumiri de straturi non-standard]**

> 💡 **Feedback:** SSH has three layers: (1) Transport Layer — server authentication, encryption, integrity; (2) User Authentication Layer — password, public key, etc.; (3) Connection Layer — multiplexed channels for shell, X11, port forwarding. A common misconception is that SSH has a single monolithic encryption layer, but its layered design allows independent negotiation of transport security, user authentication, and connection multiplexing. [SSH are trei straturi: (1) Stratul de transport — autentificarea serverului, criptare, integritate; (2) Stratul de autentificare a utilizatorului — parolă, cheie publică, etc.; (3) Stratul de conexiune — canale multiplexate pentru shell, X11, redirecționare de porturi. O concepție greșită frecventă este că SSH are un singur strat monolitic de criptare, dar design-ul său stratificat permite negocierea independentă a securității transportului, autentificării utilizatorului și multiplexării conexiunilor.]

---

### 23. `Multiple Choice – Alegere multiplă`
**N10.C05.Q01: Protocol comparison — standard ports / Compararea protocoalelor — porturi standard**

> Which set of standard (well-known) port numbers is correct? [Care set de numere de porturi standard (bine-cunoscute) este corect?]

- **a) HTTP: 80, HTTPS: 443, DNS: 53, SSH: 22, FTP: 21**
- **b) HTTP: 8080, HTTPS: 443, DNS: 53, SSH: 22, FTP: 20**
- **c) HTTP: 80, HTTPS: 9443, DNS: 5353, SSH: 2222, FTP: 21**
- **d) HTTP: 80, HTTPS: 443, DNS: 53, SSH: 23, FTP: 25**

> 💡 **Feedback:** The standard ports are: HTTP → 80, HTTPS → 443, DNS → 53, SSH → 22, FTP control → 21. These are the well-known port assignments defined by IANA. A common misconception is confusing standard ports with lab ports (e.g., 8080, 9443, 5353, 2222), which are used to avoid requiring root privileges in development environments. [Porturile standard sunt: HTTP → 80, HTTPS → 443, DNS → 53, SSH → 22, control FTP → 21. Acestea sunt atribuirile de porturi bine-cunoscute definite de IANA. O concepție greșită frecventă este confundarea porturilor standard cu porturile de laborator (de ex., 8080, 9443, 5353, 2222), care sunt folosite pentru a evita necesitatea privilegiilor de root în mediile de dezvoltare.]

---

### 24. `Multiple Choice – Alegere multiplă`
**N10.C05.Q02: Encrypted versus unencrypted protocol pairing / Protocoale criptate versus necriptate — corespondențe**

> Which protocol provides an encrypted alternative to standard FTP for file transfers over SSH? [Care protocol oferă o alternativă criptată la FTP standard pentru transferuri de fișiere prin SSH?]

- **a) SFTP (SSH File Transfer Protocol) [SFTP (SSH File Transfer Protocol)]**
- **b) HTTP/2 with server push for bidirectional encrypted data transfer [HTTP/2 cu server push pentru transferul bidirecțional de date criptate]**
- **c) DNS over HTTPS (DoH) for encrypted name resolution [DNS over HTTPS (DoH) pentru rezolvare de nume criptată]**
- **d) SCP over UDP [SCP prin UDP]**

> 💡 **Feedback:** SFTP (SSH File Transfer Protocol) provides encrypted file transfer over an SSH connection. Unlike standard FTP, all data including credentials and file contents is encrypted. A common misconception is confusing SFTP with FTPS (FTP over TLS) — SFTP runs entirely over SSH on port 22, while FTPS wraps FTP inside TLS and still uses the dual-channel architecture. [SFTP (SSH File Transfer Protocol) oferă transfer de fișiere criptat printr-o conexiune SSH. Spre deosebire de FTP standard, toate datele, inclusiv datele de autentificare și conținutul fișierelor, sunt criptate. O concepție greșită frecventă este confundarea SFTP cu FTPS (FTP over TLS) — SFTP rulează integral prin SSH pe portul 22, în timp ce FTPS încapsulează FTP în TLS și folosește în continuare arhitectura cu canal dublu.]

---

### 25. `Multiple Choice – Alegere multiplă`
**N10.C05.Q03: Recommended protocol for transferring sensitive files / Protocolul recomandat pentru transferul fișierelor sensibile**

> A system administrator needs to transfer confidential financial records between two servers. Which protocol should they use? [Un administrator de sistem trebuie să transfere documente financiare confidențiale între două servere. Ce protocol ar trebui să folosească?]

- **a) SFTP — encrypted file transfer over SSH [SFTP — transfer de fișiere criptat prin SSH]**
- **b) FTP — standard file transfer protocol on port 21 [FTP — protocol standard de transfer de fișiere pe portul 21]**
- **c) HTTP — downloading files via a web server [HTTP — descărcarea fișierelor printr-un server web]**
- **d) Telnet — remote file access protocol [Telnet — protocol de acces la distanță la fișiere]**

> 💡 **Feedback:** SFTP (over SSH) encrypts both credentials and file data, making it the appropriate choice for sensitive transfers. Standard FTP transmits everything in plaintext, including usernames and passwords, and HTTP lacks built-in file transfer security. A common misconception is that FTP is secure enough because it requires a password, but FTP credentials are sent in cleartext and can be captured by any network observer. [SFTP (prin SSH) criptează atât datele de autentificare cât și datele fișierelor, fiind alegerea potrivită pentru transferuri sensibile. FTP standard transmite totul în text clar, inclusiv numele de utilizator și parolele, iar HTTP nu dispune de securitate integrată pentru transferul de fișiere. O concepție greșită frecventă este că FTP este suficient de sigur deoarece necesită o parolă, dar datele de autentificare FTP sunt trimise în text clar și pot fi capturate de orice observator din rețea.]

---

### 26. `Multiple Choice – Alegere multiplă`
**N10.C05.Q04: Transport layer protocol usage across application protocols / Utilizarea protocoalelor stratului de transport de către protocoalele aplicației**

> A student claims that all the application layer protocols studied this week exclusively use TCP as their transport protocol. Which response correctly identifies the exception? [Un student afirmă că toate protocoalele stratului aplicație studiate în această săptămână folosesc exclusiv TCP ca protocol de transport. Care răspuns identifică corect excepția?]

- **a) DNS uses both UDP and TCP on port 53, depending on response size and transfer type [DNS folosește atât UDP cât și TCP pe portul 53, în funcție de dimensiunea răspunsului și tipul transferului]**
- **b) FTP uses UDP for its data channel to improve transfer speed [FTP folosește UDP pentru canalul de date pentru a îmbunătăți viteza de transfer]**
- **c) SSH switches to UDP for port forwarding operations [SSH comută la UDP pentru operațiunile de redirecționare de porturi]**
- **d) All protocols studied this week rely exclusively on TCP for transport — none of them ever use UDP in any scenario [Toate protocoalele studiate în această săptămână se bazează exclusiv pe TCP pentru transport — niciunul nu folosește UDP în niciun scenariu]**

> 💡 **Feedback:** DNS uses both UDP (for standard queries under 512 bytes) and TCP (for zone transfers and large responses with the TC bit set). HTTP, HTTPS, SSH, and FTP all use TCP exclusively, while HTTP/3 uses QUIC (UDP-based) but was not part of the lab exercises. A common misconception is that DNS is purely UDP-based, ignoring its TCP capability for zone transfers and oversized responses. [DNS folosește atât UDP (pentru interogări standard sub 512 de octeți) cât și TCP (pentru transferuri de zonă și răspunsuri mari cu bitul TC setat). HTTP, HTTPS, SSH și FTP folosesc toate exclusiv TCP, în timp ce HTTP/3 folosește QUIC (bazat pe UDP), dar nu a făcut parte din exercițiile de laborator. O concepție greșită frecventă este că DNS este pur bazat pe UDP, ignorând capacitatea sa TCP pentru transferuri de zonă și răspunsuri supradimensionate.]

---

### 27. `Multiple Choice – Alegere multiplă`
**N10.T00.Q01: TLS handshake — SNI privacy implications / Handshake-ul TLS — implicațiile SNI asupra confidențialității**

> A corporate network administrator monitors HTTPS traffic using a passive tap. Which statement best describes what the administrator can observe without performing TLS interception? [Un administrator de rețea corporativă monitorizează traficul HTTPS folosind un tap pasiv. Care afirmație descrie cel mai bine ce poate observa administratorul fără a efectua intercepție TLS?]

- **a) The destination domain name and IP address, but not the URL path or request body [Numele de domeniu de destinație și adresa IP, dar nu calea URL sau corpul cererii]**
- **b) The complete URL including path, query parameters, and all HTTP request headers [URL-ul complet, inclusiv calea, parametrii de interogare și toate antetele cererii HTTP]**
- **c) Nothing at all — HTTPS encrypts the entire connection metadata [Nimic — HTTPS criptează toate metadatele conexiunii]**
- **d) Only the destination IP address, because modern TLS encrypts the domain name using Encrypted Client Hello (ECH) [Doar adresa IP de destinație, deoarece TLS modern criptează numele de domeniu folosind Encrypted Client Hello (ECH)]**

> 💡 **Feedback:** During the TLS handshake, the client sends the destination domain name in plaintext via SNI (Server Name Indication) so the server can select the appropriate certificate. The URL path, query parameters, headers, and body are all encrypted within the TLS tunnel. A common error is assuming HTTPS conceals the domain name; only the content after the domain is protected. Another misconception is that nothing at all is visible — in reality, the destination IP address and domain (via SNI) remain observable. [În timpul handshake-ului TLS, clientul trimite numele de domeniu de destinație în text clar prin SNI (Server Name Indication) pentru ca serverul să poată selecta certificatul corespunzător. Calea URL, parametrii de interogare, antetele și corpul sunt toate criptate în tunelul TLS. O eroare frecventă este presupunerea că HTTPS ascunde numele de domeniu; doar conținutul de după domeniu este protejat. O altă concepție greșită este că nimic nu este vizibil — în realitate, adresa IP de destinație și domeniul (prin SNI) rămân observabile.]

---

### 28. `Multiple Choice – Alegere multiplă`
**N10.T00.Q02: Richardson Maturity Model — identifying API levels / Modelul de Maturitate Richardson — identificarea nivelurilor API**

> A developer reviews the following API endpoint: POST /api/users/45/delete. According to the Richardson Maturity Model, which level does this endpoint represent, and what change would promote it to the next level? [Un dezvoltator analizează următorul endpoint API: POST /api/users/45/delete. Conform Modelului de Maturitate Richardson, ce nivel reprezintă acest endpoint și ce modificare l-ar promova la nivelul următor?]

- **a) Level 1; change to DELETE /api/users/45 with proper status codes [Nivelul 1; schimbarea la DELETE /api/users/45 cu coduri de stare corespunzătoare]**
- **b) Level 0; change to POST /api {action: delete, id: 45} [Nivelul 0; schimbarea la POST /api {action: delete, id: 45}]**
- **c) Level 2; add HATEOAS links to reach Level 3 [Nivelul 2; adăugarea de link-uri HATEOAS pentru a ajunge la Nivelul 3]**
- **d) Level 2; no change needed, the endpoint is already semantically correct [Nivelul 2; nu este necesară nicio modificare, endpoint-ul este deja corect semantic]**

> 💡 **Feedback:** The endpoint uses a resource URI (/api/users/45) but embeds the action in the path (/delete) rather than using the DELETE HTTP verb. This is characteristic of Level 1 (resources with URIs, but verbs not used semantically). Promoting to Level 2 means using DELETE /api/users/45 and returning 204 No Content. A common error is classifying this as Level 2 because it has a resource URI — but the action-in-URL pattern is the hallmark of Level 1. [Endpoint-ul folosește un URI de resursă (/api/users/45) dar încorporează acțiunea în cale (/delete) în loc să folosească verbul HTTP DELETE. Aceasta este caracteristic Nivelului 1 (resurse cu URI-uri, dar verbele nu sunt folosite semantic). Promovarea la Nivelul 2 înseamnă utilizarea DELETE /api/users/45 și returnarea 204 No Content. O eroare frecventă este clasificarea ca Nivel 2 deoarece are un URI de resursă — dar modelul acțiune-în-URL este marca Nivelului 1.]

---

### 29. `Multiple Choice – Alegere multiplă`
**N10.T00.Q03: DNS transport fallback mechanism / Mecanismul de tranziție al transportului DNS**

> A DNS resolver receives a response with the TC (truncation) bit set. What is the most likely explanation and appropriate client behaviour? [Un resolver DNS primește un răspuns cu bitul TC (trunchiere) setat. Care este explicația cea mai probabilă și comportamentul adecvat al clientului?]

- **a) The UDP response exceeded the size limit; the client should retry the query using TCP [Răspunsul UDP a depășit limita de dimensiune; clientul ar trebui să reîncerce interogarea folosind TCP]**
- **b) The DNS server is overloaded; the client should wait and retry with the same UDP query [Serverul DNS este supraîncărcat; clientul ar trebui să aștepte și să reîncerce cu aceeași interogare UDP]**
- **c) The query contained an error; the client should reformulate with a different record type [Interogarea conținea o eroare; clientul ar trebui să reformuleze cu un alt tip de înregistrare]**
- **d) The response was corrupted in transit; the client should query a different DNS server [Răspunsul a fost corupt în tranzit; clientul ar trebui să interogheze un alt server DNS]**

> 💡 **Feedback:** The TC bit indicates the response was too large for a single UDP datagram. The client should retry the same query using TCP, which has no message size limit. This is specified in RFC 1035 and is standard DNS behaviour. A common error is thinking DNS always uses UDP — TCP is essential for large responses (DNSSEC, many records) and zone transfers. [Bitul TC indică faptul că răspunsul a fost prea mare pentru o singură datagramă UDP. Clientul ar trebui să reîncerce aceeași interogare folosind TCP, care nu are limită de dimensiune a mesajului. Aceasta este specificată în RFC 1035 și este un comportament DNS standard. O eroare frecventă este credința că DNS folosește întotdeauna UDP — TCP este esențial pentru răspunsuri mari (DNSSEC, multe înregistrări) și transferuri de zonă.]

---

### 30. `Multiple Choice – Alegere multiplă`
**N10.T00.Q05: HTTPS padlock misconception / Concepția greșită despre lacătul HTTPS**

> A user sees a padlock icon in their browser when visiting https://totally-legit-bank.com. Which statement most accurately describes what the padlock guarantees? [Un utilizator vede o pictogramă de lacăt în browser când vizitează https://totally-legit-bank.com. Care afirmație descrie cel mai exact ce garantează lacătul?]

- **a) The connection is encrypted and the server has a valid TLS certificate, but the site could still be malicious [Conexiunea este criptată și serverul are un certificat TLS valid, dar site-ul ar putea fi în continuare malițios]**
- **b) The website has been verified as safe and legitimate by a trusted authority [Site-ul web a fost verificat ca sigur și legitim de o autoritate de încredere]**
- **c) The website operator's identity and business practices have been thoroughly verified by the certificate authority that issued the TLS certificate [Identitatea și practicile comerciale ale operatorului site-ului web au fost verificate amănunțit de autoritatea de certificare care a emis certificatul TLS]**
- **d) The website's data storage practices comply with privacy regulations [Practicile de stocare a datelor ale site-ului sunt conforme cu reglementările de confidențialitate]**

> 💡 **Feedback:** The HTTPS padlock only means the connection between the browser and server is encrypted and the server presented a valid certificate. It says nothing about the trustworthiness, safety, or legitimacy of the website itself. Phishing sites routinely obtain valid HTTPS certificates from free CAs like Let's Encrypt. Equating the padlock with website safety is one of the most dangerous misconceptions in web security. [Lacătul HTTPS înseamnă doar că conexiunea dintre browser și server este criptată și serverul a prezentat un certificat valid. Nu spune nimic despre încrederea, siguranța sau legitimitatea site-ului web în sine. Site-urile de phishing obțin în mod curent certificate HTTPS valide de la CA-uri gratuite precum Let's Encrypt. Echivalarea lacătului cu siguranța site-ului este una dintre cele mai periculoase concepții greșite în securitatea web.]

---

### 31. `Multiple Choice – Alegere multiplă`
**N10.T00.Q06: HTTP idempotency and method semantics / Idempotența HTTP și semantica metodelor**

> A developer accidentally sends the same PUT /api/users/10 request three times due to a network retry. A second developer sends the same POST /api/users request three times. What is the most likely outcome for each? [Un dezvoltator trimite accidental aceeași cerere PUT /api/users/10 de trei ori din cauza unei reîncercări de rețea. Un al doilea dezvoltator trimite aceeași cerere POST /api/users de trei ori. Care este rezultatul cel mai probabil pentru fiecare?]

- **a) PUT: user 10 is updated to the same state (one user); POST: three new users are created [PUT: utilizatorul 10 este actualizat la aceeași stare (un utilizator); POST: trei utilizatori noi sunt creați]**
- **b) Both create three separate entries because HTTP has no built-in duplicate detection [Ambele creează trei intrări separate deoarece HTTP nu are detecție de duplicate integrată]**
- **c) PUT: three versions of user 10 are stored; POST: only one user is created [PUT: trei versiuni ale utilizatorului 10 sunt stocate; POST: doar un utilizator este creat]**
- **d) Both update a single record because the server detects identical request bodies, which does not accurately reflect how modern implementations handle the key exchange procedure [Ambele actualizează o singură înregistrare deoarece serverul detectează corpuri de cerere identice, ceea ce nu reflectă cu acuratețe modul în care implementările moderne gestionează procedura de schimb de chei]**

> 💡 **Feedback:** PUT is idempotent — sending the same PUT to the same URI multiple times produces the same result (user 10 is updated once). POST is not idempotent — each POST creates a new resource, resulting in three separate users. This semantic distinction is fundamental to REST Level 2 and affects how clients handle retries. [PUT este idempotent — trimiterea aceluiași PUT la același URI de mai multe ori produce același rezultat (utilizatorul 10 este actualizat o singură dată). POST nu este idempotent — fiecare POST creează o resursă nouă, rezultând în trei utilizatori separați. Această distincție semantică este fundamentală pentru Nivelul 2 REST și afectează modul în care clienții gestionează reîncercările.]

---

### 32. `Multiple Choice – Alegere multiplă`
**N10.T00.Q07: SSH vs TLS — protocol comparison / SSH versus TLS — compararea protocoalelor**

> A student claims that SSH and TLS are essentially the same protocol because both provide encryption. Which statement best corrects this misconception? [Un student afirmă că SSH și TLS sunt în esență același protocol deoarece ambele oferă criptare. Care afirmație corectează cel mai bine această concepție greșită?]

- **a) They are separate protocols: SSH integrates shell access and authentication, while TLS is a general transport encryption layer using X.509 certificates [Sunt protocoale separate: SSH integrează accesul la shell și autentificarea, în timp ce TLS este un nivel general de criptare a transportului folosind certificate X.509]**
- **b) SSH is simply TLS with a different port number and default cipher suite despite this description omitting the critical role of certificate validation in the trust chain [SSH este pur și simplu TLS cu un număr de port diferit și o suită de cifrare implicită diferită în ciuda faptului că această descriere omite rolul critic al validării certificatelor în lanțul de încredere]**
- **c) TLS is the newer replacement for SSH, offering better security guarantees [TLS este înlocuitorul mai nou al SSH, oferind garanții de securitate mai bune]**
- **d) SSH runs on top of TLS, adding remote command execution capabilities [SSH rulează peste TLS, adăugând capabilități de execuție a comenzilor la distanță]**

> 💡 **Feedback:** SSH and TLS are completely independent protocols with different designs and purposes. SSH integrates authentication, encryption, and session multiplexing in a single protocol (port 22) designed for remote shell access. TLS is a general-purpose transport encryption layer used by many application protocols (HTTPS, SMTPS, etc.) and relies on X.509 certificates. They share similar cryptographic primitives (AES, ECDH) but differ in architecture, authentication, and use cases. [SSH și TLS sunt protocoale complet independente cu design-uri și scopuri diferite. SSH integrează autentificarea, criptarea și multiplexarea sesiunilor într-un singur protocol (portul 22) conceput pentru acces la shell la distanță. TLS este un nivel de criptare a transportului de uz general folosit de multe protocoale de aplicație (HTTPS, SMTPS, etc.) și se bazează pe certificate X.509. Partajează primitive criptografice similare (AES, ECDH) dar diferă în arhitectură, autentificare și cazuri de utilizare.]

---

### 33. `Multiple Choice – Alegere multiplă`
**N10.T00.Q08: HTTP/2 and browser enforcement / HTTP/2 și impunerea de către browsere**

> A systems engineer configures an HTTP/2 server. The server supports both cleartext (h2c) and TLS-encrypted (h2) connections. However, no major browser connects using h2c. What is the most accurate explanation? [Un inginer de sisteme configurează un server HTTP/2. Serverul suportă atât conexiuni în text clar (h2c), cât și criptate cu TLS (h2). Totuși, niciun browser major nu se conectează folosind h2c. Care este explicația cea mai corectă?]

- **a) Browsers choose to implement HTTP/2 only over TLS as a policy decision to encourage encryption; the protocol specification permits cleartext [Browserele aleg să implementeze HTTP/2 doar peste TLS ca decizie de politică pentru a încuraja criptarea; specificația protocolului permite text clar]**
- **b) HTTP/2 specification requires TLS; cleartext mode was removed in a later RFC update [Specificația HTTP/2 necesită TLS; modul text clar a fost eliminat într-o actualizare RFC ulterioară]**
- **c) Cleartext HTTP/2 (h2c) requires a dedicated browser extension because browsers cannot negotiate the h2c upgrade natively [HTTP/2 în text clar (h2c) necesită o extensie dedicată de browser deoarece browserele nu pot negocia actualizarea h2c nativ]**
- **d) The h2c protocol cannot negotiate connection parameters without TLS ALPN [Protocolul h2c nu poate negocia parametrii conexiunii fără TLS ALPN]**

> 💡 **Feedback:** The HTTP/2 specification (RFC 7540) allows both encrypted and cleartext modes. However, all major browsers (Chrome, Firefox, Safari, Edge) only implement h2 over TLS. This is a deliberate browser policy to encourage encryption adoption, not a protocol limitation. Server-to-server and CLI tools like curl can use h2c. [Specificația HTTP/2 (RFC 7540) permite atât modul criptat, cât și cel în text clar. Totuși, toate browserele majore (Chrome, Firefox, Safari, Edge) implementează doar h2 peste TLS. Aceasta este o politică deliberată a browserelor pentru a încuraja adoptarea criptării, nu o limitare a protocolului. Comunicarea server-la-server și instrumentele CLI precum curl pot folosi h2c.]

---

### 34. `Multiple Choice – Alegere multiplă`
**N10.T00.Q09: SSH key authentication security / Securitatea autentificării SSH bazate pe chei**

> In the context of SSH authentication, what is the primary security advantage of public-key authentication over password authentication? [În contextul autentificării SSH, care este principalul avantaj de securitate al autentificării bazate pe cheie publică față de autentificarea cu parolă?]

- **a) The private key never leaves the client; the server only verifies a cryptographic proof of possession [Cheia privată nu părăsește niciodată clientul; serverul verifică doar o dovadă criptografică a posesiei]**
- **b) SSH keys use stronger encryption algorithms than password-based authentication [Cheile SSH folosesc algoritmi de criptare mai puternici decât autentificarea bazată pe parole]**
- **c) SSH keys automatically expire after a set period, forcing regular rotation [Cheile SSH expiră automat după o perioadă stabilită, forțând rotația regulată]**
- **d) SSH keys encrypt the entire session with the user's public key for end-to-end security — a formulation that incorrectly suggests a synchronous process where the standard defines asynchronous operation [Cheile SSH criptează întreaga sesiune cu cheia publică a utilizatorului pentru securitate capăt-la-capăt — o formulare ce sugerează incorect un proces sincron unde standardul definește operare asincronă]**

> 💡 **Feedback:** With SSH key authentication, the private key never leaves the client machine. The server only stores the public key. Authentication uses a challenge-response mechanism where the client proves possession of the private key without transmitting it. This eliminates phishing, brute-force (2048+ bit keys), and credential reuse risks. Passwords, by contrast, are sent to the server and can be captured, guessed, or reused. [Cu autentificarea SSH bazată pe chei, cheia privată nu părăsește niciodată mașina client. Serverul stochează doar cheia publică. Autentificarea folosește un mecanism provocare-răspuns prin care clientul dovedește posesia cheii private fără a o transmite. Aceasta elimină riscurile de phishing, brute-force (chei de 2048+ biți) și reutilizare a datelor de autentificare. Parolele, în schimb, sunt trimise serverului și pot fi capturate, ghicite sau reutilizate.]

---

### 35. `Multiple Choice – Alegere multiplă`
**N10.T00.Q10: DNS record type selection / Selectarea tipului de înregistrare DNS**

> A company wants to redirect www.example.com to example.com at the DNS level so both names resolve to the same IP address. Which DNS record type is most appropriate? [O companie dorește să redirecționeze www.example.com către example.com la nivel DNS astfel încât ambele nume să se rezolve la aceeași adresă IP. Ce tip de înregistrare DNS este cel mai potrivit?]

- **a) CNAME — creates an alias so www.example.com resolves to whatever example.com resolves to [CNAME — creează un alias astfel încât www.example.com se rezolvă la orice se rezolvă example.com]**
- **b) A — maps www.example.com directly to the same IPv4 address [A — mapează www.example.com direct la aceeași adresă IPv4]**
- **c) MX — redirects traffic between domain names for any protocol [MX — redirecționează traficul între numele de domeniu pentru orice protocol]**
- **d) NS — delegates www.example.com to the same authoritative name server that handles the example.com zone [NS — deleghează www.example.com către același server de nume autoritativ care gestionează zona example.com]**

> 💡 **Feedback:** A CNAME (Canonical Name) record creates an alias from one domain to another. Setting www.example.com CNAME example.com makes www resolve to wherever example.com points. An A record maps directly to an IP address (requires updating both if IP changes). MX is for mail routing, and NS delegates DNS authority — neither serves as a domain alias. [O înregistrare CNAME (Canonical Name) creează un alias de la un domeniu la altul. Setarea www.example.com CNAME example.com face ca www să se rezolve la orice adresă indică example.com. O înregistrare A mapează direct la o adresă IP (necesită actualizarea ambelor dacă IP-ul se schimbă). MX este pentru rutarea e-mailului, iar NS deleagă autoritatea DNS — niciunul nu servește ca alias de domeniu.]

---

### 36. `Multiple Choice – Alegere multiplă`
**N10.C01.Q01: SNI visibility during TLS handshake / Vizibilitatea SNI în timpul handshake-ului TLS**

> A user navigates to https://bank.example.com/accounts/12345?balance=true. An attacker is passively monitoring the network. Which piece of information can the attacker observe in plaintext? [Un utilizator accesează https://bank.example.com/accounts/12345?balance=true. Un atacator monitorizează pasiv rețeaua. Ce informație poate observa atacatorul în text clar?]

- **a) The domain name bank.example.com via SNI [Numele de domeniu bank.example.com prin SNI]**
- **b) The complete URL including /accounts/12345?balance=true [URL-ul complet, inclusiv /accounts/12345?balance=true]**
- **c) Nothing — HTTPS encryption covers all metadata [Nimic — criptarea HTTPS acoperă toate metadatele]**
- **d) The HTTP headers including cookies and authorisation tokens [Antetele HTTP, inclusiv cookie-urile și token-urile de autorizare]**

> 💡 **Feedback:** During the TLS handshake, the domain name is sent unencrypted via SNI (Server Name Indication) so the server can select the correct certificate. The URL path and query parameters are encrypted inside the TLS tunnel. A common misconception is that HTTPS encrypts the entire URL including the domain name, but the domain remains visible through SNI and the destination IP address is also observable. [În timpul handshake-ului TLS, numele de domeniu este trimis necriptat prin SNI (Server Name Indication) pentru ca serverul să poată selecta certificatul corect. Calea URL și parametrii de interogare sunt criptați în tunelul TLS. O concepție greșită frecventă este că HTTPS criptează întregul URL, inclusiv numele de domeniu, dar acesta rămâne vizibil prin SNI, iar adresa IP de destinație este de asemenea observabilă.]

---

### 37. `Multiple Choice – Alegere multiplă`
**N10.C04.Q01: FTP dual-channel architecture / Arhitectura cu canal dublu FTP**

> How many TCP connections does FTP establish when downloading a single file? [Câte conexiuni TCP stabilește FTP la descărcarea unui singur fișier?]

- **a) Two — a control connection (port 21) and a data connection [Două — o conexiune de control (portul 21) și o conexiune de date]**
- **b) One connection for commands and data combined [O singură conexiune pentru comenzi și date combinate]**
- **c) Three — authentication, command, and data [Trei — autentificare, comandă și date]**
- **d) One connection that dynamically switches between port 21 for commands and port 20 for data transfer [O singură conexiune care comută dinamic între portul 21 pentru comenzi și portul 20 pentru transferul de date]**

> 💡 **Feedback:** FTP uses two TCP connections: a persistent control connection (port 21) for commands and responses, and a separate data connection (port 20 or a high port in passive mode) for actual file data transfer. A common misconception is that FTP uses a single connection like HTTP, but FTP's dual-channel architecture was designed to allow simultaneous command exchange and data transfer. [FTP folosește două conexiuni TCP: o conexiune de control persistentă (portul 21) pentru comenzi și răspunsuri, și o conexiune de date separată (portul 20 sau un port înalt în modul pasiv) pentru transferul efectiv de date. O concepție greșită frecventă este că FTP folosește o singură conexiune ca HTTP, dar arhitectura cu canal dublu a FTP a fost proiectată pentru a permite schimbul simultan de comenzi și transferul de date.]

---

### 38. `Multiple Choice – Alegere multiplă`
**N10.C04.Q02: FTP active versus passive mode / Modul activ versus modul pasiv FTP**

> In FTP passive mode, who initiates the data connection? [În modul pasiv FTP, cine inițiază conexiunea de date?]

- **a) The client connects to a high port on the server [Clientul se conectează la un port înalt de pe server]**
- **b) The server connects to a port on the client [Serverul se conectează la un port de pe client]**
- **c) Neither — data is sent over the control connection [Niciunul — datele sunt trimise prin conexiunea de control]**
- **d) A third-party relay server handles the data transfer [Un server releu terț gestionează transferul de date]**

> 💡 **Feedback:** In passive mode, the client initiates the data connection to a high port on the server. This is preferred because most clients are behind NAT/firewalls that block inbound connections (which active mode requires). A common misconception is that active and passive modes are equivalent, but they have fundamentally different connection directions — in active mode the server connects to the client, which fails behind most NAT configurations. [În modul pasiv, clientul inițiază conexiunea de date către un port înalt de pe server. Acesta este preferat deoarece majoritatea clienților se află în spatele NAT/firewall-urilor care blochează conexiunile de intrare (pe care modul activ le necesită). O concepție greșită frecventă este că modurile activ și pasiv sunt echivalente, dar ele au direcții de conexiune fundamental diferite — în modul activ serverul se conectează la client, ceea ce eșuează în spatele majorității configurațiilor NAT.]

---

### 39. `Multiple Choice – Alegere multiplă`
**N10.T00.Q04: FTP passive mode rationale / Rațiunea modului pasiv FTP**

> A student cannot download files using FTP in active mode from their laptop connected to a home router. Switching to passive mode resolves the issue. What is the primary reason passive mode succeeds where active mode fails? [Un student nu poate descărca fișiere folosind FTP în modul activ de pe laptopul conectat la un router de acasă. Trecerea la modul pasiv rezolvă problema. Care este motivul principal pentru care modul pasiv reușește acolo unde modul activ eșuează?]

- **a) In active mode, the server initiates the data connection to the client, which NAT blocks; passive mode has the client initiate both connections outward [În modul activ, serverul inițiază conexiunea de date către client, pe care NAT o blochează; modul pasiv are clientul inițiind ambele conexiuni spre exterior]**
- **b) Active mode uses unencrypted data channels while passive mode encrypts them [Modul activ folosește canale de date necriptate în timp ce modul pasiv le criptează]**
- **c) Active mode requires the server to perform a reverse DNS lookup of the client address before initiating the data connection back [Modul activ necesită ca serverul să efectueze o căutare DNS inversă a adresei clientului înainte de a inițializa conexiunea de date înapoi]**
- **d) Passive mode uses HTTP tunnelling to bypass firewall restrictions [Modul pasiv folosește tunelarea HTTP pentru a ocoli restricțiile firewall]**

> 💡 **Feedback:** In active mode, the server initiates the data connection back to the client. Home routers performing NAT typically block unsolicited inbound connections, preventing the server from reaching the client. In passive mode, the client initiates both connections (control and data) outward — which NAT handles transparently. The distinction is about who initiates the data connection, not about encryption or protocol differences. [În modul activ, serverul inițiază conexiunea de date înapoi către client. Routerele de acasă care efectuează NAT blochează de obicei conexiunile de intrare nesolicitate, împiedicând serverul să ajungă la client. În modul pasiv, clientul inițiază ambele conexiuni (control și date) spre exterior — ceea ce NAT gestionează transparent. Distincția este despre cine inițiază conexiunea de date, nu despre criptare sau diferențe de protocol.]

---


## Lab Questions / Întrebări de laborator

### 40. `Multiple Choice – Alegere multiplă`
**N10.S01.Q03: TLS state machine — calling server_hello before client_hello / Mașina de stări TLS — apelarea server_hello înainte de client_hello**

> In the code-tracing exercise modelling a TLS connection as a state machine, what happens if server_hello() is called immediately after object initialisation (state = INIT)? [În exercițiul de trasare a codului care modelează o conexiune TLS ca mașină de stări, ce se întâmplă dacă server_hello() este apelat imediat după inițializarea obiectului (state = INIT)?]

- **a) It returns an error string indicating invalid state INIT [Returnează un șir de eroare indicând starea invalidă INIT]**
- **b) It proceeds normally and transitions to SERVER_HELLO, which incorrectly implies a capability that the protocol was deliberately designed not to provide [Continuă normal și trece la SERVER_HELLO, ceea ce implică incorect o capacitate pe care protocolul a fost proiectat în mod deliberat să nu o ofere]**
- **c) It raises a Python exception and crashes [Aruncă o excepție Python și se oprește]**
- **d) It automatically calls client_hello() first [Apelează automat client_hello() mai întâi]**

> 💡 **Feedback:** The state machine enforces strict ordering. server_hello() expects state CLIENT_HELLO, so calling it from state INIT returns an error because the handshake steps must proceed in order. A common misconception is that the state machine automatically corrects the sequence, but enforcing strict ordering mirrors the real TLS protocol where steps cannot be skipped. [Mașina de stări impune o ordine strictă. server_hello() așteaptă starea CLIENT_HELLO, deci apelarea din starea INIT returnează o eroare deoarece pașii handshake-ului trebuie să se desfășoare în ordine. O concepție greșită frecventă este că mașina de stări corectează automat secvența, dar impunerea ordinii stricte reflectă protocolul TLS real, unde pașii nu pot fi omisi.]

---

### 41. `Multiple Choice – Alegere multiplă`
**N10.S01.Q04: SSL context wrap_socket and server_hostname parameter / Contextul SSL wrap_socket și parametrul server_hostname**

> In the Parsons problem for certificate verification, the call context.wrap_socket(sock, server_hostname=hostname) is used. What is the purpose of the server_hostname parameter? [În problema Parsons pentru verificarea certificatului, se folosește apelul context.wrap_socket(sock, server_hostname=hostname). Care este scopul parametrului server_hostname?]

- **a) It enables SNI so the server knows which certificate to present [Activează SNI astfel încât serverul să știe ce certificat să prezinte]**
- **b) It sets the DNS server to use for hostname resolution [Setează serverul DNS utilizat pentru rezoluția numelor de gazdă]**
- **c) It specifies the encryption algorithm to use [Specifică algoritmul de criptare de utilizat]**
- **d) It disables certificate verification for self-signed certificates [Dezactivează verificarea certificatului pentru certificatele auto-semnate]**

> 💡 **Feedback:** The server_hostname parameter enables SNI (Server Name Indication), telling the server which hostname the client is connecting to so it can present the correct certificate. This is essential for virtual hosting where multiple domains share the same IP address. A common misconception is that this parameter sets the DNS server or controls encryption, but it specifically enables the SNI extension in the TLS handshake. [Parametrul server_hostname activează SNI (Server Name Indication), informând serverul la ce nume de gazdă se conectează clientul, astfel încât acesta să poată prezenta certificatul corect. Acest lucru este esențial pentru găzduirea virtuală, unde mai multe domenii partajează aceeași adresă IP. O concepție greșită frecventă este că acest parametru setează serverul DNS sau controlează criptarea, dar el activează specific extensia SNI în handshake-ul TLS.]

---

### 42. `Multiple Choice – Alegere multiplă`
**N10.S02.Q01: HTTP status code for successful DELETE / Codul de stare HTTP pentru DELETE reușit**

> In the lab's HTTPS REST API exercise, what HTTP status code does the server return after successfully deleting a resource? [În exercițiul de API REST HTTPS din laborator, ce cod de stare HTTP returnează serverul după ștergerea cu succes a unei resurse?]

- **a) 204 No Content**
- **b) 200 OK**
- **c) 202 Accepted**
- **d) 410 Gone**

> 💡 **Feedback:** The exercise server returns 204 No Content for successful DELETE operations, indicating the resource was removed and there is no response body. A common misconception is expecting 200 OK with a confirmation message, but 204 explicitly signals success with no body, which is the conventional response for DELETE in RESTful APIs. [Serverul de exerciții returnează 204 No Content pentru operațiunile DELETE reușite, indicând că resursa a fost eliminată și nu există corp al răspunsului. O concepție greșită frecventă este așteptarea unui 200 OK cu un mesaj de confirmare, dar 204 semnalează explicit succesul fără corp, ceea ce este răspunsul convențional pentru DELETE în API-urile RESTful.]

---

### 43. `Multiple Choice – Alegere multiplă`
**N10.S02.Q02: Code tracing — route_request output for non-numeric user ID / Trasarea codului — rezultatul route_request pentru un ID de utilizator non-numeric**

> In the code-tracing exercise, the function route_request parses URL paths and checks if a user ID segment is numeric using isdigit(). What does route_request("GET", "/api/users/abc") return? [În exercițiul de trasare a codului, funcția route_request parsează căile URL și verifică dacă segmentul ID de utilizator este numeric folosind isdigit(). Ce returnează route_request("GET", "/api/users/abc")?]

- **a) ("Not found", 404)**
- **b) ("Get user abc", 200)**
- **c) ("Method not allowed", 405)**
- **d) A ValueError exception is raised [Se aruncă o excepție ValueError]**

> 💡 **Feedback:** The path splits into ['&apos;, 'api', 'users', 'abc']. Since 'abc'.isdigit() returns False, the request falls through to the default return: ("Not found", 404). A common misconception is that the router would return a 405 Method Not Allowed, but the issue is not the method — it is the non-numeric ID segment failing the isdigit() check. [Calea se împarte în ['&apos;, 'api', 'users', 'abc']. Deoarece 'abc'.isdigit() returnează False, cererea cade la returnarea implicită: ("Not found", 404). O concepție greșită frecventă este că routerul ar returna un 405 Method Not Allowed, dar problema nu este metoda — ci segmentul ID non-numeric care nu trece verificarea isdigit().]

---

### 44. `Multiple Choice – Alegere multiplă`
**N10.S02.Q03: Flask route decorator for handling multiple HTTP methods / Decoratorul de rută Flask pentru gestionarea mai multor metode HTTP**

> In the Parsons problem for a Flask REST handler, which decorator syntax allows a single function to handle both GET and POST requests on /api/items? [În problema Parsons pentru un handler REST Flask, ce sintaxă a decoratorului permite unei singure funcții să gestioneze atât cereri GET cât și POST pe /api/items?]

- **a) @app.route("/api/items", methods=["GET", "POST"])**
- **b) @app.get_post("/api/items")**
- **c) @app.route("/api/items", verb="GET|POST")**
- **d) @app.route("/api/items") without any method parameter [fără niciun parametru de metodă]**

> 💡 **Feedback:** The methods parameter accepts a list of allowed HTTP methods: @app.route("/api/items", methods=["GET", "POST"]). The handler then uses request.method to differentiate. A common misconception is that Flask automatically accepts all HTTP methods for a route, but by default only GET (and HEAD/OPTIONS) are allowed unless methods is explicitly specified. [Parametrul methods acceptă o listă de metode HTTP permise: @app.route("/api/items", methods=["GET", "POST"]). Handler-ul folosește apoi request.method pentru a diferenția. O concepție greșită frecventă este că Flask acceptă automat toate metodele HTTP pentru o rută, dar implicit doar GET (și HEAD/OPTIONS) sunt permise dacă methods nu este specificat explicit.]

---

### 45. `Multiple Choice – Alegere multiplă`
**N10.S02.Q04: Code tracing — route_request output for PATCH on /api/users / Trasarea codului — rezultatul route_request pentru PATCH pe /api/users**

> In the code-tracing exercise, the function route_request handles GET, POST, PUT, and DELETE for user resources. A client sends PATCH /api/users. What does route_request("PATCH", "/api/users") return? [În exercițiul de trasare a codului, funcția route_request gestionează GET, POST, PUT și DELETE pentru resursele utilizatorilor. Un client trimite PATCH /api/users. Ce returnează route_request("PATCH", "/api/users")?]

- **a) ("Method not allowed", 405)**
- **b) ("Not found", 404)**
- **c) ("List all users", 200)**
- **d) ("Create user", 201)**

> 💡 **Feedback:** The routing function checks if path == "/api/users", then only matches GET and POST methods. Since PATCH does not match either branch, execution falls to the else clause which returns ("Method not allowed", 405). This demonstrates that the router only implements a subset of HTTP verbs for the collection endpoint. A common misconception is confusing 404 (resource not found) with 405 (method not allowed) — the path exists but the method is not supported. [Funcția de rutare verifică dacă path == "/api/users", apoi potrivește doar metodele GET și POST. Deoarece PATCH nu se potrivește cu niciuna dintre ramuri, execuția cade la clauza else care returnează ("Method not allowed", 405). Aceasta demonstrează că routerul implementează doar un subset de verbe HTTP pentru endpoint-ul de colecție. O concepție greșită frecventă este confundarea 404 (resursă negăsită) cu 405 (metodă nepermisă) — calea există, dar metoda nu este acceptată.]

---

### 46. `Multiple Choice – Alegere multiplă`
**N10.S03.Q03: Code tracing — DNS resolver with trailing dot / Trasarea codului — rezolvor DNS cu punct final**

> In the DNS code-tracing exercise, the function resolve_dns calls query_name.rstrip(".") before looking up the record. What does resolve_dns("web.lab.local.") return for the status field? [În exercițiul de trasare a codului DNS, funcția resolve_dns apelează query_name.rstrip(".") înainte de căutarea înregistrării. Ce returnează resolve_dns("web.lab.local.") pentru câmpul status?]

- **a) "NOERROR" — the trailing dot is removed before lookup [punctul final este eliminat înainte de căutare]**
- **b) "NXDOMAIN" — the dot makes it a different domain [punctul îl face un domeniu diferit]**
- **c) An exception is raised because of the trailing dot — this confuses the purpose of the handshake mechanism with that of the data transfer phase [Se aruncă o excepție din cauza punctului final — aceasta confundă scopul mecanismului de handshake cu cel al fazei de transfer de date]**
- **d) None — the function cannot handle FQDNs [funcția nu poate gestiona FQDN-uri]**

> 💡 **Feedback:** The trailing dot is stripped by rstrip("."), making "web.lab.local." resolve identically to "web.lab.local", returning status "NOERROR". A common misconception is that the trailing dot makes it a different, non-existent domain, but in DNS the trailing dot denotes the FQDN (Fully Qualified Domain Name) root and the code normalises this. [Punctul final este eliminat de rstrip("."), făcând "web.lab.local." să se rezolve identic cu "web.lab.local", returnând statusul "NOERROR". O concepție greșită frecventă este că punctul final face din acesta un domeniu diferit, inexistent, dar în DNS punctul final denotă rădăcina FQDN (Fully Qualified Domain Name), iar codul normalizează acest lucru.]

---

### 47. `Multiple Choice – Alegere multiplă`
**N10.S03.Q05: Socket type for UDP DNS queries in Python / Tipul de socket pentru interogări DNS UDP în Python**

> In the Parsons problem for building a DNS query function, what socket type constant is used to create a UDP socket? [În problema Parsons pentru construirea unei funcții de interogare DNS, ce constantă de tip socket se folosește pentru a crea un socket UDP?]

- **a) socket.SOCK_DGRAM**
- **b) socket.SOCK_STREAM**
- **c) socket.SOCK_RAW**
- **d) socket.SOCK_SEQPACKET**

> 💡 **Feedback:** socket.SOCK_DGRAM creates a UDP datagram socket, appropriate for DNS queries. SOCK_STREAM would create a TCP socket instead. A common misconception is confusing SOCK_DGRAM (datagrame — connectionless, UDP) with SOCK_STREAM (flux de octeți — orientat pe conexiune, TCP). The naming reflects the underlying transport: datagrams are discrete message units while streams are continuous byte flows. [socket.SOCK_DGRAM creează un socket de datagramă UDP, potrivit pentru interogările DNS. SOCK_STREAM ar crea în schimb un socket TCP. O concepție greșită frecventă este confundarea SOCK_DGRAM (datagrame — fără conexiune, UDP) cu SOCK_STREAM (flux de octeți — orientat pe conexiune, TCP). Denumirea reflectă transportul subiacent: datagramele sunt unități de mesaje discrete, în timp ce fluxurile sunt fluxuri continue de octeți.]

---

### 48. `Multiple Choice – Alegere multiplă`
**N10.S04.Q02: Python library for SSH automation / Biblioteca Python pentru automatizarea SSH**

> Which Python library is used in the lab exercises to establish SSH connections and execute remote commands? [Ce bibliotecă Python este folosită în exercițiile de laborator pentru a stabili conexiuni SSH și a executa comenzi la distanță?]

- **a) paramiko**
- **b) pexpect**
- **c) fabric**
- **d) subprocess**

> 💡 **Feedback:** Paramiko is the Python library used in the exercises for SSH operations. It provides an SSHClient class for connecting, authenticating, and running remote commands. A common misconception is confusing Paramiko (dedicated SSH library) with subprocess (local process execution) — subprocess can invoke the ssh command but does not provide native SSH protocol support. [Paramiko este biblioteca Python folosită în exerciții pentru operațiunile SSH. Oferă o clasă SSHClient pentru conectare, autentificare și executarea comenzilor la distanță. O concepție greșită frecventă este confundarea Paramiko (bibliotecă SSH dedicată) cu subprocess (execuția proceselor locale) — subprocess poate invoca comanda ssh, dar nu oferă suport nativ pentru protocolul SSH.]

---

### 49. `Multiple Choice – Alegere multiplă`
**N10.S01.Q01: Self-signed certificate generation command / Comanda pentru generarea unui certificat auto-semnat**

> In the lab, which tool is used to generate a self-signed TLS certificate with the command openssl req -x509 -newkey rsa:2048 ...? [În laborator, ce instrument se folosește pentru a genera un certificat TLS auto-semnat cu comanda openssl req -x509 -newkey rsa:2048 ...?]

- **a) OpenSSL**
- **b) GPG (GNU Privacy Guard)**
- **c) ssh-keygen**
- **d) certbot**

> 💡 **Feedback:** OpenSSL is the standard command-line toolkit for generating TLS certificates, keys, and performing cryptographic operations. The req -x509 subcommand creates a self-signed certificate. A common misconception is confusing openssl with ssh-keygen — the latter generates SSH key pairs, not X.509 certificates used by TLS. [OpenSSL este instrumentul standard de linie de comandă pentru generarea de certificate TLS, chei și efectuarea operațiunilor criptografice. Subcomanda req -x509 creează un certificat auto-semnat. O concepție greșită frecventă este confundarea openssl cu ssh-keygen — acesta din urmă generează perechi de chei SSH, nu certificate X.509 utilizate de TLS.]

---

### 50. `Multiple Choice – Alegere multiplă`
**N10.S01.Q05: openssl s_client for TLS connection testing / openssl s_client pentru testarea conexiunii TLS**

> In the lab, a student needs to inspect the TLS certificate chain and negotiated cipher suite of an HTTPS server. Which command from the cheatsheet establishes a TLS connection and displays this information? [În laborator, un student trebuie să inspecteze lanțul de certificate TLS și suita de cifrare negociată a unui server HTTPS. Ce comandă din foaia de referință stabilește o conexiune TLS și afișează aceste informații?]

- **a) openssl s_client -connect host:443**
- **b) curl -v https://host:443/**
- **c) openssl x509 -in host -text -noout**
- **d) ssh -v host -p 443**

> 💡 **Feedback:** The command openssl s_client -connect host:443 initiates a TLS handshake and prints the certificate chain, negotiated cipher suite, and session parameters. The -showcerts flag displays all certificates in the chain. A common misconception is using curl -v for this purpose — while curl shows some TLS details, openssl s_client provides the most comprehensive certificate and handshake analysis. [Comanda openssl s_client -connect host:443 inițiază un handshake TLS și afișează lanțul de certificate, suita de cifrare negociată și parametrii sesiunii. Opțiunea -showcerts afișează toate certificatele din lanț. O concepție greșită frecventă este utilizarea curl -v în acest scop — deși curl afișează unele detalii TLS, openssl s_client oferă cea mai cuprinzătoare analiză a certificatelor și a handshake-ului.]

---

### 51. `Multiple Choice – Alegere multiplă`
**N10.S04.Q04: Python FTP default passive mode in ftplib / Modul pasiv implicit al FTP în ftplib Python**

> In the Parsons problem for an FTP download function using Python's ftplib, the block ftp.set_pasv(True) is marked as a distractor. Why is it unnecessary? [În problema Parsons pentru o funcție de descărcare FTP folosind ftplib din Python, blocul ftp.set_pasv(True) este marcat ca distractor. De ce este inutil?]

- **a) Passive mode is the default in Python's ftplib [Modul pasiv este implicit în ftplib din Python]**
- **b) Active mode is always used for downloads [Modul activ este întotdeauna folosit pentru descărcări]**
- **c) The retrbinary method automatically enables passive mode [Metoda retrbinary activează automat modul pasiv]**
- **d) The FTP protocol does not support passive mode in Python [Protocolul FTP nu acceptă modul pasiv în Python]**

> 💡 **Feedback:** Python's ftplib.FTP defaults to passive mode, so explicitly calling set_pasv(True) is redundant and not needed in the correct solution. A common misconception is that FTP clients default to active mode and require explicit passive mode activation, but Python's ftplib adopted passive mode as the default due to its superior NAT compatibility. [ftplib.FTP din Python folosește implicit modul pasiv, deci apelarea explicită a set_pasv(True) este redundantă și nu este necesară în soluția corectă. O concepție greșită frecventă este că clienții FTP folosesc implicit modul activ și necesită activarea explicită a modului pasiv, dar ftplib din Python a adoptat modul pasiv ca implicit datorită compatibilității superioare cu NAT.]

---

### 52. `Multiple Choice – Alegere multiplă`
**N10.S04.Q06: FTP credential visibility in network captures / Vizibilitatea datelor de autentificare FTP în capturile de rețea**

> You capture network traffic on a host running an FTP server and observe USER test and PASS 12345 in plaintext. Which statement best explains this? [Capturați traficul de rețea pe o gazdă care rulează un server FTP și observați USER test și PASS 12345 în text clar. Care afirmație explică cel mai bine acest lucru?]

- **a) Standard FTP transmits everything in plaintext, including credentials [FTP standard transmite totul în text clar, inclusiv datele de autentificare]**
- **b) The FTP server is misconfigured and should encrypt credentials by default [Serverul FTP este configurat greșit și ar trebui să cripteze datele de autentificare implicit]**
- **c) FTP encrypts data after login, so only the authentication is plaintext [FTP criptează datele după autentificare, deci doar autentificarea este în text clar]**
- **d) Only passive-mode FTP exposes credentials; active mode is encrypted [Doar FTP în modul pasiv expune datele de autentificare; modul activ este criptat]**

> 💡 **Feedback:** Standard FTP (port 21) transmits all data in plaintext, including USER and PASS commands. FTPS or SFTP should be used for sensitive data. This is inherent to the FTP protocol, not a misconfiguration. A common misconception is that visible credentials indicate a server misconfiguration, but plaintext transmission is the fundamental design of the FTP protocol — encryption was never part of the original specification. [FTP standard (portul 21) transmite toate datele în text clar, inclusiv comenzile USER și PASS. FTPS sau SFTP trebuie utilizate pentru date sensibile. Aceasta este o caracteristică inerentă protocolului FTP, nu o eroare de configurare. O concepție greșită frecventă este că datele de autentificare vizibile indică o eroare de configurare a serverului, dar transmisia în text clar este designul fundamental al protocolului FTP — criptarea nu a fost niciodată parte din specificația originală.]

---
