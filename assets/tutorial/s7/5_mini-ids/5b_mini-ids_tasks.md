### Stage 6 – mini IDS (tema integrata pentru Seminarul 7)

In acest stage veti finaliza un mini IDS (Intrusion Detection System)
bazat pe ideile din etapele anterioare:

- sniffer RAW
- filtrare TCP/UDP
- detectare de port scan
- detectare UDP spray
- detectare flood catre un port

Rezultatul final este scriptul `mini_ids.py` + fisierul de log `ids_alerts.log`
si un scurt raport.

---

### 1. Completati functia log_alert

In `mini_ids.py`, functia:

```python
def log_alert(message: str):
    ...
````

trebuie sa:

1. construiasca un mesaj cu timestamp:

   * format sugerat: `[YYYY-MM-DD HH:MM:SS] <mesaj>`
2. afiseze mesajul pe ecran (print)
3. scrie acelasi mesaj intr-un fisier `ids_alerts.log`, cate o alerta pe linie

Pasii de baza sunt deja in cod, dar verificati:

* ca fisierul este deschis in modul append (`"a"`)
* ca folositi `full_msg + "\n"`

---

### 2. Detectarea port-scan-ului TCP

In functia:

```python
def handle_tcp_packet(src_ip, dst_ip, dst_port, flags, now):
    ...
```

exista deja logica propusa, similara cu `detect_scan.py`.

Task:

1. Intelegere:

   * pentru fiecare `src_ip`, `ids_state["tcp_scan"][src_ip]` este un dictionar:

     * cheie: `dst_port`, valoare: `timestamp`
   * `cleanup_old_entries` sterge porturile mai vechi de `WINDOW_SECONDS` secunde
   * daca numarul de porturi distincte >= `TCP_SYN_THRESHOLD`, se apeleaza `log_alert`

2. Ajustati (daca este nevoie) logica dupa cum doriti, dar pastrand ideea:

   * contorizati doar SYN fara ACK (`is_syn and not is_ack`)
   * tratati doar pachetele TCP relevante (restul pot fi ignorate)

3. Test:

   * rulati `mini_ids.py` pe un host (ex: h2)
   * rulati `port_scanner.py` de pe alt host (ex: h1) cu un interval de porturi de cel putin 20–30:

     ```bash
     h1 python3 port_scanner.py 10.0.10.2 1 200
     ```
   * verificati ca apare o alerta de tip:

     ```text
     [....] Posibil TCP PORT SCAN de la 10.0.10.1: 10 porturi SYN ...
     ```

---

### 3. Detectarea UDP "spray"

In functia:

```python
def handle_udp_packet(src_ip, dst_ip, dst_port, now):
    ...
```

trebuie sa folositi `ids_state["udp_spray"]` pentru a detecta multi-port UDP
de la aceeasi sursa.

Task:

1. Structura:

   * `ids_state["udp_spray"][src_ip]` este un dictionar:

     * cheie: `dst_port`, valoare: `timestamp`

2. Logica:

   * stergeti intrarile vechi cu `cleanup_old_entries`
   * inregistrati `dst_port` cu timestamp
   * daca numarul de porturi distincte >= `UDP_PORT_THRESHOLD` in `WINDOW_SECONDS` secunde:

     * apelati `log_alert` cu un mesaj de tip:

       ```text
       Posibil UDP SPRAY de la <src_ip>: <N> porturi UDP in ultimele <WINDOW_SECONDS>s
       ```

3. Test:

   * pe „atacator” (h1), scrieti sau adaptati un script care trimite UDP catre mai multe porturi
     (puteti chiar modifica `udp_client.py` sau sa folositi un mic script propriu).
   * rulati `mini_ids.py` pe h2
   * verificati ca apare alerta UDP dupa ce ati trimis catre suficiente porturi.

---

### 4. Detectarea flood-ului catre un port

Tot in `handle_tcp_packet`, aveti logica pentru `ids_state["flood"]`:

* cheia este un tuplu `(dst_ip, dst_port)`
* valoarea este un dictionar `{ timestamp: timestamp }` (sau alt mod simplu de a numara pachete)

Task:

1. Verificati si intelegeti logica existenta:

   * se sterg intrarile vechi (mai vechi de `WINDOW_SECONDS` secunde)
   * se adauga un nou timestamp pentru fiecare pachet
   * daca lungimea dictionarului >= `FLOOD_THRESHOLD`:

     * se apeleaza `log_alert` cu mesajul de flood

2. Optional, adaptati sau simplificati:

   * puteti folosi doar numarul de pachete, nu e nevoie sa stocati toate timestamp-urile
   * dar actuala implementare este suficient de simpla pentru laborator

3. Test:

   * rulati un script care trimite multe pachete TCP catre acelasi port intr-un timp scurt
     (puteti modifica `port_scanner.py` sa scaneze acelasi port de foarte multe ori
     sau sa scrieti un mic script care face multe connect-uri rapide).
   * verificati ca apare alerta de flood.

---

### 5. Rulare integrata si colectare log

Rulati `mini_ids.py` pe masina/hostul „victima” (ex: h2) pentru cel putin 2–3 scenarii:

1. Scenariu 1 – port scan TCP (cu `port_scanner.py`)
2. Scenariu 2 – multi-port UDP (cu un script UDP sau `udp_client.py` modificat)
3. Scenariu 3 – eventual un flood catre un port (script dedicat sau adaptare)

Dupa ce rulati aceste teste:

* opriti `mini_ids.py` cu Ctrl-C
* deschideti fisierul `ids_alerts.log`
* verificati ca sunt inregistrate alertelor corespunzatoare scenariilor de mai sus

---

### 6. Raport scurt

Creati un fisier:

```text
explanation.md
```

In care scrieti 10–15 propozitii (sau 3–5 paragrafe scurte) despre:

1. Ce tipuri de atacuri / comportamente detecteaza mini IDS-ul vostru:

   * port scan TCP
   * UDP spray
   * flood catre un port
2. Ce parametri controleaza sensibilitatea:

   * WINDOW_SECONDS
   * TCP_SYN_THRESHOLD
   * UDP_PORT_THRESHOLD
   * FLOOD_THRESHOLD
3. Exemple concrete de „false positive” si „false negative”:

   * cand ati putea avea alerta, dar nu este atac real
   * cand un atac real ar putea trece neobservat
4. Cel putin 2 idei de imbunatatire:

   * alte pattern-uri (ex: scan lent cu multe minute intre pachete)
   * analiza continutului pachetelor (signaturi)
   * integrare cu un log central sau cu un sistem de alerta real

---

### 7. Deliverable final pentru Seminarul 7

La finalul seminarului (sau ca tema), studentul trebuie sa predea un pachet
care contine cel putin:

* `packet_sniffer.py` (Stage 2, completat)
* `packet_filter.py` (Stage 3, completat)
* `port_scanner.py` (Stage 4, completat)
* `detect_scan.py` (Stage 5)
* `mini_ids.py` (Stage 6, completat)
* `sniffer_log.txt`
* `filter_results.txt`
* `scan_results.txt` sau `scan_log.txt`
* `scan_detection.txt`
* `ids_alerts.log`
* `explanation.md`

Acesta reprezinta proiectul integrat al Seminarului 7:
de la sniffer, la filtru, la port scanner, la detectie de scan/flood si mini IDS.

