# Week 01 — Computer Networks
### *Rețele de Calculatoare — Săptămâna 1*

> Practice Questions / Întrebări de practică

---

## 📚 Lecture Questions / Întrebări de curs

### Q1. `N01.C01.Q01` — Layer Where TCP and UDP Operate / Stratul la care operează TCP și UDP

*[Multiple Choice — Alegere multiplă]*

In the TCP/IP model, at which layer do TCP and UDP operate? [În modelul TCP/IP, la ce strat operează TCP și UDP?]

- **a)** Transport Layer [Stratul de transport]
- **b)** Network Layer, which handles IP routing [Stratul de rețea, care se ocupă de rutarea IP]
- **c)** Application Layer [Stratul aplicație]
- **d)** Network Interface Layer [Stratul interfață de rețea]

> 💡 **Feedback:**
> *TCP and UDP are Transport Layer protocols that provide end-to-end communication between processes via port numbers. The Network Layer handles IP addressing and routing, not process-to-process delivery. [TCP și UDP sunt protocoale ale Stratului de transport care asigură comunicarea capăt-la-capăt între procese prin numere de port. Stratul de rețea se ocupă de adresarea IP și rutare, nu de livrarea între procese.]*


---

### Q2. `N01.C01.Q02` — Protocol Used by the ping Command / Protocolul folosit de comanda ping

*[Multiple Choice — Alegere multiplă]*

Which protocol does the ping command rely on to test connectivity between hosts? [Ce protocol folosește comanda ping pentru a testa conectivitatea între gazde?]

- **a)** ICMP, a Network Layer diagnostic protocol [ICMP, un protocol de diagnosticare la Stratul de rețea]
- **b)** TCP, a connection-oriented transport protocol [TCP, un protocol de transport orientat pe conexiune]
- **c)** ARP, which maps IP addresses to MAC addresses [ARP, care asociază adrese IP cu adrese MAC]
- **d)** UDP, a connectionless transport protocol [UDP, un protocol de transport fără conexiune]

> 💡 **Feedback:**
> *The ping command uses ICMP (Internet Control Message Protocol) echo request and echo reply messages. ICMP operates at the Network Layer for diagnostics, not data transport. It has its own protocol number (1) in the IP header. [Comanda ping folosește mesaje ICMP (Internet Control Message Protocol) de tip echo request și echo reply. ICMP operează la Stratul de rețea pentru diagnosticare, nu pentru transportul datelor. Are propriul număr de protocol (1) în antetul IP.]*


---

### Q3. `N01.C01.Q03` — TCP/IP Model Has Four Layers / Modelul TCP/IP are patru straturi

*[True/False — Adevărat/Fals]*

The TCP/IP model defines exactly four layers: Application, Transport, Network, and Network Interface. [Modelul TCP/IP definește exact patru straturi: Aplicație, Transport, Rețea și Interfață de rețea.]

- **a)** True / Adevărat
- **b)** False / Fals

> 💡 **Feedback:**
> *The TCP/IP model is a four-layer architecture: Application (HTTP, DNS), Transport (TCP, UDP), Network (IP, ICMP), and Network Interface (Ethernet, Wi-Fi). This contrasts with the seven-layer OSI model. [Modelul TCP/IP este o arhitectură cu patru straturi: Aplicație (HTTP, DNS), Transport (TCP, UDP), Rețea (IP, ICMP) și Interfață de rețea (Ethernet, Wi-Fi). Acesta contrastează cu modelul OSI cu șapte straturi.]*


---

### Q4. `N01.C01.Q04` — HTTP Operates at the Application Layer / HTTP operează la Stratul aplicație

*[Multiple Choice — Alegere multiplă]*

At which TCP/IP layer does HTTP provide its services to web browsers and servers? [La ce strat TCP/IP oferă HTTP serviciile sale navigatoarelor și serverelor web?]

- **a)** Application Layer, where it defines request-response semantics [Stratul aplicație, unde definește semantica cerere-răspuns]
- **b)** Transport Layer, which provides reliable byte streams [Stratul de transport, care oferă fluxuri fiabile de octeți]
- **c)** Network Layer, where packets are routed across networks [Stratul de rețea, unde pachetele sunt rutate între rețele]
- **d)** Network Interface Layer, which frames data for physical transmission [Stratul interfață de rețea, care încadrează datele pentru transmisie fizică]

> 💡 **Feedback:**
> *HTTP is an Application Layer protocol. It relies on TCP at the Transport Layer for reliable delivery, but HTTP itself defines request-response semantics (GET, POST) at the topmost layer. [HTTP este un protocol al Stratului aplicație. Se bazează pe TCP la Stratul de transport pentru livrare fiabilă, dar HTTP în sine definește semantica cerere-răspuns (GET, POST) la stratul cel mai de sus.]*


---

### Q5. `N01.C01.Q05` — Encapsulation Order in TCP/IP / Ordinea încapsulării în TCP/IP

*[Multiple Choice — Alegere multiplă]*

When a web browser sends an HTTP request, what is the correct encapsulation order from top to bottom? [Când un navigator web trimite o cerere HTTP, care este ordinea corectă de încapsulare de sus în jos?]

- **a)** HTTP message → TCP segment → IP packet → Ethernet frame [mesaj HTTP → segment TCP → pachet IP → cadru Ethernet]
- **b)** Ethernet frame → IP packet → TCP segment → HTTP message [cadru Ethernet → pachet IP → segment TCP → mesaj HTTP]
- **c)** TCP segment → HTTP message → Ethernet frame → IP packet [segment TCP → mesaj HTTP → cadru Ethernet → pachet IP]
- **d)** IP packet → Ethernet frame → HTTP message → TCP segment [pachet IP → cadru Ethernet → mesaj HTTP → segment TCP]

> 💡 **Feedback:**
> *Data flows down the stack: the Application Layer produces the HTTP message, the Transport Layer wraps it in a TCP segment, the Network Layer adds an IP header forming a packet, and the Network Interface Layer frames it for physical delivery. [Datele coboară prin stivă: Stratul aplicație produce mesajul HTTP, Stratul de transport îl încapsulează într-un segment TCP, Stratul de rețea adaugă un antet IP formând un pachet, iar Stratul interfață de rețea îl încadrează pentru livrarea fizică.]*


---

### Q6. `N01.C05.Q01` — What ping Measures / Ce măsoară ping

*[Multiple Choice — Alegere multiplă]*

A student runs ping -c 4 8.8.8.8 and sees an average time of 12 ms. What network metric has been measured? [Un student execută ping -c 4 8.8.8.8 și vede un timp mediu de 12 ms. Ce metrică de rețea a fost măsurată?]

- **a)** Latency (Round-Trip Time) - how long a packet takes to travel to the destination and back [Latență (timp dus-întors) - cât durează un pachet să călătorească la destinație și înapoi]
- **b)** Bandwidth (throughput) - the maximum data transfer rate of the network link [Lățime de bandă (debit) - rata maximă de transfer de date a legăturii de rețea]
- **c)** Packet loss rate - the percentage of transmitted packets that failed to arrive at the destination host [Rata de pierdere a pachetelor - procentul de pachete transmise care nu au ajuns la gazda destinație]

> 💡 **Feedback:**
> *Ping measures latency as Round-Trip Time (RTT) - the time for an ICMP echo request to reach the destination and the echo reply to return. This is not bandwidth (throughput). A satellite link can have high bandwidth but terrible latency. [Ping măsoară latența ca timp dus-întors (RTT) - timpul necesar unei cereri de ecou ICMP să ajungă la destinație și răspunsului de ecou să se întoarcă. Aceasta nu este lățime de bandă (debit). O legătură prin satelit poate avea lățime de bandă mare, dar latență teribilă.]*


---

### Q7. `N01.C06.Q02` — Loopback Traffic Path / Traseul traficului loopback

*[Multiple Choice — Alegere multiplă]*

When you run ping 127.0.0.1, what happens to the ICMP packets at the network interface level? [Când executați ping 127.0.0.1, ce se întâmplă cu pachetele ICMP la nivelul interfeței de rețea?]

- **a)** Packets stay entirely within the kernel via the virtual lo interface and never reach the physical NIC [Pachetele rămân complet în kernel prin interfața virtuală lo și nu ajung niciodată la NIC-ul fizic]
- **b)** Packets are transmitted through eth0 and physically loop back through the network switch [Pachetele sunt transmise prin eth0 și se întorc fizic prin comutatorul de rețea]
- **c)** Packets are encrypted by the kernel before being sent through a dedicated hardware loopback circuit [Pachetele sunt criptate de kernel înainte de a fi trimise printr-un circuit hardware loopback dedicat]

> 💡 **Feedback:**
> *Loopback traffic never leaves the machine. The lo interface is purely virtual - packets are routed internally by the kernel. Running tcpdump -i eth0 while pinging localhost will capture nothing, because the physical NIC is not involved. [Traficul loopback nu părăsește niciodată mașina. Interfața lo este pur virtuală - pachetele sunt rutate intern de kernel. Executarea tcpdump -i eth0 în timp ce se face ping la localhost nu va captura nimic, deoarece NIC-ul fizic nu este implicat.]*


---

### Q8. `N01.T00.Q01` — Scenario - Diagnosing High Latency / Scenariu - Diagnosticarea latenței mari

*[Multiple Choice — Alegere multiplă]*

A systems administrator notices that SSH sessions to a remote server feel sluggish. She runs ping -c 10 remote-server and observes an average RTT of 340 ms. Which conclusion is most supported by this observation? [O administratoare de sistem observă că sesiunile SSH către un server de la distanță sunt lente. Ea execută ping -c 10 remote-server și observă un RTT mediu de 340 ms. Ce concluzie este cel mai bine susținută de această observație?]

- **a)** The round-trip latency to the server is high, consistent with geographic distance or congestion along the path [Latența dus-întors către server este mare, în concordanță cu distanța geografică sau congestia de-a lungul traseului]
- **b)** The bandwidth to the remote server is limited to approximately 340 kilobits per second at this time [Lățimea de bandă către serverul de la distanță este limitată la aproximativ 340 kilobits pe secundă în acest moment]
- **c)** The SSH daemon on the remote server is misconfigured and responding to ICMP with artificial delays [Daemonul SSH de pe serverul de la distanță este configurat greșit și răspunde la ICMP cu întârzieri artificiale]

> 💡 **Feedback:**
> *An average RTT of 340 ms indicates high latency, likely due to geographic distance (satellite) or network congestion. Ping measures RTT only - it says nothing about bandwidth, DNS resolution, or application-level errors. [Un RTT mediu de 340 ms indică latență mare, probabil din cauza distanței geografice (satelit) sau congestiei rețelei. Ping măsoară doar RTT - nu spune nimic despre lățimea de bandă, rezoluția DNS sau erorile la nivel de aplicație.]*


---

### Q9. `N01.T00.Q05` — Scenario - Interpreting Socket States / Scenariu - Interpretarea stărilor socket

*[Multiple Choice — Alegere multiplă]*

A student starts nc -l -p 12345 and runs ss -tln | grep 12345, seeing state LISTEN. Then a client connects and the student runs ss -tn | grep 12345. What change in state should the student expect to see? [Un student pornește nc -l -p 12345 și execută ss -tln | grep 12345, văzând starea LISTEN. Apoi un client se conectează și studentul execută ss -tn | grep 12345. Ce schimbare de stare ar trebui să se aștepte studentul să vadă?]

- **a)** A new ESTABLISHED entry appears for the active connection between client and server [O nouă intrare ESTABLISHED apare pentru conexiunea activă între client și server]
- **b)** The LISTEN state changes to SYN_RECEIVED and remains there until data transfer begins [Starea LISTEN se schimbă în SYN_RECEIVED și rămâne acolo până când începe transferul de date]
- **c)** The socket transitions to CLOSE_WAIT because the server is waiting for the client to send data [Socket-ul trece în CLOSE_WAIT deoarece serverul așteaptă ca clientul să trimită date]

> 💡 **Feedback:**
> *After a client completes the three-way handshake, the connection moves from LISTEN to ESTABLISHED. The LISTEN socket may remain (for additional clients), and a new ESTABLISHED socket appears for the active connection. [După ce un client completează handshake-ul în trei pași, conexiunea trece de la LISTEN la ESTABLISHED. Socket-ul LISTEN poate rămâne (pentru clienți suplimentari), iar un nou socket ESTABLISHED apare pentru conexiunea activă.]*


---

### Q10. `N01.T00.Q08` — Scenario - Persistent Netcat Loop / Scenariu - Buclă netcat persistentă

*[Multiple Choice — Alegere multiplă]*

A student runs nc -l -p 9100, a client connects and sends a message, then disconnects. The student observes that nc also exits. To handle multiple sequential clients without restarting manually, the student should: [Un student execută nc -l -p 9100, un client se conectează și trimite un mesaj, apoi se deconectează. Studentul observă că și nc se oprește. Pentru a gestiona mai mulți clienți secvențiali fără repornire manuală, studentul ar trebui să:]

- **a)** Wrap the command in a shell loop: while true; do nc -l -p 9100; done to automatically restart after each disconnect [Încadrați comanda într-o buclă shell: while true; do nc -l -p 9100; done pentru repornire automată după fiecare deconectare]
- **b)** Add the \--daemon flag: nc \--daemon -l -p 9100 to run netcat as a background service [Adăugați steagul \--daemon: nc \--daemon -l -p 9100 pentru a rula netcat ca serviciu de fundal]
- **c)** Increase the listen backlog: nc -l -p 9100 -q 100 to queue incoming connections automatically, allowing multiple clients to wait for service [Măriți coada de ascultare: nc -l -p 9100 -q 100 pentru a pune automat în coadă conexiunile de intrare, permițând mai multor clienți să aștepte deservierea]

> 💡 **Feedback:**
> *Standard netcat accepts one connection then exits. Wrapping it in while true; do nc -l -p 9100; done automatically restarts the listener after each client disconnects. [Netcat standard acceptă o conexiune, apoi se oprește. Încadrarea sa în while true; do nc -l -p 9100; done repornește automat ascultătorul după deconectarea fiecărui client.]*


---

### Q11. `N01.T00.Q09` — Scenario - Loopback Latency Interpretation / Scenariu - Interpretarea latenței loopback

*[Multiple Choice — Alegere multiplă]*

A student pings 127.0.0.1 and observes RTT values below 0.1 ms. She then pings 8.8.8.8 and sees RTT around 15 ms. What best explains this difference? [O studentă face ping la 127.0.0.1 și observă valori RTT sub 0,1 ms. Apoi face ping la 8.8.8.8 și vede RTT de aproximativ 15 ms. Ce explică cel mai bine această diferență?]

- **a)** Loopback traffic is handled entirely within the kernel without physical network traversal; external ping crosses real network infrastructure [Traficul loopback este gestionat complet în kernel fără traversarea rețelei fizice; ping-ul extern traversează infrastructura reală de rețea]
- **b)** The DNS resolution for 8.8.8.8 adds 14.9 ms of overhead that loopback does not require [Rezoluția DNS pentru 8.8.8.8 adaugă 14,9 ms de cost suplimentar pe care loopback-ul nu îl necesită]
- **c)** The operating system applies a deliberate rate-limit to external ping packets to prevent ICMP flood attacks, whereas loopback is exempt from this throttling policy [Sistemul de operare aplică o limitare deliberată de rată pentru pachetele ping externe pentru a preveni atacurile de tip ICMP flood, în timp ce interfața loopback este exceptată de la această politică de limitare]

> 💡 **Feedback:**
> *Loopback (127.0.0.1) never leaves the machine - the kernel routes it internally with negligible delay. Pinging 8.8.8.8 requires packets to traverse physical links, routers, and the Internet, adding real propagation and queuing delays. [Loopback (127.0.0.1) nu părăsește niciodată mașina - kernelul îl rutează intern cu întârziere neglijabilă. Ping-ul la 8.8.8.8 necesită ca pachetele să traverseze legături fizice, routere și Internetul, adăugând întârzieri reale de propagare și coadă.]*


---

## 🔬 Lab Questions / Întrebări de laborator


---

### Q12. `N01.S01.Q04` — Purpose of ping -n Flag / Scopul steagului ping -n

*[Multiple Choice — Alegere multiplă]*

What does the -n flag do when used with ping on Linux? [Ce face steagul -n când este folosit cu ping pe Linux?]

- **a)** Suppresses DNS resolution so only numeric IP addresses are displayed in the output [Suprimă rezoluția DNS, astfel încât doar adresele IP numerice sunt afișate în ieșire]
- **b)** Sets the number of echo requests to send, replacing the default infinite count [Setează numărul de cereri echo de trimis, înlocuind contorul infinit implicit]
- **c)** Forces IPv6 mode for all ping operations regardless of the target address format [Forțează modul IPv6 pentru toate operațiunile ping indiferent de formatul adresei țintă]

> 💡 **Feedback:**
> *The -n flag suppresses DNS resolution, producing numeric-only output (IP addresses instead of hostnames). This avoids delays caused by DNS lookups and makes output cleaner for scripting. [Steagul -n suprimă rezoluția DNS, producând o ieșire doar numerică (adrese IP în loc de nume de gazdă). Aceasta evită întârzierile cauzate de căutările DNS și face ieșirea mai curată pentru scriptare.]*


---

### Q13. `N01.S02.Q01` — Netcat TCP Server Command / Comandă netcat server TCP

*[Multiple Choice — Alegere multiplă]*

Which command starts a TCP server listening on port 9100 using netcat? [Ce comandă pornește un server TCP care ascultă pe portul 9100 folosind netcat?]

- **a)** nc -l -p 9100 (listen mode on TCP port 9100, awaiting one inbound connection) [nc -l -p 9100 (mod ascultare pe portul TCP 9100)]
- **b)** nc -u -l -p 9100 (this starts a UDP server instead of TCP) [nc -u -l -p 9100 (aceasta pornește un server UDP în loc de TCP)]
- **c)** nc localhost 9100 (this connects as a client, not a server) [nc localhost 9100 (aceasta se conectează ca client, nu ca server)]
- **d)** nc -w 5 -p 9100 (the -w flag sets a timeout, -l is missing) [nc -w 5 -p 9100 (steagul -w setează un timeout, -l lipsește)]

> 💡 **Feedback:**
> *The nc -l -p 9100 command starts netcat in listen mode (-l) on port 9100 (-p 9100). The -u flag would switch to UDP, and -v adds verbose output. [Comanda nc -l -p 9100 pornește netcat în mod ascultare (-l) pe portul 9100 (-p 9100). Steagul -u ar comuta la UDP, iar -v adaugă ieșire detaliată.]*


---

### Q14. `N01.S02.Q05` — Persistent Netcat Server / Server netcat persistent

*[Multiple Choice — Alegere multiplă]*

A student starts nc -l -p 9100 and connects a client. After the client disconnects, the server exits. How can the student keep the server running for multiple clients? [Un student pornește nc -l -p 9100 și conectează un client. După deconectarea clientului, serverul se oprește. Cum poate studentul menține serverul activ pentru mai mulți clienți?]

- **a)** while true; do nc -l -p 9100; done - wrapping in a shell loop restarts the listener [while true; do nc -l -p 9100; done - încadrarea într-o buclă shell repornește ascultătorul]
- **b)** nc -l -p 9100 \--persistent - using a built-in persistence flag [nc -l -p 9100 \--persistent - folosind un steag de persistență încorporat]
- **c)** nc -l -p 9100 -k - the -k flag enables keep-alive but is not available in all netcat implementations [nc -l -p 9100 -k - steagul -k activează menținerea conexiunii dar nu este disponibil în toate implementările netcat]

> 💡 **Feedback:**
> *Wrapping netcat in a while true; do nc -l -p 9100; done loop restarts the listener after each client disconnects. Standard netcat exits after one connection. [Încadrarea netcat într-o buclă while true; do nc -l -p 9100; done repornește ascultătorul după deconectarea fiecărui client. Netcat standard se oprește după o conexiune.]*


---

### Q15. `N01.S03.Q02` — Wireshark Filter for TCP Port 9300 / Filtru Wireshark pentru portul TCP 9300

*[Multiple Choice — Alegere multiplă]*

What Wireshark display filter shows only TCP traffic on port 9300? [Ce filtru de afișare Wireshark arată doar traficul TCP pe portul 9300?]

- **a)** tcp.port == 9300 (valid Wireshark display filter using the dot-separated field name and double-equals) [tcp.port == 9300 (filtru de afișare Wireshark valid)]
- **b)** port 9300 (this is a BPF capture filter, not a Wireshark display filter) [port 9300 (acesta este un filtru de captură BPF, nu un filtru de afișare Wireshark)]
- **c)** tcp.port = 9300 (single equals is invalid syntax in Wireshark display filters) [tcp.port = 9300 (egal simplu este sintaxă invalidă în filtrele de afișare Wireshark)]
- **d)** filter tcp port 9300 (not a valid Wireshark display filter expression) [filter tcp port 9300 (nu este o expresie validă de filtru de afișare Wireshark)]

> 💡 **Feedback:**
> *The display filter tcp.port == 9300 matches packets where either the source or destination TCP port is 9300. This is distinct from BPF capture filters used by tcpdump. [Filtrul de afișare tcp.port == 9300 selectează pachetele unde portul TCP sursă sau destinație este 9300. Acesta este distinct de filtrele de captură BPF folosite de tcpdump.]*


---

### Q16. `N01.S03.Q04` — Wireshark Filter for SYN Packets / Filtru Wireshark pentru pachete SYN

*[Multiple Choice — Alegere multiplă]*

Which Wireshark display filter isolates only the initial SYN packets of new TCP connections (not SYN-ACK)? [Ce filtru de afișare Wireshark izolează doar pachetele SYN inițiale ale noilor conexiuni TCP (nu SYN-ACK)?]

- **a)** tcp.flags.syn == 1 && tcp.flags.ack == 0 [tcp.flags.syn == 1 && tcp.flags.ack == 0]
- **b)** tcp.flags.syn == 1 (also matches SYN-ACK packets from the server) [tcp.flags.syn == 1 (selectează și pachetele SYN-ACK de la server)]
- **c)** tcp.flags.fin == 1 (matches connection teardown, not initiation) [tcp.flags.fin == 1 (selectează deconectarea, nu inițierea conexiunii)]

> 💡 **Feedback:**
> *The filter tcp.flags.syn == 1 && tcp.flags.ack == 0 matches packets where SYN is set but ACK is not, isolating the very first packet of new connections. Using only tcp.flags.syn == 1 also matches SYN-ACK responses. [Filtrul tcp.flags.syn == 1 && tcp.flags.ack == 0 selectează pachetele unde SYN este setat, dar ACK nu este, izolând primul pachet al noilor conexiuni. Folosind doar tcp.flags.syn == 1 se selectează și răspunsurile SYN-ACK.]*
