### Tasks — SSH in containers and a Paramiko client

---

## 1. Start the infrastructure

```bash
docker compose up --build
```

Wait until the `ssh-server` service is up.

---

## 2. Run the Paramiko script from the ssh-client container

```bash
docker compose exec ssh-client bash
python3 S10_Part03_Script_Paramiko_Client.py
```

---

## 3. Verify the results

The script will generate:

- `ssh_output.txt` — output of remote commands
- `uploaded_from_client.txt` — file uploaded to the server
- `downloaded_hostname.txt` — file downloaded from the server

---

## 4. Student tasks (required)

### A. Complete the TODO sections in `S10_Part03_Script_Paramiko_Client.py`

- complete the remote command execution step
- complete the SFTP upload section
- complete the SFTP download section

### B. In `ssh_paramiko_report.txt`, write:

1. which remote commands you executed
2. which file you uploaded and where it appears on the server
3. which file you downloaded into the client
4. what advantages Paramiko has compared with a simple SSH CLI (`ssh`)
