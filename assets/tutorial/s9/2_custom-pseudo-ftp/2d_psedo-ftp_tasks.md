### Stage 3 – Sarcini pentru pseudo-FTP (active/pasive)

Scop: sa intelegeti practic cum functioneaza un protocol de tip FTP cu:
- conexiune de control
- conexiuni de date in mod activ si pasiv

Rezultatul acestui stage va fi un fisier de log:

```

pseudoftp_log.txt

````

si codul server/client eventual usor modificat de voi.

---

## 1. Pregatirea folderelor

Asigurati-va ca aveti doua directoare:

```bash
mkdir -p temp
mkdir -p client-temp
````

In `temp` puneti cel putin 2 fisiere text (ex. `server1.txt`, `server2.txt`).

In `client-temp` puneti cel putin 1 fisier (ex. `client1.txt`).

---

## 2. Porniti serverul

Intr-un terminal:

```bash
python3 pseudo_ftp_server.py
```

Ar trebui sa vedeti:

```
[SERVER] Pseudo-FTP server listening on 127.0.0.1:3333
```

---

## 3. Porniti clientul

Intr-un alt terminal:

```bash
python3 pseudo_ftp_client.py
```

Ar trebui sa vedeti:

```text
[CLIENT] Connected to pseudo-FTP server at 127.0.0.1:3333
Commands: list, help, active_get/put, passive_get/put, Ctrl+C to exit
-> 
```

---

## 4. Testati comenzi de control (list, help)

1. In client, rulati:

```text
-> help
-> list
```

2. Copiati output-ul (atat de la `help`, cat si de la `list`) in fisierul:

```
pseudoftp_log.txt
```

---

## 5. Test activ (active_get / active_put)

### active_get

1. Din client:

```text
-> active_get server1.txt
```

2. Verificati ca fisierul `server1.txt` apare in directorul `client-temp`.

### active_put

1. Din client:

```text
-> active_put client1.txt
```

2. Verificati ca fisierul `client1.txt` apare in directorul `temp`.

Notati in `pseudoftp_log.txt` ce comenzi ati dat si daca transferurile au reusit.

---

## 6. Test pasiv (passive_get / passive_put)

### passive_get

1. Din client:

```text
-> passive_get server2.txt
```

2. Verificati ca fisierul `server2.txt` apare in `client-temp`.

### passive_put

1. Din client:

```text
-> passive_put client1.txt
```

2. Verificati ca fisierul aparut in `temp` (poate suprascrie sau crea o copie).

Adaugati in `pseudoftp_log.txt` output-ul relevant din client (mesaje [CLIENT] si eventual mesaje [SERVER] daca le vedeti).

---

## 7. Mică extensie (obligatorie, dar foarte simpla)

In `pseudo_ftp_server.py`, functia:

```python
def process_help(client, command_items):
    ...
```

contine un text de help simplu.

TASK:

* modificati textul astfel incat sa includa si o scurta descriere (1 fraza) pentru fiecare comanda.
* de exemplu:

```text
active_get <filename>  - descarca fisierul de pe server folosind mod activ
```

Rulati din nou:

```text
-> help
```

si copiati noul output in `pseudoftp_log.txt` (sub un heading separat, de forma `--- HELP MODIFICAT ---`).

---

## 8. Intrebari de reflexie (de scris la finalul pseudoftp_log.txt)

Raspundeti in 1–3 propozitii la fiecare:

1. Care este diferenta practica intre `active_get` si `passive_get` in acest protocol?
2. Ce se intampla daca rulati serverul si clientul pe masini diferite intr-o retea cu firewall/NAT?

   * care mod e mai probabil sa functioneze (activ/pasiv) si de ce?
3. In ce fel seamana acest protocol cu FTP-ul real?
4. Ce limitari evidente are (marime fisier, securitate, robustete)?

---

### Deliverable Stage 3

Predati:

* `pseudo_ftp_server.py` (poate contine doar modificarea de help)
* `pseudo_ftp_client.py` (nemodificat sau cu mici imbunatatiri de afisare)
* `pseudoftp_log.txt` cu:

  * output de la `help` (initial si modificat)
  * output de la `list`
  * cel putin un transfer `active_get` si unul `active_put`
  * cel putin un transfer `passive_get` si unul `passive_put`
  * raspunsurile la intrebarile de reflexie

