# Week 07 — Computer Networks
### *Rețele de Calculatoare — Săptămâna 7*

> Question Pool — Practice Set

---


## W07 — Curs / Lecture   (15 questions)

### Q1. `N01.T00.Q13` — One loopback capture / O captură loopback

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

Both test endpoints run on 127.0.0.1 in the same VM. TCP and UDP each use port 12345. Which command creates one PCAP containing both? [Ambele endpointuri de test rulează pe 127.0.0.1 în aceeași VM. TCP și UDP folosesc fiecare portul 12345. Ce comandă creează un singur PCAP care le conține pe ambele?]

- **a)** `sudo tcpdump -i lo -w capture.pcap 'port 12345'`
- **b)** `sudo tcpdump -i eth0 -w capture.pcap 'port 12345'`
- **c)** `sudo tcpdump -i lo -w capture.pcap 'tcp port 12345'`

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** The loopback interface carries this traffic. The capture filter port 12345 includes both transport protocols; display filters tcp.port == 12345 and udp.port == 12345 separate them afterwards. Start capture before the exchanges and stop it cleanly. [Interfața loopback transportă acest trafic. Filtrul de captură port 12345 include ambele protocoale; filtrele de afișare tcp.port == 12345 și udp.port == 12345 le separă ulterior. Porniți captura înaintea schimburilor și opriți-o curat.]

</details>

---

### 2. `Multiple Choice`
**N02.C02.Q01: Correct sequence of TCP three-way handshake flags / Secvența corectă a indicatorilor în handshake-ul TCP în trei pași**

> What is the correct order of TCP flag exchanges during the three-way handshake that establishes a connection? [Care este ordinea corectă a schimbului de indicatori TCP în timpul handshake-ului în trei pași care stabilește o conexiune?]

- **a) SYN → SYN-ACK → ACK**
- **b) ACK → SYN → SYN-ACK**
- **c) SYN → ACK → SYN-ACK**
- **d) SYN-ACK → SYN → ACK**

> 💡 **Feedback:** The client initiates with SYN, the server responds with SYN-ACK, and the client completes with ACK. This three-step process synchronises sequence numbers on both endpoints for the ordinary connection establishment used in this lab; data can accompany the final ACK, and TCP Fast Open is a separate extension. A common misconception is that the handshake occurs for every message sent; in reality, it happens only once when connect() is called, and all subsequent data flows over the established connection. [Clientul inițiază cu SYN, serverul răspunde cu SYN-ACK, iar clientul finalizează cu ACK. Acest proces în trei pași sincronizează numerele de secvență la ambele capete pentru stabilirea obișnuită folosită în laborator; datele pot însoți ACK-ul final, iar TCP Fast Open este o extensie separată. O concepție greșită frecventă este că handshake-ul are loc pentru fiecare mesaj trimis; în realitate, acesta se produce o singură dată la apelul connect(), iar toate datele ulterioare circulă pe conexiunea deja stabilită.]

---

### Q3. `N07.C01.Q02` — TCP establishment scope / Domeniul stabilirii TCP

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

Is “TCP can never transmit application data during connection establishment” universally correct? [Este universal corectă afirmația „TCP nu poate transmite niciodată date de aplicație în timpul stabilirii conexiunii”?]

- **a)** No. The final ACK can carry data and TCP Fast Open permits data in the SYN under its defined conditions. [Nu. ACK-ul final poate conține date, iar TCP Fast Open permite date în SYN în condițiile definite.]
- **b)** Yes. Every TCP packet in a handshake must have zero payload. [Da. Orice pachet TCP din handshake trebuie să aibă payload zero.]
- **c)** No, because UDP performs the TCP handshake. [Nu, deoarece UDP realizează handshake-ul TCP.]

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** The ordinary SYN/SYN-ACK/ACK teaching model establishes sequence-number state. Do not turn the simplified sequence into a prohibition on all data-bearing establishment segments. [Modelul didactic SYN/SYN-ACK/ACK stabilește starea numerelor de secvență. Secvența simplificată nu trebuie transformată într-o interdicție universală a segmentelor cu date în timpul stabilirii.]

</details>

---

### Q4. `N07.C03.Q03` — connect_ex result / Rezultatul connect_ex

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

For an AF_INET/SOCK_STREAM socket, what does connect_ex return on a successful connection? [Pentru un socket AF_INET/SOCK_STREAM, ce returnează connect_ex la conectare reușită?]

- **a)** 0
- **b)** The remote process PID [PID-ul procesului distant]
- **c)** The number of application bytes read [Numărul octeților de aplicație citiți]

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** It returns zero for success and errno-style codes for connection errors. Some errors, such as name resolution problems, can still raise exceptions. Non-zero does not uniquely mean “closed”: record refusal, timeout and unreachable outcomes separately. [Returnează zero la succes și coduri de tip errno pentru erori de conectare. Unele erori, precum rezoluția numelui, pot produce excepții. Non-zero nu înseamnă unic „închis”: înregistrați separat refuzul, timeout-ul și inaccesibilitatea.]

</details>

---

### Q5. `N07.C03.Q04` — Timeout evidence / Dovezi pentru timeout

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

A TCP connection attempt expires without completing. What is the justified observation? [O tentativă de conectare TCP expiră fără finalizare. Care este observația justificată?]

- **a)** No connection completed before the deadline; filtering, loss, an unreachable host or other causes remain possible. [Nicio conexiune nu s-a finalizat până la termen; filtrarea, pierderea, o gazdă inaccesibilă sau alte cauze rămân posibile.]
- **b)** A firewall DROP rule has been proved. [A fost demonstrată o regulă firewall DROP.]
- **c)** The port is certainly closed and sent RST. [Portul este sigur închis și a trimis RST.]

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** connect_ex may return a timeout-related errno rather than raise socket.timeout. Inspect returned codes and handle exceptions. A timeout describes the observation, not a unique remote port state. [connect_ex poate întoarce un errno asociat timeout-ului în loc să ridice socket.timeout. Inspectați codurile returnate și tratați excepțiile. Timeout-ul descrie observația, nu o stare unică a portului distant.]

</details>

---

### 6. `Multiple Choice`
**N07.C04.Q03: Capture Filter vs Display Filter / Filtru de captură vs filtru de afișare**

> What is the key operational difference between a BPF capture filter (used by tcpdump) and a Wireshark display filter? [Care este diferența operațională cheie între un filtru de captură BPF (folosit de tcpdump) și un filtru de afișare Wireshark?]

- **a) A capture filter is applied during packet collection (reducing what is recorded); a display filter is applied after capture (hiding what is already recorded) [Un filtru de captură se aplică în timpul colectării pachetelor (reducând ce se înregistrează); un filtru de afișare se aplică după captură (ascunzând ce este deja înregistrat)]**
- **b) Capture filters use Wireshark display-filter syntax while display filters use BPF capture-filter syntax — this reversal is a common confusion since both tools can parse both syntaxes at different pipeline stages [Filtrele de captură folosesc sintaxa filtrelor de afișare Wireshark în timp ce filtrele de afișare folosesc sintaxa BPF a filtrelor de captură — această inversare este o confuzie frecventă deoarece ambele instrumente pot interpreta ambele sintaxe în etape diferite ale fluxului de procesare]**
- **c) Display filters can only be applied to live traffic; capture filters work exclusively with saved pcap files [Filtrele de afișare pot fi aplicate doar traficului live; filtrele de captură funcționează exclusiv cu fișiere pcap salvate]**
- **d) Both operate at the same stage but capture filters are faster because they use hardware acceleration [Ambele operează în aceeași etapă, dar filtrele de captură sunt mai rapide deoarece folosesc accelerare hardware]**

> 💡 **Feedback:** BPF capture filters are evaluated by the kernel at capture time — packets not matching the filter are never written to the file. Display filters are applied in Wireshark after capture, allowing you to explore different subsets of already-recorded traffic. They also use different syntax. [Filtrele de captură BPF sunt evaluate de kernel în momentul capturii — pachetele care nu se potrivesc filtrului nu sunt scrise niciodată în fișier. Filtrele de afișare se aplică în Wireshark după captură, permițându-vă să explorați diferite subseturi de trafic deja înregistrat. De asemenea, folosesc sintaxe diferite.]

---

### 7. `True / False`
**N07.C04.Q05: Capture Has No Performance Impact / Captura nu are impact asupra performanței**

> Running tcpdump continuously in a high-traffic production environment has no measurable impact on system performance. [Rularea continuă a tcpdump într-un mediu de producție cu trafic intens nu are impact măsurabil asupra performanței sistemului.]

- **a) true**
- **b) false**

> 💡 **Feedback:** Capture involves copying each matching packet from kernel to userspace, buffering it, and writing to disk. On high-traffic links this can cause measurable CPU and I/O overhead, and even dropped packets if the capture cannot keep up. [Captura implică copierea fiecărui pachet care se potrivește din kernel în spațiul utilizator, bufferarea acestuia și scrierea pe disc. Pe legăturile cu trafic intens, aceasta poate cauza suprasarcină măsurabilă de CPU și I/O, și chiar pachete pierdute dacă captura nu poate ține pasul.]

---

### Q8. `N07.C05.Q01` — DROP behaviour / Comportamentul DROP

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

For packets matching a firewall rule, which action silently discards them without generating a rejection response from that rule? [Pentru pachetele potrivite unei reguli firewall, ce acțiune le elimină fără a genera prin acea regulă un răspuns de respingere?]

- **a)** DROP
- **b)** REJECT
- **c)** ACCEPT

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** DROP is silent for those matched packets. It does not make a host invisible to all other probes or guarantee that every scan times out. Other services, paths and network errors can expose information. [DROP este silențios pentru pachetele potrivite. Nu face gazda invizibilă la toate celelalte probe și nu garantează că orice scanare expiră. Alte servicii, căi și erori de rețea pot furniza informații.]

</details>

---

### Q9. `N07.T00.Q04` — Refusal and silence / Refuz și absența răspunsului

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

In a controlled reachable TCP test, no listener and no filtering produces RST; replacing this with a confirmed silent DROP rule produces no reply. What distinction is demonstrated? [Într-un test TCP controlat și accesibil, lipsa listenerului și a filtrării produce RST; o regulă DROP silențioasă confirmată produce absența răspunsului. Ce distincție este demonstrată?]

- **a)** Active refusal versus silence in this configured experiment. [Refuz activ față de absența răspunsului în experimentul configurat.]
- **b)** Any RST proves the remote application is absent. [Orice RST dovedește absența aplicației distante.]
- **c)** Any timeout proves a firewall rule. [Orice timeout dovedește o regulă firewall.]

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** A firewall can also reject with TCP RST. Packet loss and routing failures can also prevent completion. General diagnosis needs the error code, captures and configuration evidence. [Un firewall poate respinge și prin TCP RST. Pierderile și problemele de rutare pot împiedica finalizarea. Diagnosticul general necesită codul erorii, capturi și dovezi de configurație.]

</details>

---

### Q10. `N07.T00.Q05` — Socket type and connect_ex / Tipul socketului și connect_ex

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

Does connect_ex on a SOCK_DGRAM socket perform a UDP handshake that proves a server is listening? [connect_ex pe un socket SOCK_DGRAM realizează un handshake UDP care dovedește existența unui server?]

- **a)** No. UDP connect sets a default peer locally; UDP has no transport handshake. [Nu. Connect UDP stabilește local un corespondent implicit; UDP nu are handshake de transport.]
- **b)** Yes, the same three-way handshake as TCP. [Da, același handshake în trei pași ca TCP.]
- **c)** The API cannot be called on any UDP socket. [API-ul nu poate fi apelat pe niciun socket UDP.]

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** The socket type determines transport semantics. Successful UDP connect is not a service reachability test. The S07 connect scanner uses SOCK_STREAM to attempt TCP connections. [Tipul socketului determină semantica transportului. Succesul connect UDP nu testează disponibilitatea serviciului. Scannerul S07 folosește SOCK_STREAM pentru a încerca conexiuni TCP.]

</details>

---

### 11. `Multiple Choice`
**N07.T00.Q07: BPF vs Display Filter Timing / Momentul aplicării filtrelor BPF vs filtre de afișare**

> What is the key difference between a BPF capture filter and a Wireshark display filter? [Care este diferența cheie dintre un filtru de captură BPF și un filtru de afișare Wireshark?]

- **a) BPF filters apply during capture (unmatched packets are never stored); display filters apply after capture [Filtrele BPF se aplică în timpul capturii (pachetele nepotrivite nu sunt stocate niciodată); filtrele de afișare se aplică după captură]**
- **b) BPF filters use Wireshark field names such as tcp.port for matching; display filters use libpcap BPF syntax such as tcp port for post-capture selection [Filtrele BPF folosesc nume de câmpuri Wireshark precum tcp.port pentru potrivire; filtrele de afișare folosesc sintaxa libpcap BPF precum tcp port pentru selecție post-captură]**
- **c) BPF filters only work in Wireshark GUI; display filters only work in tshark CLI [Filtrele BPF funcționează doar în interfața grafică Wireshark; filtrele de afișare funcționează doar în tshark CLI]**
- **d) BPF filters operate on application-layer data; display filters operate on packet headers [Filtrele BPF operează pe datele de nivel aplicație; filtrele de afișare operează pe antetele pachetelor]**

> 💡 **Feedback:** BPF (Berkeley Packet Filter) operates at capture time in the kernel. Non-matching packets are discarded and never reach the capture file. Display filters operate post-capture on stored data. The syntax is also different: BPF uses 'tcp port 9090' while display filters use 'tcp.port == 9090'. [BPF (Berkeley Packet Filter) operează la momentul capturii în nucleu. Pachetele nepotrivite sunt eliminate și nu ajung niciodată în fișierul de captură. Filtrele de afișare operează post-captură pe datele stocate. Sintaxa este diferită: BPF folosește 'tcp port 9090' iar filtrele de afișare folosesc 'tcp.port == 9090'.]

---

### Q12. `N07.C02.Q04` — Explicit TCP rejection / Respingere TCP explicită

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

During a controlled TCP firewall lesson, which rejection setting sends an immediate reset for matching TCP probes? [Într-o lecție firewall TCP controlată, ce setare de respingere trimite imediat reset pentru probele TCP potrivite?]

- **a)** `REJECT --reject-with tcp-reset`
- **b)** `DROP`
- **c)** `LOG`

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** The explicit tcp-reset form requests RST. A default REJECT can use an ICMP error instead. Immediate refusal helps observe the policy, but a refused connection alone does not prove which device or rule generated it. [Forma explicită tcp-reset solicită RST. REJECT implicit poate folosi o eroare ICMP. Refuzul imediat ajută observarea politicii, dar o conexiune refuzată singură nu dovedește ce dispozitiv sau regulă l-a generat.]

</details>

---

### 13. `Multiple Choice`
**N07.C01.Q04: UDP Fire-and-Forget Delivery / Livrarea fire-and-forget a UDP**

> A Python application calls sendto() on a UDP socket to dispatch a datagram to a remote host. The call returns successfully. What can be said about delivery? [O aplicație Python apelează sendto() pe un socket UDP pentru a expedia o datagramă către un host la distanță. Apelul returnează cu succes. Ce se poate spune despre livrare?]

- **a) The sender has no delivery confirmation; the datagram may have been delivered, dropped by a firewall, or lost in transit [Expeditorul nu are confirmare de livrare; datagrama poate fi livrată, eliminată de un paravan de protecție sau pierdută în tranzit]**
- **b) The successful return guarantees the receiver application processed the datagram correctly [Returnarea cu succes garantează că aplicația receptorului a procesat corect datagrama]**
- **c) Python's socket library automatically retries the send until the kernel confirms delivery at the destination [Biblioteca socket din Python reîncearcă automat trimiterea până când kernelul confirmă livrarea la destinație]**
- **d) The operating-system kernel returns a non-zero error code whenever the datagram fails to reach the destination host, halting any further sends [Kernelul sistemului de operare returnează un cod de eroare diferit de zero ori de câte ori datagrama nu ajunge la hostul destinație, oprind orice trimitere ulterioară]**

> 💡 **Feedback:** UDP uses fire-and-forget semantics. The sendto() call succeeds when the packet is handed to the local network stack, not when the receiver processes it. A firewall DROP or packet loss remains invisible to the sender without an application-layer acknowledgement. [UDP folosește semantica fire-and-forget. Apelul sendto() reușește când pachetul este predat stivei locale de rețea, nu când receptorul îl procesează. Un DROP de la paravan de protecție sau pierderea pachetului rămâne invizibilă pentru expeditor fără o confirmare la nivel de aplicație.]

---

### 14. `Multiple Choice`
**N07.C02.Q05: Sender Awareness of UDP DROP / Conștientizarea expeditorului privind DROP-ul UDP**

> An iptables DROP rule is applied to UDP port 9300. A Python script sends a datagram using sendto() and reports "Datagram sent successfully". Why does the sender report success? [O regulă iptables DROP este aplicată pe portul UDP 9300. Un script Python trimite o datagramă folosind sendto() și raportează 'Datagramă trimisă cu succes'. De ce raportează expeditorul succes?]

- **a) UDP is connectionless — sendto() succeeds when the datagram is handed to the local network stack, regardless of whether it arrives [UDP este fără conexiune — sendto() reușește când datagrama este predată stivei locale de rețea, indiferent dacă ajunge]**
- **b) The DROP rule only blocks inbound traffic arriving from external hosts outside the Docker network, so local sends within the same subnet are completely unaffected [Regula DROP blochează doar traficul de intrare care sosește de la hosturi externe din afara rețelei Docker, astfel încât trimiterile locale din aceeași subrețea nu sunt deloc afectate]**
- **c) Python's socket library intercepts the DROP and automatically retries the datagram until it is delivered [Biblioteca socket din Python interceptează DROP-ul și reîncearcă automat datagrama până când este livrată]**
- **d) The firewall acknowledges receipt to the sender before silently discarding the datagram [Paravanul de protecție confirmă primirea către expeditor înainte de a elimina în tăcere datagrama]**

> 💡 **Feedback:** UDP has no delivery confirmation. A successful sendto() reports local acceptance of the datagram, not delivery. Some failures may be reported through socket errors or ICMP; silence gives no application acknowledgement. Remote DROP usually provides no direct error feedback. [UDP nu are confirmare de livrare. Succesul sendto() raportează acceptarea locală a datagramei, nu livrarea. Unele eșecuri pot fi raportate prin erori de socket sau ICMP; lipsa răspunsului nu este confirmare de aplicație. DROP distant nu furnizează de regulă feedback direct de eroare.]

---

### 15. `Multiple Choice`
**N07.T00.Q03: UDP Delivery Guarantee / Garanția de livrare UDP**

> A Python program calls sendto() to send a UDP datagram to a host with a DROP rule on the destination port. Assume local transmission succeeds and no earlier asynchronous error is pending. What does sendto() return? [Un program Python apelează sendto() pentru a trimite o datagramă UDP către o gazdă cu o regulă DROP pe portul destinație. Presupuneți că transmisia locală reușește și nu există o eroare asincronă anterioară în așteptare. Ce returnează sendto()?]

- **a) The number of bytes sent (success), because UDP has no delivery confirmation [Numărul de octeți trimiși (succes), deoarece UDP nu are confirmare de livrare]**
- **b) Zero, indicating the packet was blocked by the firewall [Zero, indicând că pachetul a fost blocat de paravan]**
- **c) Negative one (-1), signalling a network-layer rejection from the remote host or an intermediate firewall [Minus unu (-1), semnalând o respingere la nivel de rețea de la gazda la distanță sau de la un paravan de protecție intermediar]**
- **d) An exception is raised instead of returning a value [O excepție este ridicată în loc să returneze o valoare]**

> 💡 **Feedback:** UDP sendto() succeeds when the local kernel accepts the datagram for transmission. The sender has no knowledge of remote firewalls, packet loss, or whether the receiver exists. Only application-layer protocols can confirm delivery. [UDP sendto() reușește când nucleul local acceptă datagrama pentru transmisie. Expeditorul nu cunoaște paravanele remote, pierderea pachetelor sau dacă receptorul există. Doar protocoalele de nivel aplicație pot confirma livrarea.]

---

## W07 — Laborator / Lab   (16 questions)

### 16. `Multiple Choice`
**N02.S03.Q01: Wireshark filter to capture only TCP SYN packets / Filtru Wireshark pentru capturarea doar a pachetelor TCP SYN**

> Which Wireshark display filter isolates only the initial SYN packets (the very first packet of a TCP handshake, without an ACK flag)? [Care filtru de afișare Wireshark izolează doar pachetele SYN inițiale (primul pachet al unui handshake TCP, fără indicatorul ACK)?]

- **a) tcp.flags.syn == 1 and tcp.flags.ack == 0**
- **b) tcp.flags.syn == 1**
- **c) tcp.port == 12345**
- **d) tcp.flags.rst == 1**

> 💡 **Feedback:** The filter tcp.flags.syn == 1 and tcp.flags.ack == 0 matches only the initial SYN packet from the client (not the SYN-ACK from the server). Using only tcp.flags.syn == 1 (also matches SYN-ACK packets / potrivește și pachetele SYN-ACK) would also match SYN-ACK packets (which have both SYN and ACK flags set), giving false positives. Retransmitted SYN packets also match: correlate TCP streams and sequence numbers before counting distinct connection attempts. [Filtrul tcp.flags.syn == 1 and tcp.flags.ack == 0 corespunde doar pachetului SYN inițial de la client (nu SYN-ACK de la server). Utilizarea doar a tcp.flags.syn == 1 ar corespunde și pachetelor SYN-ACK (care au ambii indicatori SYN și ACK setați), producând rezultate fals pozitive. Retransmisiile SYN corespund și ele: corelați fluxurile TCP și numerele de secvență înainte de a număra tentative distincte.]

---

### 17. `Multiple Choice`
**N02.S03.Q05: Identifying a new TCP connection in a Wireshark capture / Identificarea unei conexiuni TCP noi într-o captură Wireshark**

> When analysing a Wireshark capture containing many TCP conversations, how can you identify the very first packet of a new TCP connection? [Când analizați o captură Wireshark care conține multe conversații TCP, cum puteți identifica chiar primul pachet al unei conexiuni TCP noi?]

- **a) Look for a packet with the SYN flag set and the ACK flag not set [Căutați un pachet cu indicatorul SYN setat și indicatorul ACK nesetat]**
- **b) Look for the first packet with the ACK flag set [Căutați primul pachet cu indicatorul ACK setat]**
- **c) Look for a packet with the RST flag set [Căutați un pachet cu indicatorul RST setat]**
- **d) Look for the packet with the smallest sequence number in the capture [Căutați pachetul cu cel mai mic număr de secvență din captură]**

> 💡 **Feedback:** The first packet of a TCP connection is a SYN packet with no ACK flag set. The filter tcp.flags.syn == 1 and tcp.flags.ack == 0 matches SYN packets without ACK, including retransmissions; it does not alone prove a new or completed connection. The second packet (SYN-ACK) has both SYN and ACK set, so it would not match this filter. A common error is looking for the packet with the smallest sequence number, but sequence numbers are random initial values, not ordered from zero. [Primul pachet al unei conexiuni TCP este un pachet SYN fără indicatorul ACK setat. Filtrul tcp.flags.syn == 1 and tcp.flags.ack == 0 selectează SYN fără ACK, inclusiv retransmisii; singur nu dovedește o conexiune nouă sau completă. Al doilea pachet (SYN-ACK) are ambii indicatori SYN și ACK setați, deci nu ar corespunde acestui filtru. O eroare frecventă este căutarea pachetului cu cel mai mic număr de secvență, dar numerele de secvență sunt valori inițiale aleatoare, nu ordonate de la zero.]

---

### 18. `Multiple Choice`
**N03.S03.Q02: Direct vs Tunnel Test / Test direct vs prin tunel**

> In this self-contained relay scenario, an unencrypted TCP relay on router:9090 opens a separate TCP connection to server:8080. A capture covers both legs. The student first tests a direct connection with echo 'DIRECT TEST' | nc server 8080, then tests the tunnel with echo 'TUNNEL TEST' | nc router 9090. Both return the echoed message. What is the key difference observable in Wireshark? [În acest scenariu autonom, un releu TCP necriptat de pe router:9090 deschide o conexiune TCP separată către server:8080. Captura acoperă ambele segmente. Studentul testează mai întâi o conexiune directă cu echo 'DIRECT TEST' | nc server 8080, apoi testează tunelul cu echo 'TUNNEL TEST' | nc router 9090. Ambele returnează mesajul ecou. Care este diferența cheie observabilă în Wireshark?]

- **a) The tunnel creates two separate TCP streams (ports 9090 and 8080) whereas direct creates one stream on port 8080 [Tunelul creează două fluxuri TCP separate (porturile 9090 și 8080) în timp ce directul creează un singur flux pe portul 8080]**
- **b) The tunnel adds encryption headers visible as TLS records while the direct connection sends plain text in practice [Tunelul adaugă anteturi de criptare vizibile ca înregistrări TLS în timp ce conexiunea directă trimite text simplu în practică]**
- **c) The tunnel sends UDP datagrams for efficiency while the direct connection uses standard TCP segments [Tunelul trimite datagrame UDP pentru eficiență în timp ce conexiunea directă folosește segmente TCP standard]**

> 💡 **Feedback:** The direct connection shows one TCP stream (client↔server on port 8080). The tunnel produces two TCP streams: one on port 9090 (client↔router) and another on port 8080 (router↔server). Wireshark filtering on tcp.port == 9090 or tcp.port == 8080 reveals both streams for the tunnelled case. [Conexiunea directă arată un singur flux TCP (client↔server pe portul 8080). Tunelul produce două fluxuri TCP: unul pe portul 9090 (client↔ruter) și altul pe portul 8080 (ruter↔server). Filtrarea Wireshark pe tcp.port == 9090 or tcp.port == 8080 dezvăluie ambele fluxuri pentru cazul cu tunel.]

---

### 19. `Multiple Choice`
**N03.S04.Q05: tcpdump Save Capture / Salvarea capturii tcpdump**

> To save a packet capture inside a container for later Wireshark analysis, which tcpdump flag writes output to a pcap file? [Pentru a salva o captură de pachete într-un container pentru analiza ulterioară Wireshark, care flag tcpdump scrie ieșirea într-un fișier pcap?]

- **a) -w — write captured packets to the specified file path [-w — scrie pachetele capturate la calea de fișier specificată]**
- **b) -r — read and display packets from a previously saved capture file [-r — citește și afișează pachetele dintr-un fișier de captură salvat anterior]**
- **c) -X — show packet contents in hexadecimal and ASCII dump format [-X — arată conținutul pachetelor în format dump hexazecimal și ASCII]**
- **d) -v — increase output verbosity with additional protocol details [-v — crește detaliile afișate cu informații suplimentare de protocol]**

> 💡 **Feedback:** The -w flag directs tcpdump to write raw packets to a file instead of printing them to the console. The resulting .pcap file can be opened in Wireshark for detailed analysis. The -r flag reads from a file (opposite operation). [Flag-ul -w direcționează tcpdump să scrie pachete brute într-un fișier în loc să le afișeze în consolă. Fișierul .pcap rezultat poate fi deschis în Wireshark pentru analiză detaliată. Flag-ul -r citește dintr-un fișier (operație inversă).]

---

### 20. `Multiple Choice`
**N04.S05.Q02: SYN followed by RST,ACK interpretation / Interpretarea SYN urmat de RST,ACK**

> In a Wireshark capture, you observe [SYN] → [RST,ACK]. What does this indicate? [Într-o captură Wireshark, observați [SYN] → [RST,ACK]. Ce indică acest lucru?]

- **a) The connection attempt was actively refused; a closed endpoint or a TCP-reset firewall rule may be responsible [Tentativa a fost refuzată activ; cauza poate fi un endpoint închis sau o regulă firewall TCP-reset]**
- **b) A successful TCP three-way handshake has been completed normally [Un handshake TCP cu trei căi a fost finalizat cu succes]**
- **c) The server is performing load balancing by redirecting the connection [Serverul efectuează echilibrarea încărcăturii prin redirecționarea conexiunii]**
- **d) The client has requested a half-close of the TCP connection [Clientul a solicitat o semi-închidere a conexiunii TCP]**

> 💡 **Feedback:** RST,ACK as a response to SYN means the destination port is closed (no service listening) or the connection was actively refused by a firewall. A successful handshake would show SYN → SYN,ACK → ACK. [RST,ACK ca răspuns la SYN înseamnă că portul destinație este închis (niciun serviciu nu ascultă) sau conexiunea a fost refuzată activ de un paravan de protecție. Un handshake reușit ar arăta SYN → SYN,ACK → ACK.]

---

### 21. `Multiple Choice`
**N07.S03.Q01: Capture Only SYN Packets / Capturarea doar a pachetelor SYN**

> Which tcpdump filter expression captures only TCP SYN packets (the first step of the three-way handshake)? [Care expresie de filtru tcpdump capturează doar pachetele TCP SYN (primul pas al handshake-ului tripartit)?]

- **a) tcp[tcpflags] & (tcp-syn|tcp-ack) == tcp-syn [tcp[tcpflags] & (tcp-syn|tcp-ack) == tcp-syn]**
- **b) tcp.flags.syn == 1 and not tcp.flags.ack [tcp.flags.syn == 1 and not tcp.flags.ack]**
- **c) tcp filter syn [tcp filter syn]**
- **d) tcp --syn-only [tcp --syn-only]**

> 💡 **Feedback:** tcpdump uses BPF (Berkeley Packet Filter) syntax: 'tcp[tcpflags] & (tcp-syn|tcp-ack) == tcp-syn'. The option 'tcp.flags.syn == 1' is Wireshark/tshark display filter syntax, not tcpdump capture syntax. [tcpdump folosește sintaxa BPF (Berkeley Packet Filter): 'tcp[tcpflags] & (tcp-syn|tcp-ack) == tcp-syn'. Opțiunea 'tcp.flags.syn == 1' este sintaxa de filtru de afișare Wireshark/tshark, nu sintaxa de captură tcpdump.]

---

### Q22. `N07.S03.Q05` — Capture privileges / Privilegii pentru captură

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

On Linux, must a packet-capture process always run with UID 0? [Pe Linux, procesul de captură a pachetelor trebuie întotdeauna să ruleze cu UID 0?]

- **a)** No. Appropriate capabilities and capture configuration can authorise a non-root process. [Nu. Capabilitățile și configurația de captură potrivite pot autoriza un proces non-root.]
- **b)** Yes. CAP_NET_RAW can only exist for UID 0. [Da. CAP_NET_RAW poate exista numai pentru UID 0.]
- **c)** No privileges or capabilities are ever needed. [Nu sunt necesare niciodată privilegii sau capabilități.]

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** Creating Linux packet/raw sockets requires CAP_NET_RAW in the relevant namespace; other capture operations may need additional privileges. The lab uses sudo for a simple known configuration. Do not equate that teaching choice with a universal requirement to run the whole analyser as root. [Crearea socketurilor packet/raw Linux necesită CAP_NET_RAW în namespace-ul relevant; alte operații pot necesita privilegii suplimentare. Laboratorul folosește sudo pentru o configurație simplă cunoscută. Alegerea didactică nu înseamnă că întregul analizor trebuie universal rulat ca root.]

</details>

---

### 23. `Multiple Choice`
**N07.S04.Q02: Capture vs Display Filters / Filtre de captură vs filtre de afișare**

> In Wireshark, what is the key difference between capture filters and display filters? [În Wireshark, care este diferența esențială între filtrele de captură și filtrele de afișare?]

- **a) Capture filters use BPF syntax and limit what is recorded; display filters use Wireshark syntax and filter what is shown from already-captured data [Filtrele de captură folosesc sintaxa BPF și limitează ce este înregistrat; filtrele de afișare folosesc sintaxa Wireshark și filtrează ce este afișat din datele deja capturate]**
- **b) Capture filters are applied retrospectively after full packet recording is complete, reducing the stored dataset post-hoc; display filters run during live packet acquisition and permanently discard non-matching frames at wire speed [Filtrele de captură se aplică retrospectiv după finalizarea completă a înregistrării pachetelor, reducând setul de date stocat post-hoc; filtrele de afișare rulează în timpul achiziției live de pachete și elimină permanent cadrele care nu corespund la viteza firului]**
- **c) Both filter types use identical syntax but are applied at different processing stages [Ambele tipuri de filtre folosesc sintaxă identică dar se aplică în etape diferite de procesare]**
- **d) Display filters permanently delete non-matching packets from the pcap file [Filtrele de afișare șterg permanent pachetele care nu corespund din fișierul pcap]**

> 💡 **Feedback:** Capture filters (BPF syntax, e.g., 'tcp port 9090') determine what the kernel records. Display filters (Wireshark syntax, e.g., 'tcp.port == 9090') filter the view of already-recorded data without discarding anything. [Filtrele de captură (sintaxa BPF, ex: 'tcp port 9090') determină ce înregistrează kernel-ul. Filtrele de afișare (sintaxa Wireshark, ex: 'tcp.port == 9090') filtrează vizualizarea datelor deja înregistrate fără a elimina nimic.]

---

### 24. `Multiple Choice`
**N07.S04.Q03: Display Filter for RST Packets / Filtru de afișare pentru pachete RST**

> Which Wireshark display filter shows only TCP packets with the RST (Reset) flag set? [Care filtru de afișare Wireshark arată doar pachetele TCP cu flag-ul RST (Reset) setat?]

- **a) tcp.flags.reset == 1 [tcp.flags.reset == 1]**
- **b) tcp[tcpflags] & tcp-rst != 0 [tcp[tcpflags] & tcp-rst != 0]**
- **c) tcp.reset == true [tcp.reset == true]**
- **d) filter tcp rst [filter tcp rst]**

> 💡 **Feedback:** Wireshark display filters use dot-notation: tcp.flags.reset == 1. The BPF-style expression is for tcpdump capture filters, not Wireshark display. tcp.reset and plain-text filters are not valid. [Filtrele de afișare Wireshark folosesc notație cu punct: tcp.flags.reset == 1. Expresia în stil BPF este pentru filtrele de captură tcpdump, nu pentru afișarea Wireshark. tcp.reset și filtrele text simplu nu sunt valide.]

---

### 25. `Multiple Choice`
**N07.S04.Q04: ICMP Unreachable Display Filter / Filtru de afișare ICMP Unreachable**

> Which Wireshark display filter isolates ICMP Destination Unreachable messages (typically generated by REJECT rules)? [Care filtru de afișare Wireshark izolează mesajele ICMP Destination Unreachable (generate de obicei de regulile REJECT)?]

- **a) icmp.type == 3 [icmp.type == 3]**
- **b) icmp.type == 8 [icmp.type == 8]**
- **c) icmp.unreachable == true [icmp.unreachable == true]**
- **d) icmp.code == 3 [icmp.code == 3]**

> 💡 **Feedback:** ICMP type 3 is Destination Unreachable. Type 8 is Echo Request (ping). 'icmp.unreachable' is not a valid field. icmp.code == 3 filters by sub-code (port unreachable) without constraining the type. [ICMP tipul 3 este Destination Unreachable. Tipul 8 este Echo Request (ping). 'icmp.unreachable' nu este un câmp valid. icmp.code == 3 filtrează după sub-cod (port unreachable) fără a constrânge tipul.]

---

### 26. `Multiple Choice`
**N07.S02.Q02: REJECT with TCP Reset / REJECT cu TCP Reset**

> To reject TCP connections to port 12345 with an explicit RST packet (rather than ICMP), which iptables target specification is correct? [Pentru a respinge conexiunile TCP la portul 12345 cu un pachet RST explicit (în loc de ICMP), care specificație de target iptables este corectă?]

- **a) -j REJECT --reject-with tcp-reset [-j REJECT --reject-with tcp-reset]**
- **b) -j REJECT --reject-with icmp-port-unreachable [-j REJECT --reject-with icmp-port-unreachable]**
- **c) -j DROP --reject-with tcp-reset [-j DROP --reject-with tcp-reset]**
- **d) -j REJECT --reset-tcp [-j REJECT --reset-tcp]**

> 💡 **Feedback:** The --reject-with tcp-reset option instructs the firewall to send a TCP RST packet. The default REJECT sends ICMP port unreachable. DROP cannot have --reject-with options. --reset-tcp is not a valid iptables syntax. [Opțiunea --reject-with tcp-reset instruiește paravanul de protecție să trimită un pachet TCP RST. REJECT implicit trimite ICMP port unreachable. DROP nu acceptă opțiuni --reject-with. --reset-tcp nu este o sintaxă iptables validă.]

---

### Q27. `N07.S02.Q06` — Explicit firewall rule set / Set explicit de reguli firewall

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

A hypothetical FORWARD chain accepts ICMP and UDP destination port 12345, explicitly rejects TCP destination port 12345 and silently drops everything unmatched. Which default policy implements the last clause? [Un lanț FORWARD ipotetic acceptă ICMP și UDP către portul 12345, respinge explicit TCP către portul 12345 și elimină silențios orice nu se potrivește. Ce politică implicită implementează ultima clauză?]

- **a)** DROP
- **b)** ACCEPT
- **c)** REJECT
- **d)** LOG

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** DROP is the specified default policy. This question defines its own rules and does not require an absent mixed_filtering profile. [DROP este politica implicită specificată. Itemul își definește propriile reguli și nu necesită un profil mixed_filtering absent.]

</details>

---

### Q28. `N07.S05.Q01` — Connection-probe error handling / Tratarea erorilor la conectare

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

Why can connect_ex simplify a TCP connection-probe loop? [De ce poate connect_ex simplifica o buclă de probe de conectare TCP?]

- **a)** Connection errors are generally returned as errno codes, allowing explicit classification; exceptions still need handling. [Erorile de conectare sunt în general returnate drept coduri errno, permițând clasificare explicită; excepțiile trebuie în continuare tratate.]
- **b)** It is always non-blocking. [Este întotdeauna neblocant.]
- **c)** It automatically retries every failed connection. [Reîncearcă automat orice conexiune eșuată.]

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** The return contract changes error handling, not timeout or blocking semantics. Use errno constants rather than assuming a numeric error is portable across platforms. [Contractul de retur schimbă tratarea erorilor, nu semantica de blocare sau timeout. Folosiți constante errno, nu presupuneți că un cod numeric este portabil între platforme.]

</details>

---

### Q29. `N07.S05.Q02` — Timeout evidence / Dovezi pentru timeout

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

A TCP connection attempt expires without completing. What is the justified observation? [O tentativă de conectare TCP expiră fără finalizare. Care este observația justificată?]

- **a)** No connection completed before the deadline; filtering, loss, an unreachable host or other causes remain possible. [Nicio conexiune nu s-a finalizat până la termen; filtrarea, pierderea, o gazdă inaccesibilă sau alte cauze rămân posibile.]
- **b)** A firewall DROP rule has been proved. [A fost demonstrată o regulă firewall DROP.]
- **c)** The port is certainly closed and sent RST. [Portul este sigur închis și a trimis RST.]

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** connect_ex may return a timeout-related errno rather than raise socket.timeout. Inspect returned codes and handle exceptions. A timeout describes the observation, not a unique remote port state. [connect_ex poate întoarce un errno asociat timeout-ului în loc să ridice socket.timeout. Inspectați codurile returnate și tratați excepțiile. Timeout-ul descrie observația, nu o stare unică a portului distant.]

</details>

---

### Q30. `N07.S05.Q04` — Controlled refusal case / Caz controlat de refuz

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

For a reachable local TCP endpoint with no listener, no firewall rejection and no race with another process, what result is normally expected from connect_ex? [Pentru un endpoint TCP local accesibil fără listener, fără respingere firewall și fără cursă cu alt proces, ce rezultat este așteptat în mod normal de la connect_ex?]

- **a)** `errno.ECONNREFUSED`
- **b)** `0`
- **c)** An application response body [Un corp de răspuns al aplicației]

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** In this controlled setup the operating system refuses the connection. Outside these assumptions, the same observed refusal can have other causes, including an explicit firewall reset. [În configurația controlată, sistemul de operare refuză conexiunea. În afara ipotezelor, același refuz observat poate avea alte cauze, inclusiv un reset firewall explicit.]

</details>

---

### Q31. `N07.S05.Q05` — First terminating firewall rule / Prima regulă firewall terminală

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

In a chain evaluated in order, a terminating DROP rule matching all TCP precedes an ACCEPT rule for TCP destination port 12345. What happens to a matching TCP packet for that port? [Într-un lanț evaluat în ordine, o regulă DROP terminală pentru tot TCP precede o regulă ACCEPT pentru TCP către portul 12345. Ce se întâmplă cu un pachet TCP potrivit pentru acel port?]

- **a)** It is dropped by the first rule; the later ACCEPT is not reached. [Este eliminat de prima regulă; ACCEPT ulterior nu este atins.]
- **b)** The more specific ACCEPT always overrides insertion order. [ACCEPT mai specific suprascrie mereu ordinea inserării.]
- **c)** Both terminal actions execute. [Se execută ambele acțiuni terminale.]

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** The ordering applies to matching terminating rules in this specified chain. Non-terminating operations such as LOG can continue processing. [Ordinea se aplică regulilor potrivite cu verdict terminal din lanțul specificat. Operații neterminale precum LOG pot continua procesarea.]

</details>

---

## W07 — Drag & Drop   (9 questions)

### 32. `Drag & Drop into Text`
**N02.D05.Q01: Build a Wireshark filter for TCP port 12345 / Construiți un filtru Wireshark pentru portul TCP 12345**

> Drag the tokens into the correct positions to build a Wireshark display filter that shows only TCP traffic on port 12345. [Trageți jetoanele în pozițiile corecte pentru a construi un filtru de afișare Wireshark care arată doar traficul TCP pe portul 12345.]

```
[[1]].[[2]] [[3]] [[4]]
```

**Available choices / Variante disponibile: tcp  |  port  |  ==  |  12345  |  udp  |  addr  |  =  |  80**


> 💡 **Feedback:** The correct filter is tcp.port == 12345. Wireshark display filters use a dot-separated field hierarchy (protocol.field), the double-equals comparison operator, and the value. Common mistakes include using a single equals sign (assignment, not comparison) or confusing tcp.port (matches either source or destination) with tcp.srcport or tcp.dstport. [Filtrul corect este tcp.port == 12345. Filtrele de afișare Wireshark folosesc o ierarhie de câmpuri separată prin punct (protocol.câmp), operatorul de comparare dublu-egal și valoarea. Greșeli frecvente includ utilizarea unui singur semn egal (atribuire, nu comparare) sau confundarea tcp.port (potrivește sursa sau destinația) cu tcp.srcport sau tcp.dstport.]

---

### 33. `Drag & Drop into Text`
**N02.D05.Q07: Build the tshark command for TCP conversation summary / Construiți comanda tshark pentru rezumatul conversațiilor TCP**

> Complete the tshark command to show a TCP conversation summary from a capture file. [Completați comanda tshark pentru a afișa un rezumat al conversațiilor TCP dintr-un fișier de captură.]

```
[[1]] -r pcap/week2_tcp.pcap -z [[2]],[[3]]
```

**Available choices / Variante disponibile: tshark  |  conv  |  tcp  |  tcpdump  |  stat  |  udp**


> 💡 **Feedback:** The command tshark -r file.pcap -z conv,tcp displays TCP conversation statistics including bytes transferred and duration. [Comanda tshark -r file.pcap -z conv,tcp afișează statisticile conversațiilor TCP, inclusiv octeții transferați și durata.]

---

### 34. `Drag & Drop into Text`
**N03.D05.Q07: tcpdump Save Capture / Salvare captură tcpdump**

> Complete the tcpdump command to capture test traffic known to traverse eth0 on port 12345 and save it to a pcap file. [Completați comanda tcpdump pentru a captura traficul de test despre care se știe că traversează eth0 pe portul 12345 și a-l salva într-un fișier pcap.]

```
tcpdump -i [[1]] [[2]] capture.pcap 'port [[3]]'
```

**Available choices / Variante disponibile: eth0  |  -w  |  12345  |  lo  |  -r  |  8080**


> 💡 **Feedback:** The command is: tcpdump -i eth0 -w capture.pcap 'port 12345'. The -w flag writes raw packets to a file for later analysis in Wireshark. The port and interface are assumptions supplied by this item; choose the actual traffic interface for a different topology. [Comanda este: tcpdump -i eth0 -w capture.pcap 'port 12345'. Opțiunea -w scrie pachetele brute într-un fișier pentru analiză ulterioară în Wireshark. Portul și interfața sunt ipoteze date de item; pentru altă topologie alegeți interfața traversată efectiv.]

---

### 35. `Drag & Drop into Text`
**N04.D05.Q02: Assemble Wireshark filter for TCP data on TEXT port / Asamblați filtrul Wireshark pentru date TCP pe portul TEXT**

> Assemble the Wireshark display filter that shows only data-carrying packets on the TEXT protocol port: [Asamblați filtrul de afișare Wireshark care arată doar pachetele cu date pe portul protocolului TEXT:]

```
[[1]].port == [[2]] && [[3]].len > 0
```

**Available choices / Variante disponibile: tcp  |  3333  |  tcp  |  udp  |  5401  |  ip**


> 💡 **Feedback:** tcp.port == 3333 && tcp.len > 0 — matches TCP packets on port 3333 that carry payload (excluding handshake and pure ACKs). [tcp.port == 3333 && tcp.len > 0 — potrivește pachetele TCP pe portul 3333 care transportă sarcină utilă (excluzând handshake-ul și ACK-urile pure).]

---

### 36. `Drag & Drop into Text`
**N04.D05.Q08: Complete Wireshark filter for payload content / Completați filtrul Wireshark pentru conținut sarcină utilă**

> Build the Wireshark filter to find TEXT protocol packets containing the SET command: [Construiți filtrul Wireshark pentru a găsi pachetele protocolului TEXT care conțin comanda SET:]

```
[[1]].port == 3333 && tcp.[[2]] contains "[[3]]"
```

**Available choices / Variante disponibile: tcp  |  payload  |  SET  |  udp  |  data  |  GET**


> 💡 **Feedback:** tcp.port == 3333 && tcp.payload contains "SET" — this display filter matches TCP packets on port 3333 whose payload includes the string SET. [tcp.port == 3333 && tcp.payload contains "SET" — acest filtru de afișare potrivește pachetele TCP pe portul 3333 a căror sarcină utilă include șirul SET.]

---

### 37. `Drag & Drop into Text`
**N06.D05.Q03: Build the Wireshark Display Filter / Construiți filtrul de afișare Wireshark**

> Drag the tokens to build a Wireshark display filter that shows only OpenFlow PACKET_IN messages. [Trageți simbolurile pentru a construi un filtru de afișare Wireshark care arată doar mesajele OpenFlow PACKET_IN.]

```
[[1]].[[2]] == [[3]]
```

**Available choices / Variante disponibile: openflow_v4  |  type  |  10  |  openflow_v1  |  code  |  14**


> 💡 **Feedback:** The correct filter is openflow_v4.type == 10. OpenFlow v4 (version 1.3) uses type code 10 for PACKET_IN messages. FLOW_MOD is type 14, and PACKET_OUT is type 13. [Filtrul corect este openflow_v4.type == 10. OpenFlow v4 (versiunea 1.3) folosește codul de tip 10 pentru mesajele PACKET_IN. FLOW_MOD este tipul 14, iar PACKET_OUT este tipul 13.]

---

### 38. `Drag & Drop into Text`
**N07.D05.Q05: tcpdump Compound Filter / Filtru compus tcpdump**

> Build a tcpdump filter for TCP traffic on port 9090 from host 10.0.7.100: [Construiți un filtru tcpdump pentru traficul TCP pe portul 9090 de la gazda 10.0.7.100:]

```
sudo tcpdump -i eth0 '[[1]] port 9090 [[2]] src host 10.0.7.100'
```

**Available choices / Variante disponibile: tcp  |  and  |  udp  |  or**


> 💡 **Feedback:** The filter combines protocol (tcp), port (9090), and source host (10.0.7.100) with the 'and' Boolean operator. 'or' would match either condition instead of requiring both. [Filtrul combină protocolul (tcp), portul (9090) și gazda sursă (10.0.7.100) cu operatorul boolean 'and'. 'or' ar potrivi oricare condiție în loc să le ceară pe amândouă.]

---

### Q39. `N07.D05.Q02` — Probe result interpretation / Interpretarea rezultatului probei

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

Which interpretation of TCP connect_ex outcomes is justified? [Ce interpretare a rezultatelor connect_ex pentru TCP este justificată?]

- **a)** 0: connection completed; ECONNREFUSED: active refusal; a timeout: no completed connection within the deadline. [0: conexiune finalizată; ECONNREFUSED: refuz activ; timeout: nicio conexiune finalizată până la termen.]
- **b)** Every non-zero return means closed and every exception means filtered. [Orice retur non-zero înseamnă închis și orice excepție înseamnă filtrat.]
- **c)** Any timeout proves the host does not exist. [Orice timeout dovedește că gazda nu există.]

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** Record the exact errno or exception. A timeout may be returned as an error code; refusal may originate at a firewall. These observations are not exhaustive diagnoses of the service or path. [Înregistrați errno-ul exact sau excepția. Timeout-ul poate fi returnat drept cod de eroare; refuzul poate proveni de la firewall. Observațiile nu constituie diagnostice exhaustive ale serviciului sau căii.]

</details>

---

### 40. `Drag & Drop into Text`
**N07.D05.Q08: Socket Connection for Port Probing / Conexiune socket pentru sondarea porturilor**

> In Python, create a TCP socket and set a 2-second timeout for port probing: [În Python, creați un socket TCP și setați un timeout de 2 secunde pentru sondarea porturilor:]

```
s = socket.socket(socket.AF_INET, socket.[[1]])
```

```
s.[[2]](2.0)
```

```
result = s.[[3]](('host', port))
```

**Available choices / Variante disponibile: SOCK_STREAM  |  settimeout  |  connect_ex  |  SOCK_DGRAM**


> 💡 **Feedback:** SOCK_STREAM = TCP socket, settimeout() configures the blocking timeout, connect_ex() returns error codes instead of raising exceptions. SOCK_DGRAM would create UDP socket. [SOCK_STREAM = socket TCP, settimeout() configurează timeout-ul blocant, connect_ex() returnează coduri de eroare în loc să ridice excepții. SOCK_DGRAM ar crea socket UDP.]

---


## W07 — Gap Select   (6 questions)

### 41. `Gap Select`
**N02.D10.Q07: Wireshark filter syntax elements / Elementele de sintaxă ale filtrelor Wireshark**

> Select the correct Wireshark display filter components. [Selectați componentele corecte ale filtrului de afișare Wireshark.]

```
To filter TCP traffic on port 12345: [[1]]. To filter only SYN packets: [[2]]. To filter packets to the supplied destination IP 10.0.2.10: [[3]].
```

**Available choices / Variante disponibile: tcp.port == 12345  |  tcp.flags.syn == 1  |  ip.dst == 10.0.2.10  |  tcp port 12345  |  tcp.syn = true  |  dst 10.0.2.10**


> 💡 **Feedback:** Wireshark display filters use dot notation (tcp.port, tcp.flags.syn, ip.dst). Capture filters (BPF syntax like 'tcp port 12345') are different from display filters. [Filtrele de afișare Wireshark folosesc notația cu puncte (tcp.port, tcp.flags.syn, ip.dst). Filtrele de captură (sintaxă BPF precum „tcp port 12345") sunt diferite de filtrele de afișare.]

---

### 42. `Gap Select`
**N03.D10.Q05: Broadcast MAC Address / Adresa MAC broadcast**

```
At Layer 2, broadcast frames use the destination MAC address [[1]]. This causes every [[2]] on the segment to process the frame. The Wireshark filter to capture these frames is [[3]]. [La Nivelul 2, cadrele broadcast folosesc adresa MAC destinație ___. Aceasta determină fiecare ___ din segment să proceseze cadrul. Filtrul Wireshark pentru a captura aceste cadre este ___.]
```

**Available choices / Variante disponibile: ff:ff:ff:ff:ff:ff  |  00:00:00:00:00:00  |  01:00:5e:00:00:01  |  NIC  |  router  |  switch  |  eth.dst == ff:ff:ff:ff:ff:ff  |  ip.dst == 255.255.255.255  |  frame.broadcast == 1**


> 💡 **Feedback:** The all-ones MAC ff:ff:ff:ff:ff:ff is the Ethernet broadcast address. Every NIC on the segment processes frames with this destination. The Wireshark display filter eth.dst == ff:ff:ff:ff:ff:ff isolates broadcast frames. [MAC-ul format doar din unu-uri ff:ff:ff:ff:ff:ff este adresa broadcast Ethernet. Fiecare NIC din segment procesează cadrele cu această destinație. Filtrul de afișare Wireshark eth.dst == ff:ff:ff:ff:ff:ff izolează cadrele broadcast.]

---

### 43. `Gap Select`
**N07.D10.Q06: tcpdump vs tshark vs Wireshark / tcpdump vs tshark vs Wireshark**

> Match each tool to its primary characteristic: [Potriviți fiecare instrument cu caracteristica sa principală:]

```
GUI with protocol dissection: [[1]]. [Interfață grafică cu disecția protocoalelor: ___.]
```

```
CLI packet capture with BPF filters: [[2]]. [Captură de pachete CLI cu filtre BPF: ___.]
```

```
CLI analysis with display filters and field extraction: [[3]]. [Analiză CLI cu filtre de afișare și extragerea câmpurilor: ___.]
```

**Available choices / Variante disponibile: Wireshark  |  tcpdump  |  tshark**


> 💡 **Feedback:** Wireshark provides GUI-based analysis with protocol dissection. tcpdump is CLI-based with BPF capture filters. tshark is Wireshark's CLI equivalent with display filters and -T fields extraction. [Wireshark oferă analiză grafică cu disecția protocoalelor. tcpdump este bazat pe CLI cu filtre de captură BPF. tshark este echivalentul CLI al Wireshark cu filtre de afișare și extragerea câmpurilor cu -T fields.]

---

### Q44. `N07.D10.Q02` — Known firewall actions / Acțiuni firewall cunoscute

*Matching / Asociere*

Match the configured action to its effect on a matching TCP packet. [Asociați acțiunea configurată cu efectul asupra unui pachet TCP potrivit.]

| Action / Acțiune | Effect / Efect |
|---|---|
| `DROP` | Silently discard this packet / Elimină silențios acest pachet |
| `REJECT --reject-with tcp-reset` | Send TCP RST / Trimite TCP RST |
| `ACCEPT` | Permit processing past this filter verdict / Permite continuarea după acest verdict de filtrare |

<details><summary>💡 Feedback</summary>

The table is the answer key. Predict effects from a known rule; do not infer a unique cause from a timeout or reset observed without configuration evidence. ACCEPT in one chain also does not prove end-to-end delivery. [Tabelul reprezintă cheia. Preziceți efectele unei reguli cunoscute; nu deduceți o cauză unică dintr-un timeout sau reset fără dovezi de configurație. ACCEPT într-un lanț nu dovedește livrarea capăt-la-capăt.]

</details>

---

### Q45. `N07.D10.Q03` — Probe result interpretation / Interpretarea rezultatului probei

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

Which interpretation of TCP connect_ex outcomes is justified? [Ce interpretare a rezultatelor connect_ex pentru TCP este justificată?]

- **a)** 0: connection completed; ECONNREFUSED: active refusal; a timeout: no completed connection within the deadline. [0: conexiune finalizată; ECONNREFUSED: refuz activ; timeout: nicio conexiune finalizată până la termen.]
- **b)** Every non-zero return means closed and every exception means filtered. [Orice retur non-zero înseamnă închis și orice excepție înseamnă filtrat.]
- **c)** Any timeout proves the host does not exist. [Orice timeout dovedește că gazda nu există.]

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** Record the exact errno or exception. A timeout may be returned as an error code; refusal may originate at a firewall. These observations are not exhaustive diagnoses of the service or path. [Înregistrați errno-ul exact sau excepția. Timeout-ul poate fi returnat drept cod de eroare; refuzul poate proveni de la firewall. Observațiile nu constituie diagnostice exhaustive ale serviciului sau căii.]

</details>

---

### Q46. `N07.D10.Q07` — DROP and REJECT trade-off / Compromisul DROP și REJECT

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

Which trade-off between DROP and REJECT is defensible? [Ce compromis între DROP și REJECT este justificat?]

- **a)** DROP withholds a rejection for matched packets; REJECT gives faster negative feedback. Choose policy for the stated service and environment. [DROP nu emite respingere pentru pachetele potrivite; REJECT oferă feedback negativ mai rapid. Alegeți politica pentru serviciul și mediul date.]
- **b)** DROP guarantees no information about the host can be learned. [DROP garantează că nu se poate afla nicio informație despre gazdă.]
- **c)** REJECT proves a listening service is present. [REJECT dovedește prezența unui serviciu care ascultă.]

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** Neither action is a universal security ranking. Scope the rule and assess operational needs; other traffic can reveal the host and rejection can be generated by an intermediate device. [Nicio acțiune nu reprezintă un clasament universal de securitate. Delimitați regula și evaluați nevoile operaționale; alt trafic poate dezvălui gazda, iar respingerea poate fi generată de un dispozitiv intermediar.]

</details>

---
