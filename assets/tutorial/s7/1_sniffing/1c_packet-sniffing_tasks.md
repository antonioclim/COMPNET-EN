### Sarcini – Sniffer simplu de pachete IPv4 (Stage 2)

In acest stage veti:

- completa functia `parse_ipv4_header` din `packet_sniffer.py`
- rula snifferul pe o interfata
- genera putin trafic (ping, curl, etc.)
- colecta un log cu primele 20 de pachete IPv4

---

### 1. Completati parse_ipv4_header

In fisierul `packet_sniffer.py` gasiti functia:

```python
def parse_ipv4_header(data: bytes):
    ...
    # >>> STUDENT TODO
    ...
    raise NotImplementedError("Completați funcția parse_ipv4_header")
````

Task:

1. Implementati urmatorii pasi in locul TODO-ului:

   * extrageti `version_ihl = data[0]`
   * calculati:

     * `version = version_ihl >> 4`
     * `ihl = (version_ihl & 0x0F) * 4`
   * folositi `struct.unpack` pentru a obtine:

     * `ttl`, `proto`, `src`, `dst`
   * convertiti `src` si `dst` in string cu `ipv4_addr`
   * intoarceti `(src_ip_str, dst_ip_str, proto, ihl)`

2. Dupa implementare, stergeti sau comentati linia:

```python
raise NotImplementedError("Completați funcția parse_ipv4_header")
```

Sugestie de `struct.unpack`:

```python
ttl, proto, src, dst = struct.unpack('! 8x B B 2x 4s 4s', data[:20])
```

---

### 2. Porniti snifferul

Rulati:

```bash
sudo python3 packet_sniffer.py <INTERFATA>
```

Exemple:

* pe masina locala: `eth0`, `wlan0`, `lo`
* in Mininet (pe un host): `h1-eth0`

Exemplu in Mininet (dupa ce sunteti in CLI Mininet):

```bash
h1 sudo python3 packet_sniffer.py h1-eth0
```

---

### 3. Generati trafic

In timp ce snifferul ruleaza:

* intr-un alt terminal, faceti un `ping` catre o adresa:

  * `ping 8.8.8.8` (pe masina locala)
  * sau `h1 ping 10.0.1.1` in Mininet
* sau rulati un `curl http://example.com`
* sau orice alta comanda care genereaza trafic IPv4

Observati liniile de forma:

```text
[1] 192.168.0.10 -> 8.8.8.8  proto=ICMP
[2] 8.8.8.8 -> 192.168.0.10  proto=ICMP
[3] ...
```

---

### 4. Opriti snifferul si salvati logul

Opriti snifferul cu `Ctrl-C` dupa ce au fost afisate cel putin 20 de pachete (sau dupa ce `MAX_PACKETS` este atins).

Copiati output-ul relevant intr-un fisier:

```text
sniffer_log.txt
```

Acest fisier trebuie sa contina:

* cel putin 20 de linii de forma:

  * `[N] SRC_IP -> DST_IP  proto=...`
* cateva pachete ICMP (de la ping)
* daca se poate, cateva pachete TCP sau UDP (de la curl sau alte comenzi)

---

### 5. Intrebari de reflexie (de scris in sniffer_log.txt)

Sub log, raspundeti scurt (1–2 propozitii la fiecare):

1. Ce protocol ati vazut cel mai des in captura (ICMP, TCP, UDP)?
2. Ce adrese IP apar cel mai frecvent ca destinatie? De ce?
3. Ce se intampla cu snifferul daca nu sunteti root (fara sudo)?

---

### Deliverable Stage 2

* fisierul `packet_sniffer.py` completat (cu functia `parse_ipv4_header` implementata)
* fisierul `sniffer_log.txt` cu:

  * logul pachetelor
  * raspunsurile la intrebarile de reflexie

