### Protocoale de rutare
### RIP, EIGRP (context), OSPF (si idei link-state)

---

### Obiective
La finalul cursului, studentul poate:
- Explica rolul ruterului si ce este “forwarding” vs “routing”
- Explica ce contine o tabela de rutare si cum se alege “next hop”
- Diferentia rute statice vs dinamice si cand sunt utile
- Intelege diferentele distance-vector vs link-state
- Explica pe scurt RIP (hop count, timere, probleme tipice)
- Explica pe scurt OSPF (LSDB, hello, DR/BDR, SPF/Dijkstra, arii)
- Rula exemple: Bellman-Ford, Dijkstra, Mininet cu rutare statica

---

### Ce rol are un ruter?
- Un ruter conecteaza doua sau mai multe retele
- Primeste pachete si decide pe ce interfata le trimite mai departe
- Poate face si functii secundare: filtrare, NAT, QoS, tunelare (context)

[FIG] c7-assets/fig-router-role.png

---

### Routing vs forwarding
- Forwarding: decizia locala “ies pe interfata X catre next hop Y”
- Routing: cum invat/mentin informatia care alimenteaza forwarding-ul (rute statice sau protocoale)

---

### Procesul de rutare (concept)
- Ruterul mentine o tabela de rutare
- Pentru fiecare prefix cunoscut: next hop, interfata, metrica, sursa (static/dinamic)
- Rutele direct conectate apar automat

---

### Tipuri de rute
- Statice (manual):
  - control precis
  - simple, bune pentru stub networks
  - nu sunt scalabile
- Dinamice (prin protocoale):
  - scalabile
  - se adapteaza la defecte (in functie de protocol)

---

### Metrici de rutare
- hop count (simplu)
- latency, bandwidth, reliability, load, cost administrativ (in functie de protocol)
- pot exista rute multiple cu aceeasi metrica (ECMP)

---

### Ce se modifica pe traseu (L2 vs L3)
- IP sursa/destinatie raman aceleasi
- MAC sursa/destinatie se schimba la fiecare hop
- TTL/Hop Limit scade la fiecare hop

[FIG] c7-assets/fig-l2-l3-changes.png

---

### Tabela de rutare
- exista si pe host-uri, nu doar pe rutere
- se tine in RAM
- contine:
  - direct connected
  - rute statice
  - rute dinamice
  - ruta implicita (default)

[FIG] c7-assets/fig-routing-table.png

---

### Clasificarea retelelor din perspectiva ruterului
- conectate (direct connected)
- cunoscute (statice/dinamice)
- necunoscute (default sau drop)

---

### Rutare asimetrica
- fiecare ruter decide local
- nu exista garantie ca drumul dus este identic cu drumul intors

---

### IGP vs EGP
- IGP: in interiorul unui sistem autonom (RIP, OSPF, EIGRP, IS-IS)
- EGP: intre sisteme autonome (BGP) (doar mentiune aici)

---

### Distance-vector (idea)
- ruterul nu stie topologia completa
- stie “distanta” catre retele + next hop
- update-uri periodice (clasic) sau incrementale (depinde de protocol)
- algoritm asociat: Bellman-Ford (conceptual)

[FIG] c7-assets/fig-distance-vector.png

[SCENARIO] c7-assets/scenario-bellman-ford/

---

### RIP (Routing Information Protocol)
- metrica: hop count
- hop count maxim: 15 (16 = infinit)
- ruleaza peste UDP 520
- RIPv1: fara masca (fara CIDR/VLSM)
- RIPv2: include masca, multicast 224.0.0.9, poate avea autentificare
- RIPng: pentru IPv6

---

### Problema RIP: routing loops si count-to-infinity
- in anumite defecte, rutele “cresc” pana la infinit
- mecanisme clasice:
  - split horizon
  - route poisoning
  - holddown
  - timeout/flush

[FIG] c7-assets/fig-rip-loop.png

---

### Timere RIP (concept)
- update timer
- invalid timer
- flush timer
- holddown timer

---

### Link-state (idea)
- fiecare ruter construieste o baza de date cu topologia (LSDB)
- calculeaza local rutele optime (SPF)
- algoritm asociat: Dijkstra (conceptual)

[FIG] c7-assets/fig-link-state.png

[SCENARIO] c7-assets/scenario-dijkstra/

---

### OSPF (Open Shortest Path First)
- link-state IGP
- foloseste mesaje de tip hello si LSAs (concept)
- foloseste multicast (in functie de tipul de retea)
- imparte reteaua in arii; exista backbone (Area 0)

[FIG] c7-assets/fig-ospf-areas.png

---

### OSPF: functionare (pe scurt)
- hello: descoperire vecini si mentinere adjacency
- sincronizare LSDB intre vecini
- alegere DR/BDR pe segmente multi-access
- calcul rute: SPF (Dijkstra) pe baza LSDB

---

### Unde intra Mininet in curs
- folosim o topologie simpla cu 3 rutere
- punem adrese si rute statice
- inspectam tabelele de rutare si verificam conectivitatea

[SCENARIO] c7-assets/scenario-mininet-routing/

---

### Recapitulare
- rutele statice sunt bune pentru stub si topologii simple
- RIP: simplu, hop count, limitari si probleme de convergenta
- OSPF: link-state, scalabil, SPF, arii
- BGP: alt context (inter-AS), amanat pentru nivel aplicatie/operare Internet (optional)
