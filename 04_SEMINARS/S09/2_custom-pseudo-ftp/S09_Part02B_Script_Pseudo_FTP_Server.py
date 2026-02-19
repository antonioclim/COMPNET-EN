#!/usr/bin/env python3
"""
Seminar 9 -- Pseudo-FTP server (control + data, active/passive mode).

Protocol:
  - control connection on HOST:PORT
  - text commands:
      list
      active_get <filename>
      active_put <filename>
      passive_get <filename>
      passive_put <filename>

  - temporary TCP connections are used for file transfer
    (similar to FTP, in active and passive mode).

NOTE:
  - the protocol is demonstrative; it is not robust for large files
  - file length is encoded on 1 byte (max ~255 bytes)
"""

import socket
import threading
import os

HOST = "127.0.0.1"
PORT = 3333

FILE_ROOT = "./temp"
BUFFER_SIZE = 1024
is_running = True


def process_command(client, request: bytes):
    """
    Decode the command line and call the corresponding function.

    client: the control connection socket
    request: bytes, e.g. b"list\n" or b"active_get a.txt 4000\n"
    """
    command_items = request.decode("utf-8").strip().split(" ")

    command_mappings = {
        "list": process_list,
        "active_get": active_get,
        "active_put": active_put,
        "passive_get": passive_get,
        "passive_put": passive_put,
        "help": process_help,
    }

    if not command_items:
        return

    command = command_items[0]
    if command in command_mappings:
        result = command_mappings[command](client, command_items)
        # If the function returns a text response, send it on the control connection
        if isinstance(result, str):
            client.sendall(result.encode("utf-8"))
        elif isinstance(result, bytes):
            client.sendall(result)
    else:
        client.sendall(b"Unknown command. Try 'help'.\n")


def process_help(client, command_items):
    """
    Return a message listing the supported commands.
    Students may extend / modify the text.
    """
    return (
        "Available commands:\n"
        "  list\n"
        "  active_get <filename>\n"
        "  active_put <filename>\n"
        "  passive_get <filename>\n"
        "  passive_put <filename>\n"
    )


def process_list(client, command_items):
    """
    List the files available in the FILE_ROOT directory.
    The response is sent on the control connection (text).
    """
    try:
        files = os.listdir(FILE_ROOT)
        return "\n".join(files) + "\n"
    except FileNotFoundError:
        return "FILE_ROOT not found.\n"


def active_get(client, command_items):
    """
    active_get <filename> <port>

    - the client listens on a temporary port
    - the server (here) connects to the client on that port
    - the server sends the file content (length+data)
    """
    if len(command_items) < 3:
        client.sendall(b"not enough params\n")
        return

    _, filename, port = command_items
    filepath = os.path.join(FILE_ROOT, filename)

    if not os.path.isfile(filepath):
        client.sendall(b"file not found\n")
        return

    with open(filepath, "rb") as f:
        content = f.read()
        content_size = len(content)

    host = client.getpeername()[0]
    port = int(port)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as file_socket:
        print(f"[SERVER] active_get transfer to {host}:{port}")
        file_socket.connect((host, port))
        # 1 byte for length (DEMO: max 255)
        data = content_size.to_bytes(1, byteorder="big") + content
        file_socket.sendall(data)

    client.sendall(b"done!\n")


def active_put(client, command_items):
    """
    active_put <filename> <port>

    - the client listens on a temporary port
    - the server connects to the client on that port
    - the server receives the data and saves it to FILE_ROOT/filename
    """
    if len(command_items) < 3:
        client.sendall(b"not enough params\n")
        return

    _, filename, port = command_items
    filepath = os.path.join(FILE_ROOT, filename)

    host = client.getpeername()[0]
    port = int(port)

    with open(filepath, "wb") as f:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as file_socket:
            print(f"[SERVER] active_put receiving from {host}:{port}")
            file_socket.connect((host, port))
            data = file_socket.recv(BUFFER_SIZE)
            if not data:
                client.sendall(b"no data received\n")
                return

            # First byte = length; remainder = content
            content_length = data[0]
            full_data = data[1:]

            # For simplicity we assume everything arrives in a single recv
            # (not robust for real production).
            if len(full_data) != content_length:
                print("[WARN] content_length vs data length mismatch (demo code).")

            f.write(full_data)

    client.sendall(b"done!\n")


def passive_put(client, command_items):
    """
    passive_put <filename>

    - the server listens on a temporary port
    - sends the port to the client on the control connection
    - the client connects and sends the file content
    """
    if len(command_items) < 2:
        client.sendall(b"not enough params\n")
        return

    _, filename = command_items
    filepath = os.path.join(FILE_ROOT, filename)

    with open(filepath, "wb") as f:
        temp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        temp_server.bind(("", 0))
        temp_server.listen()
        local_port = temp_server.getsockname()[1]

        # Send the port in plain text on the control connection
        client.sendall(str(local_port).encode("utf-8"))

        temp_client, _ = temp_server.accept()
        with temp_client:
            data = temp_client.recv(BUFFER_SIZE)
            if not data:
                temp_server.close()
                return

            content_length = data[0]
            full_data = data[1:]

            # As in active_put, we assume everything in a single recv
            if len(full_data) != content_length:
                print("[WARN] content_length vs data length mismatch (demo code).")

            f.write(full_data)

        temp_server.close()

    client.sendall(b"done!\n")


def passive_get(client, command_items):
    """
    passive_get <filename>

    - the server listens on a temporary port
    - sends the port to the client
    - the client connects and receives the file content
    """
    if len(command_items) < 2:
        client.sendall(b"not enough params\n")
        return

    _, filename = command_items
    filepath = os.path.join(FILE_ROOT, filename)

    if not os.path.isfile(filepath):
        client.sendall(b"file not found\n")
        return

    with open(filepath, "rb") as f:
        content = f.read()
        content_size = len(content)

    temp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    temp_server.bind(("", 0))
    temp_server.listen()
    local_port = temp_server.getsockname()[1]

    print(f"[SERVER] passive_get listening on port {local_port}")
    client.sendall(str(local_port).encode("utf-8"))

    temp_client, _ = temp_server.accept()
    with temp_client:
        data = content_size.to_bytes(1, byteorder="big") + content
        temp_client.sendall(data)

    temp_server.close()
    client.sendall(b"done!\n")


def handle_client_commands(client):
    """
    Control thread for each connected client.
    """
    with client:
        while True:
            request = client.recv(1024)
            if not request:
                break
            process_command(client, request)


def accept(server):
    """
    Accept control connections and start a thread for each client.
    """
    while is_running:
        client, addr = server.accept()
        print(f"[SERVER] {addr} has connected")
        command_thread = threading.Thread(
            target=handle_client_commands, args=(client,)
        )
        command_thread.start()


def main():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, PORT))
        server.listen()
        print(f"[SERVER] Pseudo-FTP server listening on {HOST}:{PORT}")
        accept_thread = threading.Thread(target=accept, args=(server,))
        accept_thread.start()
        accept_thread.join()
    except BaseException as err:
        print(err)
    finally:
        if server:
            server.close()


if __name__ == "__main__":
    main()
