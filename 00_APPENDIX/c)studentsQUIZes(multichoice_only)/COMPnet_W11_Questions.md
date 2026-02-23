# Week 11 — Computer Networks
### *Rețele de Calculatoare — Săptămâna 11*

> Practice Questions / Întrebări de practică

---

## 📚 Lecture Questions / Întrebări de curs

---

### Q1. `N11.C01.Q01`
**Sequential Cyclic Distribution Algorithm / Algoritmul de distribuție ciclică secvențială**

*Multiple Choice – Alegere multiplă*

> A load balancer distributes requests to three backends following the repeating pattern A → B → C → A → B → C. Identify the distribution algorithm in use. [Un echilibrator de încărcare distribuie cererile către trei servere urmând modelul repetitiv A → B → C → A → B → C. Identificați algoritmul de distribuție utilizat.]

- **a)** IP hash, which maps a client address to a fixed backend deterministically [IP hash, care asociază o adresă de client unui server fix în mod determinist]
- **b)** Least connections, which routes to the backend with fewest active sessions [Least connections, care direcționează către serverul cu cele mai puține sesiuni active]
- **c)** Consistent hashing, which minimises redistribution when backends change [Hashing consistent, care minimizează redistribuția când serverele se modifică]
- **d)** Round-robin [Round-robin]

<details><summary>💡 Feedback</summary>

Round-robin cycles through backends sequentially. It assumes homogeneous capacity and has O(1) selection complexity. Real-world factors such as concurrency and connection timing can produce uneven counts. [Round-robin parcurge serverele secvențial. Presupune capacitate omogenă și are complexitate de selecție O(1). Factori reali precum concurența și sincronizarea conexiunilor pot produce numărări inegale.]

</details>

---

### Q2. `N11.C01.Q02`
**IP Hash Affinity After Backend Pool Change / Afinitatea IP hash după modificarea grupului de servere**

*Multiple Choice – Alegere multiplă*

> IP hash provides session affinity for a load balancer with three backends. After a deployment restart that changes the backend pool, a returning user connects from the same IP. What is the most likely outcome? [IP hash asigură afinitatea sesiunii pentru un echilibrator de încărcare cu trei servere. După o repornire de implementare care modifică grupul de servere, un utilizator revine de la aceeași adresă IP. Care este cel mai probabil rezultat?]

- **a)** Nginx stores IP-to-backend mappings on disk and restores them after each restart [Nginx stochează mapările IP-server pe disc și le restaurează după fiecare repornire]
- **b)** Nginx migrates session state automatically to the newly selected backend server [Nginx migrează automat starea sesiunii către noul server selectat]
- **c)** The session is likely lost because the hash-to-backend mapping changes when the pool composition changes [Sesiunea este probabil pierdută deoarece maparea hash-server se schimbă odată cu modificarea compoziției grupului]
- **d)** The session persists because IP hash is fully deterministic regardless of pool membership and permanently maps each client address to a fixed backend index in the pool [Sesiunea persistă deoarece IP hash este complet determinist indiferent de membrii grupului și mapează permanent fiecare adresă de client la un index fix de server din grup]

<details><summary>💡 Feedback</summary>

IP hash offers affinity but not persistence. Altering the backend pool changes the hash-to-server mapping, so the user may lose their session. The hash function is deterministic only whilst the pool composition remains stable. [IP hash oferă afinitate dar nu persistență. Modificarea grupului de servere schimbă maparea hash-server, astfel încât utilizatorul își poate pierde sesiunea. Funcția hash este deterministă doar cât timp compoziția grupului rămâne stabilă.]

</details>

---

### Q3. `N11.C01.Q03`
**Optimal Algorithm for Heterogeneous Processing Times / Algoritmul optim pentru timpi de procesare eterogeni**

*Multiple Choice – Alegere multiplă*

> An application handles requests with wildly varying durations — some finish in 5 ms, others take 3 seconds. Which algorithm adapts best to this workload pattern? [O aplicație procesează cereri cu durate extrem de variabile — unele se finalizează în 5 ms, altele durează 3 secunde. Care algoritm se adaptează cel mai bine acestui model de sarcină?]

- **a)** Round-robin, because equal rotation handles all workloads effectively [Round-robin, deoarece rotația egală gestionează eficient toate sarcinile]
- **b)** Weighted round-robin, because static weights compensate for processing differences [Round-robin ponderat, deoarece ponderile statice compensează diferențele de procesare]
- **c)** IP hash, because consistent routing reduces latency variance across sessions [IP hash, deoarece rutarea consistentă reduce variația latenței între sesiuni]
- **d)** Least connections, because it considers current backend load when selecting a target [Least connections, deoarece ia în considerare încărcarea curentă a serverului la selecție]

<details><summary>💡 Feedback</summary>

Least connections routes to the backend with fewest active connections, naturally adapting to heterogeneous processing times. Round-robin ignores current load and can overload backends handling slow requests. [Least connections direcționează către serverul cu cele mai puține conexiuni active, adaptându-se natural la timpii de procesare eterogeni. Round-robin ignoră încărcarea curentă și poate supraîncărca serverele care procesează cereri lente.]

</details>

---

### Q4. `N11.C01.Q04`
**Round-Robin Perfect Distribution Claim / Afirmația distribuției perfecte round-robin**

*True/False – Adevărat/Fals*

> A round-robin load balancer with 3 backends always distributes exactly one-third of requests to each backend under real-world production conditions. [Un echilibrator de încărcare round-robin cu 3 servere distribuie întotdeauna exact o treime din cereri către fiecare server în condiții reale de producție.]

- **a)** True / Adevărat
- **b)** False / Fals

<details><summary>💡 Feedback</summary>

Connection timing, concurrency, keep-alive reuse, and backend failures cause deviations from the theoretical equal split. The claim confuses the ideal model with production behaviour. [Sincronizarea conexiunilor, concurența, reutilizarea keep-alive și căderile serverelor cauzează abateri de la împărțirea teoretică egală. Afirmația confundă modelul ideal cu comportamentul de producție.]

</details>

---

### Q5. `N11.C01.Q05`
**L4 vs L7 Load Balancing Decision Basis / Baza deciziei la echilibrarea L4 vs L7**

*Multiple Choice – Alegere multiplă*

> What routing information can a Layer 7 (application) load balancer inspect that is unavailable to a Layer 4 (transport) load balancer? [Ce informații de rutare poate inspecta un echilibrator de încărcare de nivelul 7 (aplicație) care nu sunt disponibile pentru un echilibrator de nivelul 4 (transport)?]

- **a)** Source and destination port numbers from the transport header, combined with protocol flags and sequence numbers for routing decisions [Numerele de port sursă și destinație din antetul de transport, combinate cu fanioanele de protocol și numerele de secvență pentru decizii de rutare]
- **b)** TCP SYN and ACK flag combinations from the segment header [Combinațiile de indicatori TCP SYN și ACK din antetul segmentului]
- **c)** HTTP headers, cookies, and URI paths parsed from the application payload [Antetele HTTP, cookie-urile și căile URI extrase din încărcătura utilă a aplicației]
- **d)** Source IP address and DSCP markings from the network header [Adresa IP sursă și marcajele DSCP din antetul de rețea]

<details><summary>💡 Feedback</summary>

L7 operates at the application layer and can parse HTTP headers, cookies, URI paths, and content. L4 sees only IP addresses, ports, and TCP flags, making content-aware routing impossible at that level. [L7 operează la stratul aplicație și poate analiza antetele HTTP, cookie-urile, căile URI și conținutul. L4 vede doar adresele IP, porturile și indicatorii TCP, făcând rutarea bazată pe conținut imposibilă la acel nivel.]

</details>

---

### Q6. `N11.C02.Q01`
**First Request to Crashed Backend / Prima cerere către un server căzut**

*Multiple Choice – Alegere multiplă*

> Nginx uses default settings with three backends. Backend web2 crashes. A client sends a request that Nginx routes to web2. What does the client receive? [Nginx folosește setările implicite cu trei servere. Serverul web2 se oprește. Un client trimite o cerere pe care Nginx o direcționează către web2. Ce primește clientul?]

- **a)** 200 OK, because Nginx instantly reroutes to a healthy backend before the client notices [200 OK, deoarece Nginx redirecționează instant către un server sănătos înainte ca clientul să observe]
- **b)** 504 Gateway Timeout after waiting for the configurable proxy_read_timeout interval to expire [504 Gateway Timeout după așteptarea expirării intervalului configurabil proxy_read_timeout]
- **c)** 503 Service Unavailable, which Nginx sends immediately upon detecting any failed backend [503 Service Unavailable, pe care Nginx îl trimite imediat la detectarea oricărui server eșuat]
- **d)** 502 Bad Gateway, because Nginx discovers the failure only upon forwarding the actual request [502 Bad Gateway, deoarece Nginx descoperă eșecul doar la redirecționarea cererii reale]

<details><summary>💡 Feedback</summary>

Nginx uses passive health checks by default: it detects failure only when a real request fails. The first request to the dead backend returns 502. After max_fails (default 1), Nginx marks web2 as unhealthy for fail_timeout seconds. [Nginx folosește verificări pasive de sănătate implicit: detectează eșecul doar când o cerere reală eșuează. Prima cerere către serverul căzut returnează 502. După max_fails (implicit 1), Nginx marchează web2 ca nesănătos pentru fail_timeout secunde.]

</details>

---

### Q7. `N11.C02.Q03`
**Meaning of HTTP 502 from Nginx / Semnificația HTTP 502 de la Nginx**

*Multiple Choice – Alegere multiplă*

> An Nginx reverse proxy returns HTTP 502 Bad Gateway. What does this status code indicate about the system state? [Un proxy invers Nginx returnează HTTP 502 Bad Gateway. Ce indică acest cod de stare despre starea sistemului?]

- **a)** The client sent a malformed HTTP request that Nginx cannot parse correctly [Clientul a trimis o cerere HTTP malformată pe care Nginx nu o poate analiza corect]
- **b)** The Nginx process itself has crashed and the operating system is generating the error page [Procesul Nginx s-a prăbușit și sistemul de operare generează pagina de eroare]
- **c)** Nginx is running but the upstream backend is unreachable or returned an invalid response [Nginx funcționează dar serverul din amonte este inaccesibil sau a returnat un răspuns invalid]
- **d)** The Nginx configuration file contains a syntax error discovered at runtime [Fișierul de configurare Nginx conține o eroare de sintaxă descoperită la rulare]

<details><summary>💡 Feedback</summary>

502 means Nginx itself is operational but received an invalid response (or no response) from the upstream backend. It does not indicate an Nginx crash. 503 would mean all backends are unavailable; 504 would mean the backend was too slow. [502 înseamnă că Nginx este operațional dar a primit un răspuns invalid (sau niciun răspuns) de la serverul din amonte. Nu indică o cădere a Nginx. 503 ar însemna că toate serverele sunt indisponibile; 504 ar însemna că serverul a fost prea lent.]

</details>

---

### Q8. `N11.C02.Q04`
**Nginx Instant Backend Failure Detection / Detectarea instantanee a căderilor de servere de Nginx**

*True/False – Adevărat/Fals*

> Nginx with default open-source settings detects backend failures instantly, before any client request reaches the failed backend. [Nginx cu setările implicite open-source detectează căderile serverelor instantaneu, înainte ca vreo cerere a clientului să ajungă la serverul eșuat.]

- **a)** True / Adevărat
- **b)** False / Fals

<details><summary>💡 Feedback</summary>

Default Nginx uses passive health checks: it discovers failure only when a real request fails. Active probing (which could detect failures before client impact) requires Nginx Plus or custom scripting. [Nginx implicit folosește verificări pasive de sănătate: descoperă eșecul doar când o cerere reală eșuează. Sondarea activă (care ar putea detecta căderile înainte de impactul asupra clientului) necesită Nginx Plus sau scripturi personalizate.]

</details>

---

### Q9. `N11.C02.Q05`
**proxy_next_upstream Failover Behaviour / Comportamentul de failover proxy_next_upstream**

*Multiple Choice – Alegere multiplă*

> The Nginx directive proxy_next_upstream error timeout http_502; is configured. Backend web1 returns a 502 error. What does Nginx do next? [Directiva Nginx proxy_next_upstream error timeout http_502; este configurată. Serverul web1 returnează o eroare 502. Ce face Nginx mai departe?]

- **a)** Nginx returns the 502 directly to the client without attempting any retry on other backends [Nginx returnează 502 direct clientului fără a încerca nicio reîncercare pe alte servere]
- **b)** Nginx permanently removes web1 from the pool and requires manual re-addition via reload [Nginx elimină permanent web1 din grup și necesită re-adăugare manuală prin reîncărcare]
- **c)** Nginx transparently retries the request on the next available healthy backend in the upstream pool [Nginx reîncearcă transparent cererea pe următorul server sănătos disponibil din grupul upstream]
- **d)** Nginx queues the request and waits for web1 to recover before forwarding it again [Nginx pune cererea în coadă și așteaptă ca web1 să se recupereze înainte de a o redirecționa din nou]

<details><summary>💡 Feedback</summary>

proxy_next_upstream instructs Nginx to retry the request on the next healthy backend when the specified conditions (error, timeout, http_502) occur. The client may still receive a successful response if another backend is healthy. [proxy_next_upstream instruiește Nginx să reîncerce cererea pe următorul server sănătos când condițiile specificate (error, timeout, http_502) apar. Clientul poate primi totuși un răspuns de succes dacă un alt server este sănătos.]

</details>

---

### Q10. `N11.C03.Q01`
**Nginx proxy_pass Trailing Slash Semantics / Semantica barei oblice finale în proxy_pass Nginx**

*Multiple Choice – Alegere multiplă*

> Consider two Nginx configurations:
A:location /api/ { proxy_pass http://backend; }
B:location /api/ { proxy_pass http://backend/; }
A client requests /api/users. What URI does each backend receive? [Considerați două configurații Nginx:
A:location /api/ { proxy_pass http://backend; }
B:location /api/ { proxy_pass http://backend/; }
Un client solicită /api/users. Ce URI primește fiecare server?]

- **a)** Config A: backend receives /api/users; Config B: backend receives /users (prefix stripped) [Config A: serverul primește /api/users; Config B: serverul primește /users (prefix eliminat)]
- **b)** Config A: backend receives /users; Config B: backend receives /api/users (reversed) [Config A: serverul primește /users; Config B: serverul primește /api/users (inversat)]
- **c)** Both forward /api/users identically to the backend regardless of the trailing slash [Ambele redirecționează /api/users identic către server indiferent de bara oblică finală]
- **d)** Config B causes a 404 error because the trailing slash invalidates the proxy_pass URI [Config B cauzează o eroare 404 deoarece bara oblică finală invalidează URI-ul proxy_pass]

<details><summary>💡 Feedback</summary>

Without a trailing slash, Nginx forwards the full original URI (/api/users). With a trailing slash, Nginx replaces the matched location prefix: /api/users becomes /users. This is one of the most common Nginx misconfiguration pitfalls. [Fără bara oblică finală, Nginx redirecționează URI-ul original complet (/api/users). Cu bara oblică finală, Nginx înlocuiește prefixul locației: /api/users devine /users. Aceasta este una dintre cele mai frecvente capcane de misconfigurare Nginx.]

</details>

---

### Q11. `N11.C03.Q02`
**Purpose of X-Forwarded-For Header / Scopul antetului X-Forwarded-For**

*Multiple Choice – Alegere multiplă*

> A reverse proxy sets proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; before forwarding to the backend. Why is this header necessary? [Un proxy invers setează proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; înainte de redirecționare către server. De ce este necesar acest antet?]

- **a)** It tells the backend which HTTP version to use when constructing the response, overriding the backend default protocol negotiation [Indică serverului ce versiune HTTP să folosească la construirea răspunsului, suprascriind negocierea implicită a protocolului de pe server]
- **b)** It instructs the backend to compress the response body before returning it [Instruiește serverul să comprime corpul răspunsului înainte de a-l returna]
- **c)** It preserves the original client IP address so the backend can identify the true request origin [Păstrează adresa IP originală a clientului astfel încât serverul să poată identifica originea reală a cererii]
- **d)** It encrypts the communication channel between the proxy and the backend server [Criptează canalul de comunicare între proxy și server]

<details><summary>💡 Feedback</summary>

Without X-Forwarded-For, the backend sees only the proxy's IP as the source. This header preserves the original client IP through the proxy chain, essential for logging, rate limiting, and geolocation. [Fără X-Forwarded-For, serverul vede doar IP-ul proxy-ului ca sursă. Acest antet păstrează IP-ul original al clientului prin lanțul de proxy, esențial pentru jurnalizare, limitarea ratei și geolocalizare.]

</details>

---

### Q12. `N11.C03.Q03`
**Weighted Nginx Upstream Traffic Percentage / Procentajul traficului în upstream ponderat Nginx**

*Multiple Choice – Alegere multiplă*

> Given the Nginx configuration:
upstream backend { server web1:80 weight=3; server web2:80 weight=2; server web3:80 weight=1; }
What approximate percentage of traffic does web1 receive? [Având configurația Nginx:
upstream backend { server web1:80 weight=3; server web2:80 weight=2; server web3:80 weight=1; }
Ce procent aproximativ din trafic primește web1?]

- **a)** 33%, because Nginx distributes equally among three servers regardless of weight settings [33%, deoarece Nginx distribuie egal între cele trei servere indiferent de setările de pondere]
- **b)** 30%, because weight=3 directly translates to 30 percent of total traffic distribution [30%, deoarece weight=3 se traduce direct în 30 de procente din distribuția totală a traficului]
- **c)** 60%, because weight=3 means three times the base allocation of 20% per backend [60%, deoarece weight=3 înseamnă de trei ori alocarea de bază de 20% per server]
- **d)** 50%, because weight is relative: 3 out of total 6 yields one half of all requests [50%, deoarece ponderea este relativă: 3 din totalul de 6 produce jumătate din toate cererile]

<details><summary>💡 Feedback</summary>

Weights are relative: total weight = 3+2+1 = 6. web1 receives 3/6 = 50%. A common mistake is treating weight=3 as 30% — weights are ratios, not absolute percentages. [Ponderile sunt relative: ponderea totală = 3+2+1 = 6. web1 primește 3/6 = 50%. O greșeală frecventă este tratarea weight=3 ca 30% — ponderile sunt rapoarte, nu procente absolute.]

</details>

---

### Q13. `N11.C03.Q04`
**Role of X-Real-IP Proxy Header / Rolul antetului proxy X-Real-IP**

*Multiple Choice – Alegere multiplă*

> The lab's nginx.conf includes proxy_set_header X-Real-IP $remote_addr;. How does this header differ from X-Forwarded-For? [Fișierul nginx.conf din laborator include proxy_set_header X-Real-IP $remote_addr;. Cum diferă acest antet de X-Forwarded-For?]

- **a)** X-Real-IP records the backend server address; X-Forwarded-For records the proxy address [X-Real-IP înregistrează adresa serverului; X-Forwarded-For înregistrează adresa proxy-ului]
- **b)** X-Real-IP is encrypted while X-Forwarded-For is transmitted in cleartext by the proxy [X-Real-IP este criptat în timp ce X-Forwarded-For este transmis în text clar de proxy]
- **c)** Both headers serve identical purposes and can be used interchangeably in all configurations [Ambele antete servesc scopuri identice și pot fi folosite interschimbabil în toate configurațiile]
- **d)** X-Real-IP holds a single IP address; X-Forwarded-For accumulates a chain of proxy addresses [X-Real-IP conține o singură adresă IP; X-Forwarded-For acumulează un lanț de adrese proxy]

<details><summary>💡 Feedback</summary>

X-Real-IP contains only the immediate client IP (a single address), while X-Forwarded-For is an append-only chain of all proxies in the path. X-Real-IP is simpler but loses information in multi-proxy setups. [X-Real-IP conține doar IP-ul clientului imediat (o singură adresă), în timp ce X-Forwarded-For este un lanț de adăugare cu toate proxy-urile din cale. X-Real-IP este mai simplu dar pierde informații în configurațiile multi-proxy.]

</details>

---

### Q14. `N11.C04.Q01`
**Default DNS Port Number / Numărul de port DNS implicit**

*Multiple Choice – Alegere multiplă*

> On which port does the Domain Name System primarily operate for standard queries? [Pe ce port operează Sistemul de Nume de Domeniu pentru interogări standard?]

- **a)** Port 25, since DNS queries piggyback on the SMTP mail transport channel [Portul 25, deoarece interogările DNS se transmit pe canalul de transport SMTP]
- **b)** Port 80, shared with HTTP for web-based domain resolution [Portul 80, partajat cu HTTP pentru rezoluția domeniilor bazată pe web]
- **c)** Port 53, used for both UDP queries and TCP zone transfers [Portul 53, folosit atât pentru interogări UDP cât și pentru transferuri de zonă TCP]
- **d)** Port 443, because modern DNS exclusively uses encrypted HTTPS connections [Portul 443, deoarece DNS modern folosește exclusiv conexiuni HTTPS criptate]

<details><summary>💡 Feedback</summary>

DNS uses port 53 for both UDP (standard queries) and TCP (large responses, zone transfers). DNS over TLS uses port 853. [DNS folosește portul 53 atât pentru UDP (interogări standard) cât și pentru TCP (răspunsuri mari, transferuri de zonă). DNS peste TLS folosește portul 853.]

</details>

---

### Q15. `N11.C04.Q02`
**DNS Resolution Hierarchy / Ierarhia rezoluției DNS**

*Multiple Choice – Alegere multiplă*

> A recursive resolver receives a query for www.ase.ro and has no cached data. In what order does it query the DNS hierarchy? [Un resolver recursiv primește o interogare pentru www.ase.ro și nu are date în cache. În ce ordine interogează ierarhia DNS?]

- **a)** A single central DNS server that stores all domain records worldwide [Un singur server DNS central care stochează toate înregistrările de domenii din lume]
- **b)** The client's local /etc/hosts file first, then a single authoritative server for the domain [Fișierul local /etc/hosts al clientului mai întâi, apoi un singur server autoritativ pentru domeniu]
- **c)** ase.ro authoritative servers first, then .ro TLD servers, then root servers as fallback [Servere autoritative ase.ro mai întâi, apoi servere TLD .ro, apoi servere root ca rezervă]
- **d)** Root servers, then .ro TLD servers, then ase.ro authoritative nameservers [Servere root, apoi servere TLD .ro, apoi servere de nume autoritative ase.ro]

<details><summary>💡 Feedback</summary>

DNS resolution follows a delegation chain: root servers → .ro TLD servers → ase.ro authoritative servers. Each level provides a referral to the next more specific zone until the authoritative  [Resolverul urmează lanțul de delegare: servere root → servere TLD .ro → servere autoritative ase.ro. Fiecare nivel furnizează o referință către zona mai specifică următoare până la obținerea răspunsului autoritativ.]

</details>

---

### Q16. `N11.C04.Q03`
**TTL Caching Behaviour / Comportamentul de caching TTL**

*Multiple Choice – Alegere multiplă*

> You set a DNS record TTL to 60 seconds. A user reports seeing the old IP address 5 minutes later. What is the most probable explanation? [Setați TTL-ul unei înregistrări DNS la 60 de secunde. Un utilizator raportează că vede adresa IP veche 5 minute mai târziu. Care este cea mai probabilă explicație?]

- **a)** The user's ISP resolver enforces a minimum cache duration longer than the configured TTL [Resolverul ISP al utilizatorului impune o durată minimă de cache mai lungă decât TTL-ul configurat]
- **b)** The DNS update definitively failed and the old record is still active on the authoritative server [Actualizarea DNS a eșuat definitiv și înregistrarea veche este încă activă pe serverul autoritativ]
- **c)** The user must manually flush their local DNS cache using the ipconfig /flushdns command [Utilizatorul trebuie să golească manual cache-ul DNS local folosind comanda ipconfig /flushdns]
- **d)** DNS propagation universally requires 24 to 48 hours regardless of TTL configuration settings [Propagarea DNS necesită universal 24 până la 48 de ore indiferent de setările de configurare TTL]

<details><summary>💡 Feedback</summary>

TTL is advisory, not mandatory. ISP resolvers, OS caches, and browsers may enforce minimum TTL values (often 5 minutes) that override the record's own TTL setting. [TTL este consultativ, nu obligatoriu. Resolverele ISP, cache-urile OS și browserele pot impune valori TTL minime (adesea 5 minute) care suprascriu setarea TTL proprie a înregistrării.]

</details>

---

### Q17. `N11.C04.Q04`
**Recursive vs Iterative DNS Queries / Interogări DNS recursive vs iterative**

*Multiple Choice – Alegere multiplă*

> How does a recursive DNS query differ from an iterative one? [Cum diferă o interogare DNS recursivă de una iterativă?]

- **a)** Both terms describe the same resolution process but from different vendor perspectives [Ambii termeni descriu același proces de rezoluție dar din perspective diferite ale furnizorilor]
- **b)** The recursive resolver performs complete resolution for the client; an iterative server returns referrals [Resolverul recursiv efectuează rezoluția completă pentru client; un server iterativ returnează referințe]
- **c)** Recursive queries contact only root servers; iterative queries contact only TLD servers for initial referrals before handing off to authoritative servers [Interogările recursive contactează doar servere root; interogările iterative contactează doar servere TLD pentru referințe inițiale înainte de a transfera către serverele autoritare]
- **d)** Recursive queries use UDP exclusively; iterative queries use TCP exclusively [Interogările recursive folosesc exclusiv UDP; interogările iterative folosesc exclusiv TCP]

<details><summary>💡 Feedback</summary>

In recursive mode, the resolver performs the full resolution chain on behalf of the client. In iterative mode, the queried server returns the best answer it has (often a referral), and the client must follow up. [În modul recursiv, resolverul efectuează lanțul complet de rezoluție în numele clientului. În modul iterativ, serverul interogat returnează cel mai bun răspuns pe care îl are (adesea o referință), iar clientul trebuie să continue.]

</details>

---

### Q18. `N11.C04.Q05`
**NXDOMAIN Response Semantics / Semantica răspunsului NXDOMAIN**

*Multiple Choice – Alegere multiplă*

> A DNS query returns RCODE 3 (NXDOMAIN). What does this response signify? [O interogare DNS returnează RCODE 3 (NXDOMAIN). Ce semnifică acest răspuns?]

- **a)** The DNS server is temporarily unable to process the query due to high load [Serverul DNS nu poate procesa temporar interogarea din cauza încărcării mari]
- **b)** The query was refused by the server's access control policy for the client IP [Interogarea a fost refuzată de politica de control al accesului serverului pentru IP-ul clientului]
- **c)** The DNS server software has crashed and the response is an error artefact [Software-ul serverului DNS s-a prăbușit și răspunsul este un artefact de eroare]
- **d)** The queried domain does not exist — this is a valid, definitive DNS answer [Domeniul interogat nu există — acesta este un răspuns DNS valid și definitiv]

<details><summary>💡 Feedback</summary>

NXDOMAIN is a valid, authoritative answer meaning the queried domain name does not exist in the namespace. It is not an error condition in the DNS infrastructure itself. [NXDOMAIN este un răspuns valid, autoritativ, care înseamnă că numele de domeniu interogat nu există în spațiul de nume. Nu este o condiție de eroare în infrastructura DNS în sine.]

</details>

---

### Q19. `N11.C05.Q01`
**DNS A Record Purpose / Scopul înregistrării DNS A**

*Multiple Choice – Alegere multiplă*

> What information does a DNS A record provide? [Ce informații furnizează o înregistrare DNS de tip A?]

- **a)** A mapping from a domain name to its corresponding IPv6 address (128-bit) [O mapare de la un nume de domeniu la adresa sa IPv6 corespunzătoare (128 biți)]
- **b)** An alias that redirects one domain name to another canonical domain name [Un alias care redirecționează un nume de domeniu către alt nume canonic de domeniu]
- **c)** A mapping from a domain name to its corresponding IPv4 address [O mapare de la un nume de domeniu la adresa sa IPv4 corespunzătoare]
- **d)** A pointer to the authoritative mail exchange server for the domain [Un indicator către serverul de schimb de e-mail autoritativ pentru domeniu]

<details><summary>💡 Feedback</summary>

An A record maps a domain name to an IPv4 address. AAAA maps to IPv6. MX maps to mail servers. CNAME creates an alias to another domain name. [O înregistrare A asociază un nume de domeniu cu o adresă IPv4. AAAA asociază cu IPv6. MX asociază cu servere de e-mail. CNAME creează un alias către alt nume de domeniu.]

</details>

---

### Q20. `N11.C05.Q02`
**When DNS Uses TCP Instead of UDP / Când DNS folosește TCP în loc de UDP**

*Multiple Choice – Alegere multiplă*

> Under what circumstances does DNS use TCP on port 53 instead of the more common UDP? [În ce circumstanțe folosește DNS protocolul TCP pe portul 53 în loc de mai comunul UDP?]

- **a)** TCP is reserved solely for reverse DNS lookups (PTR records) and nothing else and is never used for standard forward resolution of A or AAAA records [TCP este rezervat exclusiv pentru căutări DNS inverse (înregistrări PTR) și nimic altceva și nu este utilizat niciodată pentru rezoluția directă standard a înregistrărilor A sau AAAA]
- **b)** DNS never uses TCP — all communication occurs exclusively over UDP on port 53 [DNS nu folosește niciodată TCP — toată comunicarea are loc exclusiv prin UDP pe portul 53]
- **c)** TCP is used only when the DNS server detects packet loss on the network path [TCP este folosit doar când serverul DNS detectează pierderi de pachete pe calea de rețea]
- **d)** When the response exceeds the UDP size limit or during full zone transfers between servers [Când răspunsul depășește limita de dimensiune UDP sau în timpul transferurilor complete de zonă între servere]

<details><summary>💡 Feedback</summary>

DNS falls back to TCP when the response exceeds the UDP size limit (historically 512 bytes, now often 4096 with EDNS0), and during zone transfers (AXFR/IXFR) between servers. [DNS recurge la TCP când răspunsul depășește limita de dimensiune UDP (istoric 512 octeți, acum adesea 4096 cu EDNS0) și în timpul transferurilor de zonă (AXFR/IXFR) între servere.]

</details>

---

### Q21. `N11.C05.Q03`
**MX Record Function / Funcția înregistrării MX**

*Multiple Choice – Alegere multiplă*

> What role does an MX resource record serve in the DNS infrastructure? [Ce rol servește o înregistrare de resurse MX în infrastructura DNS?]

- **a)** It identifies the mail exchange servers for a domain, with priority-based failover ordering [Identifică serverele de schimb de e-mail pentru un domeniu, cu ordonare de failover bazată pe prioritate]
- **b)** It maps a domain name to the IPv4 address of the domain's primary web server [Asociază un nume de domeniu cu adresa IPv4 a serverului web principal al domeniului]
- **c)** It delegates authority for a subdomain to a different set of nameservers [Deleagă autoritatea pentru un subdomeniu către un set diferit de servere de nume]
- **d)** It creates a canonical name alias that points one domain to another domain name, enabling flexible hostname indirection for web services and CDN configurations [Creează un alias de nume canonic care indică de la un domeniu către alt nume de domeniu, permițând redirecționarea flexibilă a numelor de gazdă pentru servicii web și configurații CDN]

<details><summary>💡 Feedback</summary>

MX records specify the mail exchange servers responsible for receiving email for a domain. Each MX record includes a priority value — lower numbers indicate higher preference. [Înregistrările MX specifică serverele de schimb de e-mail responsabile cu primirea e-mailurilor pentru un domeniu. Fiecare înregistrare MX include o valoare de prioritate — numerele mai mici indică preferință mai mare.]

</details>

---

### Q22. `N11.C05.Q04`
**NS Record Purpose in DNS Delegation / Scopul înregistrării NS în delegarea DNS**

*Multiple Choice – Alegere multiplă*

> What function does an NS resource record perform? [Ce funcție îndeplinește o înregistrare de resurse NS?]

- **a)** It delegates a DNS zone to the specified authoritative nameservers [Deleagă o zonă DNS către serverele de nume autoritative specificate]
- **b)** It specifies the Start of Authority metadata including serial and refresh intervals [Specifică metadatele Start of Authority incluzând serialul și intervalele de reîmprospătare]
- **c)** It lists arbitrary text strings used for SPF email validation policies [Listează șiruri de text arbitrare folosite pentru politicile de validare SPF a e-mailurilor]
- **d)** It provides the IPv6 address corresponding to a given domain name [Furnizează adresa IPv6 corespunzătoare unui nume de domeniu dat]

<details><summary>💡 Feedback</summary>

NS records delegate authority for a DNS zone to specific nameservers. They form the backbone of the hierarchical delegation system that makes DNS scalable. [Înregistrările NS deleagă autoritatea pentru o zonă DNS către servere de nume specifice. Ele formează coloana vertebrală a sistemului de delegare ierarhică care face DNS scalabil.]

</details>

---

### Q23. `N11.C06.Q01`
**FTP Dual-Connection Architecture / Arhitectura cu conexiune duală FTP**

*Multiple Choice – Alegere multiplă*

> How many simultaneous TCP connections does FTP use during an active file transfer? [Câte conexiuni TCP simultane folosește FTP în timpul unui transfer activ de fișiere?]

- **a)** Two: a persistent control connection on port 21, plus a transient data connection for the transfer [Două: o conexiune de control persistentă pe portul 21, plus o conexiune de date tranzitorie pentru transfer]
- **b)** A variable number depending on file size — one connection per transferred block [Un număr variabil în funcție de dimensiunea fișierului — o conexiune per bloc transferat]
- **c)** Three concurrent TCP connections: a control connection for commands, a dedicated upload channel for outbound transfers, and a separate download channel for inbound data [Trei conexiuni TCP concurente: o conexiune de control pentru comenzi, un canal dedicat de încărcare pentru transferuri de ieșire și un canal separat de descărcare pentru date de intrare]
- **d)** One multiplexed connection on port 21 that carries both commands and file data interleaved [O conexiune multiplexată pe portul 21 care transportă atât comenzi cât și date intercalate]

<details><summary>💡 Feedback</summary>

FTP uses a dual-connection architecture: a persistent control connection on port 21 for commands and responses, plus a transient data connection (port 20 in active mode or ephemeral in passive mode) for the actual file transfer. [FTP folosește o arhitectură cu conexiune duală: o conexiune de control persistentă pe portul 21 pentru comenzi și răspunsuri, plus o conexiune de date tranzitorie (portul 20 în modul activ sau efemer în modul pasiv) pentru transferul efectiv al fișierului.]

</details>

---

### Q24. `N11.C06.Q04`
**FTPS vs SFTP Distinction / Distincția între FTPS și SFTP**

*Multiple Choice – Alegere multiplă*

> A colleague suggests migrating from plain FTP to a secure alternative. What is the key difference between FTPS and SFTP? [Un coleg sugerează migrarea de la FTP simplu la o alternativă securizată. Care este diferența cheie între FTPS și SFTP?]

- **a)** FTPS uses asymmetric encryption only; SFTP uses both symmetric and asymmetric encryption [FTPS folosește doar criptare asimetrică; SFTP folosește atât criptare simetrică cât și asimetrică]
- **b)** FTPS wraps FTP in TLS encryption; SFTP is a separate protocol running over SSH on port 22 [FTPS împachetează FTP în criptare TLS; SFTP este un protocol separat care rulează peste SSH pe portul 22]
- **c)** FTPS and SFTP are identical protocols using different vendor naming conventions [FTPS și SFTP sunt protocoale identice folosind convenții de denumire diferite ale furnizorilor]
- **d)** FTPS operates on port 990 exclusively; SFTP operates on port 115 exclusively [FTPS operează exclusiv pe portul 990; SFTP operează exclusiv pe portul 115]

<details><summary>💡 Feedback</summary>

FTPS is FTP with TLS encryption layered over the standard FTP protocol. SFTP is the SSH File Transfer Protocol — a completely different protocol that runs over SSH (port 22). They are not interchangeable. [FTPS este FTP cu criptare TLS stratificată peste protocolul FTP standard. SFTP este protocolul SSH de transfer de fișiere — un protocol complet diferit care rulează peste SSH (portul 22). Nu sunt interschimbabile.]

</details>

---

### Q25. `N11.C07.Q01`
**Default SSH Port Number / Numărul de port SSH implicit**

*Multiple Choice – Alegere multiplă*

> On which TCP port does the Secure Shell protocol listen by default? [Pe ce port TCP ascultă protocolul Secure Shell în mod implicit?]

- **a)** TCP port 21, shared with the FTP control channel [Portul TCP 21, partajat cu canalul de control FTP]
- **b)** TCP port 443, alongside HTTPS encrypted web traffic [Portul TCP 443, alături de traficul web criptat HTTPS]
- **c)** TCP port 22 [Portul TCP 22]
- **d)** TCP port 23, the legacy Telnet service port [Portul TCP 23, portul serviciului Telnet moștenit]

<details><summary>💡 Feedback</summary>

SSH uses TCP port 22 by default. Port 21 is FTP control, port 23 is Telnet (unencrypted), and port 25 is SMTP. [SSH folosește portul TCP 22 implicit. Portul 21 este controlul FTP, portul 23 este Telnet (necriptat), iar portul 25 este SMTP.]

</details>

---

### Q26. `N11.C07.Q02`
**SSH Local Port Forwarding Encryption Scope / Scopul criptării în redirecționarea portului local SSH**

*Multiple Choice – Alegere multiplă*

> Given the command ssh -L 8080:internal-web:80 user@jumphost, which network segment is encrypted? [Având comanda ssh -L 8080:internal-web:80 user@jumphost, ce segment de rețea este criptat?]

- **a)** No encryption occurs — SSH port forwarding only provides access routing without any encryption [Nu are loc nicio criptare — redirecționarea portului SSH oferă doar rutare de acces fără criptare]
- **b)** The segment from jumphost to internal-web:80 is encrypted; the local segment is plaintext [Segmentul de la jumphost la internal-web:80 este criptat; segmentul local este text clar]
- **c)** The entire path end-to-end from the local browser to internal-web:80 is fully encrypted [Întreaga cale de la un capăt la altul de la browserul local la internal-web:80 este complet criptată]
- **d)** Only the tunnel segment from the local machine to the jumphost is encrypted by SSH [Doar segmentul de tunel de la mașina locală la jumphost este criptat de SSH]

<details><summary>💡 Feedback</summary>

SSH encrypts only the tunnel segment between the SSH client and the SSH server (jumphost). Traffic from the jumphost to the destination (internal-web:80) travels in plaintext. This is not end-to-end encryption. [SSH criptează doar segmentul de tunel dintre clientul SSH și serverul SSH (jumphost). Traficul de la jumphost la destinație (internal-web:80) circulă în text clar. Aceasta nu este criptare de la un capăt la altul.]

</details>

---

### Q27. `N11.C07.Q03`
**SSH Protocol Layering Architecture / Arhitectura pe straturi a protocolului SSH**

*Multiple Choice – Alegere multiplă*

> The SSH protocol suite comprises three interdependent layers. Which layer is responsible for encrypting the communication and negotiating the key exchange? [Suita de protocoale SSH cuprinde trei straturi interdependente. Care strat este responsabil cu criptarea comunicării și negocierea schimbului de chei?]

- **a)** The User Authentication Protocol, because encryption requires verifying identity before use [Protocolul de Autentificare a Utilizatorului, deoarece criptarea necesită verificarea identității înainte de utilizare]
- **b)** The Application Protocol, which wraps shell commands in encrypted frames before transmission [Protocolul Aplicație, care împachetează comenzile shell în cadre criptate înainte de transmisie]
- **c)** The Transport Layer Protocol, which handles key exchange, encryption, and integrity verification [Protocolul Stratului de Transport, care gestionează schimbul de chei, criptarea și verificarea integrității]
- **d)** The Connection Protocol, which manages all encrypted channels and their security properties [Protocolul de Conexiune, care gestionează toate canalele criptate și proprietățile lor de securitate]

<details><summary>💡 Feedback</summary>

SSH's Transport Layer Protocol (RFC 4253) provides server authentication, confidentiality, and integrity. It negotiates key exchange (Diffie-Hellman), encryption cipher, and MAC algorithm. The User Authentication Protocol handles client identity; the Connection Protocol multiplexes channels. [Protocolul Stratului de Transport (RFC 4253) asigură autentificarea serverului, confidențialitatea și integritatea. Negociază schimbul de chei (Diffie-Hellman), cifrul de criptare și algoritmul MAC. Protocolul de Autentificare a Utilizatorului gestionează identitatea clientului; Protocolul de Conexiune multiplexează canalele.]

</details>

---

### Q28. `N11.T00.Q01`
**Scenario: Backend Failure Diagnosis / Scenariu: diagnosticarea eșecului serverului**

*Multiple Choice – Alegere multiplă*

> A student configures Nginx with 3 backends and default settings. After stopping Backend 2, they send 6 requests and observe one 502 error followed by successful responses alternating between Backends 1 and 3. Explain what happened. [Un student configurează Nginx cu 3 servere și setări implicite. După oprirea Backend 2, trimite 6 cereri și observă o eroare 502 urmată de răspunsuri de succes alternând între Backend 1 și 3. Explicați ce s-a întâmplat.]

- **a)** Backend 2 continues receiving requests because Nginx does not track backend health states [Backend 2 continuă să primească cereri deoarece Nginx nu urmărește stările de sănătate ale serverelor]
- **b)** The 502 results from passive health check detection; Nginx marks Backend 2 down and redistributes to the remaining healthy backends [502 rezultă din detectarea pasivă; Nginx marchează Backend 2 ca inactiv și redistribuie către serverele sănătoase rămase]
- **c)** Nginx detected the failure before any request reached Backend 2 using active health probes that periodically test each upstream endpoint independently [Nginx a detectat eșecul înainte ca vreo cerere să ajungă la Backend 2 folosind sonde active de sănătate care testează periodic fiecare punct final upstream în mod independent]
- **d)** The 502 error indicates that Nginx itself crashed and restarted automatically [Eroarea 502 indică faptul că Nginx s-a prăbușit și s-a repornit automat]

<details><summary>💡 Feedback</summary>

When Backend 2 receives its first request and fails, Nginx returns 502 (passive detection). Nginx marks Backend 2 as down (max_fails=1). Subsequent requests distribute between the two remaining healthy backends via round-robin. [Prima cerere direcționată către Backend 2 eșuează cu 502 (detecție pasivă). Nginx marchează Backend 2 ca inactiv (max_fails=1). Cererile ulterioare se distribuie între cele două servere sănătoase rămase prin round-robin.]

</details>

---

### Q29. `N11.T00.Q02`
**Scenario: Weighted Distribution Calculation / Scenariu: calculul distribuției ponderate**

*Multiple Choice – Alegere multiplă*

> An Nginx upstream block configures: server web1 weight=5; server web2 weight=3; server web3 weight=2;. Out of 100 requests, approximately how many does web2 receive? [Un bloc upstream Nginx configurează: server web1 weight=5; server web2 weight=3; server web3 weight=2;. Din 100 de cereri, aproximativ câte primește web2?]

- **a)** Approximately 33, because Nginx always distributes equally among all three backends regardless of any weight directives specified in the upstream block [Aproximativ 33, deoarece Nginx distribuie întotdeauna egal între cele trei servere indiferent de directivele de pondere specificate în blocul upstream]
- **b)** Approximately 50, because web2 receives the median weight allocation in the pool [Aproximativ 50, deoarece web2 primește alocarea mediană de pondere din grup]
- **c)** Approximately 3, because weight=3 means exactly 3 requests per rotation cycle [Aproximativ 3, deoarece weight=3 înseamnă exact 3 cereri per ciclu de rotație]
- **d)** Approximately 30, because web2's weight of 3 out of total weight 10 gives it 30% of traffic [Aproximativ 30, deoarece ponderea web2 de 3 din ponderea totală 10 îi conferă 30% din trafic]

<details><summary>💡 Feedback</summary>

Total weight = 5+3+2 = 10. web2 receives 3/10 = 30% of 100 = 30 requests. [Ponderea totală = 5+3+2 = 10. web2 primește 3/10 = 30% din 100 = 30 de cereri.]

</details>

---

### Q30. `N11.T00.Q03`
**Scenario: IP Hash After Server Removal / Scenariu: IP hash după eliminarea unui server**

*Multiple Choice – Alegere multiplă*

> A load balancer uses IP hash with 4 backends. Backend C is permanently removed. A returning client from IP 10.0.0.5 was previously routed to Backend B. After the removal, where does the client go? [Un echilibrator de încărcare folosește IP hash cu 4 servere. Backend C este eliminat permanent. Un client care revine de la IP 10.0.0.5 era direcționat anterior către Backend B. După eliminare, unde merge clientul?]

- **a)** The client receives an error because their hash mapping no longer exists after the removal [Clientul primește o eroare deoarece maparea lor hash nu mai există după eliminare]
- **b)** The client continues to Backend B, because IP hash is deterministic for any given IP address [Clientul continuă la Backend B, deoarece IP hash este determinist pentru orice adresă IP dată]
- **c)** The client is always routed to Backend A as the first available server in the reduced pool [Clientul este întotdeauna direcționat către Backend A ca primul server disponibil din grupul redus]
- **d)** The client may go to any remaining backend, because removing a server changes the hash modulus [Clientul poate merge la orice server rămas, deoarece eliminarea unui server schimbă modulul hash]

<details><summary>💡 Feedback</summary>

After pool changes, the client may be routed to any remaining backend (A, B, or D). Removing Backend C changes the modulus from 4 to 3, which redistributes the hash mapping. The client is not guaranteed to stay on Backend B. [Clientul poate fi direcționat către oricare dintre serverele rămase (A, B sau D). Eliminarea Backend C schimbă modulul de la 4 la 3, ceea ce redistribuie maparea hash. Clientul nu este garantat să rămână pe Backend B.]

</details>

---

### Q31. `N11.T00.Q04`
**Scenario: DNS TTL and Caching Behaviour / Scenariu: TTL DNS și comportamentul de caching**

*Multiple Choice – Alegere multiplă*

> A DNS record has TTL=300 (5 minutes). You change the IP at the authoritative server. After 10 minutes, one user sees the new IP but another does not. What explains this inconsistency? [O înregistrare DNS are TTL=300 (5 minute). Schimbați IP-ul la serverul autoritativ. După 10 minute, un utilizator vede noul IP dar altul nu. Ce explică această inconsistență?]

- **a)** The DNS change failed partially, updating some authoritative servers but not others [Schimbarea DNS a eșuat parțial, actualizând unele servere autoritative dar nu pe toate]
- **b)** The user who sees the old IP has a corrupted DNS cache that requires manual intervention such as running ipconfig /flushdns or restarting the resolver service [Utilizatorul care vede IP-ul vechi are un cache DNS corupt care necesită intervenție manuală precum rularea ipconfig /flushdns sau repornirea serviciului de rezolvare]
- **c)** DNS propagation is inherently random and unpredictable regardless of TTL settings [Propagarea DNS este inerent aleatorie și imprevizibilă indiferent de setările TTL]
- **d)** Different resolvers enforce different minimum TTL policies, causing inconsistent cache expiration times [Resolvere diferite impun politici diferite de TTL minim, cauzând timpi inconsistenți de expirare a cache-ului]

<details><summary>💡 Feedback</summary>

Different resolvers cache independently and may apply different minimum TTL policies. Browser caches, OS caches, and ISP resolvers each have their own TTL enforcement rules that may extend caching beyond the record's specified TTL. [Resolvere diferite memorează independent și pot aplica politici diferite de TTL minim. Cache-urile browserelor, cache-urile OS și resolverele ISP au fiecare regulile proprii de impunere TTL care pot extinde memorarea dincolo de TTL-ul specificat al înregistrării.]

</details>

---

### Q32. `N11.T00.Q06`
**Scenario: SSH Tunnel Security Boundaries / Scenariu: limitele de securitate ale tunelului SSH**

*Multiple Choice – Alegere multiplă*

> A developer uses ssh -L 3306:db-server:3306 user@bastion to access a remote database. A security auditor asks whether the traffic between the bastion host and db-server is encrypted. What is the correct answer? [Un dezvoltator folosește ssh -L 3306:db-server:3306 user@bastion pentru a accesa o bază de date la distanță. Un auditor de securitate întreabă dacă traficul între gazda bastion și db-server este criptat. Care este răspunsul corect?]

- **a)** No — SSH encrypts only the tunnel segment; traffic from bastion to db-server is unencrypted plaintext [Nu — SSH criptează doar segmentul de tunel; traficul de la bastion la db-server este text clar necriptat]
- **b)** Partially — SSH encrypts the database queries but not the response data returning through the tunnel [Parțial — SSH criptează interogările bazei de date dar nu datele de răspuns care revin prin tunel]
- **c)** It depends on the database protocol — MySQL traffic is encrypted but PostgreSQL traffic is not [Depinde de protocolul bazei de date — traficul MySQL este criptat dar traficul PostgreSQL nu este]
- **d)** Yes — SSH provides end-to-end encryption for all traffic flowing through the forwarded port [Da — SSH asigură criptare de la un capăt la altul pentru tot traficul care circulă prin portul redirecționat]

<details><summary>💡 Feedback</summary>

The SSH tunnel encrypts only the segment between the developer's machine and the bastion host. Traffic from the bastion to db-server travels unencrypted over the internal network. [Tunelul SSH criptează doar segmentul dintre mașina dezvoltatorului și gazda bastion. Traficul de la bastion la db-server circulă necriptat prin rețeaua internă.]

</details>

---

### Q33. `N11.T00.Q07`
**Scenario: DNS Domain Name Encoding Length / Scenariu: lungimea codificării numelui de domeniu DNS**

*Multiple Choice – Alegere multiplă*

> The domain "mail.google.com" is encoded using DNS length-prefixed labels. How many bytes does the encoded QNAME occupy including the null terminator? [Domeniul "mail.google.com" este codificat folosind etichete DNS prefixate cu lungimea. Câți octeți ocupă QNAME-ul codificat inclusiv terminatorul null?]

- **a)** 14 bytes: DNS compression eliminates repeated suffixes like .com from the encoding [14 octeți: compresia DNS elimină sufixele repetate precum .com din codificare]
- **b)** 17 bytes: \x04mail (5) + \x06google (7) + \x03com (4) + \x00 terminator (1) [17 octeți: \x04mail (5) + \x06google (7) + \x03com (4) + \x00 terminator (1)]
- **c)** 20 bytes: each label includes both a length prefix byte and a null terminator byte [20 octeți: fiecare etichetă include atât un octet prefix de lungime cât și un octet terminator null]
- **d)** 15 bytes: the raw ASCII string mail.google.com including the two dot separators [15 octeți: șirul ASCII brut mail.google.com inclusiv cele două separatoare punct]

<details><summary>💡 Feedback</summary>

Encoding: \x04mail (5) + \x06google (7) + \x03com (4) + \x00 (1) = 17 bytes. Each label gets a 1-byte length prefix. [Codificarea: \x04mail (5) + \x06google (7) + \x03com (4) + \x00 (1) = 17 octeți. Fiecare etichetă primește un prefix de lungime de 1 octet.]

</details>

---

### Q34. `N11.T00.Q08`
**Scenario: proxy_next_upstream Retry Limits / Scenariu: limitele de reîncercare proxy_next_upstream**

*Multiple Choice – Alegere multiplă*

> Nginx is configured with proxy_next_upstream_tries 3; and 5 backends. If the first 3 backends all return 502, what happens to the request? [Nginx este configurat cu proxy_next_upstream_tries 3; și 5 servere. Dacă primele 3 servere returnează toate 502, ce se întâmplă cu cererea?]

- **a)** The client receives 502 — Nginx stops after 3 tries even though 2 healthy backends remain untried [Clientul primește 502 — Nginx se oprește după 3 încercări chiar dacă 2 servere sănătoase rămân neîncercate]
- **b)** Nginx queues the request until one of the failed backends recovers and can serve it [Nginx pune cererea în coadă până când unul dintre serverele eșuate se recuperează și o poate servi]
- **c)** Nginx automatically tries all 5 backends regardless of the proxy_next_upstream_tries setting [Nginx încearcă automat toate cele 5 servere indiferent de setarea proxy_next_upstream_tries]
- **d)** Nginx returns 503 Service Unavailable once any retry limit is reached during request processing, regardless of whether other healthy backends remain available in the pool [Nginx returnează 503 Service Unavailable odată ce orice limită de reîncercare este atinsă, indiferent dacă alte servere sănătoase rămân disponibile în grup]

<details><summary>💡 Feedback</summary>

After 3 retry attempts (the configured limit), Nginx stops trying additional backends and returns the last error (502) to the client. The remaining 2 backends are not contacted for this request. [După 3 încercări de reîncercare (limita configurată), Nginx oprește încercarea serverelor suplimentare și returnează ultima eroare (502) clientului. Cele 2 servere rămase nu sunt contactate pentru această cerere.]

</details>

---

### Q35. `N11.T00.Q09`
**Scenario: Least Connections with Slow Backend / Scenariu: least connections cu server lent**

*Multiple Choice – Alegere multiplă*

> Three backends start with 0 active connections. Backend 3 has --delay 2.0 (2 second response time). After 10 rapid requests, which backend has the most active connections? [Trei servere pornesc cu 0 conexiuni active. Backend 3 are --delay 2.0 (timp de răspuns de 2 secunde). După 10 cereri rapide, care server are cele mai multe conexiuni active?]

- **a)** Backend 3 accumulates the most active connections because its 2-second delay keeps them open longer [Backend 3 acumulează cele mai multe conexiuni active deoarece întârzierea de 2 secunde le menține deschise mai mult]
- **b)** All three backends have equal active connections because least_conn distributes them evenly [Toate cele trei servere au conexiuni active egale deoarece least_conn le distribuie uniform]
- **c)** Backend 1 has the most because least_conn always prefers the first listed server [Backend 1 are cele mai multe deoarece least_conn preferă întotdeauna primul server listat]
- **d)** Connection counts cannot be predicted because they depend on operating system scheduling and kernel-level thread allocation policies that vary between operating systems [Numărătoarea conexiunilor nu poate fi prezisă deoarece depinde de planificarea sistemului de operare și politicile de alocare a firelor la nivel de kernel care variază între sistemele de operare]

<details><summary>💡 Feedback</summary>

Backend 3's 2-second delay means its connections stay open longer. Least connections initially distributes evenly, but as Backend 3 accumulates connections (slow to release), it stops receiving new ones — Backends 1 and 2 process and release faster. [Întârzierea de 2 secunde a Backend 3 înseamnă că conexiunile sale rămân deschise mai mult. Least connections distribuie inițial uniform, dar pe măsură ce Backend 3 acumulează conexiuni (lent la eliberare), oprește primirea de noi — Backend 1 și 2 procesează și eliberează mai repede.]

</details>

---

### Q36. `N11.T00.Q10`
**Scenario: Comprehensive Protocol Port Identification / Scenariu: identificarea comprehensivă a porturilor protocoalelor**

*Multiple Choice – Alegere multiplă*

> A packet capture shows the following: a TCP SYN to port 21, followed by traffic on port 53 (UDP), then an encrypted session on port 22. Identify the protocols in order. [O captură de pachete arată următoarele: un TCP SYN către portul 21, urmat de trafic pe portul 53 (UDP), apoi o sesiune criptată pe portul 22. Identificați protocoalele în ordine.]

- **a)** HTTP (21/TCP), then DHCP (53/UDP), then Telnet (22/TCP) — all application layer protocols [HTTP (21/TCP), apoi DHCP (53/UDP), apoi Telnet (22/TCP) — toate protocoale de nivel aplicație]
- **b)** SMTP (21/TCP), then NTP (53/UDP), then SFTP (22/TCP) — standard service ports [SMTP (21/TCP), apoi NTP (53/UDP), apoi SFTP (22/TCP) — porturi standard de servicii]
- **c)** Telnet (21/TCP), then DNS (53/UDP), then FTP data (22/TCP) — mixed protocol sequence [Telnet (21/TCP), apoi DNS (53/UDP), apoi date FTP (22/TCP) — secvență de protocoale mixte]
- **d)** FTP control (21/TCP), then DNS query (53/UDP), then SSH session (22/TCP) [Control FTP (21/TCP), apoi interogare DNS (53/UDP), apoi sesiune SSH (22/TCP)]

<details><summary>💡 Feedback</summary>

Port 21 TCP = FTP control connection; Port 53 UDP = DNS query; Port 22 TCP = SSH encrypted session. These are three of the standard application protocols covered in Week 11. [Portul 21 TCP = conexiune de control FTP; Portul 53 UDP = interogare DNS; Portul 22 TCP = sesiune SSH criptată. Acestea sunt trei dintre protocoalele standard de aplicație acoperite în săptămâna 11.]

</details>

---

### Q37. `N11.C02.Q02`
**Active vs Passive Health Checking / Verificări active vs pasive de sănătate**

*Multiple Choice – Alegere multiplă*

> How does passive health checking differ from active health checking in a load balancer deployment? [Cum diferă verificarea pasivă de sănătate de verificarea activă de sănătate într-o implementare de echilibrator de încărcare?]

- **a)** Passive checks query a /health endpoint every 5 seconds; active checks wait for client complaints, requiring explicit configuration of probe intervals and thresholds [Verificările pasive interoghează un endpoint /health la fiecare 5 secunde; verificările active așteaptă reclamații de la clienți, necesitând configurarea explicită a intervalelor de sondare și a pragurilor]
- **b)** Passive checks require Nginx Plus commercial licence; active checks work in the open-source edition [Verificările pasive necesită licență comercială Nginx Plus; verificările active funcționează în ediția open-source]
- **c)** Both methods are identical in behaviour but use different terminology across vendor documentation [Ambele metode sunt identice ca comportament dar folosesc terminologie diferită în documentația furnizorilor]
- **d)** Passive checks detect failure from real request errors; active checks send periodic probes independently of user traffic [Verificările pasive detectează eșecul din erorile cererilor reale; verificările active trimit sonde periodice independent de traficul utilizatorilor]

<details><summary>💡 Feedback</summary>

Passive checks infer health from production traffic failures; active checks send dedicated probe requests at configured intervals regardless of production traffic. [Verificările pasive deduc sănătatea din eșecurile traficului de producție; verificările active trimit cereri de sondare dedicate la intervale configurate, indiferent de traficul de producție.]

</details>

---

### Q38. `N11.C06.Q02`
**Why Passive Mode Traverses NAT Successfully / De ce modul pasiv traversează NAT cu succes**

*Multiple Choice – Alegere multiplă*

> FTP passive mode is preferred over active mode when clients are behind NAT. Why does passive mode work better in this scenario? [Modul pasiv FTP este preferat față de modul activ când clienții sunt în spatele NAT. De ce funcționează modul pasiv mai bine în acest scenariu?]

- **a)** Passive mode encrypts the data channel, preventing NAT from interfering with the transfer [Modul pasiv criptează canalul de date, împiedicând NAT să interfereze cu transferul]
- **b)** Passive mode compresses commands and data into a single port 21 connection [Modul pasiv comprimă comenzile și datele într-o singură conexiune pe portul 21]
- **c)** Passive mode uses UDP datagrams that traverse NAT more easily than TCP connections [Modul pasiv folosește datagrame UDP care traversează NAT mai ușor decât conexiunile TCP]
- **d)** The client initiates both outbound connections, which NAT handles without inbound rules [Clientul inițiază ambele conexiuni de ieșire, pe care NAT le gestionează fără reguli de intrare]

<details><summary>💡 Feedback</summary>

In passive mode, the client initiates both connections (control and data) as outbound TCP connections, which NAT handles naturally. In active mode, the server tries to connect back to the client — an inbound connection that NAT blocks. [În modul pasiv, clientul inițiază ambele conexiuni (control și date) ca conexiuni TCP de ieșire, pe care NAT le gestionează natural. În modul activ, serverul încearcă să se conecteze înapoi la client — o conexiune de intrare pe care NAT o blochează.]

</details>

---

### Q39. `N11.C06.Q03`
**FTP Control Port Assignment / Atribuirea portului de control FTP**

*Multiple Choice – Alegere multiplă*

> On which well-known TCP port does the FTP control connection operate? [Pe ce port TCP bine-cunoscut operează conexiunea de control FTP?]

- **a)** TCP port 22, shared with the SSH protocol on the same transport channel [Portul TCP 22, partajat cu protocolul SSH pe același canal de transport]
- **b)** TCP port 80, alongside HTTP traffic on the standard web service port [Portul TCP 80, alături de traficul HTTP pe portul standard al serviciului web]
- **c)** TCP port 21 [Portul TCP 21]
- **d)** TCP port 20, which handles all FTP communication including commands [Portul TCP 20, care gestionează toată comunicarea FTP inclusiv comenzile]

<details><summary>💡 Feedback</summary>

FTP uses TCP port 21 for its control connection. Port 20 is the default source port for the data connection in active mode. These are distinct from SSH (22) and HTTP (80). [Conexiunea de control FTP folosește portul TCP 21. Portul 20 este portul sursă implicit pentru conexiunea de date în modul activ. Acestea sunt distincte de SSH (22) și HTTP (80).]

</details>

---

### Q40. `N11.C07.Q04`
**SSH Channel Multiplexing Capability / Capacitatea de multiplexare a canalelor SSH**

*Multiple Choice – Alegere multiplă*

> A user runs an interactive shell, an SFTP transfer, and a port forwarding tunnel simultaneously over a single SSH connection. Which SSH protocol layer enables this? [Un utilizator rulează un shell interactiv, un transfer SFTP și un tunel de redirecționare a portului simultan printr-o singură conexiune SSH. Care strat al protocolului SSH permite acest lucru?]

- **a)** The TCP layer below SSH, which handles multiplexing via port number differentiation [Stratul TCP de sub SSH, care gestionează multiplexarea prin diferențierea numerelor de port]
- **b)** The Transport Layer, which splits encryption into separate parallel cipher contexts [Stratul de Transport, care împarte criptarea în contexte de cifru paralele separate]
- **c)** The Connection Protocol, which multiplexes logical channels with independent flow control [Protocolul de Conexiune, care multiplexează canale logice cu control al fluxului independent]
- **d)** The Authentication Protocol, which creates a separate session for each service type [Protocolul de Autentificare, care creează o sesiune separată pentru fiecare tip de serviciu]

<details><summary>💡 Feedback</summary>

RFC 4254 (Connection Protocol) multiplexes the encrypted tunnel into logical channels, each with independent flow control. This allows concurrent sessions, file transfers, and port forwarding over one TCP connection. [Protocolul de Conexiune (RFC 4254) multiplexează tunelul criptat în canale logice, fiecare cu control al fluxului independent. Aceasta permite sesiuni concurente, transferuri de fișiere și redirecționare de porturi printr-o singură conexiune TCP.]

</details>

---

### Q41. `N11.T00.Q05`
**Scenario: FTP Through NAT Troubleshooting / Scenariu: depanarea FTP prin NAT**

*Multiple Choice – Alegere multiplă*

> A client behind NAT can connect to an FTP server and list files (using LIST command), but file downloads in active mode fail. Switching to passive mode resolves the issue. Why? [Un client din spatele NAT se poate conecta la un server FTP și lista fișierele (folosind comanda LIST), dar descărcările de fișiere în modul activ eșuează. Comutarea la modul pasiv rezolvă problema. De ce?]

- **a)** Active mode requires the server to connect inbound to the client, which NAT blocks; passive mode keeps both connections outbound [Modul activ necesită ca serverul să se conecteze de intrare la client, ceea ce NAT blochează; modul pasiv menține ambele conexiuni de ieșire]
- **b)** Active mode encryption is incompatible with NAT translation tables used by the router [Criptarea modului activ este incompatibilă cu tabelele de traducere NAT folosite de router]
- **c)** Active mode transmits data on port 20, which is blocked by most enterprise firewalls by default, preventing the server-initiated data connection from traversing NAT gateways [Modul activ transmite date pe portul 20, care este blocat de majoritatea firewall-urilor enterprise implicit, împiedicând conexiunea de date inițiată de server să traverseze porțile NAT]
- **d)** Active mode uses UDP for data transfer, which NAT does not support for FTP connections [Modul activ folosește UDP pentru transferul de date, pe care NAT nu îl suportă pentru conexiuni FTP]

<details><summary>💡 Feedback</summary>

In active mode, the server initiates the data connection back to the client — an inbound connection that NAT blocks. In passive mode, the client initiates both connections outbound, which NAT handles naturally. LIST may have worked if it used passive mode implicitly. [În modul activ, serverul inițiază conexiunea de date înapoi către client — o conexiune de intrare pe care NAT o blochează. În modul pasiv, clientul inițiază ambele conexiuni de ieșire, pe care NAT le gestionează natural.]

</details>

---

## 📚 Lab Questions / Întrebări de laborator

---

### Q42. `N11.S01.Q01`
**Round-Robin Modulo Operation Result / Rezultatul operației modulo round-robin**

*Multiple Choice – Alegere multiplă*

> The Python load balancer exercise uses a round-robin method with self._rr_idx = (self._rr_idx + 1) % n where n = 3. After selecting the third backend (index 2), what is the value of _rr_idx? [Exercițiul cu echilibratorul de încărcare Python utilizează o metodă round-robin cu self._rr_idx = (self._rr_idx + 1) % n unde n = 3. După selectarea celui de-al treilea server (index 2), care este valoarea _rr_idx?]

- **a)** 0, because (2 + 1) % 3 wraps back to the beginning of the backend list [0, deoarece (2 + 1) % 3 revine la începutul listei de servere]
- **b)** 3, because the index simply increments without any wraparound applied [3, deoarece indexul pur și simplu crește fără nicio revenire aplicată]
- **c)** 1, because modulo 3 of the value 3 produces a remainder of 1 [1, deoarece modulo 3 din valoarea 3 produce un rest de 1]
- **d)** 2, because the index stays at the current position until the next request arrives [2, deoarece indexul rămâne la poziția curentă până când sosește următoarea cerere]

<details><summary>💡 Feedback</summary>

After selecting index 2, the expression evaluates to (2 + 1) % 3 = 0, wrapping back to the first backend. This modulo wraparound is the core mechanism that creates the cyclic pattern. [După selectarea indexului 2, expresia evaluează la (2 + 1) % 3 = 0, revenind la primul server. Această revenire prin modulo este mecanismul central care creează modelul ciclic.]

</details>

---

### Q43. `N11.S01.Q02`
**IP Hash Determinism Property / Proprietatea de determinism a IP hash**

*Multiple Choice – Alegere multiplă*

> The code h = (h * 131 + ord(ch)) & 0xFFFFFFFF computes the hash. If the same client IP sends 5 consecutive requests, how many distinct backends will be selected? [Codul h = (h * 131 + ord(ch)) & 0xFFFFFFFF calculează hash-ul. Dacă aceeași adresă IP de client trimite 5 cereri consecutive, câte servere distincte vor fi selectate?]

- **a)** Three — requests distribute evenly across all backends regardless of client IP address [Trei — cererile se distribuie uniform între toate serverele indiferent de adresa IP a clientului]
- **b)** Exactly one — the deterministic hash always maps the same IP to the same backend [Exact unul — hash-ul determinist asociază întotdeauna aceeași adresă IP cu același server]
- **c)** It varies unpredictably because the bitwise AND introduces non-deterministic truncation [Variază imprevizibil deoarece AND pe biți introduce o trunchiere nedeterministă]
- **d)** Five — each request produces a different hash because the algorithm uses random seeding [Cinci — fiecare cerere produce un hash diferit deoarece algoritmul folosește inițializare aleatorie]

<details><summary>💡 Feedback</summary>

Hash functions are deterministic: identical input always produces the same output. All 5 requests from the same IP select the same backend, providing session affinity. The & 0xFFFFFFFF constrains the hash to 32 bits. [Funcția hash este deterministă: aceeași intrare produce întotdeauna aceeași ieșire. Toate cele 5 cereri de la aceeași adresă IP selectează același server, asigurând afinitatea sesiunii. Operatorul & 0xFFFFFFFF constrânge hash-ul la 32 de biți.]

</details>

---

### Q44. `N11.S01.Q03`
**Health Check State Transition / Tranziția de stare a verificării de sănătate**

*Multiple Choice – Alegere multiplă*

> In the Python LB, mark_failure() increments fails and marks the backend down when fails >= passive_failures. If passive_failures=2, after how many consecutive failures is the backend marked down? [În echilibratorul Python, mark_failure() incrementează fails și marchează serverul ca inactiv când fails >= passive_failures. Dacă passive_failures=2, după câte eșecuri consecutive este serverul marcat ca inactiv?]

- **a)** After 2 consecutive failures, since the condition fails >= 2 becomes true at that point [După 2 eșecuri consecutive, deoarece condiția fails >= 2 devine adevărată în acel moment]
- **b)** The backend is never marked down — passive_failures only logs warnings without action [Serverul nu este niciodată marcat ca inactiv — passive_failures doar jurnalizează avertismente fără acțiune]
- **c)** After 3 failures, because >= actually requires one extra failure beyond the threshold [După 3 eșecuri, deoarece >= necesită de fapt un eșec suplimentar peste prag]
- **d)** After 1 failure, because the >= operator triggers on the first increment above zero [După 1 eșec, deoarece operatorul >= se declanșează la prima incrementare peste zero]

<details><summary>💡 Feedback</summary>

Nginx marks the backend as down on the second consecutive failure (fails reaches 2, satisfying >= 2). After marking, down_until is set to current_time + fail_timeout_s. [Serverul este marcat ca inactiv la al doilea eșec consecutiv (fails ajunge la 2, satisfăcând >= 2). După marcare, down_until este setat la timpul_curent + fail_timeout_s.]

</details>

---

### Q45. `N11.S01.Q04`
**Build Response Content-Length Calculation / Calcularea Content-Length în construcția răspunsului**

*Multiple Choice – Alegere multiplă*

> The backend server builds the body string f"Backend {backend_id} | Host: {hostname} | Time: {timestamp} | Request #{request_count}\n". The Content-Length header is set to len(body_bytes). Why is body_bytes used instead of len(body)? [Serverul construiește șirul body f"Backend {backend_id} | Host: {hostname} | Time: {timestamp} | Request #{request_count}\n". Antetul Content-Length este setat la len(body_bytes). De ce se folosește body_bytes în loc de len(body)?]

- **a)** Content-Length counts octets, not characters — encoded bytes ensure accuracy for multi-byte encodings [Content-Length numără octeți, nu caractere — octeții codificați asigură acuratețea pentru codificări multi-octet]
- **b)** Python strings are immutable, so only bytes objects can be measured for HTTP purposes [Șirurile Python sunt imuabile, deci doar obiectele bytes pot fi măsurate pentru scopuri HTTP]
- **c)** The HTTP protocol requires Content-Length to be a hexadecimal value derived from bytes [Protocolul HTTP necesită ca Content-Length să fie o valoare hexazecimală derivată din octeți]
- **d)** Using len(body) on the string would count escape sequences as single characters, understating the true byte size that the HTTP Content-Length must reflect [Folosirea len(body) pe șirul de caractere ar număra secvențele de escape ca un singur caracter, subestimând dimensiunea reală în octeți pe care Content-Length din HTTP trebuie să o reflecte]

<details><summary>💡 Feedback</summary>

HTTP Content-Length specifies the body size in bytes, not characters. For ASCII text they are equal, but UTF-8 multi-byte characters would cause a mismatch. Using the encoded bytes ensures accuracy. [HTTP Content-Length specifică dimensiunea corpului în octeți, nu caractere. Pentru text ASCII sunt egale, dar caracterele UTF-8 multi-octet ar cauza o nepotrivire. Folosirea octeților codificați asigură acuratețea.]

</details>

---

### Q46. `N11.S01.Q05`
**Backend Server SO_REUSEADDR Purpose / Scopul SO_REUSEADDR în serverul backend**

*Multiple Choice – Alegere multiplă*

> The backend server calls server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) before binding. What problem does this solve? [Serverul backend apelează server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) înainte de legare. Ce problemă rezolvă acest lucru?]

- **a)** It enables the socket to accept connections from multiple clients simultaneously [Permite socket-ului să accepte conexiuni de la mai mulți clienți simultan]
- **b)** It disables Nagle's algorithm to reduce latency for small HTTP response packets [Dezactivează algoritmul Nagle pentru a reduce latența pentru pachetele mici de răspuns HTTP]
- **c)** It allows binding to a port still in TIME_WAIT state from a previous process instance [Permite legarea la un port încă în starea TIME_WAIT de la o instanță anterioară a procesului]
- **d)** It increases the maximum buffer size for receiving large HTTP request bodies [Crește dimensiunea maximă a buffer-ului pentru primirea corpurilor mari de cereri HTTP]

<details><summary>💡 Feedback</summary>

SO_REUSEADDR allows the server to bind immediately after a restart, even if the previous socket is still in TIME_WAIT state. Without it, restarting the backend would fail with 'Address already in use' for up to 60 seconds. [SO_REUSEADDR permite serverului să se lege imediat după o repornire, chiar dacă socket-ul anterior este încă în starea TIME_WAIT. Fără aceasta, repornirea serverului ar eșua cu 'Address already in use' până la 60 de secunde.]

</details>

---

### Q47. `N11.S01.Q06`
**Weighted Round-Robin Expanded List Pattern / Modelul listei extinse round-robin ponderat**

*Multiple Choice – Alegere multiplă*

> A weighted round-robin implementation uses an expanded list: backends = {"web1": 3, "web2": 2, "web3": 1} produces ["web1","web1","web1","web2","web2","web3"]. What is the 5th request routed to? [O implementare round-robin ponderată folosește o listă extinsă: backends = {"web1": 3, "web2": 2, "web3": 1} produce ["web1","web1","web1","web2","web2","web3"]. Către ce server este direcționată a 5-a cerere?]

- **a)** web1, because the first three slots always absorb the majority of early requests [web1, deoarece primele trei sloturi absorb întotdeauna majoritatea cererilor timpurii]
- **b)** web3, because the algorithm distributes to the lowest-weight backend every fifth cycle [web3, deoarece algoritmul distribuie către serverul cu ponderea cea mai mică la fiecare al cincilea ciclu]
- **c)** web2, because index 4 in the expanded list falls within the web2 segment [web2, deoarece indexul 4 în lista extinsă se află în segmentul web2]
- **d)** Cannot be determined without knowing the current value of the internal counter state [Nu poate fi determinat fără a cunoaște valoarea curentă a stării contorului intern]

<details><summary>💡 Feedback</summary>

Indexing from 0: positions 0,1,2 → web1; positions 3,4 → web2; position 5 → web3. The 5th request (index 4) goes to web2. [Indexând de la 0: pozițiile 0,1,2 → web1; pozițiile 3,4 → web2; poziția 5 → web3. A 5-a cerere (index 4) merge la web2.]

</details>

---

### Q48. `N11.S02.Q01`
**Nginx upstream Directive Purpose / Scopul directivei upstream Nginx**

*Multiple Choice – Alegere multiplă*

> Examining nginx.conf, what is the role of the upstream backend_pool { ... } block? [Analizând nginx.conf, care este rolul blocului upstream backend_pool { ... }?]

- **a)** It configures the upstream bandwidth limit for incoming client connections [Configurează limita de lățime de bandă din amonte pentru conexiunile de intrare ale clienților]
- **b)** It specifies the DNS upstream resolver addresses for the Nginx worker processes [Specifică adresele resolverului DNS din amonte pentru procesele worker Nginx]
- **c)** It declares the TLS certificate chain used for upstream encrypted communication [Declară lanțul de certificate TLS folosit pentru comunicarea criptată din amonte]
- **d)** It defines the pool of backend servers available for load-balanced request distribution [Definește grupul de servere backend disponibile pentru distribuția echilibrată a cererilor]

<details><summary>💡 Feedback</summary>

An upstream block defines a group of backend servers that Nginx can distribute requests to. It specifies the servers, their weights, and the load balancing algorithm. [Blocul upstream definește un grup de servere backend către care Nginx poate distribui cererile. Specifică serverele, ponderile lor și algoritmul de echilibrare a încărcării.]

</details>

---

### Q49. `N11.S02.Q02`
**Docker Compose Service Dependency / Dependența de serviciu Docker Compose**

*Multiple Choice – Alegere multiplă*

> The lab's docker-compose.nginx.yml declares depends_on: [web1, web2, web3] for the nginx service. What does this ensure? [Fișierul docker-compose.nginx.yml din laborator declară depends_on: [web1, web2, web3] pentru serviciul nginx. Ce asigură acest lucru?]

- **a)** It creates a network link between nginx and the backends that would not exist otherwise [Creează o legătură de rețea între nginx și servere care nu ar exista altfel]
- **b)** Docker starts the backend containers before starting nginx, but does not guarantee backend readiness [Docker pornește containerele backend înainte de a porni nginx, dar nu garantează pregătirea serverelor]
- **c)** It guarantees that all backends are fully healthy and responding to HTTP requests before nginx starts accepting client connections [Garantează că toate serverele sunt complet sănătoase și răspund la cereri HTTP înainte ca nginx să înceapă să accepte conexiuni de la clienți]
- **d)** It binds the nginx container to use the same IP address as the backend containers [Leagă containerul nginx să folosească aceeași adresă IP ca și containerele backend]

<details><summary>💡 Feedback</summary>

depends_on controls startup order, but it does not guarantee that an application is ready to serve traffic. [depends_on controlează ordinea de pornire, dar nu garantează că aplicația este deja gata să servească trafic.]

</details>

---

### Q50. `N11.S02.Q04`
**Nginx Configuration Test Command / Comanda de testare a configurației Nginx**

*Multiple Choice – Alegere multiplă*

> Before reloading Nginx, you want to verify the configuration syntax. Which command tests the configuration without applying changes? [Înainte de reîncărcarea Nginx, doriți să verificați sintaxa configurației. Ce comandă testează configurația fără a aplica modificări?]

- **a)** nginx -s reload, which safely validates before applying any configuration changes [nginx -s reload, care validează în siguranță înainte de aplicarea oricăror modificări]
- **b)** nginx -t, which validates syntax and reports errors without affecting the running process [nginx -t, care validează sintaxa și raportează erori fără a afecta procesul în execuție]
- **c)** nginx --check, the dedicated syntax validation flag in the Nginx command suite [nginx --check, indicatorul dedicat de validare a sintaxei în suita de comenzi Nginx]
- **d)** nginx -V, which displays version information and validates the active configuration [nginx -V, care afișează informații despre versiune și validează configurația activă]

<details><summary>💡 Feedback</summary>

nginx -t tests the configuration syntax and reports errors without modifying the running server. nginx -s reload applies changes; nginx -V shows compile options. [nginx -t testează sintaxa configurației și raportează erori fără a modifica serverul în execuție. nginx -s reload aplică modificări; nginx -V arată opțiunile de compilare.]

</details>

---

### Q51. `N11.S02.Q05`
**Nginx X-Served-By Header Source / Sursa antetului X-Served-By Nginx**

*Multiple Choice – Alegere multiplă*

> The Week 11 nginx.conf includes add_header X-Served-By $upstream_addr always;. What value does the client see in this header? [Fișierul nginx.conf din săptămâna 11 include add_header X-Served-By $upstream_addr always;. Ce valoare vede clientul în acest antet?]

- **a)** The round-robin counter value indicating the position in the distribution sequence [Valoarea contorului round-robin indicând poziția în secvența de distribuție]
- **b)** The public hostname of the Nginx load balancer itself as configured in server_name [Numele de gazdă public al echilibratorului de încărcare Nginx însuși conform server_name]
- **c)** The total number of requests processed by the upstream pool since the last restart [Numărul total de cereri procesate de grupul din amonte de la ultima repornire]
- **d)** The IP address and port of the specific backend server that processed the request [Adresa IP și portul serverului specific care a procesat cererea]

<details><summary>💡 Feedback</summary>

The $upstream_addr variable contains the IP address and port of the backend that actually served the request. This allows verifying which backend handled each request when testing load distribution. [Variabila $upstream_addr conține adresa IP și portul serverului care a servit efectiv cererea. Aceasta permite verificarea care server a gestionat fiecare cerere la testarea distribuției încărcării.]

</details>

---

### Q52. `N11.S02.Q06`
**Lab Service Port Mapping Convention / Convenția de mapare a porturilor serviciilor de laborator**

*Multiple Choice – Alegere multiplă*

> The Week 11 lab maps Nginx container port 80 to host port 8080 (ports: "8080:80"). Why is port 9000 never used for lab services? [Laboratorul din săptămâna 11 mapează portul 80 al containerului Nginx la portul host 8080 (ports: "8080:80"). De ce nu este folosit niciodată portul 9000 pentru serviciile de laborator?]

- **a)** Port 9000 exceeds the range supported by Docker Compose port mapping configuration [Portul 9000 depășește intervalul suportat de configurarea mapării porturilor Docker Compose]
- **b)** Port 9000 is blocked by the Windows firewall and cannot be mapped through WSL [Portul 9000 este blocat de paravanul de protecție Windows și nu poate fi mapat prin WSL]
- **c)** Port 9000 is reserved for Portainer, the persistent Docker management service across all weeks [Portul 9000 este rezervat pentru Portainer, serviciul persistent de gestionare Docker din toate săptămânile]
- **d)** Port 9000 is a well-known protocol port assigned to a specific IANA-registered service [Portul 9000 este un port de protocol bine-cunoscut atribuit unui serviciu specific înregistrat IANA]

<details><summary>💡 Feedback</summary>

Port 9000 is permanently reserved for Portainer, the Docker management interface that runs as a global service across all lab weeks. Using it for any other service would create a port conflict. [Portul 9000 este rezervat permanent pentru Portainer, interfața de gestionare Docker care rulează ca serviciu global în toate săptămânile de laborator. Folosirea lui pentru orice alt serviciu ar crea un conflict de porturi.]

</details>

---

### Q53. `N11.S02.Q07`
**Failover Trigger Conditions in Nginx / Condițiile de declanșare a failover-ului în Nginx**

*Multiple Choice – Alegere multiplă*

> The nginx.conf file contains the directive proxy_next_upstream error timeout invalid_header http_502 http_503 http_504; is configured. A client request reaches backend web2, which returns HTTP 500. What happens next? [Fișierul nginx.conf conține directiva proxy_next_upstream error timeout invalid_header http_502 http_503 http_504; este configurată. O cerere a clientului ajunge la backend-ul web2, care returnează HTTP 500. Ce se întâmplă în continuare?]

- **a)** Nginx marks web2 as permanently down and removes it from the upstream pool for subsequent requests [Nginx marchează web2 ca permanent indisponibil și îl elimină din pool-ul upstream pentru cererile ulterioare]
- **b)** Nginx automatically retries the request on web1 or web3 since any 5xx error triggers the failover mechanism [Nginx reîncearcă automat cererea pe web1 sau web3 deoarece orice eroare 5xx declanșează mecanismul de failover]
- **c)** Nginx delivers the HTTP 500 response to the client because 500 is not in the proxy_next_upstream list [Nginx livrează răspunsul HTTP 500 clientului deoarece 500 nu figurează în lista proxy_next_upstream]
- **d)** Nginx transforms the 500 into a 502 Bad Gateway before sending it to the client as a normalised error [Nginx transformă 500 într-un 502 Bad Gateway înainte de a-l trimite clientului ca eroare normalizată]

<details><summary>💡 Feedback</summary>

Nginx's proxy_next_upstream directive specifies which upstream failures trigger a retry on the next backend. HTTP 500 is absent from the configured list (error, timeout, invalid_header, http_502, http_503, http_504), so Nginx forwards the 500 response directly to the client without attempting another backend. [Directiva proxy_next_upstream specifică ce erori ale upstream-ului declanșează reîncercarea pe alt backend. HTTP 500 lipsește din lista configurată (error, timeout, invalid_header, http_502, http_503, http_504), deci Nginx transmite răspunsul 500 direct clientului fără a încerca alt backend.]

</details>

---

### Q54. `N11.S03.Q01`
**Wireshark Interface Selection for Docker Traffic / Selectarea interfeței Wireshark pentru traficul Docker**

*Multiple Choice – Alegere multiplă*

> To capture traffic between Docker containers running in WSL, which Wireshark capture interface should you select? [Pentru a captura traficul între containerele Docker care rulează în WSL, ce interfață de captură Wireshark trebuie selectată?]

- **a)** Any interface works — Wireshark automatically detects and captures Docker traffic universally [Orice interfață funcționează — Wireshark detectează și capturează automat traficul Docker universal]
- **b)** The physical Ethernet adapter, since Docker traffic exits through the hardware NIC [Adaptorul fizic Ethernet, deoarece traficul Docker iese prin placa de rețea hardware]
- **c)** Loopback Adapter, because all Docker containers communicate via localhost only [Adaptorul Loopback, deoarece toate containerele Docker comunică doar prin localhost]
- **d)** vEthernet (WSL), because Docker container traffic in WSL traverses this virtual interface [vEthernet (WSL), deoarece traficul containerelor Docker din WSL traversează această interfață virtuală]

<details><summary>💡 Feedback</summary>

Docker containers in WSL generate traffic visible on the vEthernet (WSL) virtual interface. The physical Ethernet/Wi-Fi adapter carries only host traffic; the Loopback adapter only handles 127.0.0.1. [Containerele Docker din WSL generează trafic vizibil pe interfața virtuală vEthernet (WSL). Adaptorul fizic Ethernet/Wi-Fi transportă doar traficul gazdei; adaptorul Loopback gestionează doar 127.0.0.1.]

</details>

---

### Q55. `N11.S03.Q02`
**Wireshark Display Filter for HTTP on Port 8080 / Filtrul de afișare Wireshark pentru HTTP pe portul 8080**

*Multiple Choice – Alegere multiplă*

> You want to see only HTTP traffic on the load balancer port in Wireshark. Which display filter is appropriate? [Doriți să vedeți doar traficul HTTP pe portul echilibratorului de încărcare în Wireshark. Ce filtru de afișare este adecvat?]

- **a)** tcp.dstport == 8080 || udp.dstport == 8080, covering both transport protocols [tcp.dstport == 8080 || udp.dstport == 8080, acoperind ambele protocoale de transport]
- **b)** tcp.port == 8080 and http [tcp.port == 8080 and http]
- **c)** http.port == 8080, filtering specifically on the HTTP protocol port field [http.port == 8080, filtrând specific pe câmpul portului protocolului HTTP]
- **d)** port 8080, the simplified syntax that Wireshark accepts directly [port 8080, sintaxa simplificată pe care Wireshark o acceptă direct]

<details><summary>💡 Feedback</summary>

The filter tcp.port == 8080 and http combines a port filter with the HTTP dissector to show only HTTP traffic on port 8080. [Filtrul tcp.port == 8080 and http combină un filtru de port cu disectorul HTTP pentru a afișa doar traficul HTTP pe portul 8080.]

</details>

---

### Q56. `N11.S03.Q03`
**DNS Query Display Filter / Filtrul de afișare pentru interogări DNS**

*Multiple Choice – Alegere multiplă*

> To display only DNS query packets (not responses) in Wireshark, which filter should be applied? [Pentru a afișa doar pachetele de interogare DNS (nu răspunsurile) în Wireshark, ce filtru trebuie aplicat?]

- **a)** dns.query, a shorthand filter for DNS query messages in Wireshark [dns.query, un filtru prescurtat pentru mesajele de interogare DNS în Wireshark]
- **b)** dns.flags.response == 0, which matches only outgoing query packets [dns.flags.response == 0, care potrivește doar pachetele de interogare de ieșire]
- **c)** dns.type == query, using the type field to distinguish queries from responses [dns.type == query, folosind câmpul tip pentru a distinge interogările de răspunsuri]
- **d)** udp.port == 53 and tcp.flags.syn == 1, combining DNS port with connection initiation [udp.port == 53 and tcp.flags.syn == 1, combinând portul DNS cu inițierea conexiunii]

<details><summary>💡 Feedback</summary>

The filter dns.flags.response == 0 shows only DNS queries. Setting it to 1 would show only responses. The plain dns filter shows all DNS traffic. [Filtrul dns.flags.response == 0 afișează doar interogările DNS. Setarea la 1 ar afișa doar răspunsurile. Filtrul simplu dns afișează tot traficul DNS.]

</details>

---

### Q57. `N11.S03.Q04`
**Verifying Load Distribution with curl / Verificarea distribuției încărcării cu curl**

*Multiple Choice – Alegere multiplă*

> The command for i in {1..6}; do curl -s http://localhost:8080/; done is used to test the load balancer. With 3 backends in round-robin mode, what output pattern should appear? [Comanda for i in {1..6}; do curl -s http://localhost:8080/; done este folosită pentru a testa echilibratorul de încărcare. Cu 3 servere în modul round-robin, ce model de ieșire ar trebui să apară?]

- **a)** Random distribution with approximately 2 requests per backend but no predictable order [Distribuție aleatorie cu aproximativ 2 cereri per server dar fără ordine previzibilă]
- **b)** A repeating cycle: Backend 1 → 2 → 3 → 1 → 2 → 3, with each backend serving twice [Un ciclu repetitiv: Backend 1 → 2 → 3 → 1 → 2 → 3, fiecare server servind de două ori]
- **c)** Three pairs: requests 1-2 to Backend 1, requests 3-4 to Backend 2, requests 5-6 to Backend 3 [Trei perechi: cererile 1-2 la Backend 1, cererile 3-4 la Backend 2, cererile 5-6 la Backend 3]
- **d)** All 6 requests go to Backend 1, because round-robin exhausts one server before rotating [Toate cele 6 cereri merg la Backend 1, deoarece round-robin epuizează un server înainte de rotație]

<details><summary>💡 Feedback</summary>

Round-robin distributes sequentially: Backend 1, Backend 2, Backend 3, Backend 1, Backend 2, Backend 3. Each backend receives exactly 2 requests in this ideal scenario. [Round-robin distribuie secvențial: Backend 1, Backend 2, Backend 3, Backend 1, Backend 2, Backend 3. Fiecare server primește exact 2 cereri în acest scenariu ideal.]

</details>

---

### Q58. `N11.S03.Q05`
**DNS Client Query Construction / Construcția interogării clientului DNS**

*Multiple Choice – Alegere multiplă*

> The Week 11 DNS client encodes the domain "www.ase.ro" using length-prefixed labels. How many total bytes does the encoded QNAME occupy (including the null terminator)? [Clientul DNS din săptămâna 11 codifică domeniul "www.ase.ro" folosind etichete prefixate cu lungimea. Câți octeți ocupă în total QNAME-ul codificat (inclusiv terminatorul null)?]

- **a)** 8 bytes: DNS uses compression so only the first occurrence of common labels is stored [8 octeți: DNS folosește compresie deci doar prima apariție a etichetelor comune este stocată]
- **b)** 10 bytes: the raw ASCII characters of www.ase.ro including the two dot separators [10 octeți: caracterele ASCII brute ale www.ase.ro inclusiv cele două separatoare punct]
- **c)** 14 bytes: each label includes both a length byte and a null terminator after the text [14 octeți: fiecare etichetă include atât un octet de lungime cât și un terminator null după text]
- **d)** 12 bytes: three length-prefixed labels (4+4+3) plus the root null terminator (1) [12 octeți: trei etichete prefixate cu lungimea (4+4+3) plus terminatorul null root (1)]

<details><summary>💡 Feedback</summary>

Encoding: \x03www (4 bytes) + \x03ase (4 bytes) + \x02ro (3 bytes) + \x00 (1 byte) = 12 bytes total. Each label is preceded by its length byte. [Codificarea: \x03www (4 octeți) + \x03ase (4 octeți) + \x02ro (3 octeți) + \x00 (1 octet) = 12 octeți total. Fiecare etichetă este precedată de octetul său de lungime.]

</details>

---

### Q59. `N11.S03.Q06`
**Python vs Nginx Performance Comparison / Comparația de performanță Python vs Nginx**

*Multiple Choice – Alegere multiplă*

> When benchmarking the Python load balancer from the lab exercises against Nginx, which typically achieves higher throughput and why? [La evaluarea comparativă a echilibratorului de încărcare Python din exercițiile de laborator față de Nginx, care atinge de obicei un debit mai mare și de ce?]

- **a)** Python, because its threading model handles concurrent connections more efficiently than C [Python, deoarece modelul său de threading gestionează conexiunile concurente mai eficient decât C]
- **b)** Both achieve comparable throughput since the network I/O is the true bottleneck, not the language [Ambele ating un debit comparabil deoarece I/O-ul de rețea este blocajul real, nu limbajul]
- **c)** Nginx, because its optimised C code and event-driven architecture vastly outperform interpreted Python [Nginx, deoarece codul său C optimizat și arhitectura bazată pe evenimente depășesc cu mult Python-ul interpretat]
- **d)** The result depends entirely on the algorithm selected — Python wins with round-robin due to simpler scheduling overhead, while Nginx outperforms only with least_conn [Rezultatul depinde în întregime de algoritmul selectat — Python câștigă cu round-robin datorită costului de planificare mai simplu, în timp ce Nginx depășește doar cu least_conn]

<details><summary>💡 Feedback</summary>

Nginx typically achieves 10x+ more requests per second than the Python implementation. Nginx is written in optimised C with an asynchronous event-driven architecture, while Python's GIL and interpreted execution create bottlenecks. [Nginx atinge de obicei de peste 10 ori mai multe cereri pe secundă decât implementarea Python. Nginx este scris în C optimizat cu o arhitectură asincronă bazată pe evenimente, în timp ce GIL-ul Python și execuția interpretată creează blocaje.]

</details>

---

### Q60. `N11.S03.Q07`
**Docker Network Inspect for Container IP Discovery / Docker network inspect pentru descoperirea IP-urilor containerelor**

*True/False – Adevărat/Fals*

> Running docker network inspect lbnet displays the IP addresses assigned to each container connected to that network. [Executarea comenzii docker network inspect lbnet afișează adresele IP atribuite fiecărui container conectat la rețeaua respectivă.]

- **a)** True / Adevărat
- **b)** False / Fals

<details><summary>💡 Feedback</summary>

This command is a useful way to discover container details (including IPs) for a specific Docker network. [Comanda este utilă pentru a vedea detalii despre containere (inclusiv IP-uri) într-o rețea Docker anume.]

</details>

---
