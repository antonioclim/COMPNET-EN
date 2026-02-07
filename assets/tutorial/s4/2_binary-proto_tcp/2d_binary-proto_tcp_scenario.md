### Scenariu: Protocol binar peste TCP – framing cu LEN_BYTE și obiecte serializate

#### 1. Obiectiv

În această etapă veți:

- rula un server și un client TCP care folosesc un protocol *binar*;
- înțelege formatul `<LEN_BYTE> <PICKLED_OBJECT>`;
- extinde protocolul cu o nouă comandă `keys`;
- compara protocolul binar cu cel text (avantaje / dezavantaje).

Durată estimată: ~25 minute.

---

### 2. Rularea serverului și clientului de exemplu

1. Porniți serverul binar de exemplu:

```bash
python3 index_binary-proto_tcp-server_example.py
````

2. În alt terminal, porniți clientul binar:

```bash
python3 index_binary-proto_tcp-client_example.py
```

3. În prompt-ul `connected(binaries)>`, încercați:

```text
add user1 Alice Wonderland
get user1
remove user1
get user1
exit
```

Observați:

* nu vedeți comanda în clar în traficul brut (payload-ul e pickle);
* clientul afișează doar `payload` din Response.

---

### 3. Formatul de mesaj binar

La nivel de socket, un mesaj complet arată așa:

* 1 octet: LEN_BYTE – lungimea totală a mesajului (inclusiv acest byte)
* N-1 octeți: payload serializat cu `pickle` (Request sau Response)

Request:

* `Request(command, key, resource)`

  * `command`: bytes reprezentând string-ul (ex: b"add")
  * `key`: b"user1"
  * `resource`: b"Alice Wonderland"

Response:

* `Response(payload)`

  * `payload`: string cu mesajul de răspuns (ex: "user1 added")

Framing-ul:

* serverul citește primul chunk, ia `message_length = data[0]`,
* continuă să citească până are `message_length` bytes,
* restul e treaba lui `pickle`.

---

### 4. Diferențe față de protocolul text

Gândiți:

* Text protocol:

  * poate fi debug-uit cu `nc`, `telnet` sau `Wireshark` (follow TCP stream).
  * vizibil, lizibil.
* Binary protocol:

  * mai compact (fără spații, fără cifre pentru header-uri mari).
  * mai greu de debug-uit fără tool-uri care cunosc formatul (pickle, protobuf etc).

Veți scrie câteva observații despre asta în fișierul de activitate.

---

### 5. Sarcina studentului – comanda `keys`

1. Deschideți `index_binary-proto_tcp-server_template.py`.

2. În `process_command()` implementați comanda:

```text
keys
```

Cerere:

* `command = "keys"`
* `key` poate fi ignorat sau gol, nu contează.

Răspuns:

* dacă există chei în state:

  * payload: listă de chei separate prin virgule, ex: `"user1, user2, user3"`.
* altfel:

  * payload: `"no keys"`.

Sugestie:

* folosiți `state.resources.keys()` sau metoda `keys_list()` dacă ați decis să o implementați.

3. Porniți serverul template:

```bash
python3 index_binary-proto_tcp-server_template.py
```

4. Porniți clientul binar de exemplu:

```bash
python3 index_binary-proto_tcp-client_example.py
```

5. Testați:

```text
add k1 v1
add k2 v2
keys
remove k1
keys
exit
```

Verificați:

* că `keys` întoarce lista corectă;
* că după `remove`, lista s-a actualizat.

---

### 6. (Opțional) Mică captură Wireshark

Dacă aveți timp:

1. Porniți Wireshark cu:

```text
tcp port 3333
```

2. Trimiteți câteva comenzi binare (`add`, `get`, `keys`).

3. Dați *Follow TCP Stream* și observați:

* payload-ul nu e text lizibil;
* tot ce vedeți e „binary blob”.

Comparați cu captura din protocolul text.

---

### 7. Dovada de lucru

Creați fișierul `binary_proto_activity_output.txt` care să conțină:

1. Lista de comenzi testate și răspunsurile clientului:

   * incluzi și exemple cu `keys`.

2. 5–7 propoziții despre:

   * cum diferă framing-ul text vs binary;
   * cât de ușor e debugging-ul în fiecare caz;
   * când ați prefera text și când ați prefera binary.

(PCAP-ul e opțional; dacă îl folosiți, îl puteți numi `binary_proto_capture.pcapng`.)
