import socket
import threading

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
        "20 add user1 Alice"

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

    # Calculate the payload length as a character count.
    payload_length = len(payload)

    # MESSAGE_LENGTH = total:
    #   len(str(payload_length)) + 1 (space) + payload_length,
    # NOTE: a different design was chosen here:
    # the response is sent as "MESSAGE_LENGTH PAYLOAD",
    # where MESSAGE_LENGTH represents the TOTAL length of the resulting string.
    #
    # Here we keep the existing convention:
    message_length = len(str(payload_length)) + 1 + payload_length

    # Final response: "<message_length> <payload>"
    return f"{message_length} {payload}"


def handle_client(client: socket.socket):
    """
    Handler for a single client (runs in a separate thread).

    Steps:
      - read the first data fragment (max BUFFER_SIZE bytes)
      - extract MESSAGE_LENGTH from the textual header
      - continue reading until the entire message is received
      - call process_command() and send the response
      - repeat until the client closes the connection
    """

    with client:
        while True:
            # If client is None (defensive) or no longer exists, exit.
            if client is None:
                break

            # Read the first fragment of the message.
            data = client.recv(BUFFER_SIZE)
            if not data:
                # The client has closed the connection.
                break

            # Convert bytes to string (UTF-8).
            string_data = data.decode("utf-8")
            full_data = string_data

            # The header has the form "<MESSAGE_LENGTH> ".
            # Take the first token and convert it to int.
            message_length = int(string_data.split(" ")[0])

            # How many more characters do we need to receive the full message?
            remaining = message_length - len(string_data)

            # As long as we do not have the entire message, keep reading.
            while remaining > 0:
                data = client.recv(BUFFER_SIZE)
                if not data:
                    break
                string_data = data.decode("utf-8")
                full_data += string_data
                remaining -= len(string_data)

            # At this point, full_data should contain the complete message.
            response = process_command(full_data)

            # Send the response, encoded in UTF-8.
            client.sendall(response.encode("utf-8"))


def accept_loop(server: socket.socket):
    """
    Main server loop:
    - accepts new connections
    - starts a handle_client thread for each one
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
