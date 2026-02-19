### Scenario: Binary Protocol over TCP – Framing with LEN_BYTE and Serialised Objects

#### 1. Objective

In this stage you will:

- run a TCP server and client that use a *binary* protocol;
- understand the `<LEN_BYTE> <PICKLED_OBJECT>` format;
- extend the protocol with a new `keys` command;
- compare the binary protocol with the text one (advantages / disadvantages).

Estimated duration: ~25 minutes.

---

### 2. Running the Example Server and Client

1. Start the example binary server:

```bash
python3 index_binary-proto_tcp-server_example.py
````

2. In another terminal, start the binary client:

```bash
python3 index_binary-proto_tcp-client_example.py
```

3. At the `connected(binaries)>` prompt, try:

```text
add user1 Alice Wonderland
get user1
remove user1
get user1
exit
```

Note the following:

* you cannot see the command in clear text within the raw traffic (the payload is pickled);
* the client displays only the `payload` from the Response.

---

### 3. Binary Message Format

At the socket level, a complete message looks as follows:

* 1 byte: LEN_BYTE – total message length (including this byte)
* N−1 bytes: payload serialised with `pickle` (Request or Response)

Request:

* `Request(command, key, resource)`

  * `command`: bytes representing the string (e.g. b"add")
  * `key`: b"user1"
  * `resource`: b"Alice Wonderland"

Response:

* `Response(payload)`

  * `payload`: string with the response message (e.g. "user1 added")

Framing:

* the server reads the first chunk, takes `message_length = data[0]`,
* continues reading until `message_length` bytes are available,
* the rest is handled by `pickle`.

---

### 4. Differences from the Text Protocol

Consider the following:

* Text protocol:

  * can be debugged with `nc`, `telnet` or Wireshark (follow TCP stream).
  * visible, human-readable.
* Binary protocol:

  * more compact (no spaces, no digits for large headers).
  * harder to debug without tools that understand the format (pickle, protobuf, etc.).

You will write a few observations about this in the activity file.

---

### 5. Student Task – the `keys` Command

1. Open `index_binary-proto_tcp-server_template.py`.

2. In `process_command()` implement the command:

```text
keys
```

Request:

* `command = "keys"`
* `key` may be ignored or empty – it does not matter.

Response:

* if keys exist in state:

  * payload: list of keys separated by commas, e.g. `"user1, user2, user3"`.
* otherwise:

  * payload: `"no keys"`.

Suggestion:

* use `state.resources.keys()` or the `keys_list()` method if you chose to implement it.

3. Start the template server:

```bash
python3 index_binary-proto_tcp-server_template.py
```

4. Start the example binary client:

```bash
python3 index_binary-proto_tcp-client_example.py
```

5. Test:

```text
add k1 v1
add k2 v2
keys
remove k1
keys
exit
```

Verify:

* that `keys` returns the correct list;
* that after `remove`, the list has been updated.

---

### 6. (Optional) Short Wireshark Capture

If time permits:

1. Start Wireshark with:

```text
tcp port 3333
```

2. Send a few binary commands (`add`, `get`, `keys`).

3. Use *Follow TCP Stream* and observe:

* the payload is not human-readable text;
* all you see is a "binary blob".

Compare with the capture from the text protocol.

---

### 7. Proof of Work

Create the file `binary_proto_activity_output.txt` containing:

1. The list of tested commands and the client responses:

   * include examples with `keys`.

2. 5–7 sentences covering:

   * how text vs binary framing differs;
   * how easy debugging is in each case;
   * when you would prefer text and when you would prefer binary.

(The PCAP is optional; if you include it, name it `binary_proto_capture.pcapng`.)
