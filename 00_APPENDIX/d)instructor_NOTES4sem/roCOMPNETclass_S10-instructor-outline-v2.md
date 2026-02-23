# Seminar S10 — DNS și SSH în containere Docker

| | |
|---|---|
| **Curs** | Rețele de Calculatoare — COMPNET |
| **Kit / repo** | `compnet-2025-redo` · `04_SEMINARS/S10/` |
| **Infra** | MININET-SDN (VM Ubuntu 24.04, VirtualBox) |
| **Durată țintă** | 35–40 min |
| **Ideea-cheie** | DNS (Domain Name System) și SSH (Secure Shell) nu sunt „setări" — sunt protocoale observabile, cu mesaje pe care le poți captura, interpreta și automatiza. |

> Varianta de predare în mediul MININET-SDN (VM Linux).

---

## Obiective operaționale

La finalul seminarului, studentul va putea:

1. Interpreta o rezolvare DNS — nume cerut, tip, adresă, TTL (Time To Live) — folosind `dig`.
2. Distinge între DNS-ul intern Docker (service discovery în rețeaua Compose) și un server DNS custom containerizat.
3. Iniția o sesiune SSH către un container și executa automatizări cu Paramiko (exec + SFTP).
4. Configura un tunel `ssh -L` și demonstra — prin captură tshark — diferența dintre trafic HTTP vizibil (port local) și trafic SSH criptat (port tunel).

---

## Structura seminarului

| Bloc | Segment | Durată | Ce face instructorul | Ce face studentul |
|---|---|---|---|---|
| **A** | Hook + activare | 3 min | Scenariu concret, 2 predicții | Răspunde, formulează așteptări |
| **B** | DNS rapid — `dig` | 6 min | Demo `dig`, interpretare TTL | Observă, confirmă/infirmă predicție |
| **C** | Docker DNS vs DNS custom | 13 min | Compose up, rezolvare internă, query 5353, captură tshark | Predicție „merge / nu merge", observă output |
| **D** | SSH + Paramiko | 8 min | SSH manual + rulare script Paramiko | Identifică fișiere generate |
| **E** | SSH port forwarding + captură | 7 min | Tunel `ssh -L`, curl, captură HTTP vs SSH | Predicție „ce vede Wireshark", observă |
| **F** | Recap + temă | 3 min | Returnare hook, fixare 3 idei, temă | Notează livrabile |
| | **Total** | **40 min** | | |

---

## Bloc A — „Poate web-ul tău să ajungă la web-ul meu?" (0'–3')

> *▸ „Am două containere: unul se numește `web`, celălalt `debug`. Din `debug`, scriu `ping web` — merge. De pe VM, scriu `ping web` — nu merge. De ce? Și dacă trimit HTTP prin SSH, mai poate cineva din exterior să citească URL-ul?"*

**Predicții (mâna ridicată / răspuns rapid):**

1. „`ping web` de pe host — merge sau nu?"
2. „HTTP trimis prin SSH — Wireshark mai vede conținutul?"

**Context rapid (30 s):**

> *▸ „La S08–S09 am construit servere HTTP și am lucrat cu Docker Compose. Azi adăugăm două servicii pe care le folosim zilnic fără să le vedem: DNS — cum găsesc destinația? SSH — cum ajung sigur la ea?"*

**De ce contează:** Ancorarea e într-un conflict cognitiv dublu (același string rezolvabil/nerezolvabil; aceleași date vizibile/invizibile). Ambele întrebări revin la Bloc F.

---

## Bloc B — DNS: de la nume la IP, observabil (3'–9')

**Obiectiv:** Fixare repere QUESTION / ANSWER / TTL; DNS ca protocol cu mesaje, nu ca „setare".

> *▸ „`dig` nu e doar un ping mai deștept. Este un client DNS complet: îi spui ce nume cauți, el trimite un mesaj UDP pe portul 53, primește răspunsul și ți-l descompune."*

**🔵 Terminal A (host VM):**
```bash
dig example.com A +noall +answer
```

**Output așteptat (aproximativ):**
```
example.com.		86400	IN	A	93.184.216.34
```

**Interpretare pe ecran:** FQDN (Fully Qualified Domain Name), TTL în secunde, tipul (A = IPv4), adresa IP.

> *▸ „TTL-ul spune cât timp un cache poate reține răspunsul. Rulați din nou peste 30 de secunde — TTL-ul scade."*

**Mini-predicție (POE):**

Întrebare: „Dacă schimb DNS-ul la `@1.1.1.1`, obțin aceeași adresă?"

```bash
dig @1.1.1.1 example.com A +noall +answer
```

Observație: aceeași adresă IP, dar TTL-ul poate diferi (cache diferit).

**Punchline:** DNS este un protocol standardizat (RFC 1035); mesajele circulă în clar pe UDP 53 — ușor de inspectat, ușor de interceptat.

---

## Bloc C — Docker DNS intern vs DNS custom (9'–22')

### C1) Ridică infrastructura DNS (2 min)

> *▸ „În Docker Compose, fiecare proiect creează o rețea virtuală. Numele serviciilor din `docker-compose.yml` devin rezolvabile — dar numai înăuntru."*

**🔵 Terminal A:**
```bash
cd 04_SEMINARS/S10/2_dns-containers
ls
```

Atrage atenția: `S10_Part02_Config_Docker_Compose.yml`, `S10_Part02_Script_DNS_Server.py`, `S10_Part02_Config_Dockerfile`.

```bash
docker compose -f S10_Part02_Config_Docker_Compose.yml up --build -d
docker compose -f S10_Part02_Config_Docker_Compose.yml ps
```

Servicii vizibile: `web`, `dns-server`, `debug`.

### C2) DNS intern — service discovery (3 min)

**Predicție:** „Containerul `debug` poate rezolva numele `web`?"

**🟢 Terminal A (intră în container debug):**
```bash
docker compose -f S10_Part02_Config_Docker_Compose.yml exec debug sh
```

În shell-ul busybox:
```sh
cat /etc/resolv.conf
# Caută 127.0.0.11 — resolver-ul intern Docker
nslookup web
nslookup dns-server
ping -c 1 web
exit
```

**Ce subliniezi:** `127.0.0.11` = DNS-ul integrat Docker. Numele `web` primește IP-ul containerului din rețeaua Compose.

### C3) Conflict cognitiv — „web" pe host (30 s)

**🔵 Terminal A (host VM):**
```bash
ping -c 1 web || echo "«web» nu există în DNS-ul host-ului."
```

> *▸ „Același string — `web` — are sens sau nu, în funcție de spațiul de nume în care ești. Service discovery Docker e local și contextual."*

**Legătură:** Aceasta vizează concepția greșită #6 (localhost nu e global) și #5 (porturi nu se expun automat).

### C4) DNS custom — interogare pe 5353/UDP (4 min)

> *▸ „Serverul DNS din kit e scris în Python cu `dnslib`. Ascultă pe 5353/UDP și răspunde unui singur domeniu: `myservice.lab.local` → `10.10.10.10`. E un DNS de jucărie, dar mecanismul e real."*

**🔵 Terminal A:**
```bash
dig @127.0.0.1 -p 5353 myservice.lab.local A +noall +answer
```

**Output așteptat:**
```
myservice.lab.local.	30	IN	A	10.10.10.10
```

**Predicție (capcană):** „Ce se întâmplă dacă întreb un nume pe care serverul nu îl cunoaște?"

```bash
dig @127.0.0.1 -p 5353 inexistent.lab.local A +noall +answer
```

**Observație:** Răspuns valid, dar fără secțiune ANSWER — serverul returnează „nu știu" conform protocolului.

### C5) Captură tshark — DNS în clar (3 min)

**🟠 Terminal B (captură):**
```bash
sudo tshark -i any -f "udp port 5353" -a duration:8 -w /tmp/s10_dns_5353.pcapng
```

**🔵 Terminal A (în timpul capturii):**
```bash
dig @127.0.0.1 -p 5353 myservice.lab.local A
```

**🟠 Terminal B (interpretare):**
```bash
tshark -r /tmp/s10_dns_5353.pcapng -Y dns -T fields \
  -e frame.time_relative -e ip.src -e ip.dst -e dns.qry.name -e dns.a
```

**Epifanie:** „DNS circulă în clar: vedeți numele cerut și IP-ul primit, exact ca în output-ul `dig`. De aceea DNS poate fi și suprafață de atac — orice intermediar vede ce domenii accesați."

### C6) Oprire (15 s)

```bash
docker compose -f S10_Part02_Config_Docker_Compose.yml down
```

> *▸ „Oprim fiecare mini-laborator înainte de următorul — evităm porturi ocupate și zgomot."*

---

## Bloc D — SSH + Paramiko (22'–30')

**Tranziție:**

> *▸ „Am văzut cum DNS rezolvă «cum găsesc destinația». Acum trecem la «cum interacționez sigur cu ea» — SSH. La S01 am trimis date în clar pe TCP. SSH adaugă criptare, autentificare și posibilitatea de a transfera fișiere."*

### D1) Ridică infrastructura SSH (1 min)

**🔵 Terminal A:**
```bash
cd ../3_ssh
docker compose -f S10_Part03_Config_Docker_Compose.yml up --build -d
docker compose -f S10_Part03_Config_Docker_Compose.yml ps
```

Servicii: `ssh-server` (port 2222:22), `ssh-client`.

### D2) SSH manual — validare (1 min)

```bash
ssh -o StrictHostKeyChecking=no -p 2222 labuser@localhost "uname -a"
# parolă: labpass
```

> *▸ „Varianta manuală, utilă pentru diagnostic. Pe rețea circulă doar SSH — comanda `uname -a` nu e vizibilă unui observator."*

### D3) Paramiko — automatizare (4 min)

> *▸ „Administrarea la scară nu se face cu 1000 de terminale deschise. Se face cu biblioteci: Paramiko implementează protocolul SSH2 în Python — conectare, exec_command, SFTP."*

**Observație importantă pentru instructor:** Scriptul `S10_Part03_Script_Paramiko_Client.py` conține marcaje `TODO 1/2/3`, dar codul e deja completat. Acestea sunt puncte de discuție, nu exerciții de completare. Arată fiecare secțiune și explică ce face.

**🟢 Terminal A:**
```bash
docker compose -f S10_Part03_Config_Docker_Compose.yml exec ssh-client bash
python3 S10_Part03_Script_Paramiko_Client.py
ls -l
exit
```

**Fișiere generate (în client):** `ssh_output.txt`, `local_upload_file.txt`, `downloaded_hostname.txt`.

**Verificare pe server:**
```bash
docker compose -f S10_Part03_Config_Docker_Compose.yml exec ssh-server ls -l /home/labuser/storage
```

**Punchline:** Diferența dintre „un protocol" (SSH) și „un API de programare" (Paramiko): același mecanism, dar scriptabil, repetabil, integrabil.

### D4) Oprire (15 s)

```bash
docker compose -f S10_Part03_Config_Docker_Compose.yml down
```

---

## Bloc E — SSH local port forwarding + captură (30'–37')

### E1) Ridică bastion + web intern (1 min)

> *▸ „Scenariu clasic: un bastion host expus pe SSH, iar în spatele lui servicii interne fără port public. Port forwarding le aduce pe localhost fără să deschizi porturi."*

**🔵 Terminal A:**
```bash
cd ../4_ssh-port-forwarding
docker compose -f S10_Part04_Config_Docker_Compose.yml up --build -d
docker compose -f S10_Part04_Config_Docker_Compose.yml ps
```

**Verificare internă (10 s):**
```bash
docker compose -f S10_Part04_Config_Docker_Compose.yml exec ssh-bastion \
  bash -lc "curl -s http://web:8000/ | head"
```

### E2) Tunelul `ssh -L` (2 min)

**Predicție:**

> *▸ „După tunel, `localhost:9000` se va comporta ca și cum ar fi `web:8000` din rețeaua internă Docker. Adică vom vedea pagina HTML servită de containerul `web`, deși portul 8000 nu e mapat pe host."*

**🔵 Terminal A (sesiunea rămâne activă):**
```bash
ssh -o StrictHostKeyChecking=no -p 2222 -L 9000:web:8000 labuser@localhost
# parolă: labpass
```

**🟢 Terminal B (test):**
```bash
curl -s http://localhost:9000/ | head
```

Output așteptat: HTML cu „If you can see this page through an SSH tunnel, the forwarding is working correctly."

### E3) Epifanie cu captură: HTTP vizibil vs SSH criptat (3 min)

> *▸ „Acum vine partea revelatoare: același conținut — vizibil într-un loc, invizibil în altul."*

**🟠 Terminal B — captură pe portul local 9000:**
```bash
sudo tshark -i lo -f "tcp port 9000" -a duration:8 -w /tmp/s10_http_9000.pcapng
```

**🟢 Terminal A (generează trafic în timpul capturii):**
```bash
curl http://localhost:9000/ > /dev/null
```

**🟠 Terminal B — interpretare:**
```bash
tshark -r /tmp/s10_http_9000.pcapng -Y http.request \
  -T fields -e http.host -e http.request.uri
```

Rezultat: `localhost` și `/` — HTTP în clar, decodabil.

**🟠 Terminal B — captură pe portul SSH 2222:**
```bash
sudo tshark -i lo -f "tcp port 2222" -a duration:8 -w /tmp/s10_ssh_2222.pcapng
```

(Generează trafic din nou cu `curl http://localhost:9000/ > /dev/null`.)

**🟠 Terminal B — interpretare:**
```bash
tshark -r /tmp/s10_ssh_2222.pcapng -Y ssh
```

Rezultat: pachete SSH, fără conținut HTTP interpretabil.

> *▸ „Pe portul 9000 vedeți HTTP — cererea, URI-ul, răspunsul. Pe portul 2222 vedeți SSH — pachete criptate. Tunelul nu «teleportează» datele. El schimbă locul unde datele sunt în clar: înainte de a intra în SSH (9000) și după ce ies (pe serverul intern)."*

### E4) Oprire

În terminalul cu sesiunea SSH: `exit` sau `Ctrl+C`.

```bash
docker compose -f S10_Part04_Config_Docker_Compose.yml down
```

---

## Bloc F — Recap + temă (37'–40')

**Returnare hook:**

> *▸ „La început am întrebat: «De ce `ping web` merge din container dar nu de pe host?» Răspunsul: DNS-ul intern Docker e contextual — service discovery funcționează doar în rețeaua Compose. «Wireshark mai vede HTTP prin SSH?» Răspunsul: pe portul local da, pe portul SSH nu — tunelul criptează conținutul."*

**Trei idei fixate:**

1. DNS e un protocol cu mesaje observabile — nu o setare ascunsă.
2. Numele serviciilor Docker există doar în rețeaua lor — context, nu magie.
3. SSH port forwarding aduce un serviciu intern pe localhost; criptarea ascunde conținutul de observatori externi.

**Preview S11:** „Dacă azi am accesat un singur web intern prin SSH, la S11 distribuim traficul către mai multe instanțe — load balancing cu Nginx."

### Temă

Fișierele de task din kit descriu livrabilele complet: `S10_Part01B_Tasks_Intro.md`, `S10_Part03B_Tasks_SSH_Paramiko.md`, `S10_Part04B_Tasks_SSH_Portforward.md`.

**Trei livrabile (rezumat):**

1. **DNS în Docker (1 pagină):** output pentru `nslookup web` din container + `dig @127.0.0.1 -p 5353 myservice.lab.local` de pe host + interpretare: de ce merge acolo și nu pe host.
2. **SSH + Paramiko:** output `ssh ... "uname -a"` + fișiere generate de script + 5–8 rânduri explicative (ce comenzi, ce transfer, unde apar pe server).
3. **Port forwarding:** comanda de tunel + dovada accesului la `localhost:9000` + (bonus) fișiere `.pcapng` cu filtru `http.request` vs `ssh`.

Indicați studenților și paginile HTML interactive din `_HTMLsupport/S10/` ca material de studiu suplimentar.

---

## Cheat-sheet

### DNS

| Comandă | Ce face |
|---|---|
| `dig example.com A` | Interogare A (IPv4) pentru domeniu |
| `dig @1.1.1.1 example.com` | Interogare cu DNS specificat |
| `dig @127.0.0.1 -p 5353 myservice.lab.local A` | Interogare pe port non-standard |
| `nslookup web` (în container) | Rezolvare service name Docker |
| `cat /etc/resolv.conf` | Verificare DNS resolver configurat |

### SSH

| Comandă | Ce face |
|---|---|
| `ssh -p 2222 labuser@localhost "uname -a"` | Execuție comandă remotă |
| `ssh -L 9000:web:8000 labuser@localhost -p 2222` | Tunel local: `localhost:9000` → `web:8000` |
| `ssh -o StrictHostKeyChecking=no ...` | Sare peste verificarea cheii (doar laborator!) |

### Docker Compose (cu fișiere non-standard)

| Comandă | Ce face |
|---|---|
| `docker compose -f FISIER.yml up --build -d` | Pornire cu build, detached |
| `docker compose -f FISIER.yml ps` | Status servicii |
| `docker compose -f FISIER.yml exec SERV sh` | Shell interactiv în container |
| `docker compose -f FISIER.yml down` | Oprire + curățare |

### tshark (captură)

| Comandă | Ce face |
|---|---|
| `sudo tshark -i any -f "udp port 5353" -a duration:8 -w FILE.pcapng` | Captură DNS pe 5353 |
| `sudo tshark -i lo -f "tcp port 9000" -a duration:8 -w FILE.pcapng` | Captură HTTP pe loopback |
| `tshark -r FILE.pcapng -Y dns -T fields -e dns.qry.name -e dns.a` | Citire captură DNS |
| `tshark -r FILE.pcapng -Y http.request -T fields -e http.host -e http.request.uri` | Citire captură HTTP |

### Credențiale laborator

| Parametru | Valoare |
|---|---|
| User SSH | `labuser` |
| Parolă SSH | `labpass` |
| Port SSH mapat | `2222` (host) → `22` (container) |
| Port DNS custom | `5353/UDP` |
| Domeniu DNS test | `myservice.lab.local` → `10.10.10.10` |

---

## Plan de contingență

| # | Problemă | Cauză probabilă | Soluție |
|---|---|---|---|
| 1 | `docker compose` nu găsește fișierul | Fișierele au nume non-standard | Folosește `-f S10_PartXX_Config_Docker_Compose.yml` explicit |
| 2 | `dig` nu e instalat pe VM | Pachetul `dnsutils` lipsește | `sudo apt-get update && sudo apt-get install -y dnsutils` |
| 3 | Portul 2222 ocupat | Compose anterior nu a fost oprit | `docker ps` → identifică containerul → `docker compose -f ... down` în directorul corect |
| 4 | tshark nu capturează nimic | Filtru greșit sau interfață greșită | Verifică: `-i any` (sau `-i lo` pentru loopback); confirmă portul; generează trafic *în timpul* capturii |
| 5 | `nslookup web` eșuează în container | Containerul debug nu e în aceeași rețea | Verifică cu `docker compose -f ... ps` că toate serviciile rulează |
| 6 | SSH: „Connection refused" | Serviciul sshd nu a pornit complet | Așteaptă 5–10 s după `docker compose up`; verifică cu `docker logs ssh-server` |
| 7 | tshark nu decodează HTTP pe 9000 | Port non-standard, heuristică eșuează | Adaugă `-d tcp.port==9000,http` la comanda tshark |
| 8 | `dig @127.0.0.1 -p 5353` nu răspunde | Containerul `dns-server` nu rulează sau portul nu e mapat | `docker compose -f S10_Part02_Config_Docker_Compose.yml ps`; verifică `5353:5353/udp` |

---

## Referințe

Cohen, E., & Kaplan, H. (2003). Proactive caching of DNS records: Addressing a performance bottleneck. *Computer Networks, 41*(6), 707–726. https://doi.org/10.1016/S1389-1286(02)00424-3

Jung, J., Sit, E., Balakrishnan, H., & Morris, R. (2002). DNS performance and the effectiveness of caching. *IEEE/ACM Transactions on Networking, 10*(5), 589–603. https://doi.org/10.1109/TNET.2002.803905

Mockapetris, P. (1987). *Domain names — Implementation and specification* (RFC 1035). Internet Engineering Task Force. https://doi.org/10.17487/RFC1035

Potdar, A. M., Narayan, D. G., Kengond, S., & Mulla, M. M. (2020). Performance evaluation of Docker container and virtual machine. *Procedia Computer Science, 171*, 1419–1428. https://doi.org/10.1016/j.procs.2020.04.152

Bergsma, F., Dowling, B., Kohlar, F., Schwenk, J., & Stebila, D. (2014). Multi-ciphersuite security of the Secure Shell (SSH) protocol. In M. Yung & N. Li (Eds.), *Proceedings of the 21st ACM Conference on Computer and Communications Security (CCS 2014)* (pp. 369–381). ACM. https://doi.org/10.1145/2660267.2660286

Williams, S. C. (2011). Analysis of the SSH key exchange protocol. In L. Chen (Ed.), *Cryptography and Coding (IMACC 2011)* (Lecture Notes in Computer Science, Vol. 7089, pp. 356–374). Springer. https://doi.org/10.1007/978-3-642-25516-8_22

Toledo, S. (2023). SSH tunneling to connect to remote computers. *Software Impacts, 17*, 100545. https://doi.org/10.1016/j.simpa.2023.100545

Shah, A. A., Piro, G., Grieco, L. A., & Boggia, G. (2021). A quantitative cross-comparison of container networking technologies for virtualized service infrastructures in local computing environments. *Transactions on Emerging Telecommunications Technologies, 32*(4), e4234. https://doi.org/10.1002/ett.4234

Schultz, G. (2004). SSH protocol warning: Using ssh: Do security risks outweigh the benefits? *Network Security, 2004*(10), 7–10. https://doi.org/10.1016/S1353-4858(04)00143-6

---

## Note pedagogice

**Arc cognitiv:** Hook (conflict dublu: rezolvare contextuală + opacitate SSH) → Activare (legătură S08–S09) → Conflict cognitiv (ping web merge/nu merge) → Explorare ghidată (DNS clar, captură, SSH, tunel) → Formalizare (integrată în epifanii) → Aplicare (temă cu livrabile) → Recap (returnare hook, fixare 3 idei).

**Tipare socratice folosite:**
- POE la Bloc B (predicție „aceeași adresă cu alt DNS?"), Bloc C2–C3 (predicție „web" merge/nu merge), Bloc E2 (predicție „localhost:9000 funcționează?").
- Capcană de concepție greșită la Bloc C3 (ping web pe host — eșuează contrar intuiției).
- „Ce s-ar fi întâmplat dacă...?" la Bloc C4 (întrebare domeniu necunoscut la DNS custom).

**Regula 2-blocuri-pasive:** Niciun segment depășește 2 blocuri consecutive fără interacțiune. Bloc B conține predicție; Bloc C alternează demonstrații cu predicții; Bloc D are verificare activă; Bloc E are predicție + captură.

**Adaptare timp:** Dacă rămâi fără timp, sacrifică demonstrația tshark din Bloc C5 (menționează doar că DNS e în clar) și treci direct la SSH. Port forwarding-ul (Bloc E) e cel mai motivant — nu îl sacrifica.

**TODO-uri Paramiko:** Scriptul din kit are marcaje TODO, dar codul e completat. Tratează marcajele ca puncte de discuție („Ce face linia asta?"), nu ca exerciții de completare. Tema cere studenților să modifice comanda executată sau fișierul transferat.
