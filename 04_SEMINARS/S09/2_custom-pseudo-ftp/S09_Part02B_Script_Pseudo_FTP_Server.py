#!/usr/bin/env python3
"""Seminar 9 — local pseudo-FTP server: separate control and data connections.

Commands are LF-terminated UTF-8 lines. Replies use ASCII byte length, LF, payload.
Transfer replies are READY (active) or PORT n (passive), then exactly one done! or ERR.
Data frames keep the didactic one-byte content length (0..255 bytes). This is not FTP.
"""
import os
from pathlib import Path
import socket
import threading
from pseudo_ftp_io import read_line, send_reply, read_file, send_file, local_path

HOST = "127.0.0.1"
PORT = 3333
FILE_ROOT = str(Path(__file__).resolve().parent / "temp")
BUFFER_SIZE = 1024
is_running = True


def transfer(client, items, active, upload):
    expected = 3 if active else 2
    if len(items) != expected:
        raise ValueError("Expected command filename" + (" port" if active else ""))
    path = local_path(FILE_ROOT, items[1])
    content = None
    if not upload:
        content = path.read_bytes()
        if len(content) > 255:
            raise ValueError("File exceeds 255-byte teaching limit")
    if active:
        port = int(items[2])
        if not 1 <= port <= 65535:
            raise ValueError("Invalid data port")
        send_reply(client, "READY")
        with socket.create_connection((client.getpeername()[0], port), timeout=5) as data:
            if upload:
                path.write_bytes(read_file(data))
            else:
                send_file(data, content)
    else:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
            listener.bind((HOST, 0))
            listener.listen(1)
            listener.settimeout(5)
            send_reply(client, f"PORT {listener.getsockname()[1]}")
            data, address = listener.accept()
            with data:
                data.settimeout(5)
                if address[0] != client.getpeername()[0]:
                    raise ValueError("Data peer does not match the control peer")
                if upload:
                    path.write_bytes(read_file(data))
                else:
                    send_file(data, content)
    send_reply(client, "done!")


def active_get(client, command_items):
    transfer(client, command_items, active=True, upload=False)


def active_put(client, command_items):
    transfer(client, command_items, active=True, upload=True)


def passive_get(client, command_items):
    transfer(client, command_items, active=False, upload=False)


def passive_put(client, command_items):
    transfer(client, command_items, active=False, upload=True)


def process_list(client, command_items):
    return "\n".join(sorted(os.listdir(FILE_ROOT))) or "(empty directory)"


def process_help(client, command_items):
    return "list\nactive_get <filename>\nactive_put <filename>\npassive_get <filename>\npassive_put <filename>"


def process_command(client, request):
    try:
        items = request.decode("utf-8").strip().split()
        if not items:
            raise ValueError("Empty command")
        functions = {"active_get": active_get, "active_put": active_put,
                     "passive_get": passive_get, "passive_put": passive_put,
                     "list": process_list, "help": process_help}
        if items[0] not in functions:
            raise ValueError("Unknown command; try help")
        result = functions[items[0]](client, items)
        if result is not None:
            send_reply(client, result)
    except (OSError, ValueError, EOFError) as exc:
        send_reply(client, f"ERR {exc}")


def handle_client_commands(client):
    with client:
        try:
            while True:
                request = read_line(client)
                if request is None:
                    break
                process_command(client, request)
        except (OSError, ValueError, EOFError) as exc:
            print(f"[CONTROL CLOSED] {exc}")


def accept(server):
    while is_running:
        client, addr = server.accept()
        print(f"[SERVER] {addr} has connected")
        threading.Thread(target=handle_client_commands, args=(client,), daemon=True).start()


def main():
    Path(FILE_ROOT).mkdir(exist_ok=True)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()
        print(f"[SERVER] Pseudo-FTP server listening on {HOST}:{PORT}")
        try:
            accept(server)
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
