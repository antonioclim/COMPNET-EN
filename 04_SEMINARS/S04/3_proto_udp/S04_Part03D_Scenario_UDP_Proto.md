### Scenario: Custom Protocol over UDP – Message Types and State Machine

#### 1. Objective

In this stage you will:

- run a UDP server that implements a mini-protocol with CONNECT / SEND / LIST / DISCONNECT messages;
- run an interactive UDP client that sends these messages;
- describe the protocol as a simplified state machine;
- extend the protocol with a new `CLEAR` command.

Estimated duration: ~15–20 minutes.

---

### 2. Running the Example Server and Client

1. Start the server (example):

```bash
python3 index_udp-proto_server_example.py 4000
````

You should see something like:

```text
[INFO] UDP protocol server listening on 0.0.0.0:4000
```

2. In another terminal, start the client:

```bash
python3 index_udp-proto_client_example.py 127.0.0.1 4000
```

3. At the `storage>` prompt, try:

```text
connect
send first note
send second note
list
disconnect
list
exit
```

Note the following:

* the difference between OK and ERR_CONNECTED;
* how LIST behaves before and after DISCONNECT.

---

### 3. The Protocol as a State Machine (conceptual)

Think of the server as having a state *per client (address)*:

* States: `DISCONNECTED`, `CONNECTED`
* Events / messages:

  * `CONNECT`
  * `SEND`
  * `LIST`
  * `DISCONNECT`
  * (in the template) `CLEAR`

Rules (simplified):

* Initial state for an address: `DISCONNECTED`.
* `CONNECT`:

  * DISCONNECTED -> CONNECTED (OK)
  * CONNECTED    -> remains CONNECTED (OK)
* `SEND`:

  * CONNECTED    -> saves note (OK)
  * DISCONNECTED -> ERR_CONNECTED
* `LIST`:

  * CONNECTED    -> sends the notes (OK)
  * DISCONNECTED -> ERR_CONNECTED
* `DISCONNECT`:

  * CONNECTED    -> removes the connection (OK) -> DISCONNECTED
  * DISCONNECTED -> ERR_CONNECTED
* `CLEAR` (in the template, to be implemented):

  * CONNECTED    -> clears the notes, remains CONNECTED (OK)
  * DISCONNECTED -> ERR_CONNECTED

You will use this description in the deliverable file.

---

### 4. Student Task – the CLEAR Command

1. Open `index_udp-proto_server_template.py`.

2. Implement the logic for all messages in the `TODO` block,
   with emphasis on `CLEAR`:

* if the client is in `state.connections`:

  * call `state.clear_notes(address)`
  * respond with `ResponseMessage(ResponseMessageType.OK)`
* otherwise:

  * `ResponseMessage(ResponseMessageType.ERR_CONNECTED)`

3. Open `index_udp-proto_client_template.py` and:

* implement the `clear` command so that it sends
  `RequestMessage(RequestMessageType.CLEAR)`.

4. Run the template server:

```bash
python3 index_udp-proto_server_template.py 4000
```

5. Run the template client:

```bash
python3 index_udp-proto_client_template.py 127.0.0.1 4000
```

Test:

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

Observe:

* before `clear`: LIST shows note1/note2;
* after `clear`: LIST returns an empty payload (or just newlines).

---

### 5. Proof of Work (deliverable)

1. `udp_proto_activity_output.txt` containing:

   * the command sequence used (`connect`, `send`, `list`, `clear`, `disconnect`);
   * the server responses (OK, ERR_CONNECTED, etc.);
   * a short commentary (5–7 sentences) covering:

     * how the `(ip, port)` address is used as a "client identity";
     * the difference between this stateful UDP state machine
       and a stateless / CONNECT-free protocol.

2. `udp_proto_state_machine.md`:

   * textual description of the states (`DISCONNECTED`, `CONNECTED`);
   * a table or list with:

     * `(current state, message)` -> `(new state, response)`;
   * explicitly mention what `CLEAR` does.
