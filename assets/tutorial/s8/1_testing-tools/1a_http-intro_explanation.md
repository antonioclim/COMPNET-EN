### Introducere în HTTP și unelte de testare (curl)

În această etapă vom face o scurtă recapitulare a protocolului HTTP și vom folosi
un instrument extrem de important pentru testarea serviciilor web: **curl**.

Scopul este ca studenții să înțeleagă cum arată un request HTTP real, ce înseamnă
status code-urile, antetele și cum se comportă un client care NU este browserul
(clienții reali din producție folosesc adesea curl/wget/biblioteci HTTP).

---

### 1. Ce este HTTP?

HTTP (HyperText Transfer Protocol) este un protocol text-based, request–response.
Comunicarea are loc între:

- **Client** (browser, curl, aplicație mobilă, script)
- **Server** (Apache, nginx, Flask, Django, server custom etc.)

Structura de bază:

#### Request:

```

GET /index.html HTTP/1.1
Host: example.com
User-Agent: curl/8.0
Accept: */*

(optional body)

```

#### Response:

```

HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 1256

<html>...</html>
```

Componente importante:

* **Linia de start** (ex.: `GET / HTTP/1.1`)
* **Antete** (headers)
* **Body** (opțional, în funcție de metodă)

---

### 2. De ce curl?

`curl` este cel mai simplu și complet instrument pentru:

* testare rapidă a unui endpoint
* vizualizarea request/response brut
* testare API-uri REST
* simularea diferitelor metode (GET, POST, PUT, DELETE)
* debugging

---

### 3. Comenzi curl esențiale

#### GET normal:

```
curl http://example.com
```

#### Cerere cu detalii (request și response):

```
curl -v http://example.com
```

#### Doar antetele răspunsului (HEAD):

```
curl -I http://example.com
```

#### Trimitem un POST cu body:

```
curl -X POST -d "name=test&age=20" http://example.com/api
```

#### Salvăm răspunsul într-un fișier:

```
curl -o pagina.html http://example.com
```

---

### 4. Cum lucrăm în acest seminar?

1. Vom folosi `curl` pentru a testa serverele HTTP pe care le implementăm.
2. Vom inspecta în mod explicit status code-uri, antete și body.
3. Vom compara comportamentul diferitelor servere:

   * Python `http.server`
   * server HTTP cu `socket` implementat manual
   * server HTTP din nginx (în Docker)

---

### În etapa următoare

Vom porni un server HTTP minim folosind modulul `http.server` din Python,
pentru a avea un server complet funcțional înainte de a implementa manual
protocolul HTTP cu socket-uri.
