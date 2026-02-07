### Scenariu: Protocol custom peste UDP – tipuri de mesaje și mașină de stare

#### 1. Obiectiv

În această etapă veți:

- rula un server UDP care implementează un mini-protocol cu mesaje CONNECT / SEND / LIST / DISCONNECT;
- rula un client UDP interactiv care trimite aceste mesaje;
- descrie protocolul ca o mașină de stare simplificată;
- extinde protocolul cu o nouă comandă `CLEAR`.

Durată estimată: ~15–20 minute.

---

### 2. Rulare server + client de exemplu

1. Porniți serverul (exemplu):

```bash
python3 index_udp-proto_server_example.py 4000
````

Ar trebui să vedeți ceva de genul:

```text
[INFO] UDP protocol server listening on 0.0.0.0:4000
```

2. În alt terminal, porniți clientul:

```bash
python3 index_udp-proto_client_example.py 127.0.0.1 4000
```

3. În prompt-ul `storage>`, încercați:

```text
connect
send first note
send second note
list
disconnect
list
exit
```

Observați:

* diferența dintre OK și ERR_CONNECTED;
* cum se comportă LIST înainte și după DISCONNECT.

---

### 3. Protocolul ca mașină de stare (conceptual)

Gândiți serverul ca având o stare *per client (address)*:

* State: `DISCONNECTED`, `CONNECTED`
* Events / mesaje:

  * `CONNECT`
  * `SEND`
  * `LIST`
  * `DISCONNECT`
  * (în template) `CLEAR`

Reguli (simplificate):

* Starea inițială pentru un address: `DISCONNECTED`.
* `CONNECT`:

  * DISCONNECTED -> CONNECTED (OK)
  * CONNECTED    -> rămâne CONNECTED (OK)
* `SEND`:

  * CONNECTED    -> salvează notă (OK)
  * DISCONNECTED -> ERR_CONNECTED
* `LIST`:

  * CONNECTED    -> trimite notele (OK)
  * DISCONNECTED -> ERR_CONNECTED
* `DISCONNECT`:

  * CONNECTED    -> șterge conexiunea (OK) -> DISCONNECTED
  * DISCONNECTED -> ERR_CONNECTED
* `CLEAR` (în template, de implementat):

  * CONNECTED    -> șterge notele, rămâne CONNECTED (OK)
  * DISCONNECTED -> ERR_CONNECTED

Veți folosi această descriere în fișierul de livrat.

---

### 4. Sarcina studentului – comanda CLEAR

1. Deschideți `index_udp-proto_server_template.py`.

2. Implementați în blocul `TODO` logica pentru toate mesajele,
   cu accent pe `CLEAR`:

* dacă clientul este în `state.connections`:

  * apelați `state.clear_notes(address)`
  * răspundeți cu `ResponseMessage(ResponseMessageType.OK)`
* altfel:

  * `ResponseMessage(ResponseMessageType.ERR_CONNECTED)`

3. Deschideți `index_udp-proto_client_template.py` și:

* implementați comanda `clear` astfel încât să trimită
  `RequestMessage(RequestMessageType.CLEAR)`.

4. Rulați serverul template:

```bash
python3 index_udp-proto_server_template.py 4000
```

5. Rulați clientul template:

```bash
python3 index_udp-proto_client_template.py 127.0.0.1 4000
```

Testați:

```text
connect
send note1
send note2
list
clear
list
disconnect
exit
```

Observați:

* înainte de `clear`: LIST arată note1/note2;
* după `clear`: LIST întoarce un payload gol (sau doar newline-uri).

---

### 5. Dovada de lucru (ce veți preda)

1. `udp_proto_activity_output.txt` care să conțină:

   * secvența de comenzi folosită (`connect`, `send`, `list`, `clear`, `disconnect`);
   * răspunsurile serverului (OK, ERR_CONNECTED etc.);
   * un mic comentariu (5–7 propoziții) despre:

     * cum este folosită adresa `(ip, port)` ca „identitate de client”;
     * diferența dintre această mașină de stare pe UDP
       și un protocol fără stare / fără CONNECT.

2. `udp_proto_state_machine.md`:

   * descriere textuală a stărilor (`DISCONNECTED`, `CONNECTED`);
   * tabel sau listă cu:

     * `(stare curentă, mesaj)` -> `(stare nouă, răspuns)`;
   * menționați explicit ce face `CLEAR`.
