import socket
import threading
import pickle
import io

# Server IP address and port.
HOST = "127.0.0.1"
PORT = 3333

# Buffer size for recv().
BUFFER_SIZE = 8

# Global flag to allow stopping the loop (if desired).
is_running = True


class Response:
    """
    The response that the server sends back to the client.

    payload: any serialisable object (in this lab: string)
    """

    def __init__(self, payload):
        self.payload = payload


class Request:
    """
    The request that the client sends to the server.

    command: 'add', 'remove', 'get'
    key: text key
    resource: optional text value (used with 'add')
    """

    def __init__(self, command, key, resource=None):
        self.command = command
        self.key = key
        self.resource = resource


class State:
    """
    Global state, shared across all connections:

    resources: dict key -> resource
    lock: protects concurrent access
    """

    def __init__(self):
        self.resources = {}
        self.lock = threading.Lock()

    def add(self, key, resource):
        self.lock.acquire()
        self.resources[key] = resource
        self.lock.release()

    def remove(self, key):
        self.lock.acquire()
        self.resources.pop(key, None)
        self.lock.release()

    def get(self, key):
        if key in self.resources:
            return self.resources[key]
        else:
            return None


# Global state instance.
state = State()


def process_command(data: bytes) -> bytes:
    """
    Receives binary data representing ONE complete message:

        <LEN_BYTE> <PICKLED_REQUEST>

    Where:
      - LEN_BYTE: a single byte (0-255) holding the total message length,
                  including this first byte
      - PICKLED_REQUEST: the result of pickle.dump(Request(...))

    Steps:
      1. Ignore the first byte (len), keep the rest as payload.
      2. Deserialise the Request using pickle.
      3. Execute the logic on 'state'.
      4. Build a Response, serialise it with pickle.
      5. Frame the response in the same format:
            <LEN_BYTE> <PICKLED_RESPONSE>
    """

    # data[0] = LEN_BYTE, data[1:] = pickled payload.
    payload = data[1:]

    # Deserialise the Request from the payload.
    stream = io.BytesIO(payload)
    request: Request = pickle.load(stream)

    # Build the payload string for the response.
    payload_str = "command not recognized, doing nothing"

    if request.command == "add":
        state.add(request.key, request.resource)
        payload_str = f"{request.key} added"
    elif request.command == "remove":
        state.remove(request.key)
        payload_str = f"{request.key} removed"
    elif request.command == "get":
        value = state.get(request.key)
        if not value:
            payload_str = "key was not found"
        else:
            payload_str = value

    # Frame the response inside a Response object and serialise it.
    stream = io.BytesIO()
    pickle.dump(Response(payload_str), stream)
    serialized_payload = stream.getvalue()

    # Calculate the COMPLETE MESSAGE length (including LEN_BYTE).
    payload_length = len(serialized_payload) + 1

    # LEN_BYTE encoded as a single big-endian byte.
    len_byte = payload_length.to_bytes(1, byteorder="big")

    # Final message: LEN_BYTE + PICKLED_RESPONSE.
    return len_byte + serialized_payload


def handle_client(client: socket.socket):
    """
    Handler for a single client (runs in a separate thread).

    Steps:
      - read the first fragment of bytes
      - extract LEN_BYTE (first byte)
      - keep reading until LEN_BYTE bytes in total are collected
      - call process_command() and send the response
    """

    with client:
        while True:
            if client is None:
                break

            # First data fragment (max BUFFER_SIZE bytes).
            data = client.recv(BUFFER_SIZE)
            if not data:
                # The client has closed the connection.
                break

            # Store what has been received so far.
            full_data = data

            # The first byte contains the total message length.
            message_length = data[0]

            # How many more bytes do we need to read?
            remaining = message_length - len(full_data)

            # Keep reading until the entire message is available.
            while remaining > 0:
                chunk = client.recv(BUFFER_SIZE)
                if not chunk:
                    break
                full_data += chunk
                remaining -= len(chunk)

            # full_data should now represent a single complete message.
            response = process_command(full_data)

            # Send the response to the client.
            client.sendall(response)


def accept_loop(server: socket.socket):
    """
    Main loop: accepts new connections and starts a thread
    for each client.
    """

    while is_running:
        client, addr = server.accept()
        print(f"[CONNECT] {addr} has connected")
        client_thread = threading.Thread(target=handle_client, args=(client,))
        client_thread.start()


def main():
    server = None
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, PORT))
        server.listen()
        print(f"[START] Binary protocol TCP server on {HOST}:{PORT}")
        accept_loop(server)
    except BaseException as err:
        print(f"[ERROR] {err}")
    finally:
        if server:
            server.close()
        print("[STOP] Server closed")


if __name__ == "__main__":
    main()
