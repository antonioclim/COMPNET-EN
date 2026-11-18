# Week 10 — Computer Networks
### *Rețele de Calculatoare — Săptămâna 10*

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

### Q4. `N10.C01.Q05` — TLS handshake step ordering / Ordinea pașilor handshake-ului TLS

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

Which simplified message ordering is valid for a full, server-authenticated TLS 1.3 handshake with no resumption, HelloRetryRequest, client certificate or 0-RTT? Application data is omitted. [Ce ordine simplificată este validă pentru un handshake TLS 1.3 complet, cu autentificarea serverului, fără reluare, HelloRetryRequest, certificat client sau 0-RTT? Datele aplicației sunt omise.]

- **a)** ClientHello (key_share) → ServerHello (key_share) → encrypted EncryptedExtensions, Certificate, CertificateVerify, Finished → client Finished
- **b)** ServerHello → ClientHello → client Finished → Certificate
- **c)** ClientHello → plaintext Certificate → ServerHello → ClientKeyExchange
- **d)** ClientHello → application plaintext → ServerHello → Finished

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** TLS 1.3 exchanges ephemeral key shares in the hello messages. Handshake messages after ServerHello are encrypted; CertificateVerify authenticates the server signature and Finished authenticates the handshake transcript. ClientKeyExchange is a TLS 1.2 message, not a TLS 1.3 step. See RFC 9846 §2 (which supersedes RFC 8446). [TLS 1.3 schimbă componentele efemere de cheie în mesajele hello. Mesajele handshake după ServerHello sunt criptate; CertificateVerify autentifică semnătura serverului, iar Finished autentifică transcrierea handshake-ului. ClientKeyExchange aparține TLS 1.2, nu TLS 1.3. Vezi RFC 9846 §2, care înlocuiește RFC 8446.]

</details>

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

### Q8. `N10.C02.Q02` — Identifying Richardson Maturity Level for action-style endpoints / Identificarea nivelului de maturitate Richardson pentru endpoint-uri cu acțiuni în cale

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

An API has distinct resource URIs such as /users/123 and /orders/7. Every operation uses POST and successful or failed application outcomes are returned inside 200 bodies. There are no hypermedia controls. What Richardson level is demonstrated? [Un API are URI-uri distincte pentru resurse, precum /users/123 și /orders/7. Toate operațiile folosesc POST, iar succesul sau eșecul aplicației sunt în corpuri 200. Nu există controale hypermedia. Ce nivel Richardson este demonstrat?]

- **a)** Level 1: resource identities, without the method/status semantics of Level 2 [Nivelul1: identitatea resurselor, fără semantica metodelor/codurilor de la nivelul 2]
- **b)** Level 0 because every URI is identical [Nivelul0 deoarece toate URI-urile sunt identice]
- **c)** Level 2 because any use of POST proves correct HTTP semantics [Nivelul2 deoarece orice folosire POST dovedește semantica HTTP corectă]
- **d)** Level 3 because numeric IDs are hypermedia [Nivelul3 deoarece ID-urile numerice sunt hypermedia]

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** The complete API description supports Level 1. A single action-like path does not establish a maturity level; HTTP POST can legitimately perform application-specific actions. Level 2 adds meaningful HTTP methods/statuses and Level 3 adds hypermedia controls. [Descrierea completă a API-ului susține nivelul 1. O singură cale denumită ca acțiune nu stabilește nivelul; POST poate efectua legitim acțiuni specifice aplicației. Nivelul2 adaugă semantica HTTP a metodelor/codurilor, iar nivelul 3 controale hypermedia.]

</details>

---

### Q9. `N10.C02.Q03` — HTTP status code for successful resource creation / Codul de stare HTTP pentru crearea cu succes a unei resurse

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

A request has completed and created a new resource. Which status explicitly communicates that outcome? [O cerere s-a încheiat și a creat o resursă nouă. Ce cod comunică explicit acest rezultat?]

- **a)** 201 Created
- **b)** 200 OK
- **c)** 204 No Content
- **d)** 301 Moved Permanently

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** 201 identifies successful creation. Location can identify the primary new resource.200 is general success and 204 is success without response content; neither is universally tied to GET/PUT or DELETE. Status choice follows the actual outcome, not a rigid one-method/one-code mapping. [201 identifică o creare reușită. Location poate identifica resursa principală nouă.200 reprezintă succes general, iar 204 succes fără conținut în răspuns; acestea nu sunt legate universal de GET/PUT sau DELETE. Codul se alege după rezultat, nu printr-o corespondență rigidă metodă/cod.]

</details>

---

### 10. `Multiple Choice – Alegere multiplă`
**N10.C02.Q04: What HATEOAS adds to a Level 2 API / Ce adaugă HATEOAS unui API de Nivelul 2**

> What is the defining characteristic that elevates a REST API from Richardson Level 2 to Level 3? [Care este caracteristica definitorie care ridică un API REST de la Nivelul Richardson 2 la Nivelul 3?]

- **a) Responses include hypermedia links to related resources and available actions [Răspunsurile includ legături hypermedia către resursele asociate și acțiunile disponibile]**
- **b) The API uses JSON instead of XML as the response format [API-ul folosește JSON în loc de XML ca format de răspuns]**
- **c) All endpoints require OAuth 2.0 authentication [Toate endpoint-urile necesită autentificare OAuth 2.0]**
- **d) The API supports real-time WebSocket push connections alongside standard request-response patterns [API-ul acceptă conexiuni WebSocket în timp real alături de modelele standard cerere-răspuns]**

> 💡 **Feedback:** Richardson Level 3 adds hypermedia controls describing available transitions and related resources. Clients still need an entry point and knowledge of media types/link relations. It does not require a body containing links in literally every response: for example,204 has no content. JSON or authentication alone does not establish Level 3. [Nivelul Richardson3 adaugă controale hypermedia care descriu tranzițiile disponibile și resursele asociate. Clienții au nevoie în continuare de un punct de intrare și de semantica tipurilor media/relațiilor. Nu cere un corp cu legături în absolut fiecare răspuns: de exemplu 204 nu are conținut. JSON sau autentificarea singure nu stabilesc nivelul 3.]

---

### Q11. `N10.C02.Q05` — Idempotency of HTTP methods / Idempotența metodelor HTTP

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

Which method does HTTP not guarantee to be idempotent: repeated identical requests need not have the same intended server effect as one request? [Pentru care metodă HTTP nu garantează idempotența: cererile identice repetate nu trebuie să aibă același efect intenționat ca una singură?]

- **a)** POST
- **b)** GET
- **c)** PUT
- **d)** DELETE

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** POST is not guaranteed idempotent by its method semantics, although an application may provide idempotent operations or an idempotency-key contract. GET, PUT and DELETE are idempotent in intended effect. Responses, timestamps and incidental logging can differ across repetitions. [POST nu garantează idempotența prin semantica metodei, deși aplicația poate oferi operații idempotente sau un contract cu cheie de idempotență. GET, PUT și DELETE sunt idempotente ca efect intenționat. Răspunsurile, marcajele de timp și jurnalizarea incidentală pot diferi între repetări.]

</details>

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

### Q14. `N10.C02.Q09` — CRUD to HTTP verb mapping / Corespondența CRUD cu verbele HTTP

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

For an API that creates a resource at a server-selected URI, retrieves a representation, fully replaces a resource at a known URI and removes that resource, which conventional mapping fits? [Pentru un API care creează o resursă la un URI ales de server, citește reprezentarea, înlocuiește complet resursa de la un URI cunoscut și o elimină, ce corespondență convențională este adecvată?]

- **a)** Create via collection POST; read via GET; full replacement via PUT; remove via DELETE
- **b)** Create via GET; read via POST; replace via DELETE; remove via PUT
- **c)** Create via HEAD; read via OPTIONS; replace via GET; remove via PATCH
- **d)** Use GET for every state-changing operation

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** These assumptions make the mapping unambiguous. PUT may also create a resource at a client-chosen URI; POST is a general processing method, not a synonym for create. PATCH applies partial modification instructions and is not guaranteed idempotent. [Ipotezele fac corespondența neambiguă. PUT poate și crea o resursă la un URI ales de client; POST este o metodă generală de procesare, nu un sinonim pentru creare. PATCH aplică instrucțiuni de modificare parțială și nu garantează idempotența.]

</details>

---

### 15. `Multiple Choice – Alegere multiplă`
**N10.C03.Q01: DNS transport protocols / Protocoalele de transport DNS**

> Which transport protocol(s) does DNS use on port 53? [Ce protocol(oale) de transport folosește DNS pe portul 53?]

- **a) Both UDP and TCP, depending on response size and transfer type [Atât UDP cât și TCP, în funcție de dimensiunea răspunsului și tipul transferului]**
- **b) UDP only on port 53 for all queries and zone transfers regardless of size [Doar UDP pe portul 53 pentru toate interogările și transferurile de zonă indiferent de dimensiune]**
- **c) TCP only for reliability [Doar TCP pentru fiabilitate]**
- **d) UDP on port 53 for standard queries with TCP on port 80 for larger responses [UDP pe portul 53 pentru interogări standard cu TCP pe portul 80 pentru răspunsuri mai mari]**

> 💡 **Feedback:** Conventional DNS supports UDP and TCP on port 53. 512 octets is the historical UDP limit without EDNS; EDNS can advertise larger UDP messages. A truncated UDP response normally triggers TCP retry. AXFR uses TCP; an IXFR response may fit in UDP. TCP can also be chosen without prior truncation. [DNS convențional acceptă UDP și TCP pe portul 53. 512 octeți este limita istorică UDP fără EDNS; EDNS poate anunța mesaje UDP mai mari. Un răspuns UDP trunchiat determină în mod normal reîncercarea TCP. AXFR folosește TCP; un răspuns IXFR poate încăpea în UDP. TCP poate fi ales și fără trunchiere prealabilă.]

---

### 16. `Multiple Choice – Alegere multiplă`
**N10.C03.Q02: DNS TC (truncation) bit client behaviour / Comportamentul clientului la bitul TC (trunchiere) DNS**

> A DNS client receives a response with the TC (truncation) bit set. What is the correct next step? [Un client DNS primește un răspuns cu bitul TC (trunchiere) setat. Care este pasul corect următor?]

- **a) Retry the same query using TCP instead of UDP [Reîncercarea aceleiași interogări folosind TCP în loc de UDP]**
- **b) Accept the truncated response as final [Acceptarea răspunsului trunchiat ca definitiv]**
- **c) Switch to a different DNS server [Schimbarea la un alt server DNS]**
- **d) Increase the local UDP buffer size and retry over UDP [Mărirea dimensiunii buffer-ului UDP local și reîncercarea prin UDP]**

> 💡 **Feedback:** TC in the UDP response indicates truncation, so a conventional client normally retries over TCP for the complete answer. DNS over TCP uses a two-byte length prefix and supports at most 65535 octets per DNS message; a zone transfer can contain multiple messages. EDNS permits UDP payloads above the old 512-octet limit. [TC în răspunsul UDP indică trunchiere, deci un client convențional reîncearcă în mod normal prin TCP pentru răspunsul complet. DNS prin TCP folosește un prefix de lungime pe doi octeți și permite cel mult 65535 de octeți pe mesaj DNS; un transfer de zonă poate conține mai multe mesaje. EDNS permite payload-uri UDP peste vechea limită de 512 octeți.]

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

> A local DNS cache alone guarantees that an upstream resolver or network observer cannot learn any queried domain. [Un cache DNS local singur garantează că un resolver din amonte sau observator de rețea nu poate afla niciun domeniu interogat.]

- **a) true**
- **b) false**

> 💡 **Feedback:** False. Cache hits reduce repeated upstream queries and can therefore reduce exposure, but cache misses still require resolution. DoT/DoH protect the client-to-resolver transport against passive observers; the selected resolver still sees the queries it handles. Cache contents themselves also need appropriate access controls. [Fals. Răspunsurile din cache reduc interogările repetate în amonte și pot reduce expunerea, dar cazurile absente cer rezolvare. DoT/DoH protejează transportul client-resolver față de observatori pasivi; resolverul ales vede interogările pe care le gestionează. Și conținutul cache-ului necesită control adecvat al accesului.]

---

### Q20. `N10.C04.Q03` — SSH key authentication versus password authentication / Autentificarea SSH prin chei versus autentificarea prin parolă

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

What is a security advantage of correctly configured SSH public-key authentication compared with a reusable password? [Care este un avantaj de securitate al autentificării SSH cu cheie publică configurate corect față de o parolă reutilizabilă?]

- **a)** The authentication exchange sends a signature proving possession of the private key, not the private key itself [Schimbul de autentificare trimite o semnătură care demonstrează posesia cheii private, nu cheia privată]
- **b)** Every SSH key has 2048 bits of security regardless of algorithm [Orice cheie SSH are 2048 de biți de securitate indiferent de algoritm]
- **c)** A private key cannot be stolen or copied [O cheie privată nu poate fi furată sau copiată]
- **d)** Host-key verification is unnecessary when public keys are used [Verificarea cheii gazdei nu este necesară când se folosesc chei publice]

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** The private key is not transmitted by SSH authentication; the client signs session-bound authentication data. Key length depends on the algorithm and is not equivalent to security strength. Protect private keys/agents and verify host keys: endpoint compromise, malicious hosts and agent misuse remain risks. Password authentication also uses the encrypted SSH transport. [Cheia privată nu este transmisă de autentificarea SSH; clientul semnează date de autentificare legate de sesiune. Lungimea cheii depinde de algoritm și nu este echivalentă cu rezistența criptografică. Protejați cheile/agenții și verificați cheile gazdei: compromiterea endpoint-ului, gazdele malițioase și utilizarea abuzivă a agentului rămân riscuri. Și autentificarea cu parolă folosește transportul SSH criptat.]

</details>

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

> 💡 **Feedback:** TC in the UDP response indicates truncation, so a conventional client normally retries over TCP for the complete answer. DNS over TCP uses a two-byte length prefix and supports at most 65535 octets per DNS message; a zone transfer can contain multiple messages. EDNS permits UDP payloads above the old 512-octet limit. [TC în răspunsul UDP indică trunchiere, deci un client convențional reîncearcă în mod normal prin TCP pentru răspunsul complet. DNS prin TCP folosește un prefix de lungime pe doi octeți și permite cel mult 65535 de octeți pe mesaj DNS; un transfer de zonă poate conține mai multe mesaje. EDNS permite payload-uri UDP peste vechea limită de 512 octeți.]

---

### Q30. `N10.T00.Q05` — HTTPS padlock misconception / Concepția greșită despre lacătul HTTPS

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

A browser reports a successfully validated HTTPS connection to bank.example. What can be concluded from that connection indicator alone? [Un browser raportează o conexiune HTTPS validată reușit către bank.example. Ce se poate deduce doar din indicatorul conexiunii?]

- **a)** The connection has TLS protection and certificate identity validation for that hostname; the site may still be deceptive or harmful [Conexiunea are protecție TLS și validarea identității certificatului pentru acel nume; site-ul poate fi totuși înșelător sau dăunător]
- **b)** The operator's business practices have been audited [Practicile comerciale ale operatorului au fost auditate]
- **c)** All downloads are harmless [Toate descărcările sunt inofensive]
- **d)** The site cannot be used for phishing [Site-ul nu poate fi folosit pentru phishing]

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** TLS authenticates the endpoint identity according to the certificate trust model and protects the connection. It does not certify honesty, application security or data-storage practices. Browser icon designs vary, so reason from the validated connection, not a particular padlock graphic. [TLS autentifică identitatea endpoint-ului conform modelului de încredere al certificatelor și protejează conexiunea. Nu certifică onestitatea, securitatea aplicației sau practicile de stocare. Grafica indicatoarelor diferă între browsere, deci raționați pornind de la conexiunea validată, nu de la un anumit lacăt.]

</details>

---

### 31. `Multiple Choice – Alegere multiplă`
**N10.T00.Q06: HTTP idempotency and method semantics / Idempotența HTTP și semantica metodelor**

> Assume each successful POST creates a fresh user and there is no application deduplication or idempotency key. A developer accidentally sends the same PUT /api/users/10 request three times due to a network retry. A second developer sends the same POST /api/users request three times. What is the most likely outcome for each? [Presupuneți că fiecare POST reușit creează un utilizator nou și nu există deduplicare sau cheie de idempotență. Un dezvoltator trimite accidental aceeași cerere PUT /api/users/10 de trei ori din cauza unei reîncercări de rețea. Un al doilea dezvoltator trimite aceeași cerere POST /api/users de trei ori. Care este rezultatul cel mai probabil pentru fiecare?]

- **a) PUT: user 10 is updated to the same state (one user); POST: three new users are created [PUT: utilizatorul 10 este actualizat la aceeași stare (un utilizator); POST: trei utilizatori noi sunt creați]**
- **b) Both create three separate entries because HTTP has no built-in duplicate detection [Ambele creează trei intrări separate deoarece HTTP nu are detecție de duplicate integrată]**
- **c) PUT: three versions of user 10 are stored; POST: only one user is created [PUT: trei versiuni ale utilizatorului 10 sunt stocate; POST: doar un utilizator este creat]**
- **d) Both update a single record because the server detects identical request bodies, which does not accurately reflect how modern implementations handle the key exchange procedure [Ambele actualizează o singură înregistrare deoarece serverul detectează corpuri de cerere identice, ceea ce nu reflectă cu acuratețe modul în care implementările moderne gestionează procedura de schimb de chei]**

> 💡 **Feedback:** Under the stated application contract, the three PUTs leave user 10 with the same intended state and the three POSTs create three users. Idempotence concerns intended state, not identical response bodies or the absence of logging. POST behaviour is application-defined, so the creation/deduplication assumptions are necessary. [Conform contractului aplicației, cele trei PUT-uri lasă utilizatorul 10 în aceeași stare intenționată, iar cele trei POST-uri creează trei utilizatori. Idempotența privește starea intenționată, nu identitatea răspunsurilor sau absența jurnalizării. Comportamentul POST este definit de aplicație, deci ipotezele despre creare/deduplicare sunt necesare.]

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

### Q34. `N10.T00.Q09` — SSH key authentication security / Securitatea autentificării SSH bazate pe chei

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

In SSH public-key authentication, what does the client prove without transmitting the reusable private key? [În autentificarea SSH cu cheie publică, ce dovedește clientul fără transmiterea cheii private reutilizabile?]

- **a)** Possession of the signing key through a signature bound to the SSH session [Posesia cheii de semnare printr-o semnătură legată de sesiunea SSH]
- **b)** That the server is honest without checking its host key [Că serverul este onest fără verificarea cheii gazdei]
- **c)** That its private key cannot exist on another computer [Că cheia privată nu poate exista pe alt calculator]
- **d)** That all SSH algorithms have the same key length [Că toți algoritmii SSH au aceeași lungime a cheii]

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** The signature proof is the authentication mechanism. It does not eliminate credential theft, unsafe agent forwarding or malicious-server risks. Host-key verification and local private-key protection remain necessary;2048-bit RSA is not 2048-bit security and other SSH algorithms use different sizes. [Dovada prin semnătură este mecanismul de autentificare. Nu elimină furtul de credențiale, redirecționarea nesigură a agentului sau riscurile serverelor malițioase. Verificarea cheii gazdei și protecția locală a cheii private rămân necesare; RSA pe 2048 de biți nu înseamnă 2048 de biți de securitate, iar alți algoritmi SSH folosesc alte dimensiuni.]

</details>

---

### Q35. `N10.T00.Q10` — DNS record type selection / Selectarea tipului de înregistrare DNS

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

www.example.com has no other ordinary records and must follow the address records of example.com automatically when they change. Which DNS record expresses that alias? [www.example.com nu are alte înregistrări obișnuite și trebuie să urmeze automat înregistrările de adresă pentru example.com când acestea se schimbă. Ce înregistrare DNS exprimă aliasul?]

- **a)** www.example.com. CNAME example.com.
- **b)** A second A record whose address must be edited separately
- **c)** An MX record naming an email destination
- **d)** An NS record delegating a child zone

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** CNAME makes the owner name an alias. Duplicating an A value could produce the same address now but would not encode the requested alias relationship. DNS aliasing is not an HTTP redirect and does not change the URL displayed by a browser. [CNAME face din numele proprietar un alias. Duplicarea unei valori A poate produce aceeași adresă acum, dar nu exprimă relația de alias cerută. Aliasul DNS nu este o redirecționare HTTP și nu modifică URL-ul afișat de browser.]

</details>

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

### Q40. `N10.S01.Q03` — TLS state machine — calling server_hello before client_hello / Mașina de stări TLS — apelarea server_hello înainte de client_hello

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

Run this independent state-machine illustration. What does the final call return? It is not a TLS implementation. [Rulați această ilustrare independentă de mașină de stări. Ce returnează ultimul apel? Nu este o implementare TLS.]

```python
class HandshakeModel:
    def __init__(self):
        self.state = "INIT"
    def server_hello(self):
        if self.state != "CLIENT_HELLO":
            return f"error: invalid state {self.state}"
        self.state = "SERVER_HELLO"
        return self.state

print(HandshakeModel().server_hello())
```

- **a)** "error: invalid state INIT"
- **b)** "SERVER_HELLO"
- **c)** None
- **d)** An automatic call to client_hello()

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** The guard requires CLIENT_HELLO; the new object is in INIT, so the stated error string is returned. This is a deliberately small code-tracing contract, not a claim about all TLS states or wire messages. [Garda cere CLIENT_HELLO; obiectul nou este în INIT, deci returnează șirul de eroare indicat. Este un contract mic pentru trasarea codului, nu o afirmație despre toate stările sau mesajele TLS.]

</details>

---

### Q41. `N10.S01.Q04` — SSL context wrap_socket and server_hostname parameter / Contextul SSL wrap_socket și parametrul server_hostname

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

Assume sock is connected and context = ssl.create_default_context(). What does context.wrap_socket(sock, server_hostname="www.example.test") use that DNS hostname for? [Presupuneți că sock este conectat și context = ssl.create_default_context(). La ce folosește context.wrap_socket(sock, server_hostname="www.example.test") acel nume DNS?]

- **a)** Certificate hostname verification and SNI for the requested DNS hostname [Verificarea numelui din certificat și SNI pentru numele DNS cerut]
- **b)** Choosing a DNS resolver address [Alegerea adresei resolverului DNS]
- **c)** Disabling certificate-chain validation [Dezactivarea validării lanțului certificatului]
- **d)** Selecting an encryption algorithm by hostname spelling [Alegerea algoritmului de criptare după forma numelui]

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** With the validating default client context, server_hostname supplies the reference identity for hostname verification. A DNS name also enables SNI so a virtual-host server can select a certificate. It does not resolve the name or make an untrusted certificate trustworthy. [Cu contextul client implicit care validează, server_hostname furnizează identitatea de referință pentru verificarea numelui. Un nume DNS permite și SNI pentru selectarea certificatului pe serverul virtual. Nu rezolvă numele și nu transformă un certificat neacceptat într-unul de încredere.]

</details>

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

### Q43. `N10.S02.Q02` — Code tracing — route_request output for non-numeric user ID / Trasarea codului — rezultatul route_request pentru un ID de utilizator non-numeric

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

In this self-contained dispatcher example, what does route_request('GET','/api/users/abc') return? [În acest dispatcher autonom, ce returnează route_request('GET','/api/users/abc')?]

```python
def route_request(method, path):
    if path == "/api/users":
        if method == "GET":
            return "List all users", 200
        if method == "POST":
            return "Create user", 201
        return "Method not allowed", 405
    parts = path.split("/")
    if len(parts) == 4 and parts[1:3] == ["api", "users"] and parts[3].isdigit():
        if method == "GET":
            return f"Get user {parts[3]}", 200
        if method in ("PUT", "DELETE"):
            return "Updated or deleted", 200
        return "Method not allowed", 405
    return "Not found", 404

print(route_request('GET', '/api/users/abc'))
```

- **a)** ("Not found",404)
- **b)** ("List all users",200)
- **c)** ("Create user",201)
- **d)** A ValueError exception

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** Follow the explicit path and method guards. This function returns a teaching tuple, not a complete HTTP response; a real 405 response must also include Allow. No omitted repository exercise is needed to determine the answer. [Urmăriți gărzile explicite pentru cale și metodă. Funcția returnează un tuplu didactic, nu un răspuns HTTP complet; un răspuns 405 real trebuie să includă și Allow. Răspunsul nu depinde de un exercițiu omis din repository.]

</details>

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

### Q45. `N10.S02.Q04` — Code tracing — route_request output for PATCH on /api/users / Trasarea codului — rezultatul route_request pentru PATCH pe /api/users

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

In this self-contained dispatcher example, what does route_request('PATCH','/api/users') return? [În acest dispatcher autonom, ce returnează route_request('PATCH','/api/users')?]

```python
def route_request(method, path):
    if path == "/api/users":
        if method == "GET":
            return "List all users", 200
        if method == "POST":
            return "Create user", 201
        return "Method not allowed", 405
    parts = path.split("/")
    if len(parts) == 4 and parts[1:3] == ["api", "users"] and parts[3].isdigit():
        if method == "GET":
            return f"Get user {parts[3]}", 200
        if method in ("PUT", "DELETE"):
            return "Updated or deleted", 200
        return "Method not allowed", 405
    return "Not found", 404

print(route_request('PATCH', '/api/users'))
```

- **a)** ("Method not allowed",405)
- **b)** ("List all users",200)
- **c)** ("Create user",201)
- **d)** A ValueError exception

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** Follow the explicit path and method guards. This function returns a teaching tuple, not a complete HTTP response; a real 405 response must also include Allow. No omitted repository exercise is needed to determine the answer. [Urmăriți gărzile explicite pentru cale și metodă. Funcția returnează un tuplu didactic, nu un răspuns HTTP complet; un răspuns 405 real trebuie să includă și Allow. Răspunsul nu depinde de un exercițiu omis din repository.]

</details>

---

### Q46. `N10.S03.Q03` — Code tracing — DNS resolver with trailing dot / Trasarea codului — rezolvor DNS cu punct final

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

In this standalone dictionary model, which status does the final call produce? [În acest model autonom bazat pe dicționar, ce status produce ultimul apel?]

```python
records = {"web.lab.local": "192.0.2.10"}
def resolve_dns(query_name):
    key = query_name.rstrip(".").lower()
    return {"status": "NOERROR" if key in records else "NXDOMAIN"}

print(resolve_dns("web.lab.local.")["status"])
```

- **a)** NOERROR
- **b)** NXDOMAIN
- **c)** SERVFAIL
- **d)** None

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** rstrip removes the trailing dot before dictionary lookup, so the key exists. The terminal dot represents the DNS root in an absolute name. This toy model does not perform DNS traffic, implement delegation or model every DNS response case. [rstrip elimină punctul final înaintea căutării în dicționar, deci cheia există. Punctul terminal reprezintă rădăcina DNS într-un nume absolut. Modelul simplificat nu generează trafic DNS, nu implementează delegare și nu acoperă toate răspunsurile DNS.]

</details>

---

### Q47. `N10.S03.Q05` — Socket type for UDP DNS queries in Python / Tipul de socket pentru interogări DNS UDP în Python

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

Which type creates a UDP/IPv4 socket in socket.socket(socket.AF_INET, type)? [Ce tip creează un socket UDP/IPv4 în socket.socket(socket.AF_INET, type)?]

- **a)** socket.SOCK_DGRAM
- **b)** socket.SOCK_STREAM
- **c)** socket.SOCK_RAW
- **d)** socket.SOCK_SEQPACKET

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** For AF_INET with the default protocol, SOCK_DGRAM selects UDP. The address family matters: datagram sockets also exist for other families. Conventional DNS can use both UDP and TCP; this question explicitly asks for UDP. [Pentru AF_INET cu protocolul implicit, SOCK_DGRAM selectează UDP. Familia de adrese contează: există socket-uri de datagramă și pentru alte familii. DNS convențional poate folosi UDP și TCP; aici se cere explicit UDP.]

</details>

---

### Q48. `N10.S04.Q02` — Python library for SSH automation / Biblioteca Python pentru automatizarea SSH

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

Which library does 04_SEMINARS/S10/3_ssh/ssh-client/S10_Part03_Script_Paramiko_Client.py import for SSHClient? [Ce bibliotecă importă 04_SEMINARS/S10/3_ssh/ssh-client/S10_Part03_Script_Paramiko_Client.py pentru SSHClient?]

- **a)** paramiko
- **b)** pexpect
- **c)** fabric
- **d)** subprocess

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** The canonical S10 client imports Paramiko and creates paramiko.SSHClient(). subprocess could run an external ssh executable, but it is not the library used by this file. [Clientul canonic S10 importă Paramiko și creează paramiko.SSHClient(). subprocess ar putea lansa un executabil ssh extern, dar nu este biblioteca utilizată de acest fișier.]

</details>

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


## Repository context and reference points

Canonical practical material: [S10](../../04_SEMINARS/S10/README.md) — DNS, SSH automation and forwarding. Code-tracing models explicitly introduced in this question pool are self-contained exercises, not promises of additional files or features in that seminar. [Material practic canonic: S10. Modelele de trasare introduse explicit sunt exerciții autonome, nu promisiuni de fișiere sau funcții suplimentare în seminar.]

Protocol semantics: RFC 9110, *HTTP Semantics*. https://doi.org/10.17487/RFC9110

TLS 1.3: [RFC 9846](https://www.rfc-editor.org/rfc/rfc9846), superseding RFC 8446. SSH authentication: RFC 4252. https://doi.org/10.17487/RFC4252
