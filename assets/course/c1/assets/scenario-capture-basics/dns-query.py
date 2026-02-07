import socket

def main():
    # Interogare simpla (nu implementam DNS aici)
    # Doar fortam rezolvare pentru a genera trafic DNS in sistem
    host = "example.com"
    print("Resolving:", host)
    ip = socket.gethostbyname(host)
    print("Result:", ip)

if __name__ == "__main__":
    main()
