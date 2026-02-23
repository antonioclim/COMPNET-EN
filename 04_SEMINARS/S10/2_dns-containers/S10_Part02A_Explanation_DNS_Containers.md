### Seminar 10 – DNS in Docker containers and a minimal custom DNS server

This section addresses two important ideas:

1. **Built-in DNS in Docker Compose** – Docker provides an internal DNS service that allows containers to resolve each other using the service name.
2. **A minimal DNS server written in Python** that answers a single query, in order to understand the mechanism.

---

## 1. Built-in DNS in Docker

When you use `S10_Part02_Config_Docker_Compose.yml`, each service receives automatically:

- a DNS name equal to the service name
- an internal IP address
- access to Docker's embedded DNS resolver

Example:

```yaml
services:
  web:
    image: python:3
  db:
    image: redis
  debug:
    image: busybox
```

From inside the `debug` container:

```sh
ping web
ping db
nslookup web
```

Docker will resolve the name `web` to the internal IP address of the `web` container.

---

## 2. Minimal custom DNS server (concept)

The setup consists of:

- a container named `dns-server`
- a Python script that listens on UDP port 5353
- a simple rule:

  **if someone asks for `myservice.lab.local`, the server responds with a fixed IP address**

This is not a full DNS server. It is intentionally simplified so that you can understand:

- how a DNS message is received over UDP
- what a DNS query looks like at a high level
- how a valid response is constructed

We use the **dnslib** library because it makes encoding and decoding DNS messages much simpler than implementing the protocol manually.

---

## 3. What you will test

Inside the `debug` container:

1. resolve Docker service names:

```sh
dig web
dig db
```

2. resolve names handled by your custom DNS server:

```sh
dig @dns-server myservice.lab.local
dig @dns-server doesnotexist.local
```

3. compare the output between the built-in DNS and the Python mini DNS.

---

## 4. Files in this section

- `S10_Part02_Config_Docker_Compose.yml`
- `S10_Part02_Config_Dockerfile`
- `S10_Part02_Script_DNS_Server.py`
- `S10_Part02_Page_DNS_Containers.html`

---

## Tasks — DNS in containers and minimal custom DNS

### 1. Start the Docker infrastructure

From this directory, run:

```bash
docker compose up --build
```

Wait for the services `web`, `debug` and `dns-server` to start.

---

### 2. Test built-in DNS

Enter the debug container:

```bash
docker compose exec debug sh
```

Run:

```sh
ping web
ping db
dig web
dig db
```

Save the output in:

```text
seminar10_dns_builtin_output.txt
```

---

### 3. Test the custom DNS server

Still inside the `debug` container:

```sh
dig @dns-server myservice.lab.local
dig @dns-server doesnotexist.local
```

Save the output in:

```text
seminar10_dns_custom_output.txt
```

---

### 4. Final comparison

In `seminar10_dns_comparison.txt` explain:

- the difference between Docker's built-in DNS and the custom DNS server
- the advantage of a "real" DNS server compared with this simplified implementation
- why `dnslib` is often used for DNS prototypes

After you complete this section, you will move to **SSH with Paramiko** in containers.
