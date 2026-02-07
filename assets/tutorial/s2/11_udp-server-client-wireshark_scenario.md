### Scenariu: server și client UDP în Python, test cu netcat și analiză în Wireshark

#### 1. Obiectiv

În această etapă veți:
- rula un server UDP în Python;
- testa serverul cu netcat;
- rula un client UDP Python (exemplu + template);
- observa în Wireshark cum arată traficul UDP (fără handshake, fără conexiune);
- compara comportamentul cu TCP din etapa anterioară.

---

### 2. Rularea serverului UDP de exemplu

Porniți serverul UDP de referință:

```bash
python3 index_udp-server_example.py 12345
````

Ar trebui să vedeți:

```text
[INFO] UDP server listening on 0.0.0.0:12345
```

Lăsați serverul să ruleze.

---

### 3. Testarea serverului UDP cu netcat

Într-un alt terminal, folosiți `netcat` în modul UDP:

```bash
echo "hello udp" | nc -u 127.0.0.1 12345
```

Observați:

* în terminalul serverului: log cu mesajul primit și adresa clientului;
* în terminalul `nc` s-ar putea să NU vedeți răspuns (depinde de versiune/parametri).
  De aceea, pentru a vedea răspunsul clar, vom folosi clientul Python.

---

### 4. Testarea serverului UDP cu clientul Python de exemplu

Rulați clientul simplu:

```bash
python3 index_udp-client_example.py 127.0.0.1 12345 "Hello from client"
```

Ar trebui să vedeți în client:

```text
[INFO] Sending ... bytes to 127.0.0.1:12345 ...
[INFO] Received ... bytes from ('127.0.0.1', 12345): b'HELLO FROM CLIENT'
```

Și în server, log cu mesajul și răspunsul.

---

### 5. Capturarea traficului UDP cu Wireshark

1. Deschideți **Wireshark** și selectați interfața relevantă (`lo`, `eth0`, `wlan0`, etc.).

2. Configurați un **capture filter** pentru portul UDP folosit:

```text
udp port 12345
```

3. Porniți captura.

4. În timp ce captura rulează, rulați comenzi precum:

```bash
echo "test1" | nc -u 127.0.0.1 12345
python3 index_udp-client_example.py 127.0.0.1 12345 "ping"
```

5. Opriți captura și aplicați un **display filter**:

```text
udp.port == 12345
```

Observați:

* fiecare datagramă trimisă de client;
* răspunsul serverului;
* faptul că nu există handshake (nu SYN/SYN-ACK/ACK ca la TCP);
* pachetele apar ca perechi cerere-răspuns, dar fără noțiunea de „stream” ca în TCP.

---

### 6. Sarcina studentului – completarea serverului UDP (template)

1. Deschideți `index_udp-server_template.py`.

2. Implementați logica descrisă în blocul `TODO`:

   * decodificare mesaj;
   * log detaliat cu IP, port, text, număr de bytes;
   * protocolul:

     * `ping` -> `PONG`
     * `upper:...` -> partea de după `upper:` cu litere mari
     * altceva -> `UNKNOWN COMMAND`.

3. Rulați serverul template:

```bash
python3 index_udp-server_template.py 12345
```

4. Testați serverul:

   * folosind `netcat`:

     ```bash
     echo "ping" | nc -u 127.0.0.1 12345
     echo "upper:hello world" | nc -u 127.0.0.1 12345
     ```
   * folosind clientul de exemplu:

     ```bash
     python3 index_udp-client_example.py 127.0.0.1 12345 ping
     python3 index_udp-client_example.py 127.0.0.1 12345 "upper:hello"
     ```

Observați răspunsurile și logurile.

---

### 7. Sarcina studentului – completarea clientului UDP interactiv (template)

1. Deschideți `index_udp-client_template.py`.

2. Completați secțiunea `TODO` conform cerințelor:

   * buclă interactivă până la `exit`;
   * trimitere mesaj la server;
   * timeout pentru răspuns;
   * calcul RTT aproximativ pentru mesajele care primesc răspuns;
   * statistici finale (trimise / primite / pierderi).

3. Rulați clientul:

```bash
python3 index_udp-client_template.py 127.0.0.1 12345
```

Trimiteți cel puțin 5 mesaje:

* două cu `ping`,
* două cu `upper:...`,
* unul cu un text „random” (de ex. `abc`).

Observați:

* cum răspunde serverul la fiecare tip de mesaj;
* câte răspunsuri sunt primite.

---

### 8. Captură Wireshark pentru comunicarea UDP Python–Python

1. Porniți o nouă captură cu **capture filter**:

```text
udp port 12345
```

2. În timp ce captura rulează:

   * rulați serverul template;
   * rulați clientul template și trimiteți cele 5 mesaje de test.

3. Opriți captura și aplicați display filter:

```text
udp.port == 12345
```

4. Pentru cel puțin două mesaje:

   * identificați datagrama de la client (request);
   * identificați datagrama de la server (response);
   * comparați timpii din Wireshark cu RTT-ul afișat de client.

---

### 9. Dovada de lucru (ce veți încărca)

1. `udp_server_activity_output.txt`:

   * comenzile folosite pentru rularea serverului/template-ului;
   * cel puțin 5 linii de log din server (cu diferite comenzi: `ping`, `upper:...`, altele);
   * un scurt comentariu (3–5 propoziții) despre comportamentul protocolului (`PONG`, `UNKNOWN COMMAND`, etc.).

2. `udp_client_activity_output.txt`:

   * logurile clientului interactiv (mesaje trimise, răspunsuri primite, RTT, timeouts);
   * statistica finală (trimise/primite).

3. `udp_traffic_capture.pcapng`:

   * captură Wireshark cu traficul UDP generat de testele voastre.

Aceste fișiere vor demonstra că înțelegeți:

* cum funcționează UDP din cod;
* cum se vede traficul UDP în Wireshark;
* diferențele față de TCP (fără handshake, fără conexiune persistentă).