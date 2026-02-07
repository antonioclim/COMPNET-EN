#### `index_udp-multicast_scenario.md`

````markdown
### Scenariu: UDP multicast sender + receiver + Wireshark

#### 1. Obiectiv

Veți:

- porni un receiver multicast și vă veți abona la un grup;
- trimite un mesaj către grupul multicast cu un sender UDP;
- observa în Wireshark că mesajul este adresat grupului, nu unei adrese unicast;
- extinde receiver-ul pentru a afișa timestamp și numărul de mesaje.

---

### 2. Rularea receiver-ului multicast de exemplu

Într-un terminal:

```bash
python3 index_udp-multicast_receiver_example.py
````

Veți vedea:

```text
[INFO] UDP multicast receiver joined group 224.0.0.1 on port 5001
```

Lăsați programul să ruleze.

(Opțional: porniți încă un receiver pe alt terminal / altă mașină în aceeași rețea.)

---

### 3. Trimiterea unui mesaj multicast

În alt terminal:

```bash
python3 index_udp-multicast_sender_example.py "Hello, multicast group!"
```

În receiver:

```text
[RECV] ... bytes from 127.0.0.1:XXXXX -> "Hello, multicast group!"
```

Dacă aveți mai multe receivere, toate ar trebui să afișeze mesajul.

---

### 4. Captură Wireshark pentru multicast

1. În Wireshark, selectați interfața relevantă.

2. Configurați un **capture filter**:

```text
udp port 5001
```

3. Porniți captura.

4. Trimiteți câteva mesaje multicast:

```bash
python3 index_udp-multicast_sender_example.py "m1"
python3 index_udp-multicast_sender_example.py "m2"
```

5. Opriți captura și aplicați un **display filter**:

```text
udp.port == 5001
```

Sau pentru a vedea doar traficul multicast:

```text
ip.dst == 224.0.0.1 and udp.port == 5001
```

Observați:

* adresa de destinație este 224.0.0.1;
* pachetul ajunge la toate procesele abonate la grup.

---

### 5. Sarcina studentului – receiver multicast cu timestamp

1. Deschideți `index_udp-multicast_receiver_template.py`.

2. Completați secțiunea `TODO` pentru:

* counter mesajelor;
* timestamp lizibil (ex: `2025-03-10 14:32:01`);
* log de forma `[ #N at <timestamp> ] From <ip>:<port> -> "<text>"`.

3. Rulați receiver-ul template:

```bash
python3 index_udp-multicast_receiver_template.py
```

4. Trimiteți 3–5 mesaje multicast.

---

### 6. Dovada de lucru

Veți pregăti:

* `udp_multicast_activity_output.txt`:

  * logurile receiver-ului template pentru cel puțin 5 mesaje;
  * o scurtă comparație (5–7 propoziții) între broadcast și multicast:

    * adresă de destinație,
    * cine primește mesajul,
    * cum se vede în Wireshark;
* `udp_multicast_capture.pcapng`: captura Wireshark pentru traficul multicast.
