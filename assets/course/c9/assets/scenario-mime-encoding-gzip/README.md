### Scenario: Inspectie MIME, charset, gzip

### Obiectiv
- Observam Content-Type (MIME) si charset
- Observam Content-Encoding (gzip)
- Vedem diferenta intre un raspuns comprimat si unul necomprimat

### Cerinte
- python3
- curl

### Cum rulezi
1) Porneste serverul
- ./run.sh

2) In alt terminal, testeaza cu curl

A) HTML (fara gzip)
- curl -i http://127.0.0.1:8089/

B) JSON (fara gzip)
- curl -i http://127.0.0.1:8089/data.json

C) Cu gzip (client anunta ca accepta gzip)
- curl -i -H "Accept-Encoding: gzip" http://127.0.0.1:8089/
- curl -i -H "Accept-Encoding: gzip" http://127.0.0.1:8089/data.json

D) Descarca body-ul comprimat ca sa vezi bytes
- curl -H "Accept-Encoding: gzip" -o out.gz http://127.0.0.1:8089/data.json
- file out.gz

### Ce observi
- Content-Type: text/html; charset=utf-8
- Content-Type: application/json; charset=utf-8
- Cand Accept-Encoding include gzip:
  - serverul raspunde cu Content-Encoding: gzip
