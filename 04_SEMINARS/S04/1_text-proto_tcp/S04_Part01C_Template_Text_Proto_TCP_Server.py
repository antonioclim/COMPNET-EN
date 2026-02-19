import socket
import threading

HOST = "127.0.0.1"
PORT = 3333
BUFFER_SIZE = 8

is_running = True


class State:
    """
    Simple key -> resource storage, protected by a lock.
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

    # >>> STUDENT CODE STARTS HERE (optional)
    """
    TODO (student, optional):

    Add a count() method that returns the number of stored keys.
    Example:
        def count(self):
            return len(self.resources)
    """
    # <<< STUDENT CODE ENDS HERE


state = State()


def build_framed_response(payload: str) -> str:
    """
    Build a response with a length header, in the form:
        "<MESSAGE_LENGTH> <PAYLOAD>"
    """
    payload_length = len(payload)
    message_length = len(str(payload_length)) + 1 + payload_length
    return f"{message_length} {payload}"


def process_command(data: str) -> str:
    """
    TODO (student):

    1. Parse the command similarly to the example:
       - data = "<MESSAGE_LENGTH> <COMMAND> <KEY> [RESOURCE...]"
       - split on space and extract command and key.
       - the rest is resource (if present).

    2. Implement the following commands:
       - add <key> <value...>
       - remove <key>
       - get <key>
       - count
         * does not require key or resource
         * response: "<number_of_keys> keys"

    3. For unrecognised commands or invalid format:
       - response: "ERR unknown command"

    4. Return the result framed with build_framed_response().

    Hint:
    - use try/except to catch IndexError if arguments are missing.
    """

    # >>> STUDENT CODE STARTS HERE

    items = data.split(" ")

    # items[0] = MESSAGE_LENGTH
    if len(items) < 2:
        # Invalid message: we do not even have a command.
        payload = "ERR invalid message"
        return build_framed_response(payload)

    command = items[1]

    # Prepare default values.
    key = None
    resource = ""

    if command in ("add", "remove", "get"):
        if len(items) < 3:
            payload = "ERR missing key"
            return build_framed_response(payload)
        key = items[2]
        if command == "add" and len(items) > 3:
            resource = " ".join(items[3:])

    # Basic command implementation (the student may adjust/add count):

    if command == "add":
        state.add(key, resource)
        payload = f"{key} added"
    elif command == "remove":
        state.remove(key)
        payload = f"{key} removed"
    elif command == "get":
        value = state.get(key)
        if not value:
            payload = "key was not found"
        else:
            payload = value
    elif command == "count":
        # TODO (student): replace with a call to state.count()
        # and build the payload in the form "<n> keys"
        payload = "TODO: implement count command"
    else:
        payload = "ERR unknown command"

    return build_framed_response(payload)

    # <<< STUDENT CODE ENDS HERE


def handle_client(client: socket.socket):
    with client:
        while True:
            if client is None:
                break

            data = client.recv(BUFFER_SIZE)
            if not data:
                break

            string_data = data.decode("utf-8")
            full_data = string_data

            try:
                message_length = int(string_data.split(" ")[0])
            except ValueError:
                # Invalid header -> send error and close.
                error_response = build_framed_response("ERR invalid length header")
                client.sendall(error_response.encode("utf-8"))
                break

            remaining = message_length - len(string_data)

            while remaining > 0:
                data = client.recv(BUFFER_SIZE)
                if not data:
                    break
                string_data = data.decode("utf-8")
                full_data += string_data
                remaining -= len(string_data)

            response = process_command(full_data)
            client.sendall(response.encode("utf-8"))


def accept_loop(server: socket.socket):
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
        print(f"[START] Text protocol TCP server (template) on {HOST}:{PORT}")
        accept_loop(server)
    except BaseException as err:
        print(f"[ERROR] {err}")
    finally:
        if server:
            server.close()
        print("[STOP] Server closed")


if __name__ == "__main__":
    main()
