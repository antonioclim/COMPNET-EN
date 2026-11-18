"""Small TCP tunnel: preserves half-close and bounds idle connections."""
import argparse
import socket
import threading

def forward_stream(src, dst, direction, stop_event):
    """Forward this direction; EOF half-closes only the peer write side."""
    try:
        while not stop_event.is_set():
            data = src.recv(4096)
            if not data:
                dst.shutdown(socket.SHUT_WR)
                return
            dst.sendall(data)
    except OSError as exc:
        print(f"{direction}: {exc}")
        stop_event.set()
        for channel in (src, dst):
            try:
                channel.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass

def handle_client(client, host, port):
    """Forward both ways; the lab uses a 30-second idle timeout."""
    target = None
    try:
        target = socket.create_connection((host, port), timeout=10)
        target.settimeout(30)
        client.settimeout(30)
        stop = threading.Event()
        workers = [threading.Thread(target=forward_stream, args=args)
                   for args in ((client, target, "c-to-t", stop),
                                (target, client, "t-to-c", stop))]
        for worker in workers:
            worker.start()
        for worker in workers:
            worker.join()
    finally:
        client.close()
        if target is not None:
            target.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--listen", default="127.0.0.1:9090")
    parser.add_argument("--target", default="127.0.0.1:8080")
    args = parser.parse_args()
    bind_host, bind_port = args.listen.rsplit(":", 1)
    target_host, target_port = args.target.rsplit(":", 1)
    with socket.create_server((bind_host, int(bind_port))) as server:
        print(f"Tunnel {args.listen} -> {args.target}", flush=True)
        while True:
            client, _ = server.accept()
            threading.Thread(target=handle_client,
                             args=(client, target_host, int(target_port)),
                             daemon=True).start()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
