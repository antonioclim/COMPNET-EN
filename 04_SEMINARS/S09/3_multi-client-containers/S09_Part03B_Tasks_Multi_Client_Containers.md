### Stage 4 — Tasks: Multi-Client with Containers (FTP Server + 2 Clients)

Objective:
- simulate two clients using the same FTP server
- observe how a file uploaded by client1 can be downloaded by client2

Result:
- a log file: `ftp_multi_client_log.txt`
- files in the directories: `server-data/`, `client1-data/`, `client2-data/`

---

## 1. Preparing the environment

Make sure you have the following files in the same directory:

- `S09_Part03_Config_Docker_Compose.yml`
- `S09_Part03_Script_Pyftpd_Server.py`
- `S09_Part03_Script_Pyftpd_Multi_Client.py`

Create the required directories:

```bash
mkdir -p server-data server-anon client1-data client2-data
````

(Optional) create an initial file in `client1-data`:

```bash
echo "Hello from client1" > client1-data/from_client1.txt
```

---

## 2. Start the Docker services

Run:

```bash
docker compose up -d
```

Verify:

```bash
docker ps
```

You should see:

* `seminar9_ftp_server`
* `seminar9_client1`
* `seminar9_client2`

---

## 3. Test: client1 performs an upload

Enter the client1 container:

```bash
docker exec -it seminar9_client1 /bin/sh
```

Inside the container:

```sh
ls client-data
# make sure from_client1.txt exists (or create one)

python3 S09_Part03_Script_Pyftpd_Multi_Client.py upload from_client1.txt
```

Record the output in `ftp_multi_client_log.txt` under the section:

```text
--- CLIENT1 UPLOAD ---
<o>
```

On the host, verify:

```bash
ls server-data
```

It should contain `from_client1.txt`.

---

## 4. Test: client2 performs a download

Enter the client2 container:

```bash
docker exec -it seminar9_client2 /bin/sh
```

Inside:

```sh
python3 S09_Part03_Script_Pyftpd_Multi_Client.py download from_client1.txt
ls client-data
cat client-data/from_client1.txt
```

Record the output (including the file contents) in `ftp_multi_client_log.txt` under:

```text
--- CLIENT2 DOWNLOAD ---
<o>
```

---

## 5. Optional: test from the host

From the host machine (outside the containers):

1. Verify that the server responds on port 2121:

```bash
ftp 127.0.0.1 2121
# name: test
# password: 12345
ftp> ls
ftp> bye
```

2. Or use the Python client from Stage 2 (if it is in the same directory):

```bash
python3 pyftpd_client.py
```

Add at least one output fragment to `ftp_multi_client_log.txt` under:

```text
--- HOST TEST ---
<o>
```

---

## 6. Reflection questions (write in ftp_multi_client_log.txt)

Answer in a few sentences:

1. What is the server's role in this scenario? Why do client1 and client2 not need
   to know each other directly?
2. Why could such a server be useful within an organisation (e.g. a department or a team)?
3. What advantages does running the server and clients in separate containers bring?
4. How would you extend this scenario towards something resembling FXP (server-to-server transfer)?

---

### Stage 4 Deliverables

Submit:

* `S09_Part03_Config_Docker_Compose.yml`
* `S09_Part03_Script_Pyftpd_Server.py`
* `S09_Part03_Script_Pyftpd_Multi_Client.py`
* `ftp_multi_client_log.txt` with:

  * upload output (client1)
  * download output (client2)
  * optional: the host test
  * answers to the reflection questions

This concludes Seminar 9:

* real FTP (pyftpdlib)
* active/passive pseudo-FTP protocol
* multi-client scenario with containers.
