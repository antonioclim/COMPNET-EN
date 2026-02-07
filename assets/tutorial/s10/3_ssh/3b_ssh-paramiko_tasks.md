### Sarcini – SSH în containere + client Paramiko

---

## 1. Porniți infrastructura

```

docker compose up --build

```

Așteptați ca serviciul `ssh-server` să pornească.

---

## 2. Executați scriptul Paramiko din containerul ssh-client

```

docker compose exec ssh-client bash
python3 paramiko_client.py

```

---

## 3. Verificați rezultatele

Veți genera fișiere:

- `ssh_output.txt` – output-ul comenzilor remote
- `uploaded_from_client.txt` – fișierul upload-at pe server
- `downloaded_hostname.txt` – fișier download-at de pe server

---

## 4. Sarcini pentru studenți (obligatoriu)

### A. Completați TODO-urile din scriptul `paramiko_client.py`  
- completarea comenzii remote  
- completarea secțiunii SFTP upload  
- completarea secțiunii SFTP download  

### B. În `ssh_paramiko_report.txt`, scrieți:  
1. Ce comenzi remote ați executat  
2. Ce fișier ați upload-at și unde apare pe server  
3. Ce fișier ați download-at în client  
4. Ce avantaje are Paramiko față de un simplu `ssh` CLI  


