### Scenario: Encoding pitfall (UTF-8 vs header charset)

### Obiectiv
- Aratam ca textul depinde de charset
- Demonstram o eroare tipica: body UTF-8, dar header declara altceva

### Cerinte
- python3
- curl

### Cum rulezi
- ./run.sh

### Teste cu curl
1) Raspuns corect (UTF-8 declarat corect)
- curl -i http://127.0.0.1:8090/ok

2) Raspuns "gresit" (body UTF-8, header declara ISO-8859-1)
- curl -i http://127.0.0.1:8090/bad

3) Observa bytes (optional)
- curl -s http://127.0.0.1:8090/ok | xxd | head
- curl -s http://127.0.0.1:8090/bad | xxd | head

### Ce observi
- Body este identic (UTF-8)
- Doar charset-ul din header difera
- Un browser ar putea afisa caracterele gresit in cazul /bad
