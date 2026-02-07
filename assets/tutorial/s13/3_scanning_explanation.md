#### Seminar 13 – Stage 2

## Scanarea rețelei: nmap și implementarea unui scanner simplu în Python

În acest stage vom învăța două tehnici fundamentale de reconnaissance:

1. **Scanarea rețelei cu unelte dedicate (nmap)**
2. **Scanarea manuală printr-un script Python** (pentru înțelegerea mecanismelor interne)

Scopul este *nu doar* să descoperim porturi deschise, ci să înțelegem **comportamentul unei aplicații la nivel de socket**.

---

## 1. Scanarea cu nmap

`nmap` este unealta standard pentru:

* descoperire hosturi
* identificare porturi deschise
* identificare versiuni
* identificare vulnerabilități (prin scripturi NSE)

### 1.1. Scanare a rețelei din laborator

Rețeaua Docker este:

```
172.20.0.0/24
```

Pentru a descoperi hosturile active:

```bash
sudo nmap -sn 172.20.0.0/24
```

Pentru a descoperi porturile deschise ale fiecărui host:

```bash
nmap -sV -p- 172.20.0.10
nmap -sV -p- 172.20.0.11
nmap -sV -p- 172.20.0.12
```

Explicații:

* `-sV` identifică versiunea software
* `-p-` scanează **toate porturile (1–65535)**
* `-T4` sau `-T5` accelerează scanarea (risc: false negatives)

---

## 2. De ce scriem propriul scanner?

`nmap` este excelent, însă este complex și ascunde multe detalii.
Pentru a înțelege:

* cum funcționează o conexiune TCP
* ce înseamnă *open*, *closed*, *filtered*
* de ce timeouts contează

Vom scrie un scanner Python minimal, care:

* încearcă `connect()` pe fiecare port
* marchează porturile deschise
* are timeouts configurabile
* poate scana rapid un range de porturi

---

## 3. Anatomia unui port scanner simplu

Pașii necesari:

1. creezi un socket TCP
2. setezi un timeout (0.1 – 0.5 sec)
3. încerci conexiunea cu `connect_ex()`
4. dacă rezultatul este `0` → port deschis
5. dacă este alt cod de eroare → închis / filtrat
6. închizi socketul
7. repeți pentru un set de porturi

Vom oferi un template Python unde studenții completează logica principală.

---

## 4. De ce nu putem vedea tot cu un scanner simplu?

Lucruri pe care scannerul nostru **nu** le poate detecta:

* aplicațiile UDP (pentru UDP este nevoie de altă logică)
* serviciile protejate cu firewall
* porturi filtrate sau responsabile doar la anumite pachete
* fingerprinting de versiuni
* scanări stealth (SYN scan, FIN scan etc.)

Dar este perfect pentru:

* înțelegerea conceptelor
* identificarea porturilor TCP „open”
* analizarea comportamentului aplicațiilor din mediul vulnerabil
