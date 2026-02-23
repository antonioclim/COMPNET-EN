### Seminar 10 – SSH in Docker containers and a Python client with Paramiko

By the end of this section you will know:

1. how to run an SSH server in a Docker container
2. how to connect to it using a Python script based on **Paramiko**
3. how to execute remote commands and transfer files using SFTP
4. how to use the Docker service name as the SSH host (internal DNS)

---

## 1. Why use SSH in containers?

SSH is one of the most common protocols for remote administration.

In a real network you may have:

- an SSH bastion host
- internal servers reachable only through that bastion
- automation scripts that execute commands on remote hosts

In our simplified version, we have:

```text
ssh-client -> ssh-server
(within the Docker Compose network)
```

---

## 2. What is Paramiko?

**Paramiko** is a Python library that implements the SSH2 protocol:

- authentication via password or keys
- remote command execution (`exec_command`)
- file transfer (SFTP)
- SSH tunnelling (not used here)

Advantages:

- useful for scripting, automation, CI/CD and deployment tooling
- a cleaner API than generating `ssh` commands via `subprocess`

---

## 3. What you will build

The Docker Compose setup includes:

- `ssh-server`
  - contains `openssh-server`
  - user: `labuser`, password: `labpass`

- `ssh-client`
  - contains Python + Paramiko
  - runs the script `S10_Part03_Script_Paramiko_Client.py`

Then you will perform:

1. SSH connection
2. remote command execution (`uname -a`, `ls -l`)
3. upload: local file → server (SFTP)
4. download: server file → local (SFTP)

Students will complete a few TODO sections in the script.

---

## 4. Workflow

1. `docker compose up --build`
2. `docker compose exec ssh-client bash`
3. `python3 S10_Part03_Script_Paramiko_Client.py`
4. inspect the transferred files in the server's volume.
