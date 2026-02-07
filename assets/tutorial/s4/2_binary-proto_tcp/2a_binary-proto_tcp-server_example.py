import socket
import threading
import pickle
import io

# Adresa IP și portul serverului.
HOST = "127.0.0.1"
PORT = 3333

# Dimensiunea buffer-ului pentru recv().
BUFFER_SIZE = 8

# Flag global pentru a putea opri bucla (dacă vrem).
is_running = True


class Response:
    """
    Răspunsul pe care serverul îl trimite înapoi clientului.

    payload: orice obiect serializabil (în laborator: string)
    """

    def __init__(self, payload):
        self.payload = payload


class Request:
    """
    Cererea pe care clientul o trimite serverului.

    command: 'add', 'remove', 'get'
    key: cheie text
    resource: valoare text, opțională (folosită la 'add')
    """

    def __init__(self, command, key, resource=None):
        self.command = command
        self.key = key
        self.resource = resource


class State:
    """
    Stare globală, partajată între toate conexiunile:

    resources: dict key -> resource
    lock: protejează accesul concurent
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


# Instanța globală de stare.
state = State()


def process_command(data: bytes) -> bytes:
    """
    Primește date binare care reprezintă UN mesaj complet:

        <LEN_BYTE> <PICKLED_REQUEST>

    Unde:
      - LEN_BYTE: un octet (0-255) cu lungimea întregului mesaj,
                  inclusiv acest prim octet
      - PICKLED_REQUEST: rezultatul pickle.dump(Request(...))

    Pași:
      1. Ignorăm primul byte (len), păstrăm restul ca payload.
      2. Deserializăm Request folosind pickle.
      3. Executăm logica pe 'state'.
      4. Construim un Response, îl serializăm cu pickle.
      5. Împachetăm răspunsul în același format:
            <LEN_BYTE> <PICKLED_RESPONSE>
    """

    # data[0] = LEN_BYTE, data[1:] = payload pickled.
    payload = data[1:]

    # Deserializăm Request din payload.
    stream = io.BytesIO(payload)
    request: Request = pickle.load(stream)

    # Construim payload-ul (string) pentru răspuns.
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

    # Împachetăm răspunsul într-un obiect Response și îl serializăm.
    stream = io.BytesIO()
    pickle.dump(Response(payload_str), stream)
    serialized_payload = stream.getvalue()

    # Calculăm lungimea MESAJULUI COMPLET (inclusiv LEN_BYTE).
    payload_length = len(serialized_payload) + 1

    # LEN_BYTE codificat pe 1 octet big-endian.
    len_byte = payload_length.to_bytes(1, byteorder="big")

    # Mesaj final: LEN_BYTE + PICKLED_RESPONSE.
    return len_byte + serialized_payload


def handle_client(client: socket.socket):
    """
    Handler pentru un singur client (rulat într-un thread separat).

    Pași:
      - citim primul fragment de bytes
      - extragem LEN_BYTE (primul octet)
      - citim până ajungem la LEN_BYTE bytes în total
      - chemăm process_command() și trimitem răspunsul
    """

    with client:
        while True:
            if client is None:
                break

            # Primul fragment de date (max BUFFER_SIZE bytes).
            data = client.recv(BUFFER_SIZE)
            if not data:
                # Clientul a închis conexiunea.
                break

            # Stocăm ce am primit până acum.
            full_data = data

            # Primul byte conține lungimea mesajului complet.
            message_length = data[0]

            # Câți bytes mai trebuie să citim?
            remaining = message_length - len(full_data)

            # Continuăm să citim până avem întregul mesaj.
            while remaining > 0:
                chunk = client.recv(BUFFER_SIZE)
                if not chunk:
                    break
                full_data += chunk
                remaining -= len(chunk)

            # full_data ar trebui să reprezinte un singur mesaj complet.
            response = process_command(full_data)

            # Trimitem răspunsul către client.
            client.sendall(response)


def accept_loop(server: socket.socket):
    """
    Bucla principală: acceptă conexiuni noi și pornește câte un thread
    pentru fiecare client.
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
