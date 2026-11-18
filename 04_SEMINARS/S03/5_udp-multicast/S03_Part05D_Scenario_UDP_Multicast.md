#### `S03_Part05D_Scenario_UDP_Multicast.md`

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
python3 S03_Part05B_Example_UDP_Multicast_Receiver.py
````

You should see:

```text
[INFO] UDP multicast receiver joined group 239.255.0.1 on port 5001
```

Leave the programme running.

(Optional: start another receiver in a different terminal or on another machine within the same network.)

---

### 3. Sending a multicast message

In another terminal:

```bash
python3 S03_Part05A_Example_UDP_Multicast_Sender.py "Hello, multicast group!"
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
python3 S03_Part05A_Example_UDP_Multicast_Sender.py "m1"
python3 S03_Part05A_Example_UDP_Multicast_Sender.py "m2"
```

5. Stop the capture and apply a **display filter**:

```text
udp.port == 5001
```

Or, to see only multicast traffic:

```text
ip.dst == 239.255.0.1 and udp.port == 5001
```

Observe:

* the destination address is 239.255.0.1;
* the packet reaches all processes subscribed to the group.

---

### 5. Student task – multicast receiver with timestamp

1. Open `S03_Part05C_Template_UDP_Multicast_Receiver.py`.

2. Complete the `TODO` section to add:

* a message counter;
* a human-readable timestamp (e.g. `2025-03-10 14:32:01`);
* a log line of the form `[ #N at <timestamp> ] From <ip>:<port> -> "<text>"`.

3. Run the template receiver:

```bash
python3 S03_Part05C_Template_UDP_Multicast_Receiver.py
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

### Interface and membership controls

Use the dedicated laboratory group `239.255.0.1`, not the all-hosts group 224.0.0.1.
For a reproducible same-VM Linux exercise, use two terminals in the same network
namespace and select loopback in both:

```bash
export MCAST_INTERFACE_IP=127.0.0.1
```

Then run the receiver in one terminal and sender in the other using the commands
above. For separate lab nodes, select each node's actual address on their common
interface instead. The default `0.0.0.0` delegates interface selection to the OS.
Linux receivers set `IP_MULTICAST_ALL=0` so only memberships of that socket qualify.
When comparing with a receiver without membership, keep group, interface and socket
binding identical. Other operating systems may have different delivery rules; record
the OS and pre-existing memberships. Group membership is not a delivery guarantee.
