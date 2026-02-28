# TLS artefacts (generated locally)

This lab does **not** ship private keys.

To enable HTTPS in the Week 14 integration lab, generate a small demo CA and a server certificate:

```bash
cd 03_LECTURES/C14/assets/scenario-week14-integration-lab
bash tls/generate_demo_certs.sh
```

This creates:

- `tls/ca/ca.crt` (demo CA certificate)
- `tls/server/server.crt` (server certificate for `www.week14.local`)
- `tls/server/server.key` (server private key)
- `tls/private/ca.key` (demo CA private key)

Then start the TLS variant:

```bash
docker compose -f docker-compose.yml -f docker-compose.tls.yml up --build
```

Inside the `client` container you can verify the chain:

```bash
python client/smoke_test.py --tls --cafile /client/certs/ca.crt
```

