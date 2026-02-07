## Sarcini – Stage 4: LB Custom în Compose

Creați fișierul:
`stage4_lb_vs_nginx.txt`

Includeți:

---

### **1. Output-ul a 6 comenzi curl prin LB-ul custom**

Exemplu:

```
→ Hello from web1
→ Hello from web2
→ Hello from web3
...
```

---

### **2. Logurile LB-ului pentru aceleași cereri**

Copiați:

```
[INFO] ... → web1
[INFO] ... → web2
...
```

---

### **3. Test backend picat**

Opriți web2:

```
docker compose -f docker-compose.lb-custom.yml stop web2
```

Trimiteți 5 cereri la LB.
Note:

* răspunsuri
* erori
* comportament general

---

### **4. Comparație Nginx vs LB custom (maxim 6–8 fraze)**

Scrieți:

* două lucruri pe care LB custom le face bine
* două lucruri pe care LB custom le face prost
* un aspect la care Nginx este mult superior
* o idee de îmbunătățire pentru LB

---

### **5. Bonus opțional**

Faceți web3 lent (cum este descris în tutorial).
Explicați ce observați.

---

# **Concluzie Stage 4**

Acum avem:

* un reverse proxy industrial (Nginx)
* un reverse proxy educational (load balancer custom)
* comparație practică
* integrare completă în Compose


