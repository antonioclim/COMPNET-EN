### Seminar 10 – DNS în containere Docker + Mini server DNS custom

În această secțiune vom lucra cu două concepte importante:

1. **DNS intern în Docker Compose** – Docker oferă deja un server DNS care permite containerelor să se rezolve între ele folosind numele serviciului.
2. **Un server DNS minimal, scris în Python**, care răspunde doar unei singure interogări (pentru a înțelege mecanismul).

---

## 1. DNS implicit în Docker

Atunci când folosiți un `docker-compose.yml`, fiecare serviciu primește automat:

- un nume DNS = numele serviciului
- o adresă IP internă
- acces la un DNS integrat care rezolvă aceste nume

Exemplu:

```yaml
services:
  web:
    image: python:3
  db:
    image: redis
  debug:
    image: busybox
````

Din containerul `debug`:

```
ping web
ping db
nslookup web
```

Docker va rezolva automat numele `web` către IP-ul intern al containerului `web`.

---

## 2. Mini server DNS custom (concept)

Vom crea:

* un container `dns-server`
* un script Python care ascultă pe UDP 5353
* o regulă simplă:
  **dacă cineva întreabă de `myservice.lab.local`, serverul răspunde cu o adresă IP fixă**

Acesta nu este un server DNS complet.
Este o versiune extrem de simplificată pentru a înțelege:

* recepția unui mesaj DNS
* decodarea minimă a header-ului
* returnarea unui răspuns standard

Vom folosi biblioteca **dnslib**, care face codarea/decodarea mult mai simplă.

---

## 3. Ce veți testa

În interiorul containerului `debug`:

1. Rezolvați numele serviciilor Docker:

```
dig web
dig db
```

2. Rezolvați numele gestionate de DNS-ul vostru custom:

```
dig @dns-server myservice.lab.local
```

3. Comparați outputul între DNS implicit și mini DNS-ul Python.

---

## 4. Structura fișierelor în această secțiune

* `docker-compose.yml`
* `dns_server.py`
* `index_seminar10_dns_containers_tasks.md` (sarcinile)

---

După ce înțelegeți această parte, vom trece la **SSH cu Paramiko** în containere.

````

---

# 2. `index_seminar10_dns_containers_tasks.md` (sarcini)

```markdown
### Sarcini – DNS în containere + mini server DNS custom

---

## 1. Porniți infrastructura Docker

````

docker compose up --build

```

Așteptați ca serviciile `web`, `debug`, `dns-server` să pornească.

---

## 2. Testare DNS implicit

Intrați în containerul debug:

```

docker compose exec debug sh

```

Rulați:

```

ping web
ping db
dig web
dig db

```

Salvați rezultatul în:

```

seminar10_dns_builtin_output.txt

```

---

## 3. Testare DNS custom

Tot în containerul `debug`:

```

dig @dns-server myservice.lab.local
dig @dns-server doesnotexist.local

```

Salvați rezultatul în:

```

seminar10_dns_custom_output.txt

```

---

## 4. Comparație finală

Explicați în `seminar10_dns_comparison.txt`:

- care este diferența între DNS implicit în Docker și DNS custom
- care este avantajul unui server DNS „real” față de implementarea simplificată
- de ce se folosește deseori `dnslib` pentru prototipuri DNS

