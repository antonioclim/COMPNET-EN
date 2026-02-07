#!/usr/bin/env python3
"""
Seminar 9 – Client pseudo-FTP pentru serverul nostru custom.

Rol:
 - se conecteaza la server pe conexiunea de control (HOST:PORT)
 - afiseaza un prompt "->"
 - interpreteaza comenzile:
      list
      active_get <filename>
      active_put <filename>
      passive_get <filename>
      passive_put <filename>
      help

Fisierele locale ale clientului sunt in LOCAL_STORAGE.
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

    Clientul:
      - porneste un server temporar pe un port liber
      - trimite comanda + portul catre server
      - accepta conexiunea de date de la server
      - primeste fisierul (length+data) si il salveaza in LOCAL_STORAGE
    """
    _, filename = command.strip().split(" ")

    os.makedirs(LOCAL_STORAGE, exist_ok=True)
    filepath = os.path.join(LOCAL_STORAGE, filename)

    with open(filepath, "wb") as f:
        temp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        temp_server.bind(("", 0))
        temp_server.listen()
        local_port = temp_server.getsockname()[1]

        # Trimitem comanda extinsa (cu port) pe conexiunea de control
        command_socket.sendall(f"{command} {local_port}".encode("utf-8"))

        # Serverul va trimite un mesaj de confirmare sau "done!", dar noi ne
        # bazam in principal pe conexiunea de date.
        # Optional, putem citi ce trimite serverul dupa transfer.

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

    Clientul:
      - citeste fisierul local LOCAL_STORAGE/filename
      - porneste un server temporar si anunta portul serverului
      - serverul se conecteaza si citeste datele
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

    Clientul:
      - trimite comanda pe conexiunea de control
      - primeste portul pe care serverul asculta
      - se conecteaza la acel port
      - primeste fisierul (length+data) si il salveaza
    """
    _, filename = command.strip().split(" ")

    os.makedirs(LOCAL_STORAGE, exist_ok=True)
    filepath = os.path.join(LOCAL_STORAGE, filename)

    # Cerem serverului un port temporar
    command_socket.sendall(command.strip().encode("utf-8"))
    data = command_socket.recv(1024)
    if not data:
        print("[CLIENT] no data (port) from server.")
        return

    host = command_socket.getpeername()[0]  # adresa serverului
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

    # Citim "done!" sau mesajul final (optional)
    ack = command_socket.recv(1024)
    if ack:
        print("[CLIENT] server:", ack.decode("utf-8").strip())
    print(f"[CLIENT] passive_get {filename} complete.")


def passive_put(command_socket, command: str):
    """
    passive_put <filename>

    Clientul:
      - citeste fisierul local
      - trimite comanda pe conexiunea de control
      - primeste portul serverului
      - se conecteaza si trimite fisierul (length+data)
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

    # Citim "done!" sau mesajul final (optional)
    ack = command_socket.recv(1024)
    if ack:
        print("[CLIENT] server:", ack.decode("utf-8").strip())
    print(f"[CLIENT] passive_put {filename} complete.")


def process_command(command_socket, command: str):
    """
    Decide ce functie de transfer sa apeleze in functie de comanda.
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
        # Comenzi simple (list, help, etc.) – doar trimitem comanda si afisam raspunsul
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
