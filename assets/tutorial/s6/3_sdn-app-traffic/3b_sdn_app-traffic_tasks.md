### Sarcini: Trafic TCP si UDP prin switch-ul SDN

Aceste sarcini continua peste Stage 2 (controller Os-ken + topologie SDN).

Presupunem ca:
- controllerul Os-Ken este pornit cu `index_sdn_os-ken_controller.py`
- topologia Mininet SDN este pornita cu `index_sdn_topo_switch.py`

---

### 1. Test TCP permis intre h1 si h2

1. In CLI Mininet, porniti serverul TCP pe h2:

```bash
h2 python3 tcp_server.py 5000
````

2. In alt terminal Mininet (sau dupa ce deschideti un nou CLI cu `xterm h1`, daca il folositi), porniti clientul TCP pe h1:

```bash
h1 python3 tcp_client.py 10.0.10.2 5000
```

3. Trimiteti cateva mesaje (ex: `hello`, `test`) si verificati ca:

* serverul le afiseaza
* clientul primeste eco

4. Opriti clientul cu `exit`, apoi opriti serverul cu Ctrl-C.

---

### 2. Test TCP blocat intre h1 si h3

1. Din h1, incercati sa va conectati la h3 (fara sa rulati un server acolo, va fi oricum blocat de SDN):

```bash
h1 python3 tcp_client.py 10.0.10.3 5000
```

2. Observati:

* ar trebui sa vedeti `Connection failed` sau time-out
* in log-ul Os-ken, veti vedea mesaje despre drop pentru trafic catre 10.0.10.3
* in `ovs-ofctl dump-flows s1` ar trebui sa apara flow-ul de tip drop (instalat anterior)

Salvati output-ul clientului in fisierul de deliverable.

---

### 3. Test UDP cu h3 (initial blocat la nivel IP)

1. Porniti serverul UDP pe h3:

```bash
h3 python3 udp_server.py 6000
```

2. Din h1, porniti clientul UDP:

```bash
h1 python3 udp_client.py 10.0.10.3 6000
```

3. Incearcati sa trimiteti cateva mesaje. In functie de implementarea controllerului:

* daca aveti flow de drop general pe `dst_ip == 10.0.10.3`, este posibil sa nu ajunga nimic
* daca nu aveti inca flow de drop pentru acest caz, mesajele pot trece

În etapa următoare vom modifica explicit controllerul pentru a controla separat TCP si UDP.

---

### 4. Modificare controller Os-ken: permite UDP, blocheaza TCP spre h3

In fisierul `index_sdn_os-ken_controller.py`, in handler-ul `packet_in_handler`, modificati logica astfel incat:

* pentru trafic TCP (ip_proto = 6) catre `10.0.10.3`:

  * instalati un flow de tip drop (ca pana acum)
* pentru trafic UDP (ip_proto = 17) catre `10.0.10.3`:

  * instalati un flow care **permite** trimiterea catre portul h3

Indicii:

* obtineti protocolul din `ipv4_pkt.proto`
* puteti folosi `parser.OFPMatch` astfel:

```python
match = parser.OFPMatch(
    eth_type=0x0800,
    ip_proto=17,         # UDP
    ipv4_dst="10.0.10.3"
)
```

* pentru actiuni, folositi portul pe care este conectat h3 (de obicei 3):

```python
actions = [parser.OFPActionOutput(3)]
```

* pentru TCP, folositi `ip_proto=6` si actiuni goale (`actions = []`) pentru drop.

Dupa modificare, reporniti controllerul:

```bash
# opriti vechiul Os-ken
# apoi:
osken-manager index_sdn_os-ken_controller.py
```

Si reporniti reteaua Mininet daca era oprita.

---

### 5. Retestare UDP si TCP

1. Cu serverul UDP pe h3:

```bash
h3 python3 udp_server.py 6000
```

2. Cu clientul UDP pe h1:

```bash
h1 python3 udp_client.py 10.0.10.3 6000
```

3. Trimiteti cateva mesaje:

* acum ar trebui sa vedeti mesaje afisate de server si raspunsurile eco la client
* UDP ar trebui sa fie permis

4. Reincercati clientul TCP:

```bash
h1 python3 tcp_client.py 10.0.10.3 5000
```

* acesta trebuie sa fie in continuare blocat (drop la nivel SDN)

---

### 6. Inspectarea flow-urilor dupa modificare

Rulati:

```bash
s1 ovs-ofctl dump-flows s1
```

Cautati:

* flow pentru UDP cu ip_proto=17, dst=10.0.10.3 si actiune output spre portul h3
* flow pentru TCP cu ip_proto=6, dst=10.0.10.3 si actiuni goale (drop)

---

### Deliverable final SDN

Combinati toate rezultatele din stage 2 si 3 intr-un singur fisier:

```
sdn_lab_output.txt
```

Acesta trebuie sa contina:

1. Output relevante din stage 2:

   * ping h1 -> h2 (reusit)
   * ping h1 -> h3 (esuat)
   * un dump de flow table

2. Output din stage 3:

   * rularea clientului TCP h1 -> h2 (mesaje reusite)
   * rularea clientului TCP h1 -> h3 (esuat)
   * rularea clientului UDP h1 -> h3 (reusit dupa modificarea controllerului)
   * un dump de flow table dupa modificare

3. O explicatie de 8–10 propozitii in care descrieti:

   * diferenta dintre rutare clasica (triangle) si SDN
   * cum influenteaza controllerul Os-ken traficul TCP si UDP
   * cum se vede in flow table politica de securitate (blocare TCP, permitere UDP)
   * ce avantaje are SDN pentru astfel de politici fine (application-aware)

Acest fisier va fi tema de predat pentru Seminarul 6.

