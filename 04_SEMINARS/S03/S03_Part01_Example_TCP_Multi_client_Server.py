import socket
import threading

# IP address on which the server will listen.
# "127.0.0.1" = localhost (only connections from the same machine).
HOST = "127.0.0.1"

# Port on which the server will listen.
# Ports > 1023 are unprivileged (no special rights required).
PORT = 3333

# Global flag to allow stopping the accept loop (in theory).
is_running = True

# Global list of all connected clients.
# Helps us track how many clients are connected simultaneously.
clients = []
clients_lock = threading.Lock()


def handle_client(client_socket, client_address):
    """
    Function run in a separate THREAD for each client.

    - receives the client socket and address (ip, port)
    - reads messages in a loop
    - sends back the same message with the first letter capitalised (capitalize)
    - stops when the client closes the connection or sends no further data
    """
    ip, port = client_address
    print(f"[THREAD START] Client {ip}:{port} connected")

    with client_socket:
        while True:
            # Wait until we receive up to 1024 bytes from the client.
            data = client_socket.recv(1024)

            # If data is an empty byte string (b""), the client has closed the connection.
            if not data:
                print(f"[DISCONNECT] Client {ip}:{port} closed the connection")
                break

            print(f"[RECV] From {ip}:{port} -> {data!r}")

            # Process the message: .capitalize() makes the first letter upper-case.
            response = data.capitalize()

            # Send the response back to the same client.
            client_socket.sendall(response)
            print(f"[SEND] To   {ip}:{port} -> {response!r}")

    # Remove the client from the list when the thread finishes.
    with clients_lock:
        if client_socket in clients:
            clients.remove(client_socket)

    print(f"[THREAD END] Client {ip}:{port} handler finished\n")


def accept_loop(server_socket):
    """
    Separate loop (in a thread or even in main) that:
    - accepts new connections
    - starts a handle_client thread for each client
    """

    print(f"[INFO] Server ready, listening on {HOST}:{PORT}")
    while is_running:
        # accept() blocks until a client connects.
        client_socket, client_address = server_socket.accept()

        ip, port = client_address
        print(f"[CONNECT] New client from {ip}:{port}")

        # Add the client to the global list.
        with clients_lock:
            clients.append(client_socket)
            print(f"[INFO] Currently connected clients: {len(clients)}")

        # Start a dedicated thread for this client.
        client_thread = threading.Thread(
            target=handle_client,
            args=(client_socket, client_address),
            daemon=True,  # daemon=True -> thread terminates when the process exits
        )
        client_thread.start()


def main():
    # Create a TCP (IPv4) socket.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Bind the socket to (HOST, PORT).
        server_socket.bind((HOST, PORT))

        # Put the server into "listening" mode.
        # Parameter (backlog) = number of pending connections.
        server_socket.listen(5)
        print(f"[START] TCP multi-client server on {HOST}:{PORT}")

        # Run the accept loop (could also be in a separate thread).
        accept_loop(server_socket)

    except KeyboardInterrupt:
        print("\n[INFO] KeyboardInterrupt received, shutting down server...")
    except BaseException as err:
        print(f"[ERROR] {err}")
    finally:
        # Close the server socket.
        server_socket.close()
        print("[STOP] Server socket closed")


if __name__ == '__main__':
    main()
