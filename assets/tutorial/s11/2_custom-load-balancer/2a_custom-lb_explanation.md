## Stage 3 – Implementarea unui Load Balancer Custom în Python

### **Obiective**

În această secțiune:

* implementăm un reverse proxy HTTP extrem de simplu, scris în Python
* folosim socket-uri brute (fără librării suplimentare)
* adăugăm suport pentru *round-robin load balancing*
* conectăm load balancer-ul custom asupra celor 3 backend-uri create în Stage 2
* testăm folosind **curl**
* comparăm comportamentul cu Nginx

Acesta este un exercițiu educațional — nu reimplementăm Nginx, ci înțelegem FUNDAMENTELE.

---

## **1. Conceptul: ce face un load balancer?**

Fluxul de date într-un load balancer minimal:

```
Client → LB → (choose backend #1)
Client → LB → (choose backend #2)
Client → LB → (choose backend #3)
Client → LB → (choose backend #1)
...
```

Pașii:

1. LB acceptă o conexiune de la client.
2. Citește **cererea HTTP brută** (text).
3. Alege un backend (folosim round-robin).
4. Creează o conexiune TCP către backend.
5. Trimite cererea către backend.
6. Citește răspunsul backend-ului.
7. Îl retrimite clientului.

