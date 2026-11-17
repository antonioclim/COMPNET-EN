# Week 12 — Computer Networks
### *Rețele de Calculatoare — Săptămâna 12*

**SMTP, POP3/IMAP, MTA/MUA/MDA, RPC (JSON-RPC, XML-RPC, gRPC), Protocol Buffers**

61 questions • Bilingual EN/RO

---

## 📚 §1.  Curs / Lecture   (44 questions)

---

### Q1. `N12.C01.Q01`
**SMTP Is a Push-Only Protocol / SMTP este un protocol exclusiv de tip push**

*True / False*

> SMTP is exclusively a push protocol used for sending email. Retrieving email from a server requires a different protocol such as POP3 or IMAP. [SMTP este exclusiv un protocol de tip push, utilizat pentru trimiterea mesajelor de email. Preluarea emailurilor de pe un server necesită un protocol diferit, precum POP3 sau IMAP.]

- **a)** true
- **b)** false

<details><summary>💡 Feedback</summary>

SMTP handles only the transmission (push) of email from sender to recipient mail server. Retrieval requires POP3 (download-and-delete model) or IMAP (server-side synchronisation). An email client must be configured with two separate servers — outgoing SMTP and incoming POP3/IMAP. [SMTP gestionează exclusiv transmiterea (push) a emailurilor de la expeditor către serverul de email al destinatarului. Preluarea necesită POP3 (model descarcă-și-șterge) sau IMAP (sincronizare pe server). Un client de email trebuie configurat cu două servere separate — SMTP pentru trimitere și POP3/IMAP pentru primire.]

</details>

---

### Q2. `N12.C01.Q02`
**SMTP Response Code After DATA / Codul de răspuns SMTP după comanda DATA**

*Multiple Choice*

> After a client issues the DATA command during a valid SMTP session, what response code does the server return? [După ce un client emite comanda DATA într-o sesiune SMTP validă, ce cod de răspuns returnează serverul?]

- **a)** 354 — the server is ready to accept the message body [354 — serverul este pregătit să accepte corpul mesajului]
- **b)** 250 — the command was executed and completed successfully [250 — comanda a fost executată și finalizată cu succes]
- **c)** 220 — the SMTP service is announcing its initial greeting [220 — serviciul SMTP anunță salutul inițial]
- **d)** 221 — the server is closing the transmission channel now [221 — serverul închide canalul de transmisie acum]

<details><summary>💡 Feedback</summary>

DATA returns 354 (intermediate state) because the server transitions from command mode to data-receiving mode. The 250 code signals successful completion of a command, whilst 354 signals readiness to accept message content terminated by a lone dot on its own line. [DATA returnează 354 (stare intermediară) deoarece serverul trece din modul comandă în modul de primire a datelor. Codul 250 semnalează finalizarea cu succes a unei comenzi, în timp ce 354 semnalează pregătirea pentru acceptarea conținutului mesajului, terminat printr-un punct singular pe o linie separată.]

</details>

---

### Q3. `N12.C01.Q03`
**SMTP Command Sequence / Secvența comenzilor SMTP**

*Multiple Choice*

> Identify the correct order of SMTP commands for delivering a single email message to one recipient. [Identificați ordinea corectă a comenzilor SMTP pentru livrarea unui singur mesaj de email către un destinatar.]

- **a)** EHLO → MAIL FROM → RCPT TO → DATA → content + dot → QUIT [EHLO → MAIL FROM → RCPT TO → DATA → conținut + punct → QUIT]
- **b)** MAIL FROM → EHLO → DATA → RCPT TO → content → QUIT [MAIL FROM → EHLO → DATA → RCPT TO → conținut → QUIT]
- **c)** DATA → MAIL FROM → RCPT TO → EHLO → content + dot → QUIT [DATA → MAIL FROM → RCPT TO → EHLO → conținut + punct → QUIT]
- **d)** EHLO → DATA → MAIL FROM → RCPT TO → message content + dot → QUIT [EHLO → DATA → MAIL FROM → RCPT TO → conținut mesaj + punct → QUIT]

<details><summary>💡 Feedback</summary>

SMTP is a stateful protocol requiring a strict sequence: EHLO identifies the client, MAIL FROM sets the sender, RCPT TO sets each recipient, DATA begins the content phase, and QUIT ends the session. Skipping steps triggers a 503 Bad sequence error. [SMTP este un protocol cu stare care necesită o secvență strictă: EHLO identifică clientul, MAIL FROM stabilește expeditorul, RCPT TO stabilește fiecare destinatar, DATA începe faza de conținut, iar QUIT încheie sesiunea. Omiterea pașilor declanșează o eroare 503 Bad sequence.]

</details>

---

### Q4. `N12.C01.Q04`
**SMTP Envelope vs Message Headers / Plicul SMTP versus anteturile mesajului**

*True / False*

> In SMTP, the envelope information (MAIL FROM, RCPT TO) used for routing is separate from the message headers (From:, To:) displayed in the email client. [În SMTP, informațiile din plic (MAIL FROM, RCPT TO) utilizate pentru rutare sunt separate de anteturile mesajului (From:, To:) afișate în clientul de email.]

- **a)** true
- **b)** false

<details><summary>💡 Feedback</summary>

The SMTP envelope controls routing at the MTA level, whilst message headers are metadata displayed to the end user. These can contain entirely different addresses — a fact exploited in email spoofing. [Plicul SMTP controlează rutarea la nivelul MTA, în timp ce anteturile mesajului sunt metadate afișate utilizatorului final. Acestea pot conține adrese complet diferite — un fapt exploatat în falsificarea emailurilor.]

</details>

---

### Q5. `N12.C01.Q05`
**SMTP VRFY Command Status / Starea comenzii VRFY în SMTP**

*Multiple Choice*

> The VRFY command was designed to verify whether a given mailbox exists on the server. What is the typical status of this command on modern SMTP servers? [Comanda VRFY a fost proiectată pentru a verifica dacă o cutie poștală dată există pe server. Care este starea tipică a acestei comenzi pe serverele SMTP moderne?]

- **a)** Often disabled on production servers to prevent address harvesting by spammers [Adesea dezactivată pe serverele de producție pentru a preveni colectarea adreselor de către spammeri]
- **b)** Mandatory under RFC 5321 — every fully compliant server must unconditionally support VRFY at all times [Obligatorie conform RFC 5321 — fiecare server complet conform trebuie să suporte necondiționat VRFY în permanență]
- **c)** Replaced entirely by the NOOP command which now handles both functions [Înlocuită complet de comanda NOOP care acum gestionează ambele funcții]
- **d)** Only available after the DATA phase fully completes as a post-delivery verification step [Disponibilă doar după completarea integrală a fazei DATA ca pas de verificare post-livrare]

<details><summary>💡 Feedback</summary>

VRFY is often disabled on production SMTP servers because it can be exploited for email address harvesting by spammers. When disabled, the server typically returns a 502 or 252 response rather than confirming whether addresses exist. [VRFY este adesea dezactivată pe serverele SMTP de producție deoarece poate fi exploatată pentru colectarea adreselor de email de către spammeri. Când este dezactivată, serverul returnează de obicei un răspuns 502 sau 252 în loc să confirme existența adreselor.]

</details>

---

### Q6. `N12.C02.Q01`
**EHLO vs HELO Distinction / Diferența dintre EHLO și HELO**

*Multiple Choice*

> How does the EHLO command differ from the original HELO command in SMTP? [Cum diferă comanda EHLO de comanda originală HELO în SMTP?]

- **a)** EHLO triggers a multi-line response advertising server extensions like STARTTLS and AUTH [EHLO declanșează un răspuns pe mai multe linii care anunță extensiile serverului precum STARTTLS și AUTH]
- **b)** HELO enables TLS encryption automatically while EHLO does not support encryption [HELO activează automat criptarea TLS, în timp ce EHLO nu suportă criptarea]
- **c)** They are functionally identical — both greet the SMTP server with the same complete set of capabilities [Sunt funcțional identice — ambele salută serverul SMTP cu același set complet de capabilități]
- **d)** EHLO bypasses the authentication mechanism entirely whereas HELO always requires a valid password credential from the connecting client [EHLO ocolește complet mecanismul de autentificare, în timp ce HELO necesită întotdeauna o credențială de parolă validă de la client]

<details><summary>💡 Feedback</summary>

EHLO (Extended HELO) returns a multi-line 250 response listing available extensions such as STARTTLS, AUTH, SIZE, 8BITMIME, and PIPELINING. HELO returns a single-line greeting without extension support, limiting the session to basic RFC 821 capabilities. [EHLO (Extended HELO) returnează un răspuns 250 pe mai multe linii care listează extensiile disponibile precum STARTTLS, AUTH, SIZE, 8BITMIME și PIPELINING. HELO returnează un salut pe o singură linie fără suport pentru extensii, limitând sesiunea la capabilitățile de bază RFC 821.]

</details>

---

### Q7. `N12.C02.Q02`

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

Which registered SMTP submission port is conventionally used with STARTTLS, as distinct from implicit TLS submission on 465? [Ce port înregistrat de submission SMTP este folosit convențional cu STARTTLS, distinct de submission cu TLS implicit pe 465?]

- **a)** 587
- **b)** 25
- **c)** 465
- **d)** 443

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** 587 is the message submission port; encryption is negotiated with STARTTLS when the server supports and the policy requires it. Port 465 is the current registered submissions service using implicit TLS, not merely a legacy port. The number alone does not enable TLS or authentication. [587 este portul pentru submission; criptarea se negociază prin STARTTLS când serverul oferă suport și politica o cere. 465 este serviciul actual înregistrat submissions cu TLS implicit, nu doar un port vechi. Numărul singur nu activează TLS sau autentificarea.]

</details>

---

### Q8. `N12.C02.Q03`
**SMTP Response Code Classes / Clasele codurilor de răspuns SMTP**

*Multiple Choice*

> An SMTP server returns code 503 after a client issues DATA without first sending RCPT TO. What class of response does 503 belong to? [Un server SMTP returnează codul 503 după ce un client emite DATA fără a trimite mai întâi RCPT TO. Din ce clasă de răspunsuri face parte codul 503?]

- **a)** 5xx — permanent failure indicating the command requires a corrected sequence [5xx — eroare permanentă indicând că comanda necesită o secvență corectată]
- **b)** 4xx — temporary failure suggesting the client should retry the command later [4xx — eroare temporară sugerând că clientul ar trebui să reîncerce comanda mai târziu]
- **c)** 3xx — intermediate state meaning the server awaits additional input data [3xx — stare intermediară însemnând că serverul așteaptă date suplimentare]
- **d)** 2xx — success class confirming the operation completed without any issues [2xx — clasă de succes confirmând că operațiunea s-a finalizat fără probleme]

<details><summary>💡 Feedback</summary>

Response code 503 (Bad sequence of commands) belongs to the 5xx class — permanent failures. SMTP commands must follow a strict state-machine order: EHLO → MAIL FROM → RCPT TO → DATA. The 5xx class indicates the command cannot succeed without a fundamental change in approach. [Codul de răspuns 503 (secvență incorectă de comenzi) aparține clasei 5xx — erori permanente. Comenzile SMTP trebuie să urmeze o ordine strictă de automat finit: EHLO → MAIL FROM → RCPT TO → DATA. Clasa 5xx indică faptul că comanda nu poate reuși fără o schimbare fundamentală de abordare.]

</details>

---

### Q9. `N12.C02.Q04`
**SMTP Data Termination / Terminarea datelor SMTP**

*Multiple Choice*

> During the DATA phase of an SMTP session, how does the client signal that the message body is complete? [În timpul fazei DATA a unei sesiuni SMTP, cum semnalează clientul că corpul mesajului este complet?]

- **a)** A line containing only a single dot (CRLF.CRLF) terminates the message body [O linie care conține doar un singur punct (CRLF.CRLF) termină corpul mesajului]
- **b)** The client sends a QUIT command to indicate the message body has ended [Clientul trimite o comandă QUIT pentru a indica că corpul mesajului s-a terminat]
- **c)** An empty line with no characters signals the end of the message content [O linie goală fără caractere semnalează sfârșitul conținutului mesajului]
- **d)** The client closes the TCP connection after the final line of the body [Clientul închide conexiunea TCP după ultima linie a corpului]

<details><summary>💡 Feedback</summary>

The message body is terminated by sending a line containing only a single dot (period) preceded by CRLF. This is the . sequence. The server then returns 250 to confirm acceptance. Lines in the body that start with a dot are dot-stuffed (an extra dot is prepended). [Corpul mesajului se termină prin trimiterea unei linii care conține doar un singur punct, precedat de CRLF. Aceasta este secvența .. Serverul returnează apoi 250 pentru a confirma acceptarea. Liniile din corp care încep cu un punct sunt dot-stuffed (un punct suplimentar este adăugat la început).]

</details>

---

### Q10. `N12.C02.Q05`
**Bad Sequence Error in SMTP / Eroare de secvență greșită în SMTP**

*Multiple Choice*

> A client sends the DATA command immediately after establishing a TCP connection, before issuing EHLO or MAIL FROM. What response code does the server return? [Un client trimite comanda DATA imediat după stabilirea conexiunii TCP, înainte de a emite EHLO sau MAIL FROM. Ce cod de răspuns returnează serverul?]

- **a)** 503 Bad sequence of commands — DATA requires prior EHLO, MAIL FROM, and RCPT TO steps [503 Secvență greșită de comenzi — DATA necesită pașii anteriori EHLO, MAIL FROM și RCPT TO]
- **b)** 354 Start mail input — the server accepts DATA regardless of prior command state [354 Începeți introducerea mailului — serverul acceptă DATA indiferent de starea comenzilor anterioare]
- **c)** 220 Service ready — the server resets its state and starts a fresh mail transaction [220 Serviciu pregătit — serverul își resetează starea și începe o tranzacție nouă]
- **d)** 500 Syntax error — DATA itself is not recognised as a valid SMTP command keyword [500 Eroare de sintaxă — DATA în sine nu este recunoscută ca un cuvânt cheie SMTP valid]

<details><summary>💡 Feedback</summary>

SMTP requires commands in a specific order: EHLO → MAIL FROM → RCPT TO → DATA. Sending DATA out of sequence triggers a 503 (Bad sequence of commands) error because the server enforces the state machine transitions strictly. [SMTP necesită comenzi într-o ordine specifică: EHLO → MAIL FROM → RCPT TO → DATA. Trimiterea DATA în afara secvenței declanșează o eroare 503 (secvență de comenzi greșită) deoarece serverul impune tranzițiile mașinii de stare în mod strict.]

</details>

---

### Q11. `N12.C03.Q01`

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

Alice sends mail from a desktop mail client configured for SMTP. Bob reads the delivered message through Gmail in a web browser. Which client-facing protocols are stated by this scenario? [Alice trimite email dintr-un client desktop configurat pentru SMTP. Bob citește mesajul livrat prin Gmail în browser. Ce protocoale către clienți sunt precizate de scenariu?]

- **a)** SMTP for Alice’s submission and HTTPS for Bob’s browser access. [SMTP pentru trimiterea lui Alice și HTTPS pentru accesul lui Bob în browser.]
- **b)** FTP for submission and mandatory POP3 inside Bob’s browser. [FTP pentru trimitere și POP3 obligatoriu în browserul lui Bob.]
- **c)** IMAP must be used between Gmail’s internal components. [IMAP trebuie folosit între componentele interne Gmail.]

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** SMTP handles mail submission and inter-server relay. Browser access uses HTTPS. This scenario does not establish how the provider’s internal mail storage is accessed; do not infer IMAP or POP3 from webmail use. [SMTP gestionează submission și releul între servere. Accesul prin browser folosește HTTPS. Scenariul nu stabilește cum este accesată stocarea internă a furnizorului; folosirea webmailului nu permite deducerea IMAP sau POP3.]

</details>

---

### Q12. `N12.C03.Q02`
**MTA, MUA, MDA Roles / Rolurile MTA, MUA, MDA**

*Multiple Choice*

> Which component in the email architecture is responsible for transferring messages between mail servers? [Care componentă din arhitectura de email este responsabilă pentru transferul mesajelor între serverele de email?]

- **a)** MTA (Mail Transfer Agent) — routes email messages between servers via SMTP relay [MTA (Mail Transfer Agent) — dirijează mesajele de email între servere prin releu SMTP]
- **b)** MUA (Mail User Agent) — the email client used for reading and composing [MUA (Mail User Agent) — clientul de email utilizat pentru citire și compunere]
- **c)** MDA (Mail Delivery Agent) — places incoming mail into the recipient local mailbox [MDA (Mail Delivery Agent) — plasează emailul primit în căsuța locală a destinatarului]
- **d)** DNS resolver — translates the recipient domain into a server IP address [Resolver-ul DNS — traduce domeniul destinatarului într-o adresă IP a serverului]

<details><summary>💡 Feedback</summary>

The MTA (Mail Transfer Agent) handles server-to-server message transfer using SMTP. The MUA (Mail User Agent) is the client application, and the MDA (Mail Delivery Agent) handles final delivery to the local mailbox. [MTA (Mail Transfer Agent) gestionează transferul mesajelor între servere folosind SMTP. MUA (Mail User Agent) este aplicația client, iar MDA (Mail Delivery Agent) gestionează livrarea finală în căsuța poștală locală.]

</details>

---

### Q13. `N12.C03.Q03`
**POP3 vs IMAP / POP3 versus IMAP**

*Multiple Choice*

> A student checks email from both a laptop and a phone. Which retrieval protocol best supports multi-device synchronisation? [Un student verifică emailul atât de pe laptop, cât și de pe telefon. Care protocol de preluare suportă cel mai bine sincronizarea pe mai multe dispozitive?]

- **a)** IMAP — keeps messages on the server and synchronises across all devices [IMAP — păstrează mesajele pe server și sincronizează pe toate dispozitivele]
- **b)** POP3 — downloads messages and removes them from the server after retrieval [POP3 — descarcă mesajele și le elimină de pe server după preluare]
- **c)** SMTP — manages both sending and receiving for maximum simplicity [SMTP — gestionează atât trimiterea, cât și primirea pentru simplitate maximă]

<details><summary>💡 Feedback</summary>

IMAP (port 143/993) maintains messages on the server, supports folders, flags, and partial retrieval — ideal for multi-device access. POP3 (port 110/995) follows a download-and-delete model better suited for single-device use. [IMAP (portul 143/993) menține mesajele pe server, suportă foldere, steaguri și preluare parțială — ideal pentru acces de pe mai multe dispozitive. POP3 (portul 110/995) urmează un model descarcă-și-șterge mai potrivit pentru utilizarea pe un singur dispozitiv.]

</details>

---

### Q14. `N12.C03.Q04`
**POP3 State Progression / Progresia stărilor POP3**

*Multiple Choice*

> POP3 sessions progress through three ordered states. Identify the correct state progression for a POP3 connection. [Sesiunile POP3 progresează prin trei stări ordonate. Identificați progresia corectă a stărilor pentru o conexiune POP3.]

- **a)** AUTHORIZATION → TRANSACTION → UPDATE [AUTHORIZATION → TRANSACTION → UPDATE]
- **b)** TRANSACTION → AUTHORIZATION → UPDATE [TRANSACTION → AUTHORIZATION → UPDATE]
- **c)** AUTHORIZATION → UPDATE → TRANSACTION [AUTHORIZATION → UPDATE → TRANSACTION]

<details><summary>💡 Feedback</summary>

POP3 defines three states: AUTHORIZATION (user logs in), TRANSACTION (user reads/deletes messages), and UPDATE (server applies deletions and closes). This strict ordering ensures atomic operations on the mailbox. [POP3 definește trei stări: AUTHORIZATION (utilizatorul se autentifică), TRANSACTION (utilizatorul citește/șterge mesaje) și UPDATE (serverul aplică ștergerile și închide). Această ordonare strictă asigură operații atomice asupra cutiei poștale.]

</details>

---

### Q15. `N12.C04.Q01`
**Client Stub Role in RPC / Rolul stub-ului client în RPC**

*Multiple Choice*

> What is the primary role of the client stub in an RPC architecture? [Care este rolul principal al stub-ului client într-o arhitectură RPC?]

- **a)** Serialise parameters into a wire format and send the request over the network [Serializează parametrii într-un format de rețea și trimite cererea prin rețea]
- **b)** Execute the requested procedure directly on the server's operating system [Execută procedura cerută direct pe sistemul de operare al serverului]
- **c)** Store a persistent cache of all previous remote procedure call results [Stochează un cache persistent al tuturor rezultatelor anterioare de apeluri RPC]
- **d)** Authenticate the client identity using TLS certificate exchange with server [Autentifică identitatea clientului folosind schimb de certificate TLS cu serverul]

<details><summary>💡 Feedback</summary>

The client stub (proxy) serialises (marshalls) the method name and parameters into a network-transmittable format, sends the request over the transport layer, receives the response, and deserialises (unmarshalls) the result — hiding all network complexity from the calling application. [Stub-ul client (proxy) serializează (marshall) numele metodei și parametrii într-un format transmisibil prin rețea, trimite cererea prin stratul de transport, primește răspunsul și deserializează (unmarshall) rezultatul — ascunzând toată complexitatea rețelei de aplicația apelantă.]

</details>

---

### Q16. `N12.C04.Q02`
**RPC Components / Componentele RPC**

*Multiple Choice*

> Which set of components correctly describes the basic RPC call chain? [Care set de componente descrie corect lanțul de bază al unui apel RPC?]

- **a)** Client app → Client stub → Transport → Server stub → Server app [Aplicația client → Stub client → Transport → Stub server → Aplicația server]
- **b)** Client app → DNS lookup → HTTP proxy → Server app directly [Aplicația client → Căutare DNS → Proxy HTTP → Aplicația server direct]
- **c)** Client stub → Server stub → Transport → Client app → Server app [Stub client → Stub server → Transport → Aplicația client → Aplicația server]
- **d)** Transport layer → Client stub → Server app → Server stub → Client app [Stratul transport → Stub client → Aplicația server → Stub server → Aplicația client]

<details><summary>💡 Feedback</summary>

An RPC call flows through: client application → client stub (serialises) → transport (sends bytes) → server stub (deserialises) → server application (executes). The return path reverses this chain. [Un apel RPC parcurge: aplicația client → stub-ul client (serializează) → transport (trimite octeți) → stub-ul server (deserializează) → aplicația server (execută). Calea de întoarcere inversează acest lanț.]

</details>

---

### Q17. `N12.C04.Q03`
**RPC Can Be Asynchronous / RPC poate fi asincron**

*True / False*

> Remote Procedure Calls are always synchronous — the client must block and wait until the server returns a response before continuing execution. [Apelurile de procedură la distanță sunt întotdeauna sincrone — clientul trebuie să blocheze și să aștepte până când serverul returnează un răspuns înainte de a continua execuția.]

- **a)** true
- **b)** false

<details><summary>💡 Feedback</summary>

RPC can be synchronous or asynchronous. JSON-RPC supports notifications (requests without an id field that expect no response). gRPC supports server streaming, client streaming, and bidirectional streaming. Modern libraries offer async/await patterns. [RPC poate fi sincron sau asincron. JSON-RPC suportă notificări (cereri fără câmpul id care nu așteaptă răspuns). gRPC suportă streaming de la server, streaming de la client și streaming bidirecțional. Bibliotecile moderne oferă modele async/await.]

</details>

---

### Q18. `N12.C04.Q04`
**RPC Serialisation Layer / Stratul de serializare RPC**

*True / False*

> In the RPC architecture, the serialisation layer is responsible for converting function parameters into a byte representation suitable for network transmission and reconstructing them on the other side. [În arhitectura RPC, stratul de serializare este responsabil pentru conversia parametrilor funcției într-o reprezentare de octeți adecvată transmisiei în rețea și reconstruirea lor pe cealaltă parte.]

- **a)** true
- **b)** false

<details><summary>💡 Feedback</summary>

Serialisation (also called marshalling) converts in-memory objects to a wire format (JSON, XML, Protocol Buffers). Deserialisation (unmarshalling) reverses the process. Both client and server stubs perform these operations on their respective ends. [Serializarea (numită și marshalling) convertește obiectele din memorie într-un format de transmisie (JSON, XML, Protocol Buffers). Deserializarea (unmarshalling) inversează procesul. Atât stub-ul client cât și cel server efectuează aceste operații pe părțile lor respective.]

</details>

---

### Q19. `N12.C05.Q01`

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

The supplied S12 JSON-RPC HTTP server receives a valid request with id 1 for an unknown method. Which response does this implementation produce? [Serverul HTTP JSON-RPC S12 distribuit primește o cerere validă cu id 1 pentru o metodă necunoscută. Ce răspuns produce implementarea?]

- **a)** HTTP 200 with a JSON-RPC error object carrying code -32601 and id 1. [HTTP 200 cu un obiect de eroare JSON-RPC cu codul -32601 și id 1.]
- **b)** HTTP 404 is mandated by JSON-RPC itself. [HTTP 404 este impus de JSON-RPC însuși.]
- **c)** HTTP 405 because the JSON-RPC method name is an HTTP verb. [HTTP 405 deoarece numele metodei JSON-RPC este un verb HTTP.]

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** This is the HTTP mapping chosen by S12_Part01_Script_JSONRPC_Server.py. JSON-RPC 2.0 is transport-agnostic and does not prescribe HTTP status codes. The response preserves the valid request id and contains error, not result. [Aceasta este maparea HTTP aleasă de S12_Part01_Script_JSONRPC_Server.py. JSON-RPC 2.0 este independent de transport și nu prescrie codurile HTTP. Răspunsul păstrează id-ul valid și conține error, nu result.]

</details>

---

### Q20. `N12.C05.Q02`
**JSON-RPC Notification / Notificarea JSON-RPC**

*Multiple Choice*

> In JSON-RPC 2.0, what makes a request a notification rather than a standard call? [În JSON-RPC 2.0, ce face dintr-o cerere o notificare în loc de un apel standard?]

- **a)** The absence of the "id" field — the server processes silently without responding [Absența câmpului "id" — serverul procesează în tăcere fără a răspunde]
- **b)** Setting the "method" field to "notify" instructs the server to skip responses [Setarea câmpului "method" la "notify" instruiește serverul să omită răspunsurile]
- **c)** Including a special "notification": true flag alongside the standard fields [Includerea unui steag special "notification": true alături de câmpurile standard]
- **d)** Using HTTP DELETE instead of POST changes the semantics to notification mode [Utilizarea HTTP DELETE în loc de POST schimbă semantica la modul notificare]

<details><summary>💡 Feedback</summary>

A notification is a JSON-RPC request that omits the "id" field. The server processes it but does not send any response. This is useful for fire-and-forget operations where the client does not need confirmation. [O notificare este o cerere JSON-RPC care omite câmpul "id". Serverul o procesează dar nu trimite niciun răspuns. Aceasta este utilă pentru operațiuni de tip fire-and-forget unde clientul nu are nevoie de confirmare.]

</details>

---

### Q21. `N12.C05.Q03`
**JSON-RPC Batch Requests / Cereri JSON-RPC în lot**

*Multiple Choice*

> How are batch requests sent in JSON-RPC 2.0? [Cum se trimit cererile în lot în JSON-RPC 2.0?]

- **a)** As a JSON array of request objects sent within a single HTTP POST request body [Ca un tablou JSON de obiecte de cerere trimis într-un singur corp de cerere HTTP POST]
- **b)** By opening multiple parallel TCP connections each carrying a single request [Prin deschiderea mai multor conexiuni TCP paralele fiecare purtând o singură cerere]
- **c)** By including a batch-size header that tells the server how many follow [Prin includerea unui antet batch-size care spune serverului câte urmează]

<details><summary>💡 Feedback</summary>

A batch request is an array of JSON-RPC request objects sent in a single HTTP POST. The server returns an array of responses (one per request that has an id). Mixed results are possible — some calls succeed while others fail. [O cerere în lot este un tablou de obiecte de cerere JSON-RPC trimise într-un singur HTTP POST. Serverul returnează un tablou de răspunsuri (câte unul pentru fiecare cerere care are un id). Sunt posibile rezultate mixte — unele apeluri reușesc în timp ce altele eșuează.]

</details>

---

### Q22. `N12.C05.Q04`
**JSON-RPC Standard Error Codes / Codurile standard de eroare JSON-RPC**

*Multiple Choice*

> What does the JSON-RPC error code -32601 indicate? [Ce indică codul de eroare JSON-RPC -32601?]

- **a)** Method not found — the requested remote procedure does not exist on this server [Metodă negăsită — procedura de la distanță cerută nu există pe acest server]
- **b)** Parse error — the JSON payload was malformed and could not be decoded [Eroare de parsare — corpul JSON a fost malformat și nu a putut fi decodat]
- **c)** Invalid params — the arguments supplied do not match the method signature [Parametri invalizi — argumentele furnizate nu corespund semnăturii metodei]
- **d)** Internal error — an unexpected server condition prevented execution [Eroare internă — o condiție neașteptată a serverului a împiedicat execuția]

<details><summary>💡 Feedback</summary>

Error code -32601 means Method not found. The standard error codes range from -32700 (Parse error) through -32603 (Internal error), with -32000 to -32099 reserved for server-defined application errors. [Codul de eroare -32601 înseamnă Method not found (Metodă negăsită). Codurile standard de eroare variază de la -32700 (Parse error) până la -32603 (Internal error), cu -32000 până la -32099 rezervate pentru erori de aplicație definite de server.]

</details>

---

### Q23. `N12.C05.Q05`
**XML-RPC Transport and Format / Transportul și formatul XML-RPC**

*Multiple Choice*

> Which statement about XML-RPC is correct? [Care afirmație despre XML-RPC este corectă?]

- **a)** XML-RPC transmits over HTTP using XML serialisation and remains in active use in legacy systems [XML-RPC transmite prin HTTP folosind serializare XML și rămâne în utilizare activă în sisteme vechi]
- **b)** XML-RPC has been completely deprecated and officially replaced by JSON-RPC in all existing software and legacy systems [XML-RPC a fost complet depreciat și înlocuit oficial de JSON-RPC în toate programele existente și sistemele vechi]
- **c)** XML-RPC uses binary encoding similar to Protocol Buffers for efficient network transmission [XML-RPC folosește codificare binară similară cu Protocol Buffers pentru transmisie eficientă în rețea]
- **d)** XML-RPC requires HTTP/2 with multiplexing to handle concurrent method invocations [XML-RPC necesită HTTP/2 cu multiplexare pentru a gestiona invocări simultane de metode]

<details><summary>💡 Feedback</summary>

XML-RPC uses XML for serialisation over HTTP. It predates JSON-RPC and is still actively used in systems like WordPress (xmlrpc.php), Supervisord, and Bugzilla. It supports introspection via system.listMethods, system.methodSignature, and system.methodHelp. [XML-RPC folosește XML pentru serializare prin HTTP. Precedă JSON-RPC și este încă utilizat activ în sisteme precum WordPress (xmlrpc.php), Supervisord și Bugzilla. Suportă introspecție prin system.listMethods, system.methodSignature și system.methodHelp.]

</details>

---

### Q24. `N12.C05.Q06`
**XML-RPC Introspection Capability / Capabilitatea de introspecție XML-RPC**

*Multiple Choice*

> XML-RPC defines a set of introspection methods that allow clients to discover what operations a server supports at runtime. Which method returns the list of all available procedures? [XML-RPC definește un set de metode de introspecție care permit clienților să descopere ce operații suportă un server în timpul execuției. Ce metodă returnează lista tuturor procedurilor disponibile?]

- **a)** system.listMethods — returns an array of all method names the server exposes [system.listMethods — returnează un array cu numele tuturor metodelor pe care le expune serverul]
- **b)** system.methodSignature — returns the type signatures of all available procedures [system.methodSignature — returnează semnăturile de tip ale tuturor procedurilor disponibile]
- **c)** system.methodHelp — returns human-readable documentation for all server methods [system.methodHelp — returnează documentație lizibilă pentru toate metodele serverului]
- **d)** system.describe — auto-generates a WSDL-like description of the entire API surface [system.describe — generează automat o descriere de tip WSDL a întregii suprafețe API]

<details><summary>💡 Feedback</summary>

XML-RPC provides three introspection methods: system.listMethods (lists all methods), system.methodSignature (returns parameter types), and system.methodHelp (returns documentation text). These are optional but widely implemented. [XML-RPC oferă trei metode de introspecție: system.listMethods (listează toate metodele), system.methodSignature (returnează tipurile parametrilor) și system.methodHelp (returnează textul documentației). Acestea sunt opționale, dar implementate pe scară largă.]

</details>

---

### Q25. `N12.C06.Q01`
**Protocol Buffers Are Not Compressed JSON / Protocol Buffers nu sunt JSON comprimat**

*Multiple Choice*

> How does Protocol Buffers (protobuf) differ from JSON as a serialisation format? [Cum diferă Protocol Buffers (protobuf) de JSON ca format de serializare?]

- **a)** Protobuf uses a binary schema-defined format with field numbers, not a text format with string keys [Protobuf folosește un format binar definit prin schemă cu numere de câmp, nu un format text cu chei string]
- **b)** Protobuf applies gzip compression to JSON payloads for smaller wire size [Protobuf aplică compresie gzip la corpuri JSON pentru dimensiune mai mică pe rețea]
- **c)** Protobuf minifies the JSON keys to single characters while keeping the same underlying data structure intact [Protobuf minimizează cheile JSON la caractere unice păstrând aceeași structură de date subiacentă intactă]
- **d)** Protobuf and JSON produce identical wire formats underneath, but protobuf adds optional compile-time type checks for strict validation [Protobuf și JSON produc formate de rețea identice pe dedesubt, dar protobuf adaugă verificări opționale de tip la compilare pentru validare strictă]

<details><summary>💡 Feedback</summary>

Protocol Buffers is a completely different binary format — not compressed JSON. It uses numeric field tags (1, 2, …) instead of string keys, wire types for encoding (varint, 64-bit, length-delimited), and requires a .proto schema. You cannot read protobuf data as text. [Protocol Buffers este un format binar complet diferit — nu este JSON comprimat. Folosește etichete de câmp numerice (1, 2, …) în loc de chei de tip string, tipuri de codificare (varint, 64-bit, length-delimited) și necesită o schemă .proto. Nu puteți citi datele protobuf ca text.]

</details>

---

### Q26. `N12.C06.Q02`
**gRPC Transport Protocol / Protocolul de transport gRPC**

*Multiple Choice*

> Which transport protocol does gRPC use, and what advantage does it provide? [Ce protocol de transport folosește gRPC și ce avantaj oferă acesta?]

- **a)** HTTP/2 — enabling multiplexed streams, header compression, and efficient bidirectional communication [HTTP/2 — permițând fluxuri multiplexate, compresie a anteturilor și comunicare bidirecțională eficientă]
- **b)** HTTP/1.1 — maintaining full backwards compatibility with all existing web infrastructure and proxies [HTTP/1.1 — menținând compatibilitatea completă cu toată infrastructura web existentă și proxy-urile existente]
- **c)** Raw TCP sockets — bypassing HTTP entirely for maximum throughput and minimal latency [Socket-uri TCP brute — ocolind HTTP complet pentru debit maxim și latență minimă]
- **d)** WebSocket — enabling persistent bidirectional connections through browser-compatible channels with frame-based messaging [WebSocket — permițând conexiuni bidirecționale persistente prin canale compatibile cu browserul cu mesagerie bazată pe cadre]

<details><summary>💡 Feedback</summary>

gRPC uses HTTP/2, which provides multiplexing (multiple concurrent streams over one TCP connection), header compression, and server push. This contrasts with JSON-RPC and XML-RPC which typically use HTTP/1.1. [gRPC folosește HTTP/2, care oferă multiplexare (mai multe fluxuri concurente peste o singură conexiune TCP), compresie a anteturilor și server push. Aceasta contrastează cu JSON-RPC și XML-RPC care folosesc de obicei HTTP/1.1.]

</details>

---

### Q27. `N12.C06.Q03`
**gRPC Streaming Types / Tipurile de streaming gRPC**

*Multiple Choice*

> The S12_Part02_Config_Calculator.proto in the Week 12 lab defines unary RPCs. gRPC also supports three additional communication patterns. Which set correctly lists them? [Fișierul S12_Part02_Config_Calculator.proto din laboratorul Săptămânii 12 definește RPC-uri unare. gRPC suportă și alte trei modele de comunicare. Care set le listează corect?]

- **a)** Server streaming, client streaming, and bidirectional streaming [Streaming de la server, streaming de la client și streaming bidirecțional]
- **b)** Broadcast, multicast, and publish-subscribe event-driven messaging patterns [Broadcast, multicast și modele de mesagerie publish-subscribe bazate pe evenimente]
- **c)** Polling, long-polling, and server-sent event notification mechanisms [Polling, long-polling și mecanisme de notificare prin server-sent events]

<details><summary>💡 Feedback</summary>

gRPC supports four patterns: unary (single request/response), server streaming (one request, stream of responses), client streaming (stream of requests, one response), and bidirectional streaming (streams in both directions simultaneously). [gRPC suportă patru modele: unar (cerere/răspuns unic), streaming de la server (o cerere, flux de răspunsuri), streaming de la client (flux de cereri, un răspuns) și streaming bidirecțional (fluxuri în ambele direcții simultan).]

</details>

---

### Q28. `N12.C07.Q01`
**Protocol Selection for Mobile Backend / Selectarea protocolului pentru backend mobil**

*Multiple Choice*

> You are designing an API for a mobile banking application with limited bandwidth. Which RPC protocol is most suitable? [Proiectați un API pentru o aplicație bancară mobilă cu lățime de bandă limitată. Care protocol RPC este cel mai potrivit?]

- **a)** gRPC — bandwidth-efficient binary encoding with strong type contracts and code generation [gRPC — codificare binară eficientă ca lățime de bandă cu contracte de tip puternice și generare de cod]
- **b)** JSON-RPC — human-readable format that is ideal for debugging during mobile app development [JSON-RPC — format uman-lizibil care este ideal pentru depanare în timpul dezvoltării aplicației mobile]
- **c)** XML-RPC — self-describing payloads with built-in method introspection for service discovery and compatibility [XML-RPC — corpuri auto-descriptive cu introspecție integrată a metodelor pentru descoperirea serviciilor și compatibilitate]

<details><summary>💡 Feedback</summary>

gRPC with Protocol Buffers offers the smallest payload sizes (binary encoding), strong type contracts via .proto files, built-in code generation for mobile platforms, and HTTP/2 multiplexing for efficient use of bandwidth. [gRPC cu Protocol Buffers oferă cele mai mici dimensiuni ale corpului (codificare binară), contracte de tip puternice prin fișiere .proto, generare automată de cod pentru platforme mobile și multiplexare HTTP/2 pentru utilizare eficientă a lățimii de bandă.]

</details>

---

### Q29. `N12.C07.Q02`
**Payload Size Comparison / Compararea dimensiunii corpului**

*Multiple Choice*

> For the operation add(10, 32), rank the three RPC protocols from smallest to largest payload size. [Pentru operația add(10, 32), clasificați cele trei protocoale RPC de la cel mai mic la cel mai mare corp.]

- **a)** gRPC (≈18 bytes) → JSON-RPC (≈56 bytes) → XML-RPC (≈195 bytes) [gRPC (≈18 octeți) → JSON-RPC (≈56 octeți) → XML-RPC (≈195 octeți)]
- **b)** JSON-RPC (≈18 bytes) → gRPC (≈56 bytes) → XML-RPC (≈195 bytes) [JSON-RPC (≈18 octeți) → gRPC (≈56 octeți) → XML-RPC (≈195 octeți)]
- **c)** XML-RPC (≈18 bytes) → JSON-RPC (≈56 bytes) → gRPC (≈195 bytes) [XML-RPC (≈18 octeți) → JSON-RPC (≈56 octeți) → gRPC (≈195 octeți)]
- **d)** All three produce payloads of similar size since they encode the same data [Toate trei produc corpuri de dimensiuni similare deoarece codifică aceleași date]

<details><summary>💡 Feedback</summary>

Protocol Buffers (gRPC) produces approximately 18 bytes (binary). JSON-RPC produces approximately 56 bytes (text JSON). XML-RPC produces approximately 195 bytes (verbose XML tags). The ratio is roughly 1:3:11. [Protocol Buffers (gRPC) produce aproximativ 18 octeți (binar). JSON-RPC produce aproximativ 56 octeți (text JSON). XML-RPC produce aproximativ 195 octeți (etichete XML verbose). Raportul este aproximativ 1:3:11.]

</details>

---

### Q30. `N12.C07.Q03`
**JSON-RPC Is Transport Agnostic / JSON-RPC este agnostic față de transport**

*Multiple Choice*

> A colleague claims JSON-RPC can only work over HTTP. Is this claim accurate? [Un coleg susține că JSON-RPC funcționează doar prin HTTP. Este această afirmație exactă?]

- **a)** Incorrect — JSON-RPC is transport agnostic and works over HTTP, WebSocket, TCP, and other channels [Inexact — JSON-RPC este agnostic față de transport și funcționează prin HTTP, WebSocket, TCP și alte canale]
- **b)** Correct — the JSON-RPC 2.0 specification explicitly mandates HTTP POST as the only valid and officially supported transport method [Exact — specificația JSON-RPC 2.0 mandatează explicit HTTP POST ca singura metodă de transport validă și oficial suportată]
- **c)** Partially correct — JSON-RPC works only over HTTP and WebSocket, no other transport protocols exist [Parțial exact — JSON-RPC funcționează doar prin HTTP și WebSocket, fără alte protocoale de transport disponibile]

<details><summary>💡 Feedback</summary>

JSON-RPC is transport agnostic by specification — it defines only the message format, not the transport. It works over HTTP, WebSocket, raw TCP, Unix sockets, and even serial/UART connections. [JSON-RPC este agnostic față de transport conform specificației — definește doar formatul mesajului, nu transportul. Funcționează prin HTTP, WebSocket, TCP brut, socket-uri Unix și chiar conexiuni seriale/UART.]

</details>

---

### Q31. `N12.T00.Q01`
**Scenario: Choosing Between SMTP and IMAP / Scenariu: Alegerea între SMTP și IMAP**

*Multiple Choice*

> A network administrator configures a new email server. The server must accept incoming email from external domains. Which protocol should the server's inbound listener use? [Un administrator de rețea configurează un nou server de email. Serverul trebuie să accepte email din domenii externe. Ce protocol ar trebui să folosească listener-ul de intrare al serverului?]

- **a)** SMTP on port 25 to receive pushed messages from remote mail transfer agents [SMTP pe portul 25 pentru a primi mesaje trimise de la agenți de transfer de email la distanță]
- **b)** IMAP on port 143 because clients will eventually retrieve their email using it [IMAP pe portul 143 deoarece clienții vor prelua în cele din urmă emailul folosindu-l]
- **c)** POP3 on port 110 as the simplest protocol for handling all incoming delivery [POP3 pe portul 110 ca cel mai simplu protocol pentru gestionarea întregii livrări de intrare]
- **d)** HTTP on port 80 because modern email is delivered entirely through web services [HTTP pe portul 80 deoarece emailul modern este livrat în întregime prin servicii web]

<details><summary>💡 Feedback</summary>

SMTP is the protocol for receiving email at the MTA level. External servers push email via SMTP to port 25. IMAP/POP3 are client-facing retrieval protocols, not for inter-server delivery. [SMTP este protocolul pentru primirea emailului la nivelul MTA. Serverele externe trimit email prin SMTP pe portul 25. IMAP/POP3 sunt protocoale de preluare pentru clienți, nu pentru livrare între servere.]

</details>

---

### Q32. `N12.T00.Q02`
**Scenario: Debugging a Failed RPC Call / Scenariu: Depanarea unui apel RPC eșuat**

*Multiple Choice*

> A developer calls a JSON-RPC method and receives HTTP 200 but the response contains {"error":{"code":-32601,...}}. What happened? [Un dezvoltator apelează o metodă JSON-RPC și primește HTTP 200 dar răspunsul conține {"error":{"code":-32601,...}}. Ce s-a întâmplat?]

- **a)** The HTTP transport succeeded but the requested RPC method does not exist on the server [Transportul HTTP a reușit dar metoda RPC cerută nu există pe server]
- **b)** The server experienced an internal crash while trying to locate the method handler [Serverul a suferit o cădere internă în timp ce încerca să localizeze handler-ul metodei]
- **c)** The network connection was interrupted mid-request causing a partial response [Conexiunea de rețea a fost întreruptă la mijlocul cererii cauzând un răspuns parțial]
- **d)** The client used the wrong HTTP method — GET instead of POST for the RPC call [Clientul a folosit metoda HTTP greșită — GET în loc de POST pentru apelul RPC]

<details><summary>💡 Feedback</summary>

HTTP 200 means the transport succeeded. The JSON-RPC error -32601 (Method not found) means the method name was not registered on the server. The developer should check the method name spelling or the server's available methods. [HTTP 200 înseamnă că transportul a reușit. Eroarea JSON-RPC -32601 (Method not found) înseamnă că numele metodei nu a fost înregistrat pe server. Dezvoltatorul ar trebui să verifice ortografia numelui metodei sau metodele disponibile pe server.]

</details>

---

### Q33. `N12.T00.Q03`
**Scenario: Microservices Architecture / Scenariu: Arhitectură de microservicii**

*Multiple Choice*

> A team builds an internal microservice mesh handling 10,000 requests/second. Human readability of payloads is not required. Which RPC framework optimises for this use case? [O echipă construiește o rețea internă de microservicii care gestionează 10.000 cereri/secundă. Lizibilitatea umană a corpurilor nu este necesară. Care framework RPC se optimizează pentru acest caz de utilizare?]

- **a)** gRPC — binary Protocol Buffers minimise payload size while HTTP/2 maximises throughput [gRPC — Protocol Buffers binar minimizează dimensiunea corpului în timp ce HTTP/2 maximizează debitul]
- **b)** JSON-RPC — human-readable format allows easier debugging of high-volume traffic flows [JSON-RPC — formatul uman-lizibil permite depanarea mai ușoară a fluxurilor de trafic de mare volum]
- **c)** XML-RPC — self-describing XML provides robust introspection for service mesh routing [XML-RPC — XML-ul auto-descriptiv oferă introspecție robustă pentru rutarea rețelei de servicii]
- **d)** SMTP — proven reliability for message delivery makes it suitable for service calls [SMTP — fiabilitatea dovedită pentru livrarea mesajelor îl face potrivit pentru apeluri de servicii]

<details><summary>💡 Feedback</summary>

gRPC with Protocol Buffers provides: smallest payloads (binary), HTTP/2 multiplexing, strong contracts via .proto, built-in code generation, and streaming support — ideal for high-throughput internal services. [gRPC cu Protocol Buffers oferă: cele mai mici corpuri (binar), multiplexare HTTP/2, contracte puternice prin .proto, generare automată de cod și suport de streaming — ideal pentru servicii interne cu debit mare.]

</details>

---

### Q34. `N12.T00.Q04`
**Scenario: DATA Command Misconception / Scenariu: Concepția greșită despre comanda DATA**

*Multiple Choice*

> A student writes SMTP parsing code that checks for response 250 after every command. During testing, the parser breaks after DATA. Why? [Un student scrie cod de parsare SMTP care verifică răspunsul 250 după fiecare comandă. În timpul testării, parser-ul se blochează după DATA. De ce?]

- **a)** DATA returns 354 (intermediate), not 250 — the parser only checks for a single success code [DATA returnează 354 (intermediar), nu 250 — parser-ul verifică doar un singur cod de succes]
- **b)** The SMTP server rejected the DATA command because authentication was not enabled [Serverul SMTP a respins comanda DATA deoarece autentificarea nu era activată]
- **c)** A network timeout caused the server to drop the connection before returning a code [Un timeout de rețea a cauzat întreruperea conexiunii de către server înainte de a returna un cod]
- **d)** The student forgot to send RCPT TO before DATA causing a 503 sequencing error [Studentul a uitat să trimită RCPT TO înainte de DATA cauzând o eroare de secvență 503]

<details><summary>💡 Feedback</summary>

DATA returns 354 (intermediate state), not 250. The parser must handle different response code classes: 2xx for success, 3xx for intermediate, 4xx/5xx for errors. Hard-coding 250 for all commands is incorrect. [DATA returnează 354 (stare intermediară), nu 250. Parser-ul trebuie să gestioneze diferite clase de coduri de răspuns: 2xx pentru succes, 3xx pentru intermediar, 4xx/5xx pentru erori. Codificarea fixă a lui 250 pentru toate comenzile este incorectă.]

</details>

---

### Q35. `N12.T00.Q05`
**Scenario: Protobuf vs JSON Debugging / Scenariu: Depanare protobuf vs JSON**

*Multiple Choice*

> A developer captures gRPC traffic in Wireshark but cannot read the payload. A colleague suggests switching to JSON-RPC for the same operation. What explains the difference? [Un dezvoltator capturează traficul gRPC în Wireshark dar nu poate citi corpul. Un coleg sugerează trecerea la JSON-RPC pentru aceeași operație. Ce explică diferența?]

- **a)** Protocol Buffers encode data as binary — you need the .proto schema to decode it in Wireshark [Protocol Buffers codifică datele ca binar — aveți nevoie de schema .proto pentru a le decoda în Wireshark]
- **b)** gRPC encrypts all payloads with TLS by default making them unreadable to any packet sniffers [gRPC criptează toate corpurile cu TLS implicit făcându-le ilizibile pentru orice analizoare de pachete]
- **c)** The traffic was captured on the wrong Wireshark interface and contains unrelated packets [Traficul a fost capturat pe interfața Wireshark greșită și conține pachete nerelevante]
- **d)** gRPC compresses JSON payloads with gzip before transmission over the HTTP/2 transport [gRPC comprimă corpurile JSON cu gzip înainte de transmisia prin transportul HTTP/2]

<details><summary>💡 Feedback</summary>

gRPC uses binary Protocol Buffers which are not human-readable without the .proto schema. JSON-RPC uses text JSON which appears as readable ASCII in Wireshark's packet viewer. [gRPC folosește Protocol Buffers binare care nu sunt uman-lizibile fără schema .proto. JSON-RPC folosește JSON text care apare ca ASCII lizibil în vizualizatorul de pachete Wireshark.]

</details>

---

### Q36. `N12.T00.Q06`
**Scenario: Blockchain API Protocol / Scenariu: Protocolul API Blockchain**

*Multiple Choice*

> Bitcoin and Ethereum nodes expose their APIs using which RPC protocol? [Nodurile Bitcoin și Ethereum expun API-urile lor folosind ce protocol RPC?]

- **a)** JSON-RPC — the industry standard for blockchain node APIs due to readability and tooling [JSON-RPC — standardul industrial pentru API-uri de noduri blockchain datorită lizibilității și instrumentelor]
- **b)** gRPC — binary efficiency is essential for the high transaction volumes on blockchain [gRPC — eficiența binară este esențială pentru volumele mari de tranzacții pe blockchain]
- **c)** XML-RPC — self-describing XML provides the auditability that regulated financial systems require [XML-RPC — XML-ul auto-descriptiv oferă auditabilitatea pe care o necesită sistemele financiare reglementate]
- **d)** REST — blockchain nodes use standard HTTP CRUD operations for all interactions [REST — nodurile blockchain folosesc operații HTTP CRUD standard pentru toate interacțiunile]

<details><summary>💡 Feedback</summary>

Blockchain platforms like Bitcoin and Ethereum use JSON-RPC as their standard API protocol. This choice provides human-readable debugging, wide tooling support, and transport agnosticism. [Platformele blockchain precum Bitcoin și Ethereum folosesc JSON-RPC ca protocol API standard. Această alegere oferă depanare uman-lizibilă, suport larg de instrumente și agnosticism față de transport.]

</details>

---

### Q37. `N12.T00.Q07` — Health-check scope / Domeniul verificării de sănătate

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

A hypothetical container runs two services. Its health check tests only SMTP, while a separate RPC request fails. What can healthy status establish? [Un container ipotetic rulează două servicii. Health check-ul testează numai SMTP, în timp ce o cerere RPC separată eșuează. Ce poate stabili starea healthy?]

- **a)** Only that the configured check passed; inspect the RPC process, listener, logs and path separately. [Doar că verificarea configurată a trecut; inspectați separat procesul RPC, listenerul, logurile și calea.]
- **b)** Every service and every published port is working. [Orice serviciu și orice port publicat funcționează.]
- **c)** The Windows firewall is certainly the cause. [Firewall-ul Windows este sigur cauza.]

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** A health check has a defined scope. The scenario is independent of S12, which supplies standalone JSON-RPC and gRPC scripts rather than start_lab.py or a dms compose service. [Health check-ul are un domeniu definit. Scenariul este independent de S12, care furnizează scripturi JSON-RPC și gRPC autonome, nu start_lab.py sau un serviciu compose dms.]

</details>

---

### Q38. `N12.T00.Q08`
**Scenario: Email Spoofing Implication / Scenariu: Implicația falsificării emailului**

*Multiple Choice*

> An SMTP session uses MAIL FROM: but the message header says From: admin@company.com. Is this valid SMTP? [O sesiune SMTP folosește MAIL FROM: dar antetul mesajului spune From: admin@company.com. Este acest SMTP valid?]

- **a)** Yes — envelope and headers are independent; this mismatch is technically valid SMTP [Da — plicul și anteturile sunt independente; această nepotrivire este SMTP tehnic valid]
- **b)** No — SMTP servers reject messages where the envelope and header addresses differ [Nu — serverele SMTP resping mesajele unde adresele din plic și antet diferă]
- **c)** No — the RFC 5321 specification requires the MAIL FROM and From: header to match exactly [Nu — specificația RFC 5321 necesită ca MAIL FROM și antetul From: să corespundă exact]
- **d)** Yes but only when both addresses belong to the same domain registered in DNS records [Da, dar numai când ambele adrese aparțin aceluiași domeniu înregistrat în înregistrările DNS]

<details><summary>💡 Feedback</summary>

Yes — SMTP envelope (MAIL FROM, RCPT TO) and message headers (From:, To:) are independent. The envelope controls routing; headers control display. This separation is how email spoofing works and why SPF/DKIM/DMARC were created. [Da — plicul SMTP (MAIL FROM, RCPT TO) și anteturile mesajului (From:, To:) sunt independente. Plicul controlează rutarea; anteturile controlează afișarea. Această separare este modul în care funcționează falsificarea emailului și de ce au fost create SPF/DKIM/DMARC.]

</details>

---

### Q39. `N12.T00.Q09`
**Scenario: Batch RPC with Mixed Results / Scenariu: RPC în lot cu rezultate mixte**

*Multiple Choice*

> A JSON-RPC batch contains [add(1,2), divide(10,0), multiply(3,4)]. How many response objects does the server return? [Un lot JSON-RPC conține [add(1,2), divide(10,0), multiply(3,4)]. Câte obiecte de răspuns returnează serverul?]

- **a)** Three response objects — two with results and one with an error, all in one HTTP 200 array [Trei obiecte de răspuns — două cu rezultate și unul cu eroare, toate într-un singur tablou HTTP 200]
- **b)** One response — the server stops processing after the first error is encountered [Un răspuns — serverul oprește procesarea după ce prima eroare este întâlnită]
- **c)** Two responses — the failed divide call does not generate any response object [Două răspunsuri — apelul eșuat divide nu generează niciun obiect de răspuns]
- **d)** Zero responses — any batch containing even a single error triggers complete batch rejection [Zero răspunsuri — orice lot conținând chiar și o singură eroare declanșează respingerea completă a lotului]

<details><summary>💡 Feedback</summary>

Three — each request with an id gets a response. add succeeds (result: 3), divide fails (error: -32000), multiply succeeds (result: 12). All three responses are in one HTTP 200 JSON array. [Trei — fiecare cerere cu un id primește un răspuns. add reușește (rezultat: 3), divide eșuează (eroare: -32000), multiply reușește (rezultat: 12). Toate trei răspunsurile sunt într-un singur tablou JSON HTTP 200.]

</details>

---

### Q40. `N12.T00.Q10`
**Scenario: Real-Time Collaboration Protocol / Scenariu: Protocol de colaborare în timp real**

*Multiple Choice*

> Your team builds a collaborative code editor requiring real-time character-by-character updates. Which protocol pattern best supports continuous bidirectional data flow? [Echipa dvs. construiește un editor de cod colaborativ care necesită actualizări caracter-cu-caracter în timp real. Ce model de protocol suportă cel mai bine fluxul continuu bidirecțional de date?]

- **a)** gRPC bidirectional streaming — both sides send data continuously over a persistent connection [Streaming bidirecțional gRPC — ambele părți trimit date continuu printr-o conexiune persistentă]
- **b)** JSON-RPC with HTTP polling — the client sends repeated individual requests every few milliseconds [JSON-RPC cu polling HTTP — clientul trimite cereri individuale repetate la câteva milisecunde]
- **c)** XML-RPC with long polling — the server holds connections open until new data arrives [XML-RPC cu long polling — serverul menține conexiunile deschise până la sosirea datelor noi]
- **d)** SMTP notifications — push individual email messages for each character change to all participants [Notificări SMTP — trimiterea de emailuri individuale pentru fiecare schimbare de caracter tuturor participanților]

<details><summary>💡 Feedback</summary>

gRPC bidirectional streaming maintains a persistent connection where both client and server can push data independently. This avoids the overhead of repeated request-response cycles needed by JSON-RPC or XML-RPC. [Streaming-ul bidirecțional gRPC menține o conexiune persistentă unde atât clientul, cât și serverul pot trimite date independent. Aceasta evită overhead-ul ciclurilor repetate cerere-răspuns necesare de JSON-RPC sau XML-RPC.]

</details>

---

### Q41. `N12.T00.Q12`
**JSON-RPC Error Returns HTTP 200 / Eroarea JSON-RPC returnează HTTP 200**

*Multiple Choice*

> A student runs the following command against the Week 12 JSON-RPC server and is confused by the result:

curl -s -o /dev/null -w "%{http_code}" -X POST http://127.0.0.1:8000   -H "Content-Type: application/json"   -d '{"jsonrpc":"2.0","method":"nonexistent","params":[],"id":1}'

The output is 200 . The student concludes the call succeeded. What error exists in the student's reasoning? [Un student execută următoarea comandă pe serverul JSON-RPC din Săptămâna 12 și este confuz de rezultat:

curl -s -o /dev/null -w "%{http_code}" -X POST http://127.0.0.1:8000   -H "Content-Type: application/json"   -d '{"jsonrpc":"2.0","method":"nonexistent","params":[],"id":1}'

Ieșirea este 200 . Studentul concluzionează că apelul a reușit. Ce eroare există în raționamentul studentului?]

- **a)** JSON-RPC returns HTTP 200 even for application errors; the actual error (code -32601) is in the JSON response body, not the HTTP status [JSON-RPC returnează HTTP 200 chiar și pentru erori de aplicație; eroarea reală (cod -32601) se află în corpul răspunsului JSON, nu în starea HTTP]
- **b)** The curl command suppressed the error output with -s flag, so the actual HTTP 404 error was hidden from the terminal display [Comanda curl a suprimat ieșirea de eroare cu flag-ul -s, astfel eroarea HTTP 404 reală a fost ascunsă de pe ecranul terminalului]
- **c)** The server cached a previous successful response and returned it instead of processing the new request for the nonexistent method [Serverul a pus în cache un răspuns anterior de succes și l-a returnat în locul procesării noii cereri pentru metoda inexistentă]
- **d)** HTTP 200 confirms the method was found but returned an empty result; a truly missing method would produce HTTP 501 Not Implemented [HTTP 200 confirmă că metoda a fost găsită dar a returnat un rezultat gol; o metodă cu adevărat lipsă ar produce HTTP 501 Not Implemented]

<details><summary>💡 Feedback</summary>

JSON-RPC separates transport-level success from application-level success. HTTP 200 indicates the transport layer successfully delivered and received the message. However, the JSON body contains an error object with code -32601 (Method not found). The student confused HTTP status with RPC result — a common misconception when transitioning from REST APIs. [JSON-RPC separă succesul la nivel de transport de succesul la nivel de aplicație. HTTP 200 indică faptul că stratul de transport a livrat și primit cu succes mesajul. Totuși, corpul JSON conține un obiect de eroare cu codul -32601 (Metodă negăsită). Studentul a confundat starea HTTP cu rezultatul RPC — o concepție greșită frecventă la tranziția de la API-uri REST.]

</details>

---

### Q42. `N12.T00.Q13`

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

In the supplied S12 schema, why is the Protobuf body of `AddRequest(a=10, b=32)` four bytes? [În schema S12 distribuită, de ce corpul Protobuf al `AddRequest(a=10, b=32)` are patru octeți?]

- **a)** Two one-byte field keys and two one-byte positive int32 varints. [Două chei de câmp de un octet și două varint-uri int32 pozitive de un octet.]
- **b)** Two eight-byte doubles automatically compressed by gzip. [Două double-uri de opt octeți comprimate automat cu gzip.]
- **c)** The four bytes include all gRPC and HTTP/2 headers. [Cei patru octeți includ toate antetele gRPC și HTTP/2.]

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** The actual schema defines `int32 a = 1` and `int32 b = 2`. A field key is `(field_number << 3) | wire_type`. For int32 the wire type is 0, so the keys are 0x08 and 0x10. Positive values 10 and 32 each fit one varint byte: `08 0a 10 20`, four bytes in the Protobuf message body. Add gRPC’s five-byte message prefix and HTTP/2 framing separately when comparing transmitted traffic. [Schema reală definește `int32 a = 1` și `int32 b = 2`. Cheia unui câmp este `(field_number << 3) | wire_type`. Pentru int32, wire type este 0, deci cheile sunt 0x08 și 0x10. Valorile pozitive 10 și 32 încap fiecare într-un octet varint: `08 0a 10 20`, patru octeți în corpul mesajului Protobuf. Adăugați separat prefixul gRPC de cinci octeți și cadrajul HTTP/2 când comparați traficul transmis.]

</details>

---

### Q43. `N12.T00.Q14`
**Microservices RPC Selection / Selecția RPC pentru microservicii**

*Multiple Choice*

> A development team is building an internal microservices platform. Their requirements are: (1) sub-millisecond latency between services, (2) strong type contracts enforced at compile time, (3) bidirectional streaming for real-time telemetry, and (4) code generation for Go, Python and Java clients. Which RPC framework from the Week 12 curriculum best satisfies all four requirements, and why? [O echipă de dezvoltare construiește o platformă internă de microservicii. Cerințele lor sunt: (1) latență sub-milisecundă între servicii, (2) contracte de tip puternic impuse la compilare, (3) streaming bidirecțional pentru telemetrie în timp real și (4) generare de cod pentru clienți Go, Python și Java. Care framework RPC din curricula Săptămânii 12 satisface cel mai bine toate cele patru cerințe și de ce?]

- **a)** gRPC — binary protobuf encoding ensures low latency, .proto files enforce compile-time type contracts, HTTP/2 enables bidirectional streaming, and protoc generates multi-language stubs [gRPC — codificarea binară protobuf asigură latență redusă, fișierele .proto impun contracte de tip la compilare, HTTP/2 permite streaming bidirecțional, iar protoc generează stub-uri multi-limbaj]
- **b)** JSON-RPC — its transport-agnostic design allows WebSocket streaming, JSON Schema provides compile-time validation, and every language has native JSON support [JSON-RPC — designul său agnostic de transport permite streaming WebSocket, JSON Schema oferă validare la compilare, și fiecare limbaj are suport JSON nativ]
- **c)** XML-RPC — its self-describing XML payloads ensure strong typing, the system.methodSignature introspection provides contract enforcement, and XML parsers exist in all languages [XML-RPC — sarcinile utile XML auto-descriptive asigură tipizare puternică, introspecția system.methodSignature oferă impunerea contractelor, iar parsere XML există în toate limbajele]
- **d)** JSON-RPC over HTTP/2 — combining JSON-RPC with HTTP/2 transport provides the same streaming and performance as gRPC whilst maintaining human-readable payloads [JSON-RPC peste HTTP/2 — combinarea JSON-RPC cu transportul HTTP/2 oferă același streaming și performanță ca gRPC menținând în același timp sarcini utile lizibile]

<details><summary>💡 Feedback</summary>

gRPC meets all four requirements: (1) binary Protocol Buffer serialisation and HTTP/2 transport provide low latency, (2) .proto files enforce compile-time type safety, (3) gRPC natively supports four streaming patterns including bidirectional, and (4) protoc generates stubs for Go, Python, Java and many other languages. JSON-RPC lacks streaming and compile-time types. XML-RPC lacks streaming, type enforcement and code generation. [gRPC îndeplinește toate cele patru cerințe: (1) serializarea binară Protocol Buffers și transportul HTTP/2 asigură latență redusă, (2) fișierele .proto impun siguranța tipurilor la compilare, (3) gRPC suportă nativ patru modele de streaming inclusiv bidirecțional, și (4) protoc generează stub-uri pentru Go, Python, Java și multe alte limbaje.]

</details>

---

### Q44. `N12.T00.Q11`
**SMTP State Error Diagnosis / Diagnosticarea unei erori de stare SMTP**

*Multiple Choice*

> A student connects to the educational SMTP server on localhost:587 using netcat and types the following commands in this exact order:

EHLO student.local
DATA

The server responds with code 503. What is the most likely explanation for this error? [Un student se conectează la serverul SMTP educațional pe localhost:587 folosind netcat și tastează următoarele comenzi în această ordine exactă:

EHLO student.local
DATA

Serverul răspunde cu codul 503. Care este explicația cea mai probabilă pentru această eroare?]

- **a)** The MAIL FROM and RCPT TO commands were not issued before DATA, violating the SMTP state machine sequence [Comenzile MAIL FROM și RCPT TO nu au fost emise înainte de DATA, încălcând secvența automatului de stări SMTP]
- **b)** The server does not support the DATA command because it is an educational implementation with limited RFC 5321 support [Serverul nu suportă comanda DATA deoarece este o implementare educațională cu suport limitat RFC 5321]
- **c)** The EHLO command failed silently and the session was not properly authenticated before attempting data transfer [Comanda EHLO a eșuat silențios iar sesiunea nu a fost autentificată corespunzător înainte de transferul de date]
- **d)** Port 587 only accepts encrypted connections via STARTTLS, so unencrypted DATA commands are rejected with 503 [Portul 587 acceptă doar conexiuni criptate prin STARTTLS, astfel comenzile DATA necriptate sunt respinse cu 503]

<details><summary>💡 Feedback</summary>

SMTP is a stateful protocol. The DATA command requires that both MAIL FROM and at least one RCPT TO have been issued first. Sending DATA immediately after EHLO skips these mandatory steps, producing a 503 "Bad sequence of commands" error. The correct sequence is: EHLO → MAIL FROM → RCPT TO → DATA. [SMTP este un protocol cu stări. Comanda DATA necesită emiterea prealabilă a MAIL FROM și a cel puțin unui RCPT TO. Trimiterea DATA imediat după EHLO omite acești pași obligatorii, producând eroarea 503 „Secvență greșită de comenzi". Secvența corectă este: EHLO → MAIL FROM → RCPT TO → DATA.]

</details>

---

## 📚 §2.  Laborator / Lab   (17 questions)

---

### Q45. `N08.S02.Q02`
**MIME type for HTML files in the exercise / Tipul MIME pentru fișiere HTML în exercițiu**

*Multiple Choice*

> What MIME type does the exercise HTTP server return for .html files? [Ce tip MIME returnează serverul HTTP al exercițiului pentru fișierele .html ?]

- **a)** text/html; charset=utf-8 — the standard MIME type with explicit character encoding [text/html; charset=utf-8 — tipul MIME standard cu codificarea explicită a caracterelor]
- **b)** application/html — an incorrect MIME type not defined by IANA for HTML content [application/html — un tip MIME incorect nedefinit de IANA pentru conținut HTML]
- **c)** text/plain; charset=utf-8 — treating HTML as plain text without rendering support [text/plain; charset=utf-8 — tratând HTML-ul ca text simplu fără suport de randare]
- **d)** application/octet-stream — the fallback type used for unrecognised file extensions [application/octet-stream — tipul implicit folosit pentru extensii de fișiere nerecunoscute]

<details><summary>💡 Feedback</summary>

The MIME_TYPES dictionary in ex_8_01 maps ".html" to "text/html; charset=utf-8". The charset parameter prevents encoding ambiguity in the browser. [Dicționarul MIME_TYPES din ex_8_01 asociază ".html" cu "text/html; charset=utf-8". Parametrul charset previne ambiguitatea de codificare în browser.]

</details>

---

### Q46. `N12.S01.Q01` — Port 587 and bind permissions / Portul 587 și permisiunile bind

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

On a conventional Linux configuration with the unprivileged port threshold at 1024, is TCP port 587 automatically unprivileged? [Într-o configurație Linux convențională cu pragul porturilor neprivilegiate la 1024, portul TCP 587 este automat neprivilegiat?]

- **a)** No. It is below 1024; binding needs the configured privilege/capability or a changed namespace policy. [Nu. Este sub 1024; bind necesită privilegiul/capabilitatea configurată sau o politică modificată a namespace-ului.]
- **b)** Yes, because it is used for education. [Da, deoarece este folosit pentru educație.]
- **c)** Yes, because all SMTP ports are unprivileged. [Da, deoarece toate porturile SMTP sunt neprivilegiate.]

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** Port assignment and permission policy are different. CAP_NET_BIND_SERVICE and namespace settings can change who may bind. S12 does not distribute an SMTP Docker service; SMTP questions are theory examples. [Atribuirea portului și politica de permisiuni sunt diferite. CAP_NET_BIND_SERVICE și setările namespace-ului pot schimba cine poate face bind. S12 nu distribuie un serviciu Docker SMTP; întrebările SMTP sunt exemple teoretice.]

</details>

---

### Q47. `N12.S01.Q02` — S12 server ports / Porturile serverelor S12

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

What are the default ports of the standalone S12 JSON-RPC and gRPC servers? [Care sunt porturile implicite ale serverelor autonome JSON-RPC și gRPC S12?]

- **a)** JSON-RPC: 8000; gRPC: 50051
- **b)** JSON-RPC: 6200; gRPC: 6251
- **c)** JSON-RPC: 587; gRPC: 465

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** The JSON-RPC server defaults to 127.0.0.1:8000 and accepts --host/--port. The gRPC server uses 50051. A Mininet instructor scenario may explicitly choose JSON-RPC port 8080; use its stated endpoint. [Serverul JSON-RPC folosește implicit 127.0.0.1:8000 și acceptă --host/--port. Serverul gRPC folosește 50051. Un scenariu Mininet al profesorului poate alege explicit JSON-RPC pe 8080; folosiți endpointul precizat.]

</details>

---

### Q48. `N12.S01.Q04` — Interactive container process / Proces interactiv în container

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

Assume a running example container is named demo and has /bin/sh installed. Which command starts a new interactive shell process in it? [Presupuneți că un container exemplu rulează, se numește demo și are /bin/sh instalat. Ce comandă pornește în el un nou proces shell interactiv?]

- **a)** `docker exec -it demo /bin/sh`
- **b)** `docker run -it demo /bin/sh`
- **c)** `docker logs demo`

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** exec starts a new process in an existing running container. run creates a container from an image. This is a self-contained Docker question, not a claim that S12 provides a demo/dms container. [exec pornește un proces nou într-un container existent în execuție. run creează un container dintr-o imagine. Acesta este un item Docker autonom, nu afirmația că S12 furnizează un container demo/dms.]

</details>

---

### Q49. `N12.S02.Q01`
**curl JSON-RPC Method Call / Apel de metodă JSON-RPC cu curl**

*Multiple Choice*

> Which curl command correctly invokes the add method with parameters [10, 32] on the Week 12 JSON-RPC server? [Care comandă curl invocă corect metoda add cu parametrii [10, 32] pe serverul JSON-RPC din Săptămâna 12?]

- **a)** curl -X POST http://127.0.0.1:8000 -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"add","params":[10,32],"id":1}' [curl -X POST http://127.0.0.1:8000 -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"add","params":[10,32],"id":1}']
- **b)** curl -X GET http://127.0.0.1:8000/add?a=10&b=32 — uses REST-style query parameters to invoke the server add method [curl -X GET http://127.0.0.1:8000/add?a=10&b=32 — folosește parametri de interogare în stil REST pentru a invoca metoda de adunare de pe server]
- **c)** curl -X POST http://localhost:6201 -H "Content-Type: text/xml" -d 'add...' [curl -X POST http://localhost:6201 -H "Content-Type: text/xml" -d 'add...']

<details><summary>💡 Feedback</summary>

The correct call uses POST, Content-Type: application/json, and a valid JSON-RPC 2.0 payload with "jsonrpc":"2.0", "method":"add", "params":[10,32], "id":1 sent to http://127.0.0.1:8000. [Apelul corect folosește POST, Content-Type: application/json și un corp JSON-RPC 2.0 valid cu "jsonrpc":"2.0", "method":"add", "params":[10,32], "id":1 trimis la http://127.0.0.1:8000.]

</details>

---

### Q50. `N12.S02.Q02` — S12 arithmetic error / Eroare aritmetică S12

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

In the supplied S12 JSON-RPC server, what error is returned for a valid request with id 1, method evaluate and params ["10/0"]? [În serverul JSON-RPC S12 distribuit, ce eroare este returnată pentru o cerere validă cu id 1, metoda evaluate și params ["10/0"]?]

- **a)** -32602 — Invalid params / Parametri invalizi
- **b)** -32601 — Method not found / Metodă inexistentă
- **c)** -32700 — Parse error / Eroare de parsare

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** This implementation treats an unsupported or invalid arithmetic expression, including division by zero, as Invalid params and preserves id 1. JSON-RPC does not mandate a universal division-by-zero application code; inspect the server contract. [Implementarea tratează o expresie aritmetică nepermisă sau invalidă, inclusiv împărțirea la zero, drept Invalid params și păstrează id 1. JSON-RPC nu impune un cod universal de aplicație pentru împărțirea la zero; inspectați contractul serverului.]

</details>

---

### Q51. `N12.S02.Q03`
**Notification Response / Răspunsul la notificare**

*Multiple Choice*

> You send a JSON-RPC notification (a request without an "id" field) to the Week 12 server. What HTTP response do you receive? [Trimiteți o notificare JSON-RPC (o cerere fără câmpul "id") la serverul din Săptămâna 12. Ce răspuns HTTP primiți?]

- **a)** HTTP 204 No Content — the server processes the notification but sends no response body [HTTP 204 No Content — serverul procesează notificarea dar nu trimite corp de răspuns]
- **b)** HTTP 200 OK with a JSON response containing the result of the method call [HTTP 200 OK cu un răspuns JSON conținând rezultatul apelului de metodă]
- **c)** HTTP 400 Bad Request because the mandatory id field is missing from the payload [HTTP 400 Bad Request deoarece câmpul obligatoriu id lipsește din corp]
- **d)** HTTP 202 Accepted to indicate the request was queued for asynchronous processing [HTTP 202 Accepted pentru a indica că cererea a fost pusă în coadă pentru procesare asincronă]

<details><summary>💡 Feedback</summary>

The server returns HTTP 204 No Content with an empty body. Since the request has no id, it is a notification — the server processes it but returns no JSON-RPC response, as specified by the protocol. [Serverul returnează HTTP 204 No Content cu un corp gol. Deoarece cererea nu are id, este o notificare — serverul o procesează dar nu returnează niciun răspuns JSON-RPC, conform specificației protocolului.]

</details>

---

### Q52. `N12.S02.Q04`

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

Which method is absent from the supplied S12 JSON-RPC server? [Ce metodă lipsește din serverul JSON-RPC S12 distribuit?]

- **a)** get_stats
- **b)** evaluate
- **c)** add

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** The local example supports evaluate and add. Its deliberately small interface has no get_stats, echo, sort_list or standalone divide method. [Exemplul local suportă evaluate și add. Interfața sa deliberat mică nu are get_stats, echo, sort_list sau o metodă divide separată.]

</details>

---

### Q53. `N12.S02.Q05`
**XML-RPC Content-Type Header / Antetul Content-Type pentru XML-RPC**

*Multiple Choice*

> When sending an XML-RPC request using curl to a hypothetical XML-RPC endpoint, what Content-Type header must be specified? [Când trimiteți o cerere XML-RPC folosind curl către un endpoint XML-RPC ipotetic, ce antet Content-Type trebuie specificat?]

- **a)** text/xml — XML-RPC payloads are XML documents requiring the XML media type [text/xml — corpurile XML-RPC sunt documente XML care necesită tipul media XML]
- **b)** application/json — all RPC protocols share the same JSON-based content type [application/json — toate protocoalele RPC partajează același tip de conținut bazat pe JSON]
- **c)** application/xml-rpc — a dedicated media type registered specifically for XML-RPC [application/xml-rpc — un tip media dedicat înregistrat specific pentru XML-RPC]
- **d)** text/plain — raw text encoding without structured format declaration needed [text/plain — codificare text brut fără declarație de format structurat necesară]

<details><summary>💡 Feedback</summary>

XML-RPC uses XML serialisation, so the Content-Type must be text/xml. This differs from JSON-RPC which uses application/json. This is a protocol-theory question; S12 does not supply this XML-RPC server or a compose file. [XML-RPC folosește serializare XML, deci Content-Type trebuie să fie text/xml. Aceasta diferă de JSON-RPC care folosește application/json. Acesta este un item teoretic de protocol; S12 nu furnizează acest server XML-RPC sau un fișier compose.]

</details>

---

### Q54. `N12.S02.Q06`

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

In `smtplib.SMTP("localhost", 587)`, what does 587 identify, and what does this call alone do? [În `smtplib.SMTP("localhost", 587)`, ce identifică 587 și ce face singur acest apel?]

- **a)** The destination submission port; establishing the connection alone neither starts TLS nor authenticates. [Portul destinație de submission; stabilirea conexiunii singură nu pornește TLS și nu autentifică.]
- **b)** An unprivileged educational port that automatically encrypts and authenticates. [Un port educațional neprivilegiat care criptează și autentifică automat.]
- **c)** The source port of the local client. [Portul sursă al clientului local.]

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** Use the server’s configured submission policy. A STARTTLS client needs the explicit starttls flow with certificate verification and authentication where required. Implicit TLS submission on 465 uses SMTP_SSL. [Folosiți politica de submission configurată pe server. Un client STARTTLS necesită fluxul explicit starttls cu verificarea certificatului și autentificare când este cerută. Submission cu TLS implicit pe 465 folosește SMTP_SSL.]

</details>

---

### Q55. `N12.S03.Q01`

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

The supplied `S12_Part02_Config_Calculator.proto` defines `int32 a = 1; int32 b = 2;` in AddRequest. What are 1 and 2? [Fișierul distribuit `S12_Part02_Config_Calculator.proto` definește `int32 a = 1; int32 b = 2;` în AddRequest. Ce reprezintă 1 și 2?]

- **a)** Field numbers used with wire types to encode field keys. [Numere de câmp folosite împreună cu wire types pentru codificarea cheilor.]
- **b)** Default operand values. [Valorile implicite ale operanzilor.]
- **c)** Byte lengths of the operands. [Lungimile în octeți ale operanzilor.]

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** The actual schema defines `int32 a = 1` and `int32 b = 2`. A field key is `(field_number << 3) | wire_type`. For int32 the wire type is 0, so the keys are 0x08 and 0x10. Positive values 10 and 32 each fit one varint byte: `08 0a 10 20`, four bytes in the Protobuf message body. Add gRPC’s five-byte message prefix and HTTP/2 framing separately when comparing transmitted traffic. [Schema reală definește `int32 a = 1` și `int32 b = 2`. Cheia unui câmp este `(field_number << 3) | wire_type`. Pentru int32, wire type este 0, deci cheile sunt 0x08 și 0x10. Valorile pozitive 10 și 32 încap fiecare într-un octet varint: `08 0a 10 20`, patru octeți în corpul mesajului Protobuf. Adăugați separat prefixul gRPC de cinci octeți și cadrajul HTTP/2 când comparați traficul transmis.]

</details>

---

### Q56. `N12.S03.Q02`

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

How many bytes does the Protobuf body `AddRequest(a=10, b=32)` occupy under the supplied int32 schema, excluding gRPC and HTTP/2 framing? [Câți octeți ocupă corpul Protobuf `AddRequest(a=10, b=32)` în schema int32 distribuită, excluzând cadrajul gRPC și HTTP/2?]

- **a)** 4
- **b)** 18
- **c)** 56
- **d)** 0

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** The actual schema defines `int32 a = 1` and `int32 b = 2`. A field key is `(field_number << 3) | wire_type`. For int32 the wire type is 0, so the keys are 0x08 and 0x10. Positive values 10 and 32 each fit one varint byte: `08 0a 10 20`, four bytes in the Protobuf message body. Add gRPC’s five-byte message prefix and HTTP/2 framing separately when comparing transmitted traffic. [Schema reală definește `int32 a = 1` și `int32 b = 2`. Cheia unui câmp este `(field_number << 3) | wire_type`. Pentru int32, wire type este 0, deci cheile sunt 0x08 și 0x10. Valorile pozitive 10 și 32 încap fiecare într-un octet varint: `08 0a 10 20`, patru octeți în corpul mesajului Protobuf. Adăugați separat prefixul gRPC de cinci octeți și cadrajul HTTP/2 când comparați traficul transmis.]

</details>

---

### Q57. `N12.S03.Q03` — Supplied gRPC service / Serviciul gRPC distribuit

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

Which methods are declared in the unmodified S12 Calculator service schema? [Ce metode sunt declarate în schema serviciului Calculator S12 nemodificată?]

- **a)** Add and Multiply / Add și Multiply
- **b)** Add and Divide / Add și Divide
- **c)** Divide only / Numai Divide

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** Power is an extension to add to the .proto and regenerate. There is no Divide method in the supplied schema, so a question about its division-by-zero implementation would describe a different server. gRPC error behaviour must be tied to a method that actually exists. [Power este o extensie de adăugat în .proto și apoi de regenerat. Schema distribuită nu are metoda Divide, deci un item despre implementarea împărțirii la zero ar descrie alt server. Comportamentul erorilor gRPC trebuie asociat unei metode care există.]

</details>

---

### Q58. `N12.S03.Q04` — gRPC descriptor and endpoint / Descriptorul și endpointul gRPC

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

The supplied gRPC server uses plaintext HTTP/2 and does not enable server reflection. From S12/2_protobuf, which grpcurl command can use the supplied descriptor to call Add after the server is running? [Serverul gRPC distribuit folosește HTTP/2 necriptat și nu activează server reflection. Din S12/2_protobuf, ce comandă grpcurl poate folosi descriptorul distribuit pentru a apela Add după pornirea serverului?]

- **a)** `grpcurl -plaintext -import-path . -proto S12_Part02_Config_Calculator.proto -d '{"a":10,"b":32}' localhost:50051 seminar12.Calculator/Add`
- **b)** `grpcurl localhost:6251 list`
- **c)** `curl http://localhost:50051/Add`

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** The optional grpcurl tool needs -plaintext for this laboratory endpoint and the .proto because reflection is not enabled. The method path includes package seminar12. The ordinary course route remains the generated Python client. [Instrumentul opțional grpcurl necesită -plaintext pentru acest endpoint de laborator și .proto deoarece reflection nu este activat. Calea metodei include pachetul seminar12. Ruta obișnuită a cursului rămâne clientul Python generat.]

</details>

---

### Q59. `N12.S04.Q02` — Submission display filter / Filtru de afișare submission

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

A hypothetical SMTP submission service is known to listen on TCP 587. Which Wireshark display filter selects traffic to or from that port? [Se știe că un serviciu SMTP submission ipotetic ascultă pe TCP 587. Ce filtru de afișare Wireshark selectează traficul către sau de la acel port?]

- **a)** `tcp.port == 587`
- **b)** `udp.port == 587`
- **c)** `tcp port 587`

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** This is a port filter, not proof that every selected payload is plaintext SMTP. STARTTLS encrypts subsequent application traffic. The BPF form tcp port 587 belongs to capture filters, not display filters. [Acesta este un filtru de port, nu dovada că orice payload selectat este SMTP în clar. STARTTLS criptează traficul de aplicație ulterior. Forma BPF tcp port 587 aparține filtrelor de captură, nu de afișare.]

</details>

---

### Q60. `N12.S04.Q03` — S12 combined display filter / Filtru de afișare combinat S12

*Multiple Choice — one correct answer / Alegere multiplă — un singur răspuns corect*

Using the default standalone S12 server ports, which display filter selects JSON-RPC and gRPC traffic together? [Folosind porturile implicite ale serverelor autonome S12, ce filtru de afișare selectează împreună traficul JSON-RPC și gRPC?]

- **a)** `tcp.port == 8000 || tcp.port == 50051`
- **b)** `udp.port == 8000 || udp.port == 50051`
- **c)** `tcp.port == 587 || tcp.port == 6251`

<details><summary>💡 Feedback</summary>

**Correct answer / Răspuns corect: a.** These are the current script defaults. If the instructor changes an endpoint, change the filter accordingly. Port filtering selects candidate traffic and does not replace protocol decoding. [Acestea sunt valorile implicite ale scripturilor actuale. Dacă profesorul schimbă un endpoint, adaptați filtrul. Filtrarea după port selectează trafic candidat și nu înlocuiește decodarea protocolului.]

</details>

---

### Q61. `N12.S04.Q04`
**tshark SMTP Analysis / Analiză SMTP cu tshark**

*Multiple Choice*

> After capturing SMTP traffic into smtp.pcap, which tshark command displays only the SMTP protocol frames from the capture file? [După capturarea traficului SMTP în smtp.pcap, ce comandă tshark afișează doar cadrele de protocol SMTP din fișierul de captură?]

- **a)** tshark -r smtp.pcap -Y "smtp" — reads file and applies display filter for SMTP [tshark -r smtp.pcap -Y "smtp" — citește fișierul și aplică filtrul de afișare pentru SMTP]
- **b)** tshark -f "smtp" smtp.pcap — applies a capture filter to an already-saved file [tshark -f "smtp" smtp.pcap — aplică un filtru de captură la un fișier deja salvat]
- **c)** tshark -w smtp.pcap -Y "smtp" — writes a new capture file with SMTP frames only [tshark -w smtp.pcap -Y "smtp" — scrie un fișier de captură nou doar cu cadre SMTP]
- **d)** tshark --protocol smtp --read smtp.pcap — uses long-form protocol specification [tshark --protocol smtp --read smtp.pcap — folosește specificarea protocolului în formă lungă]

<details><summary>💡 Feedback</summary>

The command tshark -r smtp.pcap -Y "smtp" reads the capture file (-r) and applies a display filter (-Y) for SMTP protocol frames. The -Y flag specifies a display filter (applied after capture), not a capture filter (-f). [Comanda tshark -r smtp.pcap -Y "smtp" citește fișierul de captură (-r) și aplică un filtru de afișare (-Y) pentru cadrele de protocol SMTP. Flagul -Y specifică un filtru de afișare (aplicat după captură), nu un filtru de captură (-f).]

</details>

---
