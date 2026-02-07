### Stage 3 – Protocol pseudo-FTP (control + data, mod activ si pasiv)

In aceasta etapa folosim un protocol custom inspirat de FTP:

- **o conexiune de control**: comenzi text
- **conexiuni separate de date**: pentru transferul fisierelor

Scop:

- sa intelegem practic diferenta dintre control si data
- sa vedem cum arata modurile active/pasive implementate „de mana”
- sa experimentam cu un mini server de tip FTP scris cu socket-uri

---

## 1. Conexiunea de control

Clientul si serverul au o conexiune TCP permanenta (port 3333):

- pe aceasta conexiune se trimit comenzi text:
  - `list`
  - `active_get filename`
  - `active_put filename`
  - `passive_get filename`
  - `passive_put filename`

Serverul:

- citeste linia de comanda
- decide ce operatie trebuie facuta
- porneste/foloseste o a doua conexiune TCP pentru date

---

## 2. Conexiunile de date (inspirat de FTP)

Protocolul nostru are 4 comenzi principale, care se mapeaza la FTP real astfel:

| Comanda            | Rol                     | Cine asculta pe portul de date?      |
|--------------------|-------------------------|--------------------------------------|
| `list`             | doar control (fara data)| –                                    |
| `active_get file`  | GET activ (RETR)        | clientul asculta, serverul se conecteaza |
| `active_put file`  | PUT activ (STOR)        | clientul asculta, serverul se conecteaza |
| `passive_get file` | GET pasiv (RETR)        | serverul asculta, clientul se conecteaza |
| `passive_put file` | PUT pasiv (STOR)        | serverul asculta, clientul se conecteaza |

Similar cu FTP:

- **mod activ**: serverul se conecteaza la client pe un port anuntat
- **mod pasiv**: serverul deschide port, clientul se conecteaza acolo

---

## 3. Structura transferului de date

In acest laborator, pentru simplitate:

- fiecare transfer foloseste un singur mesaj:
  - 1 octet: lungimea continutului (max ~255 bytes, este doar un exemplu didactic)
  - restul: continutul fisierului
- se foloseste `recv(BUFFER_SIZE)` si presupunem ca datele vin intr-un singur `recv`.

Aceasta abordare **nu este robusta** pentru productie, dar este suficienta
pentru a intelege ideea de protocoale de nivel aplicatie peste TCP.

---

## 4. Structura codului

### Server (`pseudo_ftp_server.py`)

- asculta pe `HOST`, `PORT` (ex. 127.0.0.1:3333) pentru conexiuni de control
- cand primeste un client:
  - porneste un thread de comenzi `handle_client_commands`
  - comanda este decodata si trimisa la `process_command`
  - in functie de comanda, se apeleaza:
    - `process_list`
    - `active_get`
    - `active_put`
    - `passive_get`
    - `passive_put`

Fisierele pe server sunt in directorul:

```text
FILE_ROOT = "./temp"
```

### Client (`pseudo_ftp_client.py`)

* se conecteaza la server pe portul de control 3333
* afiseaza un prompt `->`
* in functie de comanda introdusa:

  * pentru `list` trimite comanda si afiseaza raspunsul text
  * pentru `active_get/put`:

    * porneste un server temporar (data socket) pe client
    * anunta portul serverului
    * primeste/trimite continutul fisierului
  * pentru `passive_get/put`:

    * cere serverului un port temporar
    * se conecteaza la portul anuntat pentru a transfera fisierul

Fisierele locale ale clientului sunt in:

```text
LOCAL_STORAGE = "./client-temp"
```

## 5. Ce trebuie sa faca studentul in acest stage

* sa porneasca serverul si clientul
* sa testeze `list`, `active_get`, `active_put`, `passive_get`, `passive_put`
* sa verifice ca fisierele sunt transferate corect intre:

  * directorul serverului (`./temp`)
  * directorul clientului (`./client-temp`)
* sa completeze cateva TODO-uri simple (help, mesaje de feedback)
* sa documenteze testele in `pseudoftp_log.txt`

