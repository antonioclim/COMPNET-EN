### Introducere SDN si topologia cu switch OpenFlow

In aceasta sectiune vom folosi o topologie Mininet bazata pe un switch OpenFlow (s1), controlat de un controller extern Ryu. Vom vedea cum controllerul poate decide ce trafic este permis si ce trafic este blocat, prin instalarea de flow-uri in switch.

---

### Concept de baza SDN

Software Defined Networking (SDN) separa:

- **control plane** – logica de decizie (controllerul)
- **data plane** – dispozitivele care doar aplica regulile (switch-uri, routere)

In SDN:

- controllerul vorbeste cu switch-urile printr-un protocol de control (de ex. OpenFlow)
- switch-urile trimit catre controller pachetele necunoscute (packet_in)
- controllerul raspunde cu instructiuni (packet_out, flow_mod) care instaleaza reguli de tip match–action

---

### Topologia SDN folosita

Topologia folosita in Mininet:

```

h1 ---- s1 ---- h2
|
+---- h3

```

- s1 este un Open vSwitch configurat sa foloseasca OpenFlow
- h1, h2, h3 sunt hosturi Mininet
- exista un controller Ryu extern care se conecteaza la s1

Schema de adresare (toate in acelasi subnet):

| Host | Interfata  | Adresa IPv4    |
|------|------------|----------------|
| h1   | h1-eth0    | 10.0.10.1/24   |
| h2   | h2-eth0    | 10.0.10.2/24   |
| h3   | h3-eth0    | 10.0.10.3/24   |

---

### Comportament dorit (logica SDN)

Controllerul Ryu trebuie sa impuna urmatoarea politica:

- traficul intre h1 si h2 este permis (h1 ↔ h2)  
- traficul de la h1 catre h3 este blocat  
- optionale:
  - traficul de la h3 catre h1 poate fi permis sau blocat, in functie de implementare

Implementarea face:

- la primul pachet (packet_in) dintre h1 si h2:
  - instaleaza flow-uri bidirectionale in s1 (h1 → h2 si h2 → h1)
- la un pachet cu destinatia h3:
  - instaleaza un flow de tip drop (fara actiuni) pentru a bloca traficul

---

### Ce veti face in acest stage

- veti porni controllerul Ryu cu aplicatia noastra simpla
- veti porni topologia Mininet cu switch-ul s1
- veti testa conectivitatea:
  - `h1 ping h2` trebuie sa mearga
  - `h1 ping h3` trebuie sa fie blocat
- veti inspecta flow table-ul din s1 cu `ovs-ofctl dump-flows`

Serverele si clientii Python vor fi adaugati in etapa urmatoare pentru a genera trafic mai interesant decat ping.
