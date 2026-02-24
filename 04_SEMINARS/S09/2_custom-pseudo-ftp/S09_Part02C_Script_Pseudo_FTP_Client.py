#!/usr/bin/env python3
"""
Seminar 9 -- Pseudo-FTP client for our custom server.

Role:
 - connects to the server on the control connection (HOST:PORT)
 - displays a "->" prompt
 - interprets the commands:
      list
      active_get <filename>
      active_put <filename>
      passive_get <filename>
      passive_put <filename>
      help

The client's local files are in LOCAL_STORAGE.
"""

import socket
import threading
import os

HOST = "127.0.0.1"
PORT = 3333

LOCAL_STORAGE = "./client-temp"
BUFFER_SIZE = 1024


def active_get(command_socket, command: str):
    """
    active_get <filename>

    The client:
      - starts a temporary server on a free port
      - sends the command + port to the server
      - accepts the data connection from the server
      - receives the file (length+data) and saves it to LOCAL_STORAGE
    """
    _, filename = command.strip().split(" ")

    os.makedirs(LOCAL_STORAGE, exist_ok=True)
    filepath = os.path.join(LOCAL_STORAGE, filename)

    with open(filepath, "wb") as f:
        temp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        temp_server.bind(("", 0))
        temp_server.listen()
        local_port = temp_server.getsockname()[1]

        # Send the extended command (with port) on the control connection
        command_socket.sendall(f"{command} {local_port}".encode("utf-8"))

        # The server will send a confirmation message or "done!", but we
        # rely primarily on the data connection.
        # Optionally, we can read what the server sends after the transfer.

        client, _ = temp_server.accept()
        with client:
            data = client.recv(BUFFER_SIZE)
            if not data:
                temp_server.close()
                return

            content_length = data[0]
            full_data = data[1:]

            if len(full_data) != content_length:
                print("[WARN] content_length vs data length mismatch (demo code).")

            f.write(full_data)

        temp_server.close()

    print(f"[CLIENT] active_get {filename} complete.")


def active_put(command_socket, command: str):
    """
    active_put <filename>

    The client:
      - reads the local file LOCAL_STORAGE/filename
      - starts a temporary server and announces the port to the server
      - the server connects and reads the data
    """
    _, filename = command.strip().split(" ")
    filepath = os.path.join(LOCAL_STORAGE, filename)

    if not os.path.isfile(filepath):
        print("[CLIENT] local file not found.")
        return

    with open(filepath, "rb") as f:
        content = f.read()
        content_size = len(content)

    temp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    temp_server.bind(("", 0))
    temp_server.listen()
    local_port = temp_server.getsockname()[1]

    command_socket.sendall(f"{command} {local_port}".encode("utf-8"))

    client, _ = temp_server.accept()
    with client:
        data = content_size.to_bytes(1, byteorder="big") + content
        client.sendall(data)

    temp_server.close()
    print(f"[CLIENT] active_put {filename} complete.")


def passive_get(command_socket, command: str):
    """
    passive_get <filename>

    The client:
      - sends the command on the control connection
      - receives the port on which the server listens
      - connects to that port
      - receives the file (length+data) and saves it
    """
    _, filename = command.strip().split(" ")

    os.makedirs(LOCAL_STORAGE, exist_ok=True)
    filepath = os.path.join(LOCAL_STORAGE, filename)

    # Ask the server for a temporary port
    command_socket.sendall(command.strip().encode("utf-8"))
    data = command_socket.recv(1024)
    if not data:
        print("[CLIENT] no data (port) from server.")
        return

    host = command_socket.getpeername()[0]  # server address
    port = int(data.strip())

    print(f"[CLIENT] passive_get connecting to {host}:{port}")

    with open(filepath, "wb") as f:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as file_socket:
            file_socket.connect((host, port))
            data = file_socket.recv(BUFFER_SIZE)
            if not data:
                return

            content_length = data[0]
            full_data = data[1:]

            if len(full_data) != content_length:
                print("[WARN] content_length vs data length mismatch (demo code).")

            f.write(full_data)

    # Read "done!" or the final message (optional)
    ack = command_socket.recv(1024)
    if ack:
        print("[CLIENT] server:", ack.decode("utf-8").strip())
    print(f"[CLIENT] passive_get {filename} complete.")


def passive_put(command_socket, command: str):
    """
    passive_put <filename>

    The client:
      - reads the local file
      - sends the command on the control connection
      - receives the server's port
      - connects and sends the file (length+data)
    """
    _, filename = command.strip().split(" ")
    filepath = os.path.join(LOCAL_STORAGE, filename)

    if not os.path.isfile(filepath):
        print("[CLIENT] local file not found.")
        return

    with open(filepath, "rb") as f:
        content = f.read()
        content_size = len(content)

    command_socket.sendall(command.strip().encode("utf-8"))
    data = command_socket.recv(1024)
    if not data:
        print("[CLIENT] no data (port) from server.")
        return

    host = command_socket.getpeername()[0]
    port = int(data.strip())

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as file_socket:
        file_socket.connect((host, port))
        file_socket.sendall(content_size.to_bytes(1, byteorder="big") + content)

    # Read "done!" or the final message (optional)
    ack = command_socket.recv(1024)
    if ack:
        print("[CLIENT] server:", ack.decode("utf-8").strip())
    print(f"[CLIENT] passive_put {filename} complete.")


def process_command(command_socket, command: str):
    """
    Decide which transfer function to call based on the command.
    """
    command_items = command.strip().split(" ")
    if not command_items:
        return

    cmd = command_items[0]

    if cmd == "active_get":
        temp_server_thread = threading.Thread(
            target=active_get, args=(command_socket, command)
        )
        temp_server_thread.start()
        temp_server_thread.join()

    elif cmd == "active_put":
        temp_server_thread = threading.Thread(
            target=active_put, args=(command_socket, command)
        )
        temp_server_thread.start()
        temp_server_thread.join()

    elif cmd == "passive_put":
        temp_client_thread = threading.Thread(
            target=passive_put, args=(command_socket, command)
        )
        temp_client_thread.start()
        temp_client_thread.join()

    elif cmd == "passive_get":
        temp_client_thread = threading.Thread(
            target=passive_get, args=(command_socket, command)
        )
        temp_client_thread.start()
        temp_client_thread.join()

    else:
        # Simple commands (list, help, etc.) — just send the command and display the response
        command_socket.sendall(command.strip().encode("utf-8"))
        data = command_socket.recv(4096)
        if data:
            print(data.decode("utf-8"))


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as command_socket:
        command_socket.connect((HOST, PORT))
        print(f"[CLIENT] Connected to pseudo-FTP server at {HOST}:{PORT}")
        print("Commands: list, help, active_get/put, passive_get/put, Ctrl+C to exit")

        while True:
            try:
                command = input("-> ")
            except EOFError:
                break

            if not command.strip():
                continue

            process_command(command_socket, command)


if __name__ == "__main__":
    main()
