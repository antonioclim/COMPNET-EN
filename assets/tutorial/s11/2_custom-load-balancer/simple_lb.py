import socket
import threading

# -------------------------------------------------------------
# CONFIGURAȚIE LOAD BALANCER
# -------------------------------------------------------------

BACKENDS = [
    ("web1", 8000),
    ("web2", 8000),
    ("web3", 8000)
]

# variabilă globală pentru round-robin
backend_index = 0

HOST = "0.0.0.0"
PORT = 8080

BUFFER_SIZE = 4096


def get_next_backend():
    """
    Selectează backend-ul următor folosind algoritmul round-robin.
    Aici studentul are primul TODO.
    """
    global backend_index

    # TODO:
    #  - alege BACKENDS[backend_index]
    #  - incrementează backend_index circular
    #  - returnează backend-ul selectat

    backend = BACKENDS[backend_index]
    backend_index = (backend_index + 1) % len(BACKENDS)

    return backend


def forward_request_to_backend(request_data, backend_host, backend_port):
    """
    Trimite cererea brută către backend și întoarce răspunsul brut.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as backend_socket:
        backend_socket.connect((backend_host, backend_port))
        backend_socket.sendall(request_data)

        response = b""
        while True:
            chunk = backend_socket.recv(BUFFER_SIZE)
            if not chunk:
                break
            response += chunk

        return response


def handle_client_connection(client_socket, client_addr):
    """
    Se ocupă de un singur client.
    1. Citește cererea
    2. Alege backend-ul
    3. Trimite cererea către backend
    4. Retrimite răspunsul clientului
    """
    try:
        request_data = client_socket.recv(BUFFER_SIZE)

        if not request_data:
            client_socket.close()
            return

        # Alegem backend-ul
        backend_host, backend_port = get_next_backend()
        print(f"[INFO] {client_addr} → {backend_host}:{backend_port}")

        # Forward către backend
        backend_response = forward_request_to_backend(
            request_data,
            backend_host,
            backend_port
        )

        # Trimitem clientului
        client_socket.sendall(backend_response)

    except Exception as e:
        print("[ERROR]", e)
    finally:
        client_socket.close()


def main():
    """
    Pornim serverul load balancer:
    - ascultă pe 8080
    - pentru fiecare client creează un thread nou
    """
    print(f"[LB] Starting load balancer on port {PORT}...")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        print("[LB] Listening for clients...")

        while True:
            client_socket, client_addr = s.accept()
            print(f"[LB] Client connected: {client_addr}")

            thread = threading.Thread(
                target=handle_client_connection,
                args=(client_socket, client_addr)
            )
            thread.start()


if __name__ == "__main__":
    main()
