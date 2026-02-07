### Sarcini: Topologia SDN cu Os-ken si switch OpenFlow

---

### 1. Pornirea controllerului Os-ken

Intr-un terminal separat (NU in Mininet), rulati:

```bash
osken-manager index_sdn_os-keb_controller.py
````

Ar trebui sa vedeti loguri os-ken si eventual un mesaj cand se conecteaza switch-ul.

---

### 2. Pornirea topologiei Mininet SDN

In alt terminal:

```bash
sudo python3 index_sdn_topo_switch.py
```

Dupa pornire, veti intra in CLI-ul Mininet (`mininet>`).

Verificati hosturile:

```bash
h1 ip a
h2 ip a
h3 ip a
```

---

### 3. Testarea conectivitatii cu ping

#### a) h1 catre h2 (trebuie sa mearga)

```bash
h1 ping -c 3 10.0.10.2
```

Ar trebui sa vedeti reply-uri si sa apara flow-uri noi in s1.

#### b) h1 catre h3 (trebuie sa fie blocat)

```bash
h1 ping -c 3 10.0.10.3
```

Ar trebui sa vedeti timeout (no reply). Controllerul instaleaza un flow de tip drop.

---

### 4. Inspectarea flow table-ului

In CLI-ul Mininet:

```bash
s1 ovs-ofctl dump-flows s1
```

Analizati:

* exista flow-ul table-miss (prioritate 0)?
* exista flow-uri pentru traficul 10.0.10.1 ↔ 10.0.10.2?
* exista flow-uri de tip drop pentru destinatia 10.0.10.3?

---

### 5. *Optional*: captura de trafic

Porniti o captura pe s1:

```bash
s1 tcpdump -i s1-eth1 -n
```

Si in paralel:

```bash
h1 ping -c 3 10.0.10.2
```

Observati pachetele ICMP. Opriti tcpdump cu Ctrl-C.

---

### Deliverable partial

Creati fisierul:

```
sdn_stage2_output.txt
```

Acesta trebuie sa contina:

* output de la:

  * `h1 ping 10.0.10.2`
  * `h1 ping 10.0.10.3`
* un `ovs-ofctl dump-flows s1` (complet sau partial)
* 5–7 propozitii in care explicati:

  * cum se vede in flow table faptul ca traficul h1 ↔ h2 este permis
  * cum se vede faptul ca traficul catre h3 este blocat
  * ce rol are regula table-miss

Acest fisier va fi completat in Stage 3 cu teste pe servere/cliente Python.

