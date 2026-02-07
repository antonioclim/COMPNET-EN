import socket

# Adresa serverului:
# - "127.0.0.1" înseamnă "localhost" (aceeași mașină)
# - dacă serverul rulează pe alt host, aici puneți IP-ul acelui host.
HOST = "127.0.0.1"

# Portul pe care ascultă serverul.
# Trebuie să fie același cu portul din serverul TCP (ex: 12345).
PORT = 12345


# Folosim context manager "with" ca să ne asigurăm că socket-ul
# este închis corect, chiar dacă apare o eroare.
# socket.AF_INET  -> familie de adrese IPv4
# socket.SOCK_STREAM -> tipul de socket pentru TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Stabilim conexiunea TCP către server.
    # Dacă serverul nu rulează sau portul e greșit, aici apare o eroare.
    print(f"[INFO] Connecting to {HOST}:{PORT} ...")
    s.connect((HOST, PORT))
    print("[INFO] Connected. Sending data...")

    # Trimitem un mesaj simplu către server.
    # b"Hello, world" -> șir de bytes (nu string unicode).
    s.sendall(b"Hello, world")

    # Așteptăm răspunsul de la server.
    # recv(1024) citește maxim 1024 bytes.
    data = s.recv(1024)

# Când ieșim din blocul with, socket-ul se închide automat.
print(f"[INFO] Received {data!r} from server")
