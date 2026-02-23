# Seminar S10 — DNS și SSH în containere Docker

| | |
|---|---|
| **Curs** | Rețele de Calculatoare — COMPNET |
| **Kit / repo** | `compnet-2025-redo` · `04_SEMINARS/S10/` |
| **Infra** | Windows 10/11 + Docker Desktop + Wireshark (cu Npcap) |
| **Durată țintă** | 35–40 min |
| **Ideea-cheie** | DNS (Domain Name System) și SSH (Secure Shell) nu sunt „setări" — sunt protocoale observabile, cu mesaje pe care le poți captura, interpreta și automatiza. |

> Varianta de predare fără MININET-SDN: Windows nativ + Docker Desktop + Wireshark.

---

## Obiective operaționale

La finalul seminarului, studentul va putea:

1. Interpreta o rezolvare DNS — nume cerut, tip, adresă, TTL (Time To Live) — folosind `nslookup`.
2. Distinge între DNS-ul intern Docker (service discovery în rețeaua Compose) și un server DNS custom containerizat.
3. Iniția o sesiune SSH către un container și executa automatizări cu Paramiko (exec + SFTP).
4. Configura un tunel `ssh -L` și demonstra — prin captură Wireshark — diferența dintre trafic HTTP vizibil (port local) și trafic SSH criptat (port tunel).

---

## Structura seminarului

| Bloc | Segment | Durată | Ce face instructorul | Ce face studentul |
|---|---|---|---|---|
| **A** | Hook + activare | 3 min | Scenariu concret, 2 predicții | Răspunde, formulează așteptări |
| **B** | DNS rapid — `nslookup` | 5 min | Demo `nslookup`, interpretare | Observă, confirmă/infirmă predicție |
| **C** | Docker DNS vs DNS custom + Wireshark | 14 min | Compose up, rezolvare internă, query 5353, captură Wireshark | Predicție „merge / nu merge", observă |
| **D** | SSH + Paramiko | 8 min | SSH manual + rulare script Paramiko | Identifică fișiere generate |
| **E** | SSH port forwarding + captură | 7 min | Tunel `ssh -L`, curl/browser, captură HTTP vs SSH | Predicție „ce vede Wireshark", observă |
| **F** | Recap + temă | 3 min | Returnare hook, fixare 3 idei, temă | Notează livrabile |
| | **Total** | **40 min** | | |

---

## Pregătire înainte de seminar (o singură dată)

### Checklist instructor

1. **Docker Desktop** pornit — verifică iconița din system tray.
2. În PowerShell:
   ```powershell
   docker --version
   docker compose version
   ```
3. **Wireshark** instalat cu **Npcap** (opțiunea de loopback capture activă). Verifică: în Wireshark trebuie să existe o interfață *Npcap Loopback Adapter* (sau echivalent).
4. **OpenSSH Client** disponibil: `ssh -V` în PowerShell. Dacă lipsește: Settings → Optional Features → Add a feature → OpenSSH Client.
5. Două ferestre pregătite:
   - PowerShell (Terminal A)
   - Wireshark (deschis, fără captură activă)

---

## Bloc A — „Poate web-ul tău să ajungă la web-ul meu?" (0'–3')

> *▸ „Am două containere Docker: unul se numește `web`, celălalt `debug`. Din `debug`, scriu `ping web` — merge. Din PowerShell pe Windows, scriu `ping web` — nu merge. De ce? Și dacă trimit HTTP printr-un tunel SSH, mai poate cineva din exterior să citească URL-ul?"*

**Predicții (mâna ridicată / răspuns rapid):**

1. „`ping web` din PowerShell — merge sau nu?"
2. „HTTP trimis prin SSH — Wireshark mai vede conținutul?"

**Context rapid (30 s):**

> *▸ „La S08–S09 am construit servere HTTP și am lucrat cu Docker Compose. Azi adăugăm două servicii pe care le folosim zilnic fără să le vedem: DNS — cum găsesc destinația? SSH — cum ajung sigur la ea?"*

**De ce contează:** Ancorarea e într-un conflict cognitiv dublu (același string rezolvabil/nerezolvabil; aceleași date vizibile/invizibile). Ambele întrebări revin la Bloc F.

---

## Bloc B — DNS: de la nume la IP, observabil (3'–8')

**Obiectiv:** Fixare repere „ce întrebi / ce primești / cât durează răspunsul"; DNS ca protocol cu mesaje, nu ca „setare".

> *▸ „Pe Windows, instrumentul clasic de interogare DNS este `nslookup`. Nu vă cer să memorați output-ul — vă cer să identificați: ce ai întrebat, cine a răspuns, ce ai primit."*

**🔵 Terminal A (PowerShell):**
```powershell
nslookup example.com
```

**Ce interpretezi pe ecran:**
- serverul DNS folosit (de obicei router-ul sau DNS-ul ISP-ului);
- numele cerut;
- adresa IP primită.

**Mini-predicție (POE):**

Întrebare: „Dacă folosesc alt server DNS — de exemplu `1.1.1.1` — obțin aceeași adresă?"

```powershell
nslookup example.com 1.1.1.1
```

Observație: aceeași adresă IP, server diferit. DNS-ul e distribuit, dar convergent.

**Punchline:** DNS este un protocol standardizat (RFC 1035); mesajele circulă în clar pe UDP 53 — ușor de inspectat, ușor de interceptat.

---

## Bloc C — Docker DNS intern vs DNS custom + Wireshark (8'–22')

### C1) Ridică infrastructura DNS (2 min)

> *▸ „În Docker Compose, fiecare proiect creează o rețea virtuală. Numele serviciilor din fișierul compose devin rezolvabile — dar numai înăuntru."*

**🔵 Terminal A (PowerShell):**
```powershell
cd .\04_SEMINARS\S10\2_dns-containers
dir
```

Atrage atenția: `S10_Part02_Config_Docker_Compose.yml`, `S10_Part02_Script_DNS_Server.py`, `S10_Part02_Config_Dockerfile`.

```powershell
docker compose -f S10_Part02_Config_Docker_Compose.yml up --build -d
docker compose -f S10_Part02_Config_Docker_Compose.yml ps
```

Servicii vizibile: `web`, `dns-server`, `debug`.

### C2) DNS intern — service discovery (3 min)

**Predicție:** „Containerul `debug` poate rezolva numele `web`?"

**🟢 Terminal A (intră în container debug):**
```powershell
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

### C3) Conflict cognitiv — „web" pe Windows (30 s)

**🔵 Terminal A (PowerShell, pe host):**
```powershell
ping web
```

Eșuează: Windows nu știe ce e `web`.

> *▸ „Același string — `web` — are sens sau nu, în funcție de spațiul de nume în care ești. DNS-ul Docker e local și contextual."*

**Legătură:** Aceasta vizează concepția greșită #6 (localhost nu e global) și #5 (porturi nu se expun automat).

### C4) DNS custom + captură Wireshark pe 5353/UDP (5 min)

> *▸ „Serverul DNS din kit e scris în Python cu `dnslib`. Ascultă pe 5353/UDP și răspunde unui singur domeniu: `myservice.lab.local` → `10.10.10.10`. E un DNS de jucărie, dar mecanismul e real."*

**🟠 Wireshark — pregătire captură:**
1. Selectează interfața **Npcap Loopback Adapter**.
2. Display filter (nu capture filter, pentru a evita probleme pe loopback Windows): `dns`
3. Start capture.

**🔵 Terminal A (PowerShell) — interogare DNS pe 5353:**

Varianta interactivă `nslookup`:
```powershell
nslookup
```
În prompt-ul nslookup:
```text
> server 127.0.0.1
> set port=5353
> myservice.lab.local
> exit
```

**Output așteptat:** Adresa `10.10.10.10` pentru `myservice.lab.local`.

**Predicție (capcană):** „Ce se întâmplă dacă întreb un nume necunoscut?"

```text
nslookup
> server 127.0.0.1
> set port=5353
> inexistent.lab.local
> exit
```

**Observație:** Serverul răspunde fără adresă — „nu știu" conform protocolului DNS.

**🟠 Wireshark — interpretare:**
1. Oprește captura.
2. Display filter: `dns`
3. Click pe un pachet DNS → Domain Name System (query/response):
   - `Queries` → `myservice.lab.local`
   - `Answers` → `10.10.10.10`

**Epifanie:** „DNS circulă în clar: vedeți numele cerut și IP-ul primit. De aceea DNS poate fi și suprafață de atac — orice intermediar vede ce domenii accesați."

### C5) Oprire (15 s)

```powershell
docker compose -f S10_Part02_Config_Docker_Compose.yml down
```

> *▸ „Oprim fiecare mini-laborator înainte de următorul — evităm porturi ocupate și zgomot."*

---

## Bloc D — SSH + Paramiko (22'–30')

**Tranziție:**

> *▸ „Am văzut cum DNS rezolvă «cum găsesc destinația». Acum trecem la «cum interacționez sigur cu ea» — SSH. La S01 am trimis date în clar pe TCP. SSH adaugă criptare, autentificare și posibilitatea de a transfera fișiere."*

### D1) Ridică infrastructura SSH (1 min)

**🔵 Terminal A (PowerShell):**
```powershell
cd ..\3_ssh
docker compose -f S10_Part03_Config_Docker_Compose.yml up --build -d
docker compose -f S10_Part03_Config_Docker_Compose.yml ps
```

Servicii: `ssh-server` (port 2222:22), `ssh-client`.

### D2) SSH manual — validare (1 min)

```powershell
ssh -o StrictHostKeyChecking=no -p 2222 labuser@localhost "uname -a"
```

Parolă: `labpass`.

> *▸ „Varianta manuală, utilă pentru diagnostic. Pe rețea circulă doar SSH — comanda `uname -a` nu e vizibilă unui observator."*

**Notă:** Dacă `ssh` nu e disponibil, activează OpenSSH Client din Settings → Optional Features.

### D3) Paramiko — automatizare (4 min)

> *▸ „Administrarea la scară nu se face cu 1000 de terminale deschise. Se face cu biblioteci: Paramiko implementează protocolul SSH2 în Python — conectare, exec_command, SFTP."*

**Observație importantă pentru instructor:** Scriptul `S10_Part03_Script_Paramiko_Client.py` conține marcaje `TODO 1/2/3`, dar codul e deja completat. Acestea sunt puncte de discuție, nu exerciții de completare. Arată fiecare secțiune și explică ce face.

**🟢 Terminal A (PowerShell):**
```powershell
docker compose -f S10_Part03_Config_Docker_Compose.yml exec ssh-client bash
python3 S10_Part03_Script_Paramiko_Client.py
ls -l
exit
```

**Fișiere generate (în client):** `ssh_output.txt`, `local_upload_file.txt`, `downloaded_hostname.txt`.

**Verificare pe server:**
```powershell
docker compose -f S10_Part03_Config_Docker_Compose.yml exec ssh-server ls -l /home/labuser/storage
```

**Punchline:** Diferența dintre „un protocol" (SSH) și „un API de programare" (Paramiko): același mecanism, dar scriptabil, repetabil, integrabil.

### D4) Oprire (15 s)

```powershell
docker compose -f S10_Part03_Config_Docker_Compose.yml down
```

---

## Bloc E — SSH local port forwarding + captură Wireshark (30'–37')

### E1) Ridică bastion + web intern (1 min)

> *▸ „Scenariu clasic: un bastion host expus pe SSH, iar în spatele lui servicii interne fără port public. Port forwarding le aduce pe localhost fără să deschizi porturi."*

**🔵 Terminal A (PowerShell):**
```powershell
cd ..\4_ssh-port-forwarding
docker compose -f S10_Part04_Config_Docker_Compose.yml up --build -d
docker compose -f S10_Part04_Config_Docker_Compose.yml ps
```

**Verificare internă (10 s):**
```powershell
docker compose -f S10_Part04_Config_Docker_Compose.yml exec ssh-bastion bash -lc "curl -s http://web:8000/ | head"
```

### E2) Tunelul `ssh -L` (2 min)

**Predicție:**

> *▸ „După tunel, `localhost:9000` se va comporta ca și cum ar fi `web:8000` din rețeaua internă Docker. Vom vedea pagina HTML servită de containerul `web`, deși portul 8000 nu e mapat pe host."*

**🔵 Terminal A (PowerShell — sesiunea rămâne activă):**
```powershell
ssh -o StrictHostKeyChecking=no -p 2222 -L 9000:web:8000 labuser@localhost
```

Parolă: `labpass`.

**🟢 Alt tab PowerShell (test):**
```powershell
curl http://localhost:9000/
```

Sau deschide în browser: `http://localhost:9000`

Output așteptat: HTML cu „If you can see this page through an SSH tunnel, the forwarding is working correctly."

### E3) Epifanie cu Wireshark: HTTP vizibil vs SSH criptat (3 min)

> *▸ „Acum vine partea revelatoare: același conținut — vizibil într-un loc, invizibil în altul."*

**🟠 Wireshark — captură pe Npcap Loopback Adapter:**
1. Display filter: `tcp.port == 9000 || tcp.port == 2222`
2. Start capture.

**🟢 PowerShell (generează trafic):**
```powershell
curl http://localhost:9000/ | Out-Null
```

**🟠 Wireshark — interpretare:**

1. Display filter: `tcp.port == 9000`
   → Ar trebui să vedeți pachete HTTP (sau TCP cu payload decodabil). Dacă Wireshark recunoaște HTTP, veți vedea `GET /...` în protocol.

2. Display filter: `tcp.port == 2222`
   → Ar trebui să vedeți pachete `SSH` — fără URL-uri, fără conținut HTTP decodabil.

> *▸ „Pe portul 9000 vedeți HTTP — cererea, conținutul. Pe portul 2222 vedeți SSH — pachete criptate. Tunelul nu «teleportează» datele. El schimbă locul unde datele sunt în clar: înainte de a intra în SSH (9000) și după ce ies (pe serverul intern)."*

### E4) Oprire

În fereastra cu sesiunea SSH: `exit` sau `Ctrl+C`.

```powershell
docker compose -f S10_Part04_Config_Docker_Compose.yml down
```

---

## Bloc F — Recap + temă (37'–40')

**Returnare hook:**

> *▸ „La început am întrebat: «De ce `ping web` merge din container dar nu din PowerShell?» Răspunsul: DNS-ul intern Docker e contextual — service discovery funcționează doar în rețeaua Compose. «Wireshark mai vede HTTP prin SSH?» Răspunsul: pe portul local da, pe portul SSH nu — tunelul criptează conținutul."*

**Trei idei fixate:**

1. DNS e un protocol cu mesaje observabile — nu o setare ascunsă.
2. Numele serviciilor Docker există doar în rețeaua lor — context, nu magie.
3. SSH port forwarding aduce un serviciu intern pe localhost; criptarea ascunde conținutul de observatori externi.

**Preview S11:** „Dacă azi am accesat un singur web intern prin SSH, la S11 distribuim traficul către mai multe instanțe — load balancing cu Nginx."

### Temă

Fișierele de task din kit descriu livrabilele complet: `S10_Part01B_Tasks_Intro.md`, `S10_Part03B_Tasks_SSH_Paramiko.md`, `S10_Part04B_Tasks_SSH_Portforward.md`.

**Trei livrabile (rezumat):**

1. **DNS în Docker (1 pagină):** output `nslookup web` din container + interogare `nslookup` pe 5353 pentru `myservice.lab.local` + interpretare: de ce merge acolo și nu din PowerShell pe host; captură Wireshark cu query/response DNS.
2. **SSH + Paramiko:** output `ssh ... "uname -a"` + fișiere generate de script + 5–8 rânduri explicative (ce comenzi, ce transfer, unde apar pe server).
3. **Port forwarding:** comanda de tunel + dovada accesului la `localhost:9000` + screenshot Wireshark: `tcp.port==9000` (HTTP vizibil) vs `tcp.port==2222` (SSH criptat).

Indicați studenților și paginile HTML interactive din `_HTMLsupport/S10/` ca material de studiu suplimentar.

---

## Cheat-sheet

### DNS

| Comandă | Ce face |
|---|---|
| `nslookup example.com` (PowerShell) | Interogare DNS pentru domeniu |
| `nslookup example.com 1.1.1.1` | Interogare cu DNS specificat |
| `nslookup` → `server 127.0.0.1` → `set port=5353` → `myservice.lab.local` | Interogare pe port non-standard (interactiv) |
| `nslookup web` (în container) | Rezolvare service name Docker |
| `cat /etc/resolv.conf` (în container) | Verificare DNS resolver configurat |

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

### Wireshark — filtre utile

| Filtru | Ce arată |
|---|---|
| `dns` | Doar pachetele DNS |
| `tcp.port == 9000` | Trafic pe portul 9000 (HTTP prin tunel) |
| `tcp.port == 2222` | Trafic SSH (criptat) |
| `tcp.port == 9000 \|\| tcp.port == 2222` | Ambele, pentru comparație |

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
| 2 | Wireshark nu are interfață loopback | Npcap neinstalat sau fără suport loopback | Reinstalează Wireshark + Npcap cu opțiunea „Install Npcap in WinPcap API-compatible Mode" și „Support raw 802.11 traffic" / „Support loopback traffic" |
| 3 | Portul 2222 ocupat | Compose anterior nu a fost oprit | `docker ps` → identifică containerul → `docker compose -f ... down` în directorul corect |
| 4 | `ssh` nu există pe Windows | OpenSSH Client neactivat | Settings → Optional Features → Add a feature → OpenSSH Client |
| 5 | `nslookup` pe 5353 nu răspunde | Containerul `dns-server` nu rulează sau portul nu e mapat | `docker compose -f S10_Part02_Config_Docker_Compose.yml ps`; verifică `5353:5353/udp` |
| 6 | SSH: „Connection refused" | Serviciul sshd nu a pornit complet | Așteaptă 5–10 s după `docker compose up`; verifică cu `docker logs ssh-server` |
| 7 | Wireshark nu decodează HTTP pe 9000 | Port non-standard, heuristică eșuează | Click dreapta pe pachet → Decode As → TCP port 9000 → HTTP |
| 8 | Docker Desktop nu pornește | Hyper-V / WSL2 backend dezactivat | Verifică: Settings → General → „Use the WSL 2 based engine" activat |

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

**Arc cognitiv:** Hook (conflict dublu: rezolvare contextuală + opacitate SSH) → Activare (legătură S08–S09) → Conflict cognitiv (ping web merge/nu merge) → Explorare ghidată (DNS clar, captură Wireshark, SSH, tunel) → Formalizare (integrată în epifanii) → Aplicare (temă cu livrabile) → Recap (returnare hook, fixare 3 idei).

**Tipare socratice folosite:**
- POE la Bloc B (predicție „aceeași adresă cu alt DNS?"), Bloc C2–C3 (predicție „web" merge/nu merge), Bloc E2 (predicție „localhost:9000 funcționează?").
- Capcană de concepție greșită la Bloc C3 (ping web pe host — eșuează contrar intuiției).
- „Ce s-ar fi întâmplat dacă...?" la Bloc C4 (întrebare domeniu necunoscut la DNS custom).

**Regula 2-blocuri-pasive:** Niciun segment depășește 2 blocuri consecutive fără interacțiune. Bloc B conține predicție; Bloc C alternează demonstrații cu predicții; Bloc D are verificare activă; Bloc E are predicție + captură.

**Diferență față de varianta VM (pentru coordonator):** `dig` → `nslookup`; `tshark` → Wireshark GUI; `ssh` identic (OpenSSH Client pe Windows); `cd ../` → `cd ..\`; captura pe loopback necesită Npcap (nu `-i any`/`-i lo`). Display filter în loc de capture filter pe loopback Windows — mai fiabil.

**Adaptare timp:** Dacă rămâi fără timp, sacrifică demonstrația Wireshark din Bloc C4 (menționează doar că DNS e în clar) și treci direct la SSH. Port forwarding-ul (Bloc E) e cel mai motivant — nu îl sacrifica.

**TODO-uri Paramiko:** Scriptul din kit are marcaje TODO, dar codul e completat. Tratează marcajele ca puncte de discuție („Ce face linia asta?"), nu ca exerciții de completare. Tema cere studenților să modifice comanda executată sau fișierul transferat.
