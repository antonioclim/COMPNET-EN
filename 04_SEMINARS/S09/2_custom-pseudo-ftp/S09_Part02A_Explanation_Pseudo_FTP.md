### Stage 3 — Pseudo-FTP Protocol (Control + Data, Active and Passive Mode)

In this stage we use a custom protocol inspired by FTP:

- **one control connection**: text commands
- **separate data connections**: for file transfer

Objectives:

- understand in practice the difference between control and data
- see what active/passive modes look like when implemented manually
- experiment with a mini FTP-style server written with sockets

---

## 1. The Control Connection

The client and server maintain a permanent TCP connection (port 3333):

- text commands are sent over this connection:
  - `list`
  - `active_get filename`
  - `active_put filename`
  - `passive_get filename`
  - `passive_put filename`

The server:

- reads the command line
- determines which operation must be performed
- starts/uses a second TCP connection for data

---

## 2. Data Connections (Inspired by FTP)

Our protocol has 4 main commands, which map to real FTP as follows:

| Command            | Role                    | Who listens on the data port?        |
|--------------------|-------------------------|--------------------------------------|
| `list`             | control only (no data)  | –                                    |
| `active_get file`  | active GET (RETR)       | client listens, server connects      |
| `active_put file`  | active PUT (STOR)       | client listens, server connects      |
| `passive_get file` | passive GET (RETR)      | server listens, client connects      |
| `passive_put file` | passive PUT (STOR)      | server listens, client connects      |

Similar to FTP:

- **active mode**: the server connects to the client on an announced port
- **passive mode**: the server opens a port and the client connects to it

---

## 3. Data Transfer Structure

In this laboratory, for simplicity:

- each transfer uses a single message:
  - 1 byte: content length (max ~255 bytes — this is purely a didactic example)
  - the rest: file content
- `recv(BUFFER_SIZE)` is used and we assume the data arrives in a single `recv`.

This approach is **not robust** for production, but it suffices
to understand the idea of application-level protocols over TCP.

---

## 4. Code Structure

### Server (`pseudo_ftp_server.py`)

- listens on `HOST`, `PORT` (e.g. 127.0.0.1:3333) for control connections
- when a client connects:
  - starts a command thread `handle_client_commands`
  - the command is decoded and sent to `process_command`
  - depending on the command, it calls:
    - `process_list`
    - `active_get`
    - `active_put`
    - `passive_get`
    - `passive_put`

Files on the server reside in the directory:

```text
FILE_ROOT = "./temp"
```

### Client (`pseudo_ftp_client.py`)

* connects to the server on control port 3333
* displays a `->` prompt
* depending on the entered command:

  * for `list` it sends the command and displays the text response
  * for `active_get/put`:

    * starts a temporary server (data socket) on the client
    * announces the port to the server
    * receives/sends the file content
  * for `passive_get/put`:

    * asks the server for a temporary port
    * connects to the announced port to transfer the file

The client's local files are in:

```text
LOCAL_STORAGE = "./client-temp"
```

## 5. What the Student Must Do in This Stage

* start the server and the client
* test `list`, `active_get`, `active_put`, `passive_get`, `passive_put`
* verify that files are transferred correctly between:

  * the server directory (`./temp`)
  * the client directory (`./client-temp`)
* complete a few simple TODOs (help, feedback messages)
* document the tests in `pseudoftp_log.txt`
