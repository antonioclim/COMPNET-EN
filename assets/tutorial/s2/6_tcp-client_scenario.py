"""
### Scenariu: rularea clientului TCP Python, testare cu serverul și analiză RTT în Wireshark

#### 1. Obiectiv

În această etapă veți:
- porni serverul TCP Python din etapa anterioară;
- rula un client TCP simplu (`index_tcp-client_example.py`);
- modifica un client template pentru a trimite mesaje în buclă și a măsura RTT;
- analiza traficul în Wireshark și a corela pachetele cu logurile clientului/serverului.

---

### 2. Pregătire: porniți serverul TCP

Asigurați-vă că serverul din etapa anterioară rulează (de exemplu, varianta template finalizată):

```bash
python3 index_tcp-server_template.py
````

Ar trebui să vedeți:

```text
[INFO] TCP server listening on localhost:12345
```

---

### 3. Rularea clientului de exemplu

1. Într-un alt terminal, rulați:

```bash
python3 index_tcp-client_example.py
```

2. Observați:

   * în terminalul clientului: mesajele `[INFO] Connecting...`, apoi `Received b'...'`;
   * în terminalul serverului: mesajul primit și transformat (de ex. `HELLO, WORLD`).

Repetați comanda de câteva ori și observați cum se deschid și se închid conexiuni TCP separate.

---

### 4. Capturarea traficului cu Wireshark

1. Deschideți **Wireshark** și selectați interfața relevantă (`lo`, `Loopback`, `eth0`, `wlan0`, etc.).

2. Configurați un **capture filter** pentru a capta doar traficul către portul serverului:

```text
tcp port 12345
```

3. Porniți captura.

4. Lansați din nou clientul de exemplu:

```bash
python3 index_tcp-client_example.py
```

5. Opriți captura după ce clientul a trimis și primit mesajul.

6. Aplicați un **display filter**:

```text
tcp.port == 12345
```

Analizați:

* handshake-ul TCP (SYN, SYN-ACK, ACK);
* pachetul care conține `Hello, world`;
* pachetul de răspuns al serverului (de ex. `HELLO, WORLD`).

---

### 5. Sarcina studentului – client interactiv + RTT

1. Deschideți fișierul `index_tcp-client_template.py`.

2. Completați secțiunea marcată:

```python
# >>> STUDENT CODE STARTS HERE
...
# <<< STUDENT CODE ENDS HERE
```

respectând cerințele din comentarii:

* citiți mesaje de la tastatură;
* opriți-vă la comanda `exit`;
* trimiteți mesajele la server;
* calculați și afișați RTT-ul pentru fiecare mesaj.

3. Rulați clientul modificat:

```bash
python3 index_tcp-client_template.py
```

Trimiteți cel puțin 5 mesaje diferite (de lungimi variate).

4. Lăsați serverul să afișeze loguri pentru fiecare mesaj.

---

### 6. Captură Wireshark pentru clientul interactiv

1. Porniți o nouă captură în Wireshark cu același **capture filter**:

```text
tcp port 12345
```

2. În timp ce captura rulează, trimiteți cele 5 mesaje din clientul interactiv.

3. Opriți captura și folosiți display filter:

```text
tcp.port == 12345
```

4. Pentru unul dintre mesaje:

   * identificați pachetul de request (de la client către server);
   * identificați pachetul de răspuns (de la server către client);
   * observați diferența de timp dintre ele în Wireshark (Time delta).

Comparați valoarea aproximativă a RTT-ului măsurat în cod cu intervalul de timp din Wireshark.

---

### 7. Dovada de lucru (ce veți încărca)

1. Fișier text: `tcp_client_activity_output.txt` care să conțină:

   * cel puțin 3 loguri de la client (mesaj trimis, răspuns primit, RTT);
   * 2–3 loguri relevante de la server (mesaje primite);
   * un scurt comentariu (5–7 propoziții) despre cum se corelează logurile și pachetele din Wireshark.

2. Fișier captură: `tcp_client_capture.pcapng` cu traficul generat de clientul interactiv.
"""
