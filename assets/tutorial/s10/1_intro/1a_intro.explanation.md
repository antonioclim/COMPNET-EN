Perfect — trecem la **Stage 1 – Intro DNS/SSH & unelte**.
### Seminar 10 – Servicii de rețea: DNS și SSH (Introducere)

În acest seminar vom lucra cu două servicii fundamentale de rețea:

- **DNS (Domain Name System)** – pentru rezoluția numelor în adrese IP  
- **SSH (Secure Shell)** – pentru administrare remote, execuție de comenzi și transfer de fișiere

Aceste concepte vor fi folosite în containere Docker, în scenarii reale.

---

### 1. Recapitulare DNS

DNS este un sistem distribuit care mapează nume precum:

```

[www.example.com](http://www.example.com) → 93.184.216.34

```

Câteva tipuri de înregistrări importante:

| Tip | Descriere |
|-----|-----------|
| **A** | Nume → IPv4 |
| **AAAA** | Nume → IPv6 |
| **CNAME** | Alias către un alt nume |
| **MX** | Mail exchange server |
| **NS** | Nameserver pentru o zonă |

În tool‐uri obișnuite:

- **nslookup** – simplu, interactiv  
- **dig** – detaliat, recomandat

Exemple:

```

dig example.com
dig A example.com
dig @8.8.8.8 example.com

```

DNS funcționează prin UDP (port 53), uneori TCP (mesaje mari).

---

### 2. Recapitulare SSH

SSH este un protocol securizat pentru:

- conectare remote
- execuție comenzi
- transfer fișiere (scurt) via SFTP
- tunelare trafic (port forwarding)

Conexiune simplă:

```

ssh user@host

```

Comandă remote:

```

ssh user@host "uname -a"

```

Tunelare locală (conceptual):

```

ssh -L local_port:dest_host:dest_port user@host

```

Vom folosi aceste concepte mai târziu în containere.

---

### 3. Obiectivele seminarului

1. Rezoluție DNS în interiorul unei rețele de containere Docker  
2. Implementarea unui mini server DNS care răspunde la o singură întrebare  
3. Configurarea unui server SSH în container  
4. Script Python cu **Paramiko** pentru execuție remote și SFTP  
5. SSH port forwarding către un serviciu HTTP aflat într-un alt container

Toate exercițiile vor fi însoțite de template-uri și de sarcini concrete.

---

### 4. Instrumente necesare

- **nslookup**, **dig** – pentru testare DNS
- **ssh**, **scp** – basic
- **docker** + **docker compose**
- Python + modulele:
  - `paramiko`
  - opțional: `dnslib` pentru mini DNS

