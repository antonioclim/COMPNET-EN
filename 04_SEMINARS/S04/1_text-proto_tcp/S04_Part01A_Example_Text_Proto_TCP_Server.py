import socket
import threading
from text_framing import encode_frame, read_frame

# IP address on which the server will listen.
# "127.0.0.1" = localhost (only connections from the same machine).
HOST = "127.0.0.1"

# Port on which the server will listen.
PORT = 3333

# Buffer size for each recv() call.
# The server will read the message in chunks of at most BUFFER_SIZE bytes.
BUFFER_SIZE = 8

is_running = True


class State:
    """
    Very simple in-memory storage structure.

    - resources: dictionary key -> resource (string)
    - lock: protects concurrent access (multiple client threads)
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


# Global state instance shared across all clients.
state = State()


def process_command(data: str) -> str:
    """
    Receives the complete command as a string (including the length header),
    applies the operation on 'state' and returns the response as a string
    *already framed* with the length prefix.

    Incoming message format:
        "<MESSAGE_LENGTH> <COMMAND> <KEY> [RESOURCE...]"

    Example:
        "18 add user1 Alice"

    Steps:
      1. Parse the command and arguments.
      2. Execute add/remove/get on 'state'.
      3. Build the payload (useful text).
      4. Frame the payload as:
           "<MESSAGE_LENGTH> <PAYLOAD>"

         where MESSAGE_LENGTH is the total length of this response,
         including the digits of MESSAGE_LENGTH, the space and the payload.
    """

    # Split on space. items[0] = MESSAGE_LENGTH (header).
    items = data.split(" ")

    # items[1] = command, items[2] = key.
    # The remaining elements form the resource (if present).
    if len(items) < 3:
        return encode_frame("ERR missing command or key").decode("utf-8")
    command, key = items[1:3]

    resource = ""
    if len(items) > 3:
        resource = " ".join(items[3:])

    # payload = only the useful content (without the length).
    payload = "command not recognized, doing nothing"

    if command == "add":
        state.add(key, resource)
        payload = f"{key} added"
    elif command == "remove":
        state.remove(key)
        payload = f"{key} removed"
    elif command == "get":
        payload = state.get(key)
        if not payload:
            payload = "key was not found"

    return encode_frame(payload).decode("utf-8")


def handle_client(client: socket.socket):
    """Read complete frames as bytes, then decode once; accept pipelined frames."""
    with client:
        try:
            while True:
                frame = read_frame(client)
                if frame is None:
                    break
                response = process_command(frame.decode("utf-8"))
                client.sendall(response.encode("utf-8"))
        except (OSError, EOFError, ValueError) as exc:
            print(f"[PROTOCOL ERROR] {exc}")



def accept_loop(server: socket.socket):
    """
    Main server loop:
    - accepts new connections
    - starts a handle_client thread for each one
    """

    while is_running:
        client, addr = server.accept()
        print(f"[CONNECT] {addr} has connected")
        client_thread = threading.Thread(target=handle_client, args=(client,), daemon=True)
        client_thread.start()


def main():
    server = None
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, PORT))
        server.listen()

        print(f"[START] Text protocol TCP server on {HOST}:{PORT}")
        accept_loop(server)
    except BaseException as err:
        print(f"[ERROR] {err}")
    finally:
        if server:
            server.close()
        print("[STOP] Server closed")


if __name__ == "__main__":
    main()
