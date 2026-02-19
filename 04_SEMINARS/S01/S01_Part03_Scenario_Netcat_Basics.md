### Introduction

This stage focuses on `netcat` (`nc`), one of the most versatile tools for testing connections, transferring data and quickly simulating servers and clients. Both TCP mode and UDP mode are covered to illustrate the functional differences between them.

---

### TCP server and client with netcat

#### 1. Start a TCP server on port 9000

```
nc -l -p 9000
```

The command remains blocked while it waits for a connection.

#### 2. Connect a TCP client

From another terminal:

```
nc 127.0.0.1 9000
```

Type text in either terminal. Netcat will forward it automatically to the other side.

---

### UDP server and client with netcat

UDP does not create a persistent connection, so netcat behaves slightly differently in this mode.

#### 3. Start a UDP server on port 9001

```
nc -u -l -p 9001
```

#### 4. Send a UDP message to the server

```
echo "test UDP" | nc -u 127.0.0.1 9001
```

Observe that the UDP server receives the message but does not maintain a session. For bidirectional exchange, use separate commands.

---

### Notes

Note that:

* TCP provides a stable, bidirectional connection, which is immediately visible in netcat behaviour: anything you type on one side appears on the other.
* UDP sends individual datagrams without maintaining state. Netcat will receive only each message that is sent separately.
* Netcat is useful for quick debugging, especially when testing firewalls, routing or prototyping a text protocol.
