"""
### Scenariu: UDP broadcast sender + receiver (IPv4) + Wireshark

#### 1. Obiectiv

În această etapă veți:

- rula un receiver UDP care ascultă mesaje de broadcast;
- rula un sender UDP care trimite broadcast periodic;
- observa în Wireshark cum arată traficul de broadcast;
- completa un receiver template cu logică de filtrare și numărare a mesajelor.

---

### 2. Rularea receiver-ului de exemplu

Într-un terminal:

```bash
python3 index_udp-broadcast_receiver_example.py
````

Ar trebui să vedeți:

```text
[INFO] UDP broadcast receiver listening on 0.0.0.0:5007
```

Lăsați programul să ruleze.

---

### 3. Rularea sender-ului de exemplu

Într-un alt terminal:

```bash
python3 index_udp-broadcast_sender_example.py "Hello, broadcast"
```

Ar trebui să vedeți în sender:

```text
[INFO] Sending UDP broadcast to 255.255.255.255:5007
[SEND] ... bytes -> 255.255.255.255:5007 :: 'Hello, broadcast #0'
...
```

Și în receiver:

```text
[RECV] ... bytes from 127.0.0.1:XXXXX -> 'Hello, broadcast #0'
[RECV] ... bytes from 127.0.0.1:XXXXX -> 'Hello, broadcast #1'
...
```

---

### 4. Captură Wireshark pentru broadcast

1. Deschideți **Wireshark** și selectați interfața relevantă (`lo`, `eth0`, `wlan0`, etc.).

2. Configurați un **capture filter** pentru portul UDP:

```text
udp port 5007
```

3. Porniți captura.

4. Rulați sender-ul dacă nu rulează deja și lăsați-l să trimită câteva mesaje.

5. Opriți captura și aplicați un **display filter** precum:

```text
udp.port == 5007
```

sau pentru a vedea doar broadcast:

```text
ip.dst == 255.255.255.255 and udp.port == 5007
```

Observați:

* pachete UDP cu destinația 255.255.255.255;
* aceeași datagramă ajunge la toate procesele care ascultă pe portul 5007.

---

### 5. Sarcina studentului – receiver cu filtrare

1. Deschideți `index_udp-broadcast_receiver_template.py`.

2. Completați secțiunea `TODO` astfel încât:

* să numărați mesajele primite (counter);
* să ignorați mesajele care nu încep cu `"Hello"`;
* să afișați loguri `[OK]` și `[SKIP]` conform instrucțiunilor.

3. Rulați receiver-ul template:

```bash
python3 index_udp-broadcast_receiver_template.py
```

4. Rulați sender-ul:

```bash
python3 index_udp-broadcast_sender_example.py "Hello, broadcast"
```

5. Trimiteți și câteva mesaje de test manuale, de exemplu cu `netcat`:

```bash
echo "Hello manual" | nc -u 255.255.255.255 5007
echo "Other text" | nc -u 255.255.255.255 5007
```

Observați că:

* mesajele cu prefix "Hello" apar ca `[OK]`;
* celelalte ca `[SKIP]`.

---

### 6. Dovada de lucru

Veți pregăti:

* `udp_broadcast_activity_output.txt`:

  * loguri relevante din receiver-ul template (cel puțin 5 mesaje, cu `[OK]` și `[SKIP]`);
  * un scurt comentariu (3–5 propoziții) despre cum se vede broadcast-ul în Wireshark (destinație, port, repetare etc.);
* `udp_broadcast_capture.pcapng`:

  * captura Wireshark cu traficul UDP de broadcast.
"""
