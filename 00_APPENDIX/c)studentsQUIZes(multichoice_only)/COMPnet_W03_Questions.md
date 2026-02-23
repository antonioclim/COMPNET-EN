# Week 03 — Computer Networks
### *Rețele de Calculatoare — Săptămâna 3*

> UDP Sockets, TCP vs. UDP, Broadcasting, Threaded Servers • 49 questions • Bilingual EN/RO

---

## 📚 §1. Curs / Lecture (25 questions)

### Q1.

*[Multiple Choice]*

What additional information does the UDP method recvfrom() return compared to the TCP method recv() ? [Ce informație suplimentară returnează metoda UDP recvfrom() comparativ cu metoda TCP recv() ?]

- **a)** The sender's address tuple (IP, port) [Tuplul cu adresa expeditorului (IP, port)]
- **b)** The protocol version number [Numărul versiunii protocolului]
- **c)** The total number of bytes in the datagram [Numărul total de octeți din datagramă]
- **d)** A boolean indicating whether the datagram was corrupted [O valoare booleană indicând dacă datagrama a fost coruptă]

> 💡 **Feedback:**
> *recvfrom() returns a tuple of (data, (ip, port)), providing the sender's address. This is essential for UDP because there is no persistent connection — the server needs the sender's address to reply via sendto() . A common error is discarding the address tuple, making it impossible to respond to the client. [ recvfrom() returnează un tuplu de forma (date, (ip, port)), furnizând adresa expeditorului. Acest lucru este esențial pentru UDP deoarece nu există o conexiune persistentă — serverul are nevoie de adresa expeditorului pentru a răspunde prin sendto() . O eroare frecventă este ignorarea tuplului de adresă, ceea ce face imposibil răspunsul către client.]*


---

### Q2.

*[Multiple Choice]*

A student writes a TCP server that sends b"Hello" followed immediately by b"World" . The client calls recv(1024) once and sees b"HelloWorld" . The student concludes that TCP always concatenates consecutive sends into one recv(). Which statement best describes the flaw in this reasoning? [Un student scrie un server TCP care trimite b"Hello" urmat imediat de b"World" . Clientul apelează recv(1024) o dată și vede b"HelloWorld" . Studentul concluzionează că TCP concatenează întotdeauna trimiterile consecutive într-un singur recv(). Care afirmație descrie cel mai bine defectul în acest raționament?]

- **a)** TCP does not preserve message boundaries; the observed behaviour was coincidental due to localhost timing. [TCP nu păstrează delimitarea mesajelor; comportamentul observat a fost coincidență datorită temporizării pe localhost.]
- **b)** The student is correct — TCP always delivers concatenated data from consecutive sends. [Studentul are dreptate — TCP livrează întotdeauna date concatenate din trimiteri consecutive.]
- **c)** The behaviour occurs because the buffer size (1024) is larger than the combined message size. [Comportamentul apare deoarece dimensiunea bufferului (1024) este mai mare decât dimensiunea combinată a mesajelor.]
- **d)** TCP concatenates sends only when the server does not call flush() between them. [TCP concatenează trimiterile doar când serverul nu apelează flush() între ele.]

> 💡 **Feedback:**
> *TCP is a byte stream protocol — it makes no guarantees about how bytes from multiple send() calls will be grouped in recv() calls. The student observed one possible outcome on localhost, where low latency often causes data to coalesce in kernel buffers before the client reads. On a real network with varying latency, congestion, and Nagle's algorithm, the client might receive "Hello" and "World" separately, or partial reads like "Hel" and "loWorld". The correct approach is to implement application-level framing (length prefix or delimiter). [TCP este un protocol de tip flux de octeți — nu garantează modul în care octeții din multiple apeluri send() vor fi grupați în apelurile recv(). Studentul a observat un rezultat posibil pe localhost, unde latența scăzută determină adesea coalizarea datelor în bufferele nucleului înainte ca clientul să citească. Pe o rețea reală cu latență variabilă, congestie și algoritmul Nagle, clientul ar putea primi „Hello" și „World" separat, sau citiri parțiale ca „Hel" și „loWorld". Abordarea corectă este implementarea delimitării la nivel de aplicație (prefix de lungime sau delimitator).]*


---

### Q3.

*[Multiple Choice]*

A server receives 10 simultaneous connections, each requiring 100 ms of processing. An iterative server takes 1000 ms total. The student switches to a threaded server and observes \~100 ms total. Which statement most accurately explains the improvement? [Un server primește 10 conexiuni simultane, fiecare necesitând 100 ms de procesare. Un server iterativ durează 1000 ms în total. Studentul trece la un server cu fire de execuție și observă \~100 ms în total. Care afirmație explică cel mai precis îmbunătățirea?]

- **a)** Threads allow all 10 requests to be processed concurrently; total time equals roughly the duration of a single request rather than the sum of all requests. [Firele de execuție permit procesarea concurentă a tuturor celor 10 cereri; timpul total este aproximativ egal cu durata unei singure cereri, nu cu suma tuturor cererilor.]
- **b)** Threads make each individual request run 10× faster by distributing the computation across CPU cores. [Firele de execuție fac ca fiecare cerere individuală să ruleze de 10× mai rapid distribuind calculul pe nuclee CPU.]
- **c)** Threading reduces the network round-trip time between client and server, resulting in faster responses. [Firele de execuție reduc timpul de deplasare în rețea între client și server, rezultând răspunsuri mai rapide.]
- **d)** The threaded server uses UDP internally instead of TCP, eliminating handshake overhead for each client; this internal protocol switching is transparent to the client application and explains the consistently superior performance metrics observed. [Serverul cu fire de execuție folosește UDP intern în loc de TCP, eliminând overhead-ul handshake-ului pentru fiecare client.]

> 💡 **Feedback:**
> *The iterative server serialises request processing: each client waits for all previous clients to complete. With 10 clients at 100 ms each, client 10 finishes at 1000 ms. The threaded server creates a separate thread for each client, allowing all 10 to be processed in parallel — total time is approximately max(100 ms × 1) = 100 ms plus small thread creation overhead. This speedup comes specifically from concurrent execution. However, threading has limits: excessive threads consume memory, and Python's GIL limits CPU-bound parallelism. For very high concurrency, asynchronous I/O or thread pools become preferable. [Serverul iterativ serializează procesarea cererilor: fiecare client așteaptă completarea tuturor clienților anteriori. Cu 10 clienți la 100 ms fiecare, clientul 10 termină la 1000 ms. Serverul cu fire de execuție creează un fir separat pentru fiecare client, permițând procesarea tuturor 10 în paralel — timpul total este aproximativ max(100 ms × 1) = 100 ms plus un mic overhead de creare a firelor. Această accelerare provine specific din execuția concurentă. Totuși, firele de execuție au limite: prea multe fire consumă memorie, iar GIL-ul Python limitează paralelismul legat de procesor. Pentru concurență foarte mare, I/O asincron sau pool-uri de fire devin preferabile.]*


---

### Q4.

*[Multiple Choice]*

UDP is described as a "connectionless" protocol. A student interprets this to mean that a UDP socket can only send data, never receive it. Which statement most accurately corrects this interpretation? [UDP este descris ca un protocol „fără conexiune". Un student interpretează aceasta ca însemnând că un socket UDP poate doar trimite date, niciodată primi. Care afirmație corectează cel mai precis această interpretare?]

- **a)** "Connectionless" means no handshake is required before sending; the same UDP socket can both send and receive data using sendto() and recvfrom(). [„Fără conexiune" înseamnă că nu este necesar niciun handshake înainte de trimitere; același socket UDP poate trimite și primi date folosind sendto() și recvfrom().]
- **b)** The student is correct — UDP sockets can only send data; receiving requires a separate TCP socket. [Studentul are dreptate — socket-urile UDP pot doar trimite date; primirea necesită un socket TCP separat.]
- **c)** UDP sockets can receive data, but only after calling connect() to establish a virtual connection. [Socket-urile UDP pot primi date, dar doar după apelarea connect() pentru a stabili o conexiune virtuală.]
- **d)** "Connectionless" means UDP data is broadcast to all hosts on the network rather than sent to a specific destination; this broadcast behaviour requires no prior handshake because every device on the subnet receives every datagram automatically. [„Fără conexiune" înseamnă că datele UDP sunt difuzate către toate gazdele din rețea, nu trimise la o destinație specifică.]

> 💡 **Feedback:**
> *"Connectionless" means UDP requires no handshake or state establishment before data transfer — it does NOT mean communication is unidirectional. A single UDP socket can use sendto() and recvfrom() to both transmit and receive datagrams. recvfrom() even returns the sender's address, enabling the server to reply. Many bidirectional protocols (DNS, DHCP, NTP) operate over UDP. The misconception arises from confusing "no connection" with "no reply capability". [„Fără conexiune" înseamnă că UDP nu necesită handshake sau stabilirea stării înainte de transferul de date — NU înseamnă că comunicarea este unidirecțională. Un singur socket UDP poate folosi sendto() și recvfrom() pentru a transmite și primi datagrame. recvfrom() returnează chiar adresa expeditorului, permițând serverului să răspundă. Multe protocoale bidirecționale (DNS, DHCP, NTP) funcționează peste UDP. Concepția greșită apare din confundarea „fără conexiune" cu „fără capacitate de răspuns".]*


---

### Q5.

*[Multiple Choice]*

Which IPv4 address represents a limited broadcast that routers are guaranteed never to forward? [Care adresă IPv4 reprezintă un broadcast limitat pe care ruterele nu îl redirecționează niciodată?]

- **a)** 255.255.255.255 — never forwarded beyond the local segment [255.255.255.255 — nu este redirecționat dincolo de segmentul local]
- **b)** 172.20.0.255 — directed broadcast for the 172.20.0.0/24 subnet [172.20.0.255 — broadcast direcționat pentru subrețeaua 172.20.0.0/24]
- **c)** 224.0.0.1 — reserved multicast address for all hosts on segment [224.0.0.1 — adresă multicast rezervată pentru toate gazdele din segment]
- **d)** 0.0.0.0 — unspecified address used during interface initialisation [0.0.0.0 — adresă nespecificată folosită la inițializarea interfeței]

> 💡 **Feedback:**
> *The address 255.255.255.255 is the limited broadcast, confined to the local Layer 2 domain. Directed broadcasts (e.g. 172.20.0.255) target a specific subnet but are typically blocked by modern routers. The address 224.0.0.1 belongs to the multicast range, not broadcast. [Adresa 255.255.255.255 este broadcast-ul limitat, confinat la domeniul local de Nivel 2. Broadcast-urile direcționate (ex. 172.20.0.255) vizează o subrețea specifică, dar sunt de obicei blocate de ruterele moderne. Adresa 224.0.0.1 aparține intervalului multicast, nu broadcast.]*


---

### Q6.

*[Multiple Choice]*

IPv4 multicast communication uses Class D addresses. What is the correct range for this address class? [Comunicarea multicast IPv4 folosește adrese din Clasa D. Care este intervalul corect pentru această clasă de adrese?]

- **a)** 224.0.0.0 through 239.255.255.255 [224.0.0.0 până la 239.255.255.255]
- **b)** 240.0.0.0 through 255.255.255.254 [240.0.0.0 până la 255.255.255.254]
- **c)** 192.0.0.0 through 223.255.255.255 [192.0.0.0 până la 223.255.255.255]
- **d)** 169.254.0.0 through 169.254.255.255 [169.254.0.0 până la 169.254.255.255]

> 💡 **Feedback:**
> *Class D spans 224.0.0.0 to 239.255.255.255. The sub-range 239.0.0.0/8 is administratively scoped for private use, analogous to 10.0.0.0/8 for unicast. Class E (240.0.0.0--255.255.255.254) is reserved for experimental purposes and cannot carry multicast. [Clasa D acoperă intervalul 224.0.0.0 până la 239.255.255.255. Sub-intervalul 239.0.0.0/8 este delimitat administrativ pentru utilizare privată, similar cu 10.0.0.0/8 pentru unicast. Clasa E (240.0.0.0--255.255.255.254) este rezervată pentru scopuri experimentale și nu poate transporta multicast.]*


---

### Q7.

*[True / False]*

TCP connections can use broadcast addressing to reach all hosts on a local segment simultaneously. [Conexiunile TCP pot folosi adresarea broadcast pentru a ajunge la toate gazdele dintr-un segment local simultan.]

- **a)** true
- **b)** false

> 💡 **Feedback:**
> *Broadcast operates exclusively with UDP (connectionless datagrams). TCP requires a dedicated connection between two endpoints and cannot establish sessions with "all hosts" — there is no TCP broadcast. [Broadcast-ul funcționează exclusiv cu UDP (datagrame fără conexiune). TCP necesită o conexiune dedicată între două puncte terminale și nu poate stabili sesiuni cu "toate gazdele" — nu există TCP broadcast.]*


---

### Q8.

*[Multiple Choice]*

A host sends a UDP datagram to 255.255.255.255 on port 5007. At which OSI layer is this traffic guaranteed to be stopped from propagating further? [O gazdă trimite o datagramă UDP la 255.255.255.255 pe portul 5007. La care nivel OSI este garantat că acest trafic va fi oprit din a se propaga mai departe?]

- **a)** Layer 3 — routers discard limited broadcast packets at the network boundary [Nivelul 3 — ruterele elimină pachetele de broadcast limitat la granița rețelei]
- **b)** Layer 2 — switches filter broadcast frames before they reach any other port [Nivelul 2 — comutatoarele filtrează cadrele broadcast înainte de a ajunge la alt port]
- **c)** Layer 4 — the transport protocol rejects broadcast-addressed segments [Nivelul 4 — protocolul de transport respinge segmentele adresate broadcast]
- **d)** Layer 1 — physical repeaters attenuate broadcast signals at segment boundaries [Nivelul 1 — repetoarele fizice atenuează semnalele broadcast la granițele segmentelor]

> 💡 **Feedback:**
> *Routers operate at Layer 3 (Network) and are responsible for dropping limited broadcast packets. Switches at Layer 2 flood broadcast frames to all ports within the same VLAN. The constraint is enforced at the boundary between L2 and L3: the router's network-layer processing discards 255.255.255.255. [Ruterele operează la Nivelul 3 (Rețea) și sunt responsabile pentru eliminarea pachetelor de broadcast limitat. Comutatoarele de la Nivelul 2 inundă cadrele broadcast pe toate porturile din același VLAN. Constrângerea este impusă la granița dintre L2 și L3: prelucrarea la nivelul rețea a ruterului elimină 255.255.255.255.]*


---

### Q9.

*[Multiple Choice]*

A multicast sender sets IP_MULTICAST_TTL to 1 using setsockopt() . A receiver that has joined the same group sits behind one router hop. Will the receiver get the packet? [Un expeditor multicast setează IP_MULTICAST_TTL la 1 folosind setsockopt() . Un receptor care s-a alăturat aceluiași grup se află în spatele unui salt de ruter. Va primi receptorul pachetul?]

- **a)** No — TTL=1 confines the packet to the local link; the router decrements it to 0 and discards [Nu — TTL=1 confinează pachetul la legătura locală; ruterul îl decrementează la 0 și îl elimină]
- **b)** Yes — IGMP group membership guarantees delivery regardless of the TTL value set by the sender [Da — apartenența la grupul IGMP garantează livrarea indiferent de valoarea TTL setată de expeditor]
- **c)** Yes — TTL=1 means the packet persists for one second which is ample time for one hop [Da — TTL=1 înseamnă că pachetul persistă o secundă, suficient pentru un salt]

> 💡 **Feedback:**
> *With TTL=1, the packet remains link-local and cannot cross any router. The router would decrement TTL to 0 and discard the packet. To reach a receiver one hop away, the sender needs TTL of at least 2. [Cu TTL=1, pachetul rămâne local pe legătură și nu poate traversa niciun ruter. Ruterul ar decrementa TTL la 0 și ar elimina pachetul. Pentru a ajunge la un receptor aflat la un salt distanță, expeditorul are nevoie de TTL de cel puțin 2.]*


---

### Q10.

*[True / False]*

Unlike broadcast, multicast traffic can traverse routers when multicast routing protocols (such as PIM) and IGMP are properly configured. [Spre deosebire de broadcast, traficul multicast poate traversa rutere atunci când protocoalele de rutare multicast (precum PIM) și IGMP sunt configurate corespunzător.]

- **a)** true
- **b)** false

> 💡 **Feedback:**
> *This is a critical distinction: broadcast is always confined to the L2 domain, whereas multicast can be forwarded by routers that support IGMP and a multicast routing protocol. The TTL field controls how far multicast packets may travel. [Aceasta este o distincție critică: broadcast-ul este întotdeauna confinat la domeniul L2, în timp ce multicast-ul poate fi redirecționat de rutere care suportă IGMP și un protocol de rutare multicast. Câmpul TTL controlează cât de departe pot călători pachetele multicast.]*


---

### Q11.

*[Multiple Choice]*

What is the primary function of IGMP (Internet Group Management Protocol) in multicast communication? [Care este funcția principală a IGMP (Internet Group Management Protocol) în comunicarea multicast?]

- **a)** Hosts use IGMP to report multicast group membership to their local router [Gazdele folosesc IGMP pentru a raporta apartenența la grupul multicast ruterului lor local]
- **b)** IGMP encrypts multicast packets to prevent unauthorised receivers from reading data [IGMP criptează pachetele multicast pentru a preveni citirea datelor de receptori neautorizați]
- **c)** IGMP assigns unique multicast addresses to applications that request group creation [IGMP atribuie adrese multicast unice aplicațiilor care solicită crearea de grupuri]
- **d)** IGMP routes multicast packets between autonomous systems across the public internet [IGMP rutează pachetele multicast între sisteme autonome pe internet-ul public]

> 💡 **Feedback:**
> *IGMP enables hosts to signal their interest in receiving traffic for specific multicast groups to local routers. Without IGMP Membership Reports, routers have no way to know which interfaces need multicast traffic, so they cannot forward it. IGMP does not encrypt traffic, manage addresses, or handle routing between routers. [IGMP permite gazdelor să semnaleze interesul lor de a primi trafic pentru grupuri multicast specifice către ruterele locale. Fără rapoartele de apartenență IGMP, ruterele nu au cum să știe care interfețe au nevoie de trafic multicast, deci nu îl pot redirecționa. IGMP nu criptează traficul, nu gestionează adresele și nu se ocupă de rutarea între rutere.]*


---

### Q12.

*[Multiple Choice]*

In the Week 3 Python exercises, what socket-level operation triggers the host's kernel to send an IGMP Membership Report? [În exercițiile Python din Săptămâna 3, ce operațiune la nivel de socket determină nucleul gazdei să trimită un raport de apartenență IGMP?]

- **a)** setsockopt(IPPROTO_IP, IP_ADD_MEMBERSHIP, mreq) — joining the multicast group [ setsockopt(IPPROTO_IP, IP_ADD_MEMBERSHIP, mreq) — alăturarea la grupul multicast]
- **b)** bind(('', 5001)) — binding the socket to the multicast reception port [ bind(('', 5001)) — legarea socket-ului la portul de recepție multicast]
- **c)** setsockopt(SOL_SOCKET, SO_BROADCAST, 1) — enabling broadcast transmission mode [ setsockopt(SOL_SOCKET, SO_BROADCAST, 1) — activarea modului de transmisie broadcast]
- **d)** recvfrom(1024) — the act of receiving the first multicast datagram [ recvfrom(1024) — actul de a primi prima datagramă multicast]

> 💡 **Feedback:**
> *Calling setsockopt() with IP_ADD_MEMBERSHIP instructs the kernel to join the specified multicast group, which generates an IGMP Membership Report. Simply binding to a port (bind()) or enabling broadcast (SO_BROADCAST) does not trigger IGMP. [Apelarea setsockopt() cu IP_ADD_MEMBERSHIP instruiește nucleul să se alăture grupului multicast specificat, ceea ce generează un raport de apartenență IGMP. Simpla legare la un port (bind()) sau activarea broadcast-ului (SO_BROADCAST) nu declanșează IGMP.]*


---

### Q13.

*[True / False]*

For a UDP socket to receive multicast traffic, it is sufficient to call bind(('', port)) on the correct port; no additional socket options are required. [Pentru ca un socket UDP să primească trafic multicast, este suficient să se apeleze bind(('', port)) pe portul corect; nu sunt necesare opțiuni suplimentare de socket.]

- **a)** true
- **b)** false

> 💡 **Feedback:**
> *Binding alone is insufficient for multicast reception. The socket must also call setsockopt() with IP_ADD_MEMBERSHIP to join the group. Without this call, the kernel simply ignores incoming multicast packets even if the port matches. This is the most common student error in the Week 3 exercises. [Legarea singură nu este suficientă pentru recepția multicast. Socket-ul trebuie să apeleze și setsockopt() cu IP_ADD_MEMBERSHIP pentru a se alătura grupului. Fără acest apel, nucleul pur și simplu ignoră pachetele multicast primite chiar dacă portul se potrivește. Aceasta este cea mai frecventă eroare a studenților în exercițiile din Săptămâna 3.]*


---

### Q14.

*[Multiple Choice]*

A router sends periodic IGMP Membership Queries to its connected subnets. What is the purpose of these queries? [Un ruter trimite periodic interogări de apartenență IGMP către subrețelele conectate. Care este scopul acestor interogări?]

- **a)** To determine whether any hosts still require traffic for each multicast group on the subnet [Pentru a determina dacă vreo gazdă mai necesită trafic pentru fiecare grup multicast din subrețea]
- **b)** To force all hosts to leave their current multicast groups and re-register from scratch [Pentru a forța toate gazdele să părăsească grupurile multicast curente și să se reînregistreze de la zero]
- **c)** To authenticate each host before granting permission to continue receiving group data [Pentru a autentifica fiecare gazdă înainte de a acorda permisiunea de a continua să primească date de grup]

> 💡 **Feedback:**
> *Membership Queries allow routers to discover which multicast groups still have active members. Hosts that remain interested respond with Membership Reports. If no host responds for a group, the router eventually stops forwarding that group's traffic to the subnet, conserving bandwidth. [Interogările de apartenență permit ruterelor să descopere care grupuri multicast au încă membri activi. Gazdele care rămân interesate răspund cu rapoarte de apartenență. Dacă nicio gazdă nu răspunde pentru un grup, ruterul oprește în cele din urmă redirecționarea traficului acelui grup către subrețea, economisind lățime de bandă.]*


---

### Q15.

*[Multiple Choice]*

A university needs to stream a live lecture to 10,000 students across 5 routed subnets. Why is broadcast inadequate for this scenario? [O universitate trebuie să transmită o prelegere în direct către 10.000 de studenți pe 5 subrețele rutate. De ce broadcast-ul este inadecvat pentru acest scenariu?]

- **a)** Broadcast cannot cross router boundaries; it reaches only the local L2 segment where the source resides [Broadcast-ul nu poate traversa granițele ruterelor; ajunge doar la segmentul L2 local unde se află sursa]
- **b)** Broadcast requires TCP connections and cannot handle 10,000 simultaneous streams [Broadcast-ul necesită conexiuni TCP și nu poate gestiona 10.000 de fluxuri simultane]
- **c)** Broadcast has a maximum payload of 512 bytes, insufficient for streaming video content in this case [Broadcast-ul are o sarcină utilă maximă de 512 octeți, insuficientă pentru conținut video în flux în acest caz]

> 💡 **Feedback:**
> *Broadcast is confined to a single Layer 2 domain and cannot cross routers. With 5 separate subnets, broadcast from one subnet would never reach the other four. IP multicast is the correct choice here — it traverses routers via IGMP and multicast routing while sending only a single stream from the source. [Broadcast-ul este confinat la un singur domeniu de Nivel 2 și nu poate traversa rutere. Cu 5 subrețele separate, broadcast-ul dintr-o subrețea nu ar ajunge niciodată la celelalte patru. Multicast-ul IP este alegerea corectă aici — traversează ruterele prin IGMP și rutare multicast, trimițând doar un singur flux de la sursă.]*


---

### Q16.

*[Multiple Choice]*

An online gaming company wants 100 players across the public internet to receive game state updates. Can the company rely on IP multicast for this delivery? [O companie de jocuri online dorește ca 100 de jucători de pe internet-ul public să primească actualizări ale stării jocului. Poate compania să se bazeze pe multicast IP pentru această livrare?]

- **a)** No — multicast is not widely deployed on the public internet; most ISPs do not forward multicast between networks [Nu — multicast-ul nu este implementat pe scară largă pe internet-ul public; majoritatea ISP-urilor nu redirecționează multicast între rețele]
- **b)** Yes — multicast natively works across all internet-connected networks provided the TTL is high enough under default settings [Da — multicast-ul funcționează nativ pe toate rețelele conectate la internet dacă TTL-ul este suficient de mare cu setările implicite]
- **c)** Yes — the Source-Specific Multicast (SSM) range 232.0.0.0/8 is guaranteed to work globally [Da — intervalul Source-Specific Multicast (SSM) 232.0.0.0/8 este garantat să funcționeze global]

> 💡 **Feedback:**
> *IP multicast is generally not deployed across the public internet. Most ISP routers do not support multicast routing between autonomous systems. The gaming company must use unicast (individual connections) or application-layer solutions such as CDN-based distribution or server-side fan-out. [Multicast-ul IP nu este în general implementat pe internet-ul public. Majoritatea ruterelor ISP nu suportă rutarea multicast între sisteme autonome. Compania de jocuri trebuie să folosească unicast (conexiuni individuale) sau soluții la nivelul aplicației, precum distribuția bazată pe CDN sau fan-out la nivel de server.]*


---

### Q17.

*[Multiple Choice]*

An IoT sensor network requires 99.9% message delivery reliability across routed segments. Why is UDP multicast alone insufficient for this requirement? [O rețea de senzori IoT necesită fiabilitate de livrare a mesajelor de 99,9% pe segmente rutate. De ce multicast-ul UDP singur este insuficient pentru această cerință?]

- **a)** UDP provides no acknowledgements, retransmission, or delivery guarantees — packets may be silently lost [UDP nu oferă confirmări, retransmisie sau garanții de livrare — pachetele pot fi pierdute silențios]
- **b)** Multicast addresses are limited to 256 simultaneous groups which is insufficient for IoT scale in practice [Adresele multicast sunt limitate la 256 de grupuri simultane, ceea ce este insuficient pentru scala IoT în practică]
- **c)** IGMP introduces 500ms latency per router hop which violates real-time sensor requirements (default) [IGMP introduce o latență de 500ms per salt de ruter, ceea ce încalcă cerințele senzorilor în timp real (implicit)]

> 💡 **Feedback:**
> *UDP provides no delivery guarantee — packets may be lost, duplicated, or reordered without notification. Multicast only optimises distribution; it does not add reliability. For 99.9% delivery, the architecture needs application-layer acknowledgements, as provided by protocols like MQTT with QoS 1 (at-least-once delivery). [UDP nu oferă garanție de livrare — pachetele pot fi pierdute, duplicate sau reordonate fără notificare. Multicast-ul optimizează doar distribuția; nu adaugă fiabilitate. Pentru livrare de 99,9%, arhitectura necesită confirmări la nivelul aplicației, așa cum oferă protocoale precum MQTT cu QoS 1 (livrare cel-puțin-o-dată).]*


---

### Q18.

*[Multiple Choice]*

From a security perspective, what inherent risk does broadcast communication pose within a local network? [Din perspectiva securității, ce risc inerent prezintă comunicarea broadcast în cadrul unei rețele locale?]

- **a)** All hosts on the segment receive the data regardless of interest, enabling passive eavesdropping by any listener [Toate gazdele din segment primesc datele indiferent de interes, permițând interceptarea pasivă de către orice ascultător]
- **b)** Broadcast packets are automatically encrypted at Layer 2 but the encryption keys may be compromised as per standard [Pachetele broadcast sunt criptate automat la Nivelul 2, dar cheile de criptare pot fi compromise conform standardului]
- **c)** Broadcast generates excessive IGMP traffic that overwhelms routers and causes denial of service [Broadcast-ul generează trafic IGMP excesiv care copleșește ruterele și provoacă refuzul serviciului]

> 💡 **Feedback:**
> *Broadcast frames are delivered to every host on the segment, meaning any device can capture and read the data — there is no access control or selectivity. This makes broadcast unsuitable for transmitting sensitive information without encryption. The Smurf amplification attack historically exploited broadcast for ICMP flood amplification. [Cadrele broadcast sunt livrate la fiecare gazdă din segment, ceea ce înseamnă că orice dispozitiv poate captura și citi datele — nu există control al accesului sau selectivitate. Aceasta face broadcast-ul nepotrivit pentru transmiterea informațiilor sensibile fără criptare. Atacul de amplificare Smurf a exploitat istoric broadcast-ul pentru amplificarea inundării ICMP.]*


---

### Q19.

*[Multiple Choice]*

A student writes a multicast receiver that binds to port 5001, sets SO_REUSEADDR, but forgets to call IP_ADD_MEMBERSHIP. The sender transmits to 224.0.0.1:5001. What is the observable result on the receiver? [Un student scrie un receptor multicast care se leagă la portul 5001, setează SO_REUSEADDR, dar uită să apeleze IP_ADD_MEMBERSHIP. Expeditorul transmite la 224.0.0.1:5001. Care este rezultatul observabil pe receptor?]

- **a)** The bind succeeds but recvfrom() blocks indefinitely — multicast packets are silently ignored without group membership [Legarea reușește dar recvfrom() blochează indefinit — pachetele multicast sunt ignorate silențios fără apartenență la grup]
- **b)** The kernel raises an OSError at bind time because the socket cannot listen on a multicast port without group join in practice [Nucleul ridică o eroare OSError la momentul legării deoarece socket-ul nu poate asculta pe un port multicast fără aderare în practică]
- **c)** The receiver gets all multicast traffic on the subnet automatically because binding to the port is sufficient (default) [Receptorul primește automat tot traficul multicast din subrețea deoarece legarea la port este suficientă (implicit)]

> 💡 **Feedback:**
> *Without IP_ADD_MEMBERSHIP, the kernel does not subscribe to the multicast group via IGMP. The NIC and kernel silently discard incoming multicast packets for groups not joined. Binding to the port is necessary but not sufficient — it only determines which local port to listen on, not which multicast groups to receive. [Fără IP_ADD_MEMBERSHIP, nucleul nu se abonează la grupul multicast prin IGMP. Placa de rețea și nucleul descarcă silențios pachetele multicast primite pentru grupuri la care nu s-a aderat. Legarea la port este necesară dar nu suficientă — determină doar pe ce port local să asculte, nu ce grupuri multicast să primească.]*


---

### Q20.

*[Multiple Choice]*

A Python script creates a UDP socket and immediately calls sock.sendto(b"test", ("255.255.255.255", 5007)) without setting SO_BROADCAST. What exception type does the operating system raise? [Un script Python creează un socket UDP și apelează imediat sock.sendto(b"test", ("255.255.255.255", 5007)) fără a seta SO_BROADCAST. Ce tip de excepție ridică sistemul de operare?]

- **a)** OSError or PermissionError — the kernel requires explicit SO_BROADCAST permission and refuses the send [OSError sau PermissionError — nucleul necesită permisiune SO_BROADCAST explicită și refuză trimiterea]
- **b)** socket.timeout — the packet is sent but no acknowledgement returns, causing a configurable timeout [socket.timeout — pachetul este trimis dar nu se returnează confirmarea, cauzând un timeout configurabil]
- **c)** ConnectionRefusedError — the broadcast address actively refuses connections from sockets without the flag set [ConnectionRefusedError — adresa broadcast refuză activ conexiunile de la socket-uri fără flag-ul setat]
- **d)** No exception — the send succeeds silently but the datagram is dropped before reaching the network interface [Nicio excepție — trimiterea reușește silențios dar datagrama este descărcată înainte de a ajunge la interfața de rețea]

> 💡 **Feedback:**
> *The kernel treats SO_BROADCAST as a mandatory permission flag, not a hint. Without it, sendto() to a broadcast address raises OSError (errno 101: Network is unreachable) or PermissionError. This is a deliberate safety mechanism — not a timeout, not a warning, not a DNS failure. [Nucleul tratează SO_BROADCAST ca un flag obligatoriu de permisiune, nu un indiciu. Fără acesta, sendto() la o adresă broadcast ridică OSError (errno 101: Rețeaua nu este accesibilă) sau PermissionError. Acesta este un mecanism de siguranță deliberat — nu timeout, nu avertisment, nu eșec DNS.]*


---

### Q21.

*[Multiple Choice]*

The multicast join call requires an mreq structure constructed as: mreq = socket.inet_aton("224.0.0.1") + struct.pack('=I', socket.INADDR_ANY) What does this 8-byte structure contain, and why are both components necessary? [Apelul de aderare la multicast necesită o structură mreq . Ce conține această structură de 8 octeți și de ce sunt necesare ambele componente?]

- **a)** 4 bytes for the multicast group IP (which group to join) + 4 bytes for the local interface IP (INADDR_ANY = kernel chooses interface) [4 octeți pentru IP-ul grupului multicast (la ce grup să adere) + 4 octeți pentru IP-ul interfeței locale (INADDR_ANY = nucleul alege interfața)]
- **b)** 4 bytes for the sender's IP address (to filter traffic by source) + 4 bytes for the TTL value encoded as a 32-bit integer in practice [4 octeți pentru adresa IP a expeditorului (pentru filtrarea traficului după sursă) + 4 octeți pentru valoarea TTL codificată ca întreg pe 32 biți în practică]
- **c)** 4 bytes for the multicast port number in network byte order + 4 bytes for the protocol identifier (IGMP version code) (default) [4 octeți pentru numărul portului multicast în ordinea octeților rețelei + 4 octeți pentru identificatorul de protocol (codul versiunii IGMP) (implicit)]

> 💡 **Feedback:**
> *The mreq structure is an ip_mreq with two 4-byte fields: the multicast group IP address (which group to join) and the local interface address (which NIC to join on). INADDR_ANY means the kernel selects the default interface. Both are needed because a multi-homed host might want to join the group on a specific interface only. [Structura mreq este un ip_mreq cu două câmpuri de 4 octeți: adresa IP a grupului multicast (la ce grup să adere) și adresa interfeței locale (pe ce NIC să adere). INADDR_ANY înseamnă că nucleul selectează interfața implicită. Ambele sunt necesare deoarece o gazdă cu mai multe interfețe ar putea dori să adere la grup doar pe o interfață specifică.]*


---

### Q22.

*[Multiple Choice]*

In the Week 3 lab, the TCP tunnel on the router listens on port 12345 and forwards to server:8080. When a single client connects through the tunnel, how many TCP connections exist simultaneously? [În laboratorul din Săptămâna 3, tunelul TCP de pe ruter ascultă pe portul 12345 și redirecționează către server:8080. Când un singur client se conectează prin tunel, câte conexiuni TCP există simultan?]

- **a)** Two — one from client to router:12345 and a separate one from router to server:8080 [Două — una de la client la router:12345 și una separată de la router la server:8080]
- **b)** One — the tunnel transparently extends the client's connection directly to the server in practice [Una — tunelul extinde transparent conexiunea clientului direct către server în practică]
- **c)** Three — client to router, an internal routing connection, then router to server [Trei — client la ruter, o conexiune internă de rutare, apoi ruter la server]
- **d)** Zero — TCP tunnels encapsulate data within UDP datagrams for lower overhead [Zero — tunelele TCP încapsulează datele în datagrame UDP pentru un cost mai redus]

> 💡 **Feedback:**
> *A TCP tunnel terminates the incoming connection and creates a new outbound connection. This produces two distinct TCP sessions: client↔router:12345 and router↔server:8080. The tunnel is NOT transparent — the server sees the router's IP as the source, not the client's. Running ss -tn on the router reveals both ESTABLISHED connections. [Un tunel TCP termină conexiunea primită și creează o nouă conexiune de ieșire. Aceasta produce două sesiuni TCP distincte: client↔router:12345 și router↔server:8080. Tunelul NU este transparent — serverul vede IP-ul ruterului ca sursă, nu al clientului. Executarea ss -tn pe ruter dezvăluie ambele conexiuni ESTABLISHED.]*


---

### Q23.

*[Multiple Choice]*

The TCP tunnel in the Week 3 lab uses two threads per connection. Why is a single-threaded relay insufficient for full-duplex forwarding? [Tunelul TCP din laboratorul Săptămâna 3 folosește două fire de execuție per conexiune. De ce un releu cu un singur fir de execuție este insuficient pentru redirecționarea full-duplex?]

- **a)** A blocking recv() on one direction would prevent the thread from forwarding data in the opposite direction [Un recv() blocant pe o direcție ar împiedica firul de execuție să redirecționeze date în direcția opusă]
- **b)** TCP requires separate threads for sending and receiving on the same socket object [TCP necesită fire de execuție separate pentru trimitere și recepție pe același obiect socket]
- **c)** Operating systems enforce a one-thread-per-socket limit for all network connections (default) [Sistemele de operare impun o limită de un fir de execuție per socket pentru toate conexiunile de rețea (implicit)]
- **d)** Multiple threads are required to handle the three-way handshake on both tunnel sockets in practice [Fire de execuție multiple sunt necesare pentru a gestiona handshake-ul triplu pe ambele socket-uri ale tunelului în practică]

> 💡 **Feedback:**
> *A recv() call blocks until data arrives. A single thread handling client→server direction would be stuck waiting on recv() and unable to simultaneously forward server→client data. Two threads (one per direction) ensure that data flows concurrently in both directions without blocking. [Un apel recv() blochează până când ajung date. Un singur fir de execuție care gestionează direcția client→server ar fi blocat așteptând recv() și incapabil să redirecționeze simultan datele server→client. Două fire de execuție (unul per direcție) asigură că datele curg concomitent în ambele direcții fără blocare.]*


---

### Q24.

*[Multiple Choice]*

The tunnel relay function uses sendall(data) rather than send(data) . What problem does sendall() solve that send() does not? [Funcția releu a tunelului folosește sendall(data) în loc de send(data) . Ce problemă rezolvă sendall() pe care send() nu o rezolvă?]

- **a)** send() may perform a partial write, transmitting fewer bytes than provided; sendall() guarantees the complete buffer is sent [send() poate efectua o scriere parțială, transmițând mai puțini octeți decât s-a furnizat; sendall() garantează trimiterea completă a bufferului]
- **b)** send() can only transmit strings, while sendall() also accepts bytes objects and memoryview buffers across all supported platforms [send() poate transmite doar șiruri de caractere, în timp ce sendall() acceptă și obiecte bytes și buffere memoryview pe toate platformele suportate]
- **c)** send() uses UDP internally for performance, whereas sendall() maintains proper TCP semantics [send() folosește intern UDP pentru performanță, în timp ce sendall() menține semantica TCP corespunzătoare]

> 💡 **Feedback:**
> *The send() method may transmit fewer bytes than requested (partial send), returning the count actually sent. If the relay ignores this, data is silently lost. sendall() loops internally until all bytes are transmitted, guaranteeing complete delivery. [Metoda send() poate transmite mai puțini octeți decât s-a solicitat (trimitere parțială), returnând numărul efectiv trimis. Dacă releul ignoră acest lucru, datele se pierd silențios. sendall() iterează intern până când toți octeții sunt transmiși, garantând livrarea completă.]*


---

### Q25.

*[Multiple Choice]*

In the tunnel relay function, the condition if not data (after data = src.recv(4096) ) triggers connection cleanup. What does an empty bytes return from recv() indicate? [În funcția releu a tunelului, condiția if not data (după data = src.recv(4096) ) declanșează curățarea conexiunii. Ce indică o returnare de octeți goi din recv() ?]

- **a)** The remote peer performed a graceful close by sending a FIN; no further data will arrive [Corespondentul distant a efectuat o închidere grațioasă prin trimiterea unui FIN; nu vor mai sosi date]
- **b)** The socket's receive buffer is temporarily empty and the caller should retry after a delay [Bufferul de recepție al socket-ului este temporar gol și apelantul ar trebui să reîncerce după o întârziere]
- **c)** The network connection was lost due to a timeout, causing the socket to discard pending data [Conexiunea de rețea a fost pierdută din cauza unui timeout, determinând socket-ul să renunțe la datele în așteptare]
- **d)** The recv() buffer size of 4096 was too small to hold the incoming packet which was dropped [Dimensiunea bufferului recv() de 4096 a fost prea mică pentru pachetul primit, care a fost eliminat]

> 💡 **Feedback:**
> *In TCP, recv() returning b'' (empty bytes) means the remote peer has closed their sending half of the connection (sent a FIN segment). This is the graceful shutdown signal — no more data will arrive. It does not indicate a timeout or error. [În TCP, recv() care returnează b'' (octeți goi) înseamnă că corespondentul distant și-a închis jumătatea de trimitere a conexiunii (a trimis un segment FIN). Acesta este semnalul de închidere grațioasă — nu vor mai sosi date. Nu indică un timeout sau o eroare.]*

---

## 🔬 §2. Laborator / Lab (15 questions)


---

### Q26.

*[Multiple Choice]*

A UDP client calls sendto(b"ping", ("127.0.0.1", 9300)) but the server is not running. What happens? [Un client UDP apelează sendto(b"ping", ("127.0.0.1", 9300)) dar serverul nu rulează. Ce se întâmplă?]

- **a)** sendto() succeeds silently; the subsequent recvfrom() times out waiting for a reply [sendto() reușește silențios; recvfrom() ulterior expiră așteptând un răspuns]
- **b)** sendto() raises a ConnectionRefusedError immediately [sendto() ridică imediat o eroare ConnectionRefusedError]
- **c)** sendto() blocks until the server becomes available [sendto() se blochează până când serverul devine disponibil]
- **d)** The OS automatically retransmits the datagram until it is delivered [Sistemul de operare retransmite automat datagrama până la livrare, asigurând fiabilitate completă la nivelul stratului de transport]

> 💡 **Feedback:**
> *sendto() succeeds because UDP is connectionless — it simply dispatches the datagram without verifying the receiver. The subsequent recvfrom() will time out since no server is present to send a response. This contrasts with TCP, where connect() to a non-listening port raises ConnectionRefusedError immediately. A common misconception is expecting UDP to report delivery failure at send time. [ sendto() reușește deoarece UDP este fără conexiune — pur și simplu expediază datagrama fără a verifica receptorul. Apelul recvfrom() ulterior va expira deoarece nu există niciun server care să trimită un răspuns. Aceasta contrastează cu TCP, unde connect() către un port care nu ascultă ridică imediat ConnectionRefusedError . O concepție greșită frecventă este așteptarea ca UDP să raporteze eșecul livrării la momentul trimiterii.]*


---

### Q27.

*[Multiple Choice]*

A TCP server executes conn.send(b"Hello") immediately followed by conn.send(b"World") . The client then calls data = sock.recv(1024) . What will the client's data variable contain? [Un server TCP execută conn.send(b"Hello") urmat imediat de conn.send(b"World") . Clientul apelează apoi data = sock.recv(1024) . Ce va conține variabila data a clientului?]

- **a)** It could be b"Hello" , b"HelloWorld" , or any other byte split — the result is non-deterministic [Ar putea fi b"Hello" , b"HelloWorld" sau orice altă împărțire a octeților — rezultatul este nedeterminist]
- **b)** Always b"Hello" — TCP delivers messages one at a time [Întotdeauna b"Hello" — TCP livrează mesajele pe rând]
- **c)** Always b"HelloWorld" — TCP always concatenates sequential sends [Întotdeauna b"HelloWorld" — TCP concatenează întotdeauna trimiterile secvențiale și le livrează ca un bloc unic de octeți aplicației receptoare]
- **d)** An error — you cannot call send() twice without a recv() in between [O eroare — nu puteți apela send() de două ori fără un recv() între ele]

> 💡 **Feedback:**
> *Because TCP is a byte stream, the result is non-deterministic. The client could receive b"HelloWorld" , b"Hello" , or other splits depending on OS buffering and network timing. This is the message boundary problem (Misconception #1). On localhost, small messages often arrive merged due to Nagle's algorithm and minimal latency, but this behaviour is never guaranteed. [Deoarece TCP este un flux de octeți, rezultatul este nedeterminist. Clientul ar putea primi b"HelloWorld" , b"Hello" sau alte împărțiri în funcție de tamponarea sistemului de operare și temporizarea rețelei. Aceasta este problema delimitării mesajelor (Concepția greșită nr. 1). Pe localhost, mesajele mici ajung adesea unite datorită algoritmului Nagle și latenței minime, dar acest comportament nu este niciodată garantat.]*


---

### Q28.

*[Multiple Choice]*

A threaded TCP server spawns three threads (for clients 0, 1, 2) at roughly the same time. Each thread sleeps 100 ms and then appends its client ID to a shared list. After all threads complete, what does the results list contain? [Un server TCP cu fire de execuție lansează trei fire (pentru clienții 0, 1, 2) aproximativ în același timp. Fiecare fir doarme 100 ms și apoi adaugă ID-ul clientului într-o listă partajată. După finalizarea tuturor firelor, ce conține lista de rezultate?]

- **a)** Any permutation of [0, 1, 2] — thread scheduling is non-deterministic [Orice permutare a [0, 1, 2] — planificarea firelor este nedeterministă]
- **b)** Always [0, 1, 2] — threads execute in creation order [Întotdeauna [0, 1, 2] — firele se execută în ordinea creării]
- **c)** Always [2, 1, 0] — last created thread runs first [Întotdeauna [2, 1, 0] — ultimul fir creat rulează primul]
- **d)** An error — multiple threads cannot append to the same list [O eroare — mai multe fire nu pot adăuga la aceeași listă]

> 💡 **Feedback:**
> *Thread execution order is non-deterministic. All three threads run in parallel for approximately 100 ms and may complete in any order, producing any permutation of [0, 1, 2]. The OS thread scheduler determines the actual order, which can vary between runs. A common misconception is that threads execute in creation order; in reality, thread scheduling is governed by the OS and is inherently unpredictable. [Ordinea de execuție a firelor este nedeterministă. Toate cele trei fire rulează în paralel aproximativ 100 ms și pot finaliza în orice ordine, producând orice permutare a [0, 1, 2]. Planificatorul de fire al sistemului de operare determină ordinea efectivă, care poate varia între execuții. O concepție greșită frecventă este că firele se execută întotdeauna în ordinea creării, planificatorul SO păstrând strict secvența de pornire; în realitate, planificarea firelor este guvernată de sistem și este intrinsec imprevizibilă.]*


---

### Q29.

*[Multiple Choice]*

A student's UDP broadcast sender raises OSError when calling sendto(data, ('255.255.255.255', 5007)) . The socket was created correctly as SOCK_DGRAM . What step was most likely omitted? [Expeditorul de broadcast UDP al unui student ridică OSError la apelarea sendto(data, ('255.255.255.255', 5007)) . Socket-ul a fost creat corect ca SOCK_DGRAM . Ce pas a fost cel mai probabil omis?]

- **a)** sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) — enabling broadcast permission on the socket [ sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) — activarea permisiunii de broadcast pe socket]
- **b)** sock.bind(('', 5007)) — binding to the local port before sending data to the broadcast address in practice [ sock.bind(('', 5007)) — legarea la portul local înainte de trimiterea datelor la adresa broadcast în practică]
- **c)** sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) — allowing the port to be reused by multiple processes [ sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) — permiterea reutilizării portului de mai multe procese]
- **d)** sock.connect(('255.255.255.255', 5007)) — establishing a connection before data transmission [ sock.connect(('255.255.255.255', 5007)) — stabilirea unei conexiuni înainte de transmiterea datelor]

> 💡 **Feedback:**
> *The kernel requires explicit permission via setsockopt(SOL_SOCKET, SO_BROADCAST, 1) before allowing sends to broadcast addresses. This is a safety mechanism, not a hint — omitting it raises OSError. [Nucleul necesită permisiune explicită prin setsockopt(SOL_SOCKET, SO_BROADCAST, 1) înainte de a permite trimiteri la adrese broadcast. Aceasta este un mecanism de siguranță, nu o sugestie — omiterea sa ridică OSError.]*


---

### Q30.

*[Multiple Choice]*

In the code tracing exercise T1, what value does getsockopt(SOL_SOCKET, SO_BROADCAST) return immediately after socket creation, before any setsockopt() call? [În exercițiul de urmărire a codului T1, ce valoare returnează getsockopt(SOL_SOCKET, SO_BROADCAST) imediat după crearea socket-ului, înainte de orice apel setsockopt()?]

- **a)** 0 — broadcast is disabled by default as a kernel safety mechanism [0 — broadcast-ul este dezactivat implicit ca mecanism de siguranță al nucleului]
- **b)** 1 — broadcast is enabled by default on all UDP sockets for convenience [1 — broadcast-ul este activat implicit pe toate socket-urile UDP pentru comoditate]
- **c)** -1 — the option is in an undefined state until explicitly configured [−1 — opțiunea este într-o stare nedefinită până la configurarea explicită]

> 💡 **Feedback:**
> *SO_BROADCAST defaults to 0 (disabled) on all newly created sockets. This deliberate default prevents accidental broadcast transmission. The value changes to 1 only after an explicit setsockopt() call. [SO_BROADCAST este implicit 0 (dezactivat) pe toate socket-urile nou create. Această valoare implicită deliberată previne transmisia broadcast accidentală. Valoarea se schimbă la 1 doar după un apel explicit setsockopt().]*


---

### Q31.

*[Multiple Choice]*

The Week 3 broadcast receiver binds to ('', 5007) . What does the empty string '' represent as the bind address? [Receptorul de broadcast din Săptămâna 3 se leagă la ('', 5007) . Ce reprezintă șirul gol '' ca adresă de legare?]

- **a)** INADDR_ANY (0.0.0.0) — accept packets on all available network interfaces [INADDR_ANY (0.0.0.0) — acceptă pachetele pe toate interfețele de rețea disponibile]
- **b)** Loopback address (127.0.0.1) — restrict reception to locally-originated traffic only [Adresa loopback (127.0.0.1) — restricționează recepția doar la traficul originar local]
- **c)** Broadcast address (255.255.255.255) — listen specifically for broadcast-addressed packets [Adresa broadcast (255.255.255.255) — ascultă specific pentru pachete adresate broadcast]

> 💡 **Feedback:**
> *The empty string is equivalent to INADDR_ANY (0.0.0.0), instructing the socket to accept packets arriving on any network interface. This is essential for broadcast reception — binding to a specific IP would miss broadcast packets addressed to 255.255.255.255. [Șirul gol este echivalent cu INADDR_ANY (0.0.0.0), instruind socket-ul să accepte pachetele care sosesc pe orice interfață de rețea. Aceasta este esențială pentru recepția broadcast — legarea la un IP specific ar rata pachetele broadcast adresate la 255.255.255.255.]*


---

### Q32.

*[Multiple Choice]*

When the broadcast sender in Exercise 1 transmits datagrams, the receiver output shows the sender's IP but a varying source port. Why does the sender's source port change with each execution? [Când expeditorul de broadcast din Exercițiul 1 transmite datagrame, ieșirea receptorului arată IP-ul expeditorului dar un port sursă variabil. De ce se schimbă portul sursă al expeditorului la fiecare execuție?]

- **a)** The OS assigns an ephemeral port from the dynamic range because the sender never calls bind() [SO atribuie un port efemer din intervalul dinamic deoarece expeditorul nu apelează niciodată bind()]
- **b)** Broadcast protocol mandates port randomisation as a security measure against spoofing attacks [Protocolul broadcast impune randomizarea porturilor ca măsură de securitate împotriva atacurilor de falsificare]
- **c)** Docker NAT translates the container's fixed port to a random host port for isolation (default) [Docker NAT traduce portul fix al containerului într-un port aleatoriu al gazdei pentru izolare (implicit)]

> 💡 **Feedback:**
> *The sender does not call bind() to fix a local port. The operating system therefore assigns an ephemeral port from the dynamic range (typically 49152--65535) each time the socket sends data. This is standard UDP behaviour when no explicit source port is requested. [Expeditorul nu apelează bind() pentru a fixa un port local. Prin urmare, sistemul de operare atribuie un port efemer din intervalul dinamic (de obicei 49152--65535) de fiecare dată când socket-ul trimite date. Acesta este comportamentul UDP standard când nu se solicită un port sursă explicit.]*


---

### Q33.

*[True / False]*

In the Week 3 exercises, broadcast receivers set SO_REUSEADDR before calling bind() . This option allows multiple receiver processes to bind to the same port simultaneously. [În exercițiile din Săptămâna 3, receptorii broadcast setează SO_REUSEADDR înainte de a apela bind() . Această opțiune permite mai multor procese receptor să se lege la același port simultan.]

- **a)** true
- **b)** false

> 💡 **Feedback:**
> *SO_REUSEADDR allows a socket to bind to a port that was recently released (avoiding the TIME_WAIT delay) and can allow multiple sockets to bind the same address/port combination for broadcast/multicast reception. This is important when restarting receivers quickly during lab exercises. [SO_REUSEADDR permite unui socket să se lege la un port eliberat recent (evitând întârzierea TIME_WAIT) și poate permite mai multor socket-uri să se lege la aceeași combinație adresă/port pentru recepția broadcast/multicast. Aceasta este importantă la repornirea rapidă a receptorilor în timpul exercițiilor de laborator.]*


---

### Q34.

*[Multiple Choice]*

To join multicast group 224.0.0.1, the code constructs mreq = struct.pack("4sl", socket.inet_aton("224.0.0.1"), socket.INADDR_ANY) . What is the total size of this packed structure in bytes? [Pentru a se alătura grupului multicast 224.0.0.1, codul construiește mreq = struct.pack("4sl", socket.inet_aton("224.0.0.1"), socket.INADDR_ANY) . Care este dimensiunea totală a acestei structuri împachetate în octeți?]

- **a)** 8 bytes — 4 bytes for group IP address plus 4 bytes for the local interface identifier [8 octeți — 4 octeți pentru adresa IP a grupului plus 4 octeți pentru identificatorul interfeței locale]
- **b)** 16 bytes — 4 bytes group IP, 4 bytes interface IP, plus 8 bytes for a 64-bit alignment pad in practice [16 octeți — 4 octeți IP grup, 4 octeți IP interfață, plus 8 octeți pentru alinierea pe 64 de biți în practică]
- **c)** 4 bytes — only the multicast group address is needed; the interface is implicit [4 octeți — este necesară doar adresa grupului multicast; interfața este implicită]
- **d)** 12 bytes — 4 bytes group IP, 4 bytes interface IP, plus 4 bytes for a TTL field (default) [12 octeți — 4 octeți IP grup, 4 octeți IP interfață, plus 4 octeți pentru un câmp TTL (implicit)]

> 💡 **Feedback:**
> *The structure consists of 4 bytes for the multicast group IP address (inet_aton returns 4 bytes) plus 4 bytes for the interface address (INADDR_ANY as a 32-bit integer), totalling 8 bytes. This matches the ip_mreq C structure used by the kernel for multicast group management. [Structura constă din 4 octeți pentru adresa IP a grupului multicast (inet_aton returnează 4 octeți) plus 4 octeți pentru adresa interfeței (INADDR_ANY ca întreg pe 32 de biți), totalizând 8 octeți. Aceasta corespunde structurii C ip_mreq folosită de nucleu pentru gestionarea grupurilor multicast.]*


---

### Q35.

*[Multiple Choice]*

In Exercise 2, the multicast sender uses \--ttl 4 . Which Python setsockopt() call configures this TTL value? [În Exercițiul 2, expeditorul multicast folosește \--ttl 4 . Care apel Python setsockopt() configurează această valoare TTL?]

- **a)** sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 4)
- **b)** sock.setsockopt(socket.SOL_SOCKET, socket.IP_MULTICAST_TTL, 4)
- **c)** sock.setsockopt(socket.IPPROTO_IP, socket.SO_BROADCAST, 4)
- **d)** sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 4)

> 💡 **Feedback:**
> *IP_MULTICAST_TTL is set at the IPPROTO_IP level, not SOL_SOCKET. The TTL value of 4 allows the packet to cross 3 routers before being discarded. This is separate from the unicast IP TTL which is set differently. [IP_MULTICAST_TTL este setat la nivelul IPPROTO_IP, nu SOL_SOCKET. Valoarea TTL de 4 permite pachetului să traverseze 3 rutere înainte de a fi eliminat. Aceasta este separată de TTL-ul IP unicast care este setat diferit.]*


---

### Q36.

*[Multiple Choice]*

The socket option IP_MULTICAST_LOOP controls whether a multicast sender receives its own transmitted packets. When building a chat application on multicast, why might a developer set this option to 0? [Opțiunea de socket IP_MULTICAST_LOOP controlează dacă un expeditor multicast primește propriile pachete transmise. Când construiește o aplicație de chat pe multicast, de ce ar putea un dezvoltator să seteze această opțiune la 0?]

- **a)** To prevent the sender from seeing its own messages, avoiding duplicate display in the chat interface [Pentru a preveni ca expeditorul să-și vadă propriile mesaje, evitând afișarea duplicată în interfața de chat]
- **b)** To reduce network bandwidth by disabling retransmission of multicast packets to the sender in practice [Pentru a reduce lățimea de bandă prin dezactivarea retransmisiei pachetelor multicast către expeditor în practică]
- **c)** To increase multicast TTL automatically when loopback traffic is not consuming hop counts [Pentru a crește automat TTL-ul multicast când traficul loopback nu consumă numărători de salturi]

> 💡 **Feedback:**
> *With loopback enabled (default), a sender that is also a group member receives its own messages — creating echo/duplicate display in a chat application. Disabling loopback (value 0) prevents the sender from processing its own transmissions, which simplifies chat logic. [Cu loopback activat (implicit), un expeditor care este și membru al grupului primește propriile mesaje — creând afișare de ecou/duplicat într-o aplicație de chat. Dezactivarea loopback-ului (valoare 0) împiedică expeditorul să-și proceseze propriile transmisii, ceea ce simplifică logica de chat.]*


---

### Q37.

*[Multiple Choice]*

In code tracing exercise T2, the final line calls setsockopt(IPPROTO_IP, IP_DROP_MEMBERSHIP, mreq) . What network protocol message does this trigger? [În exercițiul de urmărire a codului T2, ultima linie apelează setsockopt(IPPROTO_IP, IP_DROP_MEMBERSHIP, mreq) . Ce mesaj de protocol de rețea declanșează aceasta?]

- **a)** An IGMPv2 Leave Group message informing the router to stop forwarding this group's traffic [Un mesaj IGMPv2 Leave Group care informează ruterul să oprească redirecționarea traficului acestui grup]
- **b)** A TCP FIN segment that gracefully terminates the multicast session with the router [Un segment TCP FIN care termină grațios sesiunea multicast cu ruterul]
- **c)** An ICMP Destination Unreachable message blocking further packets to the group address in practice [Un mesaj ICMP Destination Unreachable care blochează pachete ulterioare la adresa grupului în practică]

> 💡 **Feedback:**
> *IP_DROP_MEMBERSHIP causes the kernel to send an IGMPv2 Leave Group message (type 0x17), informing the local router that this host no longer wants traffic for the specified group. The router can then stop forwarding if no other members remain. [IP_DROP_MEMBERSHIP determină nucleul să trimită un mesaj IGMPv2 Leave Group (tip 0x17), informând ruterul local că această gazdă nu mai dorește trafic pentru grupul specificat. Ruterul poate apoi să oprească redirecționarea dacă nu mai rămân alți membri.]*


---

### Q38.

*[Multiple Choice]*

To isolate Ethernet broadcast frames in a Wireshark capture, which display filter should be applied? [Pentru a izola cadrele broadcast Ethernet într-o captură Wireshark, care filtru de afișare ar trebui aplicat?]

- **a)** eth.dst == ff:ff:ff:ff:ff:ff
- **b)** ip.dst == 255.255.255.255
- **c)** udp.port == 5007
- **d)** tcp.flags.syn == 1

> 💡 **Feedback:**
> *The filter eth.dst == ff:ff:ff:ff:ff:ff matches all Ethernet frames with the broadcast destination MAC. This is a display filter (applied post-capture). A capture filter equivalent would be simply broadcast . [Filtrul eth.dst == ff:ff:ff:ff:ff:ff se potrivește cu toate cadrele Ethernet cu adresa MAC de destinație broadcast. Acesta este un filtru de afișare (aplicat post-captură). Un echivalent de filtru de captură ar fi simplu broadcast .]*


---

### Q39.

*[Multiple Choice]*

To identify new TCP connection attempts in a Wireshark capture (the first packet of a three-way handshake), which display filter isolates SYN-only segments? [Pentru a identifica tentativele de conexiune TCP noi într-o captură Wireshark (primul pachet al unui handshake triplu), care filtru de afișare izolează segmentele doar-SYN?]

- **a)** tcp.flags.syn == 1 and tcp.flags.ack == 0
- **b)** tcp.flags.fin == 1
- **c)** tcp.analysis.retransmission
- **d)** tcp.flags.rst == 1

> 💡 **Feedback:**
> *The filter tcp.flags.syn == 1 and tcp.flags.ack == 0 matches pure SYN segments (the initial connection request). Adding the ACK check excludes SYN-ACK responses. The simpler filter tcp.flags.syn == 1 would include both SYN and SYN-ACK. [Filtrul tcp.flags.syn == 1 and tcp.flags.ack == 0 se potrivește cu segmentele SYN pure (cererea inițială de conexiune). Adăugarea verificării ACK exclude răspunsurile SYN-ACK. Filtrul mai simplu tcp.flags.syn == 1 ar include atât SYN, cât și SYN-ACK.]*


---

### Q40.

*[Multiple Choice]*

In the tunnel's relay function, when the client closes its connection, how does the relay detect this event and trigger cleanup of the server-side connection? [În funcția releu a tunelului, când clientul își închide conexiunea, cum detectează releul acest eveniment și declanșează curățarea conexiunii de partea serverului?]

- **a)** recv() returns empty bytes (b''), which the relay interprets as the peer's FIN; it then calls shutdown(SHUT_WR) on the other socket [recv() returnează octeți goi (b''), pe care releul îi interpretează ca FIN al corespondentului; apoi apelează shutdown(SHUT_WR) pe celălalt socket]
- **b)** A timeout exception fires after 30 seconds of inactivity, causing both sockets to be forcibly closed, per the protocol specification [O excepție de timeout se declanșează după 30 de secunde de inactivitate, forțând închiderea ambelor socket-uri, conform specificației protocolului]
- **c)** recv() raises a ConnectionResetError immediately when the client disconnects from the tunnel [recv() ridică un ConnectionResetError imediat când clientul se deconectează de la tunel]

> 💡 **Feedback:**
> *The relay thread reading from the client socket receives an empty bytes object (b'') from recv(), indicating the client sent FIN. The thread then exits its loop and calls shutdown(SHUT_WR) on the server socket, signalling the server that no more data will arrive from this direction. [Firul de execuție al releului care citește de la socket-ul clientului primește un obiect de octeți gol (b'') de la recv(), indicând că clientul a trimis FIN. Firul de execuție iese apoi din buclă și apelează shutdown(SHUT_WR) pe socket-ul serverului, semnalând serverului că nu vor mai sosi date din această direcție.]*

---

## 🔬 §3. Drag and Drop into Text (5 questions)


---

### Q41.

*[Drag and Drop]*

Complete the Python statement that enables broadcast on a UDP socket. [Completați instrucțiunea Python care activează broadcast-ul pe un socket UDP.] sock.setsockopt(socket.[[1]], socket.[[2]], [[3]])

> *Available items / Elemente disponibile:*
[ SOL_SOCKET ] [ SO_BROADCAST ] [ 1 ] [ IPPROTO_IP ] [ SO_REUSEADDR ] [ 0 ]

> 💡 **Feedback:**
> *The correct call is sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1). SOL_SOCKET is the protocol level for general socket options, SO_BROADCAST is the specific option, and 1 enables it. [Apelul corect este sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1). SOL_SOCKET este nivelul de protocol pentru opțiuni generale de socket, SO_BROADCAST este opțiunea specifică, iar 1 o activează.]*


---

### Q42.

*[Drag and Drop]*

Complete the Python code that constructs the mreq structure and joins a multicast group. [Completați codul Python care construiește structura mreq și aderă la un grup multicast.] mreq = socket.inet_aton("[[1]]") + struct.pack('=I', socket.INADDR_ANY)sock.setsockopt(socket.[[2]], socket.[[3]], mreq)

> *Available items / Elemente disponibile:*
[ 224.0.0.1 ] [ IPPROTO_IP ] [ IP_ADD_MEMBERSHIP ] [ 224.0.0.1 ] [ SOL_SOCKET ] [ IP_MULTICAST_TTL ]

> 💡 **Feedback:**
> *The group address 224.0.0.1 is packed with INADDR_ANY into mreq. The setsockopt call uses IPPROTO_IP level and IP_ADD_MEMBERSHIP option. [Adresa de grup 224.0.0.1 este împachetată cu INADDR_ANY în mreq. Apelul setsockopt folosește nivelul IPPROTO_IP și opțiunea IP_ADD_MEMBERSHIP.]*


---

### Q43.

*[Drag and Drop]*

Complete the Python broadcast send call using the correct address and port from the Week 3 exercises. [Completați apelul de trimitere broadcast în Python folosind adresa și portul corecte din exercițiile Săptămânii 3.] sock.sendto(data, ("[[1]]", [[2]]))

> *Available items / Elemente disponibile:*
[ 255.255.255.255 ] [ 5007 ] [ 172.20.0.255 ] [ 5001 ] [ 224.0.0.1 ] [ 8080 ]

> 💡 **Feedback:**
> *The broadcast exercises use the limited broadcast address 255.255.255.255 with UDP port 5007. The limited broadcast address ensures the packet stays within the local L2 segment. [Exercițiile de broadcast folosesc adresa broadcast limitată 255.255.255.255 cu portul UDP 5007. Adresa broadcast limitată asigură că pachetul rămâne în segmentul L2 local.]*


---

### Q44.

*[Drag and Drop]*

Complete the Python statement that sets the multicast TTL to 4 hops. [Completați instrucțiunea Python care setează TTL-ul multicast la 4 salturi.] sock.setsockopt(socket.[[1]], socket.[[2]], [[3]])

> *Available items / Elemente disponibile:*
[ IPPROTO_IP ] [ IP_MULTICAST_TTL ] [ 4 ] [ SOL_SOCKET ] [ IP_ADD_MEMBERSHIP ] [ 1 ] [ 255 ]

> 💡 **Feedback:**
> *IP_MULTICAST_TTL is set at the IPPROTO_IP level. A TTL of 4 allows the multicast packet to cross up to 3 routers (decremented at each hop). TTL=1 restricts to link-local only. [IP_MULTICAST_TTL se setează la nivelul IPPROTO_IP. Un TTL de 4 permite pachetului multicast să traverseze până la 3 rutere (decrementat la fiecare salt). TTL=1 restricționează doar la local-pe-legătură.]*


---

### Q45.

*[Drag and Drop]*

Complete the core relay loop from the TCP tunnel code. When recv() returns empty bytes, the source has closed the connection. [Completați bucla principală de relay din codul tunelului TCP. Când recv() returnează octeți goi, sursa a închis conexiunea.]

```python
data = src.[[1]](4096)
if not data:
    break
dst.[[2]](data)
```

> *Available items / Elemente disponibile:*
[ recv ] [ sendall ] [ send ] [ recvfrom ] [ write ] [ read ]

> 💡 **Feedback:**
> *The relay reads with recv(4096) and writes with sendall(data). recv() returns b'' when the peer sends FIN. sendall() is used instead of send() to guarantee all bytes are transmitted. [Relay-ul citește cu recv(4096) și scrie cu sendall(data). recv() returnează b'' când peer-ul trimite FIN. sendall() este folosit în loc de send() pentru a garanta transmiterea tuturor octeților.]*

---

## 🔬 §4. Gap Select (Select Missing Words) (4 questions)


---

### Q46.

*[Gap Select]*

Broadcast is supported only over [[1]] because [[2]] requires a dedicated connection to a specific host. [Broadcast-ul este suportat doar prin ___ deoarece ___ necesită o conexiune dedicată la o gazdă specifică.]

> *Options per gap / Opțiuni pentru fiecare spațiu:*
> **Gap [[1]]:** [ UDP ] [ TCP ] [ ICMP ]
> **Gap [[2]]:** [ TCP ] [ UDP ] [ ARP ]

> 💡 **Feedback:**
> *TCP requires a connection to a single peer (3-way handshake), making broadcast impossible. UDP is connectionless and can send datagrams to broadcast addresses. [TCP necesită o conexiune la un singur peer (strângere de mână în 3 pași), făcând broadcast-ul imposibil. UDP este fără conexiune și poate trimite datagrame la adrese broadcast.]*


---

### Q47.

*[Gap Select]*

To receive multicast traffic, a socket must call [[1]] at the [[2]] protocol level. Without this call, the kernel [[3]] incoming multicast packets. [Pentru a primi trafic multicast, un socket trebuie să apeleze ___ la nivelul de protocol ___. Fără acest apel, nucleul ___ pachetele multicast primite.]

> *Options per gap / Opțiuni pentru fiecare spațiu:*
> **Gap [[1]]:** [ IP_ADD_MEMBERSHIP ] [ SO_BROADCAST ] [ IP_MULTICAST_TTL ]
> **Gap [[2]]:** [ IPPROTO_IP ] [ SOL_SOCKET ] [ IPPROTO_TCP ]
> **Gap [[3]]:** [ silently ignores ] [ queues indefinitely ] [ forwards to broadcast ]

> 💡 **Feedback:**
> *IP_ADD_MEMBERSHIP at IPPROTO_IP level is mandatory. The kernel silently ignores multicast packets for groups the host has not joined. Binding to a port alone is necessary but not sufficient. [IP_ADD_MEMBERSHIP la nivelul IPPROTO_IP este obligatoriu. Nucleul ignoră silențios pachetele multicast pentru grupuri la care gazda nu a aderat. Legarea la un port singură este necesară dar nu suficientă.]*


---

### Q48.

*[Gap Select]*

When a client connects through the TCP tunnel, a total of [[1]] TCP connections are established. The server sees the [[2]] IP address as the connection source. The relay uses [[3]] instead of send() to guarantee complete data transmission. [Când un client se conectează prin tunelul TCP, un total de ___ conexiuni TCP sunt stabilite. Serverul vede adresa IP a ___ ca sursă a conexiunii. Relay-ul folosește ___ în loc de send() pentru a garanta transmiterea completă a datelor.]

> *Options per gap / Opțiuni pentru fiecare spațiu:*
> **Gap [[1]]:** [ 2 ] [ 1 ] [ 3 ]
> **Gap [[2]]:** [ router's ] [ client's ] [ server's own ]
> **Gap [[3]]:** [ sendall() ] [ write() ] [ sendto() ]

> 💡 **Feedback:**
> *Two TCP connections exist: client↔router:12345 and router↔server:8080. The server's connection log shows 172.20.0.254 (router), not the client's address. sendall() loops internally until all bytes are written, unlike send() which may transmit partial data. [Două conexiuni TCP există: client↔router:12345 și router↔server:8080. Jurnalul de conexiuni al serverului arată 172.20.0.254 (ruter), nu adresa clientului. sendall() iterează intern până când toți octeții sunt scriși, spre deosebire de send() care poate transmite date parțiale.]*


---

### Q49.

*[Gap Select]*

In the tunnel relay loop, when recv() returns [[1]], it indicates the peer has [[2]]. The relay then calls [[3]] on the destination socket to signal end of data in one direction. [În bucla de relay a tunelului, când recv() returnează ___, aceasta indică faptul că peer-ul a ___. Relay-ul apelează apoi ___ pe socket-ul destinație pentru a semnala sfârșitul datelor într-o direcție.]

> *Options per gap / Opțiuni pentru fiecare spațiu:*
> **Gap [[1]]:** [ empty bytes (b'') ] [ None ] [ -1 ]
> **Gap [[2]]:** [ sent FIN (closed the connection) ] [ timed out ] [ sent RST (reset the connection) ]
> **Gap [[3]]:** [ shutdown(SHUT_WR) ] [ close() ] [ disconnect() ]

> 💡 **Feedback:**
> *An empty bytes object b'' from recv() means the peer sent a TCP FIN segment, initiating connection close. The relay responds with shutdown(SHUT_WR) to propagate the close signal to the other side while keeping the reverse direction open until it also receives FIN. [Un obiect bytes gol b'' de la recv() înseamnă că peer-ul a trimis un segment TCP FIN, inițiind închiderea conexiunii. Relay-ul răspunde cu shutdown(SHUT_WR) pentru a propaga semnalul de închidere către cealaltă parte păstrând direcția inversă deschisă până la primirea FIN.]*
