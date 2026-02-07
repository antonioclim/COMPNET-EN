import socket
import threading

HOST = "127.0.0.1"
PORT = 3333

is_running = True

# Listă globală cu toți clienții activi.
clients = []
clients_lock = threading.Lock()


def handle_client(client_socket, client_address):
    """
    Handler pentru un singur client, rulat într-un thread separat.

    Obiectiv:
    - primiți mesaje de la client
    - retransmiteți mesajele către TOȚI ceilalți clienți (broadcast)
    - afișați loguri clare pentru debugging
    """
    ip, port = client_address
    print(f"[THREAD START] Client {ip}:{port} connected")

    with client_socket:
        while True:
            data = client_socket.recv(1024)
            if not data:
                print(f"[DISCONNECT] Client {ip}:{port} closed the connection")
                break

            # >>> STUDENT CODE STARTS HERE
            """
            TODO (student):

            1. Afișați un log clar cu mesajul primit, de forma:
               [RECV] From <ip>:<port> -> <data>

            2. Implementați un "mini-chat":
               - construiți un mesaj text de forma:
                 f"[{ip}:{port}] {data.decode('utf-8', errors='ignore')}"
               - encodați-l în bytes (UTF-8).

               - trimiteți acest mesaj către TOȚI ceilalți clienți
                 conectați (toți din lista 'clients' mai puțin client_socket).

            3. Pentru fiecare client către care trimiteți, afișați:
               [FWD] To <other_ip>:<other_port> -> <mesaj>

               Indiciu:
               - pentru a obține adresa altui client puteți folosi:
                   other_ip, other_port = other.getpeername()
               - folosiți clients_lock pentru a proteja accesul la lista 'clients'.
            """
            # <<< STUDENT CODE ENDS HERE

    # La ieșirea din buclă, clientul se deconectează: îl scoatem din listă.
    with clients_lock:
        if client_socket in clients:
            clients.remove(client_socket)
            print(f"[INFO] Removed client {ip}:{port}. Clients left: {len(clients)}")

    print(f"[THREAD END] Client {ip}:{port} handler finished\n")


def accept_loop(server_socket):
    print(f"[INFO] Server ready, listening on {HOST}:{PORT}")
    while is_running:
        client_socket, client_address = server_socket.accept()
        ip, port = client_address
        print(f"[CONNECT] New client from {ip}:{port}")

        # Adăugăm clientul în lista globală.
        with clients_lock:
            clients.append(client_socket)
            print(f"[INFO] Currently connected clients: {len(clients)}")

        client_thread = threading.Thread(
            target=handle_client,
            args=(client_socket, client_address),
            daemon=True,
        )
        client_thread.start()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"[START] TCP multi-client chat server on {HOST}:{PORT}")
        accept_loop(server_socket)
    except KeyboardInterrupt:
        print("\n[INFO] KeyboardInterrupt received, shutting down server...")
    except BaseException as err:
        print(f"[ERROR] {err}")
    finally:
        server_socket.close()
        print("[STOP] Server socket closed")


if __name__ == '__main__':
    main()
