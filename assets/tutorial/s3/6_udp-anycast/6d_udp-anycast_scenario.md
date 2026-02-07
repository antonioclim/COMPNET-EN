### Scenariu: UDP "anycast" simulat (IPv6) + discuție conceptuală

#### 1. Obiectiv

Veți:

- rula un server UDP IPv6 care ascultă pe toate adresele locale;
- rula un client UDP IPv6 care trimite un mesaj către `2001:db8::1`;
- înțelege diferența conceptuală între unicast, broadcast, multicast și anycast;
- extinde server-ul pentru a include un "server_id" în răspuns.

---

### 2. Configurarea adresei IPv6 (laborator, dacă este permis)

Pe unele sisteme, va trebui să adăugați manual o adresă IPv6 de test pe loopback:

```bash
sudo ip -6 addr add 2001:db8::1/64 dev lo
````

(În unele medii de laborator, instructorul poate pregăti deja acest pas.)

---

### 3. Rularea serverului anycast de exemplu

Într-un terminal:

```bash
python3 index_udp-anycast_server_example.py
```

Ar trebui să vedeți:

```text
[INFO] Anycast-like UDP server listening on [::]:5007
```

---

### 4. Rularea clientului anycast

În alt terminal:

```bash
python3 index_udp-anycast_client_example.py
```

Ar trebui să vedeți:

```text
[INFO] Sending to [2001:db8::1]:5007
[INFO] Received response: 'Reply from anycast server' from (...)
```

În server, veți vedea mesajul primit și răspunsul trimis.

---

### 5. Sarcina studentului – server cu server_id

1. Deschideți `index_udp-anycast_server_template.py`.

2. Completați secțiunea `TODO` pentru:

* a cere un `server_id`;
* a include `server_id` în loguri (`[RECV-...]`, `[SEND-...]`);
* a include `server_id` în textul răspunsului.

3. Porniți serverul template:

```bash
python3 index_udp-anycast_server_template.py
```

Introduceți de ex. `S1` ca server_id.

4. Porniți clientul:

```bash
python3 index_udp-anycast_client_example.py
```

Observați:

* în client: răspunsul conține `[S1]`;
* în server: logurile indică `RECV-S1` / `SEND-S1`.

(Opțional: porniți două servere pe mașini diferite, cu același `ANYCAST_ADDR` și vedeți cine răspunde în practică – într-o rețea reală, routing-ul ar alege cel mai apropiat.)

---

### 6. Dovada de lucru

Pregătiți:

* `udp_anycast_activity_output.txt`:

  * loguri de la serverul template cu `server_id`;
  * loguri de la client;
  * o scurtă discuție (5–7 propoziții) în care descrieți:

    * unicast vs broadcast vs multicast vs anycast (conceptual),
    * ce ați simulat efectiv în laborator;
* (opțional, dacă aveți timp) `udp_anycast_capture.pcapng`: captură Wireshark cu traficul IPv6 de test.