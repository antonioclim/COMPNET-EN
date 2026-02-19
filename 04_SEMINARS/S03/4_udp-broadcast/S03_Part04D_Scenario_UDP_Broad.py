"""
### Scenario: UDP broadcast sender + receiver (IPv4) + Wireshark

#### 1. Objective

In this stage you will:

- run a UDP receiver that listens for broadcast messages;
- run a UDP sender that transmits broadcast periodically;
- observe how broadcast traffic appears in Wireshark;
- complete a receiver template with filtering and message-counting logic.

---

### 2. Running the example receiver

In a terminal:

```bash
python3 index_udp-broadcast_receiver_example.py
````

You should see:

```text
[INFO] UDP broadcast receiver listening on 0.0.0.0:5007
```

Leave the programme running.

---

### 3. Running the example sender

In another terminal:

```bash
python3 index_udp-broadcast_sender_example.py "Hello, broadcast"
```

You should see in the sender:

```text
[INFO] Sending UDP broadcast to 255.255.255.255:5007
[SEND] ... bytes -> 255.255.255.255:5007 :: 'Hello, broadcast #0'
...
```

And in the receiver:

```text
[RECV] ... bytes from 127.0.0.1:XXXXX -> 'Hello, broadcast #0'
[RECV] ... bytes from 127.0.0.1:XXXXX -> 'Hello, broadcast #1'
...
```

---

### 4. Wireshark capture for broadcast

1. Open **Wireshark** and select the relevant interface (`lo`, `eth0`, `wlan0`, etc.).

2. Set a **capture filter** for the UDP port:

```text
udp port 5007
```

3. Start the capture.

4. Run the sender if it is not already running and allow it to send a few messages.

5. Stop the capture and apply a **display filter** such as:

```text
udp.port == 5007
```

or, to see broadcast only:

```text
ip.dst == 255.255.255.255 and udp.port == 5007
```

Observe:

* UDP packets with destination 255.255.255.255;
* the same datagram reaches every process listening on port 5007.

---

### 5. Student task – receiver with filtering

1. Open `index_udp-broadcast_receiver_template.py`.

2. Complete the `TODO` section so that the receiver:

* counts the received messages (counter);
* ignores messages that do not begin with `"Hello"`;
* displays `[OK]` and `[SKIP]` logs as described in the instructions.

3. Run the template receiver:

```bash
python3 index_udp-broadcast_receiver_template.py
```

4. Run the sender:

```bash
python3 index_udp-broadcast_sender_example.py "Hello, broadcast"
```

5. Also send a few manual test messages, for example with `netcat`:

```bash
echo "Hello manual" | nc -u 255.255.255.255 5007
echo "Other text" | nc -u 255.255.255.255 5007
```

Observe that:

* messages prefixed with "Hello" appear as `[OK]`;
* all others appear as `[SKIP]`.

---

### 6. Proof of work

Prepare the following:

* `udp_broadcast_activity_output.txt`:

  * relevant logs from the template receiver (at least 5 messages, with `[OK]` and `[SKIP]`);
  * a brief commentary (3–5 sentences) about how broadcast appears in Wireshark (destination, port, repetition, etc.);
* `udp_broadcast_capture.pcapng`:

  * the Wireshark capture containing the UDP broadcast traffic.
"""
