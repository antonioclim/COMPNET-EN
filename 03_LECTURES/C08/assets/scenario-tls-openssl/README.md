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

## Files

| Name | Lines |
|------|-------|
| `cleanup.sh` | 8 |
| `gen_certs.sh` | 17 |
| `run_client.sh` | 13 |
| `run_server.sh` | 16 |

## Cross-References

Parent lecture: [`C08/ — Transport Layer (TCP, UDP, TLS, QUIC)`](../../)
  
Lecture slides: [`c8-transport-layer.md`](../../c8-transport-layer.md)
  
Quiz: [`W08`](../../../../00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W08_Questions.md)

## Selective Clone

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set 03_LECTURES/C08/assets/scenario-tls-openssl
```

**Method B — Direct download**

Browse at: `https://github.com/antonioclim/COMPNET-EN/tree/main/03_LECTURES/C08/assets/scenario-tls-openssl`
