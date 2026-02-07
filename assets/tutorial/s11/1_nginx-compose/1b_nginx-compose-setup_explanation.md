## Stage 2 – Configurarea unei Arhitecturi cu 3 Backend-uri + Nginx Reverse Proxy (Docker Compose)

### **Obiective**

În această etapă vom construi un mediu complet funcțional folosind Docker Compose:

* trei servere backend simple, fiecare rulând `python -m http.server 8000`
* un container Nginx configurat ca reverse proxy + load balancer
* verificare folosind `curl` ca load balancing-ul funcționează (round robin)
* pregătirea mediului pentru etapa următoare (înlocuirea Nginx cu LB-ul custom)

---

## **1. Structura arhitecturii**

Vom avea următoarele containere:

```
nginx (reverse proxy)
 ├── web1:8000
 ├── web2:8000
 └── web3:8000
```

Clienții vor accesa sistemul prin:

```
http://localhost:8080
```

## **3. Pornirea arhitecturii**

În terminal:

```
docker compose -f docker-compose.nginx.yml up --build
```

Apoi într-un alt terminal testați:

```
curl http://localhost:8080
curl http://localhost:8080
curl http://localhost:8080
curl http://localhost:8080
```

Ar trebui să vedeți:

```
<h1>Hello from web1</h1>
<h1>Hello from web2</h1>
<h1>Hello from web3</h1>
<h1>Hello from web1</h1>
...
```

---

## **4. Observație importantă**

Backend-urile **nu sunt vizibile din exterior** (nu au porturi mapate pe host).
Doar Nginx este expus către localhost.

Acesta este un comportament tipic într-o arhitectură cu reverse proxy.

---

## **5. Ce urmează?**

În **Stage 3**, vom înlocui Nginx cu un load balancer scris în Python care:

* ascultă conexiuni HTTP
* preia request-uri
* le forward-ează către backend-uri
* implementează algoritmul round-robin

Vom compara apoi comportamentul cu Nginx.

