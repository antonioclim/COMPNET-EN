### Scenario: Observarea handshake-ului TLS cu openssl

### Obiectiv
- Sa vezi cum arata un handshake TLS (mesaje, versiune, cipher)
- Sa vezi certificatul (subject/issuer) si verificarea lui
- Sa intelegi diferenta dintre "TCP connect" si "TLS handshake"

### Cerinte
- Linux
- openssl
- sudo optional (nu e necesar)

### Varianta recomandata: server local

1. Genereaza certificat self-signed
   - ./gen_certs.sh

2. Porneste server TLS (Terminal 1)
   - ./run_server.sh

3. Porneste client TLS (Terminal 2)
   - ./run_client.sh

### Ce observi
- In output-ul clientului:
  - Protocol: TLSv1.3 (sau TLSv1.2)
  - Cipher negociat
  - Certificat (self-signed) si motivul pentru care nu e trusted

### Curatare
- ./cleanup.sh
