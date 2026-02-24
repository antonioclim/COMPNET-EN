import socket
import time

HOST = "0.0.0.0"
PORT = 9091

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, PORT))
    s.settimeout(1.0)

    received = set()
    start = time.time()

    while True:
        try:
            data, _ = s.recvfrom(2048)
        except socket.timeout:
            if time.time() - start > 5:
                break
            continue

        msg = data.decode("utf-8", errors="replace").strip()
        if msg.startswith("MSG "):
            try:
                n = int(msg.split(" ", 1)[1])
                received.add(n)
            except Exception:
                pass

    if received:
        mn = min(received)
        mx = max(received)
        missing = [i for i in range(mn, mx + 1) if i not in received]
        print(f"[udp_receiver] received {len(received)} messages, range {mn}..{mx}")
        print(f"[udp_receiver] missing count: {len(missing)}")
        if missing[:20]:
            print(f"[udp_receiver] first missing: {missing[:20]}")
    else:
        print("[udp_receiver] received nothing")

if __name__ == "__main__":
    main()
