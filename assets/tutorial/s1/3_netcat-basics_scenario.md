### Introducere

În această etapă vom lucra cu `netcat` (nc), unul dintre cele mai versatile instrumente pentru testarea conexiunilor, transferul de date și simularea rapidă a serverelor și clienților. Vom acoperi atât modul TCP, cât și modul UDP, pentru a înțelege diferențele funcționale dintre ele.

---

### Server și client TCP cu netcat

#### 1. Pornirea unui server TCP pe portul 9000

```
nc -l -p 9000
```

Comanda rămâne blocată în așteptarea unei conexiuni.

#### 2. Conectarea unui client TCP

Dintr-un alt terminal:

```
nc 127.0.0.1 9000
```

Scrieți text în oricare din cele două terminale. Netcat îl va transmite automat în cealaltă parte.

---

### Server și client UDP cu netcat

UDP nu creează o conexiune persistentă, iar netcat funcționează ușor diferit în acest mod.

#### 3. Pornirea unui server UDP pe portul 9001

```
nc -u -l -p 9001
```

#### 4. Trimiterea unui mesaj UDP către server

```
echo "test UDP" | nc -u 127.0.0.1 9001
```

Observați că serverul UDP primește mesajul, dar nu menține o sesiune. Pentru trimitere bidirecțională, folosiți comenzi separate.

---

### Observații

Notă că:

* TCP oferă o conexiune stabilă, bidirecțională, vizibilă imediat în comportamentul netcat: orice scrieți într-o parte apare în cealaltă.
* UDP trimite datagrame individuale fără a menține o stare; netcat va primi doar fiecare mesaj trimis separat.
* Netcat este util pentru debugging rapid, mai ales când se testează firewall-uri, rutări sau prototiparea unui protocol text.

