import socket

# Adresa și portul serverului de text protocol.
HOST = "127.0.0.1"
PORT = 3333

# Dimensiunea buffer-ului folosit la recv().
BUFFER_SIZE = 8


def get_command(command: str) -> bytes:
    """
    Transformă o linie de comandă în formatul de protocol.

    Input (de la utilizator):
        command = "add user1 Alice"

    Dorim să trimitem peste TCP:
        "<TOTAL_LENGTH> <command>"

    unde:
      TOTAL_LENGTH = len(command) + len(str(len(command))) + 1

    Explicație:
      - len(command) = numărul de caractere din "add user1 Alice"
      - len(str(len(command))) = câte caractere are numărul lungimii
        (ex: len("15") = 2)
      - +1 = spațiul dintre TOTAL_LENGTH și command.
    """
    c = command.strip()
    content_length = len(c)
    total_length = content_length + len(str(content_length)) + 1
    frame = f"{total_length} {c}"
    return frame.encode("utf-8")


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Conectare la server.
        s.connect((HOST, PORT))
        print(f"[INFO] Connected to {HOST}:{PORT}")

        command = ""
        # Buclă interactivă de comenzi.
        while command.strip() != "exit":
            command = input("connected> ")

            # Dacă utilizatorul doar apasă Enter, trecem mai departe.
            if not command.strip():
                continue

            # Construim mesajul în formatul de protocol.
            framed = get_command(command)

            # Trimitem mesajul la server.
            s.sendall(framed)

            # Citim răspunsul în bucăți până avem mesajul complet.
            data = s.recv(BUFFER_SIZE)
            if not data:
                print("[INFO] Server closed connection.")
                break

            string_data = data.decode("utf-8")
            full_data = string_data

            # Primul token e MESSAGE_LENGTH.
            message_length = int(string_data.split(" ")[0])
            remaining = message_length - len(string_data)

            while remaining > 0:
                data = s.recv(BUFFER_SIZE)
                if not data:
                    break
                string_data = data.decode("utf-8")
                full_data += string_data
                remaining -= len(string_data)

            # full_data are forma "<MESSAGE_LENGTH> <PAYLOAD>"
            # Afișăm doar payload-ul (partea după primul spațiu).
            payload = " ".join(full_data.split(" ")[1:])
            print(payload)


if __name__ == "__main__":
    main()
