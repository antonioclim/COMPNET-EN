Perfect — începem cu **prima parte a seminarului**, adică:

## **STAGE 1 — Topologia de triunghi cu 3 routere + rutare statică (Mininet)**

Așa cum am făcut în seminariile anterioare, vom avea:

1. **`index_routing-triangle_explanation.md`**
2. **`index_routing-triangle_topology.py`** – cod Mininet complet, comentat
3. **`index_routing-triangle_tasks.md`** – exercițiile studentului + deliverable

Dacă e totul ok, continuăm apoi cu partea SDN.

---

# 1. `index_routing-triangle_explanation.md`

```markdown
### Introducere: Rutare pe trei routere (topologie triunghi)

În această secțiune vom folosi Mininet pentru a crea o topologie formată din trei routere Linux (noduri Mininet cu IP forwarding activat) și două hosturi. Scopul este să configurăm rute statice astfel încât h1 și h3 să poată comunica prin diferite căi ale triunghiului.

Topologia folosită:

```

```
h1
 |
r1 ----- r2
 \       /
  \     /
    r3
    |
    h3
```

```

Această structură permite analizarea:
- rutării statice pe mai multe căi
- tabelelor de rutare de pe mai multe routere
- influenței configurației asupra comenzii `traceroute`
- comutării rutei prin modificarea unui singur hop

---

### Scheme de adresare folosite

Pentru simplitate vom folosi subrețele /30, câte una pentru fiecare legătură punct-la-punct:

| Legătură        | Subnet        | r1 IP      | r2 IP      | r3 IP      | h1/h3 |
|-----------------|---------------|------------|------------|------------|-------|
| h1 ↔ r1         | 10.0.1.0/30   | 10.0.1.1   | —          | —          | 10.0.1.2 |
| r1 ↔ r2         | 10.0.12.0/30  | 10.0.12.1  | 10.0.12.2  | —          | —     |
| r2 ↔ r3         | 10.0.23.0/30  | —          | 10.0.23.1  | 10.0.23.2  | —     |
| r1 ↔ r3         | 10.0.13.0/30  | 10.0.13.1  | —          | 10.0.13.2  | —     |
| r3 ↔ h3         | 10.0.3.0/30   | —          | —          | 10.0.3.1   | 10.0.3.2 |

