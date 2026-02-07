import socket
import threading

# Adresa IP pe care va asculta serverul.
# "127.0.0.1" = localhost (doar conexiuni de pe aceeași mașină).
HOST = "127.0.0.1"

# Portul pe care va asculta serverul.
PORT = 3333

# Dimensiunea buffer-ului pentru fiecare apel recv().
# Serverul va citi mesajul în bucăți de maximum BUFFER_SIZE bytes.
BUFFER_SIZE = 8

is_running = True


class State:
    """
    Structură foarte simplă de stocare (în memorie).

    - resources: dicționar key -> resource (string)
    - lock: protejează accesul concurent (thread-uri multiple de clienți)
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


# Instanța globală de stare partajată între toți clienții.
state = State()


def process_command(data: str) -> str:
    """
    Primește comanda completă ca string (inclusiv header-ul de lungime),
    aplică operația asupra 'state' și întoarce răspunsul ca string
    *deja împachetat* cu lungime la început.

    Format mesaj primit:
        "<MESSAGE_LENGTH> <COMMAND> <KEY> [RESOURCE...]"

    Exemplu:
        "20 add user1 Alice"

    Pași:
      1. Parsăm comanda și argumentele.
      2. Executăm add/remove/get pe 'state'.
      3. Construim payload-ul (textul util).
      4. Împachetăm payload-ul ca:
           "<MESSAGE_LENGTH> <PAYLOAD>"

         unde MESSAGE_LENGTH este lungimea totală a acestui răspuns,
         incluzând cifrele lui MESSAGE_LENGTH, spațiul și payload-ul.
    """

    # Spargem după spațiu. items[0] = MESSAGE_LENGTH (header).
    items = data.split(" ")

    # items[1] = command, items[2] = key.
    # Restul elementelor formează resource (dacă există).
    command, key = items[1:3]

    resource = ""
    if len(items) > 3:
        resource = " ".join(items[3:])

    # payload = doar conținutul util (fără lungime).
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

    # Calculăm lungimea payload-ului ca număr de caractere.
    payload_length = len(payload)

    # MESSAGE_LENGTH = totalul:
    #   len(str(payload_length)) + 1 (spațiu) + payload_length,
    # DAR atenție: aici s-a ales un alt design:
    # se trimite ca "MESSAGE_LENGTH PAYLOAD",
    # iar MESSAGE_LENGTH reprezintă lungimea TOTALĂ a stringului rezultat.
    #
    # Aici ținem convenția existentă:
    message_length = len(str(payload_length)) + 1 + payload_length

    # Răspunsul final: "<message_length> <payload>"
    return f"{message_length} {payload}"


def handle_client(client: socket.socket):
    """
    Handler pentru un singur client (rulat într-un thread separat).

    Pași:
      - citim primul fragment de date (max BUFFER_SIZE bytes)
      - extragem MESSAGE_LENGTH din header-ul textual
      - continuăm să citim până avem tot mesajul
      - apelăm process_command() și trimitem răspunsul
      - repetăm până când clientul închide conexiunea
    """

    with client:
        while True:
            # Dacă client este None (defensiv) sau nu mai există, ieșim.
            if client is None:
                break

            # Citim primul fragment din mesaj.
            data = client.recv(BUFFER_SIZE)
            if not data:
                # Clientul a închis conexiunea.
                break

            # Convertim bytes în string (UTF-8).
            string_data = data.decode("utf-8")
            full_data = string_data

            # Header-ul are forma "<MESSAGE_LENGTH> ".
            # Luăm primul token și îl transformăm în int.
            message_length = int(string_data.split(" ")[0])

            # Câte caractere mai trebuie să primim pentru a avea tot mesajul?
            remaining = message_length - len(string_data)

            # Atâta timp cât nu avem întregul mesaj, continuăm să citim.
            while remaining > 0:
                data = client.recv(BUFFER_SIZE)
                if not data:
                    break
                string_data = data.decode("utf-8")
                full_data += string_data
                remaining -= len(string_data)

            # La acest punct, full_data ar trebui să conțină mesajul complet.
            response = process_command(full_data)

            # Trimitem răspunsul, codificat în UTF-8.
            client.sendall(response.encode("utf-8"))


def accept_loop(server: socket.socket):
    """
    Buclă principală a serverului:
    - acceptă conexiuni noi
    - pornește un thread handle_client pentru fiecare
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
