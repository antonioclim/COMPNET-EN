### Scenario: Text Protocol over TCP – Framing, Commands and Mini-Spec

#### 1. Objective

In this stage you will:

- run a TCP server and client that implement a simple text protocol;
- understand how framing works using a length header;
- extend the protocol with a new `count` command;
- describe the protocol as a mini-specification (text plus a simplified state-machine representation).

Estimated duration: ~30–35 minutes out of 80.

---

### 2. Running the Example Server and Client

1. Start the example server:

```bash
python3 index_text-proto_tcp-server_example.py
````

You should see:

```text
[START] Text protocol TCP server on 127.0.0.1:3333
```

2. In another terminal, start the example client:

```bash
python3 index_text-proto_tcp-client_example.py
```

3. At the `connected>` prompt, try:

```text
add user1 Alice
get user1
remove user1
get user1
exit
```

Note the following:

* the format of commands (command, key, resource…);
* the server responses (text message);
* the fact that the protocol does **not** close the connection on `exit` – the client simply stops sending commands.

---

### 3. Message Format Analysis

Use `print` (if you wish) or simply reason through the following:

* Message sent by the client:

  * `"TOTAL_LENGTH command key [resource...]"` as a string,
  * encoded in UTF-8,
  * TOTAL_LENGTH is the total character count of the entire line.

* The server:

  * reads the first fragment,
  * extracts `TOTAL_LENGTH` (the first value),
  * continues reading until exactly `TOTAL_LENGTH` characters have been collected,
  * parses and executes the command.

In the mini-spec, note explicitly:

* Request:

  * `REQUEST = <LEN> SP <COMMAND_LINE>`
  * `COMMAND_LINE = <COMMAND> SP <KEY> [SP <RESOURCE>...]`

* Response:

  * `RESPONSE = <LEN> SP <PAYLOAD>`

---

### 4. Short Wireshark Capture (optional)

If time permits:

1. Open **Wireshark** and select the interface (`lo` / `Loopback` or another).

2. Set a **capture filter**:

```text
tcp port 3333
```

3. Start the capture.

4. Send 2–3 commands from the client (`add`, `get`, `remove`).

5. Stop the capture and apply a **display filter**:

```text
tcp.port == 3333
```

Observe:

* that the payload is plain text (visible when you follow the TCP stream);
* there is no special delimiter between messages at the TCP level – framing is performed *in the application* (via the length field).

---

### 5. Student Task – Extending the Protocol (the `count` Command)

1. Open `index_text-proto_tcp-server_template.py`.

2. Implement:

* the `count()` method in `State` (if you choose to use it);
* in `process_command`, the command:

```text
count
```

takes no arguments; the response must be:

```text
"<N> keys"
```

where `N` is the current number of keys in `state`.

3. For unrecognised commands, return:

```text
"ERR unknown command"
```

framed with `build_framed_response()`.

4. Start the template server:

```bash
python3 index_text-proto_tcp-server_template.py
```

5. Run the example client:

```bash
python3 index_text-proto_tcp-client_example.py
```

Test sequences such as:

```text
add k1 v1
add k2 v2
count
remove k1
count
get k3
foo something
exit
```

Verify:

* that `count` returns the expected number;
* that the unrecognised command `foo` returns `ERR unknown command`.

---

### 6. Protocol Mini-Specification (deliverable)

Create a file `text_protocol_spec.md` containing:

1. **Informal description** (max 10–15 lines):

   * What the protocol does
   * Which commands exist: `add`, `remove`, `get`, `count`
   * Typical responses (OK, not found, error)

2. **Request/response format** (pseudo-grammar):

   * `REQUEST = <LEN> SP <COMMAND_LINE>`
   * `COMMAND_LINE = <COMMAND> [SP <KEY> [SP <RESOURCE>...]]`
   * `RESPONSE = <LEN> SP <PAYLOAD>`

3. **Command list**:

   * `add <key> <resource...>` – description
   * `remove <key>` – description
   * `get <key>` – description
   * `count` – description

4. **Simplified state-machine representation** (text, not necessarily a diagram):

   * The connection state is always "CONNECTED" until the client closes.
   * For each message:

     * the server receives a REQUEST,
     * executes the command,
     * sends a RESPONSE,
     * returns to the same state: "awaiting REQUEST".

   (You may also describe this as a list of "events" + "actions".)

---

### 7. Proof of Work (what you upload)

* `text_protocol_spec.md` – the protocol mini-spec.
* `text_proto_activity_output.txt`:

  * log with the tested commands (`add`, `remove`, `get`, `count`, invalid commands);
  * the responses received by the client;
  * a short commentary (5–7 sentences) covering:

    * why a length header is needed,
    * what happens if the message is truncated or the header is invalid.

(The Wireshark PCAP is optional for this seminar – if you include it, name it `text_proto_capture.pcapng`.)
