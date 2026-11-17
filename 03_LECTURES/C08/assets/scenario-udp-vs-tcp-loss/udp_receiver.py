import socket
import time
import argparse

HOST = "0.0.0.0"
PORT = 9091

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=200, help="Agreed sender sequence length, starting at zero")
    expected = parser.parse_args().count
    if expected <= 0:
        parser.error("--count must be positive")
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
                if 0 <= n < expected:
                    received.add(n)
            except Exception:
                pass

    s.close()
    missing = [i for i in range(expected) if i not in received]
    print(f"[udp_receiver] received {len(received)}/{expected} unique messages (sequence 0..{expected - 1})")
    print(f"[udp_receiver] missing count: {len(missing)}")
    print(f"[udp_receiver] first missing: {missing[:20]}")

if __name__ == "__main__":
    main()
