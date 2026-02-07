
### Sarcini introductive – DNS și SSH

În acest fișier aveți primul set de exerciții care trebuie completate înainte de a trece la partea cu containere.

---

### 1. Testați rezoluția DNS

Rulați următoarele comenzi:

```

dig example.com
dig A example.com
dig @1.1.1.1 example.com
dig google.com

```

Salvați outputul în fișierul:

```

seminar10_intro_dns_output.txt

```

**Ce trebuie să comentați în fișier:**

- care este diferența între interogarea `dig example.com` și `dig A example.com`
- ce înseamnă câmpul **ANSWER SECTION**
- ce reprezintă **TTL**

---

### 2. Testați o sesiune SSH (dacă aveți acces la un server de laborator)

Dacă aveți un server accesibil, rulați:

```

ssh USER@HOST "uname -a"
ssh USER@HOST "ls -l /"

```

Dacă nu aveți, folosiți exemplul:

```

# (simulare)

ssh test@fakehost "uname -a"

```

și explicați **ce ați fi obținut** dacă hostul exista.

Salvați în:

```

seminar10_intro_ssh_output.txt

```

---

### 3. Pregătirea pentru partea cu containere

Asigurați-vă că:

- `docker --version` funcționează
- `docker compose version` funcționează

Faceți un screenshot/fișier text cu aceste două comenzi:

```

seminar10_docker_check.txt

```
