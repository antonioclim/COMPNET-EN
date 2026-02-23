# Week 07 — Computer Networks
### *Rețele de Calculatoare — Săptămâna 7*

> Question Pool — Practice Set

---


## W07 — Curs / Lecture   (15 questions)

### 1. `Multiple Choice`
**N01.T00.Q13: Choosing Capture Strategy for TCP vs UDP / Alegerea strategiei de captură pentru TCP vs UDP**

> A student needs to demonstrate both the TCP three-way handshake on port 12345 and a UDP datagram exchange on port 12345 inside week1_lab. The resulting PCAP must clearly distinguish both flows for grading. Which capture approach produces the cleanest evidence? [Un student trebuie să demonstreze atât handshake-ul TCP cu trei căi pe portul 12345, cât și un schimb de datagrame UDP pe portul 12345 în week1_lab. Fișierul PCAP rezultat trebuie să distingă clar ambele fluxuri pentru notare. Ce abordare de captură produce cele mai curate dovezi?]

- **a) Run tcpdump -i lo -w capture.pcap port 12345 or port 12345, then use Wireshark display filters to separate the TCP and UDP flows in the single capture file [Rulați tcpdump -i lo -w capture.pcap port 12345 or port 12345, apoi folosiți filtre de afișare Wireshark pentru a separa fluxurile TCP și UDP]**
- **b) Run two separate tcpdump instances simultaneously, one filtering tcp port 12345 and the other filtering udp port 12345, writing to different PCAP files [Rulați două instanțe tcpdump separat simultan, una filtrând tcp port 12345 și cealaltă filtrând udp port 12345, scriind în fișiere PCAP diferite]**
- **c) Capture on eth0 with no filter to ensure all traffic is captured, then apply display filters in Wireshark to isolate the relevant ports [Capturați pe eth0 fără filtru pentru a vă asigura că tot traficul este capturat, apoi aplicați filtre de afișare în Wireshark]**

> 💡 **Feedback:** A single capture on loopback with a compound BPF filter (port 12345 or port 12345) captures both flows interleaved. The display filters tcp.port==12345 and udp.port==12345 cleanly separate them in Wireshark. Separate captures create file management overhead and risk missing interleaved traffic. Capturing on eth0 misses loopback-only traffic. [O singură captură pe loopback cu un filtru BPF compus surprinde ambele fluxuri intercalate. Filtrele de afișare le separă curat în Wireshark.]

---

### 2. `Multiple Choice`
**N02.C02.Q01: Correct sequence of TCP three-way handshake flags / Secvența corectă a indicatorilor în handshake-ul TCP în trei pași**

> What is the correct order of TCP flag exchanges during the three-way handshake that establishes a connection? [Care este ordinea corectă a schimbului de indicatori TCP în timpul handshake-ului în trei pași care stabilește o conexiune?]

- **a) SYN → SYN-ACK → ACK**
- **b) ACK → SYN → SYN-ACK**
- **c) SYN → ACK → SYN-ACK**
- **d) SYN-ACK → SYN → ACK**

> 💡 **Feedback:** The client initiates with SYN, the server responds with SYN-ACK, and the client completes with ACK. This three-step process synchronises sequence numbers on both endpoints before any data is exchanged. A common misconception is that the handshake occurs for every message sent; in reality, it happens only once when connect() is called, and all subsequent data flows over the established connection. [Clientul inițiază cu SYN, serverul răspunde cu SYN-ACK, iar clientul finalizează cu ACK. Acest proces în trei pași sincronizează numerele de secvență la ambele capete înainte de orice schimb de date. O concepție greșită frecventă este că handshake-ul are loc pentru fiecare mesaj trimis; în realitate, acesta se produce o singură dată la apelul connect(), iar toate datele ulterioare circulă pe conexiunea deja stabilită.]

---

### 3. `True / False`
**N07.C01.Q02: TCP Connection-Oriented Nature / Natura orientată pe conexiune a TCP**

> TCP requires a three-way handshake (SYN, SYN-ACK, ACK) to be completed before any application data can be transmitted. [TCP necesită finalizarea unui handshake în trei pași (SYN, SYN-ACK, ACK) înainte ca orice date ale aplicației să fie transmise.]

- **a) true**
- **b) false**

> 💡 **Feedback:** TCP is connection-oriented — unlike UDP, it cannot send application data until the three-way handshake synchronises initial sequence numbers on both sides. [TCP este orientat pe conexiune — spre deosebire de UDP, nu poate trimite date ale aplicației până când handshake-ul în trei pași nu sincronizează numerele de secvență inițiale pe ambele părți.]

---

### 4. `Multiple Choice`
**N07.C03.Q03: connect_ex vs connect Distinction / Distincția între connect_ex și connect**

> In the port probe code, connect_ex() is used instead of connect(). What practical advantage does connect_ex() provide for port probing? [În codul de sondare a porturilor, se folosește connect_ex() în loc de connect(). Ce avantaj practic oferă connect_ex() pentru sondarea porturilor?]

- **a) It returns an error code (0 for success, non-zero for failure) instead of raising an exception, simplifying state classification [Returnează un cod de eroare (0 pentru succes, non-zero pentru eșec) în loc să ridice o excepție, simplificând clasificarea stării]**
- **b) It automatically handles both TCP and UDP probing in a single function call [Gestionează automat sondarea atât TCP cât și UDP într-un singur apel de funcție]**
- **c) It supports asynchronous connections, allowing multiple ports to be probed simultaneously [Suportă conexiuni asincrone, permițând sondarea simultană a mai multor porturi]**
- **d) It bypasses firewall rules by using raw sockets at the kernel level, giving more accurate probe results and revealing the true state of every port regardless of iptables configuration [Ocolește regulile de firewall folosind socketuri raw la nivelul nucleului, oferind rezultate de sondare mai precise și dezvăluind starea reală a fiecărui port indiferent de configurația iptables]**

> 💡 **Feedback:** connect_ex() returns an integer error code rather than raising an exception. A return of 0 means the port is open; a non-zero value (e.g. 111 = ECONNREFUSED) means closed. socket.timeout exceptions still indicate filtered ports. This avoids wrapping every probe in try/except for the normal closed-port case. [connect_ex() returnează un cod de eroare întreg în loc să ridice o excepție. Un retur de 0 înseamnă că portul este deschis; o valoare non-zero (de ex. 111 = ECONNREFUSED) înseamnă închis. Excepțiile socket.timeout indică în continuare porturile filtrate. Aceasta evită încadrarea fiecărei sondări într-un try/except pentru cazul normal de port închis.]

---

### 5. `Multiple Choice`
**N07.C03.Q04: Port Probe Timeout Interpretation / Interpretarea timeout-ului sondării de porturi**

> The port probe script sets sock.settimeout(2.0) and attempts connect_ex(). A socket.timeout exception is raised. How does the script classify this port? [Scriptul de sondare a porturilor setează sock.settimeout(2.0) și încearcă connect_ex(). O excepție socket.timeout este ridicată. Cum clasifică scriptul acest port?]

- **a) Filtered — the timeout indicates no response was received, likely due to a firewall DROP rule [Filtrat — timeout-ul indică că nu s-a primit niciun răspuns, probabil din cauza unei reguli DROP de la firewall]**
- **b) Open — the timeout means the server is busy processing the connection and needs more time [Deschis — timeout-ul înseamnă că serverul este ocupat procesând conexiunea și are nevoie de mai mult timp]**
- **c) Closed — the timeout is functionally equivalent to receiving a TCP RST packet [Închis — timeout-ul este echivalent funcțional cu primirea unui pachet TCP RST]**
- **d) Error — the timeout indicates an unreachable network rather than a filtering decision [Eroare — timeout-ul indică o rețea inaccesibilă și nu o decizie de filtrare]**

> 💡 **Feedback:** When connect_ex() times out, it means no response was received — neither SYN-ACK (open) nor RST (closed). This is consistent with a firewall DROP rule silently discarding the probe. The code uses the try/except block to classify timeouts as "filtered". [Când connect_ex() expiră, înseamnă că nu s-a primit niciun răspuns — nici SYN-ACK (deschis), nici RST (închis). Aceasta este consistentă cu o regulă DROP care elimină în tăcere sondarea. Codul folosește blocul try/except pentru a clasifica timeout-urile ca 'filtrat'.]

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

### 8. `Multiple Choice`
**N07.C05.Q01: External Service Filtering Choice / Alegerea filtrării pentru servicii externe**

> An attacker is scanning your public-facing network to discover which services are running. Which filtering action makes it hardest for the attacker to identify active hosts and open ports? [Un atacator scanează rețeaua dvs. publică pentru a descoperi ce servicii rulează. Care acțiune de filtrare face cel mai dificil pentru atacator să identifice gazdele active și porturile deschise?]

- **a) DROP — all probed ports appear "filtered" with timeouts, so the attacker cannot distinguish active services from non-existent hosts [DROP — toate porturile sondate apar 'filtrate' cu timeout-uri, astfel încât atacatorul nu poate distinge serviciile active de gazdele inexistente]**
- **b) REJECT — the attacker receives explicit refusal messages for each probed port, but these do not reveal which specific services are running behind the firewall [REJECT — atacatorul primește mesaje explicite de refuz pentru fiecare port sondat, dar acestea nu dezvăluie ce servicii specifice rulează în spatele paravanului de protecție]**
- **c) ACCEPT with rate limiting — allowing connections but throttling them prevents effective reconnaissance [ACCEPT cu limitare de rată — permiterea conexiunilor dar limitarea lor previne recunoașterea eficientă]**
- **d) LOG without any action — recording the probes deters the attacker without blocking anything [LOG fără nicio acțiune — înregistrarea sondărilor descurajează atacatorul fără a bloca nimic]**

> 💡 **Feedback:** DROP makes all ports appear identically "filtered" — the attacker sees timeouts everywhere and cannot distinguish between a host with DROP on port 80 versus a non-existent host. REJECT reveals that a firewall (and therefore a host) exists by sending back RST or ICMP. [DROP face toate porturile să apară identic ca 'filtrate' — atacatorul vede timeout-uri peste tot și nu poate distinge între o gazdă cu DROP pe portul 80 și o gazdă inexistentă. REJECT dezvăluie că un paravan de protecție (și prin urmare o gazdă) există prin trimiterea înapoi a RST sau ICMP.]

---

### 9. `Multiple Choice`
**N07.T00.Q04: Closed vs Filtered Port / Port închis vs port filtrat**

> What distinguishes a closed TCP port from a filtered TCP port when probed with a SYN packet? [Ce distinge un port TCP închis de un port TCP filtrat când este sondat cu un pachet SYN?]

- **a) A closed port sends RST immediately; a filtered port produces no response (timeout) [Un port închis trimite RST imediat; un port filtrat nu produce niciun răspuns (timeout)]**
- **b) A closed port sends ICMP unreachable after consulting the routing table; a filtered port sends TCP RST back to the sender [Un port închis trimite ICMP unreachable după consultarea tabelei de rutare; un port filtrat trimite TCP RST înapoi expeditorului]**
- **c) Both send RST, but a filtered port includes an ICMP warning [Ambele trimit RST, dar un port filtrat include o avertizare ICMP]**
- **d) A closed port produces a timeout; a filtered port sends FIN-ACK [Un port închis produce un timeout; un port filtrat trimite FIN-ACK]**

> 💡 **Feedback:** Closed = host reachable, no service listening → kernel sends RST. Filtered = firewall DROP → no response, client times out. This distinction is critical for network diagnosis: RST confirms host reachability. [Închis = gazdă accesibilă, niciun serviciu activ → nucleul trimite RST. Filtrat = DROP de la paravan → niciun răspuns, clientul dă timeout. Această distincție este critică pentru diagnosticul rețelei: RST confirmă accesibilitatea gazdei.]

---

### 10. `Multiple Choice`
**N07.T00.Q05: connect_ex() Port Probe Advantage / Avantajul connect_ex() pentru sondarea porturilor**

> Why is socket.connect_ex() preferred over socket.connect() for port scanning scripts? [De ce este socket.connect_ex() preferat față de socket.connect() pentru scripturile de scanare a porturilor?]

- **a) It returns an error code instead of raising an exception, simplifying control flow [Returnează un cod de eroare în loc să ridice o excepție, simplificând fluxul de control]**
- **b) It bypasses firewall rules at the kernel level to detect services hidden behind DROP policies [Ocolește regulile de paravan la nivelul nucleului pentru a detecta servicii ascunse în spatele politicilor DROP]**
- **c) It automatically retries on timeout, improving detection accuracy [Reîncearcă automat la timeout, îmbunătățind acuratețea detecției]**
- **d) It supports both TCP and UDP probing in a single call [Suportă sondarea atât TCP cât și UDP într-un singur apel]**

> 💡 **Feedback:** connect_ex() returns 0 on success or an errno value on failure. This allows clean if/else logic instead of try/except blocks. It does NOT bypass firewalls, retry automatically, or support UDP. [connect_ex() returnează 0 la succes sau o valoare errno la eșec. Aceasta permite logică if/else curată în loc de blocuri try/except. NU ocolește paravanele, nu reîncearcă automat și nu suportă UDP.]

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

### 12. `Multiple Choice`
**N07.C02.Q04: DROP vs REJECT for Debugging / DROP vs REJECT pentru depanare**

> During development on an internal network, a colleague cannot connect to your test server. You suspect a firewall rule is blocking the traffic. Which filtering action would have made the problem easier to diagnose? [În timpul dezvoltării pe o rețea internă, un coleg nu se poate conecta la serverul dvs. de test. Suspectați că o regulă de firewall blochează traficul. Care acțiune de filtrare ar fi făcut problema mai ușor de diagnosticat?]

- **a) REJECT — the immediate "Connection refused" error clearly indicates a firewall is active and blocking traffic [REJECT — eroarea imediată 'Conexiune refuzată' indică clar că un paravan de protecție este activ și blochează traficul]**
- **b) DROP — the timeout behaviour provides more security, which is the top priority even for internal debugging [DROP — comportamentul de timeout oferă mai multă securitate, care este prioritatea principală chiar și pentru depanarea internă]**
- **c) LOG — logging alone resolves the connectivity issue without any additional configuration changes [LOG — doar logarea rezolvă problema de conectivitate fără nicio modificare suplimentară de configurare]**
- **d) ACCEPT — switching all rules to ACCEPT is the only reliable diagnostic approach for internal networks [ACCEPT — schimbarea tuturor regulilor la ACCEPT este singura abordare de diagnostic fiabilă pentru rețelele interne]**

> 💡 **Feedback:** For internal debugging, REJECT is preferable because the immediate feedback (connection refused) saves considerable diagnostic time compared to waiting for DROP timeouts. DROP is better suited for external-facing services where concealing the firewall's presence is more important than fast diagnosis. [Pentru depanarea internă, REJECT este preferabil deoarece feedback-ul imediat (conexiune refuzată) economisește timp considerabil de diagnostic comparativ cu așteptarea timeout-urilor DROP. DROP este mai potrivit pentru serviciile expuse extern, unde ascunderea prezenței paravanului de protecție este mai importantă decât diagnosticul rapid.]

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

> 💡 **Feedback:** UDP has no delivery confirmation. The sendto() call completes successfully the moment the packet leaves the local network stack. Whether a firewall DROPs it, the network loses it, or the receiver is offline — the sender never learns of the failure without an application-layer acknowledgement protocol. [UDP nu are confirmare de livrare. Apelul sendto() se finalizează cu succes în momentul în care pachetul părăsește stiva locală de rețea. Fie că un paravan de protecție îl elimină, rețeaua îl pierde sau receptorul este offline — expeditorul nu află niciodată de eșec fără un protocol de confirmare la nivel de aplicație.]

---

### 15. `Multiple Choice`
**N07.T00.Q03: UDP Delivery Guarantee / Garanția de livrare UDP**

> A Python program calls sendto() to send a UDP datagram to a host with a DROP rule on the destination port. What value does sendto() return? [Un program Python apelează sendto() pentru a trimite o datagramă UDP către o gazdă cu o regulă DROP pe portul destinație. Ce valoare returnează sendto()?]

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

> 💡 **Feedback:** The filter tcp.flags.syn == 1 and tcp.flags.ack == 0 matches only the initial SYN packet from the client (not the SYN-ACK from the server). Using only tcp.flags.syn == 1 (also matches SYN-ACK packets / potrivește și pachetele SYN-ACK) would also match SYN-ACK packets (which have both SYN and ACK flags set), giving false positives. This is a critical distinction in Wireshark analysis for counting the number of new TCP connections. [Filtrul tcp.flags.syn == 1 and tcp.flags.ack == 0 corespunde doar pachetului SYN inițial de la client (nu SYN-ACK de la server). Utilizarea doar a tcp.flags.syn == 1 ar corespunde și pachetelor SYN-ACK (care au ambii indicatori SYN și ACK setați), producând rezultate fals pozitive. Aceasta este o distincție critică în analiza Wireshark pentru numărarea conexiunilor TCP noi.]

---

### 17. `Multiple Choice`
**N02.S03.Q05: Identifying a new TCP connection in a Wireshark capture / Identificarea unei conexiuni TCP noi într-o captură Wireshark**

> When analysing a Wireshark capture containing many TCP conversations, how can you identify the very first packet of a new TCP connection? [Când analizați o captură Wireshark care conține multe conversații TCP, cum puteți identifica chiar primul pachet al unei conexiuni TCP noi?]

- **a) Look for a packet with the SYN flag set and the ACK flag not set [Căutați un pachet cu indicatorul SYN setat și indicatorul ACK nesetat]**
- **b) Look for the first packet with the ACK flag set [Căutați primul pachet cu indicatorul ACK setat]**
- **c) Look for a packet with the RST flag set [Căutați un pachet cu indicatorul RST setat]**
- **d) Look for the packet with the smallest sequence number in the capture [Căutați pachetul cu cel mai mic număr de secvență din captură]**

> 💡 **Feedback:** The first packet of a TCP connection is a SYN packet with no ACK flag set. The filter tcp.flags.syn == 1 and tcp.flags.ack == 0 isolates these initial SYN packets. The second packet (SYN-ACK) has both SYN and ACK set, so it would not match this filter. A common error is looking for the packet with the smallest sequence number, but sequence numbers are random initial values, not ordered from zero. [Primul pachet al unei conexiuni TCP este un pachet SYN fără indicatorul ACK setat. Filtrul tcp.flags.syn == 1 and tcp.flags.ack == 0 izolează aceste pachete SYN inițiale. Al doilea pachet (SYN-ACK) are ambii indicatori SYN și ACK setați, deci nu ar corespunde acestui filtru. O eroare frecventă este căutarea pachetului cu cel mai mic număr de secvență, dar numerele de secvență sunt valori inițiale aleatoare, nu ordonate de la zero.]

---

### 18. `Multiple Choice`
**N03.S03.Q02: Direct vs Tunnel Test / Test direct vs prin tunel**

> Exercise 3 first tests a direct connection with echo 'DIRECT TEST' | nc server 8080, then tests the tunnel with echo 'TUNNEL TEST' | nc router 9090. Both return the echoed message. What is the key difference observable in Wireshark? [Exercițiul 3 testează mai întâi o conexiune directă cu echo 'DIRECT TEST' | nc server 8080, apoi testează tunelul cu echo 'TUNNEL TEST' | nc router 9090. Ambele returnează mesajul ecou. Care este diferența cheie observabilă în Wireshark?]

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

- **a) The destination port is closed or blocked — no service is listening there [Portul destinație este închis sau blocat — niciun serviciu nu ascultă acolo]**
- **b) A successful TCP three-way handshake has been completed normally [Un handshake TCP cu trei căi a fost finalizat cu succes]**
- **c) The server is performing load balancing by redirecting the connection [Serverul efectuează echilibrarea încărcăturii prin redirecționarea conexiunii]**
- **d) The client has requested a half-close of the TCP connection [Clientul a solicitat o semi-închidere a conexiunii TCP]**

> 💡 **Feedback:** RST,ACK as a response to SYN means the destination port is closed (no service listening) or the connection was actively refused by a firewall. A successful handshake would show SYN → SYN,ACK → ACK. [RST,ACK ca răspuns la SYN înseamnă că portul destinație este închis (niciun serviciu nu ascultă) sau conexiunea a fost refuzată activ de un paravan de protecție. Un handshake reușit ar arăta SYN → SYN,ACK → ACK.]

---

### 21. `Multiple Choice`
**N07.S03.Q01: Capture Only SYN Packets / Capturarea doar a pachetelor SYN**

> Which tcpdump filter expression captures only TCP SYN packets (the first step of the three-way handshake)? [Care expresie de filtru tcpdump capturează doar pachetele TCP SYN (primul pas al handshake-ului tripartit)?]

- **a) tcp[tcpflags] & tcp-syn != 0 [tcp[tcpflags] & tcp-syn != 0]**
- **b) tcp.flags.syn == 1 and not tcp.flags.ack [tcp.flags.syn == 1 and not tcp.flags.ack]**
- **c) tcp filter syn [tcp filter syn]**
- **d) tcp --syn-only [tcp --syn-only]**

> 💡 **Feedback:** tcpdump uses BPF (Berkeley Packet Filter) syntax: 'tcp[tcpflags] & tcp-syn != 0'. The option 'tcp.flags.syn == 1' is Wireshark/tshark display filter syntax, not tcpdump capture syntax. [tcpdump folosește sintaxa BPF (Berkeley Packet Filter): 'tcp[tcpflags] & tcp-syn != 0'. Opțiunea 'tcp.flags.syn == 1' este sintaxa de filtru de afișare Wireshark/tshark, nu sintaxa de captură tcpdump.]

---

### 22. `True / False`
**N07.S03.Q05: tcpdump Requires Root Privileges / tcpdump necesită privilegii root**

> The tcpdump command requires root (sudo) privileges because it needs raw socket access to capture packets at the network interface level. [Comanda tcpdump necesită privilegii root (sudo) deoarece are nevoie de acces la socket-uri brute pentru a captura pachete la nivelul interfeței de rețea.]

- **a) true**
- **b) false**

> 💡 **Feedback:** Raw packet capture operates below the normal socket API, reading frames directly from the network interface. This privileged operation requires CAP_NET_RAW, hence the sudo requirement. [Captura de pachete brute operează sub API-ul normal de socket, citind cadre direct de la interfața de rețea. Această operațiune privilegiată necesită CAP_NET_RAW, de aici cerința sudo.]

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

### 27. `Multiple Choice`
**N07.S02.Q06: mixed_filtering Default Policy / Politica implicită mixed_filtering**

> In the lab's 'mixed_filtering' firewall profile, what is the FORWARD chain default policy (forward_policy)? [În profilul de firewall 'mixed_filtering' al laboratorului, care este politica implicită a lanțului FORWARD (forward_policy)?]

- **a) DROP (all traffic blocked unless explicitly allowed) [DROP (tot traficul blocat dacă nu este permis explicit)]**
- **b) ACCEPT (all traffic allowed unless explicitly blocked) [ACCEPT (tot traficul permis dacă nu este blocat explicit)]**
- **c) REJECT (all traffic refused with ICMP notification) [REJECT (tot traficul refuzat cu notificare ICMP)]**
- **d) LOG (all traffic recorded but still forwarded) [LOG (tot traficul înregistrat dar încă redirecționat)]**

> 💡 **Feedback:** The mixed_filtering profile sets forward_policy: DROP, making it a whitelist configuration. Only explicitly allowed traffic passes (ICMP and UDP 12345 are ACCEPTed; TCP 12345 is REJECTed; everything else is DROPped). [Profilul mixed_filtering setează forward_policy: DROP, făcându-l o configurație de tip whitelist. Doar traficul permis explicit trece (ICMP și UDP 12345 sunt acceptate; TCP 12345 este REJECT; orice altceva este DROP).]

---

### 28. `Multiple Choice`
**N07.S05.Q01: connect_ex() vs connect() / connect_ex() vs connect()**

> In the lab's port_probe.py, the probe() function uses sock.connect_ex() instead of sock.connect(). What is the practical difference? [În port_probe.py din laborator, funcția probe() folosește sock.connect_ex() în loc de sock.connect(). Care este diferența practică?]

- **a) connect_ex() returns an error code (0 for success) instead of raising an exception, allowing programmatic status checking [connect_ex() returnează un cod de eroare (0 pentru succes) în loc să ridice o excepție, permițând verificarea programatică a stării]**
- **b) connect_ex() performs an extended connection with automatic retry on failure, unlike connect() which tries once [connect_ex() realizează o conexiune extinsă cu reîncercare automată la eșec, spre deosebire de connect() care încearcă o singură dată]**
- **c) connect_ex() establishes a connection in non-blocking mode regardless of the socket timeout setting [connect_ex() stabilește o conexiune în mod non-blocant indiferent de setarea timeout-ului socket-ului]**
- **d) connect_ex() sends an extended TCP handshake with additional diagnostic headers [connect_ex() trimite un handshake TCP extins cu antete de diagnosticare suplimentare]**

> 💡 **Feedback:** connect_ex() returns 0 on success or an OS error code (e.g., 111 ECONNREFUSED on Linux) on failure. connect() raises socket.error on failure. The 'ex' suffix means 'extended error reporting', not 'extended connection'. [connect_ex() returnează 0 la succes sau un cod de eroare OS (ex: 111 ECONNREFUSED pe Linux) la eșec. connect() ridică socket.error la eșec. Sufixul 'ex' înseamnă 'raportare extinsă a erorilor', nu 'conexiune extinsă'.]

---

### 29. `Multiple Choice`
**N07.S05.Q02: Port Probe: Filtered State Detection / Sondare port: Detectarea stării filtered**

> In port_probe.py, when does the probe() function return 'timeout' (indicating a filtered port)? [În port_probe.py, când returnează funcția probe() valoarea 'timeout' (indicând un port filtrat)?]

- **a) When socket.timeout exception is caught, meaning the connect_ex() call blocked until the timeout expired with no response [Când excepția socket.timeout este capturată, însemnând că apelul connect_ex() a blocat până la expirarea timeout-ului fără răspuns]**
- **b) When connect_ex() returns error code 110 (ETIMEDOUT), which the function maps to the timeout string [Când connect_ex() returnează codul de eroare 110 (ETIMEDOUT), pe care funcția îl mapează la șirul timeout]**
- **c) When the TCP handshake completes successfully but the server does not respond to the application data payload within the configured timeout period [Când handshake-ul TCP se completează cu succes dar serverul nu răspunde la sarcina utilă de date a aplicației în perioada de timeout configurată]**
- **d) When connect_ex() returns 0 but subsequent recv() times out, distinguishing open but unresponsive services [Când connect_ex() returnează 0 dar recv() ulterior expiră, distingând serviciile deschise dar care nu răspund]**

> 💡 **Feedback:** In port_probe.py, the try/except catches socket.timeout. This occurs when a firewall DROP rule silently discards the SYN — the socket waits for a response that never arrives until the configured timeout. [În port_probe.py, blocul try/except captează socket.timeout. Aceasta apare când o regulă firewall DROP elimină silențios SYN-ul — socket-ul așteaptă un răspuns care nu vine niciodată până la timeout-ul configurat.]

---

### 30. `Multiple Choice`
**N07.S05.Q04: Code Tracing: Closed Port Path / Trasare cod: Calea pentru port închis**

> In the code_tracing.md Exercise T2, when probe_port() is called on port 9999 with no server and no firewall, what execution path is followed? [În Exercițiul T2 din code_tracing.md, când probe_port() este apelat pe portul 9999 fără server și fără firewall, ce cale de execuție este urmată?]

- **a) Lines 1→2→3→4→6→9→10, returning 'closed' (connect_ex returns non-zero ECONNREFUSED) [Liniile 1→2→3→4→6→9→10, returnând 'closed' (connect_ex returnează non-zero ECONNREFUSED)]**
- **b) Lines 1→2→3→7→8→9→10, returning 'filtered' (socket.timeout exception is raised after blocking) [Liniile 1→2→3→7→8→9→10, returnând 'filtered' (excepția socket.timeout se ridică după blocare)]**
- **c) Lines 1→2→3→4→5→9→10, returning 'open' (connect_ex returns 0) [Liniile 1→2→3→4→5→9→10, returnând 'open' (connect_ex returnează 0)]**
- **d) Lines 1→2→3→7→10, returning 'error' (generic exception is raised) [Liniile 1→2→3→7→10, returnând 'error' (se ridică excepție generică)]**

> 💡 **Feedback:** With no server listening and no firewall, the OS kernel responds with RST (ECONNREFUSED, code 111 on Linux). connect_ex() returns non-zero, so result != 0 at Line 4, branching to Line 6 (status = 'closed'). The finally block (Line 9) always executes. [Fără server care ascultă și fără firewall, kernel-ul OS răspunde cu RST (ECONNREFUSED, cod 111 pe Linux). connect_ex() returnează non-zero, deci result != 0 la Linia 4, ramificând la Linia 6 (status = 'closed'). Blocul finally (Linia 9) se execută întotdeauna.]

---

### 31. `Multiple Choice`
**N07.S05.Q05: Rule Order in Firewall Processing / Ordinea regulilor în procesarea firewall**

> In code_tracing.md Exercise T3, if the default DROP rule (rule index 3, port=None) were moved to position 0, what would happen to TCP traffic on port 12345? [În Exercițiul T3 din code_tracing.md, dacă regula DROP implicită (indexul 3, port=None) ar fi mutată la poziția 0, ce s-ar întâmpla cu traficul TCP pe portul 12345?]

- **a) TCP 12345 would be DROPped because the general-purpose rule (port=None) matches all TCP before specific port rules are checked [TCP 12345 ar fi eliminat cu DROP deoarece regula cu scop general (port=None) potrivește tot TCP-ul înainte ca regulile specifice de port să fie verificate]**
- **b) TCP 12345 would still be ACCEPTed because iptables automatically prioritizes specific port-match rules over general catch-all rules regardless of their declared insertion order [TCP 12345 ar fi tot ACCEPT deoarece iptables prioritizează automat regulile cu potrivire specifică de port față de regulile generale de tip catch-all indiferent de ordinea lor declarată de inserare]**
- **c) TCP 12345 would be REJECTed because the REJECT rule has higher priority than DROP regardless of position [TCP 12345 ar fi REJECT deoarece regula REJECT are prioritate mai mare decât DROP indiferent de poziție]**
- **d) The firewall would raise an error because a None-port rule cannot precede port-specific rules [Paravanul de protecție ar genera o eroare deoarece o regulă cu port None nu poate preceda regulile specifice de port]**

> 💡 **Feedback:** Firewall rules are evaluated sequentially — first match wins. A general rule (port=None) at position 0 matches ALL TCP traffic before any specific port rule can be reached. This is why specific rules must always precede general/default rules. [Regulile de firewall sunt evaluate secvențial — prima potrivire câștigă. O regulă generală (port=None) la poziția 0 potrivește TOT traficul TCP înainte ca vreo regulă specifică de port să fie atinsă. De aceea regulile specifice trebuie întotdeauna să preceadă regulile generale/implicite.]

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

> Complete the tcpdump command to capture tunnel traffic on port 12345 and save it to a pcap file. [Completați comanda tcpdump pentru a captura traficul tunelului pe portul 12345 și a-l salva într-un fișier pcap.]

```
tcpdump -i [[1]] [[2]] capture.pcap 'port [[3]]'
```

**Available choices / Variante disponibile: eth0  |  -w  |  12345  |  lo  |  -r  |  8080**


> 💡 **Feedback:** The command is: tcpdump -i eth0 -w capture.pcap 'port 12345'. The -w flag writes raw packets to a file for later analysis in Wireshark. Port 12345 is the tunnel listen port on the router. [Comanda este: tcpdump -i eth0 -w capture.pcap 'port 12345'. Opțiunea -w scrie pachetele brute într-un fișier pentru analiză ulterioară în Wireshark. Portul 12345 este portul de ascultare al tunelului pe ruter.]

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
sudo tcpdump -i eth0 '[[1]] port 9090 [[2]] host 10.0.7.100'
```

**Available choices / Variante disponibile: tcp  |  and  |  udp  |  or**


> 💡 **Feedback:** The filter combines protocol (tcp), port (9090), and source host (10.0.7.100) with the 'and' Boolean operator. 'or' would match either condition instead of requiring both. [Filtrul combină protocolul (tcp), portul (9090) și gazda sursă (10.0.7.100) cu operatorul boolean 'and'. 'or' ar potrivi oricare condiție în loc să le ceară pe amândouă.]

---

### 39. `Drag & Drop into Text`
**N07.D05.Q02: Port Probe Results / Rezultatele sondării porturilor**

> The port_probe.py script classifies ports into states. Complete the mapping: [Scriptul port_probe.py clasifică porturile în stări. Completați maparea:]

```
connect_ex() returns 0 → port is [[1]] [connect_ex() returnează 0 → portul este ___]
```

```
connect_ex() returns non-zero → port is [[2]] [connect_ex() returnează non-zero → portul este ___]
```

```
socket.timeout is raised → port is [[3]] [socket.timeout este ridicat → portul este ___]
```

**Available choices / Variante disponibile: open  |  closed  |  filtered  |  unknown**


> 💡 **Feedback:** connect_ex() returns 0 for successful connection (open), non-zero error code for refused connection (closed), and socket.timeout indicates no response (filtered by DROP). [connect_ex() returnează 0 pentru conexiune reușită (deschis), cod de eroare non-zero pentru conexiune refuzată (închis), iar socket.timeout indică absența răspunsului (filtrat cu DROP).]

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
To filter TCP traffic on port 12345: [[1]]. To filter only SYN packets: [[2]]. To filter packets to the lab container IP: [[3]].
```

**Available choices / Variante disponibile: tcp.port == 12345  |  tcp.flags.syn == 1  |  ip.addr == 10.0.2.10  |  tcp port 12345  |  tcp.syn = true  |  dst 10.0.2.10**


> 💡 **Feedback:** Wireshark display filters use dot notation (tcp.port, tcp.flags.syn, ip.addr). Capture filters (BPF syntax like 'tcp port 12345') are different from display filters. [Filtrele de afișare Wireshark folosesc notația cu puncte (tcp.port, tcp.flags.syn, ip.addr). Filtrele de captură (sintaxă BPF precum „tcp port 12345") sunt diferite de filtrele de afișare.]

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

### 44. `Gap Select`
**N07.D10.Q02: Firewall Action Effects / Efectele acțiunilor de paravan**

> Match each firewall effect to its action: [Potriviți fiecare efect al paravanului cu acțiunea sa:]

```
Client experiences timeout: [[1]]. [Clientul experimentează timeout: ___.]
```

```
Client receives RST (TCP): [[2]]. [Clientul primește RST (TCP): ___.]
```

```
Packet passes through: [[3]]. [Pachetul trece prin: ___.]
```

**Available choices / Variante disponibile: DROP  |  REJECT  |  ACCEPT**


> 💡 **Feedback:** DROP = silence → timeout. REJECT = active refusal → RST (TCP) or ICMP (UDP). ACCEPT = packet is allowed through. [DROP = tăcere → timeout. REJECT = refuz activ → RST (TCP) sau ICMP (UDP). ACCEPT = pachetul trece.]

---

### 45. `Gap Select`
**N07.D10.Q03: Port Probe Results Mapping / Maparea rezultatelor sondării porturilor**

> Map each connect_ex() outcome to the port state: [Mapați fiecare rezultat connect_ex() la starea portului:]

```
Returns 0: port is [[1]]. [Returnează 0: portul este ___.]
```

```
Returns 111 (ECONNREFUSED): port is [[2]]. [Returnează 111 (ECONNREFUSED): portul este ___.]
```

```
Raises socket.timeout: port is [[3]]. [Ridică socket.timeout: portul este ___.]
```

**Available choices / Variante disponibile: open  |  closed  |  filtered**


> 💡 **Feedback:** 0 = connection succeeded (open). 111/ECONNREFUSED = RST received (closed, host reachable but no service). socket.timeout = no response within deadline (filtered by DROP rule). [0 = conexiune reușită (deschis). 111/ECONNREFUSED = RST primit (închis, gazdă accesibilă dar fără serviciu). socket.timeout = niciun răspuns în termenul limită (filtrat de regulă DROP).]

---

### 46. `Gap Select`
**N07.D10.Q07: Recommended Firewall Strategies / Strategii recomandate de paravan de protecție**

> Select the recommended firewall action for each scenario: [Selectați acțiunea de paravan recomandată pentru fiecare scenariu:]

```
External-facing services (minimise reconnaissance): [[1]]. [Servicii expuse extern (minimizare recunoaștere): ___.]
```

```
Internal debugging (fast error feedback): [[2]]. [Depanare internă (feedback rapid la erori): ___.]
```

```
Honeypot deception (mimic non-existent host): [[1]]. [Deceptare honeypot (imitare gazdă inexistentă): ___.]
```

**Available choices / Variante disponibile: DROP  |  REJECT**


> 💡 **Feedback:** External + honeypot = DROP (stealthy, no information leakage). Internal debugging = REJECT (immediate error response aids diagnosis). [Extern + honeypot = DROP (discret, fără scurgeri de informații). Depanare internă = REJECT (răspunsul imediat la erori ajută diagnosticarea).]

---
