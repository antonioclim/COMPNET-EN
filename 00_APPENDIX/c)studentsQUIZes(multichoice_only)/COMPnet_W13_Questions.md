# Week 13 — Computer Networks
### *Rețele de Calculatoare — Săptămâna 13*

> Question Pool — Practice Set

---

## 📚 W13 — Curs / Lecture   (41 questions)

---

### Q1. `N13.C01.Q01`
**Standard MQTT plaintext port / Portul standard MQTT în text clar**

*Multiple Choice*

> Which port number is designated by IANA for unencrypted MQTT connections? [Ce număr de port este desemnat de IANA pentru conexiuni MQTT necriptate?]

- **a)** 1883 [1883]
- **b)** 8080 [8080]
- **c)** 443 [443]
- **d)** 8883 [8883]

<details><summary>💡 Feedback</summary>

MQTT uses port 1883 for plaintext and 8883 for TLS. Confusing the two is common, but 1883 is always the unencrypted listener. [MQTT folosește portul 1883 pentru text clar și 8883 pentru TLS. Confundarea lor este frecventă, dar 1883 este întotdeauna ascultătorul necriptat.]

</details>

---

### Q2. `N13.C01.Q02`
**Core MQTT publish-subscribe components / Componentele fundamentale ale modelului MQTT publicare-abonare**

*Multiple Choice*

> Which three components form the core of the MQTT publish-subscribe architecture? [Care sunt cele trei componente care formează nucleul arhitecturii MQTT de tip publicare-abonare?]

- **a)** Client, Server, Database backend [Client, Server, Backend de baze de date]
- **b)** Publisher, Broker, Subscriber [Publicator, Broker, Abonat]
- **c)** Sender, Router, Receiver [Expeditor, Ruter, Destinatar]
- **d)** Producer, Queue, Consumer [Producător, Coadă, Consumator]

<details><summary>💡 Feedback</summary>

MQTT uses the Publisher-Broker-Subscriber triad. The broker mediates all routing between clients. This differs from traditional message queues that use point-to-point delivery. [MQTT utilizează triada Publicator-Broker-Abonat. Brokerul mediază întreaga rutare între clienți. Acest model diferă de cozile de mesaje tradiționale ce utilizează livrarea punct-la-punct.]

</details>

---

### Q3. `N13.C01.Q03`
**Primary function of an MQTT broker / Funcția principală a unui broker MQTT**

*Multiple Choice*

> What is the primary function of the broker in an MQTT architecture? [Care este funcția principală a brokerului într-o arhitectură MQTT?]

- **a)** Encrypts all messages automatically before forwarding them to any subscriber [Criptează automat toate mesajele înainte de a le retransmite către orice abonat]
- **b)** Receives published messages and routes them to subscribers based on topic matching [Primește mesajele publicate și le rutează către abonați pe baza potrivirii topicurilor]
- **c)** Stores all messages permanently in a database for later retrieval by any client [Stochează permanent toate mesajele într-o bază de date pentru recuperarea ulterioară de către orice client]
- **d)** Establishes direct TCP connections between each publisher and every subscriber [Stabilește conexiuni TCP directe între fiecare publicator și fiecare abonat]

<details><summary>💡 Feedback</summary>

The broker receives messages from publishers and routes them to clients subscribed to matching topics. It does not process or modify payloads. [Brokerul primește mesaje de la publicatori și le rutează către clienții abonați la topicuri corespunzătoare. Nu procesează și nu modifică conținutul mesajelor.]

</details>

---

### Q4. `N13.C01.Q04`
**MQTT topics use forward-slash hierarchy / Topicurile MQTT utilizează ierarhia cu bară oblică**

*True / False*

> MQTT topics are structured hierarchically using forward slashes as level separators (e.g., sensors/building1/temperature). [Topicurile MQTT sunt structurate ierarhic utilizând bare oblice ca separatoare de nivel (de ex., sensors/building1/temperature).]

- **a)** true
- **b)** false

<details><summary>💡 Feedback</summary>

Topic hierarchy in MQTT uses forward slashes. This enables wildcard subscriptions using + (single level) and # (multi-level) patterns. [Ierarhia topicurilor MQTT folosește bare oblice. Aceasta permite abonări cu metacaractere utilizând + (un singur nivel) și # (mai multe niveluri).]

</details>

---

### Q5. `N13.C01.Q05`
**MQTT retained message behaviour / Comportamentul mesajelor reținute MQTT**

*Multiple Choice*

> What happens when a new client subscribes to a topic that has a retained message? [Ce se întâmplă când un client nou se abonează la un topic care are un mesaj reținut?]

- **a)** The broker discards all previous messages and starts fresh for the new client [Brokerul elimină toate mesajele anterioare și pornește de la zero pentru noul client]
- **b)** The broker delivers the last retained message immediately upon subscription [Brokerul livrează imediat ultimul mesaj reținut la momentul abonării]
- **c)** The subscriber must wait until a new message is published on that topic [Abonatul trebuie să aștepte până când un mesaj nou este publicat pe acel topic]
- **d)** The subscriber receives the complete message history from when the topic was created [Abonatul primește întregul istoric al mesajelor de la crearea topicului]

<details><summary>💡 Feedback</summary>

The broker stores the last retained message on a topic and delivers it immediately when a new subscriber connects. This ensures subscribers receive the latest known state. [Brokerul stochează ultimul mesaj reținut pe un topic și îl livrează imediat când un abonat nou se conectează. Aceasta asigură că abonații primesc ultima stare cunoscută.]

</details>

---

### Q6. `N13.C01.Q06`
**Last Will and Testament purpose / Scopul funcției Last Will and Testament**

*Multiple Choice*

> What is the purpose of the MQTT Last Will and Testament (LWT) feature? [Care este scopul funcției MQTT Last Will and Testament (LWT)?]

- **a)** It encrypts the final message in a session using the client's private key [Criptează ultimul mesaj dintr-o sesiune folosind cheia privată a clientului]
- **b)** It forces all subscribers to acknowledge receipt before the publisher disconnects [Forțează toți abonații să confirme primirea înainte ca publicatorul să se deconecteze]
- **c)** The broker publishes a pre-registered message if a client disconnects ungracefully [Brokerul publică un mesaj pre-înregistrat dacă un client se deconectează brusc]
- **d)** It permanently logs every message the client ever published for legal compliance [Înregistrează permanent fiecare mesaj publicat de client pentru conformitate legală]

<details><summary>💡 Feedback</summary>

LWT allows a client to register a message that the broker publishes if the client disconnects unexpectedly. This is used for device status monitoring in IoT deployments. [LWT permite unui client să înregistreze un mesaj pe care brokerul îl publică dacă clientul se deconectează neașteptat. Aceasta se utilizează pentru monitorizarea stării dispozitivelor în implementările IoT.]

</details>

---

### Q7. `N13.C02.Q01`
**Single-level wildcard character / Metacaracterul de nivel unic**

*Multiple Choice*

> Which character represents the single-level wildcard in MQTT topic subscriptions? [Ce caracter reprezintă metacaracterul de un singur nivel în abonările la topicuri MQTT?]

- **a)** ? [?]
- **b)** * [*]
- **c)** + [+]
- **d)** # [#]

<details><summary>💡 Feedback</summary>

The + character matches exactly one topic level between slashes. It differs from # which matches zero or more levels but only at the end of a subscription pattern. [Caracterul + se potrivește cu exact un nivel de topic între bare oblice. Diferă de # care se potrivește cu zero sau mai multe niveluri, dar numai la sfârșitul unui model de abonare.]

</details>

---

### Q8. `N13.C02.Q02`
**Topic not matching single-level wildcard / Topicul care nu corespunde metacaracterului de nivel unic**

*Multiple Choice*

> Given the subscription building/+/temperature, which topic does NOT match? [Având abonarea building/+/temperature, care topic NU se potrivește?]

- **a)** building/basement/temperature [building/basement/temperature]
- **b)** building/floor1/temperature [building/floor1/temperature]
- **c)** building/outdoor/temperature [building/outdoor/temperature]
- **d)** building/floor1/room1/temperature [building/floor1/room1/temperature]

<details><summary>💡 Feedback</summary>

The + wildcard matches exactly one level. building/floor1/room1/temperature has two levels between building/ and /temperature, so it fails to match. [Metacaracterul + se potrivește cu exact un nivel. building/floor1/room1/temperature are două niveluri între building/ și /temperature, deci nu se potrivește.]

</details>

---

### Q9. `N13.C02.Q03`
**Multi-level wildcard must be last / Metacaracterul multi-nivel trebuie să fie ultimul**

*True / False*

> The MQTT multi-level wildcard # can only appear as the last character in a subscription filter (e.g., sensors/# is valid, but #/temperature is NOT). [Metacaracterul MQTT multi-nivel # poate apărea doar ca ultimul caracter într-un filtru de abonare (de ex., sensors/# este valid, dar #/temperature NU este).]

- **a)** true
- **b)** false

<details><summary>💡 Feedback</summary>

The # wildcard matches zero or more levels but must be the final token in the subscription string. It cannot appear in the middle of a filter. [Metacaracterul # se potrivește cu zero sau mai multe niveluri, dar trebuie să fie ultimul element din șirul de abonare. Nu poate apărea în mijlocul unui filtru.]

</details>

---

### Q10. `N13.C02.Q04`
**Wildcards used only in subscriptions / Metacaracterele se folosesc doar în abonări**

*True / False*

> MQTT wildcards (+ and #) can be used in both publish and subscribe operations. [Metacaracterele MQTT (+ și #) pot fi utilizate atât în operațiunile de publicare, cât și în cele de abonare.]

- **a)** true
- **b)** false

<details><summary>💡 Feedback</summary>

Wildcards are valid only in subscribe operations. Publishing must always target a specific, concrete topic string without wildcards. [Metacaracterele sunt valide doar în operațiunile de abonare. Publicarea trebuie să vizeze întotdeauna un șir de topic specific, concret, fără metacaractere.]

</details>

---

### Q11. `N13.C02.Q05`
**Multi-level wildcard matching depth / Potrivirea metacaracterului multi-nivel la adâncime**

*Multiple Choice*

> A client subscribes to sensors/#. Which topic will this subscription receive? [Un client se abonează la sensors/#. Ce topic va primi această abonare?]

- **a)** iot/sensors/pressure (sensors is not the first level) [iot/sensors/pressure (sensors nu este primul nivel)]
- **b)** weather/sensors/temperature (different root topic) [weather/sensors/temperature (topic rădăcină diferit)]
- **c)** sensors/building/floor3/room7/humidity [sensors/building/floor3/room7/humidity]
- **d)** sensor/temperature (note: sensor not sensors) [sensor/temperature (notă: sensor nu sensors)]

<details><summary>💡 Feedback</summary>

The # wildcard matches zero or more levels after sensors/. This means sensors/a/b/c/d is matched because # captures all subsequent levels regardless of depth. [Metacaracterul # se potrivește cu zero sau mai multe niveluri după sensors/. Aceasta înseamnă că sensors/a/b/c/d este potrivit deoarece # captează toate nivelurile ulterioare, indiferent de adâncime.]

</details>

---

### Q12. `N13.C03.Q01`
**QoS 0 delivery guarantee / Garanția de livrare QoS 0**

*Multiple Choice*

> What delivery guarantee does MQTT QoS level 0 provide? [Ce garanție de livrare oferă nivelul QoS 0 din MQTT?]

- **a)** Guaranteed delivery with automatic retransmission on timeout [Livrare garantată cu retransmisie automată la expirarea timpului]
- **b)** At-least-once delivery requiring a PUBACK acknowledgement packet [Livrare cel puțin o dată, necesitând un pachet de confirmare PUBACK]
- **c)** At-most-once delivery with no acknowledgement from the broker [Livrare cel mult o dată, fără confirmare din partea brokerului]
- **d)** Exactly-once delivery using a four-step handshake protocol [Livrare exact o dată utilizând un protocol de handshake în patru pași]

<details><summary>💡 Feedback</summary>

QoS 0 is fire-and-forget: the sender transmits once with no acknowledgement. Messages may be lost during network disruptions. [QoS 0 este de tip fire-and-forget: expeditorul transmite o singură dată fără confirmare. Mesajele pot fi pierdute în timpul întreruperilor de rețea.]

</details>

---

### Q13. `N13.C03.Q02`
**QoS 2 four-step handshake / Handshake-ul în patru pași al QoS 2**

*Multiple Choice*

> How many protocol-level messages are exchanged in an MQTT QoS 2 delivery? [Câte mesaje la nivel de protocol se schimbă într-o livrare MQTT QoS 2?]

- **a)** 2 (PUBLISH, PUBACK) [2 (PUBLISH, PUBACK)]
- **b)** 3 (PUBLISH, PUBREC, PUBCOMP) [3 (PUBLISH, PUBREC, PUBCOMP)]
- **c)** 1 (PUBLISH only, fire and forget) [1 (doar PUBLISH, fire and forget)]
- **d)** 4 (PUBLISH, PUBREC, PUBREL, PUBCOMP) [4 (PUBLISH, PUBREC, PUBREL, PUBCOMP)]

<details><summary>💡 Feedback</summary>

QoS 2 uses four messages: PUBLISH, PUBREC, PUBREL, PUBCOMP. This ensures exactly-once delivery at the cost of additional overhead. [QoS 2 utilizează patru mesaje: PUBLISH, PUBREC, PUBREL, PUBCOMP. Aceasta asigură livrarea exact o dată cu costul unui overhead suplimentar.]

</details>

---

### Q14. `N13.C03.Q03`
**QoS 2 does not provide encryption / QoS 2 nu oferă criptare**

*True / False*

> MQTT QoS level 2 provides message encryption as part of its exactly-once delivery guarantee. [Nivelul QoS 2 al MQTT oferă criptarea mesajelor ca parte a garanției de livrare exact o dată.]

- **a)** true
- **b)** false

<details><summary>💡 Feedback</summary>

QoS levels define delivery guarantees only, not security. Encryption requires TLS (port 8883). A common misconception is equating higher QoS with higher security. [Nivelurile QoS definesc doar garanțiile de livrare, nu securitatea. Criptarea necesită TLS (portul 8883). O concepție greșită frecventă este echivalarea unui QoS mai mare cu o securitate mai mare.]

</details>

---

### Q15. `N13.C03.Q04`
**Effective QoS with mismatched levels / QoS efectiv cu niveluri diferite**

*Multiple Choice*

> A publisher sends at QoS 2, but the subscriber is registered with QoS 1. At what effective QoS level will the subscriber receive the message? [Un publicator trimite la QoS 2, dar abonatul este înregistrat cu QoS 1. La ce nivel efectiv de QoS va primi abonatul mesajul?]

- **a)** QoS 2 — the publisher's level always takes precedence over the subscriber's [QoS 2 — nivelul publicatorului are întotdeauna prioritate față de cel al abonatului]
- **b)** The broker rejects the delivery because QoS levels do not match [Brokerul respinge livrarea deoarece nivelurile QoS nu se potrivesc]
- **c)** QoS 1 — the effective level is the minimum of publisher and subscriber QoS [QoS 1 — nivelul efectiv este minimul dintre QoS-ul publicatorului și al abonatului]
- **d)** QoS 0 — mismatched levels cancel each other and default to the lowest [QoS 0 — nivelurile nepotrivite se anulează reciproc și revin la cel mai scăzut]

<details><summary>💡 Feedback</summary>

The effective QoS is the minimum of the publisher's and subscriber's QoS. Since min(2,1)=1, the subscriber receives at QoS 1. [QoS-ul efectiv este minimul dintre QoS-ul publicatorului și cel al abonatului. Deoarece min(2,1)=1, abonatul primește la QoS 1.]

</details>

---

### Q16. `N13.C03.Q05`
**QoS selection for sensor telemetry / Selectarea QoS pentru telemetria senzorilor**

*Multiple Choice*

> For a temperature sensor publishing readings every 5 seconds, which QoS level is most appropriate and why? [Pentru un senzor de temperatură care publică citiri la fiecare 5 secunde, care nivel de QoS este cel mai potrivit și de ce?]

- **a)** QoS 2 — temperature readings are critical sensor data that must arrive exactly once via the four-step handshake to prevent duplicate entries and avoid recording errors [QoS 2 — citirile de temperatură sunt date critice de la senzori care trebuie să sosească exact o dată prin handshake-ul în patru pași pentru a preveni intrările duplicate și a evita erorile de înregistrare]
- **b)** QoS 0 — occasional loss is acceptable given the high publish frequency and constrained device resources [QoS 0 — pierderea ocazională este acceptabilă dată fiind frecvența mare de publicare și resursele limitate ale dispozitivului]
- **c)** No QoS is needed because MQTT always delivers messages reliably over TCP [Nu este nevoie de QoS deoarece MQTT livrează întotdeauna mesajele fiabil prin TCP]
- **d)** QoS 1 — every reading needs acknowledgement to maintain a complete historical record [QoS 1 — fiecare citire necesită confirmare pentru a menține un istoric complet]

<details><summary>💡 Feedback</summary>

QoS 0 suits frequent, non-critical telemetry. If one reading is lost, the next arrives in 5 seconds. The low overhead preserves bandwidth and battery on constrained devices. [QoS 0 se potrivește telemetriei frecvente, necritice. Dacă se pierde o citire, următoarea sosește în 5 secunde. Overhead-ul scăzut conservă lățimea de bandă și bateria pe dispozitivele cu resurse limitate.]

</details>

---

### Q17. `N13.C04.Q01`
**Metadata visible despite TLS encryption / Metadate vizibile în ciuda criptării TLS**

*Multiple Choice*

> When MQTT traffic is encrypted with TLS, which of the following remains visible to a network observer? [Când traficul MQTT este criptat cu TLS, care dintre următoarele rămâne vizibil pentru un observator de rețea?]

- **a)** MQTT topic names and client identifiers used during publish operations [Numele topicurilor MQTT și identificatorii de client utilizați în operațiunile de publicare]
- **b)** Nothing — TLS encrypts all information including IP headers and port numbers [Nimic — TLS criptează toate informațiile, inclusiv antetele IP și numerele de port]
- **c)** The message payload content including sensor readings and commands [Conținutul mesajelor, inclusiv citirile senzorilor și comenzile]
- **d)** Source and destination IP addresses, port numbers, and approximate packet sizes [Adresele IP sursă și destinație, numerele de port și dimensiunea aproximativă a pachetelor]

<details><summary>💡 Feedback</summary>

TLS encrypts application data (topics, payloads, credentials) but network metadata — IP addresses, port numbers, timing, and approximate message sizes — remains observable. [TLS criptează datele aplicației (topicuri, conținut, credențiale), dar metadatele de rețea — adrese IP, numere de port, temporizare și dimensiunea aproximativă a mesajelor — rămân observabile.]

</details>

---

### Q18. `N13.C04.Q02`
**MQTT over TLS standard port / Portul standard pentru MQTT prin TLS**

*Multiple Choice*

> What is the IANA-assigned port number for MQTT over TLS? [Care este numărul de port atribuit de IANA pentru MQTT prin TLS?]

- **a)** 993 [993]
- **b)** 8883 [8883]
- **c)** 1883 [1883]
- **d)** 443 [443]

<details><summary>💡 Feedback</summary>

Port 8883 is the standard for MQTT-over-TLS. Port 1883 is plaintext MQTT. Confusing these two ports is a common error in IoT configuration. [Portul 8883 este standardul pentru MQTT prin TLS. Portul 1883 este MQTT în text clar. Confundarea acestor două porturi este o eroare frecventă în configurarea IoT.]

</details>

---

### Q19. `N13.C04.Q03`
**Three security properties of TLS / Trei proprietăți de securitate ale TLS**

*Multiple Choice*

> Which three security properties does TLS provide for network communications? [Ce trei proprietăți de securitate oferă TLS pentru comunicațiile de rețea?]

- **a)** Authentication, authorisation, and accounting [Autentificare, autorizare și contabilizare]
- **b)** Confidentiality, integrity, and authentication [Confidențialitate, integritate și autentificare]
- **c)** Encryption, compression, and load balancing [Criptare, compresie și echilibrarea încărcăturii]
- **d)** Confidentiality, availability, and non-repudiation [Confidențialitate, disponibilitate și nerepudiere]

<details><summary>💡 Feedback</summary>

TLS provides confidentiality (encryption), integrity (tamper detection via MACs), and authentication (certificate verification). It does not provide authorisation. [TLS oferă confidențialitate (criptare), integritate (detectarea falsificării prin MAC-uri) și autentificare (verificarea certificatelor). Nu oferă autorizare.]

</details>

---

### Q20. `N13.C04.Q04`
**Broker-level limitation of MQTT over TLS / Limitarea MQTT prin TLS la nivelul brokerului**

*Multiple Choice*

> Even when MQTT uses TLS, what security limitation exists at the broker level? [Chiar și când MQTT utilizează TLS, ce limitare de securitate există la nivelul brokerului?]

- **a)** The broker decrypts messages for routing and has full access to plaintext content [Brokerul decriptează mesajele pentru rutare și are acces complet la conținutul în text clar]
- **b)** TLS prevents the broker from reading messages, ensuring end-to-end encryption [TLS împiedică brokerul să citească mesajele, asigurând criptare de la un capăt la altul]
- **c)** The broker cannot verify subscriber identities when TLS is enabled [Brokerul nu poate verifica identitățile abonaților când TLS este activat]
- **d)** TLS disables topic-based routing because encrypted topics cannot be parsed [TLS dezactivează rutarea bazată pe topicuri deoarece topicurile criptate nu pot fi parsate]

<details><summary>💡 Feedback</summary>

TLS encrypts transit only. The broker decrypts messages to route them, so it has access to plaintext content. This means a compromised broker exposes all data. [TLS criptează doar tranzitul. Brokerul decriptează mesajele pentru a le ruta, deci are acces la conținutul în text clar. Aceasta înseamnă că un broker compromis expune toate datele.]

</details>

---

### Q21. `N13.C04.Q05`
**TLS version compatibility / Compatibilitatea versiunilor TLS**

*Multiple Choice*

> Why might a legacy IoT client using only TLS 1.1 fail to connect to a server configured for TLS 1.3? [De ce ar putea un client IoT vechi care folosește doar TLS 1.1 să nu reușească să se conecteze la un server configurat pentru TLS 1.3?]

- **a)** The server automatically downgrades to TLS 1.1 for backwards compatibility [Serverul face automat downgrade la TLS 1.1 pentru compatibilitate]
- **b)** TLS 1.3 removed older cipher suites, so clients limited to TLS 1.1 cannot negotiate a common cipher [TLS 1.3 a eliminat suitele de cifruri vechi, astfel încât clienții limitați la TLS 1.1 nu pot negocia un cifru comun]
- **c)** TLS 1.3 requires IPv6 which legacy devices do not support [TLS 1.3 necesită IPv6 pe care dispozitivele vechi nu îl suportă]
- **d)** TLS 1.1 uses larger certificates that exceed the TLS 1.3 maximum handshake message size, causing negotiation failures during the initial key exchange phase [TLS 1.1 folosește certificate mai mari care depășesc dimensiunea maximă a mesajelor de handshake din TLS 1.3, provocând eșecuri de negociere în timpul fazei inițiale de schimb de chei, care depășesc dimensiunea maximă TLS 1.3]

<details><summary>💡 Feedback</summary>

TLS 1.3 removed deprecated cipher suites from older versions. A TLS 1.1-only client cannot negotiate compatible ciphers, causing the handshake to fail. [TLS 1.3 a eliminat suitele de cifruri depreciate din versiunile anterioare. Un client exclusiv TLS 1.1 nu poate negocia cifruri compatibile, provocând eșecul handshake-ului.]

</details>

---

### Q22. `N13.C05.Q01`
**Top-ranked OWASP IoT vulnerability / Vulnerabilitatea de rang maxim OWASP IoT**

*Multiple Choice*

> According to the OWASP IoT Top 10, which vulnerability category is ranked as the most critical? [Conform OWASP IoT Top 10, care categorie de vulnerabilitate este clasată ca cea mai critică?]

- **a)** I7 — Insecure Data Transfer without transport encryption [I7 — Transfer nesigur de date fără criptare de transport]
- **b)** I1 — Weak, Guessable, or Hardcoded Passwords (OWASP IoT #1) [I1 — Parole slabe, ușor de ghicit sau codificate fix (OWASP IoT #1)]
- **c)** I2 — Insecure Network Services with unnecessary open ports [I2 — Servicii de rețea nesigure cu porturi deschise inutile]
- **d)** I3 — Insecure Ecosystem Interfaces including vulnerable web APIs [I3 — Interfețe nesigure ale ecosistemului, inclusiv API-uri web vulnerabile]

<details><summary>💡 Feedback</summary>

OWASP ranks I1 — Weak, Guessable, or Hardcoded Passwords as the top IoT vulnerability. Devices shipping with default credentials remain trivially exploitable at scale. [OWASP clasează I1 — Parole slabe, ușor de ghicit sau codificate fix ca vulnerabilitatea IoT principală. Dispozitivele livrate cu credențiale implicite rămân exploatabile trivial la scară largă.]

</details>

---

### Q23. `N13.C05.Q02`
**OWASP I2 Insecure Network Services / OWASP I2 servicii de rețea nesigure**

*Multiple Choice*

> A device exposes Telnet and FTP services that are not required for normal operation. Which OWASP IoT category does this represent? [Un dispozitiv expune servicii Telnet și FTP care nu sunt necesare funcționării normale. Ce categorie OWASP IoT reprezintă aceasta?]

- **a)** I1 — Weak, Guessable, or Hardcoded Passwords [I1 — Parole slabe, ușor de ghicit sau codificate fix]
- **b)** I2 — Insecure Network Services [I2 — Servicii de rețea nesigure]
- **c)** I5 — Lack of Secure Update Mechanism [I5 — Lipsa mecanismului de actualizare securizat]
- **d)** I3 — Insecure Ecosystem Interfaces [I3 — Interfețe nesigure ale ecosistemului]

<details><summary>💡 Feedback</summary>

Unnecessary services on device interfaces expand the attack surface. This maps directly to OWASP I2 — Insecure Network Services. [Serviciile inutile pe interfețele dispozitivului extind suprafața de atac. Aceasta corespunde direct categoriei OWASP I2 — Servicii de rețea nesigure.]

</details>

---

### Q24. `N13.C05.Q03`
**Mirai botnet primary attack vector / Vectorul principal de atac al botnetului Mirai**

*Multiple Choice*

> The Mirai botnet successfully compromised approximately 600,000 IoT devices in 2016. What was its primary attack vector? [Botnetul Mirai a compromis cu succes aproximativ 600.000 de dispozitive IoT în 2016. Care a fost vectorul său principal de atac?]

- **a)** Man-in-the-middle attacks on unencrypted MQTT broker communications [Atacuri de tip man-in-the-middle pe comunicațiile MQTT necriptate ale brokerului]
- **b)** Default and factory credentials on cameras, routers, and DVR devices [Credențiale implicite și din fabrică pe camere, routere și dispozitive DVR]
- **c)** Zero-day exploits targeting unpatched firmware on industrial sensors [Exploituri zero-day vizând firmware nepachetuit pe senzori industriali]
- **d)** SQL injection through vulnerable web interfaces on smart home hubs [Injecție SQL prin interfețe web vulnerabile pe hub-uri smart home]

<details><summary>💡 Feedback</summary>

Mirai targeted IoT devices with default or factory credentials (cameras, routers, DVRs). This directly demonstrates why OWASP ranks weak passwords as the top IoT vulnerability. [Mirai a vizat dispozitive IoT cu credențiale implicite sau din fabrică (camere, routere, DVR-uri). Aceasta demonstrează direct de ce OWASP clasează parolele slabe ca vulnerabilitatea IoT principală.]

</details>

---

### Q25. `N13.C05.Q04`
**Simple IoT devices are not safe from attacks / Dispozitivele IoT simple nu sunt sigure împotriva atacurilor**

*True / False*

> IoT devices with minimal functionality (e.g., a temperature sensor that only sends readings) are inherently safe from network attacks because they are too simple to be exploited. [Dispozitivele IoT cu funcționalitate minimală (de ex., un senzor de temperatură care trimite doar citiri) sunt inerent sigure împotriva atacurilor de rețea deoarece sunt prea simple pentru a fi exploatate.]

- **a)** true
- **b)** false

<details><summary>💡 Feedback</summary>

Simple devices are prime targets because they often lack authentication, encryption, and update mechanisms. They can be recruited into botnets, used for data injection, or as pivot points into internal networks. [Dispozitivele simple sunt ținte principale deoarece adesea le lipsesc autentificarea, criptarea și mecanismele de actualizare. Pot fi recrutate în botneturi, folosite pentru injectare de date sau ca puncte de pivot în rețelele interne.]

</details>

---

### Q26. `N13.C05.Q05`
**Authentication versus encryption priority / Prioritatea autentificării față de criptare**

*Multiple Choice*

> According to IoT security best practices, which security measure should be prioritised first? [Conform celor mai bune practici de securitate IoT, care măsură de securitate ar trebui prioritizată prima?]

- **a)** Network monitoring — detecting attacks is more effective than preventing them [Monitorizarea rețelei — detectarea atacurilor este mai eficientă decât prevenirea lor]
- **b)** TLS encryption — protecting data in transit is the most fundamental security layer [Criptarea TLS — protecția datelor în tranzit este cel mai fundamental strat de securitate]
- **c)** Strong authentication — it prevents unauthorised access regardless of encryption state [Autentificarea puternică — previne accesul neautorizat indiferent de starea criptării]
- **d)** Firmware updates — keeping software current eliminates all known vulnerability classes [Actualizări de firmware — menținerea software-ului la zi elimină toate clasele de vulnerabilități cunoscute]

<details><summary>💡 Feedback</summary>

Authentication prevents unauthorised access, which is more critical than protecting data in transit. An encrypted channel with default password gives an attacker encrypted access. OWASP ranks weak passwords (I1) above insecure data transfer (I7). [Autentificarea previne accesul neautorizat, ceea ce este mai critic decât protecția datelor în tranzit. Un canal criptat cu parolă implicită oferă atacatorului acces criptat. OWASP clasează parolele slabe (I1) peste transferul nesigur de date (I7).]

</details>

---

### Q27. `N13.C06.Q01`
**Defence-in-depth security model / Modelul de securitate apărare în adâncime**

*Multiple Choice*

> What is the core principle of a defence-in-depth security strategy? [Care este principiul fundamental al unei strategii de securitate de tip apărare în adâncime?]

- **a)** Multiple overlapping security layers ensure that compromise of one control does not breach the system [Mai multe straturi de securitate suprapuse asigură că compromiterea unui control nu încalcă sistemul]
- **b)** A single, extremely strong security barrier is sufficient if properly implemented [O singură barieră de securitate extrem de puternică este suficientă dacă este implementată corect]
- **c)** Each device independently manages its own security without centralised coordination [Fiecare dispozitiv își gestionează independent propria securitate fără coordonare centralizată]
- **d)** Security controls are applied exclusively at the outer network perimeter to block external threats at the boundary [Controalele de securitate se aplică exclusiv la perimetrul exterior al rețelei pentru a bloca amenințările externe la granița de rețea]

<details><summary>💡 Feedback</summary>

Defence-in-depth deploys multiple overlapping security controls so that the failure of any single layer does not compromise the entire system. [Apărarea în adâncime implementează mai multe controale de securitate suprapuse, astfel încât eșecul oricărui strat individual să nu compromită întregul sistem.]

</details>

---

### Q28. `N13.C06.Q02`
**Network segmentation purpose / Scopul segmentării rețelei**

*Multiple Choice*

> Why should IoT devices be placed on a separate network segment (VLAN) from corporate systems? [De ce ar trebui dispozitivele IoT plasate pe un segment de rețea separat (VLAN) de sistemele corporative?]

- **a)** To allow IoT devices to use different IP addressing schemes than corporate servers [Pentru a permite dispozitivelor IoT să folosească scheme de adresare IP diferite de serverele corporative]
- **b)** To make IoT devices invisible to all network traffic analysers and monitoring tools [Pentru a face dispozitivele IoT invizibile pentru toate analizoarele de trafic și instrumentele de monitorizare]
- **c)** To contain breaches: a compromised IoT device cannot pivot to more valuable corporate assets [Pentru limitarea breșelor: un dispozitiv IoT compromis nu poate pivota către active corporative mai valoroase]
- **d)** To improve IoT device performance by reducing network congestion on the main LAN [Pentru a îmbunătăți performanța dispozitivelor IoT prin reducerea congestiei pe LAN-ul principal]

<details><summary>💡 Feedback</summary>

Network segmentation isolates IoT devices so that a compromised sensor cannot be used as a pivot to access corporate databases or internal services. [Segmentarea rețelei izolează dispozitivele IoT astfel încât un senzor compromis să nu poată fi folosit ca punct de pivot pentru a accesa bazele de date sau serviciile interne ale companiei.]

</details>

---

### Q29. `N13.C06.Q03`
**Secure boot in IoT / Pornirea securizată în IoT**

*Multiple Choice*

> What does secure boot ensure in an IoT device? [Ce asigură pornirea securizată într-un dispozitiv IoT?]

- **a)** Cryptographic verification of firmware integrity before the device executes any code [Verificarea criptografică a integrității firmware-ului înainte ca dispozitivul să execute orice cod]
- **b)** Encrypted storage of all user data on the device's internal flash memory partition [Stocarea criptată a tuturor datelor utilizatorului pe partiția de memorie flash internă]
- **c)** Automatic connection to the nearest secure Wi-Fi network upon powering on the device [Conectarea automată la cea mai apropiată rețea Wi-Fi securizată la pornirea dispozitivului]
- **d)** Faster boot times by skipping unnecessary hardware initialisation checks during startup [Timpi de pornire mai rapizi prin omiterea verificărilor inutile de inițializare hardware]

<details><summary>💡 Feedback</summary>

Secure boot cryptographically verifies firmware integrity before execution. This prevents execution of tampered or malicious code injected through compromised update channels. [Pornirea securizată verifică criptografic integritatea firmware-ului înainte de execuție. Aceasta previne executarea codului falsificat sau malițios injectat prin canale de actualizare compromise.]

</details>

---

### Q30. `N13.C06.Q04`
**Defence-in-depth uses multiple layers / Apărarea în adâncime utilizează straturi multiple**

*True / False*

> Defence-in-depth means that a single strong firewall rule is sufficient to protect an IoT network, provided the rule is comprehensive enough. [Apărarea în adâncime înseamnă că o singură regulă de firewall puternică este suficientă pentru a proteja o rețea IoT, cu condiția ca regula să fie suficient de cuprinzătoare.]

- **a)** true
- **b)** false

<details><summary>💡 Feedback</summary>

Defence-in-depth explicitly requires MULTIPLE layers of security controls. A single control, no matter how strong, creates a single point of failure. [Apărarea în adâncime necesită explicit MULTIPLE straturi de controale de securitate. Un singur control, oricât de puternic, creează un singur punct de eșec.]

</details>

---

### Q31. `N13.C06.Q05`
**Secure OTA firmware update requirements / Cerințe pentru actualizarea securizată OTA a firmware-ului**

*Multiple Choice*

> Which combination of features is required for a secure Over-the-Air (OTA) firmware update mechanism? [Ce combinație de caracteristici este necesară pentru un mecanism securizat de actualizare a firmware-ului Over-the-Air (OTA)?]

- **a)** Peer-to-peer distribution, checksum verification, and administrator email alerts [Distribuție peer-to-peer, verificare checksum și alerte email pentru administrator]
- **b)** Signed firmware images, encrypted transport channel, and rollback capability [Imagini de firmware semnate, canal de transport criptat și capacitate de revenire]
- **c)** Password-protected download URL, version numbering, and change log documentation [URL de descărcare protejat cu parolă, numerotare a versiunii și documentare changelog]
- **d)** Firmware compression, automatic scheduling, and device restart notification [Compresie firmware, programare automată și notificare de repornire a dispozitivului]

<details><summary>💡 Feedback</summary>

Secure OTA requires digitally signed images (integrity), encrypted transport (confidentiality), and rollback capability (resilience). Missing any of these creates an exploitable attack surface. [OTA securizat necesită imagini semnate digital (integritate), transport criptat (confidențialitate) și capacitate de revenire (reziliență). Lipsa oricăreia dintre acestea creează o suprafață de atac exploatabilă.]

</details>

---

### Q32. `N13.T00.Q01`
**MQTT broker role in message delivery / Rolul brokerului MQTT în livrarea mesajelor**

*Multiple Choice*

> In the MQTT publish-subscribe model, what role does the broker perform that enables decoupled communication between publishers and subscribers? [În modelul MQTT publicare-abonare, ce rol îndeplinește brokerul care permite comunicarea decuplată între publicatori și abonați?]

- **a)** The broker establishes persistent TCP connections between each publisher and every subscriber at connection time [Brokerul stabilește conexiuni TCP persistente între fiecare publicator și fiecare abonat la momentul conexiunii]
- **b)** The broker encrypts all messages before routing to ensure confidentiality between communicating parties [Brokerul criptează toate mesajele înainte de rutare pentru a asigura confidențialitatea între părțile comunicante]
- **c)** The broker temporarily stores all published messages in a sequential first-in-first-out queue and delivers them one by one to the next available consumer in round-robin order [Brokerul stochează temporar toate mesajele publicate într-o coadă secvențială first-in-first-out și le livrează pe rând următorului consumator disponibil în ordine round-robin]
- **d)** The broker maintains topic subscriptions and routes published messages to matching subscribers without direct publisher-subscriber contact [Brokerul menține abonările la topicuri și rutează mesajele publicate către abonații corespunzători fără contact direct publicator-abonat]

<details><summary>💡 Feedback</summary>

The broker maintains a registry of topic subscriptions and routes incoming published messages to all matching subscribers. Publishers and subscribers never communicate directly. [Brokerul menține un registru al abonărilor la topicuri și rutează mesajele publicate primite către toți abonații corespunzători. Publicatorii și abonații nu comunică niciodată direct.]

</details>

---

### Q33. `N13.T00.Q02`
**Effective QoS in multi-hop MQTT / QoS efectiv în MQTT multi-hop**

*Multiple Choice*

> A sensor publishes temperature readings at QoS 2 to a broker. A dashboard subscribes to the same topic at QoS 0. At what QoS will the dashboard actually receive messages? [Un senzor publică citiri de temperatură la QoS 2 către un broker. Un tablou de bord se abonează la același topic la QoS 0. La ce QoS va primi efectiv tabloul de bord mesajele?]

- **a)** QoS 0 — effective delivery uses the minimum of publisher (2) and subscriber (0) QoS levels [QoS 0 — livrarea efectivă folosește minimul nivelurilor QoS ale publicatorului (2) și abonatului (0)]
- **b)** QoS 1 — the broker averages QoS levels between publisher and subscriber for balanced delivery [QoS 1 — brokerul face media nivelurilor QoS între publicator și abonat pentru livrare echilibrată]
- **c)** The broker rejects the subscription because mismatched QoS levels are not permitted in MQTT [Brokerul respinge abonarea deoarece nivelurile QoS nepotrivite nu sunt permise în MQTT]
- **d)** QoS 2 — the publisher's higher QoS guarantees exactly-once delivery regardless of subscriber setting [QoS 2 — QoS-ul mai mare al publicatorului garantează livrarea exact o dată indiferent de setarea abonatului]

<details><summary>💡 Feedback</summary>

MQTT QoS is determined per-hop. The effective delivery QoS is the minimum of publisher and subscriber levels. min(2,0) = 0, so delivery is at-most-once (fire and forget). [QoS MQTT se determină per hop. QoS-ul efectiv de livrare este minimul nivelurilor publicatorului și abonatului. min(2,0) = 0, deci livrarea este cel mult o dată (fire and forget).]

</details>

---

### Q34. `N13.T00.Q03`
**TLS metadata leakage in IoT analysis / Scurgerea de metadate TLS în analiza IoT**

*Multiple Choice*

> A security analyst captures encrypted MQTT traffic (port 8883) between an IoT sensor and a broker. Without decrypting the traffic, which analysis is still possible? [Un analist de securitate captează traficul MQTT criptat (portul 8883) dintre un senzor IoT și un broker. Fără a decripta traficul, ce analiză este încă posibilă?]

- **a)** Reading the MQTT topic hierarchy and message payloads to understand what data is being transmitted [Citirea ierarhiei topicurilor MQTT și a conținutului mesajelor pentru a înțelege ce date se transmit]
- **b)** Inferring sensor activity patterns from connection timing, message frequency, and approximate payload sizes [Inferarea tiparelor de activitate ale senzorului din temporizarea conexiunilor, frecvența mesajelor și dimensiunea aproximativă a conținutului]
- **c)** Extracting the ephemeral TLS session keys directly from the captured handshake negotiation packets to fully decrypt all subsequent encrypted communications [Extragerea cheilor de sesiune TLS efemere direct din pachetele de negociere handshake capturate pentru a decripta complet toate comunicațiile criptate ulterioare]
- **d)** Determining the exact firmware version of the IoT device from its TLS certificate fingerprint alone [Determinarea versiunii exacte de firmware a dispozitivului IoT doar din amprenta certificatului TLS]

<details><summary>💡 Feedback</summary>

Traffic analysis remains possible: the analyst can observe connection timing, message frequency, packet sizes, and endpoint addresses. This metadata leakage enables inference of device behaviour patterns. [Analiza traficului rămâne posibilă: analistul poate observa temporizarea conexiunilor, frecvența mesajelor, dimensiunile pachetelor și adresele punctelor terminale. Această scurgere de metadate permite inferența tiparelor de comportament ale dispozitivelor.]

</details>

---

### Q35. `N13.T00.Q04`
**MQTT wildcard subscription matching / Potrivirea abonării cu metacaractere MQTT**

*Multiple Choice*

> A client subscribes to factory/+/status. Which of the following published topics will this client receive? [Un client se abonează la factory/+/status. Care dintre topicurile publicate următoare le va primi acest client?]

- **a)** factory/status (zero levels — + requires exactly one level) [factory/status (zero niveluri — + necesită exact un nivel)]
- **b)** factory/line1/status — the + wildcard substitutes exactly one topic level (line1) [factory/line1/status — wildcard-ul + substituie exact un nivel de topic (line1)]
- **c)** warehouse/line1/status (different root level: warehouse does not match the factory prefix in the subscription) [warehouse/line1/status (nivel rădăcină diferit: warehouse nu corespunde prefixului factory din abonament)]
- **d)** factory/building2/line1/status (two levels between factory and status) [factory/building2/line1/status (două niveluri între factory și status)]

<details><summary>💡 Feedback</summary>

The + wildcard matches exactly one level. factory/line1/status has exactly one level (line1) between factory/ and /status, so it matches. [Metacaracterul + se potrivește cu exact un nivel. factory/line1/status are exact un nivel (line1) între factory/ și /status, deci se potrivește.]

</details>

---

### Q36. `N13.T00.Q05`
**OWASP IoT vulnerability prioritisation / Prioritizarea vulnerabilităților OWASP IoT**

*Multiple Choice*

> During a security audit, you discover:
> (a) the MQTT broker accepts anonymous connections,
> (b) firmware updates are unsigned,
> (c) the device web interface has a SQL injection flaw. Using OWASP IoT Top 10 ranking, which should be remediated first? [În timpul unui audit de securitate, descoperiți: (a) brokerul MQTT acceptă conexiuni anonime,
> (b) actualizările de firmware sunt nesemnate,
> (c) interfața web a dispozitivului are o vulnerabilitate de injecție SQL. Folosind clasamentul OWASP IoT Top 10, care ar trebui remediată prima?]

- **a)** Unsigned firmware updates (I5 — enables persistent compromise through malicious updates) [Actualizări de firmware nesemnate (I5 — permite compromiterea persistentă prin actualizări malițioase)]
- **b)** SQL injection in the web interface (I3 — exploitable remotely with immediate data breach risk) [Injecție SQL în interfața web (I3 — exploatabilă de la distanță cu risc imediat de breșă de date)]
- **c)** Anonymous MQTT access (I1 — Weak Passwords is the top-ranked OWASP IoT vulnerability) [Accesul MQTT anonim (I1 — Parolele slabe este vulnerabilitatea OWASP IoT de rang cel mai înalt)]
- **d)** All three should be fixed simultaneously since they present equal risk levels [Toate trei ar trebui reparate simultan deoarece prezintă niveluri de risc egale]

<details><summary>💡 Feedback</summary>

OWASP ranks I1 (weak authentication) highest. Anonymous MQTT access is an I1 issue. SQL injection maps to I3 and unsigned firmware to I5. I1 takes priority. [OWASP clasează I1 (autentificare slabă) cel mai sus. Accesul MQTT anonim este o problemă I1. Injecția SQL corespunde I3 iar firmware-ul nesemnat I5. I1 are prioritate.]

</details>

---

### Q37. `N13.T00.Q06`
**Port scanning speed vs accuracy / Compromisul viteză vs acuratețe în scanarea de porturi**

*Multiple Choice*

> In the Week 13 port scanner, reducing the timeout from 0.5s to 0.05s increases scan speed. What is the primary trade-off? [În scanerul de porturi din Săptămâna 13, reducerea timeout-ului de la 0,5s la 0,05s crește viteza scanării. Care este compromisul principal?]

- **a)** TCP connections will fail entirely because the three-way handshake requires a minimum of 1 second [Conexiunile TCP vor eșua complet deoarece handshake-ul în trei pași necesită un minim de 1 secundă]
- **b)** Network intrusion detection systems are more likely to flag rapid scanning as malicious activity [Sistemele de detectare a intruziunilor în rețea sunt mai predispuse să semnaleze scanarea rapidă ca activitate malițioasă]
- **c)** The scanner will consume more CPU resources because shorter timeouts require more processing [Scanerul va consuma mai multe resurse CPU deoarece timeout-urile mai scurte necesită mai multă procesare]
- **d)** Slow-responding services may be incorrectly classified as filtered due to insufficient timeout [Serviciile cu răspuns lent pot fi clasificate incorect ca filtrate din cauza timeout-ului insuficient]

<details><summary>💡 Feedback</summary>

A shorter timeout increases the risk of misclassifying open or slow-responding ports as filtered. Services with high latency may not complete the handshake within 50ms. [Un timeout mai scurt crește riscul de clasificare greșită a porturilor deschise sau cu răspuns lent ca filtrate. Serviciile cu latență mare pot să nu finalizeze handshake-ul în 50ms.]

</details>

---

### Q38. `N13.T00.Q07`
**Defence-in-depth for MQTT broker / Apărare în adâncime pentru securitatea brokerului MQTT**

*Multiple Choice*

> Which combination of security controls best implements defence-in-depth for an MQTT broker? [Ce combinație de controale de securitate implementează cel mai bine apărarea în adâncime pentru un broker MQTT?]

- **a)** TLS encryption, client authentication with credentials or certificates, and topic-based ACLs for authorisation [Criptare TLS, autentificarea clienților cu credențiale sau certificate și ACL-uri bazate pe topic pentru autorizare]
- **b)** Firewall rules blocking all external access combined with internal network monitoring for anomaly detection [Reguli de firewall care blochează tot accesul extern combinate cu monitorizarea rețelei interne pentru detectarea anomaliilor]
- **c)** Only TLS encryption is needed because it provides all three properties: confidentiality, integrity, and authorisation [Doar criptarea TLS este necesară deoarece oferă toate cele trei proprietăți: confidențialitate, integritate și autorizare]
- **d)** Moving the broker behind a VPN eliminates the need for TLS or authentication on the MQTT protocol [Mutarea brokerului în spatele unui VPN elimină necesitatea TLS sau autentificării pe protocolul MQTT]

<details><summary>💡 Feedback</summary>

Defence-in-depth: TLS for transport encryption, username/password or certificate authentication, and topic-based ACLs for authorisation. This addresses confidentiality, authentication, and access control at different layers. [Apărare în adâncime: TLS pentru criptarea transportului, autentificare cu username/password sau certificat și ACL-uri bazate pe topic pentru autorizare.]

</details>

---

### Q39. `N13.T00.Q08`
**Wireshark plaintext vs TLS analysis / Analiza Wireshark text clar vs TLS**

*Multiple Choice*

> A student captures MQTT traffic on both port 1883 and port 8883 during the same session. When comparing the two captures, what key difference is observable? [Un student captează traficul MQTT atât pe portul 1883, cât și pe portul 8883 în aceeași sesiune. La compararea celor două capturi, ce diferență cheie este observabilă?]

- **a)** Port 1883 shows only TCP SYN packets while port 8883 shows complete application data in cleartext [Portul 1883 arată doar pachete TCP SYN în timp ce portul 8883 arată date complete de aplicație în text clar]
- **b)** Both port 1883 and port 8883 captures appear identical because Wireshark automatically decrypts all TLS-encrypted traffic during live capture for immediate protocol analysis [Ambele capturi de pe portul 1883 și portul 8883 arată identic deoarece Wireshark decriptează automat tot traficul criptat TLS în timpul capturii live pentru analiză imediată a protocolului]
- **c)** Port 8883 shows no packets at all because TLS traffic is invisible to packet capture tools [Portul 8883 nu arată niciun pachet deoarece traficul TLS este invizibil pentru instrumentele de captură de pachete]
- **d)** Port 1883 reveals topic names and payload content; port 8883 shows only encrypted Application Data records [Portul 1883 dezvăluie numele topicurilor și conținutul mesajelor; portul 8883 arată doar înregistrări de date de aplicație criptate]

<details><summary>💡 Feedback</summary>

Port 1883 shows plaintext MQTT with readable topics and payloads. Port 8883 shows TLS records with encrypted Application Data. Both show IP addresses and port numbers. [Portul 1883 arată MQTT text clar cu topicuri și conținut lizibil. Portul 8883 arată înregistrări TLS cu date de aplicație criptate. Ambele arată adresele IP și numerele de port.]

</details>

---

### Q40. `N13.T00.Q09`
**IoT device vulnerability despite simplicity / Vulnerabilitatea dispozitivului IoT în ciuda simplității**

*Multiple Choice*

> A temperature sensor with no web interface, no SSH, and only an MQTT client is deployed on a factory network. Why does this device still represent a security risk? [Un senzor de temperatură fără interfață web, fără SSH și doar cu un client MQTT este implementat într-o rețea de fabrică. De ce acest dispozitiv reprezintă totuși un risc de securitate?]

- **a)** The MQTT client can be exploited for data injection, botnet recruitment, or as a network pivot point even without web or SSH interfaces [Clientul MQTT poate fi exploatat pentru injectare de date, recrutare în botnet sau ca punct de pivot în rețea chiar și fără interfețe web sau SSH]
- **b)** Only devices equipped with more than 64MB of available RAM can possibly be exploited because embedded sensors fundamentally lack the sufficient computational resources for hosting malware [Doar dispozitivele echipate cu mai mult de 64MB de RAM disponibil pot fi exploatate deoarece senzorii încorporați nu au fundamental resursele computaționale suficiente pentru găzduirea malware-ului]
- **c)** The device is completely safe because without SSH or web access there is no attack vector for remote exploitation [Dispozitivul este complet sigur deoarece fără acces SSH sau web nu există vector de atac pentru exploatare de la distanță]
- **d)** The risk is purely theoretical and has never been observed in real-world IoT deployments worldwide [Riscul este pur teoretic și nu a fost observat niciodată în implementările IoT din lumea reală]

<details><summary>💡 Feedback</summary>

Even minimal devices with MQTT can be exploited: anonymous publish allows data injection, the device can be recruited into a botnet, or used as a pivot point. The Mirai botnet targeted similarly simple devices. [Chiar și dispozitivele minimale cu MQTT pot fi exploatate: publicarea anonimă permite injectarea de date, dispozitivul poate fi recrutat într-un botnet sau folosit ca punct de pivot. Botnetul Mirai a vizat dispozitive similare.]

</details>

---

### Q41. `N13.T00.Q10`
**Secure boot purpose in IoT / Scopul pornirii securizate în dispozitivele IoT**

*Multiple Choice*

> A manufacturer implements secure boot on their IoT gateway device. What specific attack does this mitigate? [Un producător implementează pornirea securizată pe dispozitivul lor gateway IoT. Ce atac specific atenuează aceasta?]

- **a)** SQL injection attacks targeting the device's internal SQLite database used for configuration storage [Atacuri de injecție SQL vizând baza de date SQLite internă a dispozitivului utilizată pentru stocarea configurării]
- **b)** Denial-of-service attacks that overwhelm the device with excessive volumes of network traffic during normal operation [Atacuri de refuzare a serviciului care supraîncarcă dispozitivul cu trafic excesiv de rețea în timpul funcționării normale]
- **c)** Eavesdropping on encrypted MQTT communications between the gateway and connected sensor devices [Interceptarea comunicațiilor MQTT criptate între gateway și dispozitivele senzoriale conectate]
- **d)** Execution of tampered or malicious firmware injected through compromised update channels or physical device access [Executarea firmware-ului falsificat sau malițios injectat prin canale de actualizare compromise sau acces fizic la dispozitiv]

<details><summary>💡 Feedback</summary>

Secure boot verifies firmware cryptographic signatures before execution. This prevents execution of tampered or malicious firmware that could be injected through a compromised update channel or physical access. [Pornirea securizată verifică semnăturile criptografice ale firmware-ului înainte de execuție. Aceasta previne executarea firmware-ului falsificat sau malițios care ar putea fi injectat printr-un canal de actualizare compromis sau acces fizic.]

</details>

---

## 📚 W13 — Laborator / Lab   (21 questions)

---

### Q42. `N13.S01.Q03`
**Open port does not mean vulnerable / Un port deschis nu înseamnă vulnerabil**

*True / False*

> Discovering that port 22 (SSH) is open on a server means that the SSH service is necessarily vulnerable to exploitation. [Descoperirea că portul 22 (SSH) este deschis pe un server înseamnă că serviciul SSH este neapărat vulnerabil la exploatare.]

- **a)** true
- **b)** false

<details><summary>💡 Feedback</summary>

An open port means a service is listening, not that it is vulnerable. Vulnerability depends on software version, configuration, authentication policy, and known CVEs. [Un port deschis înseamnă că un serviciu ascultă, nu că este vulnerabil. Vulnerabilitatea depinde de versiunea software-ului, configurare, politica de autentificare și CVE-uri cunoscute.]

</details>

---

### Q43. `N13.S01.Q04`
**Port scanning legality in controlled lab / Legalitatea scanării de porturi în laborator controlat**

*True / False*

> Scanning ports on containers within the Week 13 controlled Docker laboratory environment is legal because you have explicit authorisation over the target systems. [Scanarea porturilor pe containerele din mediul de laborator Docker controlat din Săptămâna 13 este legală deoarece aveți autorizare explicită asupra sistemelor țintă.]

- **a)** true
- **b)** false

<details><summary>💡 Feedback</summary>

Port scanning legality depends on authorisation. In this lab, all containers are under student control. Scanning without permission outside the lab constitutes unauthorised access. [Legalitatea scanării de porturi depinde de autorizare. În acest laborator, toate containerele sunt sub controlul studentului. Scanarea fără permisiune în afara laboratorului constituie acces neautorizat.]

</details>

---

### Q44. `N13.S01.Q05`
**Expected open ports in Week 13 lab / Porturile deschise așteptate în laboratorul Săptămânii 13**

*Multiple Choice*

> When scanning the Week 13 Docker lab from the host (IoT broker + pentest services running), how many host ports are expected to be open? [La scanarea laboratorului Docker din Săptămâna 13 de pe gazdă (broker IoT + servicii de pentest pornite), câte porturi gazdă se așteaptă să fie deschise?]

- **a)** 4 — ports 1883, 2121, 8080, and 8888 but not the backdoor port on 6200 [4 — porturile 1883, 2121, 8080 și 8888, dar nu portul backdoor 6200]
- **b)** 7 — including SSH on port 22 and MySQL on port 3306 in addition to lab services [7 — incluzând SSH pe portul 22 și MySQL pe portul 3306 pe lângă serviciile de laborator]
- **c)** 5 — ports 1883 (MQTT), 2121 (FTP), 6200 (backdoor), 8080 (WebGoat), and 8888 (DVWA) [5 — porturile 1883 (MQTT), 2121 (FTP), 6200 (backdoor), 8080 (WebGoat) și 8888 (DVWA)]
- **d)** 3 — only 1883 (MQTT), 8080 (WebGoat), and 8888 (DVWA) are accessible [3 — doar 1883 (MQTT), 8080 (WebGoat) și 8888 (DVWA) sunt accesibile]

<details><summary>💡 Feedback</summary>

Count only the host-exposed ports (the left side of the mappings) from the Week 13 compose files. In COMPnet, those are 1883 (MQTT broker), 8888 (DVWA), 8080 (WebGoat), 2121 (FTP), and 6200 (backdoor). [Numărați doar porturile expuse pe gazdă (partea stângă a mapărilor) din fișierele compose din Săptămâna 13. În COMPnet, acestea sunt 1883 (broker MQTT), 8888 (DVWA), 8080 (WebGoat), 2121 (FTP) și 6200 (backdoor).]

</details>

---

### Q45. `N13.S01.Q06`
**connect_ex return value for open port / Valoarea returnată de connect_ex pentru port deschis**

*Multiple Choice*

> In the Week 13 port scanner code, what value does socket.connect_ex() return when a port is open? [În codul scanerului de porturi din Săptămâna 13, ce valoare returnează socket.connect_ex() când un port este deschis?]

- **a)** 1 — the conventional success code for TCP socket operations in Python [1 — codul convențional de succes pentru operațiunile de socket TCP în Python]
- **b)** -1 — following the POSIX convention where negative values indicate success [-1 — conform convenției POSIX unde valorile negative indică succes]
- **c)** The port number itself is returned to confirm which port was connected [Numărul portului în sine este returnat pentru a confirma ce port a fost conectat]
- **d)** 0 — indicating the three-way handshake completed successfully [0 — indicând că handshake-ul în trei pași s-a finalizat cu succes]

<details><summary>💡 Feedback</summary>

connect_ex() returns 0 when the TCP three-way handshake succeeds. Non-zero values indicate errors (e.g., 111 for ECONNREFUSED meaning closed). [connect_ex() returnează 0 când handshake-ul TCP în trei pași reușește. Valorile nenule indică erori (de ex., 111 pentru ECONNREFUSED care înseamnă închis).]

</details>

---

### Q46. `N13.S02.Q03`
**Observable data in plaintext MQTT capture / Date observabile în captura MQTT text clar**

*Multiple Choice*

> When capturing plaintext MQTT traffic (port 1883) in Wireshark and following the TCP stream, which information is directly visible? [La capturarea traficului MQTT în text clar (portul 1883) în Wireshark și urmărirea fluxului TCP, ce informații sunt direct vizibile?]

- **a)** Topic names, message payloads, and client identifiers in the TCP stream [Numele topicurilor, conținutul mesajelor și identificatorii clienților în fluxul TCP]
- **b)** Only the QoS level, because message content is base64-encoded by default in MQTT [Doar nivelul QoS, deoarece conținutul mesajelor este codificat base64 implicit în MQTT]
- **c)** Only the broker IP address, because MQTT clients do not reveal their identifiers [Doar adresa IP a brokerului, deoarece clienții MQTT nu dezvăluie identificatorii lor]
- **d)** Only packet sizes and timing, because MQTT automatically obfuscates payload data [Doar dimensiunile pachetelor și temporizarea, deoarece MQTT obfuscă automat datele utile]

<details><summary>💡 Feedback</summary>

Plaintext MQTT reveals topic strings, payload content (sensor data, commands), and client identifiers. This is why TLS is essential for sensitive IoT data. [MQTT în text clar dezvăluie șirurile topicurilor, conținutul mesajelor (date senzori, comenzi) și identificatorii clienților. De aceea TLS este esențial pentru datele IoT sensibile.]

</details>

---

### Q47. `N13.S03.Q01`
**Mosquitto anonymous access in lab / Accesul anonim Mosquitto în laborator**

*True / False*

> The Mosquitto broker in the Week 13 laboratory is configured with allow_anonymous true, permitting connections without credentials. [Brokerul Mosquitto din laboratorul Săptămânii 13 este configurat cu allow_anonymous true, permițând conexiuni fără credențiale.]

- **a)** true
- **b)** false

<details><summary>💡 Feedback</summary>

The mosquitto.conf file explicitly sets allow_anonymous true for both listeners (1883 and 8883). This is intentional for educational purposes to demonstrate the risk. [Fișierul mosquitto.conf setează explicit allow_anonymous true pentru ambele ascultătoare (1883 și 8883). Aceasta este intenționat în scopuri educaționale pentru a demonstra riscul.]

</details>

---

### Q48. `N13.S03.Q02`
**Docker network subnet for Week 13 / Subrețeaua Docker pentru Săptămâna 13**

*Multiple Choice*

> What is the Docker network subnet configured for the Week 13 laboratory environment? [Care este subrețeaua de rețea Docker configurată pentru mediul de laborator al Săptămânii 13?]

- **a)** 192.168.13.0/24 [192.168.13.0/24]
- **b)** 172.17.0.0/16 [172.17.0.0/16]
- **c)** 10.13.0.0/16 [10.13.0.0/16]
- **d)** 172.20.0.0/24 [172.20.0.0/24]

<details><summary>💡 Feedback</summary>

In COMPnet, the pentest lab uses network pentestnet with subnet 172.20.0.0/24 (see docker-compose.pentest.yml). [În COMPnet, laboratorul de pentest folosește rețeaua pentestnet cu subrețeaua 172.20.0.0/24 (vezi docker-compose.pentest.yml).]

</details>

---

### Q49. `N13.S03.Q03`
**Mosquitto broker IP in lab network / Adresa IP a brokerului Mosquitto în rețeaua de laborator**

*Multiple Choice*

> What static IP address is assigned to the DVWA container in the Week 13 pentest Docker network? [Ce adresă IP statică este atribuită containerului DVWA în rețeaua Docker de pentest din Săptămâna 13?]

- **a)** 172.20.0.12 [172.20.0.12]
- **b)** 172.20.0.11 [172.20.0.11]
- **c)** 172.20.0.1 [172.20.0.1]
- **d)** 172.20.0.1 [172.20.0.1]

<details><summary>💡 Feedback</summary>

The pentest compose assigns 172.20.0.10 to the DVWA service (172.20.0.11 for WebGoat, 172.20.0.12 for vsftpd). [Fișierul de compose pentru pentest atribuie 172.20.0.10 serviciului DVWA (172.20.0.11 pentru WebGoat, 172.20.0.12 pentru vsftpd).]

</details>

---

### Q50. `N13.S03.Q04`
**Backdoor stub host port / Portul gazdă al stub-ului backdoor**

*Multiple Choice*

> Which host port is mapped to the vsftpd backdoor service in the Week 13 pentest lab? [Ce port de pe gazdă este mapat la serviciul backdoor vsftpd în laboratorul de pentest din Săptămâna 13?]

- **a)** 8888 [8888]
- **b)** 2121 [2121]
- **c)** 6200 [6200]
- **d)** 6100 [6100]

<details><summary>💡 Feedback</summary>

docker-compose.pentest.yml exposes port 6200 on the host for the backdoor connection. [docker-compose.pentest.yml expune portul 6200 pe gazdă pentru conexiunea backdoor.]

</details>

---

### Q51. `N13.S03.Q05`
**Host port for FTP access / Portul gazdă pentru acces FTP**

*Multiple Choice*

> Which host port provides FTP access to the vsftpd container in the Week 13 pentest lab? [Ce port de pe gazdă oferă acces FTP la containerul vsftpd în laboratorul de pentest din Săptămâna 13?]

- **a)** 8021 [8021]
- **b)** 2121 [2121]
- **c)** 21 [21]
- **d)** 2222 [2222]

<details><summary>💡 Feedback</summary>

docker-compose.pentest.yml maps host port 2121 to container port 21 (standard FTP). The non-standard host port avoids conflicts with any local FTP service. [docker-compose.pentest.yml mapează portul gazdă 2121 la portul 21 al containerului (FTP standard). Portul gazdă nestandard evită conflictele cu servicii FTP locale.]

</details>

---

### Q52. `N13.S04.Q01`
**Python socket type for TCP / Tipul de socket Python pentru TCP**

*Multiple Choice*

> Which socket module constant creates a TCP connection-oriented socket in Python? [Ce constantă a modulului socket creează un socket TCP orientat pe conexiune în Python?]

- **a)** socket.SOCK_DGRAM [socket.SOCK_DGRAM]
- **b)** socket.SOCK_TCP [socket.SOCK_TCP]
- **c)** socket.SOCK_RAW [socket.SOCK_RAW]
- **d)** socket.SOCK_STREAM [socket.SOCK_STREAM]

<details><summary>💡 Feedback</summary>

socket.SOCK_STREAM creates a TCP socket. SOCK_DGRAM is for UDP datagrams. SOCK_RAW is for raw socket access. [socket.SOCK_STREAM creează un socket TCP. SOCK_DGRAM este pentru datagrame UDP. SOCK_RAW este pentru acces raw la socket.]

</details>

---

### Q53. `N13.S04.Q02`
**ThreadPoolExecutor for concurrent scanning / ThreadPoolExecutor pentru scanare concurentă**

*Multiple Choice*

> In the Week 13 port scanner, which Python class from concurrent.futures enables parallel port scanning with a thread pool? [În scanerul de porturi din Săptămâna 13, ce clasă Python din concurrent.futures permite scanarea paralelă a porturilor cu un pool de fire de execuție?]

- **a)** AsyncioExecutor [AsyncioExecutor]
- **b)** ProcessPoolExecutor [ProcessPoolExecutor]
- **c)** ThreadPoolExecutor [ThreadPoolExecutor]
- **d)** MultiThreadQueue [MultiThreadQueue]

<details><summary>💡 Feedback</summary>

ThreadPoolExecutor manages a pool of threads, submitting scan tasks concurrently. ProcessPoolExecutor would use processes, which is less efficient for I/O-bound socket operations. [ThreadPoolExecutor gestionează un pool de fire de execuție, trimițând sarcini de scanare concurent. ProcessPoolExecutor ar folosi procese, ceea ce este mai puțin eficient pentru operațiuni de socket limitate de I/O.]

</details>

---

### Q54. `N13.S04.Q03`
**Code tracing — port scan results / Trasarea codului — rezultatele scanării de porturi**

*Multiple Choice*

> Given the code tracing exercise T1, with SSH (22), MQTT (1883), and DVWA (8888) running but nothing on ports 80 and 9999: what does print(f"Open ports: {open_count}") output? [Având exercițiul de trasare a codului T1, cu SSH (22), MQTT (1883) și DVWA (8888) pornite dar nimic pe porturile 80 și 9999: ce afișează print(f"Open ports: {open_count}")?]

- **a)** Open ports: 0 [Open ports: 0]
- **b)** Open ports: 3 [Open ports: 3]
- **c)** Open ports: 2 [Open ports: 2]
- **d)** Open ports: 5 [Open ports: 5]

<details><summary>💡 Feedback</summary>

Three services respond (22, 1883, 8888). Ports 80 and 9999 return non-zero from connect_ex() (ECONNREFUSED), counting as closed. open_count = 3. [Trei servicii răspund (22, 1883, 8888). Porturile 80 și 9999 returnează valori nenule din connect_ex() (ECONNREFUSED), numărându-se ca închise. open_count = 3.]

</details>

---

### Q55. `N13.S04.Q04`
**Code tracing — MQTT message count / Trasarea codului — numărarea mesajelor MQTT**

*Multiple Choice*

> In exercise T2, a subscriber is registered with client.subscribe("sensors/#", qos=1). Three messages are published to topics sensors/temp, sensors/humidity, and weather/temp. How many messages does the subscriber receive? [În exercițiul T2, un abonat este înregistrat cu client.subscribe("sensors/#", qos=1). Trei mesaje sunt publicate pe topicurile sensors/temp, sensors/humidity și weather/temp. Câte mesaje primește abonatul?]

- **a)** 0 — the subscriber must reconnect after publishing begins to receive any messages [0 — abonatul trebuie să se reconecteze după ce publicarea începe pentru a primi mesaje]
- **b)** 1 — only the first message matching the pattern is delivered to the subscriber [1 — doar primul mesaj care se potrivește cu modelul este livrat abonatului]
- **c)** 3 — the wildcard # matches all three messages regardless of topic hierarchy [3 — metacaracterul # se potrivește cu toate cele trei mesaje indiferent de ierarhia topicurilor]
- **d)** 2 — only sensors/temp and sensors/humidity match the subscription pattern [2 — doar sensors/temp și sensors/humidity se potrivesc cu modelul de abonare]

<details><summary>💡 Feedback</summary>

The subscription sensors/# matches sensors/temp and sensors/humidity but NOT weather/temp (different root). Total: 2 messages. [Abonarea sensors/# se potrivește cu sensors/temp și sensors/humidity dar NU cu weather/temp (rădăcină diferită). Total: 2 mesaje.]

</details>

---

### Q56. `N13.S04.Q06`
**Protocol detection for TLS traffic on port 8883 / Detectarea protocolului pentru trafic TLS pe portul 8883**

*Multiple Choice*

> In the code tracing exercise T4, when detect_protocol receives a packet with dst_port=8883 and payload starting with byte 0x16, what protocol does it return? [În exercițiul de trasare a codului T4, când detect_protocol primește un pachet cu dst_port=8883 și payload-ul începând cu octetul 0x16, ce protocol returnează?]

- **a)** MQTT-like [MQTT-like]
- **b)** HTTPS [HTTPS]
- **c)** MQTT-TLS [MQTT-TLS]
- **d)** MQTT [MQTT]

<details><summary>💡 Feedback</summary>

Port 8883 matches MQTT_PORTS, and byte 0x16 is the TLS handshake record type. The function returns MQTT-TLS for TLS traffic on MQTT ports. [Portul 8883 se potrivește cu MQTT_PORTS, iar octetul 0x16 este tipul de înregistrare handshake TLS. Funcția returnează MQTT-TLS pentru traficul TLS pe porturile MQTT.]

</details>

---

### Q57. `N13.S01.Q01`
**Filtered port scan result meaning / Semnificația rezultatului port filtrat**

*Multiple Choice*

> When a port scanner reports a port as "filtered", what has occurred at the network level? [Când un scanner de porturi raportează un port ca «filtrat», ce s-a întâmplat la nivel de rețea?]

- **a)** The port actively refused the connection by sending a TCP RST packet back to the scanner [Portul a refuzat activ conexiunea trimițând un pachet TCP RST înapoi la scanner]
- **b)** The target host is powered off and cannot respond to any incoming network packets [Gazda țintă este oprită și nu poate răspunde la niciun pachet de rețea care intră]
- **c)** The service is actively running but requires valid authentication credentials before accepting any inbound TCP connections [Serviciul funcționează activ dar necesită acreditări de autentificare valide înainte de a accepta orice conexiuni TCP de intrare]
- **d)** No response was received; a firewall silently dropped the SYN packet without sending a RST [Nu s-a primit niciun răspuns; un firewall a eliminat silențios pachetul SYN fără a trimite un RST]

<details><summary>💡 Feedback</summary>

Filtered means no response was received within the timeout period, typically because a firewall is silently dropping packets (iptables -j DROP). The actual service state behind the firewall is unknown. [Filtrat înseamnă că nu s-a primit niciun răspuns în perioada de timeout, de obicei deoarece un firewall elimină silențios pachetele (iptables -j DROP). Starea reală a serviciului din spatele firewall-ului este necunoscută.]

</details>

---

### Q58. `N13.S01.Q02`
**TCP RST indicates closed port / TCP RST indică un port închis**

*Multiple Choice*

> In a TCP connect scan, receiving a RST (Reset) packet in response to a SYN indicates that the port is: [Într-o scanare TCP connect, primirea unui pachet RST (Reset) ca răspuns la un SYN indică faptul că portul este:]

- **a)** Open — the service accepted the connection and is ready for data transfer [Deschis — serviciul a acceptat conexiunea și este gata pentru transferul de date]
- **b)** Closed — the host is reachable but no service is listening on that port [Închis — gazda este accesibilă dar niciun serviciu nu ascultă pe acel port]
- **c)** Filtered — a firewall intercepted the connection attempt before it reached the host [Filtrat — un firewall a interceptat tentativa de conexiune înainte de a ajunge la gazdă]
- **d)** Half-open — the three-way handshake started but was not completed by the service [Semi-deschis — handshake-ul în trei pași a început dar nu a fost finalizat de serviciu]

<details><summary>💡 Feedback</summary>

A RST packet means the host is reachable and actively refused the connection — no service is listening. This contrasts with filtered (no response) and open (SYN-ACK received). [Un pachet RST înseamnă că gazda este accesibilă și a refuzat activ conexiunea — niciun serviciu nu ascultă. Aceasta contrastează cu filtrat (fără răspuns) și deschis (SYN-ACK primit).]

</details>

---

### Q59. `N13.S02.Q01`
**Wireshark filter for MQTT PUBLISH / Filtru Wireshark pentru MQTT PUBLISH**

*Multiple Choice*

> Which Wireshark display filter shows only MQTT PUBLISH packets? [Ce filtru de afișare Wireshark arată doar pachetele MQTT PUBLISH?]

- **a)** mqtt.publish == true [mqtt.publish == true]
- **b)** mqtt.topic != "" [mqtt.topic != ""]
- **c)** mqtt.msgtype == 3 [mqtt.msgtype == 3]
- **d)** tcp.port == 1883 [tcp.port == 1883]

<details><summary>💡 Feedback</summary>

The display filter mqtt.msgtype == 3 selects PUBLISH messages. MQTT message type 3 corresponds to PUBLISH in the MQTT specification. [Filtrul de afișare mqtt.msgtype == 3 selectează mesajele PUBLISH. Tipul de mesaj MQTT 3 corespunde PUBLISH în specificația MQTT.]

</details>

---

### Q60. `N13.S02.Q02`
**TLS handshake display filter / Filtru de afișare pentru handshake TLS**

*Multiple Choice*

> Which Wireshark display filter captures TLS handshake packets? [Ce filtru de afișare Wireshark captează pachetele de handshake TLS?]

- **a)** tls.version >= 0x0303 [tls.version >= 0x0303]
- **b)** tls.handshake (captures all handshake messages) [tls.handshake (capturează toate mesajele de handshake)]
- **c)** ssl.record.content_type == 22 [ssl.record.content_type == 22]
- **d)** tcp.port == 8883 and tls [tcp.port == 8883 and tls]

<details><summary>💡 Feedback</summary>

The filter tls.handshake isolates handshake-phase packets including ClientHello, ServerHello, and certificate exchanges. This works regardless of port. [Filtrul tls.handshake izolează pachetele din faza de handshake, inclusiv ClientHello, ServerHello și schimbul de certificate. Funcționează indiferent de port.]

</details>

---

### Q61. `N13.S02.Q05`
**BPF capture filter for MQTT plaintext / Filtru de captură BPF pentru MQTT text clar**

*Multiple Choice*

> Which BPF capture filter (used with tcpdump or Wireshark capture options) isolates MQTT plaintext traffic? [Ce filtru de captură BPF (utilizat cu tcpdump sau opțiunile de captură Wireshark) izolează traficul MQTT text clar?]

- **a)** mqtt.port == 1883 [mqtt.port == 1883]
- **b)** port 1883 and protocol mqtt [port 1883 and protocol mqtt]
- **c)** tcp.port == 1883 [tcp.port == 1883]
- **d)** tcp port 1883 [tcp port 1883]

<details><summary>💡 Feedback</summary>

The BPF filter tcp port 1883 captures all TCP packets to/from port 1883. BPF capture filters use different syntax from Wireshark display filters — they cannot reference application protocols like mqtt. [Filtrul BPF tcp port 1883 captează toate pachetele TCP de la/către portul 1883. Filtrele de captură BPF utilizează o sintaxă diferită de filtrele de afișare Wireshark — nu pot referi protocoale de aplicație precum mqtt.]

</details>

---

### Q62. `N13.S04.Q05`
**Python settimeout method / Metoda settimeout din Python**

*Multiple Choice*

> In the port scanner code, which method configures the socket timeout for distinguishing between closed and filtered ports? [În codul scanerului de porturi, care metodă configurează timeout-ul socket-ului pentru a distinge între porturile închise și filtrate?]

- **a)** socket.setdefaulttimeout(timeout) [socket.setdefaulttimeout(timeout)]
- **b)** sock.settimeout(timeout) [sock.settimeout(timeout)]
- **c)** sock.timeout = timeout [sock.timeout = timeout]
- **d)** sock.configure(timeout=timeout) [sock.configure(timeout=timeout)]

<details><summary>💡 Feedback</summary>

sock.settimeout(timeout) configures the socket's blocking timeout. When connect_ex() exceeds this duration, a socket.timeout exception is raised, classified as filtered. [sock.settimeout(timeout) configurează timeout-ul de blocare al socket-ului. Când connect_ex() depășește această durată, se ridică o excepție socket.timeout, clasificată ca filtrat.]

</details>

---

## 📚 W13 — Numerical   (8 questions)

---

### Q63. `N13.D03.Q01`
**MQTT plaintext port / Portul MQTT text clar**

*Numerical*

> What is the standard port number for plaintext MQTT? Enter the number. [Care este numărul de port standard pentru MQTT text clar? Introduceți numărul.]


<details><summary>💡 Feedback</summary>

IANA assigns port (...) for plaintext MQTT. [IANA atribuie portul (...) pentru MQTT text clar.]

</details>

---

### Q64. `N13.D03.Q02`
**MQTT TLS port / Portul MQTT TLS**

*Numerical*

> State the standard port number for MQTT over TLS? Enter the number. [Care este numărul de port standard pentru MQTT prin TLS? Introduceți numărul.]


<details><summary>💡 Feedback</summary>

IANA assigns port (...) for MQTT-over-TLS. [IANA atribuie portul (...) pentru MQTT prin TLS.]

</details>

---

### Q65. `N13.D03.Q03`
**Usable hosts in /24 subnet / Gazde utilizabile în subrețeaua /24**

*Numerical*

> How many usable host addresses are available in the Week 13 lab subnet 172.20.0.0/24? Enter the number. [Câte adrese de gazdă utilizabile sunt disponibile în subrețeaua de laborator 172.20.0.0/24? Introduceți numărul.]


<details><summary>💡 Feedback</summary>

A /24 subnet has 2^8 - 2 = (...) usable host addresses (excluding network and broadcast). [O subrețea /24 are 2^8 - 2 = (...) adrese de gazdă utilizabile (excluzând rețeaua și broadcast).]

</details>

---

### Q66. `N13.D03.Q04`
**QoS 2 handshake messages / Mesaje handshake QoS 2**

*Numerical*

> How many protocol messages are exchanged in an MQTT QoS 2 delivery? Enter the count. [Câte mesaje de protocol se schimbă într-o livrare MQTT QoS 2? Introduceți numărul.]


<details><summary>💡 Feedback</summary>

QoS 2: PUBLISH + PUBREC + PUBREL + PUBCOMP = (...). [QoS 2: PUBLISH + PUBREC + PUBREL + PUBCOMP = (...).]

</details>

---

### Q67. `N13.D03.Q05`
**Expected open ports in lab scan / Porturile deschise așteptate în scanare**

*Numerical*

> How many host ports report as OPEN when scanning the Week 13 Docker setups from the host? Enter the count. [Câte porturi de pe gazdă raportează ca DESCHISE la scanarea setup-urilor Docker din Săptămâna 13, de pe gazdă? Introduceți numărul.]


<details><summary>💡 Feedback</summary>

Consider the host port mappings for the Week 13 services: 1883, 2121, 6200, 8080, 8888. [Luați în calcul mapările de porturi pe gazdă pentru serviciile din Săptămâna 13: 1883, 2121, 6200, 8080, 8888.]

</details>

---

### Q68. `N13.D03.Q06`
**connect_ex success return / Valoarea de succes connect_ex**

*Numerical*

> What integer does Python's socket.connect_ex() return when a TCP connection succeeds? Enter the number. [Ce întreg returnează socket.connect_ex() din Python când o conexiune TCP reușește? Introduceți numărul.]


<details><summary>💡 Feedback</summary>

connect_ex() returns (...) on successful connection. [connect_ex() returnează (...) la conexiune reușită.]

</details>

---

### Q69. `N13.D03.Q07`
**MQTT PUBLISH message type number / Numărul tipului de mesaj MQTT PUBLISH**

*Numerical*

> In the MQTT specification, what numeric message type value corresponds to PUBLISH (used in Wireshark filter mqtt.msgtype)? Enter the number. [În specificația MQTT, ce valoare numerică a tipului de mesaj corespunde PUBLISH (utilizat în filtrul Wireshark mqtt.msgtype)? Introduceți numărul.]


<details><summary>💡 Feedback</summary>

MQTT message type (...) = PUBLISH. [Tipul de mesaj MQTT (...) = PUBLISH.]

</details>

---

### Q70. `N13.D03.Q08`
**Code tracing open port count / Numărarea porturilor deschise în trasarea codului**

*Numerical*

> In code tracing exercise T1, with services on ports 22, 1883, and 8888 only, how many ports are reported as open? Enter the count. [În exercițiul de trasare a codului T1, cu servicii doar pe porturile 22, 1883 și 8888, câte porturi sunt raportate ca deschise? Introduceți numărul.]


<details><summary>💡 Feedback</summary>

Ports 22, 188(...), and 8888 are open. Ports 80 and 9999 are closed. Total open: (...). [Porturile 22, 188(...) și 8888 sunt deschise. Porturile 80 și 9999 sunt închise. Total deschise: (...).]

</details>

---

## 📚 W13 — Drag & Drop   (8 questions)

---

### Q71. `N13.D05.Q02`
**Assemble mosquitto_sub with TLS / Asamblați mosquitto_sub cu TLS**

*Drag & Drop into Text*

> Arrange the mosquitto_sub command for TLS-encrypted subscription: [Aranjați comanda mosquitto_sub pentru abonare criptată cu TLS:]

```
[[1]] -h localhost -p [[2]] --cafile [[3]] -t "iot/#" -v
```

📋 Available choices / Variante disponibile: mosquitto_sub  |  8883  |  docker/configs/certs/ca.crt  |  mosquitto_pub  |  1883  |  server.key


<details><summary>💡 Feedback</summary>

mosquitto_sub connects to port 8883 with the CA certificate for TLS verification. [mosquitto_sub se conectează la portul 8883 cu certificatul CA pentru verificarea TLS.]

</details>

---

### Q72. `N13.D05.Q04`
**Build Python socket TCP connection / Construiți conexiunea TCP socket Python**

*Drag & Drop into Text*

> Complete the Python code for TCP port scanning: [Completați codul Python pentru scanarea porturilor TCP:]

```python
sock = socket.socket(socket.AF_INET, socket.[[1]])
sock.[[2]](0.5)
error = sock.[[3]]((host, port))
```

📋 Available choices / Variante disponibile: SOCK_STREAM  |  settimeout  |  connect_ex  |  SOCK_DGRAM  |  timeout  |  connect


<details><summary>💡 Feedback</summary>

SOCK_STREAM for TCP, settimeout for timeout, connect_ex for non-blocking connect. [SOCK_STREAM pentru TCP, settimeout pentru timeout, connect_ex pentru conectare neblocantă.]

</details>

---

### Q73. `N13.D05.Q05`
**Arrange MQTT QoS 2 handshake / Aranjați handshake-ul MQTT QoS 2**

*Drag & Drop into Text*

> Place the four QoS 2 handshake messages in correct order: [Plasați cele patru mesaje de handshake QoS 2 în ordinea corectă:]
> Step 1: [[1]] → Step 2: [[2]] → Step 3: [[3]] → Step 4: [[4]]

📋 Available choices / Variante disponibile: PUBLISH  |  PUBREC  |  PUBREL  |  PUBCOMP  |  PUBACK  |  CONNACK  |  PINGREQ  |  PINGRESP


<details><summary>💡 Feedback</summary>

QoS 2 sequence: PUBLISH, PUBREC, PUBREL, PUBCOMP. [Secvența QoS 2: PUBLISH, PUBREC, PUBREL, PUBCOMP.]

</details>

---

### Q74. `N13.D05.Q06`
**Build TLS context in Python / Construiți contextul TLS în Python**

*Drag & Drop into Text*

> Complete the Python code for creating a TLS context: [Completați codul Python pentru crearea unui context TLS:]

```python
context = ssl.[[1]]()
context.[[2]]("ca.crt")
secure = context.[[3]](sock, server_hostname=host)
```

📋 Available choices / Variante disponibile: create_default_context  |  load_verify_locations  |  wrap_socket  |  SSLContext  |  load_cert_chain  |  connect


<details><summary>💡 Feedback</summary>

create_default_context creates the context, load_verify_locations loads the CA, wrap_socket wraps the TCP socket. [create_default_context creează contextul, load_verify_locations încarcă CA, wrap_socket împachetează socket-ul TCP.]

</details>

---

### Q75. `N13.D05.Q07`
**Build docker network inspect command / Construiți comanda docker network inspect**

*Drag & Drop into Text*

> Complete the Docker command to inspect the Week 13 network: [Completați comanda Docker pentru a inspecta rețeaua Săptămânii 13:]

```
[[1]] [[2]] [[3]] [[4]]
```

📋 Available choices / Variante disponibile: docker  |  network  |  inspect  |  pentestnet  |  compose  |  ls  |  bridge  |  dockerd


<details><summary>💡 Feedback</summary>

docker network inspect pentestnet displays network configuration details. [docker network inspect pentestnet afișează detaliile configurării rețelei.]

</details>

---

### Q76. `N13.D05.Q08`
**Complete Wireshark combined lab filter / Completați filtrul combinat de laborator Wireshark**

*Drag & Drop into Text*

> Build a Wireshark display filter for all Week 13 lab traffic: [Construiți un filtru de afișare Wireshark pentru tot traficul laboratorului Săptămâna 13:]
> tcp.port in {[[1]], [[2]], [[3]], [[4]], [[5]]}

📋 Available choices / Variante disponibile: 1883  |  2121  |  6200  |  8080  |  8888  |  9000  |  443  |  80  |  8443  |  8883


<details><summary>💡 Feedback</summary>

The five relevant host ports in Week 13 are 1883, 2121, 6200, 8080, 8888 (MQTT broker + pentest services). [Cele cinci porturi relevante pe gazdă în Săptămâna 13 sunt 1883, 2121, 6200, 8080, 8888 (broker MQTT + servicii de pentest).]

</details>

---

### Q77. `N13.D05.Q01`
**Build Wireshark MQTT PUBLISH filter / Construiți filtru Wireshark MQTT PUBLISH**

*Drag & Drop into Text*

> Complete the Wireshark display filter to show only MQTT PUBLISH packets: [Completați filtrul de afișare Wireshark pentru a arăta doar pachetele MQTT PUBLISH:]

```
[[1]].[[2]] == [[3]]
```

📋 Available choices / Variante disponibile: mqtt  |  msgtype  |  3  |  tcp  |  port  |  1883


<details><summary>💡 Feedback</summary>

The correct filter is mqtt.msgtype == 3 where 3 is the PUBLISH message type. [Filtrul corect este mqtt.msgtype == 3, unde 3 este tipul de mesaj PUBLISH.]

</details>

---

### Q78. `N13.D05.Q03`
**Arrange tcpdump MQTT capture / Aranjați comanda tcpdump pentru captură MQTT**

*Drag & Drop into Text*

> Build the tcpdump command to capture MQTT plaintext traffic: [Construiți comanda tcpdump pentru a captura traficul MQTT text clar:]

```
[[1]] -i [[2]] port [[3]] -w pcap/mqtt.pcap
```

📋 Available choices / Variante disponibile: tcpdump  |  any  |  1883  |  wireshark  |  eth0  |  8883


<details><summary>💡 Feedback</summary>

tcpdump -i any port 1883 captures MQTT plaintext on all interfaces. [tcpdump -i any port 1883 captează MQTT text clar pe toate interfețele.]

</details>

---

## 📚 W13 — Gap Select   (8 questions)

---

### Q79. `N13.D10.Q01`
**IoT connectivity protocols / Protocoale de conectivitate IoT**

*Gap Select*

> MQTT operates over [[1]] on port 1883. For encrypted communication, it uses [[2]] on port 8883. CoAP uses [[3]] with optional DTLS. [MQTT operează prin ___ pe portul 1883. Pentru comunicare criptată, utilizează ___ pe portul 8883. CoAP folosește ___ cu DTLS opțional.]

📋 Available choices / Variante disponibile: TCP  |  UDP  |  TLS  |  SSL  |  UDP  |  TCP


<details><summary>💡 Feedback</summary>

MQTT=TCP, MQTT-TLS=TLS, CoAP=UDP. [MQTT=TCP, MQTT-TLS=TLS, CoAP=UDP.]

</details>

---

### Q80. `N13.D10.Q02`
**MQTT topic wildcard behaviour / Comportamentul metacaracterelor de topic MQTT**

*Gap Select*

> The MQTT single-level wildcard [[1]] matches exactly one topic level. The multi-level wildcard [[2]] matches zero or more levels. Wildcards are valid only in [[3]] operations. [Metacaracterul MQTT de nivel unic ___ se potrivește cu exact un nivel de topic. Metacaracterul multi-nivel ___ se potrivește cu zero sau mai multe niveluri. Metacaracterele sunt valide doar în operațiunile de ___.]

📋 Available choices / Variante disponibile: +  |  *  |  #  |  $  |  subscribe  |  publish


<details><summary>💡 Feedback</summary>

+, #, subscribe. [+, #, abonare.]

</details>

---

### Q81. `N13.D10.Q03`
**Port scan classification / Clasificarea scanării de porturi**

*Gap Select*

> When a TCP connection succeeds, the port is [[1]]. When a RST is received, the port is [[2]]. When no response arrives, the port is [[3]]. [Când o conexiune TCP reușește, portul este ___. Când se primește un RST, portul este ___. Când nu sosește niciun răspuns, portul este ___.]

📋 Available choices / Variante disponibile: open  |  closed  |  closed  |  filtered  |  filtered  |  open


<details><summary>💡 Feedback</summary>

open, closed, filtered. [deschis, închis, filtrat.]

</details>

---

### Q82. `N13.D10.Q04`
**MQTT broker role / Rolul brokerului MQTT**

*Gap Select*

> In MQTT, the [[1]] receives messages from [[2]] and routes them to [[3]] based on topic matching. [În MQTT, ___ primește mesaje de la ___ și le rutează către ___ pe baza potrivirii topicurilor.]

📋 Available choices / Variante disponibile: broker  |  publisher  |  publishers  |  subscribers  |  subscribers  |  brokers


<details><summary>💡 Feedback</summary>

broker, publishers, subscribers. [broker, publicatori, abonați.]

</details>

---

### Q83. `N13.D10.Q06`
**QoS 2 handshake steps / Pașii handshake-ului QoS 2**

*Gap Select*

> QoS 2 four-step handshake: [[1]] → [[2]] → [[3]] → [[4]]. [Handshake-ul QoS 2 în patru pași: ___ → ___ → ___ → ___.]

📋 Available choices / Variante disponibile: PUBLISH  |  PUBACK  |  PUBREC  |  CONNACK  |  PUBREL  |  SUBACK  |  PUBCOMP  |  DISCONNECT


<details><summary>💡 Feedback</summary>

PUBLISH, PUBREC, PUBREL, PUBCOMP. [PUBLISH, PUBREC, PUBREL, PUBCOMP.]

</details>

---

### Q84. `N13.D10.Q07`
**Security priority ordering / Ordinea de prioritate a securității**

*Gap Select*

> IoT security priorities: first implement [[1]], then [[2]], then [[3]], and finally monitoring. [Prioritățile securității IoT: mai întâi implementați ___, apoi ___, apoi ___ și în final monitorizarea.]

📋 Available choices / Variante disponibile: authentication  |  encryption  |  authorisation  |  monitoring  |  encryption  |  authentication


<details><summary>💡 Feedback</summary>

authentication, authorisation (ACLs), encryption (TLS). [autentificarea, autorizarea (ACL-uri), criptarea (TLS).]

</details>

---

### Q85. `N13.D10.Q08`
**Lab network addressing / Adresarea rețelei de laborator**

*Gap Select*

> The Week 13 Docker network uses subnet [[1]] with gateway [[2]]. The DVWA container is at [[3]]. [Rețeaua Docker din Săptămâna 13 folosește subrețeaua ___ cu poarta de acces ___. Containerul DVWA este la ___.]

📋 Available choices / Variante disponibile: 172.20.0.0/24  |  172.17.0.0/16  |  172.20.0.1  |  172.20.0.10  |  172.20.0.10  |  172.20.0.11


<details><summary>💡 Feedback</summary>

172.20.0.0/24, 172.20.0.1, 172.20.0.10. [172.20.0.0/24, 172.20.0.1, 172.20.0.10.]

</details>

---

### Q86. `N13.D10.Q05`
**TLS handshake sequence / Secvența handshake TLS**

*Gap Select*

> The TLS handshake begins with [[1]] from the client. The server responds with [[2]] and its certificate. After verification, [[3]] is established. [Handshake-ul TLS începe cu ___ de la client. Serverul răspunde cu ___ și certificatul său. După verificare, se stabilește ___.]

📋 Available choices / Variante disponibile: ClientHello  |  ServerHello  |  ServerHello  |  Certificate  |  encrypted channel  |  plain channel


<details><summary>💡 Feedback</summary>

ClientHello, ServerHello, encrypted channel. [ClientHello, ServerHello, canal criptat.]

</details>

---
