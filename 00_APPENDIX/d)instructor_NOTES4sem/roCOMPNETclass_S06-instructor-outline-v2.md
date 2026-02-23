# Seminar S06 — Routare statică și SDN (Software‑Defined Networking)

| | |
|---|---|
| **Curs** | Rețele de Calculatoare — COMPNET |
| **Kit / repo** | `compnet-2025-redo` (arhiva: `claudev11_EN_compnet-2025-redo-main.zip`) |
| **Infra** | **MININET‑SDN VM** (Ubuntu 24.04, VirtualBox) — Mininet 2.3 · Open vSwitch 3.3 · Os‑Ken · Python 3.12 (venv `compnet`) · `iproute2` · `traceroute` · `tcpdump` |
| **Durată țintă** | 35–40 min (demo ghidat + ancorare conceptuală). Exercițiile complete rămân ca lucru individual, cu livrabile. |
| **Ideea‑cheie** | **Clasic:** fiecare router decide local pe baza *routing table*. **SDN:** decizia e centrală (controller) și se materializează ca **flow rules** în switch (match–action). |

---

## Obiective operaționale

La finalul S06 (și după finalizarea temelor), studenții ar trebui să poată:

1. **Configura și interpreta static routing** într‑o topologie cu 3 routere Linux (triunghi), folosind `ip route`, `ping`, `traceroute`.
2. **Explica (empiric) de ce o modificare într‑un singur router schimbă traseul global**: ruta din *primul router* determină calea pentru tot fluxul.
3. **Descrie arhitectura SDN** — separarea control plane / data plane — și rolul regulii **table‑miss**.
4. **Observa în practică** cum un controller (Os‑Ken) instalează flows în OVS (`ovs-ofctl dump-flows`) pentru a **permite** sau **bloca** trafic.
5. **Produce trafic aplicație (TCP/UDP)** și lega comportamentul observat de politica din flow table (TCP blocat către h3, UDP permis după modificarea controllerului).

> Notă didactică: scopul seminarului nu este memorarea de comenzi, ci construcția unui model mental: *cine decide*, *unde se vede decizia*, *cum o verifici*.

---

## Structura seminarului

| Interval | Bloc | Ce construiești |
|---:|---|---|
| 0:00–0:03 | **A** | Hook + activare S05: „cine decide drumul?" |
| 0:03–0:15 | **B** | Triangle routing: pornești topologia, verifici IP‑uri, comutezi ruta, *vezi* schimbarea în `traceroute` |
| 0:15–0:18 | **C** | Tranziție: de la „decizie distribuită" la „decizie centrală" (SDN) |
| 0:18–0:30 | **D** | SDN Stage 2: controller Os‑Ken + topologie OVS, ping permis/blocat, inspectezi flow table |
| 0:30–0:38 | **E** | SDN Stage 3: trafic TCP permis (h1↔h2), TCP blocat (h1→h3); dacă ai ritm — modificare controller: UDP permis |
| 0:38–0:40 | **F** | Recap (revenire la hook) + livrabile |

> **Dacă rămâi fără timp:** Stage 3 (modificarea controllerului) devine temă. În clasă ancorezi ideea arătând blocul de cod și modul de validare cu `dump-flows`.

---

## Fișierele din kit folosite (S06)

> Directorul de lucru: `04_SEMINARS/S06/`

### Stage 1 — Routare statică (triangle)
- `1_routing/S06_Part01A_Explanation_Routing_Triangle.md` — schema de adresare, concepte (pentru referința instructorului)
- `1_routing/S06_Part01B_Script_Routing_Triangle_Topology.py` — topologie Mininet
- `1_routing/S06_Part01C_Tasks_Routing_Triangle.md` — exerciții + livrabil

### Stage 2 — SDN (OpenFlow switch + controller Os‑Ken)
- `2_sdn/S06_Part02A_Explanation_SDN.md` — concepte SDN, topologie, politică dorită
- `2_sdn/S06_Part02B_Script_SDN_Topo_Switch.py` — topologie Mininet cu OVS
- `2_sdn/S06_Part02C_Script_SDNOS_Ken_Controller.py` — controller Os‑Ken (OpenFlow 1.3)
- `2_sdn/S06_Part02D_Tasks_SDN.md` — exerciții + livrabil parțial

### Stage 3 — Trafic aplicație prin SDN (TCP/UDP)
- `3_sdn-app-traffic/S06_Part03A_Explanation_SDN_App_Traffic.md` — concepte, porturi, obiective
- `3_sdn-app-traffic/S06_Part03_Script_TCP_Server.py` — echo server TCP (port argument)
- `3_sdn-app-traffic/S06_Part03_Script_TCP_Client.py` — echo client TCP
- `3_sdn-app-traffic/S06_Part03_Script_UDP_Server.py` — echo server UDP (port argument)
- `3_sdn-app-traffic/S06_Part03_Script_UDP_Client.py` — echo client UDP
- `3_sdn-app-traffic/S06_Part03B_Tasks_SDN_App_Traffic.md` — exerciții + livrabil final

### Materiale suport HTML (pentru studiu individual)
- `_HTMLsupport/S06/1_routing/S06_Part01_Page_Routing_Triangle.html`
- `_HTMLsupport/S06/2_sdn/S06_Part02_Page_2_ab_SDN_Topo_Switch.html`
- `_HTMLsupport/S06/2_sdn/S06_Part02_Page_2_cd_SDNOS_Ken_Controller.html`
- `_HTMLsupport/S06/3_sdn-app-traffic/S06_Part03_Page_SDN_App_Traffic.html`

> **Discrepanță de denumiri:** Fișierul de tasks (`S06_Part02D`) folosește `index_*` ca prefixe. Scripturile au prefix `S06_...`. Pentru a evita confuzia în clasă, fie creezi copii:
> ```bash
> cd 04_SEMINARS/S06
> cp 1_routing/S06_Part01B_Script_Routing_Triangle_Topology.py  1_routing/index_routing-triangle_topology.py
> cp 2_sdn/S06_Part02B_Script_SDN_Topo_Switch.py               2_sdn/index_sdn_topo_switch.py
> cp 2_sdn/S06_Part02C_Script_SDNOS_Ken_Controller.py          2_sdn/index_sdn_os-ken_controller.py
> ```
> fie folosești în mod consecvent numele din kit (`S06_...`).

---

## Checklist înainte de oră

1. **3 terminale SSH deschise** în VM:
   - 🔵 T1: Stage 1 (triangle)
   - 🟢 T2: controller Os‑Ken (Stage 2–3)
   - 🟠 T3: Mininet SDN (Stage 2–3)
2. Verifici uneltele:
   ```bash
   python3 --version       # 3.12.x
   mn --version            # 2.3.x
   ovs-vsctl --version     # 3.3.x
   osken-manager --version 2>/dev/null || echo "verifică: python3 -m os_ken.cmd.manager --version"
   traceroute --version 2>/dev/null || true
   tcpdump --version 2>/dev/null || true
   ```
3. Curățare instanțe rămase:
   ```bash
   sudo mn -c
   sudo pkill -f osken-manager || true
   ```

---

## Bloc A (0:00–0:03) — Hook: „Drumul nu e al pachetului, ci al deciziei"

### Ce spui

> *▸ „La S05 am construit o topologie simplă — h1–r1–h2 — și am configurat rute manual. Astăzi complicăm: avem 3 routere în triunghi, deci două drumuri posibile. Întrebarea mea: dacă schimb o singură intrare în tabelul de rutare al unui singur router, se poate schimba traseul complet de la h1 la h3?"*

Pauză. Votează cu mâna: cine zice DA, cine zice NU, cine nu e sigur.

> *▸ „Rețineți ce ați ales — revenim la final. Și o a doua întrebare, pe care o lăsăm deschisă: dacă un nod central decide **ce trafic trece și ce nu**, mai avem nevoie de tabele de rutare în fiecare dispozitiv?"*

### De ce funcționează
Întrebarea 1 este verificabilă empiric (Bloc B). Întrebarea 2 creează tensiune pentru tranziția către SDN (Bloc C). Ambele se reiau la recap (Bloc F).

---

## Bloc B (0:03–0:15) — Stage 1: Triangle routing + „epifania traceroute"

### B0. Pornirea topologiei (1 min)

**🔵 T1:**
```bash
cd 04_SEMINARS/S06/1_routing
sudo python3 S06_Part01B_Script_Routing_Triangle_Topology.py
```

> *▸ „Scriptul creează r1, r2, r3 — noduri Linux cu `ip_forward=1` — plus h1 și h3. Configurează adrese /30 pe fiecare legătură și setează o conectivitate inițială: h1 și h3 au default route, iar r1 și r3 au o rută directă între ele."*

Topologia (de desenat pe tablă sau proiectat):
```
h1 (10.0.1.2)
 |
r1 ——— r2
 \     /
  \   /
   r3
    |
h3 (10.0.3.2)
```

### B1. Verificare IP‑uri (2 min)

**În `mininet>`:**
```text
r1 ip a
r2 ip a
r3 ip a
h1 ip a
h3 ip a
```

> *▸ „Nu citiți tot output‑ul. Căutați două lucruri: (1) fiecare legătură are /30 corect alocat, (2) h1 e 10.0.1.2 și h3 e 10.0.3.2."*

### B2. Traseul actual — ping + traceroute (3 min)

**POE 1 — Predicție:** > *▸ „Înainte să rulez, spuneți‑mi: câte hop‑uri va arăta `traceroute` de la h1 la h3?"*

(Răspunsul corect: 2 hop‑uri dacă ruta trece prin r1→r3 direct, 3 dacă ar trece prin r2.)

**Observație:**
```text
h1 ping -c 2 10.0.3.2
h1 traceroute -n 10.0.3.2
```

**Explicație:**
> *▸ „`ping` spune doar **că** ajunge. `traceroute` spune **pe unde**. Observați: r1 → r3 direct, deci 2 hop‑uri. Scriptul setează ruta `r1 → 10.0.3.0/30 via 10.0.13.2` (legătura directă r1–r3)."*

> *▸ Observație `-n`: evită rezolvări DNS (Domain Name System) și face output‑ul mai curat.*

### B3. Comutarea rutei: forțăm drumul prin r2 (5–6 min)

Aici construiești conflictul cognitiv: „o singură modificare, efect global".

**Pas 1 — r2 trebuie să știe cum ajunge la h3 și cum se întoarce la h1:**
```text
r2 ip route add 10.0.3.0/30 via 10.0.23.2
r2 ip route add 10.0.1.0/30 via 10.0.12.1
```

> *▸ „Dacă vreau ca r1 să trimită prin r2, atunci r2 trebuie să știe cum duce pachetul mai departe la r3 **și** cum trimite răspunsul înapoi la h1. Fără rute pe ambele direcții, traficul se oprește la r2."*

**Pas 2 — comutezi ruta din r1:**
```text
r1 ip route del 10.0.3.0/30
r1 ip route add 10.0.3.0/30 via 10.0.12.2
```

**Pas 3 — verifici:**
```text
h1 ping -c 2 10.0.3.2
h1 traceroute -n 10.0.3.2
```

**Epifanie 1:**
> *▸ „Am schimbat o singură intrare în r1, iar traseul s‑a schimbat: acum e r1 → r2 → r3, deci 3 hop‑uri. Routerele nu ghicesc — urmează tabelele. Cine a zis DA la hook avea dreptate."*

> Observație fină (20 secunde, dacă ai timp): drumul de întoarcere poate fi diferit (asymmetric routing) — r3 are rută directă către r1, deci reply‑urile pot veni pe altă cale. Nu e greșeală; e un rezultat normal al rutelor statice.

---

## Bloc C (0:15–0:18) — Tranziție: de la tabele distribuite la controller central

> *▸ „Până acum, planul de control este distribuit: fiecare router are propriul tabel. Dacă am avea 50 de routere, ar trebui să configurez rute în fiecare — sau să folosesc un protocol dinamic (OSPF, BGP) care face asta automat."*

> *▸ „SDN — Software‑Defined Networking — propune altceva: separăm complet **cine decide** (controller) de **cine execută** (switch). Switch‑ul nu decide nimic inteligent; el execută reguli match–action din flow table. Controllerul le instalează prin protocolul OpenFlow."*

> *▸ „Acum refacem un scenariu simplu: h1, h2, h3 conectate la un switch s1. Un controller Os‑Ken impune politica: h1↔h2 permis, trafic către h3 blocat. Scopul: să vedem **decizia** în flow table, nu doar efectul în ping."*

**POE 2 (pregătire):** > *▸ „Predicție: dacă controllerul blochează traficul către h3, unde se vede blocajul? În outputul de ping (timeout), în flow table (regulă cu acțiuni goale), sau în amândouă?"*

---

## Bloc D (0:18–0:30) — Stage 2: SDN (Os‑Ken + OVS)

### D0. Pornirea controllerului (2 min)

**🟢 T2:**
```bash
cd 04_SEMINARS/S06/2_sdn
osken-manager S06_Part02C_Script_SDNOS_Ken_Controller.py
```

> *▸ „Controllerul este o aplicație Python care vorbește OpenFlow 1.3 (specificația ONF TS‑025). Logurile sunt utile: ne arată evenimentele `packet_in` și decizia luată (permit/drop)."*

> Dacă `osken-manager` nu există: `python3 -m os_ken.cmd.manager S06_Part02C_Script_SDNOS_Ken_Controller.py`. Folosești ce e instalat în VM.

### D1. Pornirea topologiei SDN (2 min)

**🟠 T3:**
```bash
cd 04_SEMINARS/S06/2_sdn
sudo python3 S06_Part02B_Script_SDN_Topo_Switch.py
```

> *▸ „Un singur switch OVS (s1), 3 hosturi: h1 = 10.0.10.1, h2 = 10.0.10.2, h3 = 10.0.10.3, toate pe 10.0.10.0/24. Switch‑ul este data plane pur: înainte să aibă reguli, trimite pachetele necunoscute la controller (table‑miss)."*

> Dacă suspectezi negociere de versiune OpenFlow:
> ```text
> mininet> s1 ovs-vsctl set bridge s1 protocols=OpenFlow13
> ```

### D2. Test: permis vs blocat (3 min)

**În `mininet>` (🟠 T3):**
```text
h1 ping -c 3 10.0.10.2
h1 ping -c 3 10.0.10.3
```

**Observație în 🟢 T2 (loguri controller):** primele pachete generează `PacketIn`. Pentru h1→h2 apar mesaje „Permitted", pentru h1→h3 apare „Blocking traffic towards 10.0.10.3".

> *▸ „h1→h2 merge: controllerul instalează flows bidirecționale. h1→h3 nu merge: controllerul instalează un drop flow. Observați: decizia se ia o singură dată (la primul pachet), apoi switch‑ul execută singur."*

### D3. „Unde se vede decizia?" — dump flow table (5 min)

```text
mininet> s1 ovs-ofctl dump-flows s1
```
(dacă e nevoie: `s1 ovs-ofctl -O OpenFlow13 dump-flows s1`)

> *▸ „Citim împreună trei lucruri:"*

| Ce cauți | Match | Actions | Ce înseamnă |
|---|---|---|---|
| **Table‑miss** (priority=0) | `*` (orice) | `OUTPUT:CONTROLLER` | Pachet necunoscut → controller (slow path) |
| **Flow permis** (h1↔h2) | `ipv4_src=10.0.10.1, ipv4_dst=10.0.10.2` | `OUTPUT:2` | Trafic h1→h2 livrat pe portul 2 |
| **Flow drop** (→h3) | `ipv4_dst=10.0.10.3` | (gol) | Trafic către h3 distrus silențios |

**Epifanie 2:**
> *▸ „După ce flow‑ul este instalat, următoarele pachete identice nu mai ajung la controller — sunt procesate local de switch. E tranziția de la decizie centrală (packet_in) la execuție locală (match–action). Asta e ideea‑cheie a SDN."*

---

## Bloc E (0:30–0:38) — Stage 3: trafic aplicație TCP/UDP

> Într‑un mediu headless (SSH), evităm `xterm`. Rulăm serverele în background și alimentăm clienții prin pipe. Pedagogic este suficient: scopul e să apară trafic TCP/UDP care trece sau nu prin politica din flow table.

### E1. TCP permis (h1 → h2) (3–4 min)

**🟠 T3 (`mininet>`):**

1) 🔵 Server TCP pe h2 (background):
```text
h2 python3 ../3_sdn-app-traffic/S06_Part03_Script_TCP_Server.py 5000 &
```

2) 🟢 Client TCP pe h1:
```text
h1 sh -c 'printf "hello\nexit\n" | python3 ../3_sdn-app-traffic/S06_Part03_Script_TCP_Client.py 10.0.10.2 5000'
```

> *▸ „Nu e doar ICMP acum. Avem handshake TCP (SYN, SYN‑ACK, ACK — RFC 793), porturi, payload. Controllerul vede pachetele IP și flows‑urile existente le acoperă."*

### E2. TCP blocat (h1 → h3) (2 min)

**Capcana de concepție greșită:** > *▸ „Predicție: dacă nu există server pe h3, de ce eșuează conexiunea? E din cauza lipsei serverului sau din cauza politicii SDN?"*

```text
h1 sh -c 'printf "test\nexit\n" | python3 ../3_sdn-app-traffic/S06_Part03_Script_TCP_Client.py 10.0.10.3 5000'
```

> *▸ „Răspuns: politica SDN blochează traficul **înainte** să ajungă la h3. Chiar dacă ar exista un server pe h3, SYN‑ul nu trece de switch. Verificați în T2 (loguri): apare mesaj de drop. E o diferență de nivel: nu e aplicația care refuză, e rețeaua."*

### E3. (Opțional, dacă ai 4–5 min) Modificare controller: UDP permis, TCP blocat către h3

> Dacă nu ai timp, arată doar patch‑ul pe ecran, explici logica `ip_proto 6 vs 17` și lași implementarea ca temă. Validarea rămâne `dump-flows`.

#### Ce spui (setarea problemei)
> *▸ „Controllerul actual blochează orice trafic către 10.0.10.3, indiferent de protocol. Vreau o politică mai fină: TCP blocat, dar UDP permis — de exemplu pentru un server UDP pe h3. Asta este tipic SDN: politici granulare, pe baza câmpurilor din header."*

#### Ce faci (🟢 T2)
1) Oprești controllerul curent (Ctrl+C).
2) Editezi `S06_Part02C_Script_SDNOS_Ken_Controller.py` — înlocuiești blocul `if dst_ip == "10.0.10.3":` cu:

```python
        # Case 2: destination is h3 (10.0.10.3) -> protocol-aware policy
        if dst_ip == "10.0.10.3":

            # TCP towards h3 -> drop
            if ipv4_pkt.proto == 6:
                match = parser.OFPMatch(
                    eth_type=0x0800,
                    ip_proto=6,
                    ipv4_dst=dst_ip
                )
                actions = []  # empty => drop

                self.add_flow(
                    datapath,
                    priority=20,
                    match=match,
                    actions=actions,
                    buffer_id=msg.buffer_id
                    if msg.buffer_id != ofproto.OFP_NO_BUFFER else None
                )
                self.logger.info("Blocking TCP towards %s (drop flow installed)", dst_ip)
                return

            # UDP towards h3 -> allow (output to port 3, where h3 is connected)
            if ipv4_pkt.proto == 17:
                match = parser.OFPMatch(
                    eth_type=0x0800,
                    ip_proto=17,
                    ipv4_dst=dst_ip
                )
                actions = [parser.OFPActionOutput(3)]

                self.add_flow(
                    datapath,
                    priority=20,
                    match=match,
                    actions=actions,
                    buffer_id=msg.buffer_id
                    if msg.buffer_id != ofproto.OFP_NO_BUFFER else None
                )

                if msg.buffer_id == ofproto.OFP_NO_BUFFER:
                    out = parser.OFPPacketOut(
                        datapath=datapath,
                        buffer_id=ofproto.OFP_NO_BUFFER,
                        in_port=in_port,
                        actions=actions,
                        data=msg.data
                    )
                    datapath.send_msg(out)

                self.logger.info("Permitting UDP towards %s via port 3", dst_ip)
                return

            # Other protocols towards h3 -> drop
            match = parser.OFPMatch(
                eth_type=0x0800,
                ipv4_dst=dst_ip
            )
            actions = []
            self.add_flow(datapath, priority=10, match=match, actions=actions)
            return
```

3) Repornești controllerul:
```bash
osken-manager S06_Part02C_Script_SDNOS_Ken_Controller.py
```

4) Repornești topologia SDN (recomandat, pentru a porni curat):
```text
mininet> exit
```
Apoi:
```bash
sudo mn -c
sudo python3 S06_Part02B_Script_SDN_Topo_Switch.py
```

#### Retest (2 min)

**🟠 T3 (`mininet>`):**

1) Server UDP pe h3:
```text
h3 python3 ../3_sdn-app-traffic/S06_Part03_Script_UDP_Server.py 6000 &
```

2) Client UDP pe h1:
```text
h1 sh -c 'printf "udp1\nexit\n" | python3 ../3_sdn-app-traffic/S06_Part03_Script_UDP_Client.py 10.0.10.3 6000'
```

3) TCP către h3 rămâne blocat:
```text
h1 sh -c 'printf "tcp\nexit\n" | python3 ../3_sdn-app-traffic/S06_Part03_Script_TCP_Client.py 10.0.10.3 5000'
```

4) Dump flows:
```text
s1 ovs-ofctl dump-flows s1
```

**Epifanie 3:**
> *▸ „Flow table codifică acum o politică la nivel de transport: `ip_proto=17` (UDP, RFC 768) permis, `ip_proto=6` (TCP, RFC 793) blocat — aceeași destinație, tratament diferit. În rețele clasice, ai nevoie de ACL‑uri distribuite; în SDN, exprimi politica central și se propagă ca rules."*

---

## Bloc F (0:38–0:40) — Recap + livrabile

### Recap — revenire la hook

> *▸ „La început am întrebat: se poate schimba traseul modificând o singură intrare? Da — am văzut cu traceroute: de la 2 hop‑uri la 3."*
>
> *▸ „Am întrebat și: dacă un nod central decide ce trece, mai avem nevoie de tabele distribuite? Răspunsul e: în SDN, switch‑urile au flow table — care sunt tot tabele, dar populate de controller, nu configurate manual router cu router."*

Trei idei de fixat:
1. În routing static, drumul e controlat de tabelele de rutare; `traceroute` arată traseul efectiv.
2. În SDN, controllerul decide; switch‑ul execută match–action. Flow table e „dovada".
3. Traficul aplicație (TCP/UDP) testează politica mai credibil decât `ping`: handshake vs datagramă, nivelul de transport vs nivelul de rețea.

### Livrabile

1. **Stage 1:** `triangle_routing_output.txt` (conform `S06_Part01C_Tasks_Routing_Triangle.md`): output `ip route` din fiecare router, `ping` + `traceroute` înainte și după comutare, captură scurtă `tcpdump`, paragraf explicativ (6–8 propoziții).
2. **Stage 2 + 3:** `sdn_lab_output.txt` (conform `S06_Part03B_Tasks_SDN_App_Traffic.md`): ping permis/blocat, flow table dump, client/server TCP + UDP, explicație comparativă routing vs SDN (8–10 propoziții).

> Materiale suplimentare pentru studiu individual: paginile HTML din `_HTMLsupport/S06/`.

### Conexiune cu seminarele adiacente
> *▸ „De la S05 am preluat `ip route`, `traceroute`, configurarea manuală. La S07 vom trece la capturarea și filtrarea pachetelor TCP/UDP — ceea ce am văzut azi prin `dump-flows` o vom vedea și la nivel de octeți."*

---

## Cheat‑sheet

### Comenzi Mininet (Stage 1 — triangle)
| Ce vrei | Comanda |
|---|---|
| Pornire topologie | `sudo python3 S06_Part01B_Script_Routing_Triangle_Topology.py` |
| Verificare IP‑uri | `r1 ip a` / `h1 ip a` |
| Tabel de rutare | `r1 ip route` |
| Ping | `h1 ping -c 2 10.0.3.2` |
| Traceroute (fără DNS) | `h1 traceroute -n 10.0.3.2` |
| Adăugare rută | `r2 ip route add 10.0.3.0/30 via 10.0.23.2` |
| Ștergere rută | `r1 ip route del 10.0.3.0/30` |
| Captură tcpdump | `r2 tcpdump -i r2-eth1 -n -c 20` |
| Captură în fișier | `r2 tcpdump -i r2-eth1 -n -w /tmp/triangle.pcap -c 50` |

### Comenzi SDN (Stage 2–3)
| Ce vrei | Comanda |
|---|---|
| Pornire controller | `osken-manager S06_Part02C_Script_SDNOS_Ken_Controller.py` |
| Pornire topologie SDN | `sudo python3 S06_Part02B_Script_SDN_Topo_Switch.py` |
| Ping h1→h2 | `h1 ping -c 3 10.0.10.2` |
| Ping h1→h3 (blocat) | `h1 ping -c 3 10.0.10.3` |
| Dump flow table | `s1 ovs-ofctl dump-flows s1` |
| Dump cu OF13 explicit | `s1 ovs-ofctl -O OpenFlow13 dump-flows s1` |
| Set OF13 pe bridge | `s1 ovs-vsctl set bridge s1 protocols=OpenFlow13` |
| Server TCP pe h2 | `h2 python3 ../3_sdn-app-traffic/S06_Part03_Script_TCP_Server.py 5000 &` |
| Client TCP din h1 | `h1 sh -c 'printf "msg\nexit\n" \| python3 ../3_sdn-app-traffic/S06_Part03_Script_TCP_Client.py 10.0.10.2 5000'` |
| Server UDP pe h3 | `h3 python3 ../3_sdn-app-traffic/S06_Part03_Script_UDP_Server.py 6000 &` |
| Client UDP din h1 | `h1 sh -c 'printf "msg\nexit\n" \| python3 ../3_sdn-app-traffic/S06_Part03_Script_UDP_Client.py 10.0.10.3 6000'` |

### Urgențe
| Ce s‑a stricat | Fix |
|---|---|
| Reset Mininet | `sudo mn -c` |
| Kill controller | `sudo pkill -f osken-manager` |
| Verificare procese | `ps aux \| grep -E "(mininet\|osken)"` |

---

## Plan de contingență

| # | Problemă | Soluție |
|---|---|---|
| 1 | Controllerul nu se conectează la switch | Verifici portul: scriptul folosește 6633. Unele configurări pot folosi 6653. Asiguri consistența între `RemoteController(port=6633)` și procesul Os‑Ken. |
| 2 | `ovs-ofctl dump-flows` pare gol | Rulezi mai întâi `h1 ping -c 1 10.0.10.2` pentru a forța un `PacketIn` și instalarea de flows. |
| 3 | Versiune OpenFlow nepotrivită | Setezi explicit: `s1 ovs-vsctl set bridge s1 protocols=OpenFlow13` și folosești `ovs-ofctl -O OpenFlow13 dump-flows s1`. |
| 4 | Nu ai timp de modificat controllerul | Arăți patch‑ul pe ecran, explici logica (ip_proto 6 vs 17), lași implementarea ca temă. În clasă validezi doar Stage 2. |
| 5 | `traceroute` nu funcționează (asteriscuri) | ICMP TTL exceeded poate fi blocat. Folosești `ip route get 10.0.3.2` pe r1 pentru a vedea next‑hop. Alternativ: `h1 ping -c 1 -t 1 10.0.3.2`, apoi `-t 2`, manual. |
| 6 | `osken-manager` nu există ca comandă | Verifici venv: `source ~/compnet/bin/activate`. Alternativ: `python3 -m os_ken.cmd.manager ...`. |
| 7 | Eroare „Address already in use" la server TCP/UDP | Verifici: `ss -tlnp \| grep 5000`. Oprești procesul existent sau folosești alt port. Sau: adaugă flag `SO_REUSEADDR` (deja prezent în script). |

---

## Referințe (APA 7th ed.)

| Referință | DOI |
|---|---|
| Baker, F. (1995). *Requirements for IP Version 4 Routers* (RFC 1812). RFC Editor. | https://doi.org/10.17487/RFC1812 |
| Kreutz, D., Ramos, F. M. V., Veríssimo, P., Rothenberg, C. E., Azodolmolky, S., & Uhlig, S. (2015). Software-Defined Networking: A Comprehensive Survey. *Proceedings of the IEEE, 103*(1), 14–76. | https://doi.org/10.1109/JPROC.2014.2371999 |
| Lantz, B., Heller, B., & McKeown, N. (2010). A network in a laptop: Rapid prototyping for software-defined networks. *Proceedings of the 9th ACM SIGCOMM Workshop on Hot Topics in Networks*. | https://doi.org/10.1145/1868447.1868466 |
| McKeown, N., Anderson, T., Balakrishnan, H., Parulkar, G., Peterson, L., Rexford, J., Shenker, S., & Turner, J. (2008). OpenFlow: Enabling innovation in campus networks. *ACM SIGCOMM Computer Communication Review, 38*(2), 69–74. | https://doi.org/10.1145/1355734.1355746 |
| Open Networking Foundation. (2015). *OpenFlow Switch Specification Version 1.3.5* (ONF TS-025). | — |
| Postel, J. (1981). *Internet Protocol* (RFC 791). RFC Editor. | https://doi.org/10.17487/RFC0791 |
| Postel, J. (1980). *User Datagram Protocol* (RFC 768). RFC Editor. | https://doi.org/10.17487/RFC0768 |
| Postel, J. (1981). *Transmission Control Protocol* (RFC 793). RFC Editor. | https://doi.org/10.17487/RFC0793 |

---

## Note pedagogice

### Misconcepții anticipate (nescrise în kit, dar previzibile la S06)

| Concepția greșită | Unde se adresează | Tipar socratic |
|---|---|---|
| „Routerul alege automat cel mai scurt drum" (confuzie cu routing dinamic) | Bloc B3: comutarea manuală arată că ruta e explicit configurată | POE 1 |
| „Switch‑ul SDN ia decizii inteligente" (confuzie control/data plane) | Bloc D1 + D3: switch‑ul execută doar ce e în flow table | Explicație la D3 |
| „Dacă ping merge, TCP merge sigur" (confuzie L3/L4) | Bloc E1 + E2: TCP trece, dar doar pentru că flows‑urile acoperă IP‑urile respective | Capcana la E2 |

### Structura socratică

| Tipar | Loc | Obiectiv vizat |
|---|---|---|
| **POE 1** (predicție hop‑uri) | B2 | OB1 — interpretare `traceroute` |
| **POE 2** (unde se vede blocajul) | C → D3 | OB3 — rolul flow table |
| **Capcana** (lipsă server vs politică SDN) | E2 | OB4 — diferența L3/L4 |
| **„Ce s‑ar fi întâmplat dacă…"** | B3 (comutare rută) + E3 (modificare controller) | OB2, OB5 |

### Plan de sacrificare (dacă ai doar 30 min)

| Prioritate | Ce scoți | Ce păstrezi |
|---|---|---|
| Prima tăietură | E3 (modificare controller) — devine temă | Blocuri A–E2 + F |
| A doua tăietură | B1 (verificare IP) — o menționezi verbal | Blocuri A, B0+B2+B3, C–E2, F |
| A treia tăietură | E1–E2 (trafic aplicație) — doar menționat, devine temă | Blocuri A–D + F (25 min) |
