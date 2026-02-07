### Scenariu: rularea unui server TCP în Python, test cu netcat și analiză de trafic cu Wireshark

#### 1. Obiectiv

În această etapă veți:
- rula un server TCP simplu scris în Python;
- testa serverul folosind `netcat` ca și client;
- captura și analiza traficul TCP în Wireshark;
- modifica logica serverului într-un fișier template.

---

### 2. Rularea serverului TCP de exemplu

1. Lansați serverul de referință:

```bash
python3 1_tcp-server_example.py
````

Ar trebui să vedeți un mesaj de tip:

```text
[INFO] TCP server listening on localhost:12345
```

Serverul rămâne pornit și așteaptă conexiuni.

---

### 3. Testarea serverului cu netcat (nc)

2. Într-un alt terminal, conectați-vă la server:

```bash
nc 127.0.0.1 12345
```

3. Scrieți un mesaj, de exemplu:

```text
hello tcp
```

și apăsați Enter.

4. Observați că:

   * în fereastra `netcat` primiți răspunsul în litere mari (`HELLO TCP`);
   * în terminalul serverului apare IP-ul clientului și mesajul primit.

Puteți testa și cu:

```bash
echo "test message" | nc 127.0.0.1 12345
```

---

### 4. Capturarea traficului cu Wireshark

1. Deschideți **Wireshark** și selectați interfața de rețea pe care are loc traficul
   (de ex. `lo` / `Loopback` sau `eth0`/`wlan0`, în funcție de sistem).

2. Configurați un **capture filter** pentru a capta doar traficul către portul nostru:

```text
tcp port 12345
```

3. Porniți captura, apoi repetați pașii cu `nc` de mai sus (trimiterea unui mesaj).

4. Opriți captura după ce ați trimis și primit cel puțin un mesaj.

5. Aplicați un **display filter** pentru a izola conversația:

```text
tcp.port == 12345
```

Observați:

* handshake-ul TCP (SYN, SYN-ACK, ACK);
* pachetul care conține mesajul trimis de `netcat`;
* pachetul cu răspunsul serverului (mesajul în litere mari).

---

### 5. Sarcina studentului

1. **Modificați serverul în template-ul `2_tcp-server_template.py`:**

   * completați secțiunea marcată între:

     ```python
     # >>> STUDENT CODE STARTS HERE
     ...
     # <<< STUDENT CODE ENDS HERE
     ```
   * respectați cerințele din comentarii (afișarea IP:port, lungimea mesajului, răspunsul `OK: ...`).

2. **Rulați serverul modificat:**

```bash
python3 2_tcp-server_template.py
```

3. **Testați cu netcat**:

   * trimiteți cel puțin 3 mesaje diferite (de lungimi diferite);
   * observați logurile din server: IP, port, lungime, mesaj.

4. **Capturați din nou traficul în Wireshark**:

   * folosiți capture filter `tcp port 12345`;
   * aplicați display filter `tcp.port == 12345`;
   * identificați în pachetul de răspuns stringul `OK: ` în payload.

---

### 6. Dovada de lucru (ce veți încărca)

1. Fișier text: `tcp_server_activity_output.txt` care să conțină:

   * comenzile folosite (`python3 ...`, `nc ...`);
   * logurile afișate de server pentru cele 3 mesaje test;
   * câteva observații (3–5 propoziții) despre ce vedeți în loguri vs. în Wireshark.

2. Fișier captură: `tcp_server_capture.pcapng` (exportat din Wireshark) care conține traficul pentru testele voastre.

Aceste fișiere vor fi folosite pentru evaluarea înțelegerii fluxului server–client și a relației dintre cod și pachetele observate în rețea.
