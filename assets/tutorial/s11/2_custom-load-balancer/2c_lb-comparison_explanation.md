## Stage 4 – Integrarea Load Balancer-ului Custom în Docker Compose & Compararea cu Nginx

### **Obiective**

În această etapă:

* înlocuim Nginx cu load balancer-ul custom scris în Stage 3
* îl rulăm în Docker Compose alături de `web1`, `web2`, `web3`
* testăm comportamentul în scenarii controlate
* comparăm direct cu Nginx:

  * distribuția cererilor
  * comportamentul la backend picat
  * latență / blocaje
  * robustete

Acesta este un exercițiu foarte important:
**cum se comportă teoria la nivel industrial față de un prototip didactic.**

---

## **1. Ce modificăm în Compose?**

În Stage 2, arhitectura era:

```
client → nginx → web1/web2/web3
```

Acum devine:

```
client → lb-custom → web1/web2/web3
```

Diferența majoră:

* Nginx este înlocuit cu un container care rulează `simple_lb.py`.
* LB custom nu va avea toate optimizările Nginx → EXACT asta trebuie observat.


---

## **4. Pornirea arhitecturii**

În terminal:

```
docker compose -f docker-compose.lb-custom.yml up --build
```

Apoi:

```
curl http://localhost:8080
curl http://localhost:8080
curl http://localhost:8080
```

Veți observa:

* răspunsuri corecte, dar latență mai mare
* logurile LB-ului:

```
[INFO] ('172.18.0.1', 49566) → web1:8000
[INFO] ('172.18.0.1', 49570) → web2:8000
[INFO] ('172.18.0.1', 49574) → web3:8000
```

---

## **5. Test: ce se întâmplă dacă un backend pică?**

Opriți web2:

```
docker compose -f docker-compose.lb-custom.yml stop web2
```

Apoi trimiteți cereri:

```
curl http://localhost:8080
curl http://localhost:8080
```

Rezultat așteptat:

* LB custom **va încerca în continuare să trimită cereri către web2**
* va afișa erori în consolă
* request-ul va eșua

Aici vedem prima diferență majoră față de Nginx:

> **Nginx ocolește automat backend-urile nefuncționale**
> Load balancer-ul nostru — NU.

---

## **6. Test: backend lent**

Faceți web3 lent (editare rapidă):

În `web3/index.html`, adăugați un script Python în Compose:

Schimbăm comanda web3:

```yaml
command: ["python3", "-u", "-c", "import time, http.server; time.sleep(5); http.server.test(port=8000)"]
```

Reporniți doar web3:

```
docker compose restart web3
```

Ce se întâmplă?

* LB custom **va bloca firul** pentru acel request timp de 5 secunde
* Nginx ar fi gestionat asta mai elegant
* este o lecție importantă despre non-blocking I/O și event loops

---

## **7. Concluzii**

Diferențele principale observate:

| Funcționalitate             |    Nginx    |      LB Custom     |
| --------------------------- | :---------: | :----------------: |
| Round-robin load balancing  |      ✔      |          ✔         |
| Header rewriting            |      ✔      |          ❌         |
| Health checks               |      ✔      |          ❌         |
| Retry logic                 |      ✔      |          ❌         |
| Handling backend failure    |      ✔      |          ❌         |
| Parallel request processing |      ✔      | semi-✔ (threading) |
| Performanță                 | foarte bună |        slabă       |
| Configurabilitate           |     mare    |       minimă       |

Acesta este EXACT scopul seminarului.
