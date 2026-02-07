### Sarcini — Introducere HTTP + curl

#### 1. Testați câteva site-uri publice folosind curl

Rulați următoarele comenzi și salvați rezultatele într-un fișier numit:

```

curl_basics_log.txt

```

Comenzi recomandate:

1. `curl http://example.com`
2. `curl -v http://example.com`
3. `curl -I http://example.com`

Pentru fiecare comandă, identificați în fișierul vostru:

- status code-ul (ex.: `200 OK`)
- cel puțin 3 antete HTTP (ex.: `Content-Type`, `Server`, `Date`)
- diferențele dintre request și response

---

#### 2. Testați un endpoint dynamic

Alegeți orice server care expune un endpoint API simplu (ex.: httpbin.org):

```

curl -v [http://httpbin.org/get](http://httpbin.org/get)
curl -X POST -d "x=1&y=2" [http://httpbin.org/post](http://httpbin.org/post)

```

Adăugați rezultatele în același fișier `curl_basics_log.txt`.

---

#### 3. Întrebare scurtă (de pus în raport)

Într-un fișier nou:

```

curl_questions.txt

```

Răspundeți în 2–3 propoziții:

- De ce este util să vezi request-ul complet atunci când debugezi un serviciu HTTP?
- De ce `curl` este adesea preferat browserului pentru debugging tehnic?