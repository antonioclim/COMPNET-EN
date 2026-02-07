### Seminar 10 – SSH în containere Docker + Client Python cu Paramiko

În această secțiune vom învăța:

1. Cum rulăm un server SSH într-un container Docker
2. Cum ne conectăm la acesta folosind un script Python bazat pe biblioteca **Paramiko**
3. Cum executăm comenzi remote și cum transferăm fișiere cu SFTP
4. Cum folosim numele serviciului Docker ca host SSH (DNS intern)

---

## 1. De ce folosim SSH în containere?

SSH este unul dintre cele mai comune servicii de administrare remote.  
Într-o rețea reală, putem avea:

- un bastion SSH
- servere interne accesibile doar prin acest bastion
- scripturi automate care execută comenzi pe hosturi

În versiunea noastră simplificată, avem:

```

ssh-client → ssh-server
(în rețea Docker Compose)

```

---

## 2. Ce este Paramiko?

**Paramiko** este o bibliotecă Python care implementează protocolul SSH2:

- autentificare cu parolă sau chei
- execuție de comenzi remote (`exec_command`)
- transfer fișiere (SFTP)
- tunelare SSH (nu folosim aici)

Avantaje:

- util pentru scripting, automatizare, CI/CD, tooluri de deployment
- API simplu comparat cu generarea de comenzi `ssh` prin `subprocess`

---

## 3. Ce vom realiza

Vom porni un setup Docker Compose:

- `ssh-server`  
  - conține `openssh-server`
  - user: `labuser` parola: `labpass`

- `ssh-client`  
  - conține Python + Paramiko
  - rulează scriptul `paramiko_client.py`

Apoi vom rula:

1. Conectare SSH
2. Execuție comandă remote (`uname -a`, `ls -l`)
3. Upload fișier local → server (SFTP)
4. Download fișier din server → local

Studenții vor completa câteva TODO-uri din script.

---

## 4. Fluxul de lucru

1. `docker compose up --build`  
2. `docker compose exec ssh-client bash`  
3. `python3 paramiko_client.py`  
4. Inspectați fișierele transferate în volumele serverului.
