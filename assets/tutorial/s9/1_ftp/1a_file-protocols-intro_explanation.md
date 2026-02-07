# **Stage 1 – Introducere protocoale de fișiere**

### `index_file-protocols_intro.md`

```markdown
### Seminar 9 – Protocoale de fișiere: FTP, active/passive, control + data

În acest seminar vom studia modul în care se transferă fișiere prin rețea, folosind:

- un server FTP real implementat cu `pyftpdlib`
- un protocol custom (pseudo-FTP) care folosește două conexiuni, similar cu FTP
- testare multi-client cu containere

Scopul acestei prime etape este să înțelegem **conceptual** cum funcționează protocoalele de transfer de fișiere.

---

## 1. Ce sunt protocoalele de transfer de fișiere?

Exemple cunoscute:
- **FTP** – File Transfer Protocol (vintage, încă folosit, complet necriptat)
- **FTPS** – FTP over TLS
- **SFTP** – Secure File Transfer Protocol (parte din SSH, complet diferit de FTP!)
- **HTTP/HTTPS** – foarte des folosit pentru descărcări/upload
- **NFS**, **SMB** – pentru montare de directoare în rețea (file sharing)

În acest seminar ne concentrăm pe ideea de **două fluxuri**:
- un canal de **control** (comenzi)
- un canal de **transfer** (date brute)

---

## 2. Conexiunea de control vs conexiunea de date

FTP clasic folosește:

1. **Conexiune de control**: port 21  
   Aici circulă *comenzi*: `USER`, `PASS`, `LIST`, `RETR`, `STOR`

2. **Conexiune de date**: porturi diferite  
   Folosită DOAR pentru transferul efectiv al fișierelor.

În pseudo-FTP-ul din seminar vom replica exact această idee.

---

## 3. Mod activ și mod pasiv

### Mod activ (Active Mode)
- Clientul începe transferul **ascultând pe un port**.
- Serverul FTP se conectează la client pe portul anunțat.

Schema:

```

client ---control---> server
client <---data------ server (conexiune inițiată de server)

```

Probleme:
- aproape imposibil prin firewall/NAT modern

---

### Mod pasiv (Passive Mode)
- Serverul deschide un port temporar.
- Clientul se conectează la acel port pentru transfer.

Schema:

```

client ---control---> server
client ------data---> server

```

Avantaj:
- funcționează mult mai bine cu NAT/firewall → este modul standard în zilele noastre.

Aceste două moduri apar explicit în pseudo-FTP-ul nostru.

---

## 4. Mini-întrebări (de scris în fișierul de log)

1. Care este diferența dintre conexiunea de **control** și **conexiunea de date**?  
2. De ce modul activ este dificil în rețele moderne?  
3. Ce avantaje are modul pasiv?  
4. De ce protocoale precum SFTP/HTTPS sunt preferate astăzi?

Scrieți răspunsurile într-un fișier:

```

intro_file_protocols_log.txt

```

Acesta va fi livrabilul pentru Stage 1.

