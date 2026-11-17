### Scenario: simulated UDP "anycast" (IPv6) + conceptual discussion

#### 1. Objective

You will:

- run a UDP IPv6 server that listens on all local addresses;
- run a UDP IPv6 client that sends a message to `::1`;
- understand the conceptual difference between unicast, broadcast, multicast and anycast;
- extend the server to include a "server_id" in its response.

---

### 2. Local IPv6 baseline

The example client uses `::1` (IPv6 loopback), so no additional address is needed.
This is an analogy for selecting one local endpoint, not a real routed anycast deployment.
A routed anycast extension requires an explicitly configured shared address and routing.

### 3. Running the example anycast server

In a terminal:

```bash
python3 S03_Part06A_Example_UDP_Anycast_Server.py
```

You should see:

```text
[INFO] Anycast-like UDP server listening on [::]:5007
```

---

### 4. Running the anycast client

In another terminal:

```bash
python3 S03_Part06B_Example_UDP_Anycast_Client.py
```

You should see:

```text
[INFO] Sending to [::1]:5007
[INFO] Received response: 'Reply from anycast server' from (...)
```

In the server terminal the received message and sent reply will appear.

---

### 5. Student task – server with server_id

1. Open `S03_Part06C_Template_UDP_Anycast.py`.

2. Complete the `TODO` section to:

* prompt for a `server_id`;
* include `server_id` in logs (`[RECV-...]`, `[SEND-...]`);
* include `server_id` in the reply text.

3. Start the template server:

```bash
python3 S03_Part06C_Template_UDP_Anycast.py
```

Enter e.g. `S1` as the server_id.

4. Start the client:

```bash
python3 S03_Part06B_Example_UDP_Anycast_Client.py
```

Observe:

* in the client: the reply contains `[S1]`;
* in the server: the logs show `RECV-S1` / `SEND-S1`.

(Optional: start two servers on different machines, with the same `ANYCAST_ADDR`, and observe which one responds in practice — in a real network the routing layer would select the nearest one.)

---

### 6. Proof of work

Prepare the following:

* `udp_anycast_activity_output.txt`:

  * logs from the template server with `server_id`;
  * client logs;
  * a short discussion (5–7 sentences) in which you describe:

    * unicast vs broadcast vs multicast vs anycast (conceptually),
    * what you effectively simulated in the laboratory;
* (optional, if time permits) `udp_anycast_capture.pcapng`: a Wireshark capture with the test IPv6 traffic.
