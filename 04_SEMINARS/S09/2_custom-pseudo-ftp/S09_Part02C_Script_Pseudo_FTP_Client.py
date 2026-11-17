#!/usr/bin/env python3
"""Seminar 9 — pseudo-FTP client for the supplied local server.

Each transfer consumes its initial response and final acknowledgement before
another command is issued. Files are limited to 255 bytes by the teaching format.
"""
from pathlib import Path
import socket
from pseudo_ftp_io import read_reply, read_file, send_file, local_path

HOST = "127.0.0.1"
PORT = 3333
LOCAL_STORAGE = str(Path(__file__).resolve().parent / "client-temp")
BUFFER_SIZE = 1024


def transfer(command_socket, command, active, upload):
    items = command.strip().split()
    if len(items) != 2:
        raise ValueError("Expected command filename")
    Path(LOCAL_STORAGE).mkdir(exist_ok=True)
    path = local_path(LOCAL_STORAGE, items[1])
    content = path.read_bytes() if upload else None
    if upload and len(content) > 255:
        raise ValueError("File exceeds the 255-byte teaching limit")
    if active:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
            listener.bind((HOST, 0))
            listener.listen(1)
            listener.settimeout(5)
            command_socket.sendall(f"{command.strip()} {listener.getsockname()[1]}\n".encode("utf-8"))
            initial = read_reply(command_socket)
            if initial != "READY":
                raise ValueError(initial)
            data, address = listener.accept()
            with data:
                data.settimeout(5)
                if address[0] != command_socket.getpeername()[0]:
                    raise ValueError("Unexpected data peer")
                if upload:
                    send_file(data, content)
                else:
                    path.write_bytes(read_file(data))
    else:
        command_socket.sendall((command.strip() + "\n").encode("utf-8"))
        initial = read_reply(command_socket)
        if not initial.startswith("PORT "):
            raise ValueError(initial)
        port = int(initial.split()[1])
        with socket.create_connection((command_socket.getpeername()[0], port), timeout=5) as data:
            if upload:
                send_file(data, content)
            else:
                path.write_bytes(read_file(data))
    acknowledgement = read_reply(command_socket)
    if acknowledgement != "done!":
        raise ValueError(acknowledgement)
    print(f"[CLIENT] {command.strip()} complete; server: {acknowledgement}")


def active_get(command_socket, command):
    transfer(command_socket, command, active=True, upload=False)


def active_put(command_socket, command):
    transfer(command_socket, command, active=True, upload=True)


def passive_get(command_socket, command):
    transfer(command_socket, command, active=False, upload=False)


def passive_put(command_socket, command):
    transfer(command_socket, command, active=False, upload=True)


def process_command(command_socket, command):
    items = command.strip().split()
    if not items:
        return
    functions = {"active_get": active_get, "active_put": active_put,
                 "passive_get": passive_get, "passive_put": passive_put}
    if items[0] in functions:
        functions[items[0]](command_socket, command)
    else:
        command_socket.sendall((command.strip() + "\n").encode("utf-8"))
        print(read_reply(command_socket))


def main():
    with socket.create_connection((HOST, PORT), timeout=10) as command_socket:
        print(f"[CLIENT] Connected to {HOST}:{PORT}; type help or exit")
        while True:
            try:
                command = input("-> ").strip()
                if command == "exit":
                    break
                process_command(command_socket, command)
            except (EOFError, KeyboardInterrupt):
                break
            except (OSError, ValueError) as exc:
                print(f"[ERROR] {exc}; reconnect before issuing another command")
                break


if __name__ == "__main__":
    main()
