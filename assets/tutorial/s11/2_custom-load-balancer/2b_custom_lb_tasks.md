## Sarcini pentru studenți – Load Balancer Custom

Creați fișierul:
`stage3_lb_custom_output.txt`
și includeți toate cerințele următoare.

---

## **1. Completați TODO-ul din simple_lb.py**

Secțiunea:

```python
# TODO: round robin selection
```

Trebuie completată corect.
Includeți în fișierul final **codul complet al funcției get_next_backend()**.

---

## **2. Rulați load balancer-ul**

În terminal:

```
python3 simple_lb.py
```

LB trebuie să se conecteze la backend-urile `web1`, `web2`, `web3` care rulează din Stage 2.

---

## **3. Testați manual cu curl**

Executați:

```
curl http://localhost:8080
curl http://localhost:8080
curl http://localhost:8080
curl http://localhost:8080
curl http://localhost:8080
```

Copiați output-ul în fișierul final.

---

## **4. Observați logurile LB-ului**

În consola LB trebuie să apară:

```
[INFO] ('127.0.0.1', 53792) → web1:8000
[INFO] ('127.0.0.1', 53794) → web2:8000
[INFO] ('127.0.0.1', 53796) → web3:8000
...
```

Includeți o captură de ecran sau copiați textul relevant în fișier.

---

## **5. Mini-raport (3–5 fraze)**

Răspundeți:

1. Ce face load balancer-ul custom similar cu Nginx?
2. Ce NU face load balancer-ul custom (dar Nginx face foarte bine)?
3. Care ar fi primul lucru pe care l-ați îmbunătăți?

---

# **Ce urmează?**

În **Stage 4**, vom integra load balancer-ul custom în Docker Compose și îl vom compara direct cu Nginx — inclusiv comportamentul în cazuri de eroare.

