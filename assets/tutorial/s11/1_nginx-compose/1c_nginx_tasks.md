## Sarcini pentru studenți

Creați fișierul:
`stage2_nginx_output.txt`

Și includeți:

### **1. Output-ul a 5 comenzi curl**

Exemplu:

```
curl http://localhost:8080 → Hello from web1
curl http://localhost:8080 → Hello from web2
curl http://localhost:8080 → Hello from web3
curl http://localhost:8080 → Hello from web1
curl http://localhost:8080 → Hello from web2
```

### **2. Un scurt răspuns (2–3 fraze):**

Explicați, în cuvintele voastre, ce face load balancing round-robin în Nginx.

### **3. Bonus (opțional):**

Opriți un backend:

```
docker stop web2
```

Executați încă 5 comenzi curl și notați rezultatele.

În fișier scrieți ce observați:
Nginx sare peste un backend picat? Returnează erori? Cum se comportă?

