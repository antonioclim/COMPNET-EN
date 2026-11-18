# TCP tunnel and half-close

From this directory, start `python3 echo.py` in terminal 1 and `python3 tunnel.py`
in terminal 2. In terminal 3 run:

```bash
python3 - <<'PY'
import socket
with socket.create_connection(('127.0.0.1', 9090), timeout=3) as s:
    s.sendall(b'hello tunnel')
    s.shutdown(socket.SHUT_WR)
    parts = []
    while True:
        data = s.recv(4096)
        if not data:
            break
        parts.append(data)
    assert b''.join(parts) == b'hello tunnel'
    print('Echo received and EOF propagated in both directions')
PY
```

The echo server ends when its single connection closes. Stop the tunnel with
Ctrl+C. Each forwarding direction propagates EOF using SHUT_WR; an idle timeout
or socket error cancels both directions. The 30-second timeout is a lab policy,
not a TCP protocol timeout. For Mininet, use `--listen 0.0.0.0:PORT` and the
explicit reachable target address; both scripts use the same CLI syntax.
