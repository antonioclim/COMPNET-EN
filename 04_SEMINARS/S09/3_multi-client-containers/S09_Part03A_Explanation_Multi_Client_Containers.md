### Stage 4 — Multi-Client Testing with Containers (FTP Server + 2 Clients)

In this stage we use Docker containers to simulate:

- **a file server** (FTP with pyftpdlib)
- **two independent clients** (client1 and client2) that:
  - connect to the same server
  - use the same protocol (FTP)
  - transfer files through the server

Basic scenario:

1. client1 **uploads** a file to the server
2. client2 **downloads** the same file from the server
3. we demonstrate that the file travelled from client1 to client2 **via the server**

This scenario is analogous to real-world situations:

- multiple machines using the same FTP server for file sharing
- "indirect" flows: client A -> server -> client B

---

## 1. Architecture with Docker Compose

We will have a `S09_Part03_Config_Docker_Compose.yml` with 3 services:

- `ftp-server`
  - image: `python:3`
  - runs `S09_Part03_Script_Pyftpd_Server.py` with pyftpdlib
  - has a volume `./server-data` mounted as the FTP data directory

- `client1`
  - image: `python:3`
  - does nothing automatically (stays "alive" with `tail -f /dev/null`)
  - we enter the container with `docker exec` and run the client script

- `client2`
  - same as `client1`

All services:

- are on the same Docker network (e.g. `ftpnet`)
- can resolve `ftp-server` as a hostname
- can use port 2121 for FTP

Additionally, we map port 2121 to the host, so that:

- we can also test the server from outside the containers:
  - `ftp 127.0.0.1 2121`
  - or `python3 pyftpd_client.py` from the host.

---

## 2. Laboratory Scenario

1. `docker compose up -d` starts:
   - the FTP server
   - client1
   - client2

2. In `client1`:
   - we run a Python script `S09_Part03_Script_Pyftpd_Multi_Client.py`
   - the script connects to `ftp-server:2121`
   - it uploads (`STOR`) a file (e.g. `from_client1.txt`)

3. In `client2`:
   - we run the same script, but in download mode (`RETR`)
   - we download the same file into the `client2` container

4. We verify that:

- the file appears in the server volume (`./server-data`)
- the file has reached client2

---

## 3. Connection with the Other Stages

- Stage 2: you ran `S09_Part03_Script_Pyftpd_Server.py` and `pyftpd_client.py` on the local machine.
- Stage 3: you worked with active/passive pseudo-FTP (custom protocol over TCP).
- Stage 4: you use a real FTP server (pyftpdlib) in a multi-client environment
  — a scenario much closer to real-world usage.

---

## 4. Terminology

- **service** in Docker Compose:
  - defines an application (container) + its configuration
- **network**:
  - virtual address space for inter-service communication
- **volume**:
  - persistent directory for data
  - here: `./server-data` will contain the FTP server's files
