import socket
import threading

# -------------------------------------------------------------
# LOAD BALANCER CONFIGURATION
# -------------------------------------------------------------

BACKENDS = [
    ("web1", 8000),
    ("web2", 8000),
    ("web3", 8000)
]

# global variable for round-robin
backend_index = 0

HOST = "0.0.0.0"
PORT = 8080

BUFFER_SIZE = 4096


def get_next_backend():
    """
    Select the next backend using the round-robin algorithm.

    This is the first TODO for students.
    """
    global backend_index

    # TODO:
    #  - choose BACKENDS[backend_index]
    #  - increment backend_index circularly
    #  - return the selected backend

    backend = BACKENDS[backend_index]
    backend_index = (backend_index + 1) % len(BACKENDS)

    return backend


def forward_request_to_backend(request_data, backend_host, backend_port):
    """
    Send the raw request to the backend and return the raw response.
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
    Handle a single client connection.

    1. Read the request
    2. Choose a backend
    3. Forward the request to the backend
    4. Relay the response back to the client
    """
    try:
        request_data = client_socket.recv(BUFFER_SIZE)

        if not request_data:
            client_socket.close()
            return

        # Choose the backend
        backend_host, backend_port = get_next_backend()
        print(f"[INFO] {client_addr} -> {backend_host}:{backend_port}")

        # Forward to the backend
        backend_response = forward_request_to_backend(
            request_data,
            backend_host,
            backend_port
        )

        # Send back to the client
        client_socket.sendall(backend_response)

    except Exception as e:
        print("[ERROR]", e)
    finally:
        client_socket.close()


def main():
    """
    Start the load balancer server:
    - listen on port 8080
    - create a new thread for each client
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
