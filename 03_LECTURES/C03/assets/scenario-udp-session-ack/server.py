import socket
import uuid

HOST = "127.0.0.1"
PORT = 9300

sessions = {}  # addr -> token
seq = {}       # token -> counter

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))
        print(f"UDP session server listening on {HOST}:{PORT}")

        while True:
            data, addr = s.recvfrom(2048)
            text = data.decode("utf-8", errors="replace").strip()

            if text == "HELLO":
                token = uuid.uuid4().hex[:8]
                sessions[addr] = token
                seq[token] = 0
                s.sendto(f"TOKEN:{token}\n".encode("utf-8"), addr)
                continue

            if text.startswith("MSG:"):
                parts = text.split(":", 2)
                if len(parts) != 3:
                    s.sendto(b"ERR:FORMAT\n", addr)
                    continue
                _, token, payload = parts
                if token not in seq:
                    s.sendto(b"ERR:TOKEN\n", addr)
                    continue
                seq[token] += 1
                n = seq[token]
                print(f"From {addr} token={token} seq={n} payload={payload}")
                s.sendto(f"ACK:{token}:{n}\n".encode("utf-8"), addr)
                continue

            s.sendto(b"ERR:UNKNOWN\n", addr)

if __name__ == "__main__":
    main()
