# Seminar S04 — Protocoale custom peste TCP/UDP: framing (text vs. binary) + state machine

| | |
|---|---|
| **Curs** | Rețele de Calculatoare — COMPNET |
| **Kit / repo** | `compnet-2025-redo` (arhiva: `claudev11_EN_compnet-2025-redo-main.zip`) |
| **Infra** | MININET-SDN VM (Ubuntu 24.04, VirtualBox) + `python3` + `tshark`/Wireshark |
| **Durată țintă** | 35–40 min |
| **Ideea-cheie** | TCP nu transmite „mesaje" — transmite bytes. „Mesajele" apar abia după ce **noi** definim framing + reguli (protocol). |

---

## Obiective operaționale

La finalul seminarului, studenții vor putea:

1. **Explica** de ce TCP, fiind un byte stream (RFC 793, §1.5), impune framing la nivel de aplicație — și să indice cel puțin două strategii de framing (prefix de lungime, delimiter).
2. **Rula și testa** un protocol text peste TCP (`add`/`get`/`remove`/`count`) și observa traficul într-o captură Wireshark.
3. **Compara** (în captură) un protocol text cu unul binar: lizibilitate, dimensiune payload, nevoie de tooling.
4. **Implementa** comanda `count` în template-ul text, testând-o end-to-end.
5. **Descrie** (cel puțin informal) ce înseamnă un protocol ca mini-spec + state machine.
6. **(Teaser)** Recunoaște cum un protocol „cu stare" funcționează peste UDP, folosind `(ip, port)` ca identitate.

---

## Structura seminarului

| Bloc | Conținut | Durată |
|:--:|---|---:|
| **A** | Hook + predicție: „două comenzi, câte `recv()`-uri?" | 2–3 min |
| **B** | Demo: protocol text TCP (exemplu) + captură scurtă | 12–13 min |
| **C** | Implementare: `count` în template + testare | 9–10 min |
| **D** | Demo: protocol binar TCP + comparație în captură | 6–7 min |
| **E** | Teaser: protocol UDP cu stare (CONNECT/SEND/LIST/DISCONNECT) | 5–6 min |
| **F** | Recap (cu revenire la hook) + temă + livrabile | 2–3 min |

> Dacă pierzi timp la capturi: scurtezi Blocul E la 2 min (doar arăți ERR_CONNECTED fără connect, fixezi ideea, restul devine temă). Blocul E poate fi deschis și la începutul S05.

---

## Fișiere din kit folosite în S04

Lucrezi din `04_SEMINARS/S04/`:

### Protocol text TCP

- `1_text-proto_tcp/S04_Part01A_Example_Text_Proto_TCP_Server.py` — server exemplu
- `1_text-proto_tcp/S04_Part01B_Example_Text_Proto_TCP_Client.py` — client exemplu
- `1_text-proto_tcp/S04_Part01C_Template_Text_Proto_TCP_Server.py` — template student (TODO: `count`)
- `1_text-proto_tcp/S04_Part01D_Scenario_Text_Proto_TCP.md` — cerințe + livrabile

### Protocol binar TCP (pickle + LEN_BYTE)

- `2_binary-proto_tcp/S04_Part02A_Example_Binary_Proto_TCP_Server.py` — server exemplu
- `2_binary-proto_tcp/S04_Part02B_Example_Binary_Proto_TCP_Client.py` — client exemplu
- `2_binary-proto_tcp/S04_Part02C_Template_Binary_Proto_TCP_Server.py` — template student (TODO: `keys`)
- `2_binary-proto_tcp/S04_Part02D_Scenario_Binary_Proto_TCP.md` — cerințe + livrabile

### Protocol UDP (message types + state machine)

- `3_proto_udp/S04_Part03A_Example_UDP_Proto_Server.py` — server exemplu
- `3_proto_udp/S04_Part03B_Example_UDP_Proto_Client.py` — client exemplu
- `3_proto_udp/S04_Part03C_Template_UDP_Proto_Server.py` — template student (TODO: `CLEAR`)
- `3_proto_udp/S04_Part03C_Template_UDP_Proto_Client.py` — template student (TODO: `clear`)
- `3_proto_udp/S04_Part03D_Scenario_UDP_Proto.md` — cerințe + livrabile
- `3_proto_udp/S04_Part03_Script_Transfer_Units.py` — enum-uri `RequestMessageType`, `ResponseMessageType` + clasele `RequestMessage`, `ResponseMessage`
- `3_proto_udp/S04_Part03_Script_State.py` — clasa `State` (dicționar `connections`, metode `add_connection`, `add_note`, `get_notes`, `clear_notes`, `remove_connection`)
- `3_proto_udp/S04_Part03_Script_Serialization.py` — funcții `serialize()`/`deserialize()` cu `pickle`

### Suport HTML (opțional, pentru studiu individual)

- `_HTMLsupport/S04/1_text-proto_tcp/S04_Part01_Page_Text_Proto_TCP.html`
- `_HTMLsupport/S04/2_binary-proto_tcp/S04_Part02_Page_Binary_Proto_TCP.html`
- `_HTMLsupport/S04/3_proto_udp/S04_Part03_Page_Proto_UDP.html`

---

## Checklist pre-seminar

### Pornire mediu (30 sec dacă ești organizat)

1) Pornești VM-ul MININET-SDN și te conectezi (SSH sau consolă):
```bash
cd ~/compnet-2025-redo/04_SEMINARS/S04
```

2) Verifici rapid uneltele:
```bash
python3 --version
tshark -v | head -n 2
```

### „Teatrul didactic": 3 terminale

| Terminal | Rol | Emoji |
|---|---|---|
| Terminal 1 | 🔵 SERVER — pornești/oprești servere | 🔵 |
| Terminal 2 | 🟢 CLIENT — pornești clienți | 🟢 |
| Terminal 3 | 🟠 CAPTURĂ — `tshark -w …` | 🟠 |

> Dacă nu ai Terminal 3, faci captură doar „la cerere" (Blocul D) sau explici conceptual fără captură live.

---

## Bloc A (2–3 min) — Hook: „două comenzi, câte `recv()`-uri?"

### Scenariu concret

> *▸ „Imaginați-vă: un client trimite pe TCP, imediat una după alta, două comenzi — `add user1 Alice` și `get user1`. Serverul apelează `recv(1024)`. Întrebare: serverul va primi exact două bucăți separate, câte una per comandă? Sau poate primi totul într-un singur `recv()`? Sau trei fragmente?"*

Lași 3–4 studenți să răspundă. Majoritatea vor zice „două separate". Fixezi:

> *▸ „TCP nu are noțiunea de 'mesaj'. Livrează un șir de bytes, în ordine, fără pierderi — dar fără granițe. Două `send()`-uri consecutive pot ajunge în `recv()` ca un blob unic. De la S03 știm că `recv()` poate returna mai puțin decât am cerut — azi vedem și cealaltă față: poate returna mai mult decât un 'mesaj'."*

Scrii pe tablă, fără explicații lungi (20 sec):

```
Trei strategii de framing:
1. delimiter (\n)
2. length prefix (<LEN> <payload>)
3. fixed-size records
```

> *▸ „Azi le vedem pe primele două în acțiune. Să pornim."*

**Notă pedagogică:** Hook-ul vizează direct concepția greșită #12 din kit ("`recv()` returnează mereu mesajul complet"). Se reia explicit la recap (Bloc F).

---

## Bloc B (12–13 min) — Demo: protocol text TCP + captură

> Scop: studenții văd un protocol human-readable funcțional și înțeleg rolul prefixului de lungime.

### B1) 🟠 CAPTURĂ — pornire (Terminal 3)

```bash
sudo tshark -i lo -f "tcp port 3333" -F pcapng -w s04_text_proto_tcp.pcapng
```

> *▸ „Capturăm doar portul 3333, pe loopback. Oprim în mai puțin de un minut."*

### B2) 🔵 SERVER — pornire server text (Terminal 1)

```bash
python3 1_text-proto_tcp/S04_Part01A_Example_Text_Proto_TCP_Server.py
```

Verifici output-ul:
```
[START] Text protocol TCP server on 127.0.0.1:3333
```

Dacă apare `Address already in use` — vezi Cheat-sheet (portul e blocat de o instanță anterioară).

### B3) 🟢 CLIENT — pornire client text (Terminal 2)

```bash
python3 1_text-proto_tcp/S04_Part01B_Example_Text_Proto_TCP_Client.py
```

Verifici promptul: `connected>`

### B4) Test dictat (studenții urmăresc, apoi replică)

Tastezi exact:

```text
add user1 Alice
get user1
remove user1
get user1
exit
```

Ce subliniezi în timp real:
- „Formatul e `command key [resource...]`."
- „`exit` nu trimite nimic special serverului — doar clientul se oprește din buclă."

### B5) 🟠 CAPTURĂ — oprire (Terminal 3)

`Ctrl+C` în `tshark`. Verifici:

```bash
ls -lh s04_text_proto_tcp.pcapng
```

### B6) **Epifanie: de ce `BUFFER_SIZE = 8`?**

🔵 Terminal 1 — arăți rapid:

```bash
grep -n "BUFFER_SIZE\|message_length\|remaining" 1_text-proto_tcp/S04_Part01A_Example_Text_Proto_TCP_Server.py | head -n 10
```

> *▸ „Observați: `BUFFER_SIZE = 8`. E intenționat mic — 8 bytes. Dacă mesajul are 20 de caractere, serverul va face 3 apeluri `recv()` ca să-l primească integral. Prefixul de lungime — prima cifră din mesaj — e modul prin care serverul știe cât mai are de citit."*

**Predicție (tipar POE):** Înainte de a arăta captura:

> *▸ „Când deschidem Wireshark și facem Follow TCP Stream — vom vedea text clar sau bytes indescifrabile?"*

(Toți vor zice „text clar" — corect. Contrastul vine la Blocul D.)

### B7) Wireshark — Follow TCP Stream

Dacă ai GUI în VM:
```bash
wireshark s04_text_proto_tcp.pcapng &
```

Dacă nu, copiezi fișierul pe gazdă și deschizi acolo.

Pași în Wireshark:
1. Display filter: `tcp.port == 3333`
2. Click dreapta pe un pachet → **Follow → TCP Stream**
3. Arăți payload-ul: `add user1 Alice`, etc. — vizibil ca text.

**Punchline:**

> *▸ „Wireshark reconstruiește stream-ul, dar nu 'știe' unde se termină un mesaj și unde începe altul. Granițele sunt invizibile pentru el — apar doar pentru că noi am definit protocolul: `<LEN> <comandă>`. Asta e tot ce înseamnă 'protocol de aplicație' la nivel tehnic."*

---

## Bloc C (9–10 min) — Implementare: `count` în template + testare

> Scop: „moment de control" — studenții modifică 2–3 linii și văd rezultatul imediat.

### C1) 🔵 SERVER — oprire server exemplu (Terminal 1)

`Ctrl+C`

### C2) 🔵 Editare template (Terminal 1)

```bash
nano 1_text-proto_tcp/S04_Part01C_Template_Text_Proto_TCP_Server.py
```

Spui exact unde:

> *▸ „Căutați `elif command == "count":` — linia 125 aproximativ."*

Înlocuiești:

```python
elif command == "count":
    payload = "TODO: implement count command"
```

cu:

```python
elif command == "count":
    n = len(state.resources)
    payload = f"{n} keys"
```

Opțional (dacă vrei varianta „curată"): adaugi metoda în clasa `State`:
```python
def count(self):
    return len(self.resources)
```
și apoi `n = state.count()`.

### C3) 🔵 SERVER — pornire template (Terminal 1)

```bash
python3 1_text-proto_tcp/S04_Part01C_Template_Text_Proto_TCP_Server.py
```

Verifici: `[START] Text protocol TCP server (template) on 127.0.0.1:3333`

### C4) 🟢 CLIENT — testare (Terminal 2)

```bash
python3 1_text-proto_tcp/S04_Part01B_Example_Text_Proto_TCP_Client.py
```

**Predicție (tipar POE) — înainte de al doilea `count`:**

> *▸ „Înainte să apăsați Enter la al doilea `count`: câte chei ar trebui să returneze? De ce?"*

Dictare:

```text
add k1 v1
add k2 v2
count
remove k1
count
foo something
exit
```

Rezultate așteptate: primul `count` → `2 keys`, al doilea → `1 keys`, `foo something` → `ERR unknown command`.

**Întrebare scurtă (15 sec):**

> *▸ „De ce `foo something` trebuie să returneze eroare explicită, nu să tacă? Hint: gândiți-vă la debugging — un client care nu primește răspuns nu știe dacă mesajul a ajuns sau nu."*

### C5) Fixare: ce e o mini-spec (30–45 sec)

> *▸ „Asta e ceea ce diferențiază 'merge pe calculatorul meu' de inginerie: o mini-spec scrisă. Nu roman — 10 linii de descriere, formatul cerere/răspuns ca pseudo-gramatică, lista de comenzi, și o state machine minimalistă."*

Arăți (fără a scrie complet) structura cerută în scenariul `S04_Part01D_Scenario_Text_Proto_TCP.md`:
- `text_protocol_spec.md` — informală + pseudo-gramatică + state machine textuală
- `text_proto_activity_output.txt` — log + 5–7 propoziții de interpretare

---

## Bloc D (6–7 min) — Demo: protocol binar TCP + comparație în captură

> Scop: aceeași funcționalitate, dar payload opac. Studenții înțeleg de ce tooling-ul devine obligatoriu.

### D1) 🔵 SERVER — oprire template text (Terminal 1)

`Ctrl+C`

### D2) 🟠 CAPTURĂ — pornire nouă (Terminal 3)

```bash
sudo tshark -i lo -f "tcp port 3333" -F pcapng -w s04_binary_proto_tcp.pcapng
```

### D3) 🔵 SERVER — pornire server binar (Terminal 1)

```bash
python3 2_binary-proto_tcp/S04_Part02A_Example_Binary_Proto_TCP_Server.py
```

Verifici: `[START] Binary protocol TCP server on 127.0.0.1:3333`

### D4) 🟢 CLIENT — pornire client binar (Terminal 2)

```bash
python3 2_binary-proto_tcp/S04_Part02B_Example_Binary_Proto_TCP_Client.py
```

Promptul afișat: `connected(binaries)>`

Testezi rapid:

```text
add user1 Alice Wonderland
get user1
remove user1
get user1
exit
```

**Notă:** clientul binar aruncă `ValueError` dacă introduci `exit` (cere minim 2 cuvinte: `<command> <key>`). Serverul nu se oprește — comportamentul e normal; clientul se închide oricum.

### D5) 🟠 CAPTURĂ — oprire (Terminal 3)

`Ctrl+C` și verifici:
```bash
ls -lh s04_binary_proto_tcp.pcapng
```

### D6) Wireshark — **Epifanie: „nu mai vedem text"**

**Predicție (tipar POE):**

> *▸ „Am făcut aceleași comenzi: add, get, remove. Cum credeți că arată Follow TCP Stream de data asta?"*

Deschizi captura, faci Follow TCP Stream. Payload-ul e un blob binar.

**Punchline:**

> *▸ „Vedeți bytes care sunt un obiect Python serializat cu `pickle`. Fără un dissector sau un decoder, traficul e opac. Asta e tipic pentru protocoale binare: compact și strict, dar necesită tooling dedicat."*

**Notă de igienă (15 sec):**

> *▸ „`pickle` e convenabil în laborator. În producție — nu-l folosiți pe date neîncrezute: permite execuție arbitrară de cod. Folosim `pickle` ca să înțelegem serializare + framing, nu ca best practice."*

### D7) Temă binară (20 sec)

> *▸ „Tema pentru protocolul binar: implementați comanda `keys` în template-ul `S04_Part02C_Template_Binary_Proto_TCP_Server.py`. Pattern-ul e identic cu `count` de adineauri, doar că lucrați cu obiecte `Request`/`Response` serializate, nu cu text. Comanda `keys` returnează lista cheilor separate prin virgulă, sau `no keys` dacă dicționarul e gol."*

---

## Bloc E (5–6 min) — Teaser: protocol UDP cu stare

> Scop: „click" — idea de state machine per client la UDP. **Nu codificăm nimic** — doar demonstrăm exemplul.

### E1) 🔵 SERVER — oprire server binar (Terminal 1)

`Ctrl+C`

### E2) 🔵 SERVER — pornire server UDP (Terminal 1)

```bash
python3 3_proto_udp/S04_Part03A_Example_UDP_Proto_Server.py 4000
```

Verifici: `[INFO] UDP protocol server listening on 0.0.0.0:4000`

### E3) 🟢 CLIENT — pornire client UDP (Terminal 2)

```bash
python3 3_proto_udp/S04_Part03B_Example_UDP_Proto_Client.py 127.0.0.1 4000
```

Promptul afișat: `storage>`

### E4) Demo „cu conflict cognitiv" (dictare exactă)

**Pasul 1 — capcana:**

> *▸ „Înainte de `connect`, tastați `list`. Ce vă așteptați?"*

Tastezi:
```text
list
```

Răspunsul: `ERR_CONNECTED`.

> *▸ „Serverul refuză: nu știe cine sunteți. La UDP nu există conexiune la nivel transport — dar protocolul nostru implementează una logică: trebuie să faci `CONNECT` înainte de orice."*

**Pasul 2 — fluxul complet:**

```text
connect
send prima notă
send a doua notă
list
disconnect
list
exit
```

Al doilea `list` (după `disconnect`) → din nou `ERR_CONNECTED`.

**Punchline:**

> *▸ „Serverul ține stare într-un dicționar cu cheia `(ip, port)` primită de la `recvfrom()`. Asta e 'identitatea clientului' la UDP. Dacă clientul se închide și se redeschide — portul sursă se schimbă, serverul vede alt client."*

### E5) Explicație structură + temă (30 sec)

> *▸ „Protocolul UDP din kit are 3 fișiere helper: `Script_Transfer_Units.py` (tipurile de mesaje ca enum), `Script_State.py` (dicționarul de conexiuni), `Script_Serialization.py` (serialize/deserialize cu pickle). Tema: adăugați comanda `CLEAR` — atât în server (`S04_Part03C_Template_UDP_Proto_Server.py`) cât și în client (`S04_Part03C_Template_UDP_Proto_Client.py`) — și descrieți state machine-ul în `udp_proto_state_machine.md`."*

---

## Bloc F (2–3 min) — Recap + livrabile

### Recap cu revenire la hook

> *▸ „La început am întrebat: două `send()`-uri consecutive ajung ca două `recv()`-uri separate? Acum știți răspunsul: nu neapărat. TCP e un stream. Am construit trei protocoale care adaugă granițe:"*

Enumerare scurtă (3 idei fixe):
1. **Framing** — prefixul de lungime spune receptorului cât să citească.
2. **Text vs. binar** — text e ușor de inspectat dar mai mare; binar e compact dar opac fără tooling.
3. **State machine** — chiar și peste UDP (fără conexiune transport), aplicația poate defini stări (CONNECTED/DISCONNECTED) și reguli.

### Livrabile (din scenarii)

| Parte | Fișiere cerute | Ce conțin |
|---|---|---|
| Text TCP | `text_protocol_spec.md` | Mini-spec: descriere informală + pseudo-gramatică + lista de comenzi + state machine textuală |
| | `text_proto_activity_output.txt` | Log comenzi + 5–7 propoziții despre rolul prefixului de lungime |
| | `text_proto_capture.pcapng` *(opțional)* | Captură Wireshark |
| Binar TCP | `binary_proto_activity_output.txt` | Log comenzi (inclusiv `keys`) + 5–7 propoziții comparație text vs. binar |
| | `binary_proto_capture.pcapng` *(opțional)* | Captură comparativă |
| UDP | `udp_proto_activity_output.txt` | Secvență comenzi + 5–7 propoziții despre `(ip, port)` ca identitate |
| | `udp_proto_state_machine.md` | Stări (DISCONNECTED, CONNECTED), tabel `(stare, mesaj) → (stare nouă, răspuns)`, inclusiv `CLEAR` |

> Fiecare fișier `*_activity_output.txt` trebuie să conțină **interpretare**, nu doar log brut. Cine copiază doar output-ul fără 5–7 propoziții de analiză nu primește punctaj complet.

---

## Cheat-sheet

### Comenzi rapide

| Ce vrei | Comanda | Context |
|---|---|---|
| Pornire captură TCP port 3333 | `sudo tshark -i lo -f "tcp port 3333" -F pcapng -w <fișier>.pcapng` | 🟠 Terminal 3 |
| Pornire captură UDP port 4000 | `sudo tshark -i lo -f "udp port 4000" -F pcapng -w <fișier>.pcapng` | 🟠 Terminal 3 |
| Display filter Wireshark TCP | `tcp.port == 3333` | Wireshark |
| Display filter Wireshark UDP | `udp.port == 4000` | Wireshark |
| Follow TCP stream | Click dreapta → Follow → TCP Stream | Wireshark |
| Identificare port ocupat | `ss -ltnp \| grep ":3333"` | Orice terminal |
| Kill proces pe port | `sudo kill -9 <PID>` | Orice terminal |
| Filtrare conversație TCP | `tcp.stream eq 0` (sau alt index) | Wireshark |

### Porturi utilizate

| Protocol | Port | Fișier server |
|---|---|---|
| Text TCP | 3333 | `S04_Part01A_...` / `S04_Part01C_...` |
| Binar TCP | 3333 | `S04_Part02A_...` / `S04_Part02C_...` |
| UDP | 4000 (argument CLI) | `S04_Part03A_...` / `S04_Part03C_...` |

### Secvență de oprire/pornire servere

Text → Binar → UDP: fiecare server se oprește cu `Ctrl+C` înainte de a porni următorul. Text și binar folosesc același port (3333). UDP folosește 4000.

---

## Plan de contingență

| # | Problemă | Simptom | Soluție rapidă |
|---|---|---|---|
| 1 | Port ocupat | `Address already in use` | Oprești serverul vechi (`Ctrl+C`). Dacă nu găsești terminalul: `ss -ltnp \| grep ":3333"` → `sudo kill -9 <PID>`. |
| 2 | Client nu se conectează | `Connection refused` | Verifici că serverul rulează, că portul e 3333, că ești pe `127.0.0.1`. |
| 3 | Nu ai Wireshark GUI | Nu poți deschide capturi în VM | Capturezi cu `tshark -w ...` și copiezi fișierul pe Windows: `scp stud@<IP_VM>:~/compnet-2025-redo/04_SEMINARS/S04/<fișier>.pcapng .` |
| 4 | Clientul binar aruncă `ValueError` la `exit` | `ValueError: Command must have at least: <command> <key>` | Normal — clientul binar cere minim 2 argumente. `exit` e tratat de buclă dar ajunge și la `get_command()`. Ignoră eroarea; clientul se închide oricum. |
| 5 | Rămâi fără timp | Nu mai apuci Blocul E (UDP) | Scurtezi E la 2 min: arăți doar `list` fără `connect` → `ERR_CONNECTED`, fixezi ideea de state machine, restul devine temă. Sau muți E la începutul S05. |
| 6 | `tshark` nu e instalat / nu funcționează | `command not found` sau eroare de permisiuni | `sudo apt install tshark`. Dacă nu merge: renunți la captură live, explici conceptual Follow TCP Stream, studenții fac captură acasă. |
| 7 | Template-ul text nu compilează | `SyntaxError` după editare | Verifici indentarea (Python!). Cel mai frecvent: taburi amestecate cu spații. `python3 -tt <fișier>` detectează inconsistențele. |

---

## Referințe (APA 7th ed.)

| Nr. | Referință | DOI |
|---:|---|---|
| 1 | Braden, R. (1989). *Requirements for Internet hosts—Communication layers* (RFC 1122). RFC Editor. | https://doi.org/10.17487/RFC1122 |
| 2 | Chi, M. T. H. (2009). Active-constructive-interactive: A conceptual framework for differentiating learning activities. *Topics in Cognitive Science, 1*(1), 73–105. | https://doi.org/10.1111/j.1756-8765.2008.01005.x |
| 3 | Chow, T. S. (1978). Testing software design modeled by finite-state machines. *IEEE Transactions on Software Engineering, SE-4*(3), 178–187. | https://doi.org/10.1109/TSE.1978.231496 |
| 4 | Clark, D. D. (1988). The design philosophy of the DARPA internet protocols. In *Proceedings of SIGCOMM '88* (pp. 106–114). ACM. | https://doi.org/10.1145/52324.52336 |
| 5 | Postel, J. (1980). *User Datagram Protocol* (RFC 768). RFC Editor. | https://doi.org/10.17487/RFC0768 |
| 6 | Postel, J. (1981). *Transmission Control Protocol* (RFC 793). RFC Editor. | https://doi.org/10.17487/RFC0793 |
| 7 | Prince, M. (2004). Does active learning work? A review of the research. *Journal of Engineering Education, 93*(3), 223–231. | https://doi.org/10.1002/j.2168-9830.2004.tb00809.x |
| 8 | Saltzer, J. H., Reed, D. P., & Clark, D. D. (1984). End-to-end arguments in system design. *ACM Transactions on Computer Systems, 2*(4), 277–288. | https://doi.org/10.1145/357401.357402 |

---

## Note pedagogice

**Concepție greșită vizată.** Întregul seminar se construiește pe #12 din kit: studenții presupun că `recv()` returnează mereu exact un mesaj. Hook-ul (Bloc A), `BUFFER_SIZE = 8` (B6) și comparația text/binar (D6) atacă această presupunere din unghiuri diferite.

**Tipare socratice folosite.** (1) POE în B6 (predicție: „text sau binar în captură?"), C4 (predicție: „câte chei?"), D6 (predicție: „cum arată payload-ul binar?"). (2) Capcana de concepție greșită în E4 (`list` fără `connect` → eroare neașteptată). (3) „Ce s-ar fi întâmplat dacă?" — implicit în C (comanda `foo` → eroare explicită vs. tăcere).

**Progresie.** De la S03 (broadcast/multicast, tunnel) la S04 (framing, protocoale) — trecerea de la „cum trimit date" la „cum definesc structura datelor". La S05 (adresare, rutare) se trece de la aplicație la rețea.

**Dacă grupul e avansat.** Poți menționa alternative la `pickle`: `struct.pack` (framing binar cu format fix), Protocol Buffers (schemă explicită), JSON (text, dar cu overhead). Nu intra în detalii — doar numești și trimiți la documentație.

**Dacă grupul e în urmă.** Renunți la Blocul D (binar) și extinzi C (template text) cu testare mai detaliată + dictare a primelor 5 linii din mini-spec pe tablă.
