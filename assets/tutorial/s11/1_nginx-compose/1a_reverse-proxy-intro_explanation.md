## Introducere: Reverse Proxy și Load Balancing în Arhitecturi Distribuite

### **Obiectivele acestui stagiu**

La finalul acestei secțiuni, studenții vor înțelege:

* ce este un reverse proxy și cum diferă de un forward proxy
* de ce este folosit Nginx ca reverse proxy în arhitecturi moderne
* ce înseamnă load balancing și unde se aplică în pipeline-ul HTTP
* cum arată, conceptual, fluxul de request–response printr-un proxy
* ce rol va avea load balancer-ul custom pe care îl vom implementa ulterior

---

### **1. Ce este un Reverse Proxy?**

Un **reverse proxy** este un server aflat între client și un set de servere backend.
El primește request-urile de la clienți și le redirecționează către unul sau mai multe servicii interne.

```
Client → Reverse Proxy → Backend 1
                       ↘ Backend 2
                       ↘ Backend 3
```

Spre deosebire de un **forward proxy**, care reprezintă clientul în exterior,
un **reverse proxy reprezintă serviciile backend**.

---

### **2. De ce folosim Nginx ca reverse proxy?**

Nginx este folosit în majoritatea aplicațiilor moderne pentru că oferă:

* **terminare TLS (HTTPS)**
* **load balancing** (round robin, least_conn etc.)
* **buffering și caching**
* **optimizări de performanță HTTP/1.1 și HTTP/2**
* **gestionarea eficientă a conexiunilor concurente**
* **izolare a backend-urilor** (expunem doar proxy-ul, nu serviciile interne)

Acest seminar pornește cu Nginx ca exemplu de „proxy industrial”,
după care vom implementa **un load balancer propriu**, mult mai simplu, dar educativ.

---

### **3. Ce este load balancing?**

Load balancing este procesul prin care încărcarea este distribuită între mai multe instanțe backend pentru:

* scalare
* disponibilitate ridicată (HA)
* performanță mai bună
* izolare a căderilor parțiale

Exemplu cu 3 backend-uri:

```
Request 1 → web1
Request 2 → web2
Request 3 → web3
Request 4 → web1
...
```

Acesta este algoritmul standard **round-robin**, folosit de majoritatea load balancer-elor.

---

### **4. Unde se află un reverse proxy în arhitectură?**

Iată o arhitectură tipică simplificată:

```
                     ┌────────────────────────────┐
                     │        Internet              │
                     └───────────────┬──────────────┘
                                     │
                              Client Browser
                                     │
                                     ▼
                          ┌───────────────────┐
                          │   Reverse Proxy   │  ← Nginx sau LB custom
                          └───────┬───────────┘
             ┌────────────────────┼────────────────────┐
             ▼                    ▼                    ▼
      ┌────────────┐      ┌────────────┐      ┌────────────┐
      │  web1:8000 │      │  web2:8000 │      │  web3:8000 │
      └────────────┘      └────────────┘      └────────────┘
```

---

### **5. Scopul seminarului 11**

Acest seminar este împărțit în două etape mari:

#### **Etapa A — Folosirea unui load balancer real (Nginx)**

* vom crea o arhitectură cu 3 backend-uri Python
* Nginx va fi configurat ca reverse proxy
* vom testa load balancing-ul folosind `curl`

#### **Etapa B — Implementarea unui load balancer custom în Python**

* vom înlocui Nginx cu un script Python (`simple_lb.py`)
* load balancing round-robin implementat manual
* vom observa diferențele față de Nginx
* vom rula ambele scenarii în Docker Compose

---

### **6. Ce urmează în Stage 2**

În etapa următoare vom:

* crea o arhitectură Docker Compose cu 3 servere web simple
* configurăm Nginx ca reverse proxy peste ele
* verificăm distribuția request-urilor
* pregătim terenul pentru load balancer-ul custom

---

### **7. Sarcina Studentului**

Creați un fișier text numit:
`reverse_proxy_intro_findings.txt`

Și răspundeți la următoarele întrebări:

1. În propriile cuvinte: **care este diferența dintre un reverse proxy și un forward proxy?**
2. De ce credeți că un reverse proxy este util pentru microservicii?
3. Desenați un mic ASCII diagram care arată un reverse proxy și 3 backend-uri.
4. Care sunt două avantaje concrete ale load balancing-ului?

Fișierul trebuie încărcat la finalul seminarului.
