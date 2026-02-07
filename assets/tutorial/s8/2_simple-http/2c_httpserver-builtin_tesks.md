### Sarcini – Server HTTP Python (http.server)

#### 1. Porniți serverul

Rulați:

```

python3 simple_http_builtin.py 8000

```

Apoi testați cu:

```

curl -v [http://localhost:8000/](http://localhost:8000/)
curl -v [http://localhost:8000/hello](http://localhost:8000/hello)
curl -v [http://localhost:8000/api/time](http://localhost:8000/api/time)

```

Salvați rezultatele într-un fișier:

```

builtin_http_log.txt

```

---

#### 2. Adăugați un endpoint nou

În fișierul **simple_http_builtin.py**, modificați clasa `MyHandler` astfel
încât să existe un nou endpoint:

```

/student

````

care să întoarcă JSON cu structura:

```json
{
  "name": "<numele vostru>",
  "lab": 8
}
````

---

#### 3. Testați endpoint-ul nou

Folosiți:

```
curl -v http://localhost:8000/student
```

Adăugați rezultatul în `builtin_http_log.txt`.

---

#### 4. Observați antetele

În același fișier, răspundeți la următoarele întrebări (2–3 propoziții fiecare):

1. Ce antet generează automat `SimpleHTTPRequestHandler` pentru fișiere statice?
2. Ce diferențe există între antetele generate de `/hello` și cele generate de `/api/time`?
3. De ce este important să trimitem corect `Content-Type` și `Content-Length`?

---

După acest stage, sunteți pregătiți pentru **implementarea unui server HTTP manual cu socket-uri**, unde vom construi răspunsurile HTTP de la zero.
