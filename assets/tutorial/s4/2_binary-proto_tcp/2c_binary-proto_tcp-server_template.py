import socket
import threading
import pickle
import io

HOST = "127.0.0.1"
PORT = 3333
BUFFER_SIZE = 8

is_running = True


class Response:
    def __init__(self, payload):
        self.payload = payload


class Request:
    def __init__(self, command, key, resource=None):
        self.command = command
        self.key = key
        self.resource = resource


class State:
    """
    Stare globală simplă: key -> resource (string).
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

    Adăugați o metodă keys_list() care întoarce lista cheilor stocate,
    de exemplu ca listă de string-uri.
    """
    # <<< STUDENT CODE ENDS HERE


state = State()


def build_response(payload_str: str) -> bytes:
    """
    Construiți un mesaj binar complet:

      <LEN_BYTE> <PICKLED_RESPONSE>

    bazat pe payload_str (string).
    """
    # Serializăm un obiect Response(payload_str).
    stream = io.BytesIO()
    pickle.dump(Response(payload_str), stream)
    serialized_payload = stream.getvalue()

    payload_length = len(serialized_payload) + 1
    len_byte = payload_length.to_bytes(1, byteorder="big")
    return len_byte + serialized_payload


def process_command(data: bytes) -> bytes:
    """
    TODO (student):

    1. Ignorați primul octet (LEN_BYTE) și deserializați Request din rest.
    2. Implementați comenzi:
       - add / remove / get (ca în exemplu)
       - keys
         * întoarce lista tuturor cheilor stocate într-un string, de forma:
           "k1, k2, k3" sau "no keys" dacă nu avem nimic.

    3. Pentru comenzi necunoscute:
       - payload: "command not recognized, doing nothing"

    4. Întoarceți rezultatul folosind build_response(payload_str).
    """

    # >>> STUDENT CODE STARTS HERE

    # 1. Deserializăm Request.
    payload = data[1:]
    stream = io.BytesIO(payload)
    request: Request = pickle.load(stream)

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
    elif request.command == "keys":
        # TODO (student): înlocuiți cu implementarea dorită
        # (e.g. folosind state.resources.keys()).
        # De exemplu:
        #   keys = list(state.resources.keys())
        #   payload_str = ", ".join(keys) if keys else "no keys"
        payload_str = "TODO: implement keys command"

    # 4. Împachetăm răspunsul.
    return build_response(payload_str)

    # <<< STUDENT CODE ENDS HERE


def handle_client(client: socket.socket):
    with client:
        while True:
            if client is None:
                break

            data = client.recv(BUFFER_SIZE)
            if not data:
                break

            full_data = data
            message_length = data[0]  # LEN_BYTE

            remaining = message_length - len(full_data)
            while remaining > 0:
                chunk = client.recv(BUFFER_SIZE)
                if not chunk:
                    break
                full_data += chunk
                remaining -= len(chunk)

            response = process_command(full_data)
            client.sendall(response)


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
        print(f"[START] Binary protocol TCP server (template) on {HOST}:{PORT}")
        accept_loop(server)
    except BaseException as err:
        print(f"[ERROR] {err}")
    finally:
        if server:
            server.close()
        print("[STOP] Server closed")


if __name__ == "__main__":
    main()
