### Scenariu: Protocol text peste TCP – framing, comenzi și mini-spec

#### 1. Obiectiv

În această etapă veți:

- rula un server și un client TCP care implementează un protocol text simplu;
- înțelege cum se face *framing*-ul cu un header de lungime;
- extinde protocolul cu o nouă comandă `count`;
- descrie protocolul sub forma unei mini-specificații (text + mică reprezentare de mașină de stare).

Durata estimată: ~30–35 minute din cele 80.

---

### 2. Rularea serverului și clientului de exemplu

1. Porniți serverul de exemplu:

```bash
python3 index_text-proto_tcp-server_example.py
````

Ar trebui să vedeți:

```text
[START] Text protocol TCP server on 127.0.0.1:3333
```

2. Într-un alt terminal, porniți clientul de exemplu:

```bash
python3 index_text-proto_tcp-client_example.py
```

3. În prompt-ul `connected>`, încercați:

```text
add user1 Alice
get user1
remove user1
get user1
exit
```

Observați:

* formatul comenzilor (command, key, resource...);
* răspunsurile serverului (mesaj text);
* faptul că protocolul **nu** oprește conexiunea la `exit` – clientul doar nu mai trimite comenzi.

---

### 3. Analiza formatului de mesaj

Folosiți `print` (dacă doriți) sau doar gândiți:

* Mesaj trimis de client:

  * `"TOTAL_LENGTH command key [resource...]"` ca string,
  * codificat în UTF-8,
  * TOTAL_LENGTH este numărul total de caractere al întregii linii.

* Serverul:

  * citește primul fragment,
  * extrage `TOTAL_LENGTH` (prima valoare),
  * continuă să citească până strâng exact `TOTAL_LENGTH` caractere,
  * parsează și execută comanda.

În mini-spec, veți nota explicit:

* Request:

  * `REQUEST = <LEN> SP <COMMAND_LINE>`
  * `COMMAND_LINE = <COMMAND> SP <KEY> [SP <RESOURCE>...]`

* Response:

  * `RESPONSE = <LEN> SP <PAYLOAD>`

---

### 4. Mini-captură Wireshark (opțional, scurtă)

Dacă aveți timp:

1. Deschideți **Wireshark** și selectați interfața (`lo` / `Loopback` sau alta).

2. Configurați un **capture filter**:

```text
tcp port 3333
```

3. Porniți captura.

4. Trimiteți 2–3 comenzi din client (`add`, `get`, `remove`).

5. Opriți captura și aplicați un **display filter**:

```text
tcp.port == 3333
```

Observați:

* că payload-ul este text (dacă dați follow TCP stream);
* nu există delimitare specială între mesaje la nivel TCP – framing-ul e făcut *în aplicație* (prin len).

---

### 5. Sarcina studentului – extinderea protocolului (comanda `count`)

1. Deschideți `index_text-proto_tcp-server_template.py`.

2. Implementați:

* metoda `count()` în `State` (dacă ați ales să o folosiți);
* în `process_command`, comanda:

```text
count
```

fără argumente; răspunsul trebuie să fie:

```text
"<N> keys"
```

unde `N` este numărul curent de chei din `state`.

3. Pentru comenzi necunoscute, întoarceți:

```text
"ERR unknown command"
```

împachetat cu `build_framed_response()`.

4. Porniți serverul template:

```bash
python3 index_text-proto_tcp-server_template.py
```

5. Rulați clientul de exemplu:

```bash
python3 index_text-proto_tcp-client_example.py
```

Testați secvențe precum:

```text
add k1 v1
add k2 v2
count
remove k1
count
get k3
foo something
exit
```

Verificați:

* că `count` întoarce numărul așteptat;
* că comanda necunoscută `foo` întoarce `ERR unknown command`.

---

### 6. Mini-specificație de protocol (ce trebuie să predați)

Creați un fișier `text_protocol_spec.md` cu:

1. **Descriere informală** (max 10–15 rânduri):

   * Ce face protocolul
   * Ce comenzi există: `add`, `remove`, `get`, `count`
   * Ce răspunsuri tipice există (OK, not found, error)

2. **Format request/response** (pseudo-gramatică):

   * `REQUEST = <LEN> SP <COMMAND_LINE>`
   * `COMMAND_LINE = <COMMAND> [SP <KEY> [SP <RESOURCE>...]]`
   * `RESPONSE = <LEN> SP <PAYLOAD>`

3. **Listă de comenzi**:

   * `add <key> <resource...>` – descriere
   * `remove <key>` – descriere
   * `get <key>` – descriere
   * `count` – descriere

4. **Reprezentare simplificată de mașină de stare** (text, nu desen neapărat):

   * Starea conexiunii este mereu „CONNECTED” până când clientul închide.
   * Pentru fiecare mesaj:

     * serverul primește REQUEST,
     * execută comanda,
     * trimite RESPONSE,
     * revine în aceeași stare: „așteaptă REQUEST”.

   (Puteți descrie și ca o listă de „events” + „actions”.)

---

### 7. Dovada de lucru (ce încărcați)

* `text_protocol_spec.md` – mini-spec-ul protocolului.
* `text_proto_activity_output.txt`:

  * log cu comenzile testate (`add`, `remove`, `get`, `count`, comenzi invalide);
  * răspunsurile primite de client;
  * un scurt comentariu (5–7 propoziții) despre:

    * de ce avem nevoie de header cu lungime,
    * ce se întâmplă dacă mesajul e trunchiat sau header-ul e invalid.

(PCAP-ul Wireshark e opțional pentru acest seminar – dacă îl cereți, îl puteți numi `text_proto_capture.pcapng`.)