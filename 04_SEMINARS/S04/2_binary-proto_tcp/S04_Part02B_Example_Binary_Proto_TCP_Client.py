import socket
import pickle
import io

HOST = "127.0.0.1"
PORT = 3333
BUFFER_SIZE = 8


class Response:
    """
    The same class must be defined as on the server so that pickle
    can correctly deserialise the Response object.
    """

    def __init__(self, payload):
        self.payload = payload


class Request:
    """
    Same as on the server: command, key, resource.
    """

    def __init__(self, command, key, resource=None):
        self.command = command
        self.key = key
        self.resource = resource


def get_command(command: str) -> bytes:
    """
    Transforms a user input line into a binary message
    conforming to the protocol:

        <LEN_BYTE> <PICKLED_REQUEST>

    Steps:
      1. Parse the line: command key [resource...]
      2. Build a Request(command, key, resource)
      3. Serialise the Request with pickle into BytesIO.
      4. Calculate payload_length = len(serialized_payload) + 1
         (1 for LEN_BYTE).
      5. Return: LEN_BYTE + serialized_payload
    """

    c = command.strip()
    items = c.split(" ")

    # We expect at least command and key.
    if len(items) < 2:
        raise ValueError("Command must have at least: <command> <key>")

    cmd = items[0]
    key = items[1]
    resource = " ".join(items[2:]) if len(items) > 2 else None

    request = Request(cmd, key, resource)

    # Serialise the Request.
    stream = io.BytesIO()
    pickle.dump(request, stream)
    serialized_payload = stream.getvalue()

    # Total message length (including LEN_BYTE).
    payload_length = len(serialized_payload) + 1

    # LEN_BYTE encoded as a single byte.
    len_byte = payload_length.to_bytes(1, byteorder="big")

    return len_byte + serialized_payload


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"[INFO] Connected to {HOST}:{PORT}")

        command = ""
        while command.strip() != "exit":
            command = input("connected(binaries)> ")

            if not command.strip():
                continue

            try:
                message = get_command(command)
            except ValueError as ve:
                print(f"[ERROR] {ve}")
                continue

            # Send the serialised message.
            s.sendall(message)

            # Read the first response fragment.
            data = s.recv(BUFFER_SIZE)
            if not data:
                print("[INFO] Server closed connection.")
                break

            full_data = data
            message_length = data[0]  # LEN_BYTE

            remaining = message_length - len(full_data)
            while remaining > 0:
                chunk = s.recv(BUFFER_SIZE)
                if not chunk:
                    break
                full_data += chunk
                remaining -= len(chunk)

            # full_data = LEN_BYTE + PICKLED_RESPONSE
            response_payload = full_data[1:]  # ignore LEN_BYTE
            stream = io.BytesIO(response_payload)
            response: Response = pickle.load(stream)
            print(response.payload)


if __name__ == "__main__":
    main()
