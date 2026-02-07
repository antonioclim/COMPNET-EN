### Sarcini – Server HTTP implementat manual

#### 1. Completați fișierul `socket_http_server.py`

Zonele marcate cu:

```

# >>> STUDENT TODO

```

trebuie completate:

- parsarea primei linii din request
- trimiterea răspunsului 404
- trimiterea răspunsului 200

---

#### 2. Porniți serverul

```

python3 socket_http_server.py 8000

```

Ar trebui să vedeți:

```

Server HTTP manual pornit pe portul 8000

```

---

#### 3. Testați cu curl

Executați:

```

curl -v [http://localhost:8000/](http://localhost:8000/)
curl -v [http://localhost:8000/index.html](http://localhost:8000/index.html)
curl -v [http://localhost:8000/doesnotexist](http://localhost:8000/doesnotexist)

```

Salvați rezultatele în:

```

socket_http_log.txt

```

---

#### 4. Test în browser

Accesați:

```

[http://localhost:8000/](http://localhost:8000/)

```

Descrieți în `socket_http_log.txt` dacă pagina se încarcă corect.

---

#### 5. Explicație scurtă (obligatoriu)

În același fișier, în 5–6 propoziții explicați:

- cum parsează serverul request-ul
- cum decide ce fișier să trimită
- de ce este necesar `Content-Length`
- ce se întâmplă când fișierul nu există

---

Acest server simplu este baza pentru etapa următoare: integrarea cu **nginx reverse proxy**.
