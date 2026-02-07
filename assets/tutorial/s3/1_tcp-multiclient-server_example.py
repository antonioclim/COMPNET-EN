import socket
import threading

# Adresa IP pe care va asculta serverul.
# "127.0.0.1" = localhost (doar conexiuni de pe aceeași mașină).
HOST = "127.0.0.1"

# Portul pe care va asculta serverul.
# Porturile > 1023 sunt neprivilegiate (nu necesită drepturi speciale).
PORT = 3333

# Flag global pentru a putea opri bucla de acceptare (teoretic).
is_running = True

# O listă globală cu toți clienții conectați.
# Ne ajută să vedem câți clienți sunt simultan.
clients = []
clients_lock = threading.Lock()


def handle_client(client_socket, client_address):
    """
    Funcție rulată într-un THREAD separat pentru fiecare client.

    - primește socket-ul clientului și adresa (ip, port)
    - citește mesaje într-o buclă
    - trimite înapoi același mesaj, dar cu prima literă mare (capitalize)
    - se oprește când clientul închide conexiunea sau nu mai trimite date
    """
    ip, port = client_address
    print(f"[THREAD START] Client {ip}:{port} connected")

    with client_socket:
        while True:
            # Așteptăm până primim maxim 1024 bytes de la client.
            data = client_socket.recv(1024)

            # Dacă data este șir vid (b""), înseamnă că clientul a închis conexiunea.
            if not data:
                print(f"[DISCONNECT] Client {ip}:{port} closed the connection")
                break

            print(f"[RECV] From {ip}:{port} -> {data!r}")

            # Prelucrăm mesajul: .capitalize() pune prima literă mare.
            response = data.capitalize()

            # Trimitem înapoi răspunsul către același client.
            client_socket.sendall(response)
            print(f"[SEND] To   {ip}:{port} -> {response!r}")

    # Scoatem clientul din listă când thread-ul se termină.
    with clients_lock:
        if client_socket in clients:
            clients.remove(client_socket)

    print(f"[THREAD END] Client {ip}:{port} handler finished\n")


def accept_loop(server_socket):
    """
    Buclă separată (într-un thread sau chiar în main) care:
    - acceptă conexiuni noi
    - pornește câte un thread handle_client pentru fiecare client
    """

    print(f"[INFO] Server ready, listening on {HOST}:{PORT}")
    while is_running:
        # accept() blochează până când un client se conectează.
        client_socket, client_address = server_socket.accept()

        ip, port = client_address
        print(f"[CONNECT] New client from {ip}:{port}")

        # Adăugăm clientul în lista globală.
        with clients_lock:
            clients.append(client_socket)
            print(f"[INFO] Currently connected clients: {len(clients)}")

        # Pornim un thread dedicat pentru acest client.
        client_thread = threading.Thread(
            target=handle_client,
            args=(client_socket, client_address),
            daemon=True,  # daemon=True -> thread-ul se închide când se închide procesul
        )
        client_thread.start()


def main():
    # Creăm un socket TCP (IPv4).
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Legăm socket-ul de (HOST, PORT).
        server_socket.bind((HOST, PORT))

        # Punem serverul în modul "ascultare".
        # Parametru (backlog) = număr de conexiuni în așteptare.
        server_socket.listen(5)
        print(f"[START] TCP multi-client server on {HOST}:{PORT}")

        # Rulăm bucla de acceptare (poate fi și într-un thread separat).
        accept_loop(server_socket)

    except KeyboardInterrupt:
        print("\n[INFO] KeyboardInterrupt received, shutting down server...")
    except BaseException as err:
        print(f"[ERROR] {err}")
    finally:
        # Închidem socket-ul serverului.
        server_socket.close()
        print("[STOP] Server socket closed")


if __name__ == '__main__':
    main()
