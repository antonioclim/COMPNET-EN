# Week 06 — Computer Networks
### *Rețele de Calculatoare — Săptămâna 6*

> NAT / MASQUERADE, iptables, Conntrack, ARP, DHCP, SDN / OpenFlow
> 77 questions  •  Bilingual EN/RO

---


## §1.  Curs / Lecture   (44 questions)

### Q1. `Multiple Choice`
**PAT as Many-to-One NAT Variant / PAT ca variantă NAT de tip mulți-la-unu**

> Which form of Network Address Translation enables many internal hosts to share a single public IP address by multiplexing connections through unique port numbers? [Care formă de traducere a adreselor de rețea (NAT) permite mai multor gazde interne să partajeze o singură adresă IP publică prin multiplexarea conexiunilor cu ajutorul numerelor de port unice?]

- **a)  Dynamic NAT with pool-based address allocation [NAT dinamic cu alocare de adrese din grup]**
- **b)  Static NAT with permanent one-to-one address mapping [NAT static cu mapare permanentă unu-la-unu]**
- **c)  Proxy ARP [Proxy ARP]**
- **d)  PAT (Port Address Translation) [PAT (Port Address Translation)]**

> 💡 **Feedback:** PAT (Port Address Translation), also known as NAPT or NAT Overload, multiplexes connections via translated port numbers, enabling many-to-one address mapping. A common misconception is confusing static NAT (one-to-one mapping) with PAT; static NAT requires a dedicated public address per internal host and cannot share a single IP among multiple hosts. [PAT (Port Address Translation), cunoscut și ca NAPT sau NAT Overload, multiplexează conexiunile prin numere de port traduse, permițând o mapare mulți-la-unu. O concepție greșită frecventă este confuzia între NAT static (mapare unu-la-unu) și PAT; NAT static necesită o adresă publică dedicată pentru fiecare gazdă internă și nu poate partaja o singură adresă IP între mai multe gazde.]

---

### Q2. `Multiple Choice`
**Static NAT Characteristics / Caracteristicile NAT-ului static**

> What distinguishes static NAT from dynamic NAT and PAT? [Ce deosebește NAT-ul static de NAT-ul dinamic și de PAT?]

- **a)  It encrypts traffic between internal and external hosts [Criptează traficul între gazdele interne și cele externe]**
- **b)  It assigns public IPs from a pool on demand and releases them when connections end [Atribuie adrese IP publice dintr-un grup la cerere și le eliberează la terminarea conexiunilor]**
- **c)  It establishes a permanent one-to-one mapping between an internal and an external address [Stabilește o mapare permanentă unu-la-unu între o adresă internă și o adresă externă]**
- **d)  It multiplexes many internal hosts through port numbers on a single public IP [Multiplexează mai multe gazde interne prin numere de port pe o singură adresă IP publică]**

> 💡 **Feedback:** Static NAT maintains a permanent one-to-one mapping between a specific internal address and a specific external address, typically used for servers that must be consistently reachable from outside. A common misconception is that all NAT variants share a single public IP; in fact, static NAT always requires a dedicated public address per mapped host. [NAT static menține o mapare permanentă unu-la-unu între o adresă internă specifică și o adresă externă specifică, fiind utilizat de obicei pentru servere care trebuie să fie accesibile constant din exterior. O concepție greșită frecventă este că toate variantele NAT partajează o singură adresă IP publică; în realitate, NAT static necesită întotdeauna o adresă publică dedicată pentru fiecare gazdă mapată.]

---

### Q3. `Multiple Choice`
**RFC 1918 Private Address Ranges / Intervalele de adrese private RFC 1918**

> Which of the following is not one of the three private IPv4 address ranges defined by RFC 1918? [Care dintre următoarele nu este unul dintre cele trei intervale de adrese IPv4 private definite de RFC 1918?]

- **a)  10.0.0.0/8**
- **b)  192.168.0.0/16**
- **c)  172.16.0.0/12**
- **d)  203.0.113.0/24**

> 💡 **Feedback:** RFC 1918 defines three private ranges: 10.0.0.0/8, 172.16.0.0/12, and 192.168.0.0/16. The range 203.0.113.0/24 is TEST-NET-3, reserved for documentation by RFC 5737. A common misconception is treating documentation-reserved ranges as private address space; they serve entirely different purposes. [RFC 1918 definește trei intervale private: 10.0.0.0/8, 172.16.0.0/12 și 192.168.0.0/16. Intervalul 203.0.113.0/24 este TEST-NET-3, rezervat pentru documentație de RFC 5737. O concepție greșită frecventă este tratarea intervalelor rezervate pentru documentație ca spațiu de adrese private; acestea au scopuri complet diferite.]

---

### Q4. `Multiple Choice`
**IPv4 Address Exhaustion and NAT / Epuizarea adreselor IPv4 și NAT**

> NAT emerged as a practical response to a fundamental limitation of IPv4. What was the core problem it addressed? [NAT a apărut ca un răspuns practic la o limitare fundamentală a IPv4. Care a fost problema esențială pe care a rezolvat-o?]

- **a)  IPv4 packets being too large for network transmission, requiring fragmentation at every intermediate router [Pachetele IPv4 fiind prea mari pentru transmisia prin rețea, necesitând fragmentare la fiecare ruter intermediar]**
- **b)  IPv4 lacking native encryption capabilities, leaving all traffic vulnerable to eavesdropping without additional protocols [IPv4 neavând capacități native de criptare, lăsând tot traficul vulnerabil la interceptare pasivă fără protocoale suplimentare]**
- **c)  IPv4 address space exhaustion — insufficient public addresses for the growing number of devices [Epuizarea spațiului de adrese IPv4 — adrese publice insuficiente pentru numărul tot mai mare de dispozitive]**
- **d)  IPv4 being incompatible with Ethernet frame formats, requiring a complete redesign of the data link layer [IPv4 fiind incompatibil cu formatele de cadre Ethernet, necesitând reproiectarea completă a stratului legătură de date]**

> 💡 **Feedback:** The 32-bit IPv4 address space (approximately 4.3 billion addresses) was insufficient for the growing number of Internet-connected devices. IANA exhausted the free pool in 2011. NAT allows organisations to use private addresses internally while sharing limited public addresses. A common misconception is that NAT was designed as a security measure; it was created purely to conserve IPv4 addresses. [Spațiul de adrese IPv4 pe 32 de biți (aproximativ 4,3 miliarde de adrese) a fost insuficient pentru numărul tot mai mare de dispozitive conectate la Internet. IANA a epuizat grupul de adrese libere în 2011. NAT permite organizațiilor să utilizeze adrese private intern, partajând adresele publice limitate. O concepție greșită frecventă este că NAT a fost conceput ca o măsură de securitate; în realitate, a fost creat exclusiv pentru conservarea adreselor IPv4.]

---

### Q5. `Multiple Choice`
**Conntrack Table Stores Both Tuples / Tabela conntrack stochează ambele tupluri**

> When a host at 192.168.10.2:45678 connects through a NAT router (public IP 203.0.113.1, translated port 50001) to a server at 8.8.8.8:443, what information does the conntrack table record? [Când o gazdă de la 192.168.10.2:45678 se conectează printr-un ruter NAT (IP public 203.0.113.1, port tradus 50001) la un server de la 8.8.8.8:443, ce informații înregistrează tabela conntrack?]

- **a)  Only the original internal source and destination addresses before translation begins [Doar adresele sursă și destinație interne originale înainte de începerea traducerii]**
- **b)  Only the translated external tuple with a timestamp [Doar tuplul extern tradus cu o marcă temporală]**
- **c)  Only the destination server address and port [Doar adresa și portul serverului destinație]**
- **d)  Both the original (internal) tuple and the translated (external) tuple [Atât tuplul original (intern), cât și tuplul tradus (extern)]**

> 💡 **Feedback:** Conntrack stores both the original tuple (internal source/destination) and the reply/translated tuple (external addresses) to enable bidirectional reverse translation for return traffic. A common misconception is that only the external tuple is stored; without the original tuple, the router could not reverse-translate return packets to the correct internal host. [Conntrack stochează atât tuplul original (sursa/destinația internă), cât și tuplul de răspuns/tradus (adresele externe), pentru a permite traducerea inversă bidirecțională a traficului de retur. O concepție greșită frecventă este că se stochează doar tuplul extern; fără tuplul original, ruterul nu ar putea traduce invers pachetele de retur către gazda internă corectă.]

---

### Q6. `Multiple Choice`
**PAT Port Multiplexing for Identical Internal Ports / Multiplexarea porturilor PAT pentru porturi interne identice**

> Two internal hosts (192.168.10.2 and 192.168.10.3) both open connections using local port 12345 to the same external server. How does the NAT router distinguish return traffic for each host? [Două gazde interne (192.168.10.2 și 192.168.10.3) deschid ambele conexiuni folosind portul local 12345 către același server extern. Cum distinge ruterul NAT traficul de retur pentru fiecare gazdă?]

- **a)  It uses a different public IP address for each internal host [Folosește o adresă IP publică diferită pentru fiecare gazdă internă]**
- **b)  Only one host can connect at a time; the second connection is blocked [Doar o singură gazdă se poate conecta la un moment dat; a doua conexiune este blocată]**
- **c)  It inspects the application-layer payload to identify the sender [Inspectează sarcina utilă (payload) de la nivelul aplicație pentru a identifica expeditorul]**
- **d)  It assigns different translated source ports to each connection [Atribuie porturi sursă traduse diferite fiecărei conexiuni]**

> 💡 **Feedback:** The NAT router assigns different translated source ports to each connection (e.g., 50001 and 50002), even though both hosts used internal port 12345. Return traffic is then distinguished by these unique external ports. A common misconception is that NAT preserves the original source port; the router selects a port from its available pool and there is no guarantee the original port is reused. [Ruterul NAT atribuie porturi sursă traduse diferite fiecărei conexiuni (de exemplu, 50001 și 50002), chiar dacă ambele gazde au folosit portul intern 12345. Traficul de retur este apoi diferențiat prin aceste porturi externe unice. O concepție greșită frecventă este că NAT păstrează portul sursă original; ruterul selectează un port din grupul disponibil și nu există garanția reutilizării portului original.]

---

### Q7. `True / False`
**NAT May Change Source Port / NAT poate modifica portul sursă**

> During PAT translation, the NAT router selects a source port from its available pool and may assign a different port than the one used by the internal application, especially when the original port is already in use by another connection. [În timpul traducerii PAT, routerul NAT selectează un port sursă din grupul său disponibil și poate atribui un port diferit de cel folosit de aplicația internă, în special când portul original este deja utilizat de o altă conexiune.]

- **a)  true**
- **b)  false**

> 💡 **Feedback:** The NAT router selects a source port from its available pool. It may reuse the original port if available, but there is no guarantee — another connection may already occupy that port on the public interface. Applications that assume port preservation (some P2P protocols, certain VoIP implementations) may fail behind NAT. [Routerul NAT selectează un port sursă din grupul disponibil. Poate reutiliza portul original dacă este disponibil, dar nu există nicio garanție — o altă conexiune poate ocupa deja acel port pe interfața publică. Aplicațiile care presupun păstrarea portului (unele protocoale P2P, anumite implementări VoIP) pot eșua în spatele NAT.]

---

### Q8. `True / False`
**Conntrack Entries Are Permanent / Intrările conntrack sunt permanente**

> Once a NAT mapping is created in the conntrack table, it remains permanently until the router is rebooted or the entry is manually deleted. [Odată creată o mapare NAT în tabela conntrack, aceasta rămâne permanent până la repornirea ruterului sau ștergerea manuală a intrării.]

- **a)  true**
- **b)  false**

> 💡 **Feedback:** Conntrack entries have timeouts. TCP established connections typically expire after extended inactivity (e.g., 5 days), while UDP entries expire much sooner (30 seconds to 2 minutes). Long-running connections need keepalive packets to prevent NAT timeout. A common misconception is that once created, NAT mappings persist indefinitely; VoIP and gaming applications frequently suffer from unexpected disconnections caused by conntrack entry expiration. [Intrările conntrack au perioade de expirare. Conexiunile TCP stabilite expiră de obicei după inactivitate prelungită (de exemplu, 5 zile), iar intrările UDP expiră mult mai repede (30 de secunde până la 2 minute). Conexiunile de lungă durată necesită pachete keepalive pentru a preveni expirarea NAT. O concepție greșită frecventă este că, odată create, mapările NAT persistă la nesfârșit; aplicațiile VoIP și de gaming suferă frecvent de deconectări neașteptate cauzate de expirarea intrărilor conntrack.]

---

### Q9. `Multiple Choice`
**Conntrack Lifecycle State After SYN-ACK / Starea ciclului de viață conntrack după SYN-ACK**

> During a TCP connection through NAT, the conntrack entry is initially created in the NEW state when the internal host sends a SYN. After the external server responds with SYN-ACK, to which state does the conntrack entry transition? [În timpul unei conexiuni TCP prin NAT, intrarea conntrack este creată inițial în starea NEW când gazda internă trimite un SYN. După ce serverul extern răspunde cu SYN-ACK, în ce stare trece intrarea conntrack?]

- **a)  RELATED**
- **b)  TIME_WAIT**
- **c)  ESTABLISHED**
- **d)  CONFIRMED**

> 💡 **Feedback:** After the SYN-ACK arrives and confirms bidirectional communication, the conntrack entry transitions to ESTABLISHED, which enables continued translation for the duration of the session. A common misconception is confusing conntrack states with TCP states such as TIME_WAIT; conntrack states (NEW, ESTABLISHED, RELATED) track translation eligibility, not the TCP finite state machine. [După ce SYN-ACK ajunge și confirmă comunicarea bidirecțională, intrarea conntrack trece în starea ESTABLISHED, ceea ce permite continuarea traducerii pe durata sesiunii. O concepție greșită frecventă este confuzia dintre stările conntrack și stările TCP precum TIME_WAIT; stările conntrack (NEW, ESTABLISHED, RELATED) urmăresc eligibilitatea traducerii, nu mașina de stări finită TCP.]

---

### Q10. `Multiple Choice`
**NAT Translation Trace — Server-Visible Source / Trasarea traducerii NAT — sursa vizibilă de server**

> Host h1 (192.168.10.2) sends a packet to server h3 (203.0.113.2) through a NAT router with public IP 203.0.113.1. What source IP address does the server h3 observe? [Gazda h1 (192.168.10.2) trimite un pachet către serverul h3 (203.0.113.2) prin intermediul unui ruter NAT cu IP-ul public 203.0.113.1. Ce adresă IP sursă observă serverul h3?]

- **a)  192.168.10.2 (h1's private IP) [192.168.10.2 (IP-ul privat al lui h1)]**
- **b)  192.168.10.1 (the router's private interface) [192.168.10.1 (interfața privată a ruterului)]**
- **c)  203.0.113.1 (the NAT router's public IP) [203.0.113.1 (IP-ul public al ruterului NAT)]**
- **d)  203.0.113.2 (h3's own IP) [203.0.113.2 (IP-ul propriu al lui h3)]**

> 💡 **Feedback:** Private addresses (RFC 1918) are never visible outside the NAT boundary. The server only sees the NAT router's public IP, 203.0.113.1, as the source. A common misconception is that private IP addresses travel across the Internet; in reality, the NAT router rewrites the source address before forwarding the packet, and external hosts have no knowledge of the internal addressing scheme. [Adresele private (RFC 1918) nu sunt niciodată vizibile în afara granței NAT. Serverul vede doar IP-ul public al ruterului NAT, 203.0.113.1, ca sursă. O concepție greșită frecventă este că adresele IP private circulă prin Internet; în realitate, ruterul NAT rescrie adresa sursă înainte de a redirecționa pachetul, iar gazdele externe nu au cunoștință despre schema de adresare internă.]

---

### Q11. `Multiple Choice`
**Why NAT Breaks Inbound Connections / De ce NAT întrerupe conexiunile de intrare**

> Peer-to-peer applications and inbound connections often fail when traversing NAT. What is the fundamental reason for this? [Aplicațiile peer-to-peer (egal la egal) și conexiunile de intrare eșuează adesea la traversarea NAT. Care este motivul fundamental?]

- **a)  Without an existing conntrack entry, NAT cannot map unsolicited inbound packets to an internal host [Fără o intrare conntrack existentă, NAT nu poate mapa pachetele de intrare nesolicitate către o gazdă internă]**
- **b)  NAT blocks all UDP traffic by default [NAT blochează tot traficul UDP implicit]**
- **c)  NAT encrypts all outbound traffic at the network layer, preventing external hosts from responding or establishing reverse connections [NAT criptează tot traficul de ieșire la nivelul rețelei, împiedicând gazdele externe să răspundă sau să stabilească conexiuni inverse]**
- **d)  NAT requires all applications to use TCP exclusively [NAT necesită ca toate aplicațiile să utilizeze exclusiv TCP]**

> 💡 **Feedback:** NAT relies on conntrack entries created by outbound connections. Without a pre-existing entry, unsolicited inbound packets cannot be mapped to any internal host and are dropped. A common misconception is that NAT blocks inbound traffic intentionally as a security feature; in reality, it simply has no mapping to route unsolicited packets, which is obscurity rather than deliberate security enforcement. [NAT se bazează pe intrările conntrack create de conexiunile de ieșire. Fără o intrare preexistentă, pachetele de intrare nesolicitate nu pot fi mapate către nicio gazdă internă și sunt eliminate. O concepție greșită frecventă este că NAT blochează traficul de intrare intenționat ca funcție de securitate; în realitate, pur și simplu nu are o mapare pentru a direcționa pachetele nesolicitate, ceea ce reprezintă obscuritate, nu aplicarea deliberată a securității.]

---

### Q12. `True / False`
**NAT Provides Security / NAT oferă securitate**

> NAT is an adequate replacement for a firewall because it hides internal IP addresses and blocks all inbound attacks. [NAT este un înlocuitor adecvat al unui firewall (paravan de protecție) deoarece ascunde adresele IP interne și blochează toate atacurile de intrare.]

- **a)  true**
- **b)  false**

> 💡 **Feedback:** NAT provides obscurity, not security. While it blocks unsolicited inbound connections (no conntrack entry), it does not inspect packet contents, block outbound malware, detect intrusions, or encrypt traffic. A proper stateful firewall is still required. The key question to consider: if an employee clicks a malicious link, does NAT stop the malware from calling home? The  [NAT oferă obscuritate, nu securitate. Deși blochează conexiunile de intrare nesolicitate (fără intrare conntrack), nu inspectează conținutul pachetelor, nu blochează programele malware de ieșire, nu detectează intruziunile și nu criptează traficul. Un firewall (paravan de protecție) cu inspecție de stare rămâne necesar. Întrebarea cheie de considerat: dacă un angajat accesează un link malițios, oprește NAT-ul programul malware să comunice cu serverul de comandă? Răspunsul este nu.]

---

### Q13. `Multiple Choice`
**Protocols Requiring ALGs Behind NAT / Protocoale care necesită ALG-uri în spatele NAT**

> Certain application-layer protocols embed IP addresses within their payload data, causing them to break when traversing NAT without special handling. What mechanism is used to address this? [Anumite protocoale de la nivelul aplicație încorporează adrese IP în cadrul sarcinii lor utile (payload), ceea ce le face să nu funcționeze la traversarea NAT fără o gestionare specială. Ce mecanism este utilizat pentru a rezolva această problemă?]

- **a)  Proxy ARP [Proxy ARP]**
- **b)  Hairpin NAT [Hairpin NAT]**
- **c)  Application Layer Gateway (ALG) [Application Layer Gateway (ALG)]**
- **d)  Port forwarding [Redirecționarea porturilor (port forwarding)]**

> 💡 **Feedback:** Application Layer Gateways (ALGs) are NAT helpers that understand specific protocols (such as FTP, SIP, H.323) and modify embedded IP addresses in payloads to match the translated addresses. A common misconception is that port forwarding solves this problem; port forwarding maps ports to internal hosts but does not inspect or modify payload-level IP references. [ALG-urile (Application Layer Gateway) sunt module de asistență NAT care înțeleg protocoale specifice (precum FTP, SIP, H.323) și modifică adresele IP încorporate în sarcina utilă (payload) pentru a corespunde adreselor traduse. O concepție greșită frecventă este că redirecționarea porturilor (port forwarding) rezolvă această problemă; redirecționarea porturilor mapează porturile către gazde interne, dar nu inspectează și nu modifică referințele IP din sarcina utilă.]

---

### Q14. `Multiple Choice`
**NAT State Dependency as Single Point of Failure / Dependența de stare a NAT ca punct unic de eșec**

> A network administrator argues that NAT introduces a reliability risk because the NAT device must maintain session state for all active connections. If the NAT device fails, what happens to existing connections passing through it? [Un administrator de rețea susține că NAT introduce un risc de fiabilitate deoarece dispozitivul NAT trebuie să mențină starea sesiunii pentru toate conexiunile active. Dacă dispozitivul NAT eșuează, ce se întâmplă cu conexiunile existente care trec prin el?]

- **a)  Connections seamlessly fail over to an alternate path using IPv6 [Conexiunile trec automat pe o cale alternativă utilizând IPv6]**
- **b)  Connections continue because external hosts remember the original private addresses [Conexiunile continuă deoarece gazdele externe rețin adresele private originale]**
- **c)  Only UDP connections are affected; TCP connections survive because they are connection-oriented [Doar conexiunile UDP sunt afectate; conexiunile TCP supraviețuiesc deoarece sunt orientate pe conexiune]**
- **d)  All connections are dropped because the translation state in the conntrack table is lost [Toate conexiunile sunt pierdute deoarece starea de traducere din tabela conntrack se pierde]**

> 💡 **Feedback:** NAT is stateful — the conntrack table holds bidirectional mappings for every active session. If the NAT device fails, all stored translation state is lost and existing connections cannot continue, because return packets have no mapping to reach internal hosts. This makes the NAT device a single point of failure for all traversing sessions. A common misconception is that external hosts could somehow reach internal hosts directly after NAT failure; since external hosts only know the NAT public IP, they have no route to internal addresses. [NAT este cu stare (stateful) — tabela conntrack conține mapări bidirecționale pentru fiecare sesiune activă. Dacă dispozitivul NAT eșuează, toată starea de traducere stocată se pierde și conexiunile existente nu pot continua, deoarece pachetele de retur nu au nicio mapare pentru a ajunge la gazdele interne. Aceasta face din dispozitivul NAT un punct unic de eșec pentru toate sesiunile care îl traversează. O concepție greșită frecventă este că gazdele externe ar putea cumva ajunge direct la gazdele interne după eșecul NAT; deoarece gazdele externe cunosc doar IP-ul public NAT, ele nu au rută către adresele interne.]

---

### Q15. `True / False`
**NAT and IPv6 Relationship / Relația dintre NAT și IPv6**

> NAT is fundamentally an IPv4 workaround for address exhaustion, and IPv6 was designed to restore end-to-end connectivity without requiring address translation. [NAT este fundamental o soluție provizorie IPv4 pentru epuizarea adreselor, iar IPv6 a fost proiectat pentru a restabili conectivitatea de la capăt la capăt fără a necesita traducerea adreselor.]

- **a)  true**
- **b)  false**

> 💡 **Feedback:** IPv6 provides a vastly larger address space (128-bit vs. 32-bit), making NAT unnecessary for address conservation. IPv6 restores the original Internet design principle of end-to-end addressing where every device can have a globally unique address. A common misconception is that NAT is also needed in IPv6 networks; whilst NAT66 exists for specific edge cases, the fundamental purpose of IPv6 is to eliminate the need for address translation. [IPv6 oferă un spațiu de adrese mult mai mare (128 de biți față de 32 de biți), făcând NAT inutil pentru conservarea adreselor. IPv6 restabilește principiul original de proiectare a Internetului — adresarea de la capăt la capăt, unde fiecare dispozitiv poate avea o adresă unică la nivel global. O concepție greșită frecventă este că NAT este necesar și în rețelele IPv6; deși NAT66 există pentru cazuri specifice, scopul fundamental al IPv6 este eliminarea necesității traducerii adreselor.]

---

### Q16. `Multiple Choice`
**Protocol for IPv4 to MAC Resolution / Protocolul pentru rezoluția IPv4 în MAC**

> A host on a local network segment needs to discover the MAC address associated with a known IPv4 address. Which protocol accomplishes this? [O gazdă dintr-un segment de rețea locală trebuie să descopere adresa MAC asociată unei adrese IPv4 cunoscute. Ce protocol realizează acest lucru?]

- **a)  NDP**
- **b)  ICMP**
- **c)  DHCP**
- **d)  ARP**

> 💡 **Feedback:** ARP (Address Resolution Protocol) broadcasts a request on the local segment and receives a unicast reply containing the target's MAC address. A common misconception is confusing ARP with NDP; ARP operates exclusively in IPv4 networks, while NDP is the IPv6 equivalent that uses ICMPv6 Neighbour Solicitation messages instead of broadcast frames. [ARP (Address Resolution Protocol) difuzează (broadcast) o cerere pe segmentul local și primește un răspuns unicast conținând adresa MAC a țintei. O concepție greșită frecventă este confuzia dintre ARP și NDP; ARP funcționează exclusiv în rețele IPv4, în timp ce NDP este echivalentul IPv6 care utilizează mesaje ICMPv6 Neighbour Solicitation în loc de cadre broadcast.]

---

### Q17. `Multiple Choice`
**DHCP Handshake Steps / Pașii handshake-ului DHCP**

> The DHCP protocol follows a four-step process commonly abbreviated as DORA. What do these four letters represent? [Protocolul DHCP urmează un proces în patru pași, abreviat de obicei ca DORA. Ce reprezintă aceste patru litere?]

- **a)  Dynamic, Obtain, Renew, Assign [Dynamic, Obtain, Renew, Assign]**
- **b)  Data, Operation, Request, Acknowledge (DORA) [Data, Operation, Request, Acknowledge]**
- **c)  Discover, Offer, Request, Acknowledge [Discover, Offer, Request, Acknowledge (DORA)]**
- **d)  Destination, Origin, Route, Address [Destination, Origin, Route, Address]**

> 💡 **Feedback:** DORA stands for Discover, Offer, Request, Acknowledge — the four-step handshake by which a client obtains IP configuration from a DHCP server. A common misconception is omitting the Request step, assuming the client simply accepts the first Offer; the Request is essential because multiple DHCP servers may respond with Offers, and the client must explicitly select one. [DORA înseamnă Discover, Offer, Request, Acknowledge — handshake-ul în patru pași prin care un client obține configurația IP de la un server DHCP. O concepție greșită frecventă este omiterea pasului Request, presupunând că clientul acceptă pur și simplu primul Offer; Request este esențial deoarece mai multe servere DHCP pot răspunde cu Offers, iar clientul trebuie să selecteze explicit unul.]

---

### Q18. `Multiple Choice`
**NDP as IPv6 Replacement for ARP / NDP ca înlocuitor IPv6 pentru ARP**

> In IPv6 networks, which protocol replaces ARP for resolving network-layer addresses to link-layer addresses, and additionally provides features such as Router Discovery and SLAAC? [În rețelele IPv6, ce protocol înlocuiește ARP pentru rezoluția adreselor de la nivelul de rețea în adrese de la nivelul legăturii de date, oferind în plus funcționalități precum Router Discovery și SLAAC?]

- **a)  DHCPv6**
- **b)  ICMPv6 Echo**
- **c)  ARP version 6 with extended 128-bit address resolution [ARP versiunea 6 cu rezoluție de adrese extinse pe 128 biți]**
- **d)  NDP (Neighbour Discovery Protocol) [NDP (Neighbour Discovery Protocol)]**

> 💡 **Feedback:** NDP (Neighbour Discovery Protocol) is IPv6's replacement for ARP, providing neighbour resolution, router discovery, prefix discovery, SLAAC, and duplicate address detection. A common misconception is assuming an "ARP version 6" exists; NDP is an entirely different protocol built on ICMPv6, not an extension of ARP. [NDP (Neighbour Discovery Protocol) este înlocuitorul IPv6 pentru ARP, oferind rezoluția vecinilor, descoperirea ruterelor, descoperirea prefixelor, SLAAC și detectarea adreselor duplicate. O concepție greșită frecventă este presupunerea că există un „ARP versiunea 6"; NDP este un protocol complet diferit construit pe ICMPv6, nu o extensie a ARP.]

---

### Q19. `Multiple Choice`
**ICMP Message Types for Ping / Tipurile de mesaje ICMP pentru Ping**

> Which ICMP type and code pair represents an Echo Request, commonly used by the ping utility? [Ce pereche tip și cod ICMP reprezintă un Echo Request, utilizat frecvent de utilitarul ping ?]

- **a)  Type 8, Code 0 [Tipul 8, Codul 0]**
- **b)  Type 0, Code 0 [Tipul 0, Codul 0]**
- **c)  Type 11, Code 0 [Tipul 11, Codul 0]**
- **d)  Type 3, Code 0 [Tipul 3, Codul 0]**

> 💡 **Feedback:** ICMP Echo Request is type 8, code 0. The corresponding Echo Reply is type 0, code 0. A common misconception is reversing the two: students often believe type 0 is the request because it is the lower number, but type 0 is actually the reply. [ICMP Echo Request este tipul 8, codul 0. Echo Reply corespunzător este tipul 0, codul 0. O concepție greșită frecventă este inversarea celor două: studenții cred adesea că tipul 0 este cererea deoarece este numărul mai mic, dar tipul 0 este de fapt răspunsul.]

---

### Q20. `True / False`
**ARP Reply is Unicast / Răspunsul ARP este unicast**

> In the ARP resolution process, the ARP Request is broadcast to all hosts on the segment, while the ARP Reply is sent as a unicast directly to the requesting host. [În procesul de rezoluție ARP, cererea ARP este difuzată (broadcast) către toate gazdele din segment, în timp ce răspunsul ARP este trimis unicast direct către gazda care a inițiat cererea.]

- **a)  true**
- **b)  false**

> 💡 **Feedback:** ARP Requests are broadcast (destination MAC ff:ff:ff:ff:ff:ff) so all hosts receive them, but the ARP Reply is unicast back only to the host that initiated the request. A common misconception is that ARP replies are also broadcast; this would generate unnecessary traffic on the segment. Note that ARP has no authentication mechanism, making it vulnerable to spoofing (falsificare) attacks. [Cererile ARP sunt difuzate (broadcast, cu MAC destinație ff:ff:ff:ff:ff:ff) astfel încât toate gazdele le primesc, dar răspunsul ARP este trimis unicast doar către gazda care a inițiat cererea. O concepție greșită frecventă este că răspunsurile ARP sunt și ele difuzate; acest lucru ar genera trafic inutil pe segment. De remarcat că ARP nu dispune de un mecanism de autentificare, ceea ce îl face vulnerabil la atacuri de spoofing (falsificare).]

---

### Q21. `Multiple Choice`
**When Packet-In Messages Are Sent / Când se trimit mesajele Packet-In**

> Under what condition does an OpenFlow switch send a Packet-In message to the SDN controller? [În ce condiție un comutator OpenFlow trimite un mesaj Packet-In către controlerul SDN?]

- **a)  When the switch runs out of flow table memory and cannot allocate new entries for incoming packets [Când comutatorul rămâne fără memorie pentru tabela de fluxuri și nu poate aloca intrări noi]**
- **b)  When a packet does not match any existing flow rule (table-miss) [Când un pachet nu corespunde niciunei reguli de flux existente (table-miss)]**
- **c)  Only for TCP packets [Doar pentru pachete TCP]**
- **d)  For every packet that passes through the switch [Pentru fiecare pachet care trece prin comutator]**

> 💡 **Feedback:** A Packet-In is triggered when a packet matches no existing flow rule (table-miss). The controller then decides what action to take and may install a new flow rule (reactive flow installation). A common misconception is that the controller processes every packet; if this were the case, SDN would be prohibitively slow — the controller only intervenes when no matching rule exists. [Un Packet-In este declanșat când un pachet nu corespunde niciunei reguli de flux existente (table-miss). Controlerul decide apoi ce acțiune să întreprindă și poate instala o nouă regulă de flux (instalare reactivă de flux). O concepție greșită frecventă este că controlerul procesează fiecare pachet; dacă ar fi așa, SDN ar fi prohibitiv de lent — controlerul intervine doar când nu există nicio regulă care să corespundă.]

---

### Q22. `Multiple Choice`
**OpenFlow Message for Installing Flow Rules / Mesajul OpenFlow pentru instalarea regulilor de flux**

> Which OpenFlow message type does the SDN controller send to a switch to install, modify, or delete flow entries? [Ce tip de mesaj OpenFlow trimite controlerul SDN unui comutator pentru a instala, modifica sau șterge intrări de flux?]

- **a)  Packet-In**
- **b)  Stats-Reply**
- **c)  Packet-Out**
- **d)  Flow-Mod**

> 💡 **Feedback:** Flow-Mod (OFPT_FLOW_MOD) is the message the controller sends to add, modify, or delete flow entries in a switch's flow table. A common misconception is confusing Packet-In (switch-to-controller notification) with Flow-Mod (controller-to-switch command); the direction of communication is opposite. [Flow-Mod (OFPT_FLOW_MOD) este mesajul pe care controlerul îl trimite pentru a adăuga, modifica sau șterge intrări de flux în tabela de fluxuri a comutatorului. O concepție greșită frecventă este confuzia dintre Packet-In (notificare de la comutator la controler) și Flow-Mod (comandă de la controler la comutator); direcția comunicării este opusă.]

---

### Q23. `True / False`
**OpenFlow Priority Semantics / Semantica priorităților OpenFlow**

> In OpenFlow, a flow rule with priority 300 takes precedence over a flow rule with priority 30, because higher numerical values indicate greater importance in the flow matching process. [În OpenFlow, o regulă de flux cu prioritatea 300 are precedență față de o regulă cu prioritatea 30, deoarece valorile numerice mai mari indică o importanță mai mare în procesul de potrivire a fluxurilor.]

- **a)  true**
- **b)  false**

> 💡 **Feedback:** OpenFlow uses a numerical priority system where higher numbers indicate higher importance. Priority 300 takes precedence over priority 30. The maximum is 65535, and 0 is reserved for the table-miss rule (lowest possible). This is the opposite of everyday language where "Priority 1" typically means most important. [OpenFlow folosește un sistem numeric de priorități în care numerele mai mari indică importanță mai mare. Prioritatea 300 are precedență față de prioritatea 30. Maximul este 65535, iar 0 este rezervat regulii table-miss (cea mai scăzută posibilă). Aceasta este opusul limbajului curent unde „Prioritatea 1" înseamnă de obicei cea mai importantă.]

---

### Q24. `Multiple Choice`
**Core Architectural Difference of SDN / Diferența arhitecturală fundamentală a SDN**

> What is the fundamental architectural innovation that distinguishes Software-Defined Networking from traditional networking? [Care este inovația arhitecturală fundamentală care distinge rețelele definite prin software (SDN) de rețelele tradiționale?]

- **a)  Use of faster hardware for packet forwarding [Utilizarea unui hardware mai rapid pentru redirecționarea pachetelor]**
- **b)  Elimination of IP addressing [Eliminarea adresării IP]**
- **c)  Separation of the control plane from the data plane [Separarea planului de control de planul de date]**
- **d)  Encryption of all traffic by default [Criptarea întregului trafic implicit]**

> 💡 **Feedback:** SDN's key innovation is the separation of the control plane (centralised decision-making on a controller) from the data plane (distributed packet forwarding on switches), enabling programmable, centrally-managed network behaviour. A common misconception is equating SDN with a specific protocol such as OpenFlow; SDN is an architectural pattern, and OpenFlow is merely one possible southbound interface. [Inovația cheie a SDN este separarea planului de control (luarea deciziilor centralizat pe un controler) de planul de date (redirecționarea (forwarding) distribuită a pachetelor pe comutatoare), permițând un comportament de rețea programabil și gestionat centralizat. O concepție greșită frecventă este echivalarea SDN cu un protocol specific, precum OpenFlow; SDN este un model arhitectural, iar OpenFlow este doar o posibilă interfață sudică (southbound).]

---

### Q25. `True / False`
**SDN Controller as Packet Forwarder / Controlerul SDN ca echipament de redirecționare a pachetelor**

> In an SDN architecture, every data packet traverses the centralised controller before being forwarded to its destination. [Într-o arhitectură SDN, fiecare pachet de date traversează controlerul centralizat înainte de a fi redirecționat către destinație.]

- **a)  true**
- **b)  false**

> 💡 **Feedback:** The controller only installs rules in switches. The data plane (switches) performs the actual forwarding at line rate. Once a flow rule is installed, matching packets are forwarded directly by the switch without controller involvement. An analogy: the controller is like a GPS navigator — it tells you where to go but does not drive the car. [Controlerul doar instalează reguli în comutatoare. Planul de date (comutatoarele) efectuează redirecționarea (forwarding) efectivă la viteza liniei. Odată ce o regulă de flux este instalată, pachetele corespunzătoare sunt redirecționate direct de comutator fără implicarea controlerului. O analogie: controlerul este ca un navigator GPS — îți spune unde să mergi, dar nu conduce mașina.]

---

### Q26. `Multiple Choice`
**Southbound Interface in SDN / Interfața sudică (southbound) în SDN**

> In SDN architecture, what is the "southbound interface"? [În arhitectura SDN, ce este „interfața sudică" (southbound interface)?]

- **a)  The management console used to configure switches and monitor forwarding tables remotely [Consola de management utilizată pentru configurarea comutatoarelor și monitorizarea tabelelor de dirijare]**
- **b)  The physical cable connecting switches to the controller [Cablul fizic care conectează comutatoarele la controler]**
- **c)  The API between the controller and network applications [API-ul dintre controler și aplicațiile de rețea]**
- **d)  The protocol between the SDN controller and the switches (e.g., OpenFlow) [Protocolul dintre controlerul SDN și comutatoare (de exemplu, OpenFlow)]**

> 💡 **Feedback:** The southbound interface is the protocol used for communication between the SDN controller and the network switches. OpenFlow is the most common example of a southbound interface. A common misconception is confusing the southbound interface with the northbound interface; the northbound interface is the API between the controller and network applications (management software), not the switches. [Interfața sudică (southbound) este protocolul utilizat pentru comunicarea dintre controlerul SDN și comutatoarele de rețea. OpenFlow este cel mai frecvent exemplu de interfață sudică. O concepție greșită frecventă este confuzia dintre interfața sudică și interfața nordică (northbound); interfața nordică este API-ul dintre controler și aplicațiile de rețea (software de management), nu comutatoarele.]

---

### Q27. `True / False`
**OpenFlow Is the Only SDN Protocol / OpenFlow este singurul protocol SDN**

> OpenFlow is the only protocol that can be used for SDN. Without OpenFlow, Software-Defined Networking is impossible. [OpenFlow este singurul protocol care poate fi utilizat pentru SDN. Fără OpenFlow, rețelele definite prin software sunt imposibile.]

- **a)  true**
- **b)  false**

> 💡 **Feedback:** SDN is an architectural pattern (separation of control and data planes), not a specific protocol. Other approaches include P4, NETCONF/YANG, gRPC, and proprietary APIs such as Cisco ACI and VMware NSX. A common misconception is equating "SDN" with "OpenFlow"; understanding SDN as an architecture rather than a protocol is essential when evaluating different networking technologies. [SDN este un model arhitectural (separarea planurilor de control și de date), nu un protocol specific. Alte abordări includ P4, NETCONF/YANG, gRPC și API-uri proprietare precum Cisco ACI și VMware NSX. O concepție greșită frecventă este echivalarea „SDN" cu „OpenFlow"; înțelegerea SDN ca arhitectură, nu ca protocol, este esențială la evaluarea diferitelor tehnologii de rețea.]

---

### Q28. `True / False`
**Volatility of OpenFlow Rules / Volatilitatea regulilor OpenFlow**

> By default, OpenFlow flow rules are stored in the switch's volatile memory, meaning they may be lost when the controller restarts or the connection drops, unless the controller proactively reinstalls them upon reconnection. [Implicit, regulile de flux OpenFlow sunt stocate în memoria volatilă a comutatorului, ceea ce înseamnă că pot fi pierdute când controlerul repornește sau conexiunea se întrerupe, cu excepția cazului în care controlerul le reinstalează proactiv la reconectare.]

- **a)  true**
- **b)  false**

> 💡 **Feedback:** OpenFlow flow rules reside in the switch's volatile memory (typically TCAM or software tables). When the controller restarts, crashes, or the TCP connection between controller and switch drops, existing rules may be lost depending on switch implementation. Robust SDN applications handle this by proactively reinstalling rules upon reconnection. Rules with hard_timeout=0 do not expire automatically but remain volatile across restarts. [Regulile de flux OpenFlow se află în memoria volatilă a comutatorului (de obicei TCAM sau tabele software). Când controlerul repornește, se blochează sau conexiunea TCP se întrerupe, regulile existente pot fi pierdute. Aplicațiile SDN robuste gestionează aceasta reinstalând proactiv regulile la reconectare. Regulile cu hard_timeout=0 nu expiră automat, dar rămân volatile la repornire.]

---

### Q29. `Multiple Choice`
**SDN Learning Switch — Flood vs Unicast Decision / Comutatorul cu învățare SDN — decizia flood vs unicast**

> In an SDN learning switch controller, when a packet-in event arrives and the destination MAC address is not in the controller's MAC-to-port table, what action does the controller instruct the switch to take? [Într-un controler SDN de tip comutator cu învățare, când un eveniment packet-in sosește și adresa MAC destinație nu se află în tabela MAC-port a controlerului, ce acțiune instruiește controlerul comutatorul să efectueze?]

- **a)  Flood the packet to all ports except the ingress port [Difuzează (flood) pachetul pe toate porturile cu excepția portului de intrare]**
- **b)  Drop the packet silently [Elimină pachetul în tăcere]**
- **c)  Send the packet back to the source host [Trimite pachetul înapoi către gazda sursă]**
- **d)  Buffer the packet until the destination is manually registered [Stochează pachetul în buffer până când destinația este înregistrată manual]**

> 💡 **Feedback:** When the destination MAC is unknown, the controller instructs the switch to flood the packet out all ports (except the ingress port). Once the destination host responds, the controller learns its MAC-port mapping for future unicast forwarding. A common misconception is that the switch drops unknown-destination packets; flooding ensures discovery of previously unseen hosts, mirroring the behaviour of a traditional learning switch. [Când MAC-ul destinație este necunoscut, controlerul instruiește comutatorul să difuzeze (flood) pachetul pe toate porturile (cu excepția portului de intrare). Odată ce gazda destinație răspunde, controlerul învață maparea MAC-port pentru redirecționarea viitoare unicast. O concepție greșită frecventă este că comutatorul elimină pachetele cu destinație necunoscută; difuzarea (flooding) asigură descoperirea gazdelor necunoscute anterior, reproducând comportamentul unui comutator tradițional cu învățare.]

---

### Q30. `Multiple Choice`
**SDN Controller Single Point of Failure / Controlerul SDN ca punct unic de eșec**

> Which of the following is a key failure domain trade-off of SDN compared to traditional distributed networking? [Care dintre următoarele este un compromis cheie al domeniului de eșec al SDN comparativ cu rețelele distribuite tradiționale?]

- **a)  The centralised controller is a single point of failure; if it fails, no new flows can be installed [Controlerul centralizat este un punct unic de eșec; dacă acesta eșuează, nu pot fi instalate fluxuri noi]**
- **b)  SDN has no single point of failure because switches are distributed [SDN nu are punct unic de eșec deoarece comutatoarele sunt distribuite]**
- **c)  Traditional networks converge faster than SDN after a failure [Rețelele tradiționale converg mai rapid decât SDN după un eșec]**
- **d)  If the controller fails, all existing flows stop working immediately because switches cannot forward without real-time instructions [Dacă controlerul eșuează, toate fluxurile existente încetează să funcționeze imediat deoarece comutatoarele nu pot direcționa fără instrucțiuni în timp real]**

> 💡 **Feedback:** The centralised controller is a single point of failure (SPOF). If it goes down, no new flows can be installed, although existing flows continue to work because the data plane operates independently. Controller redundancy is a common mitigation. A common misconception is that all traffic stops when the controller fails; existing flow rules remain in switch memory and continue forwarding — only new, unmatched flows are affected. [Controlerul centralizat este un punct unic de eșec (SPOF). Dacă acesta se oprește, nu pot fi instalate fluxuri noi, deși fluxurile existente continuă să funcționeze deoarece planul de date operează independent. Redundanța controlerului este o măsură de atenuare frecventă. O concepție greșită frecventă este că tot traficul se oprește când controlerul eșuează; regulile de flux existente rămân în memoria comutatorului și continuă redirecționarea — doar fluxurile noi, fără corespondență, sunt afectate.]

---

### Q31. `Multiple Choice`
**SDN Scalability Trade-Off / Compromisul de scalabilitate SDN**

> Which of the following represents a scalability advantage of SDN over traditional networking? [Care dintre următoarele reprezintă un avantaj de scalabilitate al SDN față de rețelele tradiționale?]

- **a)  Single point of configuration with consistent policies automatically propagated [Un singur punct de configurare cu politici consistente propagate automat]**
- **b)  Distributed decision-making that scales naturally [Luarea deciziilor distribuit care scalează natural]**
- **c)  No controller latency for first packets of new flows since all decisions are made locally [Fără latență a controlerului pentru primele pachete ale fluxurilor noi deoarece toate deciziile sunt locale]**
- **d)  No single bottleneck for forwarding decisions [Fără punct unic de blocaj pentru deciziile de redirecționare]**

> 💡 **Feedback:** SDN provides a single point of configuration for the entire network, ensuring consistent policies are automatically propagated to all switches, which is a major scalability advantage over per-device configuration in traditional networks. A common misconception is that "no single bottleneck" is an SDN advantage; in fact, distributed decision-making is a characteristic of traditional networking, not SDN. [SDN oferă un singur punct de configurare pentru întreaga rețea, asigurând că politicile consistente sunt propagate automat către toate comutatoarele, ceea ce reprezintă un avantaj major de scalabilitate față de configurarea per-dispozitiv din rețelele tradiționale. O concepție greșită frecventă este că „absența unui punct unic de blocaj" este un avantaj SDN; de fapt, luarea deciziilor distribuit este o caracteristică a rețelelor tradiționale, nu a SDN.]

---

### Q32. `Multiple Choice`
**SDN Controller as Single Point of Failure / Controlerul SDN ca punct unic de eșec**

> In an SDN deployment, the controller fails and cannot be reached by any switches. What is the immediate impact on existing network traffic that already matches installed flow rules? [Într-o implementare SDN, controlerul eșuează și nu poate fi contactat de niciun comutator. Care este impactul imediat asupra traficului de rețea existent care corespunde deja regulilor de flux instalate?]

- **a)  All traffic immediately stops because the controller must approve every packet [Tot traficul se oprește imediat deoarece controlerul trebuie să aprobe fiecare pachet]**
- **b)  All flow rules are immediately deleted from switch memory when the controller disconnects, causing the data plane to stop forwarding any traffic until reconnection occurs [Toate regulile de flux sunt șterse imediat din memoria comutatorului când controlerul se deconectează, determinând planul de date să oprească dirijarea oricărui trafic până la reconectare]**
- **c)  Switches automatically revert to traditional distributed routing protocols like OSPF [Comutatoarele revin automat la protocoale de rutare distribuite tradiționale precum OSPF]**
- **d)  Existing flows continue to work because the data plane forwards independently; only new unmatched flows are affected [Fluxurile existente continuă să funcționeze deoarece planul de date redirecționează independent; doar fluxurile noi fără corespondență sunt afectate]**

> 💡 **Feedback:** The data plane operates independently of the controller. Existing flow rules remain in switch memory and continue to match and forward packets at line rate. However, new flows that trigger a table-miss cannot be installed since the controller is unreachable. A common misconception is that switches automatically revert to traditional routing protocols like OSPF when the controller is lost; OpenFlow switches do not have this fallback capability. [Planul de date operează independent de controler. Regulile de flux existente rămân în memoria comutatorului și continuă să corespundă și să redirecționeze pachetele la viteza liniei. Totuși, fluxurile noi care declanșează un table-miss nu pot fi instalate deoarece controlerul este inaccesibil. O concepție greșită frecventă este că comutatoarele revin automat la protocoale de rutare tradiționale precum OSPF când controlerul se pierde; comutatoarele OpenFlow nu au această capacitate de rezervă (fallback).]

---

### Q33. `Multiple Choice`
**Configuration Complexity — Traditional vs SDN / Complexitatea configurării — tradițional vs SDN**

> An enterprise manages 200 network switches. When comparing traditional networking with SDN, which statement best describes the configuration management trade-off? [O întreprindere administrează 200 de comutatoare de rețea. Comparând rețelele tradiționale cu SDN, care afirmație descrie cel mai bine compromisul în managementul configurării?]

- **a)  SDN requires per-device configuration just like traditional networking, but uses a different protocol [SDN necesită configurare per-dispozitiv la fel ca rețelele tradiționale, dar utilizează un protocol diferit]**
- **b)  Both approaches scale identically because all modern switches support automated provisioning [Ambele abordări scalează identic deoarece toate comutatoarele moderne suportă provizionarea automată]**
- **c)  Traditional networking requires per-device configuration that scales linearly with device count, while SDN centralises configuration at the controller [Rețelele tradiționale necesită configurare per-dispozitiv care scalează liniar cu numărul de dispozitive, în timp ce SDN centralizează configurarea la controler]**
- **d)  Traditional networking is easier to manage at scale because each device makes its own forwarding and routing decisions autonomously without requiring any external coordination point [Rețelele tradiționale sunt mai ușor de administrat la scară mare deoarece fiecare dispozitiv ia propriile decizii de dirijare și rutare autonom fără a necesita vreun punct extern de coordonare]**

> 💡 **Feedback:** In traditional networking, each of the 200 devices must be configured individually via CLI or GUI, and configuration complexity grows linearly with device count. SDN provides a single point of configuration — the controller — which propagates policies uniformly to all switches via OpenFlow. A common misconception is that SDN also requires per-device configuration but with a different protocol; the fundamental advantage is centralisation, not merely a protocol change. [În rețelele tradiționale, fiecare dintre cele 200 de dispozitive trebuie configurat individual prin CLI sau GUI, iar complexitatea configurării crește liniar cu numărul de dispozitive. SDN oferă un singur punct de configurare — controlerul — care propagă politicile uniform către toate comutatoarele prin OpenFlow. O concepție greșită frecventă este că SDN necesită de asemenea configurare per-dispozitiv, dar cu un protocol diferit; avantajul fundamental este centralizarea, nu simpla schimbare a protocolului.]

---

### Q34. `Multiple Choice`
**Recommended Deployment Model for Data Centres / Modelul de implementare recomandat pentru centre de date**

> A cloud service provider needs to manage traffic engineering, multi-tenancy and automated provisioning across thousands of servers. According to the trade-off analysis of traditional vs SDN approaches, which deployment is most suitable? [Un furnizor de servicii cloud trebuie să gestioneze ingineria traficului, multi-tenancy și provizionarea automată pe mii de servere. Conform analizei de compromis între abordările tradiționale și SDN, care implementare este cea mai potrivită?]

- **a)  Traditional networking — it is always preferred for large-scale deployments due to maturity [Rețelele tradiționale — sunt întotdeauna preferate pentru implementări la scară mare datorită maturității]**
- **b)  SDN — it provides traffic engineering, multi-tenancy and automation capabilities essential for data centres [SDN — oferă inginerie de trafic, multi-tenancy și capabilități de automatizare esențiale pentru centrele de date]**
- **c)  Traditional networking — its distributed architecture is more reliable for mission-critical workloads [Rețelele tradiționale — arhitectura distribuită este mai fiabilă pentru sarcinile critice]**
- **d)  Neither — data centres use entirely proprietary protocols that are unrelated to SDN or traditional routing [Niciuna — centrele de date utilizează protocoale complet proprietare care nu au legătură cu SDN sau rutarea tradițională]**

> 💡 **Feedback:** Data centres benefit most from SDN because they require fine-grained traffic engineering, multi-tenancy isolation, and API-driven automation — all core SDN strengths. SDN's programmability allows custom forwarding logic and rapid policy changes without hardware upgrades. A common misconception is that traditional networking is always preferred for large-scale deployments due to maturity; maturity alone does not address the automation and multi-tenancy requirements of modern data centres. [Centrele de date beneficiază cel mai mult de SDN deoarece necesită inginerie de trafic granulară, izolarea multi-tenancy și automatizare bazată pe API — toate punctele forte esențiale ale SDN. Programabilitatea SDN permite logică de redirecționare personalizată și schimbări rapide de politici fără upgrade-uri hardware. O concepție greșită frecventă este că rețelele tradiționale sunt întotdeauna preferate pentru implementările la scară mare datorită maturității; maturitatea singură nu abordează cerințele de automatizare și multi-tenancy ale centrelor de date moderne.]

---

### Q35. `Multiple Choice`
**Primary Purpose of PAT / Scopul principal al PAT**

> What is the primary purpose of Port Address Translation (PAT) in modern networks? [Care este scopul principal al Port Address Translation (PAT) în rețelele moderne?]

- **a)  Encrypt traffic between internal and external networks [Criptează traficul între rețelele interne și cele externe]**
- **b)  Provide comprehensive network security by hiding internal addresses from external threats and inspecting all inbound traffic [Asigură securitate completă a rețelei prin ascunderea adreselor interne față de amenințările externe și inspectarea întregului trafic de intrare]**
- **c)  Allow multiple internal hosts to share a single public IP via port multiplexing [Permite mai multor gazde interne să partajeze o singură adresă IP publică prin multiplexarea porturilor]**
- **d)  Accelerate packet forwarding through hardware offloading [Accelerează dirijarea pachetelor prin descărcare hardware]**

> 💡 **Feedback:** PAT's primary purpose is enabling multiple internal hosts to share a single public IP address by multiplexing through unique port numbers. This directly addresses IPv4 address exhaustion. A common wrong  Encrypting traffic is a function of protocols like TLS, not NAT. [Scopul principal al PAT este de a permite mai multor gazde interne să partajeze o singură adresă IP publică prin multiplexarea cu numere de port unice. Aceasta adresează direct epuizarea adreselor IPv4. Un răspuns greșit frecvent este „asigurarea securității rețelei" — deși NAT blochează conexiunile de intrare nesolicitate ca efect secundar, scopul său este conservarea adreselor, nu securitatea. Criptarea traficului este o funcție a protocoalelor precum TLS, nu a NAT.]

---

### Q36. `Multiple Choice`
**Conntrack Entry Contents / Conținutul unei intrări conntrack**

> A student examines a conntrack entry on a NAT router and sees two tuples. Which statement best describes why two tuples are stored? [Un student examinează o intrare conntrack pe un ruter NAT și vede două tupluri. Care afirmație descrie cel mai bine de ce sunt stocate două tupluri?]

- **a)  To allow two simultaneous connections from the same internal host [Pentru a permite două conexiuni simultane de la aceeași gazdă internă]**
- **b)  To store a backup in case the primary tuple becomes corrupted or lost during high packet-rate conditions [Pentru a stoca o copie de siguranță în cazul în care tuplul primar se corupe sau se pierde în condiții de rată mare de pachete]**
- **c)  To track both TCP and UDP connections separately [Pentru a urmări separat conexiunile TCP și UDP]**
- **d)  To enable bidirectional reverse translation between original and translated addresses [Pentru a permite traducerea inversă bidirecțională între adresele originale și cele traduse]**

> 💡 **Feedback:** Conntrack stores the original tuple (pre-translation) and the reply tuple (post-translation) so the router can perform bidirectional reverse translation. The original tuple records the internal source; the reply tuple records the translated addresses. Without both, return traffic cannot be correctly mapped back. Storing only the translated tuple would prevent the router from knowing which internal host to forward replies to. [Conntrack stochează tuplul original (pre-traducere) și tuplul de răspuns (post-traducere) astfel încât ruterul să poată efectua traducerea inversă bidirecțională. Tuplul original înregistrează sursa internă; tuplul de răspuns înregistrează adresele traduse. Fără ambele, traficul de retur nu poate fi mapat corect. Stocarea doar a tuplului tradus ar împiedica ruterul să știe cărei gazde interne să dirijeze răspunsurile.]

---

### Q37. `Multiple Choice`
**SDN Controller vs Switch Roles / Rolurile controlerului SDN vs comutatorului**

> In an SDN deployment, 1000 packets matching an already-installed flow rule pass through switch S1. How many of these packets does the SDN controller process? [Într-un deployment SDN, 1000 de pachete care corespund unei reguli de flux deja instalate trec prin comutatorul S1. Câte dintre aceste pachete procesează controlerul SDN?]

- **a)  500 — the controller samples half the traffic using a statistical round-robin method [500 — controlerul eșantionează jumătate din trafic utilizând o metodă statistică round-robin]**
- **b)  0 — the switch forwards all matching packets independently [0 — comutatorul dirijează toate pachetele corespunzătoare independent]**
- **c)  1 — the controller processes only the first packet [1 — controlerul procesează doar primul pachet]**
- **d)  1000 — the controller processes every packet [1000 — controlerul procesează fiecare pachet]**

> 💡 **Feedback:** Once a flow rule is installed, the switch forwards matching packets at line rate without involving the controller. The controller is only contacted during table-miss events (when no rule matches). This is what makes SDN scalable — the data plane operates independently. A common misconception is that every packet passes through the controller, which would make SDN extremely slow. [Odată ce o regulă de flux este instalată, comutatorul dirijează pachetele corespunzătoare la viteză de linie fără a implica controlerul. Controlerul este contactat doar în timpul evenimentelor table-miss (când nicio regulă nu corespunde). Aceasta este ceea ce face SDN scalabil — planul de date funcționează independent. O concepție greșită frecventă este că fiecare pachet trece prin controler, ceea ce ar face SDN extrem de lent.]

---

### Q38. `Multiple Choice`
**OpenFlow Priority Semantics / Semantica priorităților OpenFlow**

> A switch has two conflicting flow rules: Rule A with priority 10 (action: drop) and Rule B with priority 100 (action: output:2). Both match the same incoming packet. Which rule is applied and why? [Un comutator are două reguli de flux conflictuale: Regula A cu prioritatea 10 (acțiune: drop) și Regula B cu prioritatea 100 (acțiune: output:2). Ambele corespund aceluiași pachet primit. Care regulă se aplică și de ce?]

- **a)  Rule A — lower priority number means higher importance [Regula A — un număr de prioritate mai mic înseamnă importanță mai mare]**
- **b)  Rule B — higher priority number (100) takes precedence [Regula B — numărul de prioritate mai mare (100) are prioritate]**
- **c)  Both rules are applied in sequence [Ambele reguli sunt aplicate în secvență]**
- **d)  Rule A — the first installed rule always takes precedence [Regula A — prima regulă instalată are întotdeauna prioritate]**

> 💡 **Feedback:** In OpenFlow, higher priority number means higher importance. Rule B (priority 100) takes precedence over Rule A (priority 10), so the packet is forwarded to port 2. Many students mistakenly assume "priority 1" means "first priority" (most important), but OpenFlow uses the opposite convention. The table-miss rule at priority 0 is the least important. [În OpenFlow, un număr de prioritate mai mare înseamnă o importanță mai mare. Regula B (prioritatea 100) are prioritate față de Regula A (prioritatea 10), deci pachetul este dirijat la portul 2. Mulți studenți presupun greșit că „prioritatea 1" înseamnă „prima prioritate" (cea mai importantă), dar OpenFlow folosește convenția opusă. Regula table-miss la prioritatea 0 este cea mai puțin importantă.]

---

### Q39. `Multiple Choice`
**NAT Impact on End-to-End Connectivity / Impactul NAT asupra conectivității capăt-la-capăt**

> A developer discovers that their peer-to-peer application fails to establish direct connections between two users, both behind separate NAT routers. What is the most likely explanation? [Un dezvoltator descoperă că aplicația sa peer-to-peer nu reușește să stabilească conexiuni directe între doi utilizatori, ambii în spatele unor rutere NAT separate. Care este explicația cea mai probabilă?]

- **a)  Both NAT routers occupy all available ports, leaving none for P2P [Ambele rutere NAT ocupă toate porturile disponibile, nelăsând niciunul pentru P2P]**
- **b)  Neither host can initiate inbound connections without existing conntrack entries [Niciuna dintre gazde nu poate iniția conexiuni de intrare fără intrări conntrack existente]**
- **c)  NAT reduces bandwidth below the threshold needed for P2P connections [NAT reduce lățimea de bandă sub pragul necesar pentru conexiuni P2P]**
- **d)  NAT encrypts the packets at the transport layer, preventing the P2P protocol from reading source addresses [NAT criptează pachetele la nivelul transport, împiedicând protocolul P2P să citească adresele sursă]**

> 💡 **Feedback:** NAT breaks end-to-end connectivity because without an existing conntrack entry, unsolicited inbound packets are dropped. Neither host can initiate a direct connection to the other because both are behind NAT. This is why techniques like STUN, TURN, and ICE were developed for NAT traversal in P2P and VoIP applications. The issue is not about ports being "occupied" or bandwidth — it is fundamentally about the absence of conntrack entries for inbound connections. [NAT întrerupe conectivitatea capăt-la-capăt deoarece fără o intrare conntrack existentă, pachetele de intrare nesolicitate sunt abandonate. Niciuna dintre gazde nu poate iniția o conexiune directă cu cealaltă deoarece ambele sunt în spatele NAT. De aceea au fost dezvoltate tehnici precum STUN, TURN și ICE pentru traversarea NAT în aplicații P2P și VoIP. Problema nu este despre porturi „ocupate" sau lățime de bandă — este fundamental despre absența intrărilor conntrack pentru conexiunile de intrare.]

---

### Q40. `Multiple Choice`
**MASQUERADE Chain Selection / Selectarea lanțului MASQUERADE**

> A student configures NAT with the command: iptables -t nat -A PREROUTING -o eth1 -j MASQUERADE . The NAT does not work. Which statement best explains why? [Un student configurează NAT cu comanda: iptables -t nat -A PREROUTING -o eth1 -j MASQUERADE . NAT-ul nu funcționează. Care afirmație explică cel mai bine de ce?]

- **a)  The command needs the -s flag to specify the source subnet [Comanda necesită fanionul -s pentru a specifica subrețeaua sursă]**
- **b)  The -o flag is invalid in the nat table [Fanionul -o este invalid în tabela nat]**
- **c)  MASQUERADE only works with the filter table in the FORWARD chain, not with the nat table [MASQUERADE funcționează doar cu tabela filter în lanțul FORWARD, nu cu tabela nat]**
- **d)  MASQUERADE requires the POSTROUTING chain; PREROUTING is for destination NAT [MASQUERADE necesită lanțul POSTROUTING; PREROUTING este pentru NAT destinație]**

> 💡 **Feedback:** MASQUERADE (source NAT) must be in the POSTROUTING chain because it translates the source address after the routing decision. PREROUTING is for destination NAT (DNAT), which translates the destination address before the routing decision. The chain name indicates when in the packet processing pipeline the rule is applied. This is one of the most common iptables NAT configuration errors. [MASQUERADE (NAT sursă) trebuie să fie în lanțul POSTROUTING deoarece traduce adresa sursă după decizia de rutare. PREROUTING este pentru NAT destinație (DNAT), care traduce adresa destinație înainte de decizia de rutare. Numele lanțului indică momentul din pipeline-ul de procesare a pachetelor în care se aplică regula. Aceasta este una dintre cele mai frecvente erori de configurare NAT iptables.]

---

### Q41. `Multiple Choice`
**Traditional vs SDN Failure Domains / Domenii de defecțiune tradiționale vs SDN**

> In an SDN deployment, the controller becomes unreachable due to a network failure. What happens to traffic that matches already-installed flow rules? [Într-un deployment SDN, controlerul devine inaccesibil din cauza unei defecțiuni de rețea. Ce se întâmplă cu traficul care corespunde regulilor de flux deja instalate?]

- **a)  All traffic immediately stops because switches depend on the controller [Tot traficul se oprește imediat deoarece comutatoarele depind de controler]**
- **b)  Switches automatically create their own flow rules to compensate [Comutatoarele creează automat propriile reguli de flux pentru a compensa]**
- **c)  Matching traffic continues flowing; only new unmatched flows fail [Traficul corespunzător continuă să circule; doar fluxurile noi fără corespondență eșuează]**
- **d)  All flow rules are automatically deleted when the controller disconnects [Toate regulile de flux sunt șterse automat când controlerul se deconectează]**

> 💡 **Feedback:** Existing flow rules continue to work because the data plane operates independently of the controller. Switches forward matching packets at line rate using rules already in their flow tables. However, new flows that would trigger a table-miss cannot be processed because the controller is unavailable. This is a key trade-off in SDN: the controller is a single point of failure for new flow installation, but the data plane continues independently. [Regulile de flux existente continuă să funcționeze deoarece planul de date operează independent de controler. Comutatoarele dirijează pachetele corespunzătoare la viteză de linie folosind regulile deja din tabelele lor de flux. Cu toate acestea, fluxurile noi care ar declanșa un table-miss nu pot fi procesate deoarece controlerul este indisponibil. Acesta este un compromis cheie în SDN: controlerul este un singur punct de defecțiune pentru instalarea fluxurilor noi, dar planul de date continuă independent.]

---

### Q42. `Multiple Choice`
**SDN Policy Priority Design / Proiectarea priorităților politicii SDN**

> A network administrator wants to: (1) allow SSH to server 10.0.10.2, (2) block all other traffic to 10.0.10.2, and (3) allow all remaining traffic. Which priority assignment correctly implements this policy? [Un administrator de rețea dorește să: (1) permită SSH la serverul 10.0.10.2, (2) blocheze tot celălalt trafic la 10.0.10.2 și (3) permită tot traficul rămas. Care atribuire de priorități implementează corect această politică?]

- **a)  All three rules at priority=100 with installation order determining matching [Toate cele trei reguli la prioritate=100 cu ordinea instalării determinând potrivirea]**
- **b)  SSH allow: priority=100, Block to .12: priority=50, Default allow: priority=10 [Permisiune SSH: prioritate=100, Blocare la .12: prioritate=50, Permisiune implicită: prioritate=10]**
- **c)  Block to .12: priority=100, SSH allow: priority=50, Default allow: priority=10 [Blocare la .12: prioritate=100, Permisiune SSH: prioritate=50, Permisiune implicită: prioritate=10]**
- **d)  Default allow: priority=100, SSH allow: priority=50, Block to .12: priority=10 [Permisiune implicită: prioritate=100, Permisiune SSH: prioritate=50, Blocare la .12: prioritate=10]**

> 💡 **Feedback:** The correct pattern is: specific permit at highest priority (100) > general deny at medium priority (50) > default allow at lowest priority (10). The SSH allow rule must have higher priority than the block rule so it is matched first for SSH packets. If the block rule had the highest priority, even SSH packets would be dropped. [Modelul corect este: permisiune specifică la cea mai mare prioritate (100) > interdicție generală la prioritate medie (50) > permisiune implicită la cea mai mică prioritate (10). Regula de permisiune SSH trebuie să aibă o prioritate mai mare decât regula de blocare pentru a fi potrivită prima pentru pachetele SSH. Dacă regula de blocare ar avea cea mai mare prioritate, chiar și pachetele SSH ar fi abandonate.]

---

### Q43. `Multiple Choice`
**ARP Resolution Process / Procesul de rezoluție ARP**

> Host A needs to send a packet to Host B on the same subnet. Host A's ARP cache has no entry for Host B. Which sequence of events correctly describes what happens? [Gazda A trebuie să trimită un pachet gazdei B pe aceeași subrețea. Cache-ul ARP al gazdei A nu are nicio intrare pentru gazda B. Care secvență de evenimente descrie corect ce se întâmplă?]

- **a)  Host A sends a unicast ARP request directly to Host B; Host B broadcasts the reply to all nodes [Gazda A trimite o cerere ARP unicast direct gazdei B; Gazda B difuzează răspunsul tuturor nodurilor]**
- **b)  Host A queries the DHCP server for Host B's MAC address [Gazda A interoghează serverul DHCP pentru adresa MAC a Gazdei B]**
- **c)  The switch resolves the MAC address on behalf of Host A [Comutatorul rezolvă adresa MAC în numele Gazdei A]**
- **d)  Host A broadcasts an ARP request; Host B sends a unicast ARP reply with its MAC address [Gazda A difuzează o cerere ARP; Gazda B trimite un răspuns ARP unicast cu adresa sa MAC]**

> 💡 **Feedback:** ARP resolution follows a broadcast request / unicast reply pattern. The request is broadcast because the sender does not know the destination's MAC address. The reply is unicast directly to the requester because the destination now knows the sender's MAC from the request frame. A common misconception is that the reply is also broadcast — this would create unnecessary network traffic. [Rezoluția ARP urmează un model cerere difuzată / răspuns unicast. Cererea este difuzată deoarece expeditorul nu cunoaște adresa MAC a destinației. Răspunsul este unicast direct la solicitant deoarece destinația cunoaște acum MAC-ul expeditorului din cadrul cererii. O concepție greșită frecventă este că și răspunsul este difuzat — aceasta ar crea trafic de rețea inutil.]

---

### Q44. `Multiple Choice`
**SDN Architecture Advantage / Avantajul arhitecturii SDN**

> In the context of network management, which statement most accurately describes a key advantage SDN has over traditional networking? [În contextul gestionării rețelei, care afirmație descrie cel mai exact un avantaj cheie al SDN față de rețelele tradiționale?]

- **a)  SDN provides built-in encryption for all network traffic [SDN oferă criptare încorporată pentru tot traficul de rețea]**
- **b)  SDN switches forward packets faster than traditional switches due to hardware-optimised flow table lookups [Comutatoarele SDN dirijează pachetele mai rapid decât comutatoarele tradiționale datorită căutărilor optimizate hardware în tabela de fluxuri]**
- **c)  SDN eliminates the need for routing protocols entirely [SDN elimină complet necesitatea protocoalelor de rutare]**
- **d)  Centralised global network view enables consistent policies and optimal path computation [Viziunea globală centralizată a rețelei permite politici consistente și calculul optim al căilor]**

> 💡 **Feedback:** SDN's centralised controller maintains a global view of the entire network, enabling consistent policy enforcement and optimal path computation. Traditional networking only provides each device with a local view (neighbour information from routing protocols). This global visibility is SDN's primary operational advantage. SDN does not inherently provide faster hardware switching — the data plane hardware is often the same. [Controlerul centralizat SDN menține o viziune globală a întregii rețele, permițând aplicarea consistentă a politicilor și calculul optim al căilor. Rețeaua tradițională oferă fiecărui dispozitiv doar o viziune locală (informații despre vecini de la protocoale de rutare). Această vizibilitate globală este principalul avantaj operațional al SDN. SDN nu oferă în mod inerent comutare hardware mai rapidă — hardware-ul planului de date este adesea același.]

---


## §2.  Laborator / Lab   (16 questions)

### Q45. `Multiple Choice`
**Correct iptables MASQUERADE Command / Comanda iptables MASQUERADE corectă**

> A Linux router has eth0 connected to private network 192.168.10.0/24 and eth1 connected to a public network with a dynamic IP. Which iptables command correctly enables MASQUERADE for outbound traffic? [Un ruter Linux are eth0 conectat la rețeaua privată 192.168.10.0/24 și eth1 conectat la o rețea publică cu IP dinamic. Care comandă iptables activează corect MASQUERADE pentru traficul de ieșire?]

- **a)  iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE**
- **b)  iptables -A FORWARD -o eth1 -j MASQUERADE**
- **c)  iptables -t nat -A POSTROUTING -o eth1 -s 192.168.10.0/24 -j MASQUERADE**
- **d)  iptables -t nat -A PREROUTING -i eth1 -s 192.168.10.0/24 -j MASQUERADE**

> 💡 **Feedback:** MASQUERADE must be placed in the POSTROUTING chain (applied after the routing decision), on the outbound public interface (-o eth1), for traffic from the private subnet. MASQUERADE automatically uses the outgoing interface's current IP. A common misconception is placing MASQUERADE in the PREROUTING chain; PREROUTING handles DNAT (inbound translation), whilst POSTROUTING handles SNAT/MASQUERADE (outbound translation). [MASQUERADE trebuie plasat în lanțul POSTROUTING (aplicat după decizia de rutare), pe interfața publică de ieșire (-o eth1), pentru traficul din subrețeaua privată. MASQUERADE utilizează automat IP-ul curent al interfeței de ieșire. O concepție greșită frecventă este plasarea MASQUERADE în lanțul PREROUTING; PREROUTING gestionează DNAT (traducerea de intrare), în timp ce POSTROUTING gestionează SNAT/MASQUERADE (traducerea de ieșire).]

---

### Q46. `Multiple Choice`
**FORWARD Chain for Return Traffic / Lanțul FORWARD pentru traficul de retur**

> When configuring a Linux NAT router, the FORWARD chain must allow return traffic from the public interface to the private interface. Which iptables rule correctly permits only traffic belonging to already-established connections? [La configurarea unui ruter NAT Linux, lanțul FORWARD trebuie să permită traficul de retur de la interfața publică la interfața privată. Care regulă iptables permite corect doar traficul aparținând conexiunilor deja stabilite?]

- **a)  iptables -t nat -A PREROUTING -i eth1 -p tcp --dport 80 -j REDIRECT --to-port 8080**
- **b)  iptables -A INPUT -i eth1 -j ACCEPT**
- **c)  iptables -A FORWARD -i eth1 -o eth0 -j ACCEPT**
- **d)  iptables -A FORWARD -i eth1 -o eth0 -m state --state ESTABLISHED,RELATED -j ACCEPT**

> 💡 **Feedback:** Using -m state --state ESTABLISHED,RELATED allows only return traffic that corresponds to connections initiated from the private network, rather than permitting all inbound traffic. A common misconception is using a blanket ACCEPT rule without state matching; this would allow ALL inbound traffic to pass through, defeating the purpose of the NAT router as a controlled gateway. [Utilizarea -m state --state ESTABLISHED,RELATED permite doar traficul de retur care corespunde conexiunilor inițiate din rețeaua privată, în loc să permită tot traficul de intrare. O concepție greșită frecventă este utilizarea unei reguli ACCEPT generale fără potrivirea stării; aceasta ar permite TOT traficul de intrare să treacă, anulând scopul ruterului NAT ca poartă de acces controlată.]

---

### Q47. `Multiple Choice`
**MASQUERADE vs Static SNAT / MASQUERADE vs SNAT static**

> In iptables, what advantage does MASQUERADE have over specifying a static SNAT address (--to-source) for outbound NAT? [În iptables, ce avantaj are MASQUERADE față de specificarea unei adrese SNAT statice (--to-source) pentru NAT de ieșire?]

- **a)  MASQUERADE encrypts the translated traffic [MASQUERADE criptează traficul tradus]**
- **b)  MASQUERADE is faster because it skips conntrack [MASQUERADE este mai rapid deoarece sare peste conntrack]**
- **c)  MASQUERADE automatically uses the outgoing interface's current IP, ideal for dynamic addresses [MASQUERADE utilizează automat IP-ul curent al interfeței de ieșire, ideal pentru adrese dinamice]**
- **d)  MASQUERADE provides load balancing across multiple public IPs by distributing outbound connections evenly using round-robin selection [MASQUERADE oferă echilibrarea încărcării pe mai multe IP-uri publice prin distribuirea uniformă a conexiunilor de ieșire folosind selecție round-robin]**

> 💡 **Feedback:** MASQUERADE automatically uses the current IP address of the outbound interface, making it ideal for interfaces with dynamically assigned (DHCP) addresses. Static SNAT requires knowing the address in advance. A common misconception is that MASQUERADE skips conntrack for better performance; MASQUERADE still uses conntrack for state tracking, the only difference is automatic IP address discovery. [MASQUERADE utilizează automat adresa IP curentă a interfeței de ieșire, fiind ideal pentru interfețele cu adrese atribuite dinamic (DHCP). SNAT static necesită cunoașterea adresei în prealabil. O concepție greșită frecventă este că MASQUERADE sare peste conntrack pentru performanță mai bună; MASQUERADE utilizează în continuare conntrack pentru urmărirea stării, singura diferență fiind descoperirea automată a adresei IP.]

---

### Q48. `Multiple Choice`
**Correct ovs-ofctl Command to Add ICMP Flow / Comanda ovs-ofctl corectă pentru adăugarea unui flux ICMP**

> You want to install a flow rule on switch s1 that forwards ICMP traffic from 10.0.10.1 to 10.0.10.2 out port 2, using OpenFlow 1.3 with priority 100. Which command is correct? [Doriți să instalați o regulă de flux pe comutatorul s1 care redirecționează traficul ICMP de la 10.0.10.1 la 10.0.10.2 pe portul 2, folosind OpenFlow 1.3 cu prioritatea 100. Care comandă este corectă?]

- **a)  ovs-vsctl add-flow s1 "priority=100,icmp,actions=output:2"**
- **b)  ovs-ofctl add-flow s1 "priority=100,icmp,nw_src=10.0.10.1,nw_dst=10.0.10.2,actions=output:2,CONTROLLER"**
- **c)  ovs-ofctl -O OpenFlow13 add-flow s1 "priority=100,icmp,nw_src=10.0.10.1,nw_dst=10.0.10.2,actions=output:2"**
- **d)  ovs-ofctl -O OpenFlow13 del-flows s1 "priority=100,icmp"**

> 💡 **Feedback:** The -O OpenFlow13 flag is required to specify the protocol version. The match includes icmp, source and destination IPs, and the action outputs to port 2. A common misconception is confusing ovs-ofctl (flow management) with ovs-vsctl (bridge/port configuration); they serve entirely different purposes. [Flagul -O OpenFlow13 este necesar pentru a specifica versiunea protocolului. Potrivirea include icmp, IP-urile sursă și destinație, iar acțiunea redirecționează către portul 2. O concepție greșită frecventă este confuzia dintre ovs-ofctl (managementul fluxurilor) și ovs-vsctl (configurarea bridge-urilor/porturilor); acestea servesc scopuri complet diferite.]

---

### Q49. `Multiple Choice`
**Interpreting Flow Table Statistics / Interpretarea statisticilor tabelei de fluxuri**

> After running ovs-ofctl -O OpenFlow13 dump-flows s1 , you see the following entry:priority=100,icmp,nw_src=10.0.10.1,nw_dst=10.0.10.2 actions=output:2, n_packets=42, n_bytes=3528What does the n_packets=42 field indicate? [După executarea ovs-ofctl -O OpenFlow13 dump-flows s1 , vedeți următoarea intrare:priority=100,icmp,nw_src=10.0.10.1,nw_dst=10.0.10.2 actions=output:2, n_packets=42, n_bytes=3528Ce indică câmpul n_packets=42 ?]

- **a)  42 packets have matched this flow rule and been forwarded to port 2 [42 de pachete au corespuns acestei reguli de flux și au fost redirecționate pe portul 2]**
- **b)  42 packets have been dropped by this rule [42 de pachete au fost eliminate de această regulă]**
- **c)  The flow rule has been installed for 42 seconds [Regula de flux a fost instalată de 42 de secunde]**
- **d)  42 packets were sent to the controller for this flow because no matching rule was found [42 de pachete au fost trimise către controler pentru acest flux deoarece nu s-a găsit nicio regulă potrivită]**

> 💡 **Feedback:** The n_packets counter records how many packets have matched this specific flow rule since it was installed. Here, 42 ICMP packets from h1 to h2 have been forwarded to port 2. A common misconception is confusing the packet counter with duration or dropped packets; the counter tracks matched packets regardless of the action type. [Contorul n_packets înregistrează câte pachete au corespuns acestei reguli de flux specifice de la instalarea acesteia. Aici, 42 de pachete ICMP de la h1 la h2 au fost redirecționate pe portul 2. O concepție greșită frecventă este confuzia dintre contorul de pachete și durata sau pachetele eliminate; contorul urmărește pachetele corespunzătoare indiferent de tipul acțiunii.]

---

### Q50. `Multiple Choice`
**OpenFlow Version Flag in ovs-ofctl / Flagul versiunii OpenFlow în ovs-ofctl**

> In the Week 6 lab, all ovs-ofctl commands include the flag -O OpenFlow13 . What happens if you omit this flag when adding a flow rule that uses OpenFlow 1.3 match fields? [În laboratorul din săptămâna 6, toate comenzile ovs-ofctl includ flagul -O OpenFlow13 . Ce se întâmplă dacă omiteți acest flag la adăugarea unei reguli de flux care utilizează câmpuri de potrivire OpenFlow 1.3?]

- **a)  The flow rule is installed correctly but with reduced priority [Regula de flux este instalată corect, dar cu prioritate redusă]**
- **b)  The command defaults to an older OpenFlow version, which may not support the required match fields and could fail or behave unexpectedly [Comanda utilizează implicit o versiune OpenFlow mai veche, care poate să nu suporte câmpurile de potrivire necesare și poate eșua sau se poate comporta neașteptat]**
- **c)  The switch ignores the flag entirely because it always uses OpenFlow 1.3 [Comutatorul ignoră complet flagul deoarece utilizează întotdeauna OpenFlow 1.3]**
- **d)  The command automatically detects and uses the highest OpenFlow version supported by the switch through an initial capabilities handshake, ensuring backward compatibility with all installed flow rules [Comanda detectează automat și utilizează cea mai înaltă versiune OpenFlow suportată de comutator printr-un handshake inițial de capabilități, asigurând compatibilitate inversă cu toate regulile de flux instalate]**

> 💡 **Feedback:** The -O OpenFlow13 flag specifies the OpenFlow protocol version. Without it, ovs-ofctl defaults to an older OpenFlow version (typically 1.0), which may not support all match fields and actions available in OpenFlow 1.3. A common misconception is that ovs-ofctl auto-negotiates the highest supported version; it does not — the version must be explicitly specified. [Flagul -O OpenFlow13 specifică versiunea protocolului OpenFlow. Fără acesta, ovs-ofctl utilizează implicit o versiune OpenFlow mai veche (de obicei 1.0), care poate să nu suporte toate câmpurile de potrivire și acțiunile disponibile în OpenFlow 1.3. O concepție greșită frecventă este că ovs-ofctl negociază automat cea mai înaltă versiune suportată; nu o face — versiunea trebuie specificată explicit.]

---

### Q51. `Multiple Choice`
**Priority-Based Flow Matching — ICMP Permitted / Potrivirea fluxurilor bazată pe prioritate — ICMP permis**

> An SDN switch has the following flow rules:priority=10, ip, nw_dst=10.0.10.3, actions=droppriority=100, icmp, nw_src=10.0.10.1, nw_dst=10.0.10.3, actions=output:3What happens when h1 (10.0.10.1) sends an ICMP ping to h3 (10.0.10.3)? [Un comutator SDN are următoarele reguli de flux:priority=10, ip, nw_dst=10.0.10.3, actions=droppriority=100, icmp, nw_src=10.0.10.1, nw_dst=10.0.10.3, actions=output:3Ce se întâmplă când h1 (10.0.10.1) trimite un ping ICMP către h3 (10.0.10.3)?]

- **a)  Forwarded to port 3 — the priority 100 ICMP permit rule wins over the priority 10 drop rule [Redirecționat pe portul 3 — regula de permitere ICMP cu prioritatea 100 câștigă față de regula de eliminare cu prioritatea 10]**
- **b)  Sent to controller due to conflicting rules [Trimis la controler din cauza regulilor conflictuale]**
- **c)  Dropped — priority 10 is higher than priority 100 because OpenFlow uses inverse priority ordering where lower numeric values indicate more specific rules [Eliminat — prioritatea 10 este mai mare decât prioritatea 100 deoarece OpenFlow folosește ordonare inversă a priorităților unde valorile numerice mai mici indică reguli mai specifice]**
- **d)  Dropped — the drop rule was installed first [Eliminat — regula de eliminare a fost instalată prima]**

> 💡 **Feedback:** In OpenFlow, higher priority number means higher importance. The ICMP-specific permit rule at priority 100 takes precedence over the general drop rule at priority 10, so the ping is forwarded to port 3. A common misconception is that installation order determines precedence; only the priority number matters. [In OpenFlow, un număr de prioritate mai mare înseamnă importanță mai mare. Regula de permitere specifică ICMP cu prioritatea 100 are precedență față de regula generală de eliminare cu prioritatea 10, deci ping-ul este redirecționat pe portul 3. O concepție greșită frecventă este că ordinea instalării determină precedența; contează doar numărul de prioritate.]

---

### Q52. `Multiple Choice`
**TCP to Blocked Host Falls Through to Drop Rule / TCP către gazda blocată cade pe regula de eliminare**

> Using the same flow rules as above (priority=10 drop to h3, priority=100 ICMP permit from h1 to h3), what happens when h1 sends a TCP packet to h3 (10.0.10.3)? [Folosind aceleași reguli de flux ca mai sus (priority=10 drop către h3, priority=100 permitere ICMP de la h1 la h3), ce se întâmplă când h1 trimite un pachet TCP către h3 (10.0.10.3)?]

- **a)  Dropped — TCP matches the priority 10 IP-level drop rule, since it does not match the ICMP-specific permit [Eliminat — TCP corespunde regulii de eliminare IP cu prioritatea 10, deoarece nu corespunde permiterii specifice ICMP]**
- **b)  Forwarded to port 3 — the priority 100 ICMP permit rule applies to all IP protocols including TCP from h1 to h3 [Redirecționat pe portul 3 — regula de permitere ICMP cu prioritatea 100 se aplică tuturor protocoalelor IP inclusiv TCP de la h1 la h3]**
- **c)  Sent to controller — TCP does not match any rule [Trimis la controler — TCP nu corespunde niciunei reguli]**
- **d)  Error — conflicting rules for the same destination [Eroare — reguli conflictuale pentru aceeași destinație]**

> 💡 **Feedback:** TCP packets match the general "ip, nw_dst=10.0.10.3" rule at priority 10 but do not match the "icmp" rule at priority 100 (since TCP is not ICMP). The drop rule therefore applies. A common misconception is assuming the priority 100 rule allows all traffic from h1 to h3; it specifically matches only ICMP, not TCP or other protocols. [Pachetele TCP corespund regulii generale „ip, nw_dst=10.0.10.3" cu prioritatea 10, dar nu corespund regulii „icmp" cu prioritatea 100 (deoarece TCP nu este ICMP). Regula de eliminare se aplică, prin urmare. O concepție greșită frecventă este presupunerea că regula cu prioritatea 100 permite tot traficul de la h1 la h3; aceasta corespunde în mod specific doar ICMP, nu TCP sau alte protocoale.]

---

### Q53. `Multiple Choice`
**Table-Miss Packet Handling / Gestionarea pachetelor table-miss**

> A flow table contains rules for h1-h2 ICMP traffic and a drop rule for h3, plus a table-miss rule at priority 0 with action CONTROLLER. A packet from an unknown host 10.0.10.99 arrives at the switch. What happens? [O tabelă de fluxuri conține reguli pentru traficul ICMP h1-h2 și o regulă de eliminare pentru h3, plus o regulă table-miss cu prioritatea 0 și acțiunea CONTROLLER. Un pachet de la o gazdă necunoscută 10.0.10.99 sosește la comutator. Ce se întâmplă?]

- **a)  The packet is silently dropped [Pachetul este eliminat în tăcere]**
- **b)  The switch generates an error message [Comutatorul generează un mesaj de eroare]**
- **c)  The packet is sent to the controller via the table-miss rule (priority 0, action CONTROLLER) [Pachetul este trimis la controler prin regula table-miss (priority 0, acțiunea CONTROLLER)]**
- **d)  The packet is flooded to all ports because unknown destination addresses trigger the default broadcasting behaviour in the OpenFlow pipeline [Pachetul este difuzat pe toate porturile deoarece adresele de destinație necunoscute declanșează comportamentul implicit de difuzare în pipeline-ul OpenFlow]**

> 💡 **Feedback:** The packet from 10.0.10.99 does not match any specific flow rule, so it falls through to the table-miss entry (priority=0) which sends it to the controller for a forwarding decision. A common misconception is that unmatched packets are silently dropped; without a table-miss rule they would be, but the priority=0 CONTROLLER action ensures the controller receives unknown traffic for decision-making. [Pachetul de la 10.0.10.99 nu corespunde niciunei reguli de flux specifice, deci cade pe intrarea table-miss (priority=0) care îl trimite la controler pentru o decizie de redirecționare. O concepție greșită frecventă este că pachetele fără corespondență sunt eliminate în tăcere; fără o regulă table-miss ar fi, dar acțiunea CONTROLLER cu priority=0 asigură că controlerul primește traficul necunoscut pentru luarea deciziilor.]

---

### Q54. `Multiple Choice`
**Matching HTTP Traffic in OpenFlow / Potrivirea traficului HTTP în OpenFlow**

> An SDN switch has: priority=200, tcp, nw_dst=10.0.10.2, tp_dst=80, actions=output:2. What happens when h1 sends an HTTP request (TCP port 80) to h2 (10.0.10.2)? [Un comutator SDN are: priority=200, tcp, nw_dst=10.0.10.2, tp_dst=80, actions=output:2. Ce se întâmplă când h1 trimite o cerere HTTP (portul TCP 80) către h2 (10.0.10.2)?]

- **a)  Dropped — OpenFlow cannot match HTTP traffic [Eliminat — OpenFlow nu poate potrivi traficul HTTP]**
- **b)  Sent to controller — the rule needs to specify "http" as the application protocol name [Trimis la controler — regula trebuie să specifice „http" ca nume de protocol aplicativ]**
- **c)  Forwarded to port 2 — the packet matches tcp, nw_dst=10.0.10.2, tp_dst=80 [Redirecționat pe portul 2 — pachetul corespunde tcp, nw_dst=10.0.10.2, tp_dst=80]**
- **d)  Forwarded to all ports [Redirecționat pe toate porturile]**

> 💡 **Feedback:** OpenFlow matches HTTP by specifying tcp and tp_dst=80 (not by matching the string "http"). The packet matches this rule and is forwarded to port 2. A common misconception is that OpenFlow cannot match HTTP or that the rule must specify the string "http" as the protocol; OpenFlow operates at layers 3-4 and matches transport port numbers, not application-layer protocol names. [OpenFlow potrivește HTTP specificând tcp și tp_dst=80 (nu prin potrivirea șirului „http"). Pachetul corespunde acestei reguli și este redirecționat pe portul 2. O concepție greșită frecventă este că OpenFlow nu poate potrivi HTTP sau că regula trebuie să specifice șirul „http" ca protocol; OpenFlow operează la straturile 3-4 și potrivește numerele de port de transport, nu numele protocoalelor de la nivelul aplicație.]

---

### Q55. `Multiple Choice`
**Priority Ordering for Allow-Specific-Block-General Policy / Ordinea priorităților pentru politica de permitere specifică și blocare generală**

> You need an SDN policy that: (1) allows HTTP (port 80) to server h2 (10.0.10.2), (2) blocks all other traffic to h2, (3) allows all other network traffic. What priority ordering ensures correct behaviour? [Aveți nevoie de o politică SDN care: (1) permite HTTP (portul 80) către serverul h2 (10.0.10.2), (2) blochează tot restul traficului către h2, (3) permite tot restul traficului de rețea. Ce ordine a priorităților asigură comportamentul corect?]

- **a)  Block h2: priority=100, HTTP allow: priority=50, Default allow: priority=10 [Blocare h2: priority=100, Permitere HTTP: priority=50, Permitere implicită: priority=10]**
- **b)  HTTP allow: priority=50, Block h2: priority=100, Default allow: priority=10 [Permitere HTTP: priority=50, Blocare h2: priority=100, Permitere implicită: priority=10]**
- **c)  Default allow: priority=100, Block h2: priority=50, HTTP allow: priority=10 [Permitere implicită: priority=100, Blocare h2: priority=50, Permitere HTTP: priority=10]**
- **d)  HTTP allow: priority=100, Block h2: priority=50, Default allow: priority=10 [Permitere HTTP: priority=100, Blocare h2: priority=50, Permitere implicită: priority=10]**

> 💡 **Feedback:** The pattern is: specific permit (highest priority) > general deny (medium) > default allow (lowest). This ensures the HTTP exception overrides the block, and the block only applies to h2. A common misconception is placing the block rule at the highest priority, which would override all permits including the intended HTTP exception. [Modelul este: permitere specifică (prioritate maximă) > refuz general (medie) > permitere implicită (minimă). Acest lucru asigură că excepția HTTP suprascrie blocarea, iar blocarea se aplică doar lui h2. O concepție greșită frecventă este plasarea regulii de blocare la cea mai mare prioritate, ceea ce ar suprascrie toate permiterile, inclusiv excepția HTTP intenționată.]

---

### Q56. `Multiple Choice`
**Designing SSH-Only Access Policy / Proiectarea politicii de acces exclusiv SSH**

> You must design flow rules to allow only SSH (TCP port 22) from h1 to h2, block all other traffic to h2, and allow everything else. Which set of rules implements this correctly? [Trebuie să proiectați reguli de flux care să permită doar SSH (portul TCP 22) de la h1 la h2, să blocheze tot restul traficului către h2 și să permită tot restul. Care set de reguli implementează acest lucru corect?]

- **a)  priority=50,tcp,nw_dst=10.0.10.2,tp_dst=22,actions=output:2 priority=100,ip,nw_dst=10.0.10.2,actions=drop priority=10,ip,actions=NORMAL,FLOOD,LOCAL**
- **b)  priority=100,tcp,nw_src=10.0.10.1,nw_dst=10.0.10.2,tp_dst=22,actions=output:2 priority=50,ip,nw_dst=10.0.10.2,actions=drop priority=10,ip,actions=NORMAL**
- **c)  priority=100,ip,actions=drop priority=50,tcp,tp_dst=22,actions=output:2 priority=10,ip,actions=NORMAL**
- **d)  priority=10,ip,nw_dst=10.0.10.2,actions=drop priority=10,tcp,tp_dst=22,actions=output:2 priority=10,ip,actions=NORMAL**

> 💡 **Feedback:** The correct pattern places the specific SSH permit at the highest priority (100), the general block for h2 at medium priority (50), and the default allow at the lowest priority (10). A common misconception is assigning all rules the same priority, which creates ambiguous matching; priorities must differ to ensure deterministic behaviour. [Modelul corect plasează permiterea SSH specifică la cea mai mare prioritate (100), blocarea generală pentru h2 la prioritate medie (50) și permiterea implicită la cea mai mică prioritate (10). O concepție greșită frecventă este atribuirea aceleiași priorități tuturor regulilor, ceea ce creează potrivire ambiguă; prioritățile trebuie să difere pentru a asigura un comportament determinist.]

---

### Q57. `Multiple Choice`
**Adding a Temporary Override Rule / Adăugarea unei reguli temporare de suprascriere**

> An existing flow rule blocks all traffic to h3 at priority 30. You need to temporarily allow ICMP from h1 to h3. What priority should the new permit rule have? [O regulă de flux existentă blochează tot traficul către h3 la prioritatea 30. Trebuie să permiteți temporar ICMP de la h1 la h3. Ce prioritate ar trebui să aibă noua regulă de permitere?]

- **a)  Any priority higher than 30 (e.g., 300) [Orice prioritate mai mare decât 30 (de exemplu, 300)]**
- **b)  Priority 10 — lower priority overrides higher [Prioritatea 10 — prioritatea mai mică suprascrie prioritatea mai mare]**
- **c)  Priority 30 — same level allows both rules to coexist [Prioritatea 30 — același nivel permite ambelor reguli să coexiste]**
- **d)  Priority 0 — table-miss priority [Prioritatea 0 — prioritatea table-miss]**

> 💡 **Feedback:** The permit rule must have a higher priority number than the block rule (30) to override it. Any value above 30 works. A common misconception is that priority 0 could override other rules; priority 0 is the lowest possible priority, reserved for the table-miss default action. [Regula de permitere trebuie să aibă un număr de prioritate mai mare decât regula de blocare (30) pentru a o suprascrie. Orice valoare peste 30 funcționează. O concepție greșită frecventă este că prioritatea 0 ar putea suprascrie alte reguli; prioritatea 0 este cea mai mică prioritate posibilă, rezervată acțiunii implicite table-miss.]

---

### Q58. `Multiple Choice`
**SDN Controller Framework Used in Lab / Framework-ul controlerului SDN utilizat în laborator**

> In the Week 6 laboratory, which SDN controller framework is used to implement flow-based policies on the Open vSwitch? [În laboratorul din săptămâna 6, ce framework de controler SDN este utilizat pentru implementarea politicilor bazate pe fluxuri pe Open vSwitch?]

- **a)  OpenDaylight**
- **b)  OS-Ken**
- **c)  Floodlight**
- **d)  ONOS**

> 💡 **Feedback:** The lab uses OS-Ken as the SDN controller framework, communicating with Open vSwitch (OVS) via OpenFlow 1.3 on port 6633. A common misconception is confusing different controller frameworks; OS-Ken, OpenDaylight, ONOS, and Floodlight are distinct SDN controllers with different architectures and use cases. [Laboratorul utilizează OS-Ken ca framework de controler SDN, comunicând cu Open vSwitch (OVS) prin OpenFlow 1.3 pe portul 6633. O concepție greșită frecventă este confuzia dintre diferitele framework-uri de controler; OS-Ken, OpenDaylight, ONOS și Floodlight sunt controlere SDN distincte cu arhitecturi și cazuri de utilizare diferite.]

---

### Q59. `Multiple Choice`
**NAT Topology Lab — Private Subnet Address / Topologia NAT din laborator — adresa subrețelei private**

> In the Week 6 NAT topology, what is the private network subnet used by internal hosts h1 and h2? [În topologia NAT din săptămâna 6, care este subrețeaua privată utilizată de gazdele interne h1 și h2?]

- **a)  172.16.0.0/12**
- **b)  10.0.10.0/24**
- **c)  203.0.113.0/24**
- **d)  192.168.10.0/24**

> 💡 **Feedback:** The NAT topology uses 192.168.10.0/24 as the private network, with h1 at 192.168.10.2 and h2 at 192.168.10.3. A common misconception is confusing the NAT private subnet (192.168.10.0/24) with the SDN topology subnet (10.0.10.0/24); these are separate topologies in the lab with different addressing schemes. [Topologia NAT utilizează 192.168.10.0/24 ca rețea privată, cu h1 la 192.168.10.2 și h2 la 192.168.10.3. O concepție greșită frecventă este confuzia dintre subrețeaua privată NAT (192.168.10.0/24) și subrețeaua topologiei SDN (10.0.10.0/24); acestea sunt topologii separate în laborator cu scheme de adresare diferite.]

---

### Q60. `Multiple Choice`
**SDN Host Access Levels in Lab Topology / Nivelurile de acces ale gazdelor SDN în topologia laboratorului**

> In the Week 6 SDN topology (10.0.10.0/24), three hosts are connected to switch s1. According to the lab's default policy, which host has restricted access — meaning most inbound traffic to it is dropped? [În topologia SDN din săptămâna 6 (10.0.10.0/24), trei gazde sunt conectate la comutatorul s1. Conform politicii implicite a laboratorului, care gazdă are acces restricționat — adică majoritatea traficului de intrare către ea este eliminat?]

- **a)  All three hosts have identical access levels [Toate cele trei gazde au niveluri de acces identice]**
- **b)  h1 (10.0.10.1)**
- **c)  h3 (10.0.10.3)**
- **d)  h2 (10.0.10.2)**

> 💡 **Feedback:** In the SDN topology, h3 (10.0.10.3) has restricted access. The default policy drops IP traffic destined for h3 at priority 50, while h1 (10.0.10.1) has full access and h2 (10.0.10.2) acts as the server. A common misconception is that all three hosts have identical access; the SDN policy explicitly differentiates access levels using priority-based flow rules. [În topologia SDN, h3 (10.0.10.3) are acces restricționat. Politica implicită elimină traficul IP destinat lui h3 la prioritatea 50, în timp ce h1 (10.0.10.1) are acces complet, iar h2 (10.0.10.2) acționează ca server. O concepție greșită frecventă este că toate cele trei gazde au acces identic; politica SDN diferențiază explicit nivelurile de acces folosind reguli de flux bazate pe priorități.]

---


## §3.  Numerical (Răspuns numeric)   (2 questions)

### Q61. `Numerical`
**Approximate Size of IPv4 Address Space / Dimensiunea aproximativă a spațiului de adrese IPv4**

> The IPv4 address space uses 32-bit addresses. How many total addresses does this provide, in billions? (Round to one decimal place.) [Spațiul de adrese IPv4 utilizează adrese pe 32 de biți. Câte adrese oferă în total, exprimate în miliarde? (Rotunjiți la o zecimală.)]

> 🔑 *Hint: Hint: answer format — digits only (no units). If decimals are needed, use '.' as the decimal separator. [Indiciu: format răspuns — doar cifre (fără unități). Dacă sunt necesare zecimale, folosiți '.' ca separator.]*


> 💡 **Feedback:** 2^32 = 4,294,967,296, which is approximately (...) billion addresses. Although this number seems large, it is far smaller than the number of devices connected to the Internet today, which is why NAT became essential. A common misconception is that (...) billion addresses should be sufficient; in practice, address blocks are allocated in contiguous ranges, leading to significant waste. [2^32 = 4.294.967.296, adică aproximativ 4,3 miliarde de adrese. Deși acest număr pare mare, el este cu mult mai mic decât numărul de dispozitive conectate la Internet astăzi, motiv pentru care NAT a devenit esențial. O concepție greșită frecventă este că 4,3 miliarde de adrese ar trebui să fie suficiente; în practică, blocurile de adrese se alocă în intervale contigue, ceea ce generează pierderi semnificative.]

---

### Q62. `Numerical`
**OpenFlow Controller Port in Lab / Portul controlerului OpenFlow în laborator**

> In the Week 6 SDN lab environment, the OS-Ken controller communicates with the Open vSwitch using the legacy OpenFlow port. What is the TCP port number used for this controller-switch communication? [În mediul de laborator SDN din săptămâna 6, controlerul OS-Ken comunică cu Open vSwitch utilizând portul OpenFlow moștenit. Care este numărul portului TCP utilizat pentru comunicarea controler-comutator?]

> 🔑 *Hint: Hint: answer format — digits only (no units). If decimals are needed, use '.' as the decimal separator. [Indiciu: format răspuns — doar cifre (fără unități). Dacă sunt necesare zecimale, folosiți '.' ca separator.]*


> 💡 **Feedback:** The lab uses TCP port (...) for OpenFlow controller-switch communication. This is the legacy OpenFlow port; the IANA-assigned standard port is 6653. A common misconception is confusing the two ports; the lab uses the legacy port (...) for compatibility with the OS-Ken controller framework configuration, not the IANA-standard 6653. [Laboratorul utilizează portul TCP (...) pentru comunicarea controler-comutator OpenFlow. Acesta este portul moștenit OpenFlow; portul standard atribuit de IANA este 6653. O concepție greșită frecventă este confuzia dintre cele două porturi; laboratorul utilizează portul moștenit (...) pentru compatibilitate cu configurația framework-ului controlerului OS-Ken, nu portul standard IANA 6653.]

---


## §4.  Drag and Drop into Text   (7 questions)

### Q63. `Drag and Drop`
**Build the MASQUERADE Command / Construiți comanda MASQUERADE**

```
Drag the tokens to build the correct iptables MASQUERADE command for outbound NAT. [Trageți simbolurile pentru a construi comanda corectă iptables MASQUERADE pentru NAT de ieșire.] iptables -t [[1]] -A [[2]] -o [[3]] -s 192.168.10.0/24 -j MASQUERADE
```

**Available items / Elemente disponibile:**

  `[ nat ]   [ filter ]`

  `[ POSTROUTING ]   [ PREROUTING ]`

  `[ eth1 ]   [ eth0 ]`


> 💡 **Feedback:** The correct command is: iptables -t nat -A POSTROUTING -o eth1 -s 192.168.10.0/24 -j MASQUERADE . The nat table handles address translation. POSTROUTING is used because SNAT occurs after the routing decision. eth1 is the public interface. [Comanda corectă este: iptables -t nat -A POSTROUTING -o eth1 -s 192.168.10.0/24 -j MASQUERADE . Tabela nat gestionează traducerea adreselor. POSTROUTING este utilizat deoarece SNAT are loc după decizia de rutare. eth1 este interfața publică.]

---

### Q64. `Drag and Drop`
**Build the OpenFlow Rule / Construiți regula OpenFlow**

```
Drag the tokens to complete the ovs-ofctl command that blocks ICMP from 10.0.10.1. [Trageți simbolurile pentru a completa comanda ovs-ofctl care blochează ICMP de la 10.0.10.1.] ovs-ofctl -O OpenFlow13 [[1]] s1 "priority=100,[[2]],nw_src=10.0.10.1,actions=[[3]]"
```

**Available items / Elemente disponibile:**

  `[ add-flow ]   [ del-flows ]`

  `[ icmp ]   [ ip ]`

  `[ drop ]   [ output:1 ]`


> 💡 **Feedback:** The correct command uses add-flow to install a new rule, icmp to match ICMP protocol, and drop as the action. Note that del-flows removes rules. The match field is icmp (not ip which matches all IP traffic). [Comanda corectă folosește add-flow pentru a instala o regulă nouă, icmp pentru a corespunde protocolului ICMP și drop ca acțiune. Rețineți că del-flows elimină regulile. Câmpul de potrivire este icmp (nu ip care corespunde întregului trafic IP).]

---

### Q65. `Drag and Drop`
**Conntrack Listing Command / Comanda de listare conntrack / Comanda de listare conntrack**

```
Drag the components to form the command that displays active NAT translation entries on the router. [Trageți componentele pentru a forma comanda care afișează intrările active de traducere NAT pe ruter.] [[1]] [[2]]
```

**Available items / Elemente disponibile:**

  `[ conntrack ]   [ -L ]   [ iptables ]   [ -t ]   [ ovs-ofctl ]   [ dump-flows ]`


> 💡 **Feedback:** The conntrack -L command lists all entries in the connection tracking table, showing active NAT translations with their state and timeout values. [Comanda conntrack -L listează toate intrările din tabela de urmărire a conexiunilor, afișând traducerile NAT active cu starea și valorile de timeout.]

---

### Q66. `Drag and Drop`
**OpenFlow Flow Addition / Adăugare flux OpenFlow / Adăugare flux OpenFlow**

```
Arrange the fragments to install a flow rule on switch s1 that drops all ICMP traffic from host 10.0.10.1 using OpenFlow 1.3. [Aranjați fragmentele pentru a instala o regulă de flux pe comutatorul s1 care blochează tot traficul ICMP de la gazda 10.0.10.1 folosind OpenFlow 1.3.] [[1]] [[2]] [[3]] [[4]] "priority=100,icmp,nw_src=10.0.10.1,actions=[[5]]"
```

**Available items / Elemente disponibile:**

  `[ ovs-ofctl ]   [ -O ]   [ OpenFlow13 ]   [ add-flow ]   [ drop ]   [ s1 ]   [ CONTROLLER ]   [ del-flows ]   [ output:1 ]`


> 💡 **Feedback:** The correct command is: ovs-ofctl -O OpenFlow13 add-flow s1 "priority=100,icmp,nw_src=10.0.10.1,actions=drop". The -O flag specifies the OpenFlow version, and actions=drop silently discards matching packets. [Comanda corectă este: ovs-ofctl -O OpenFlow13 add-flow s1 "priority=100,icmp,nw_src=10.0.10.1,actions=drop". Flagul -O specifică versiunea OpenFlow, iar actions=drop elimină silențios pachetele care corespund.]

---

### Q67. `Drag and Drop`
**MASQUERADE Rule Construction / Construcția regulii MASQUERADE / Construcția regulii MASQUERADE**

```
Drag tokens into the correct positions to construct the iptables command that enables PAT for the 192.168.10.0/24 subnet going out through eth1. [Trageți jetoanele în pozițiile corecte pentru a construi comanda iptables care activează PAT pentru subrețeaua 192.168.10.0/24 prin eth1.] iptables -t [[1]] -A [[2]] -o [[3]] -s 192.168.10.0/24 -j [[4]]
```

**Available items / Elemente disponibile:**

  `[ nat ]   [ POSTROUTING ]   [ eth1 ]   [ MASQUERADE ]   [ filter ]   [ PREROUTING ]   [ eth0 ]   [ DNAT ]   [ SNAT ]`


> 💡 **Feedback:** The MASQUERADE target in the POSTROUTING chain of the nat table rewrites the source address to match the outgoing interface (eth1). The -s flag restricts this to packets from the 192.168.10.0/24 subnet. [Ținta MASQUERADE din lanțul POSTROUTING al tabelei nat rescrie adresa sursă pentru a corespunde interfeței de ieșire (eth1). Flagul -s restricționează acest lucru la pachetele din subrețeaua 192.168.10.0/24.]

---

### Q68. `Drag and Drop`
**DHCP DORA Sequence / Secvența DORA a DHCP / Secvența DORA a DHCP**

```
Place the DHCP message types in the correct order of the DORA process. [Plasați tipurile de mesaje DHCP în ordinea corectă a procesului DORA.]Step 1: [[1]] → Step 2: [[2]] → Step 3: [[3]] → Step 4: [[4]]
```

**Available items / Elemente disponibile:**

  `[ Discover ]   [ Offer ]   [ Request ]   [ Acknowledge ]   [ Release ]   [ Inform ]`


> 💡 **Feedback:** DHCP uses a four-step process: the client broadcasts a Discover, the server responds with an Offer containing an available IP, the client formally Requests that IP, and the server sends an Acknowledge to confirm the lease. [DHCP utilizează un proces în patru pași: clientul difuzează un Discover, serverul răspunde cu un Offer conținând un IP disponibil, clientul solicită formal acel IP prin Request, iar serverul trimite un Acknowledge pentru confirmarea împrumutului.]

---

### Q69. `Drag and Drop`
**Flow Dump Command / Comanda de afișare fluxuri / Comanda de afișare fluxuri**

```
Build the command that displays all flow rules installed on OVS bridge s1 using OpenFlow 1.3 protocol. [Construiți comanda care afișează toate regulile de flux instalate pe bridge-ul OVS s1 folosind protocolul OpenFlow 1.3.] [[1]] [[2]] [[3]] [[4]] [[5]]
```

**Available items / Elemente disponibile:**

  `[ ovs-ofctl ]   [ -O ]   [ OpenFlow13 ]   [ dump-flows ]   [ s1 ]   [ add-flow ]   [ ovs-vsctl ]   [ show ]   [ del-flows ]`


> 💡 **Feedback:** ovs-ofctl -O OpenFlow13 dump-flows s1 displays all entries in the flow table of switch s1, including match criteria, actions, counters, and timeouts. [ovs-ofctl -O OpenFlow13 dump-flows s1 afișează toate intrările din tabela de flux a comutatorului s1, incluzând criteriile de potrivire, acțiunile, contoarele și timeout-urile.]

---


## §5.  Gap Select (Select Missing Words)   (8 questions)

### Q70. `Gap Select`
**SDN Plane Terminology / Terminologia planurilor SDN**

```
In SDN, the [[1]] makes forwarding decisions, while the [[2]] performs actual packet forwarding at line rate. [În SDN, ___ ia deciziile de dirijare, în timp ce ___ efectuează dirijarea efectivă a pachetelor la viteză de linie.]
```

**Options per gap / Opțiuni pentru fiecare spațiu:**

- Gap [[1]]: [ control plane [planul de control] ]   [ data plane [planul de date] ]
- Gap [[2]]: [ data plane [planul de date] ]   [ control plane [planul de control] ]

> 💡 **Feedback:** The control plane (centralised controller) computes paths and installs rules. The data plane (distributed switches) forwards packets based on installed flow rules. A common misconception is that the controller forwards packets directly — it only installs rules. [Planul de control (controlerul centralizat) calculează căile și instalează regulile. Planul de date (comutatoarele distribuite) dirijează pachetele pe baza regulilor de flux instalate. O concepție greșită frecventă este că controlerul dirijează pachetele direct — acesta doar instalează reguli.]

---

### Q71. `Gap Select`
**NAT Security Characteristics / Caracteristicile de securitate NAT**

```
NAT provides [[1]], not true [[2]]. A proper [[3]] with stateful inspection is still necessary for defence in depth. [NAT oferă ___, nu ___ reală. Un ___ adecvat cu inspecție cu stare este în continuare necesar pentru apărare în profunzime.]
```

**Options per gap / Opțiuni pentru fiecare spațiu:**

- Gap [[1]]: [ obscurity [obscuritate] ]   [ security [securitate] ]
- Gap [[2]]: [ security [securitate] ]   [ obscurity [obscuritate] ]
- Gap [[3]]: [ firewall [firewall] ]   [ router [ruter] ]

> 💡 **Feedback:** NAT hides internal IP addresses (obscurity) but does not inspect traffic, block malware, or prevent attacks. A proper firewall provides stateful inspection, application-layer filtering, and security logging. Relying solely on NAT for security is a dangerous misconception. [NAT ascunde adresele IP interne (obscuritate), dar nu inspectează traficul, nu blochează malware-ul și nu previne atacurile. Un firewall adecvat oferă inspecție cu stare, filtrare la nivel de aplicație și jurnal de securitate. A te baza exclusiv pe NAT pentru securitate este o concepție greșită periculoasă.]

---

### Q72. `Gap Select`
**iptables Chain Selection / Selectarea lanțului iptables**

```
For outbound NAT (SNAT/MASQUERADE), use the [[1]] chain. For inbound NAT (DNAT/port forwarding), use the [[2]] chain. Both require the [[3]] table. [Pentru NAT de ieșire (SNAT/MASQUERADE), utilizați lanțul ___. Pentru NAT de intrare (DNAT/port forwarding), utilizați lanțul ___. Ambele necesită tabela ___.]
```

**Options per gap / Opțiuni pentru fiecare spațiu:**

- Gap [[1]]: [ POSTROUTING ]   [ PREROUTING ]
- Gap [[2]]: [ PREROUTING ]   [ POSTROUTING ]
- Gap [[3]]: [ nat ]   [ filter ]

> 💡 **Feedback:** POSTROUTING handles outbound source address translation (after the routing decision). PREROUTING handles inbound destination address translation (before the routing decision). Both must be in the nat table, not the default filter table. [POSTROUTING gestionează traducerea adresei sursă la ieșire (după decizia de rutare). PREROUTING gestionează traducerea adresei destinație la intrare (înainte de decizia de rutare). Ambele trebuie să fie în tabela nat, nu în tabela implicită filter.]

---

### Q73. `Gap Select`
**OpenFlow Flow Entry Structure / Structura intrării de flux OpenFlow / Structura intrării de flux OpenFlow**

```
In an OpenFlow flow table, the [[1]] field determines which packets are affected, the [[2]] field specifies what the switch does with those packets, and the [[3]] field decides which rule takes precedence when multiple entries match. [Într-o tabelă de flux OpenFlow, câmpul ___ determină care pachete sunt afectate, câmpul ___ specifică ce face comutatorul cu acele pachete, iar câmpul ___ decide care regulă are prioritate când mai multe intrări se potrivesc.]
```

**Options per gap / Opțiuni pentru fiecare spațiu:**

- Gap [[1]]: [ match ]   [ actions ]   [ counter ]   [ cookie ]
- Gap [[2]]: [ actions ]   [ match ]   [ priority ]   [ timeout ]
- Gap [[3]]: [ priority ]   [ duration ]   [ cookie ]   [ table ]

> 💡 **Feedback:** A flow entry has three core components: match (criteria for selecting packets), actions (what to do — output, drop, etc.), and priority (precedence among conflicting rules). [O intrare de flux are trei componente de bază: match (criterii de selectare a pachetelor), actions (ce să facă — output, drop, etc.) și priority (precedență între regulile conflictuale).]

---

### Q74. `Gap Select`
**MASQUERADE Operation / Operarea MASQUERADE / Operarea MASQUERADE**

```
The MASQUERADE target operates in the [[1]] chain of the [[2]] table. It dynamically rewrites the [[3]] address of outgoing packets to match the outgoing interface's current IP. [Ținta MASQUERADE operează în lanțul ___ al tabelei ___. Ea rescrie dinamic adresa ___ a pachetelor trimise pentru a corespunde IP-ului curent al interfeței de ieșire.]
```

**Options per gap / Opțiuni pentru fiecare spațiu:**

- Gap [[1]]: [ POSTROUTING ]   [ PREROUTING ]   [ FORWARD ]   [ INPUT ]
- Gap [[2]]: [ nat ]   [ filter ]   [ mangle ]   [ raw ]
- Gap [[3]]: [ source ]   [ destination ]   [ gateway ]   [ broadcast ]

> 💡 **Feedback:** MASQUERADE works in the POSTROUTING chain (after routing decision) of the nat table, rewriting the source IP. Unlike SNAT, it dynamically uses the current interface IP, making it ideal for DHCP-assigned addresses. [MASQUERADE funcționează în lanțul POSTROUTING (după decizia de rutare) al tabelei nat, rescriind IP-ul sursă. Spre deosebire de SNAT, utilizează dinamic IP-ul curent al interfeței, fiind ideal pentru adresele atribuite prin DHCP.]

---

### Q75. `Gap Select`
**Traditional vs SDN Architecture / Arhitectura tradițională vs SDN / Arhitectura tradițională vs SDN**

```
In traditional networking, each device maintains a [[1]] view of the network and uses [[2]] protocols like OSPF for routing. In SDN, the controller has a [[3]] view and pushes rules to switches via the [[4]] interface. [În rețelistica tradițională, fiecare dispozitiv menține o viziune ___ asupra rețelei și folosește protocoale de ___ precum OSPF pentru rutare. În SDN, controlerul are o viziune ___ și transmite reguli comutatoarelor prin interfața ___.]
```

**Options per gap / Opțiuni pentru fiecare spațiu:**

- Gap [[1]]: [ local ]   [ global ]   [ partial ]   [ cached ]
- Gap [[2]]: [ distributed ]   [ centralised ]   [ static ]   [ manual ]
- Gap [[3]]: [ global ]   [ local ]   [ partial ]   [ distributed ]
- Gap [[4]]: [ southbound ]   [ northbound ]   [ eastbound ]   [ management ]

> 💡 **Feedback:** Traditional networking: each device has local knowledge and uses distributed routing protocols. SDN: centralised controller has a global network view and programmes switches via the southbound interface (OpenFlow). [Rețelistica tradițională: fiecare dispozitiv are cunoștințe locale și folosește protocoale de rutare distribuite. SDN: controlerul centralizat are o viziune globală asupra rețelei și programează comutatoarele prin interfața southbound (OpenFlow).]

---

### Q76. `Gap Select`
**ARP Resolution Process / Procesul de rezolvare ARP / Procesul de rezolvare ARP**

```
When host A needs to send a frame to host B on the same subnet, it first checks its [[1]]. If no entry exists, it sends an ARP [[2]] as a [[3]] frame. Host B responds with an ARP [[4]] containing its MAC address. [Când gazda A trebuie să trimită un cadru către gazda B pe aceeași subrețea, verifică mai întâi ___. Dacă nu există nicio intrare, trimite un ARP ___ ca un cadru ___. Gazda B răspunde cu un ARP ___ care conține adresa sa MAC.]
```

**Options per gap / Opțiuni pentru fiecare spațiu:**

- Gap [[1]]: [ ARP cache ]   [ routing table ]   [ DNS cache ]   [ flow table ]
- Gap [[2]]: [ request ]   [ reply ]   [ probe ]   [ announcement ]
- Gap [[3]]: [ broadcast ]   [ unicast ]   [ multicast ]   [ anycast ]
- Gap [[4]]: [ reply ]   [ request ]   [ acknowledgement ]   [ redirect ]

> 💡 **Feedback:** ARP resolves IP→MAC within a LAN. The sender checks its cache first, then broadcasts a request. The target responds with a unicast reply. This is fundamental to L2 communication. [ARP rezolvă IP→MAC în cadrul unei rețele LAN. Expeditorul verifică mai întâi cache-ul, apoi difuzează o cerere. Ținta răspunde cu un răspuns unicast. Acest lucru este fundamental pentru comunicarea la nivelul 2.]

---

### Q77. `Gap Select`
**Conntrack State Lifecycle / Ciclul de viață al stării conntrack / Ciclul de viață al stării conntrack**

```
A new TCP connection through NAT begins in the [[1]] state. After the three-way handshake completes, it transitions to [[2]]. TCP established connections have a default timeout of approximately [[3]]. UDP entries have much shorter timeouts of [[4]]. [O nouă conexiune TCP prin NAT începe în starea ___. După finalizarea strângerii de mână în trei pași, trece în starea ___. Conexiunile TCP stabilite au un timeout implicit de aproximativ ___. Intrările UDP au timeout-uri mult mai scurte de ___.]
```

**Options per gap / Opțiuni pentru fiecare spațiu:**

- Gap [[1]]: [ SYN_SENT ]   [ ESTABLISHED ]   [ NEW ]   [ TIME_WAIT ]
- Gap [[2]]: [ ESTABLISHED ]   [ SYN_SENT ]   [ CLOSE_WAIT ]   [ LISTEN ]
- Gap [[3]]: [ 5 days ]   [ 30 seconds ]   [ 2 minutes ]   [ 1 hour ]
- Gap [[4]]: [ 30 seconds to 2 minutes ]   [ 5 days ]   [ 1 hour ]   [ 24 hours ]

> 💡 **Feedback:** Conntrack tracks connection states: SYN_SENT → ESTABLISHED for TCP. TCP established timeout ≈ 5 days; UDP timeout ≈ 30 sec to 2 min. These timeouts matter for long-lived connections requiring keepalives. [Conntrack urmărește stările conexiunilor: SYN_SENT → ESTABLISHED pentru TCP. Timeout TCP stabilit ≈ 5 zile; timeout UDP ≈ 30 sec până la 2 min. Aceste timeout-uri contează pentru conexiunile de lungă durată care necesită keepalive.]

---
