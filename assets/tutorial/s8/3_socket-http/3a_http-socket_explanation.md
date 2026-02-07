### Server HTTP minimal implementat manual cu socket-uri

În această etapă vom implementa un server HTTP *de la zero*, folosind doar:

- `socket.socket`
- `bind`, `listen`, `accept`
- citirea request-urilor din rețea
- trimiterea unui răspuns HTTP valid

Scopul nu este să implementăm standardul complet HTTP, ci să înțelegem:

1. cum arată REAL un request HTTP
2. de ce este nevoie de `Content-Length`
3. de ce trebuie trimisă linia de status
4. cum se servește un fișier static

---

### Structura unui request HTTP real

Clientul trimite cel puțin:

```

GET /index.html HTTP/1.1
Host: localhost:8000
User-Agent: curl/8.0
Accept: */*

(optional body)

```

Noi vom folosi DOAR prima linie. Restul headerelor sunt ignorate în acest stadiu.

---

### Structura minimă a unui răspuns HTTP

```

HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 42

<content aici>
```

Dacă `Content-Length` este greșit, browserul:

* fie nu afișează pagina
* fie „așteaptă” restul datelor
* fie închide conexiunea prematur

**Deci: Content-Length este obligatoriu.**

---

### Ce implementăm în acest stage

1. Server TCP care ascultă pe port (ex.: 8000)
2. Primește conexiuni de la clienți (curl / browser)
3. Citește request-ul (cel puțin prima linie)
4. Parsează metoda și path-ul
5. Servește fișierul din directorul `static/`
6. Dacă fișierul nu există → trimite `404 Not Found`

---

### Avantaj

După acest stage, studenții înțeleg clar:

* diferența dintre un server „adevărat” și `http.server`
* ce înseamnă „parsing HTTP”
* cum se formează pachetele HTTP

Apoi, în Stage 4 vom pune acest backend în spatele nginx ca reverse proxy.

