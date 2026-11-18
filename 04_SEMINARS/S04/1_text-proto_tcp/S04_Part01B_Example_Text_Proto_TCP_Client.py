import socket
from text_framing import encode_frame, read_frame

# Address and port of the text protocol server.
HOST = "127.0.0.1"
PORT = 3333

# Buffer size used for recv().
BUFFER_SIZE = 8


def get_command(command: str) -> bytes:
    """Frame the command using its encoded UTF-8 byte length, including header."""
    return encode_frame(command.strip())


def main():
    with socket.create_connection((HOST, PORT), timeout=10) as s:
        print(f"[INFO] Connected to {HOST}:{PORT}")
        while True:
            try:
                command = input("connected> ").strip()
            except EOFError:
                break
            if command == "exit":
                break
            if not command:
                continue
            try:
                s.sendall(get_command(command))
                frame = read_frame(s)
                if frame is None:
                    print("[INFO] Server closed connection.")
                    break
                print(frame.split(b" ", 1)[1].decode("utf-8"))
            except (OSError, EOFError, ValueError) as exc:
                print(f"[ERROR] {exc}")
                break


if __name__ == "__main__":
    main()
