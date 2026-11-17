import os

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

def main():
    authorizer = DummyAuthorizer()
    authorizer.add_user("student", "student", "/data", perm="elradfmwMT")
    authorizer.add_anonymous("/data", perm="elr")

    handler = FTPHandler
    handler.authorizer = authorizer

    # PASV advertises the reachable client-side address of the DNAT firewall.
    handler.masquerade_address = os.environ.get("FTP_MASQUERADE_ADDRESS")
    # Active PORT/EPRT targets are still checked against the control peer.
    handler.passive_ports = range(30000, 30010)

    address = ("0.0.0.0", 2121)
    server = FTPServer(address, handler)
    print("FTP server on", address)
    server.serve_forever()

if __name__ == "__main__":
    main()
