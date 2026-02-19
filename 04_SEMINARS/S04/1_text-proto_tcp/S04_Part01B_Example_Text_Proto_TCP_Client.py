import socket

# Address and port of the text protocol server.
HOST = "127.0.0.1"
PORT = 3333

# Buffer size used for recv().
BUFFER_SIZE = 8


def get_command(command: str) -> bytes:
    """
    Transforms a command line into the protocol format.

    Input (from user):
        command = "add user1 Alice"

    We want to send over TCP:
        "<TOTAL_LENGTH> <command>"

    where:
      TOTAL_LENGTH = len(command) + len(str(len(command))) + 1

    Explanation:
      - len(command) = number of characters in "add user1 Alice"
      - len(str(len(command))) = how many characters the length number has
        (e.g. len("15") = 2)
      - +1 = the space between TOTAL_LENGTH and command.
    """
    c = command.strip()
    content_length = len(c)
    total_length = content_length + len(str(content_length)) + 1
    frame = f"{total_length} {c}"
    return frame.encode("utf-8")


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Connect to the server.
        s.connect((HOST, PORT))
        print(f"[INFO] Connected to {HOST}:{PORT}")

        command = ""
        # Interactive command loop.
        while command.strip() != "exit":
            command = input("connected> ")

            # If the user just presses Enter, skip.
            if not command.strip():
                continue

            # Build the message in the protocol format.
            framed = get_command(command)

            # Send the message to the server.
            s.sendall(framed)

            # Read the response in chunks until the full message is received.
            data = s.recv(BUFFER_SIZE)
            if not data:
                print("[INFO] Server closed connection.")
                break

            string_data = data.decode("utf-8")
            full_data = string_data

            # First token is MESSAGE_LENGTH.
            message_length = int(string_data.split(" ")[0])
            remaining = message_length - len(string_data)

            while remaining > 0:
                data = s.recv(BUFFER_SIZE)
                if not data:
                    break
                string_data = data.decode("utf-8")
                full_data += string_data
                remaining -= len(string_data)

            # full_data has the form "<MESSAGE_LENGTH> <PAYLOAD>"
            # Display only the payload (the part after the first space).
            payload = " ".join(full_data.split(" ")[1:])
            print(payload)


if __name__ == "__main__":
    main()
