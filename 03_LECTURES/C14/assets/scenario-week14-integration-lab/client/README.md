# Client toolbox (Week 14 integration lab)

The `client` container in this scenario is a controlled environment for running checks *inside the lab network*.

Enter the container:

```bash
docker compose exec client sh
```

Then run:

```bash
python dns_query.py www.week14.local
python smoke_test.py
```

For the TLS variant:

```bash
python smoke_test.py --tls --cafile /client/certs/ca.crt
```

