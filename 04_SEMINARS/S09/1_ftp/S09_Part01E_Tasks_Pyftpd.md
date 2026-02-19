### Stage 2 — FTP Server + FTP Client Tasks

---

## 1. Start the pyftpdlib server

In a terminal run:

```

python3 S09_Part03_Script_Pyftpd_Server.py

```

You should see:

```

FTP server (pyftpdlib) started on port 2121...
User: test / 12345

```

---

## 2. Test the connection with a CLI FTP client (optional)

```

ftp 127.0.0.1 2121
Name: test
Password: 12345
ftp> ls
ftp> get a.txt
ftp> bye

```

---

## 3. Modify and run the Python client

```

python3 pyftpd_client.py

```

Complete the TODOs so that the client:

- displays the file list
- downloads a file
- uploads a file

---

## 4. Mandatory tests (write in pyftpd_log.txt)

Execute and save the output for:

1. LIST (displaying the files)
2. RETR for an existing file
3. STOR for a new file
4. What happens if you attempt to download a non-existent file?
5. (optional) logging in with username/password instead of anonymous

Format:

```

---- LIST ---- <output here>

---- RETR ---- <output here>

---- STOR ---- <output here>

---- Observations ----
<short sentences about what works, what does not, what you understood>

```

This log file will be the deliverable for Stage 2.
