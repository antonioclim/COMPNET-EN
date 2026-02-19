### Scenario: observing the TLS handshake with OpenSSL

### Objective
- Identify key elements of a TLS handshake (messages, version and cipher suite)
- Inspect the certificate (subject and issuer) and the verification result
- Distinguish between establishing a TCP connection and performing a TLS handshake

### Requirements
- Linux
- openssl
- sudo is not required

### Recommended approach: local server

1. Generate a self-signed certificate
   - ./gen_certs.sh

2. Start the TLS server (Terminal 1)
   - ./run_server.sh

3. Start the TLS client (Terminal 2)
   - ./run_client.sh

### What to observe
- In the client output:
  - Protocol: TLSv1.3 (or TLSv1.2)
  - Negotiated cipher suite
  - Certificate (self-signed) and why it is not trusted

### Cleanup
- ./cleanup.sh
