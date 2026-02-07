### Sarcina studentului

Realizați următorul scenariu și generați un fișier cu dovezi:

1. Configurați un capture filter pentru a capta doar traficul TCP către portul **9300**.
2. Porniți un server TCP cu netcat pe portul 9300 și conectați un client.
3. Trimiteți trei mesaje diferite.
4. Opriți captura și aplicați un display filter pentru a izola stream-ul TCP.
5. Repetați procesul cu UDP pe portul **9301**, cu un capture filter și un display filter separate.
6. Identificați în capturi:

   * handshake-ul TCP,
   * un pachet cu payload,
   * un pachet UDP.

**Dovadă necesară**
Creați fișierul `wireshark_activity_output.zip` care trebuie să conțină:

* Screenshots ale filtrelor folosite (capture și display),
* Screenshots ale pachetelor identificate,
* O scurtă explicație (5–7 propoziții) privind diferențele observate între traficul TCP și UDP în captură.

Fișierul va fi încărcat ulterior ca dovadă de finalizare.
