### Scenariu: Server TCP multi-client cu threads (mini „chat”) + test cu netcat / client Python + Wireshark

#### 1. Obiectiv

În această etapă veți:

- înțelege cum funcționează un server TCP multi-client cu threads;
- rula serverul de exemplu și a-l testa cu mai mulți clienți simultan (netcat sau clientul din tutorialul anterior);
- modifica un template pentru a implementa un mini „chat” (mesajele unui client sunt retransmise către ceilalți);
- analiza în Wireshark traficul generat de mai mulți clienți simultan.

---

### 2. Rularea serverului de exemplu

1. Porniți serverul de exemplu:

```bash
python3 index_tcp-multiclient-server_example.py
````

Ar trebui să vedeți:

```text
[START] TCP multi-client server on 127.0.0.1:3333
[INFO] Server ready, listening on 127.0.0.1:3333
```

Lăsați serverul să ruleze.

---

### 3. Conectarea mai multor clienți (netcat sau client Python)

Deschideți **cel puțin 2–3 terminale** suplimentare.

#### Variantă A – netcat

În fiecare terminal:

```bash
nc 127.0.0.1 3333
```

Scrieți mesaje și apăsați Enter. Observați în terminalul serverului:

* pentru fiecare client apare `[CONNECT] New client ...`;
* pentru fiecare mesaj apare `[RECV]` și `[SEND]`.

#### Variantă B – clientul Python din tutorialul anterior

Folosiți clientul TCP cu portul ajustat la 3333 (dacă este necesar, modificați `PORT = 3333`):

```bash
python3 index_tcp-client_template.py
```

Trimiteți mesaje din 2 instanțe de client.

---

### 4. Capturarea traficului multi-client în Wireshark

1. Deschideți **Wireshark** și selectați interfața relevantă (`lo`, `Loopback`, `eth0`, `wlan0`, etc.).

2. Configurați un **capture filter**:

```text
tcp port 3333
```

3. Porniți captura.

4. În timp ce captura rulează:

   * conectați 2–3 clienți;
   * trimiteți câte 2–3 mesaje din fiecare client.

5. Opriți captura și folosiți un **display filter**:

```text
tcp.port == 3333
```

Observați:

* mai multe „TCP streams” în paralel (de exemplu `tcp.stream eq 0`, `tcp.stream eq 1`, etc.);
* faptul că fiecare client are propriul său stream cu serverul;
* diferența de timp între mesajele clienților.

---

### 5. Sarcina studentului – implementarea mini „chat”-ului

1. Deschideți fișierul `index_tcp-multiclient-server_template.py`.

2. Completați secțiunea marcată:

```python
# >>> STUDENT CODE STARTS HERE
...
# <<< STUDENT CODE ENDS HERE
```

Conform cerințelor din comentarii:

* log clar pentru fiecare mesaj primit;
* construirea unui mesaj de forma `[ip:port] text...`;
* trimiterea mesajului către toți ceilalți clienți din lista `clients`.

3. Rulați serverul template:

```bash
python3 index_tcp-multiclient-server_template.py
```

4. Deschideți cel puțin **3 clienți**:

* fie cu `nc 127.0.0.1 3333`,
* fie cu clientul Python (modificat să vorbească pe portul 3333).

5. Trimiteți mesaje dintr-un client și verificați că:

* le primiți înapoi în **ceilalți** clienți;
* logurile din server arată către ce clienți a fost trimis mesajul (`[FWD] ...`).

---

### 6. Captură Wireshark pentru mini „chat”

1. Porniți **o nouă captură** cu același **capture filter**:

```text
tcp port 3333
```

2. În timp ce captura rulează:

* rulați serverul template;
* conectați 3 clienți;
* trimiteți câteva mesaje „încrucișate” (client 1 către client 2, client 2 către client 3, etc.).

3. Opriți captura și aplicați display filter:

```text
tcp.port == 3333
```

4. Analizați:

* pachetele care pleacă de la un client către server (request);
* pachetele de la server către ceilalți clienți (forward/broadcast);
* cum se văd în Wireshark stream-urile diferiților clienți (`tcp.stream eq N`).

---

### 7. Dovada de lucru (ce veți încărca)

1. `tcp_multiclient_server_output.txt`:

   * comanda de pornire a serverului;
   * loguri de server pentru cel puțin 5 mesaje (de la clienți diferiți);
   * 5–7 propoziții în care explicați:

     * cum știți din loguri că există mai mulți clienți;
     * cum se leagă logurile de pachetele din Wireshark.

2. `tcp_multiclient_chat_capture.pcapng`:

   * captura Wireshark cu traficul generat de mini „chat”.

