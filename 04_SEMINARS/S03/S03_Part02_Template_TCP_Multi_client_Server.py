import socket
import threading

HOST = "127.0.0.1"
PORT = 3333

is_running = True

# Global list of all active clients.
clients = []
clients_lock = threading.Lock()


def handle_client(client_socket, client_address):
    """
    Handler for a single client, run in a separate thread.

    Objective:
    - receive messages from the client
    - forward messages to ALL other clients (broadcast)
    - display clear logs for debugging
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

            1. Display a clear log with the received message, in the form:
               [RECV] From <ip>:<port> -> <data>

            2. Implement a "mini-chat":
               - construct a text message of the form:
                 f"[{ip}:{port}] {data.decode('utf-8', errors='ignore')}"
               - encode it to bytes (UTF-8).

               - send this message to ALL other connected clients
                 (all entries in the 'clients' list except client_socket).

            3. For each client you send to, display:
               [FWD] To <other_ip>:<other_port> -> <message>

               Hint:
               - to obtain the address of another client you can use:
                   other_ip, other_port = other.getpeername()
               - use clients_lock to protect access to the 'clients' list.
            """
            # <<< STUDENT CODE ENDS HERE

    # Upon exiting the loop the client has disconnected: remove it from the list.
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

        # Add the client to the global list.
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
