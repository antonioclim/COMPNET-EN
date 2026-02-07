### Sarcini – Filtru de pachete TCP/UDP (Stage 3)

In acest stage veti adapta sniffer-ul pentru a afisa DOAR pachetele de interes,
prin implementarea functiei `passes_filter` din `packet_filter.py`.

---

### 1. Copiati implementarea parse_ipv4_header

Daca `packet_filter.py` nu are deja o versiune completa a functiei:

```python
def parse_ipv4_header(data: bytes):
    ...
````

atunci copiati implementarea corecta pe care ati scris-o in `packet_sniffer.py`.

Asigurati-va ca:

* intoarce `(src_ip_str, dst_ip_str, proto, ihl)`
* foloseste `struct.unpack('! 8x B B 2x 4s 4s', data[:20])`

---

### 2. Implementati filtrul – Pasul 1 (numai TCP)

In `passes_filter`, implementati mai intai o regula simpla:

* afisati DOAR pachetele TCP (proto == 6)
* ignorati toate celelalte pachete

Pseudo-cod:

```python
if proto == 6:
    return True
else:
    return False
```

Rulati:

```bash
sudo python3 packet_filter.py <INTERFATA>
```

Generati trafic (ex: `curl`, `ssh`, `nc`, etc.) si verificati ca vedeti doar linii cu `proto=TCP`.

---

### 3. Implementati filtrul – Pasul 2 (UDP port 53)

Extindeti filtrul astfel incat sa aveti urmatoarea logica:

1. Daca pachetul este UDP si `dst_port == 53`, afisati-l (DNS).
2. Daca pachetul este TCP, afisati-l doar daca `dst_port > 1024`.
3. Restul pachetelor sunt ignorate.

Sugestie:

```python
# Pachet UDP catre portul 53
if proto == 17 and dst_port == 53:
    return True

# Pachet TCP catre port ne-privilegiat
if proto == 6 and dst_port is not None and dst_port > 1024:
    return True

return False
```

Rulati din nou scriptul si:

* faceti un `dig google.com` sau `nslookup` (pentru a genera trafic DNS)
* faceti un `curl http://example.com` (trafic TCP catre port 80, care va fi filtrat sau nu in functie de regula)
* observati care pachete trec filtrul

---

### 4. Implementati filtrul – Pasul 3 (filtru pe sursa IP)

Adaugati un criteriu suplimentar:

* afisati DOAR pachetele (care deja trec de regulile de mai sus) si au adresa sursa intr-o retea specifica.
* de exemplu, doar adrese sursa din `10.x.x.x` (string-ul sursa incepe cu `"10."`)

Pseudo-cod:

```python
if not src_ip.startswith("10."):
    return False
```

In final, filtrul vostru poate arata ca o combinatie:

```python
# doar surse din 10.0.0.0/8
if not src_ip.startswith("10."):
    return False

# UDP catre 53
if proto == 17 and dst_port == 53:
    return True

# TCP catre port > 1024
if proto == 6 and dst_port is not None and dst_port > 1024:
    return True

return False
```

Adaptati la mediul vostru (puteti folosi `192.168.` sau alte prefixe relevante).

---

### 5. Rulati si colectati rezultate

Rulati:

```bash
sudo python3 packet_filter.py <INTERFATA>
```

In timp ce filtrul ruleaza:

* generati trafic DNS (dig / nslookup)
* generati trafic HTTP (curl)
* generati trafic SSH sau alt TCP (daca este relevant)
* asigurati-va ca filtrul chiar elimina pachetele nedorite

Copiati output-ul relevant (cel putin 20 de linii) intr-un fisier:

```text
filter_results.txt
```

---

### 6. Intrebari de reflectie (de scris in filter_results.txt)

Sub log, raspundeti la:

1. Ce tip de trafic ati reusit sa filtrati cel mai usor (TCP/UDP)?
2. De ce filtrarea pe port destinatie poate fi inselatoare in practică (hint: port reuse, tunneling, servicii non-standard)?
3. Ce ati schimba in filtrul vostru daca ati fi interesati doar de detectarea traficului DNS catre un singur server (de exemplu 8.8.8.8)?

---

### Deliverable Stage 3

Predati:

* `packet_filter.py` complet (cu `passes_filter` implementata)
* `filter_results.txt` cu:

  * minimum 20 de linii de output ale filtrului
  * raspunsurile la intrebarile de reflexie
