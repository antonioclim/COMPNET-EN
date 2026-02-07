from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

def main():
    authorizer = DummyAuthorizer()
    authorizer.add_user("student", "student", "/data", perm="elradfmwMT")
    authorizer.add_anonymous("/data", perm="elr")

    handler = FTPHandler
    handler.authorizer = authorizer

    # Ascultam pe 2121 in container (mapat extern pe 2121)
    handler.passive_ports = range(30000, 30010)

    address = ("0.0.0.0", 2121)
    server = FTPServer(address, handler)
    print("FTP server on", address)
    server.serve_forever()

if __name__ == "__main__":
    main()
