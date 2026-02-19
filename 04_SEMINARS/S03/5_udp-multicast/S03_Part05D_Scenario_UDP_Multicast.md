#### `index_udp-multicast_scenario.md`

````markdown
### Scenario: UDP multicast sender + receiver + Wireshark

#### 1. Objective

You will:

- start a multicast receiver and subscribe to a group;
- send a message to the multicast group with a UDP sender;
- observe in Wireshark that the message is addressed to the group rather than to a unicast address;
- extend the receiver to display a timestamp and message count.

---

### 2. Running the example multicast receiver

In a terminal:

```bash
python3 index_udp-multicast_receiver_example.py
````

You should see:

```text
[INFO] UDP multicast receiver joined group 224.0.0.1 on port 5001
```

Leave the programme running.

(Optional: start another receiver in a different terminal or on another machine within the same network.)

---

### 3. Sending a multicast message

In another terminal:

```bash
python3 index_udp-multicast_sender_example.py "Hello, multicast group!"
```

In the receiver:

```text
[RECV] ... bytes from 127.0.0.1:XXXXX -> "Hello, multicast group!"
```

If you have multiple receivers, all of them should display the message.

---

### 4. Wireshark capture for multicast

1. In Wireshark, select the relevant interface.

2. Set a **capture filter**:

```text
udp port 5001
```

3. Start the capture.

4. Send a few multicast messages:

```bash
python3 index_udp-multicast_sender_example.py "m1"
python3 index_udp-multicast_sender_example.py "m2"
```

5. Stop the capture and apply a **display filter**:

```text
udp.port == 5001
```

Or, to see only multicast traffic:

```text
ip.dst == 224.0.0.1 and udp.port == 5001
```

Observe:

* the destination address is 224.0.0.1;
* the packet reaches all processes subscribed to the group.

---

### 5. Student task – multicast receiver with timestamp

1. Open `index_udp-multicast_receiver_template.py`.

2. Complete the `TODO` section to add:

* a message counter;
* a human-readable timestamp (e.g. `2025-03-10 14:32:01`);
* a log line of the form `[ #N at <timestamp> ] From <ip>:<port> -> "<text>"`.

3. Run the template receiver:

```bash
python3 index_udp-multicast_receiver_template.py
```

4. Send 3–5 multicast messages.

---

### 6. Proof of work

Prepare the following:

* `udp_multicast_activity_output.txt`:

  * template receiver logs for at least 5 messages;
  * a short comparison (5–7 sentences) between broadcast and multicast:

    * destination address,
    * who receives the message,
    * how each appears in Wireshark;
* `udp_multicast_capture.pcapng`: the Wireshark capture for the multicast traffic.

